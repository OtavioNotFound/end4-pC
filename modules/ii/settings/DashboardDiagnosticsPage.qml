import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import qs.services
import qs.modules.common
import qs.modules.common.widgets

Item {
    id: root
    signal back()
    signal chooseWallpaper()

    ColumnLayout {
        anchors.fill: parent
        spacing: 12
        RowLayout {
            Layout.fillWidth: true
            RippleButtonWithIcon {
                materialIcon: "arrow_back"
                mainText: Translation.tr("Back")
                Accessible.name: mainText
                onClicked: root.back()
            }
            StyledText {
                Layout.fillWidth: true
                text: Translation.tr("Check configuration")
                font.pixelSize: Appearance.font.pixelSize.larger
                color: Appearance.colors.colOnLayer0
            }
            RippleButtonWithIcon {
                materialIcon: "refresh"
                mainText: Translation.tr("Check again")
                Accessible.name: mainText
                enabled: !SettingsDiagnostics.running
                onClicked: SettingsDiagnostics.run()
            }
        }
        NoticeBox {
            Layout.fillWidth: true
            text: SettingsDiagnostics.running ? Translation.tr("Checking configuration… No settings are changed.")
                : SettingsDiagnostics.error || (SettingsDiagnostics.completed
                    ? Translation.tr("Check complete. Missing optional dependencies only affect their own features.")
                    : Translation.tr("This check is local and read-only."))
        }
        StyledFlickable {
            id: scroll
            Layout.fillWidth: true
            Layout.fillHeight: true
            contentHeight: results.implicitHeight
            clip: true
            ColumnLayout {
                id: results
                width: scroll.width
                spacing: 8
                Repeater {
                    model: SettingsDiagnostics.assets
                    delegate: NoticeBox {
                        required property var modelData
                        Layout.fillWidth: true
                        text: [modelData.field, modelData.path, modelData.reason,
                            modelData.candidates.length === 1 ? Translation.tr("Suggested file: %1").arg(modelData.candidates[0]) : ""].filter(value => value).join("\n")
                    }
                }
                RippleButtonWithIcon {
                    visible: SettingsDiagnostics.assets.length > 0
                    materialIcon: "wallpaper"
                    mainText: Translation.tr("Choose a wallpaper")
                    Accessible.name: mainText
                    onClicked: root.chooseWallpaper()
                }
                Repeater {
                    model: SettingsDiagnostics.checks
                    delegate: NoticeBox {
                        required property var modelData
                        Layout.fillWidth: true
                        materialIcon: modelData.status === "ok" ? "check_circle" : "info"
                        text: SettingsDiagnostics.label(modelData.check) + " · " + SettingsDiagnostics.status(modelData.status)
                            + (modelData.detail ? "\n" + modelData.detail : "")
                    }
                }
                StyledText {
                    Layout.fillWidth: true
                    visible: SettingsDiagnostics.completed
                    text: Translation.tr("Optional packages are not installed automatically. After installing cliphist, restart only the shell so it can be detected.")
                    wrapMode: Text.WordWrap
                    color: Appearance.colors.colSubtext
                    font.pixelSize: Appearance.font.pixelSize.small
                }
            }
        }
    }
}
