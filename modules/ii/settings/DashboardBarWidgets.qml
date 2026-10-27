import QtQuick
import qs.services

QtObject {
    readonly property var multipleAllowed: ["visualizer", "divisor"]

    readonly property var all: [
        { id: "leftSidebarButton", name: Translation.tr("Left Sidebar Button"), icon: "left_panel_open" },
        { id: "workspaces", name: Translation.tr("Workspaces"), icon: "steppers" },
        { id: "weatherBar", name: Translation.tr("Weather"), icon: "flare" },
        { id: "liveWallpaper", name: Translation.tr("Live wallpaper"), icon: "play_pause" },
        { id: "media", name: Translation.tr("Media"), icon: "music_note" },
        { id: "resources", name: Translation.tr("Resources"), icon: "empty_dashboard" },
        { id: "systemIcons", name: Translation.tr("System Icons"), icon: "info" },
        { id: "networkSpeed", name: Translation.tr("Network Speed"), icon: "network_check" },
        { id: "clockWidget", name: Translation.tr("Clock"), icon: "schedule" },
        { id: "utilButtons", name: Translation.tr("Util Buttons"), icon: "toggle_on" },
        { id: "sysTray", name: Translation.tr("Tray"), icon: "inbox" },
        { id: "batteryIndicator", name: Translation.tr("Battery"), icon: "battery_android_frame_full" },
        { id: "bluetooth", name: Translation.tr("Bluetooth"), icon: "bluetooth" },
        { id: "activeWindow", name: Translation.tr("Active Window"), icon: "subtitles" },
        { id: "powerButton", name: Translation.tr("Power Button"), icon: "power_settings_new" },
        { id: "updatesCount", name: Translation.tr("Updates"), icon: "deployed_code_update" },
        { id: "docktoPanel", name: Translation.tr("Dock to Panel"), icon: "apps" },
        { id: "visualizer", name: Translation.tr("Visualizer"), icon: "graphic_eq" },
        { id: "hyprlandXkbIndicator", name: Translation.tr("Keyboard Layout"), icon: "keyboard" },
        { id: "divisor", name: Translation.tr("Divider"), icon: "horizontal_distribute" },
        { id: "launcherButton", name: Translation.tr("Launcher Button"), icon: "search" },
        { id: "dynamicIsland", name: Translation.tr("Dynamic Island"), icon: "nest_wifi_pro" },
        { id: "aiUsage", name: Translation.tr("AI Usage"), icon: "neurology" },
        { id: "avatar", name: Translation.tr("Avatar"), icon: "account_circle" }
    ]

    function description(id) {
        const descriptions = {
            leftSidebarButton: "Opens the left sidebar. Its icon can be customized.",
            workspaces: "Switches workspaces and shows their numbers or application icons.",
            weatherBar: "Shows weather using the shared city and location settings.",
            liveWallpaper: "Controls playback of a video wallpaper. Requires a video wallpaper backend.",
            media: "Shows media from a compatible player. No player means there may be nothing to display.",
            resources: "Shows CPU, memory and other selected system measurements.",
            systemIcons: "Shows shared system status indicators.",
            networkSpeed: "Shows current network transfer speed.",
            clockWidget: "Shows the time and optional date. These formats are shared with other clock displays.",
            utilButtons: "Provides the utility shortcuts you choose below.",
            sysTray: "Shows status icons published by running applications.",
            batteryIndicator: "Shows battery status when the system provides a battery.",
            bluetooth: "Shows Bluetooth status and access to devices.",
            activeWindow: "Shows information about the focused window.",
            powerButton: "Opens session and power actions.",
            updatesCount: "Shows updates reported by the configured update service.",
            docktoPanel: "Shows application buttons inside the bar.",
            visualizer: "Displays an audio visualization when an audio source is available.",
            hyprlandXkbIndicator: "Shows the active keyboard layout provided by the compositor.",
            divisor: "Separates neighboring items. Requires transparent groups.",
            launcherButton: "Opens the application launcher.",
            dynamicIsland: "Combines live activity in the center. Requires a horizontal bar and an exclusive center region.",
            aiUsage: "Shows usage reported by the configured AI service.",
            avatar: "Shows your account avatar."
        };
        return Translation.tr(descriptions[id] ?? "Unknown preset item. It is preserved until you explicitly remove it.");
    }

    function byId(id) {
        return all.find(w => w.id === id) ?? { id: id, name: id, icon: "widgets" };
    }
}
