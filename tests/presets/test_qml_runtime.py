"""Real QML bindings in a minimal offscreen shell; never start end4-pC itself."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('qs'), 'Quickshell unavailable; run the documented graphical matrix separately')
class QmlRuntimeTests(unittest.TestCase):
    def test_glass_transparency_persistence_and_external_reload(self):
        with tempfile.TemporaryDirectory(prefix='end4-qml-test-') as temporary:
            root = Path(temporary)
            common = root / 'modules/common'
            functions = common / 'functions'
            services = root / 'services'
            functions.mkdir(parents=True)
            services.mkdir()
            config = root / 'config.json'
            wall_a = root / 'a.svg'
            wall_b = root / 'b.svg'
            for wall in (wall_a, wall_b):
                wall.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="2" height="2"><rect width="2" height="2" fill="red"/></svg>')
            config.write_text(json.dumps({'background': {'wallpaperPath': str(wall_a)}}))
            for filename in ('Config.qml', 'Appearance.qml'):
                shutil.copy2(ROOT / 'modules/common' / filename, common / filename)
            shutil.copy2(ROOT / 'modules/common/functions/ColorUtils.qml', functions / 'ColorUtils.qml')
            shutil.copy2(ROOT / 'services/WallpaperResources.qml', services / 'WallpaperResources.qml')
            (common / 'Directories.qml').write_text('pragma Singleton\nimport Quickshell\nSingleton {\n'
                f'property string shellConfigPath: {json.dumps(str(config))}\n'
                f'property string scriptPath: {json.dumps(str(ROOT / "scripts"))}\n'
                'property string videos: "file:///tmp"\n}\n')
            runtime = root / 'runtime'
            runtime.mkdir(mode=0o700)
            env = {**os.environ, 'HOME': str(root), 'XDG_CONFIG_HOME': str(root / 'config'),
                   'XDG_CACHE_HOME': str(root / 'cache'), 'XDG_STATE_HOME': str(root / 'state'),
                   'XDG_RUNTIME_DIR': str(runtime), 'QT_QPA_PLATFORM': 'offscreen',
                   'QT_QUICK_BACKEND': 'software'}
            harness = '''import QtQuick
import Quickshell
import Quickshell.Io
import qs.modules.common
import qs.services
ShellRoot {
    id: root
    property int step: 0
    property int combination: 0
    property string nextWallpaper: NEXT_WALL
    FileView { id: disk; path: Directories.shellConfigPath; blockLoading: true }
    function fail(message) { console.error("TEST_FAILURE: " + message); Qt.quit() }
    Process {
        id: external
        command: ["python3", "-c", "import json,sys; p=sys.argv[1]; d=json.load(open(p)); assert d['appearance']['transparency']['contentTransparency']==0.42; d['background']['widgets']['glass']['enable']=False; json.dump(d,open(p,'w'))", Directories.shellConfigPath]
        onExited: code => {
            if (code !== 0) { root.fail("external writer"); return }
            Config.endPresetUpdate()
            root.step = 3
        }
    }
    Timer {
        interval: 150; running: true; repeat: true
        onTriggered: {
            if (!Config.ready) return
            if (root.step === 0) {
                Config.options.background.widgets.glass.enable = !!(root.combination & 1)
                Config.options.appearance.transparency.enable = !!(root.combination & 2)
                Config.options.appearance.transparency.automatic = !!(root.combination & 4)
                root.step = 1
            } else if (root.step === 1) {
                if (WallpaperResources.desktopSource === "") return
                disk.reload(); disk.waitForJob()
                const saved = JSON.parse(disk.text())
                if (saved.background.widgets.glass.enable !== !!(root.combination & 1)
                    || saved.appearance.transparency.enable !== !!(root.combination & 2)
                    || saved.appearance.transparency.automatic !== !!(root.combination & 4)) {
                    root.fail("persisted switch mismatch"); return
                }
                if (!Number.isFinite(Appearance.backgroundTransparency) || !Number.isFinite(Appearance.contentTransparency)) {
                    root.fail("invalid transparency value"); return
                }
                if (root.combination < 7) { root.combination++; root.step = 0; return }
                Config.options.appearance.transparency.contentTransparency = 0.42
                const previousSource = WallpaperResources.desktopSource
                Config.options.background.wallpaperPath = root.nextWallpaper
                if (WallpaperResources.desktopSource !== previousSource) { root.fail("lost previous image while checking next"); return }
                if (!Config.beginPresetUpdate()) { root.fail("pause writes"); return }
                root.step = 2
                external.running = true
            } else if (root.step === 3) {
                if (!WallpaperResources.desktopSource.endsWith("/b.svg")) return
                if (Config.blockWrites || Config.options.background.widgets.glass.enable !== false) {
                    root.fail("external reload mismatch"); return
                }
                console.log("TEST_PASS: matrix and reload")
                Qt.quit()
            }
        }
    }
}
'''
            shell = root / 'shell.qml'
            shell.write_text(harness.replace('NEXT_WALL', json.dumps(str(wall_b))))
            result = subprocess.run(['qs', '-p', str(root), '--no-color'], env=env, capture_output=True, text=True, timeout=15)
            output = result.stdout + result.stderr
            self.assertIn('TEST_PASS: matrix and reload', output, output)
            self.assertNotIn('TEST_FAILURE', output)
            self.assertNotIn('TypeError', output)
            self.assertNotIn('Unable to assign', output)
            # A second process proves the value survived shell restart.
            shell.write_text('''import QtQuick
import Quickshell
import qs.modules.common
ShellRoot {
    Timer {
        running: Config.ready; interval: 300
        onTriggered: {
            console.log(Config.ready && !Config.options.background.widgets.glass.enable ? "TEST_PASS: restart" : "TEST_FAILURE: restart")
            Qt.quit()
        }
    }
}
''')
            result = subprocess.run(['qs', '-p', str(root), '--no-color'], env=env, capture_output=True, text=True, timeout=10)
            self.assertIn('TEST_PASS: restart', result.stdout + result.stderr)
