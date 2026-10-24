pragma Singleton
pragma ComponentBehavior: Bound

import qs
import qs.modules.common
import qs.services
import QtQuick
import Quickshell
import Quickshell.Io

/**
 * Automatically reloads generated material colors.
 * It is necessary to run reapplyTheme() on startup because Singletons are lazily loaded.
 */
Singleton {
    id: root
    property string filePath: Directories.generatedMaterialThemePath

    function reapplyTheme() {
        themeFileView.reload()
    }

    function applyColors(fileContent) {
        let json
        try {
            json = JSON.parse(fileContent)
            if (!json || Array.isArray(json) || typeof json !== "object" || Object.keys(json).length === 0)
                throw new Error("Expected a non-empty color object")
            // Validate all supported roles before changing any of the palette.
            for (const key of Object.keys(json)) {
                const role = `m3${key.replace(/_([a-z])/g, (g) => g[1].toUpperCase())}`
                if (role in Appearance.m3colors && (typeof json[key] !== "string" || !/^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$/.test(json[key])))
                    throw new Error(`Invalid color: ${key}`)
            }
        } catch (error) {
            console.warn("[MaterialThemeLoader] Keeping last valid palette:", root.filePath, error.message)
            return
        }
        for (const key in json) {
            if (json.hasOwnProperty(key)) {
                // Convert snake_case to CamelCase
                const camelCaseKey = key.replace(/_([a-z])/g, (g) => g[1].toUpperCase())
                const m3Key = `m3${camelCaseKey}`
                if (m3Key in Appearance.m3colors) Appearance.m3colors[m3Key] = json[key]
            }
        }
        Appearance.m3colors.darkmode = (Appearance.m3colors.m3background.hslLightness < 0.5)
        // Custom window border colors are stored as palette roles, so they
        // have to be pushed to Hyprland again whenever the palette changes.
        HyprlandConfig.applyBorderColors()
    }

    function resetFilePathNextTime() {
        resetFilePathNextWallpaperChange.enabled = true
    }

    function useLockTheme() {
        root.filePath = ""
        root.filePath = Directories.generatedLockMaterialThemePath
    }

    function useLiveTheme() {
        root.filePath = ""
        root.filePath = Directories.generatedMaterialThemePath
    }

    Connections {
        id: resetFilePathNextWallpaperChange
        enabled: false
        target: Config.options.background
        function onWallpaperPathChanged() {
            root.filePath = ""
            root.filePath = Directories.generatedMaterialThemePath
            resetFilePathNextWallpaperChange.enabled = false
        }
    }

    Timer {
        id: delayedFileRead
        interval: Config.options?.hacks?.arbitraryRaceConditionDelay ?? 100
        repeat: false
        running: false
        onTriggered: {
            root.applyColors(themeFileView.text())
        }
    }

    FileView {
        id: themeFileView
        path: Qt.resolvedUrl(root.filePath)
        watchChanges: true
        printErrors: false
        onFileChanged: {
            this.reload()
            delayedFileRead.start()
        }
        onLoaded: {
            const fileContent = themeFileView.text()
            root.applyColors(fileContent)
        }
        onLoadFailed: root.resetFilePathNextTime();
    }
}
