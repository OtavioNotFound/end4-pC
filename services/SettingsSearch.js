.pragma library

// Shared by dashboard and launcher. No filesystem, Config writes or host APIs.
function normalize(value) {
    return String(value ?? "").normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .toLowerCase().replace(/[_\-.:/]+/g, " ").replace(/\s+/g, " ").trim();
}

function tokens(value) {
    return normalize(value).split(" ").filter(token => token.length > 0);
}

function score(text, queryTokens, fuzzyScore) {
    const haystack = normalize(text);
    if (!queryTokens.length) return -1;
    let result = 0;
    for (const token of queryTokens) {
        const at = haystack.indexOf(token);
        if (at < 0) {
            const fuzzy = fuzzyScore ? fuzzyScore(haystack, [token]) : -1;
            if (fuzzy < 0) return -1;
            result += Math.min(10, fuzzy);
            continue;
        }
        result += haystack === token ? 100 : at === 0 ? 60 : haystack[at - 1] === " " ? 40 : 20;
    }
    return result;
}

function mask(line, state) {
    let code = "";
    for (let i = 0; i < line.length; i++) {
        const c = line[i], next = line[i + 1];
        if (state.comment) {
            if (c === "*" && next === "/") { state.comment = false; code += "  "; i++; }
            else code += " ";
        } else if (state.quote) {
            if (c === "\\") { code += "  "; i++; }
            else { if (c === state.quote) state.quote = ""; code += " "; }
        } else if (c === "/" && next === "/") {
            code += " ".repeat(line.length - i); break;
        } else if (c === "/" && next === "*") {
            state.comment = true; code += "  "; i++;
        } else if (c === '"' || c === "'" || c === "`") {
            state.quote = c; code += " ";
        } else code += c;
    }
    return code;
}

function decode(value) {
    return value.replace(/\\(["'\\])/g, "$1").replace(/\\n/g, " ");
}

function parsePage(source, labelledTypes) {
    const entries = [], stack = [], state = { comment: false, quote: "" };
    for (const line of source.split("\n")) {
        const code = mask(line, state);
        const property = code.match(/^\s*(title|text|description|helpText):/);
        const literal = property ? line.match(/^\s*(?:title|text|description|helpText):\s*Translation\.tr\(\s*(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)')\s*\)/) : null;
        const frame = stack[stack.length - 1];
        if (literal && frame) {
            const label = decode(literal[1] ?? literal[2]);
            const sectionFrame = [...stack].reverse().find(item => item.type === "ContentSection");
            const subFrame = [...stack].reverse().find(item => item.type === "ContentSubsection");
            if (property[1] === "description" || property[1] === "helpText") {
                frame.description = label;
                if (frame.entry) frame.entry.description = label;
            } else if (frame.type === "ContentSection" && property[1] === "title") {
                frame.label = label;
                frame.entry = { kind: "section", section: label, subsection: "", label: label, description: frame.description ?? "" };
                entries.push(frame.entry);
            } else if (labelledTypes.includes(frame.type)) {
                if (frame.type === "ContentSubsection") frame.label = label;
                frame.entry = { kind: "option", section: sectionFrame?.label ?? "", subsection: frame.type === "ContentSubsection" ? "" : subFrame?.label ?? "", label: label, description: frame.description ?? "" };
                entries.push(frame.entry);
            }
        }
        const type = code.match(/^\s*([A-Z][\w.]*)\s*\{/);
        const typeBrace = type ? code.indexOf("{", type.index) : -1;
        for (let i = 0; i < code.length; i++) {
            if (code[i] === "{") stack.push({ type: i === typeBrace ? type[1] : "" });
            else if (code[i] === "}") stack.pop();
        }
    }
    return entries;
}
