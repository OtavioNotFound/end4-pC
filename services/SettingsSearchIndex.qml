pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io
import qs.services
import qs.modules.common.functions
import "SettingsSearch.js" as Search
import "SettingsMetadata.js" as Metadata

Singleton {
    id: root

    property var entriesByPage: ({})

    readonly property var labelledTypes: [
        "ConfigSwitch", "ConfigSpinBox", "ConfigTextArea", "ConfigSelectionArray",
        "ConfigComboBox", "ConfigSlider", "ConfigSelectionShapeArray", "ConfigRow",
        "ColorSelectionArray", "ContentSubsection"
    ]

    function parsePage(source) {
        return Search.parsePage(source, root.labelledTypes)
    }

    function indexPage(pageId, source) {
        const next = Object.assign({}, root.entriesByPage);
        next[pageId] = root.parsePage(source);
        root.entriesByPage = next;
    }

    function search(query, limit) {
        const tokens = Search.tokens(query);
        if (tokens.length === 0) return [];

        const results = [];
        for (const page of SettingsPages.pages) {
            const pageName = page.name.toLowerCase();
            const pageScore = Search.score(pageName + " " + page.id + " " + (Metadata.pageKeywords[page.id] ?? ""), tokens, Wallpapers.scoreItem);
            if (pageScore >= 0) {
                results.push({
                    pageId: page.id, pageName: page.name, icon: page.icon,
                    kind: "page", section: "", label: page.name, score: pageScore + 50
                });
            }
            for (const entry of (root.entriesByPage[page.id] ?? [])) {
                const label = Translation.tr(entry.label);
                const section = Translation.tr(entry.section);
                const controlKey = SettingsQuickControls.keyFor(page.id, entry.section, entry.subsection, entry.label);
                const meta = Metadata.forKey(controlKey);
                const description = [entry.description ?? "", Translation.tr(meta.description ?? ""), meta.description ?? "", meta.keywords ?? ""].join(" ");
                const haystack = [label, entry.label, section, pageName, entry.subsection ?? "", description].join(" ");
                if (Search.score(haystack, tokens, Wallpapers.scoreItem) < 0) continue;
                const labelScore = Math.max(
                    root.scoreText(label.toLowerCase(), tokens),
                    root.scoreText(entry.label.toLowerCase(), tokens)
                );
                results.push({
                    pageId: page.id, pageName: page.name, icon: page.icon,
                    kind: entry.kind, section: section, label: label, rawLabel: entry.label, rawSection: entry.section, subsection: Translation.tr(entry.subsection ?? ""), rawSubsection: entry.subsection ?? "",
                    score: labelScore + (entry.kind === "section" ? 10 : 0)
                });
            }
        }
        results.sort((a, b) => b.score - a.score);
        return results.slice(0, limit);
    }

    function scoreText(text, tokens) {
        return Search.score(text, tokens, Wallpapers.scoreItem);
    }

    Instantiator {
        model: SettingsPages.pages
        delegate: FileView {
            required property var modelData
            path: FileUtils.trimFileProtocol(Quickshell.shellPath(modelData.path))
            onLoaded: root.indexPage(modelData.id, text())
        }
    }
}
