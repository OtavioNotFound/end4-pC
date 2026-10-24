import QtQuick
import QtQuick.Layouts
import qs.services
import qs.modules.common
import qs.modules.common.widgets

DashboardCard {
    id: root
    property string title: ""
    property string description: ""
    property string icon: "open_in_new"
    property string unavailableReason: ""
    signal activated()

    tint: Appearance.colors.colPrimaryContainer

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 6
        RowLayout {
            Layout.fillWidth: true
            MaterialSymbol { text: root.icon; iconSize: 24; color: Appearance.colors.colOnPrimaryContainer }
            StyledText {
                Layout.fillWidth: true
                text: root.title
                font.pixelSize: Appearance.font.pixelSize.normal
                font.weight: Font.DemiBold
                color: Appearance.colors.colOnPrimaryContainer
                wrapMode: Text.WordWrap
                maximumLineCount: 2
                elide: Text.ElideRight
            }
        }
        StyledText {
            Layout.fillWidth: true
            text: root.description
            font.pixelSize: Appearance.font.pixelSize.smaller
            color: Appearance.colors.colOnPrimaryContainer
            wrapMode: Text.WordWrap
            maximumLineCount: 2
            elide: Text.ElideRight
        }
        Item { Layout.fillHeight: true }
        RippleButtonWithIcon {
            Layout.fillWidth: true
            materialIcon: "arrow_forward"
            mainText: Translation.tr("Open")
            Accessible.name: root.title
            enabled: root.unavailableReason === ""
            onClicked: root.activated()
        }
    }
}
