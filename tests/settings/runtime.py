"""Isolated QML scene using real settings/common components and inert services."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]


class Runtime:
    def __init__(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='end4-ux-test-')
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / 'modules/common', self.root / 'modules/common')
        shutil.copytree(ROOT / 'modules/ii', self.root / 'modules/ii')
        services = self.root / 'services'
        services.mkdir()
        (self.root / 'assets').symlink_to(ROOT / 'assets', target_is_directory=True)
        for source in (ROOT / 'services').glob('*.qml'):
            self.stub(source.stem, '')
        for name in ('SettingsHelp.qml', 'SettingsQuickControls.qml', 'SettingsSearchIndex.qml', 'SettingsPages.qml',
                     'SettingsDiagnostics.qml', 'SettingsMetadata.js', 'SettingsSearch.js', 'Fonts.qml'):
            shutil.copy2(ROOT / 'services' / name, services / name)
        self.config = self.root / 'config.json'
        self.config.write_text(json.dumps({'settings': {'style': 'dashboard'}, 'appearance': {'transparency': {'enable': True, 'automatic': True}}}))
        dirs = ['home', 'config', 'state', 'cache', 'genericCache', 'pictures', 'documents', 'downloads', 'music', 'videos']
        values = {key: (self.root / key).as_uri() for key in dirs}
        # No cleanup handlers, autostart, live directories or desktop process.
        values.update({name: str(self.root / name) for name in (
            'shellConfig', 'userPresetsPath', 'userAvatarPathAccountsService', 'userAvatarPathRicersAndWeirdSystems',
            'userAvatarPathRicersAndWeirdSystems2', 'wallpaperSwitchScriptPath', 'presetsScriptPath')})
        values.update(shellConfigPath=str(self.config), scriptPath=str(ROOT / 'scripts'), assetsPath=str(ROOT / 'assets'))
        (self.root / 'modules/common/Directories.qml').write_text('pragma Singleton\nimport Quickshell\nSingleton {\n' +
            '\n'.join(f'property string {key}: {json.dumps(value)}' for key, value in values.items()) + '\n}\n')
        translation = json.loads((ROOT / 'translations/pt_BR.json').read_text())
        self.stub('Translation', 'property bool portuguese: false\nproperty var allAvailableLanguages: ["en_US","pt_BR"]\n'
                  f'property var dictionary: {json.dumps(translation, ensure_ascii=False)}\n'
                  'function tr(text) { return root.portuguese ? (root.dictionary[text] ?? text) : text; }')
        self.stub('WM', 'property string compositor: "hyprland"')
        self.stub('WallpaperResources', 'property string desktopSource: ""\nproperty var resources: ({})')
        self.stub('ColorSchemes', '''property string current: ""
property var currentData: null
property var schemes: ({})
property string userDir: ""
function schemeOptions() { return [{displayName:"Material",value:""}]; }
function materialPreview() { return [{color:"#123456"},{color:"#abcdef"},{color:"#fedcba"}]; }
function accentOptions() { return []; }
function currentAccent() { return ""; }''')
        self.stub('HyprlandOptions', '''property var values: ({})
function get(key, fallback) { return root.values[key] ?? fallback; }
function refresh() {}
function apply() {}''')
        self.stub('HyprlandConfig', '''signal reloaded()
function set() {}
function applyBorderColors() {}
function resetBorderColors() {}''')
        self.stub('SystemAppearance', '''property var fonts: []
property var iconThemes: []
property var cursorThemes: []
property string iconTheme: "test"
property string cursorTheme: "test"
property string fontFamily: "Sans Serif"
property string monoFamily: "Monospace"
property int fontSize: 11
property int monoSize: 11
property int cursorSize: 24
function toOptions(values) { return values.map(value => ({value:value,displayName:value})); }
function fontOptions() { return []; }
function iconPath() { return ""; }''')
        self.stub('DesktopWidgets', '''property var catalog: []
property int enabledCount: 0
function isEnabled() { return false; }
function isStarred() { return false; }''')
        self.stub('Cliphist', 'property bool availabilityKnown: true\nproperty bool available: false')
        self.stub('Weather', 'property bool gpsActive: false\nproperty var location: ({})\nproperty var data: ({})')
        self.stub('SystemInfo', 'property string username: "fixture"\nproperty string distroName: "Fixture OS"')
        self.stub('Webapps', 'property var items: []\nproperty string error: ""')
        self.stub('Collage', 'property bool enabled: false\nfunction layouts() { return []; }')
        self.stub('Presets', 'property bool operationRunning: false\nsignal operationFinished(string operation, string name, bool success)\nfunction isPublished() { return false; }')
        self.stub('PresetsOnline', 'property string downloadingName: ""\nproperty string error: ""\nfunction displayName(name) { return name; }\nfunction isPublished() { return false; }')
        self.stub('DateTime', 'property string time: "12:34"\nproperty string date: "Fixture"')
        global_source = (ROOT / 'GlobalStates.qml').read_text()
        function = global_source[global_source.index('    function openSettingsAt('):global_source.index('    property Item currentPageInstance:')]
        (self.root / 'GlobalStates.qml').write_text('''pragma Singleton
import QtQuick
import Quickshell
import qs.modules.common
Singleton {
id: root
property bool settingsOpen: false
property bool settingsDetailedView: false
property bool settingsDiagnosticsOpen: false
property var settingsTarget: null
property string dashboardGroup: ""
property int dashboardPage: 4
property Item currentPageInstance: null
''' + function + '\n}\n')
        runtime = self.root / 'runtime'
        runtime.mkdir(mode=0o700)
        binary = self.root / 'bin'
        binary.mkdir()
        notifier = binary / 'notify-send'
        notifier.write_text('#!/bin/sh\nexit 0\n')
        notifier.chmod(0o755)
        self.env = {**os.environ, 'HOME': str(self.root), 'XDG_CONFIG_HOME': str(self.root / 'config'),
                    'XDG_STATE_HOME': str(self.root / 'state'), 'XDG_CACHE_HOME': str(self.root / 'cache'),
                    'XDG_RUNTIME_DIR': str(runtime), 'QT_QPA_PLATFORM': 'offscreen', 'QT_QUICK_BACKEND': 'software',
                    'PATH': str(binary) + os.pathsep + os.environ['PATH']}

    def stub(self, name, body):
        (self.root / 'services' / f'{name}.qml').write_text('pragma Singleton\nimport QtQuick\nimport Quickshell\nSingleton {\nid: root\n' + body + '\n}\n')

    def run(self, body, timeout=15):
        shell = '''import QtQuick
import QtQuick.Controls
import Quickshell
import Quickshell.Io
import qs
import qs.modules.common
import qs.modules.common.widgets
import qs.modules.ii.settings
import qs.services
ShellRoot {
''' + body + '\n}\n'
        (self.root / 'shell.qml').write_text(shell)
        return subprocess.run(['qs', '-p', str(self.root), '--no-color'], env=self.env, capture_output=True, text=True, timeout=timeout)

    def close(self):
        self.temporary.cleanup()
