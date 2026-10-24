import QtQuick
import QtQuick.Layouts
import qs.services
import qs.modules.common
import qs.modules.common.widgets

DashboardCard {
    id: root

    property string controlKey: ""
    property string unavailableReason: SettingsHelp.disabledReason(controlKey, "", "")
    property string title: ""
    Accessible.name: root.title
    Accessible.description: controlHelp.text
    property string icon: "tune"
    property var tileShape: MaterialShape.Shape.Flower
    property bool showPercent: true

    property var override: null
    readonly property var control: override ?? SettingsQuickControls.controls[controlKey] ?? null
    readonly property real current: control ? control.get() : 0
    readonly property real fromValue: control?.from ?? 0
    readonly property real toValue: control?.to ?? 1

    tint: Appearance.colors.colSecondaryContainer

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            MaterialShapeWrappedMaterialSymbol {
                shape: root.tileShape
                text: root.icon
                iconSize: 24
                fill: 1
                padding: 10
                color: Appearance.colors.colSecondary
                colSymbol: Appearance.colors.colOnSecondary
            }

            StyledText {
                Layout.fillWidth: true
                text: root.title
                font.pixelSize: Appearance.font.pixelSize.larger
                font.weight: Font.DemiBold
                color: Appearance.colors.colOnSecondaryContainer
                elide: Text.ElideRight
            }

            StyledText {
                text: SettingsHelp.displayValue(root.controlKey, root.current, root.showPercent, root.fromValue, root.toValue)
                font.pixelSize: 28
                font.weight: Font.Light
                color: Appearance.colors.colOnSecondaryContainer
            }
        }

        Item { Layout.fillHeight: true }

        StyledSlider {
            enabled: root.unavailableReason === ""
            Accessible.name: root.title
            Accessible.description: controlHelp.text
            Layout.fillWidth: true
            configuration: StyledSlider.Configuration.Wavy
            from: root.fromValue
            to: root.toValue
            value: root.current
            usePercentTooltip: root.showPercent
            tooltipContent: SettingsHelp.displayValue(root.controlKey, value, root.showPercent, root.fromValue, root.toValue)
            stopIndicatorValues: root.control?.stopIndicatorValues ?? []
            highlightColor: Appearance.colors.colSecondary
            trackColor: Qt.rgba(1, 1, 1, 0.15)
            handleColor: Appearance.colors.colSecondary
            onMoved: {
                if (root.control && !root.unavailableReason) root.control.set(value);
            }
        }
    }
    SettingsControlHelp {
        id: controlHelp
        anchors.fill: parent
        controlKey: root.controlKey
        reason: root.unavailableReason
    }
}
