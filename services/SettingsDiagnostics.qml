pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io
import qs.modules.common

// Thin UI adapter. All integrity checks remain in the existing Python doctor.
Singleton {
    id: root
    readonly property bool running: checker.running
    property bool completed: false
    property string error: ""
    property var checks: []
    property var assets: []

    function run() {
        if (checker.running) return
        root.error = ""
        root.completed = false
        root.checks = []
        root.assets = []
        checker.command = ["python3", `${Directories.scriptPath}/doctor.py`, "--config", Directories.shellConfigPath, "--local-json"]
        checker.running = true
    }

    function label(check) {
        const labels = {
            "config-json": "Configuration file", "config-json-or-schema": "Configuration file",
            "asset": "Image resources", "generated-colors": "Generated colors", "wallpaper-order": "Wallpaper order",
            "wayland-session": "Wayland session", "glass-wallpaper": "Glassy UI wallpaper", "video-thumbnail": "Video thumbnail",
            "geoclue": "Automatic location", "desktop-portal": "Desktop portal"
        }
        return labels[check] ? Translation.tr(labels[check]) : check
    }

    function status(status) {
        return Translation.tr(({ ok: "Available", error: "Needs attention", warning: "Warning", info: "Information", "optional-missing": "Optional dependency missing" })[status] ?? "Unknown")
    }

    Process {
        id: checker
        stdout: StdioCollector { id: output }
        onExited: code => {
            try {
                const result = JSON.parse(output.text)
                if (code > 1 || !Array.isArray(result.checks)) throw new Error("Invalid doctor result")
                root.checks = result.checks
                root.assets = result.assets ?? []
                root.completed = true
            } catch (error) {
                root.error = Translation.tr("Could not run the configuration check. Verify Python 3 and the fork's scripts, then try again.")
            }
        }
    }
}
