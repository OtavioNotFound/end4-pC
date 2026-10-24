import QtQuick
import QtQuick.Layouts
import QtQuick.Effects
import qs.services
import qs.modules.common
import qs.modules.common.widgets

DashboardCard {
    id: root

    property string controlKey: ""
    property string unavailableReason: SettingsHelp.disabledReason(controlKey, "", "")
    property string title: ""
    property string icon: "toggle_on"
    property var tileShape: MaterialShape.Shape.Cookie6Sided

    property var override: null
    property string actionIcon: ""
    property string actionTip: ""
    readonly property string helpText: SettingsHelp.text(controlKey)
    Accessible.name: root.title
    Accessible.description: controlHelp.text
    Accessible.role: Accessible.CheckBox
    Accessible.checkable: true
    Accessible.checked: root.checked
    activeFocusOnTab: true
    border.width: root.activeFocus ? 1 : 0
    border.color: Appearance.colors.colPrimary
    Keys.onSpacePressed: if (root.control && !root.unavailableReason) root.control.set(!root.checked)

    signal actionTriggered()
    readonly property var control: override ?? SettingsQuickControls.controls[controlKey] ?? null
    readonly property bool checked: control ? !!control.get() : false

    tint: checked ? Appearance.colors.colPrimaryContainer : Appearance.colors.colLayer1

    Behavior on tint {
        ColorAnimation { duration: 200 }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 0

        RowLayout {
            Layout.fillWidth: true

            MaterialShapeWrappedMaterialSymbol {
                shape: root.tileShape
                text: root.icon
                iconSize: 24
                fill: 1
                padding: 10
                color: root.checked ? Appearance.colors.colPrimary : Appearance.colors.colSecondaryContainer
                colSymbol: root.checked ? Appearance.colors.colOnPrimary : Appearance.colors.colOnSecondaryContainer
            }

            Item { Layout.fillWidth: true }

            Rectangle {
                id: track
                implicitWidth: 47
                implicitHeight: 27
                radius: height / 2
                color: root.checked ? Appearance.colors.colPrimary : Appearance.m3colors.m3surfaceBright

                Behavior on color {
                    ColorAnimation { duration: 180 }
                }

                Rectangle {
                    anchors.fill: parent
                    radius: parent.radius
                    color: "transparent"
                    border.width: 1
                    border.color: Qt.rgba(1, 1, 1, 0.06)
                }

                Rectangle {
                    id: thumb
                    width: 23
                    height: 23
                    radius: width / 2
                    anchors.verticalCenter: parent.verticalCenter
                    x: root.checked ? track.width - width - 2 : 2
                    color: root.checked ? Appearance.colors.colOnPrimary : Appearance.colors.colPrimary

                    layer.enabled: true
                    layer.effect: MultiEffect {
                        shadowEnabled: true
                        shadowColor: Qt.rgba(0, 0, 0, 0.55)
                        shadowVerticalOffset: 2
                        shadowHorizontalOffset: 0
                        shadowBlur: 0.4
                    }

                    Behavior on x {
                        NumberAnimation {
                            duration: 320
                            easing.type: Easing.BezierSpline
                            easing.bezierCurve: [0.42, 1.5, 0.28, 0.95, 1, 1]
                        }
                    }
                    Behavior on color {
                        ColorAnimation { duration: 180 }
                    }
                }
            }
        }

        Item { Layout.fillHeight: true }

        StyledText {
            Layout.fillWidth: true
            text: root.title
            font.pixelSize: Appearance.font.pixelSize.larger
            font.weight: Font.DemiBold
            color: root.checked ? Appearance.colors.colOnPrimaryContainer : Appearance.colors.colOnLayer1
            elide: Text.ElideRight
        }
        StyledText {
            text: root.unavailableReason ? Translation.tr("Unavailable") : root.checked ? Translation.tr("On") : Translation.tr("Off")
            font.pixelSize: Appearance.font.pixelSize.smaller
            color: root.checked ? Appearance.colors.colOnPrimaryContainer : Appearance.colors.colSubtext
            opacity: 0.8
        }
    }

    MouseArea {
        id: toggleMouse
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            if (!root.control || root.unavailableReason) return;
            const next = !root.checked;
            Qt.callLater(() => root.control.set(next));
        }
    }


    RippleButton {
        id: actionButton
        visible: root.actionIcon !== "" && root.checked
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 12
        implicitWidth: 38
        implicitHeight: 38
        buttonRadius: 19
        colBackground: Qt.rgba(1, 1, 1, 0.12)
        colBackgroundHover: Qt.rgba(1, 1, 1, 0.22)
        colRipple: Qt.rgba(1, 1, 1, 0.3)
        onClicked: root.actionTriggered()

        contentItem: MaterialSymbol {
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: root.actionIcon
            iconSize: 22
            fill: 1
            color: Appearance.colors.colOnPrimaryContainer
        }

        StyledToolTip {
            text: root.actionTip
        }
    }
    SettingsControlHelp {
        id: controlHelp
        anchors.fill: parent
        controlKey: root.controlKey
        reason: root.unavailableReason
    }
}
