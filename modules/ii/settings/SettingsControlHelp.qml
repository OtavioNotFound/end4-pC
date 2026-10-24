import QtQuick
import qs.services
import qs.modules.common
import qs.modules.common.widgets

Item {
    id: root
    property string controlKey: ""
    property string reason: ""
    readonly property string statusText: reason || SettingsHelp.warning(controlKey)
    readonly property string text: [SettingsHelp.text(controlKey), reason].filter(value => value).join("\n")
    z: 10

    HoverHandler { id: hover }
    StyledToolTip {
        text: root.text
        maximumContentWidth: 420
        extraVisibleCondition: root.text !== "" && (hover.hovered || (root.parent?.activeFocus ?? false))
    }
    StyledText {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: 14
        anchors.rightMargin: 14
        anchors.bottomMargin: 1
        visible: root.statusText !== ""
        text: root.statusText
        color: Appearance.colors.colSubtext
        font.pixelSize: Appearance.font.pixelSize.smallest
        elide: Text.ElideRight
    }
}
