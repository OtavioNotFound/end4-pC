import QtQuick
import QtQuick.Layouts
import Quickshell
import qs.services
import qs.modules.common
import qs.modules.common.widgets

ColumnLayout {
    id: root
    required property string configPath
    property var screenNames: Quickshell.screens.map(screen => screen.name)
    readonly property var control: SettingsQuickControls.optionAccessors(configPath)
    readonly property var selected: Array.from(control.get())
    readonly property var names: screenNames.concat(selected.filter(name => !screenNames.includes(name)))
    property string message: ""
    function setScreen(name, enabled) {
        if (Config.blockWrites) return;
        const current = selected.length ? selected.slice() : screenNames.slice();
        const next = current.filter(value => value !== name);
        if (enabled) next.push(name);
        if (!next.length) { message = Translation.tr("Keep at least one monitor selected, or choose all monitors."); return; }
        control.set(next);
        message = "";
    }
    ConfigSwitch {
        id: allSwitch
        text: Translation.tr("All monitors, including new ones")
        enabled: !Config.blockWrites
        Binding { target: allSwitch; property: "checked"; value: root.selected.length === 0 }
        onClicked: { root.control.set([]); root.message = ""; }
    }
    Repeater {
        model: root.names
        delegate: ConfigSwitch {
            id: monitorSwitch
            required property string modelData
            text: modelData + (root.screenNames.includes(modelData) ? "" : " · " + Translation.tr("Disconnected"))
            enabled: !Config.blockWrites
            Binding { target: monitorSwitch; property: "checked"; value: root.selected.length === 0 || root.selected.includes(monitorSwitch.modelData) }
            onClicked: {
                root.setScreen(modelData, root.selected.length > 0 && !root.selected.includes(modelData));
                checked = root.selected.length === 0 || root.selected.includes(modelData);
            }
        }
    }
    StyledText {
        Layout.fillWidth: true
        visible: root.message !== "" || (root.selected.length > 0 && !root.selected.some(name => root.screenNames.includes(name)))
        text: root.message || Translation.tr("None of the selected monitors is connected. Choose a connected monitor to show this component.")
        wrapMode: Text.WordWrap
        color: Appearance.colors.colError
    }
}
