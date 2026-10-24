pragma Singleton
pragma ComponentBehavior: Bound

import QtQuick
import Quickshell
import Quickshell.Io
import qs.modules.common

// Validate once per configured path, instead of once per glass surface.
Singleton {
    id: root

    readonly property var paths: [Config.options.background.wallpaperPath,
        Config.options.background.lockWall, Config.options.background.thumbnailPath,
        Config.options.background.centeredWallpaperImage]
    property var resources: ({})
    property var warned: ({})
    property bool pending: false
    property string desktopSource: ""
    property string lockSource: ""

    function source(path) {
        return root.resources[path]?.source ?? ""
    }

    function refresh() {
        if (checkProc.running) {
            root.pending = true
            return
        }
        checkProc.command = ["python3", `${Directories.scriptPath}/preset_resources.py`, "--sources", JSON.stringify(root.paths)]
        checkProc.running = true
    }

    onPathsChanged: checkTimer.restart()
    Component.onCompleted: checkTimer.restart()

    Timer {
        id: checkTimer
        interval: 25
        onTriggered: root.refresh()
    }

    Timer {
        interval: 10000
        repeat: true
        running: Object.values(root.resources).some(record => record.source === "")
        onTriggered: root.refresh() // Recover when a missing file is restored in place.
    }

    Process {
        id: checkProc
        stdout: StdioCollector { id: output }
        onExited: code => {
            if (code === 0) {
                try {
                    const records = JSON.parse(output.text)
                    root.resources = records
                    const background = Config.options.background
                    const desktop = /\.(mp4|webm|mkv|avi|mov)$/i.test(background.wallpaperPath) ? background.thumbnailPath : background.wallpaperPath
                    const locked = /\.(mp4|webm|mkv|avi|mov)$/i.test(background.lockWall) ? background.thumbnailPath : background.lockWall
                    // Retain the current image while a new path is pending. This
                    // preserves the original transition between two valid images.
                    if (desktop === "" || Object.prototype.hasOwnProperty.call(records, desktop))
                        root.desktopSource = records[desktop]?.source ?? ""
                    if (locked === "") root.lockSource = root.desktopSource
                    else if (Object.prototype.hasOwnProperty.call(records, locked))
                        root.lockSource = records[locked]?.source ?? ""
                    for (const path of Object.keys(records)) {
                        const issue = records[path].issue
                        if (!issue || root.warned[path]) continue
                        root.warned[path] = true
                        const suggestion = issue.candidates.length === 1 ? `; suggested / sugerido: ${issue.candidates[0]}` : ""
                        console.warn(`[WallpaperResources] ${path}: ${issue.reason}${suggestion}. Run / execute: python3 scripts/preset_resources.py CONFIG.json`)
                    }
                } catch (error) {
                    console.warn("[WallpaperResources] Invalid validation response", error)
                }
            } else {
                root.desktopSource = ""
                root.lockSource = ""
                if (!root.warned.validator) {
                    root.warned.validator = true
                    console.warn("[WallpaperResources] Resource validator failed; run python3 scripts/doctor.py / Falha no validador de recursos.")
                }
            }
            if (root.pending) {
                root.pending = false
                checkTimer.restart()
            }
        }
    }
}
