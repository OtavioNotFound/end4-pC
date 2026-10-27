pragma Singleton

import QtQuick
import Quickshell
import qs.modules.common

Singleton {
    id: root

    property string selectedKey: "clock"

    readonly property var catalog: [
        { key: "clock",       icon: "schedule",          name: Translation.tr("Clock") },
        { key: "weather",     icon: "partly_cloudy_day", name: Translation.tr("Weather") },
        { key: "calendar",    icon: "calendar_month",    name: Translation.tr("Calendar") },
        { key: "worldClock",  icon: "public",            name: Translation.tr("World Clock") },
        { key: "media",       icon: "music_note",        name: Translation.tr("Media") },
        { key: "visualizer",  icon: "graphic_eq",        name: Translation.tr("Visualizer") },
        { key: "resources",   icon: "monitor_heart",     name: Translation.tr("Resources") },
        { key: "userCard",    icon: "person",            name: Translation.tr("User Card") },
        { key: "todo",        icon: "add_task",          name: Translation.tr("To-Do") },
        { key: "notes",       icon: "note_stack_add",    name: Translation.tr("Notes") },
        { key: "timers",      icon: "timer",             name: Translation.tr("Timers") },
        { key: "images",      icon: "photo_library",     name: Translation.tr("Image Converter") },
        { key: "customImage", icon: "image",             name: Translation.tr("Custom Image") },
        { key: "imageCard",   icon: "photo_size_select_large", name: Translation.tr("Image Card") },
        { key: "customText", icon: "text_fields", name: Translation.tr("Custom text") },
        { key: "sticker",     icon: "sticker",           name: Translation.tr("Sticker") }
    ]

    readonly property var hidden: Array.from(Config.options.background.widgets.menuHidden)
    readonly property var menuItems: catalog.filter(w => !hidden.includes(w.key))
    readonly property int enabledCount: catalog.filter(w => isEnabled(w.key)).length

    function isEnabled(key) {
        return Config.options.background.widgets[key].enable;
    }

    function setEnabled(key, value) {
        if (Config.blockWrites || !catalog.some(item => item.key === key)) return;
        Config.options.background.widgets[key].enable = value;
    }

    function isStarred(key) {
        return !hidden.includes(key);
    }

    function setStarred(key, starred) {
        if (Config.blockWrites || !catalog.some(item => item.key === key)) return;
        const next = hidden.filter(k => k !== key);
        if (!starred) next.push(key);
        Config.options.background.widgets.menuHidden = next;
    }

    function select(key) {
        if (catalog.some(item => item.key === key)) root.selectedKey = key;
    }
    property var previousPosition: null
    property string expectedPosition: ""
    function recoverPosition(key) {
        if (Config.blockWrites || !catalog.some(item => item.key === key)) return false;
        const entry = Config.options.background.widgets[key];
        previousPosition = { key: key, x: entry.x, y: entry.y, placementStrategy: entry.placementStrategy };
        entry.placementStrategy = "free";
        entry.x = 24; entry.y = 24;
        expectedPosition = JSON.stringify({ key: key, x: entry.x, y: entry.y, placementStrategy: entry.placementStrategy });
        return true;
    }
    readonly property bool canUndoPosition: {
        if (!previousPosition || Config.blockWrites) return false;
        const entry = Config.options.background.widgets[previousPosition.key];
        return expectedPosition === JSON.stringify({ key: previousPosition.key, x: entry.x, y: entry.y, placementStrategy: entry.placementStrategy });
    }
    function undoPosition() {
        if (!canUndoPosition) return false;
        const previous = previousPosition;
        previousPosition = null;
        const entry = Config.options.background.widgets[previous.key];
        entry.x = previous.x; entry.y = previous.y; entry.placementStrategy = previous.placementStrategy;
        return true;
    }

    function toggleStar(key) {
        setStarred(key, !isStarred(key));
    }
}
