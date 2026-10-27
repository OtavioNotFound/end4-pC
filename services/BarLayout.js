.pragma library

// Operate on copies: unknown legacy IDs survive unrelated edits.
function copy(lists) {
    return { left: Array.from(lists.left), middle: Array.from(lists.middle), right: Array.from(lists.right) };
}
function validLane(lane) { return ["left", "middle", "right"].includes(lane); }
function reason(id, lane, lists, vertical, mode, adding) {
    if (!validLane(lane)) return "Choose a bar region.";
    if (id === "dynamicIsland") {
        if (vertical) return "Dynamic Island requires a horizontal bar.";
        if (lane !== "middle") return "Dynamic Island belongs in the center region.";
        if (lists.middle.length) return "Dynamic Island needs the center region to itself.";
    } else if (lane === "middle" && lists.middle.includes("dynamicIsland")) {
        return "Dynamic Island needs the center region to itself.";
    }
    if (id === "divisor" && mode !== "transparent") return "Dividers require the transparent group style.";
    if (adding && !["visualizer", "divisor"].includes(id)
        && lists.left.concat(lists.middle, lists.right).includes(id)) return "This item is already on the bar.";
    return "";
}
function transfer(lists, from, index, target, position, id, vertical, mode) {
    const next = copy(lists);
    if (from !== "tray") {
        if (!validLane(from) || !Number.isInteger(index) || index < 0 || index >= next[from].length)
            return { error: "The layout changed. Select the item again." };
        if (next[from][index] !== id) return { error: "The layout changed. Select the item again." };
        next[from].splice(index, 1);
    }
    if (target !== "tray") {
        // Reordering within a region preserves legacy combinations, including unknown IDs.
        const error = from === target ? "" : reason(id, target, next, vertical, mode, from === "tray");
        if (error) return { error: error };
        if (!Number.isInteger(position) || position < 0 || position > next[target].length)
            return { error: "Choose a bar region." };
        next[target].splice(position, 0, id);
    }
    return { lists: next };
}
