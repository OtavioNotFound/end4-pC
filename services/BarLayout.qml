pragma Singleton
import QtQuick
import Quickshell
import qs.modules.common
import qs.services
import "BarLayout.js" as Rules

Singleton {
    id: root
    readonly property var lists: ({ left: Array.from(Config.options.bar.layouts.leftLayout), middle: Array.from(Config.options.bar.layouts.middleLayout), right: Array.from(Config.options.bar.layouts.rightLayout) })
    readonly property string signature: JSON.stringify(lists)
    property var previous: null
    property string expected: ""
    property string message: ""
    readonly property bool canUndo: previous !== null && signature === expected && !Config.blockWrites

    function reason(id, lane, adding) {
        return Translation.tr(Rules.reason(id, lane, root.lists, Config.options.bar.vertical, Config.options.bar.borderless, adding));
    }
    function write(next) {
        const layouts = Config.options.bar.layouts;
        layouts.leftLayout = next.left;
        layouts.middleLayout = next.middle;
        layouts.rightLayout = next.right;
    }
    function apply(next) {
        if (Config.blockWrites) { message = Translation.tr("A preset is being applied. Wait for the operation to finish."); return false; }
        if (JSON.stringify(next) === signature) return true;
        previous = Rules.copy(lists);
        write(next);
        expected = JSON.stringify(next);
        message = Translation.tr("Layout updated. You can undo this change.");
        return true;
    }
    function transfer(from, index, target, position, id) {
        const result = Rules.transfer(lists, from, index, target, position, id, Config.options.bar.vertical, Config.options.bar.borderless);
        if (result.error) { message = Translation.tr(result.error); return false; }
        return apply(result.lists);
    }
    function clear() { return apply({ left: [], middle: [], right: [] }); }
    function undo() {
        if (!canUndo) { message = Translation.tr("The layout changed elsewhere. Undo is unavailable."); return false; }
        const restore = previous;
        previous = null;
        write(restore);
        expected = "";
        message = Translation.tr("Previous layout restored.");
        return true;
    }
}
