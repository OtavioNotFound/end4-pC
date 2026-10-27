import QtQuick
import QtQuick.Layouts
import qs
import qs.services
import qs.modules.common
import qs.modules.common.widgets
import ".."

ContentPage {
    id: page
    forceWidth: true
    baseWidth: Math.max(300, Math.min(680, width - 32))
    readonly property string selectedKey: DesktopWidgets.selectedKey
    readonly property var widgetInfo: DesktopWidgets.catalog.find(item => item.key === selectedKey)
    readonly property var entry: Config.options.background.widgets[selectedKey]
    readonly property var entries: {
        const sectionTitles = {
            clock: ["Clock", "Digital clock", "Cookie clock", "Daily clock", "Pixel clock", "Quote"],
            weather: ["Weather"], customText: ["Text"], resources: ["Resource widget"],
            media: ["Media widget"], visualizer: ["Visualizer"],
            customImage: ["Custom image"], imageCard: ["Custom image"]
        }[selectedKey] ?? [];
        if (selectedKey === "imageCard") return catalog.sections.reduce((all, section) => all.concat(section.cards.filter(card => ["desktop:Image card/Enable", "desktop:Image card layout"].includes(card.key))), []);
        return catalog.sections.filter(section => sectionTitles.some(title => section.title === Translation.tr(title)) && (!section.when || !SettingsHelp.conditionReason(section.when, "")))
            .reduce((all, section) => all.concat(section.cards.filter(card => card.type !== "weathermap" && !(selectedKey === "customImage" && card.key.startsWith("desktop:Image card"))).map(card => Object.assign({ when: section.when ?? "" }, card))), []);
    }
    DashboardSettingsCatalog { id: catalog }
    ContentSection {
        title: Translation.tr("Desktop widgets")
        icon: "widgets"
        StyledText {
            Layout.fillWidth: true
            text: Translation.tr("Choose a widget to configure. Visibility and the desktop menu are separate choices.")
            wrapMode: Text.WordWrap
            color: Appearance.colors.colSubtext
        }
        Flow {
            Layout.fillWidth: true
            spacing: 4
            Repeater {
                model: DesktopWidgets.catalog
                delegate: RippleButton {
                    required property var modelData
                    buttonText: modelData.name
                    Accessible.name: buttonText
                    toggled: page.selectedKey === modelData.key
                    horizontalPadding: 10; verticalPadding: 6
                    onClicked: DesktopWidgets.select(modelData.key)
                }
            }
        }
    }
    ContentSection {
        title: page.widgetInfo?.name ?? Translation.tr("Widget")
        icon: page.widgetInfo?.icon ?? "widgets"
        ConfigSwitch {
            id: enableSwitch
            text: Translation.tr("Show on desktop")
            enabled: !Config.blockWrites
            Binding { target: enableSwitch; property: "checked"; value: Boolean(page.entry?.enable) }
            onClicked: DesktopWidgets.setEnabled(page.selectedKey, !page.entry.enable)
        }
        ConfigSwitch {
            id: menuSwitch
            text: Translation.tr("Show in desktop menu")
            enabled: !Config.blockWrites
            Binding { target: menuSwitch; property: "checked"; value: DesktopWidgets.isStarred(page.selectedKey) }
            onClicked: DesktopWidgets.toggleStar(page.selectedKey)
        }
        StyledText {
            Layout.fillWidth: true
            text: page.selectedKey === "weather" ? Translation.tr("City, units and location are shared with weather in the bar. GPS may fall back to the configured city.")
                : page.selectedKey === "media" ? (MprisController.activePlayer ? Translation.tr("A compatible media player is available.") : Translation.tr("No compatible media player is active. The widget remains enabled and will receive media when a player appears."))
                : page.selectedKey === "resources" ? Translation.tr("Choose CPU, memory and the third measurement. Automatic uses battery when available, otherwise disk.")
                : Translation.tr("Settings apply to the selected widget. Disabling it preserves its content and position.")
            wrapMode: Text.WordWrap
            color: Appearance.colors.colSubtext
        }
        StyledText {
            Layout.fillWidth: true
            visible: page.selectedKey === "resources" && !page.entry.showCpu && !page.entry.showMemory && page.entry.thirdMetric === "none"
            text: Translation.tr("All measurements are hidden. Enable at least one measurement to see this widget.")
            wrapMode: Text.WordWrap
            color: Appearance.colors.colError
        }
        SettingsInlineControls {
            Layout.fillWidth: true
            entries: page.entries
            catalog: catalog
            onOpenFullSettings: GlobalStates.openSettingsAt(page.selectedKey === "weather" ? "services" : "desktop")
        }
        StyledText {
            Layout.fillWidth: true
            visible: page.entries.length === 0
            text: Translation.tr("No additional controls are exposed here yet. Visibility and position remain available.")
            wrapMode: Text.WordWrap
            color: Appearance.colors.colSubtext
        }
        RippleButton {
            buttonText: Translation.tr("Place near top-left")
            Accessible.name: buttonText
            enabled: !Config.blockWrites
            onClicked: DesktopWidgets.recoverPosition(page.selectedKey)
        }
        StyledText {
            Layout.fillWidth: true
            text: Translation.tr("Moves only this widget to a visible starting position and selects manual placement. Content is preserved; coordinates are shared across desktop monitors.")
            wrapMode: Text.WordWrap
            color: Appearance.colors.colSubtext
        }
        RippleButton { buttonText: Translation.tr("Undo widget position"); Accessible.name: buttonText; enabled: DesktopWidgets.canUndoPosition; onClicked: DesktopWidgets.undoPosition() }
    }
    ContentSection {
        title: Translation.tr("Desktop organization")
        icon: "drag_pan"
        ConfigSwitch {
            id: lockSwitch
            text: Translation.tr("Lock widget positions")
            enabled: !Config.blockWrites
            Binding { target: lockSwitch; property: "checked"; value: Config.options.background.widgetsLocked }
            onClicked: Config.options.background.widgetsLocked = !Config.options.background.widgetsLocked
        }
        SettingsScreenSelection { Layout.fillWidth: true; configPath: "background.screenList" }
    }
}
