import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Widgets
import qs
import qs.services
import qs.modules.common
import qs.modules.common.widgets
import ".."
import "../../../../services/SettingsSearch.js" as Search

ContentPage {
    id: page
    forceWidth: true
    baseWidth: Math.max(300, Math.min(680, width - 32))
    property string appQuery: ""
    readonly property var apps: Array.from(DesktopEntries.applications.values).filter(app => Search.score(app.name + " " + app.id, Search.tokens(appQuery)) >= 0 || !appQuery.trim()).slice(0, 30)
    readonly property var pinned: Array.from(Config.options.dock.pinnedApps)
    DashboardSettingsCatalog { id: catalog }

    ContentSection {
        title: Translation.tr("Dock")
        icon: "dock_to_bottom"
        StyledText {
            Layout.fillWidth: true
            text: Translation.tr("Changes apply immediately unless a control says otherwise. Your pinned applications are kept when the dock is disabled.")
            wrapMode: Text.WordWrap
            color: Appearance.colors.colSubtext
        }
        SettingsInlineControls {
            Layout.fillWidth: true
            entries: catalog.sections.filter(section => section.cards.some(card => card.key === "interface:Dock/Enable")).reduce((all, section) => all.concat(section.cards), [])
            catalog: catalog
            onOpenFullSettings: GlobalStates.openSettingsAt("interface", "", Translation.tr("Dock"))
        }
    }
    ContentSection {
        title: Translation.tr("Dock style")
        icon: "style"
        SettingsInlineControls {
            Layout.fillWidth: true
            entries: catalog.sections.filter(section => section.cards.some(card => card.key === "interface:Dock/Position")).reduce((all, section) => all.concat(section.cards), [])
            catalog: catalog
            onOpenFullSettings: GlobalStates.openSettingsAt("interface", "", Translation.tr("Dock"))
        }
    }
    ContentSection {
        title: Translation.tr("Show dock on")
        icon: "monitor"
        SettingsScreenSelection { Layout.fillWidth: true; configPath: "dock.screenList" }
    }
    ContentSection {
        title: Translation.tr("Pinned applications")
        icon: "push_pin"
        StyledText {
            Layout.fillWidth: true
            text: Translation.tr("Reorder or unpin applications here. Unpinning never uninstalls an application.")
            wrapMode: Text.WordWrap
            color: Appearance.colors.colSubtext
        }
        Repeater {
            model: page.pinned
            delegate: RowLayout {
                id: pinnedRow
                required property string modelData
                required property int index
                readonly property var entry: DesktopEntries.byId(modelData)
                Layout.fillWidth: true
                IconImage { implicitSize: 24; source: SystemAppearance.iconPath(pinnedRow.entry?.icon ?? "image-missing", "image-missing") }
                StyledText {
                    Layout.fillWidth: true
                    text: (pinnedRow.entry?.name ?? pinnedRow.modelData) + (pinnedRow.entry ? "" : " · " + Translation.tr("Application unavailable"))
                    textFormat: Text.PlainText
                    wrapMode: Text.WordWrap
                }
                RippleButton { buttonText: "↑"; Accessible.name: Translation.tr("Move earlier"); enabled: pinnedRow.index > 0 && !Config.blockWrites; onClicked: TaskbarApps.movePinned(pinnedRow.modelData, -1) }
                RippleButton { buttonText: "↓"; Accessible.name: Translation.tr("Move later"); enabled: pinnedRow.index < page.pinned.length - 1 && !Config.blockWrites; onClicked: TaskbarApps.movePinned(pinnedRow.modelData, 1) }
                RippleButton { buttonText: Translation.tr("Unpin"); Accessible.name: buttonText + " · " + (pinnedRow.entry?.name ?? pinnedRow.modelData); enabled: !Config.blockWrites; onClicked: TaskbarApps.togglePin(pinnedRow.modelData) }
            }
        }
        MaterialTextField {
            Layout.fillWidth: true
            placeholderText: Translation.tr("Find an application to pin")
            Accessible.name: placeholderText
            onTextEdited: page.appQuery = text
        }
        StyledText {
            Layout.fillWidth: true
            text: Translation.tr("Up to 30 applications are shown. Type to narrow the list.")
            wrapMode: Text.WordWrap
            color: Appearance.colors.colSubtext
        }
        StyledText {
            Layout.fillWidth: true
            visible: page.apps.length === 0
            text: Translation.tr("No applications match this search.")
            color: Appearance.colors.colSubtext
        }
        Repeater {
            model: page.apps
            delegate: RowLayout {
                required property var modelData
                Layout.fillWidth: true
                IconImage { implicitSize: 24; source: SystemAppearance.iconPath(parent.modelData.icon, "image-missing") }
                StyledText { Layout.fillWidth: true; text: parent.modelData.name; textFormat: Text.PlainText; wrapMode: Text.WordWrap }
                RippleButton {
                    Accessible.name: buttonText + " · " + parent.modelData.name
                    buttonText: TaskbarApps.isPinned(parent.modelData.id) ? Translation.tr("Pinned") : Translation.tr("Pin")
                    enabled: !TaskbarApps.isPinned(parent.modelData.id) && !Config.blockWrites
                    onClicked: TaskbarApps.togglePin(parent.modelData.id)
                }
            }
        }
    }
}
