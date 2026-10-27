import QtQuick
import QtQuick.Layouts
import qs.services
import qs.modules.common
import qs.modules.common.widgets

ColumnLayout {
    id: root
    property var entries: []
    property var catalog: null
    spacing: 12

    Repeater {
        model: root.entries
        delegate: ColumnLayout {
            id: row
            required property var modelData
            readonly property var control: root.catalog?.controlFor(modelData.key) ?? SettingsQuickControls.controls[modelData.key] ?? null
            readonly property string reason: SettingsHelp.disabledReason(modelData.key, modelData.when ?? "", modelData.requires ?? "")
            readonly property string label: SettingsHelp.title(modelData.key, modelData.title)
            readonly property var current: control ? control.get() : null
            Layout.fillWidth: true
            spacing: 3
            Loader {
                Layout.fillWidth: true
                enabled: row.reason === ""
                sourceComponent: row.modelData.type === "swatch" && row.control ? swatchControl : row.control?.type === "switch" ? switchControl
                    : row.control?.type === "spin" ? spinControl
                    : row.control?.type === "slider" ? sliderControl
                    : row.control?.options ? selectControl : row.control?.type === "text" ? textControl : fallbackControl
            }
            StyledText {
                Layout.fillWidth: true
                visible: text !== ""
                text: [SettingsHelp.text(row.modelData.key), row.reason].filter(Boolean).join("\n")
                textFormat: Text.PlainText
                wrapMode: Text.WordWrap
                font.pixelSize: Appearance.font.pixelSize.smaller
                color: row.reason ? Appearance.colors.colError : Appearance.colors.colSubtext
            }
            Component {
                id: swatchControl
                DashboardSwatchCard {
                    implicitHeight: 140
                    controlKey: row.modelData.key
                    title: row.label
                    override: row.control
                }
            }
            Component {
                id: switchControl
                ConfigSwitch {
                    id: toggle
                    objectName: "inline:" + row.modelData.key
                    text: row.label
                    description: SettingsHelp.text(row.modelData.key)
                    Binding { target: toggle; property: "checked"; value: Boolean(row.current) }
                    onClicked: if (row.control && !row.reason) row.control.set(!row.current)
                }
            }
            Component {
                id: spinControl
                ConfigSpinBox {
                    objectName: "inline:" + row.modelData.key
                    text: row.label + (SettingsHelp.unit(row.modelData.key) ? " (" + SettingsHelp.unit(row.modelData.key) + ")" : "")
                    from: row.control.from; to: row.control.to; stepSize: row.control.stepSize ?? 1
                    value: Number(row.current)
                    onValueModified: row.control.set(value)
                }
            }
            Component {
                id: sliderControl
                ColumnLayout {
                    StyledText { text: row.label + " · " + SettingsHelp.displayValue(row.modelData.key, row.current, row.control.usePercentTooltip, row.control.from, row.control.to) }
                    ConfigSlider {
                        Layout.fillWidth: true
                        showLabel: false
                        from: row.control.from; to: row.control.to; value: Number(row.current)
                        usePercentTooltip: row.control.usePercentTooltip ?? false
                        stopIndicatorValues: row.control.stopIndicatorValues ?? []
                        onMoved: row.control.set(value)
                    }
                }
            }
            Component {
                id: selectControl
                ColumnLayout {
                    StyledText { text: row.label }
                    StyledComboBoxSearch {
                        objectName: "inline:" + row.modelData.key
                        Layout.fillWidth: true
                        Accessible.name: row.label
                        model: row.control.options.map(option => Object.assign({ displayName: option.displayName ?? option.value }, option))
                        textRole: "displayName"
                        currentIndex: row.control.options.findIndex(option => option.value === row.current)
                        displayText: currentIndex < 0 ? String(row.current ?? Translation.tr("Unavailable")) : String(row.control.options[currentIndex]?.displayName ?? row.control.options[currentIndex]?.value ?? "")
                        onActivated: index => row.control.set(row.control.options[index].value)
                    }
                }
            }
            Component {
                id: textControl
                ColumnLayout {
                    StyledText { text: row.label }
                    MaterialTextField {
                        id: textField
                        Layout.fillWidth: true
                        Accessible.name: row.label
                        text: String(row.current ?? "")
                        onEditingFinished: if (row.control && !row.reason && text !== String(row.current ?? "")) row.control.set(text)
                        Connections {
                            target: row
                            function onCurrentChanged() { if (!textField.activeFocus) textField.text = String(row.current ?? ""); }
                        }
                    }
                }
            }
            Component {
                id: fallbackControl
                RippleButton {
                    buttonText: row.label + " · " + Translation.tr("Open all options")
                    Accessible.name: buttonText
                    onClicked: root.openFullSettings()
                }
            }
        }
    }
    signal openFullSettings()
}
