pragma Singleton

import QtQuick
import QtQuick as QQ
import qs.modules.common
import qs.modules.common.functions
import Quickshell
import Quickshell.Io

Singleton {
    id: root
    property string firstRunFilePath: `${Directories.state}/user/first_run.txt`
    property string firstRunFileContent: "This file is just here to confirm you've been greeted :>"
    property string firstRunNotifSummary: "Welcome!"
    property string firstRunNotifBody: "Hit Super+/ for a list of keybinds"
    property string defaultWallpaperPath: FileUtils.trimFileProtocol(`${Directories.assetsPath}/images/default_wallpaper.png`)
    property string welcomeQmlPath: FileUtils.trimFileProtocol(Quickshell.shellPath("welcome.qml"))
    property bool welcomePending: false

    function load() {
        firstRunFileView.reload()
    }

    function enableNextTime() {
        Quickshell.execDetached(["rm", "-f", root.firstRunFilePath])
    }
    function disableNextTime() {
        Quickshell.execDetached(["bash", "-c", `echo '${root.firstRunFileContent}' > '${root.firstRunFilePath}'`])
    }

    function handleFirstRun() {
        if (!Config.ready) { root.welcomePending = true; return; }
        root.welcomePending = false
        if (!Config.options.background.wallpaperPath)
            Quickshell.execDetached([Directories.wallpaperSwitchScriptPath, root.defaultWallpaperPath])
        Quickshell.execDetached(["bash", "-c", `qs -p '${root.welcomeQmlPath}'`])
    }

    QQ.Connections {
        target: Config
        function onReadyChanged() { if (Config.ready && root.welcomePending) root.handleFirstRun(); }
    }

    FileView {
        id: firstRunFileView
        path: Qt.resolvedUrl(firstRunFilePath)
        onLoadFailed: (error) => {
            if (error == FileViewError.FileNotFound) {
                firstRunFileView.setText(root.firstRunFileContent)
                root.handleFirstRun()
            }
        }
    }
}
