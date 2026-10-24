import json
import os
from pathlib import Path
import shutil
import unittest

from runtime import ROOT, Runtime


@unittest.skipUnless(shutil.which('qs'), 'Quickshell required for offscreen settings integration')
class SettingsRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.runtime = Runtime()
        self.addCleanup(self.runtime.close)

    def assert_pass(self, result):
        output = result.stdout + result.stderr
        self.assertIn('UX_TEST_PASS', output, output)
        for error in ('TypeError', 'ReferenceError', 'Unable to assign', 'Cannot assign', 'Binding loop', 'UX_TEST_FAIL'):
            self.assertNotIn(error, output, output)

    def test_dashboard_search_and_navigation_preserve_config(self):
        result = self.runtime.run('''
    Item { id: pager; property string searchQuery: ""; property int wallpapersPage: 1; signal pageExitRequested(); function goToPage(index) {} }
    Window {
        id: window
        visible: true; width: 1100; height: 680
        DashboardSettingsPage { id: page; anchors.fill: parent; anchors.margins: 16; pager: pager }
    }
    property int phase: 0
    Timer {
        running: Config.ready; interval: 250; repeat: true
        onTriggered: {
            if (phase === 1) {
                if (GlobalStates.settingsTarget?.page !== "hyprland") { console.error("UX_TEST_FAIL Hyprland target"); Qt.quit(); return }
                WM.compositor = "niri"
                page.activateAction("displays")
                phase = 2; return
            }
            if (phase === 2) {
                if (GlobalStates.settingsTarget?.page !== "niri" || Config.options.settings.style !== "dashboard") { console.error("UX_TEST_FAIL Niri target"); Qt.quit(); return }
                console.log("UX_TEST_PASS"); Qt.quit(); return
            }
            const style = Config.options.settings.style
            if (!page.matches(["vidro"]).some(entry => entry.key === "interface:Glassy UI")) { console.error("UX_TEST_FAIL glass"); Qt.quit(); return }
            if (!page.matches(["cpu", "temperature"]).length) { console.error("UX_TEST_FAIL conditional"); Qt.quit(); return }
            GlobalStates.dashboardGroup = "bar"
            Translation.portuguese = true
            if (page.group !== "bar") { console.error("UX_TEST_FAIL locale"); Qt.quit(); return }
            page.activateAction("displays")
            if (!GlobalStates.settingsDetailedView || Config.options.settings.style !== style) { console.error("UX_TEST_FAIL navigation"); Qt.quit(); return }
            phase = 1
        }
    }
''')
        self.assert_pass(result)

    def test_diagnostics_uses_existing_doctor_and_displays_private_asset_paths(self):
        self.runtime.config.write_text(json.dumps({'background': {'wallpaperPath': '/fixture/missing-wallpaper.png'}}))
        result = self.runtime.run('''
    Item { id: pager; property string searchQuery: ""; signal pageExitRequested() }
    Window {
        visible: true; width: 1100; height: 680
        DashboardSettingsPage { id: page; anchors.fill: parent; pager: pager }
    }
    Timer {
        running: Config.ready; interval: 150
        onTriggered: page.activateAction("diagnostics")
    }
    Timer {
        running: true; repeat: true; interval: 100
        onTriggered: {
            if (SettingsDiagnostics.completed) {
                if (!page.diagnosisOpen || !SettingsDiagnostics.checks.length || SettingsDiagnostics.assets[0]?.path !== "/fixture/missing-wallpaper.png") {
                    console.error("UX_TEST_FAIL diagnostic assets"); Qt.quit(); return
                }
                console.log("UX_TEST_PASS"); Qt.quit()
            } else if (SettingsDiagnostics.error) { console.error("UX_TEST_FAIL " + SettingsDiagnostics.error); Qt.quit() }
        }
    }
''')
        self.assert_pass(result)

    def test_preset_overwrite_requires_two_clicks_and_success_requires_completion(self):
        result = self.runtime.run('''
    Item { id: pager; property bool editingText: false }
    Window {
        visible: true; width: 1100; height: 680
        DashboardPresetDetail {
            id: detail; anchors.fill: parent; pager: pager
            preset: ({name:"fixture",source:"mine",summary:{origin:"fixture"}})
            onOverwriteRequested: Presets.operationRunning = true
        }
    }
    function find(item) {
        if (item.modelData?.id === "overwrite") return item
        for (let child of item.children ?? []) { const found = find(child); if (found) return found }
        return null
    }
    property int phase: 0
    Timer {
        running: Config.ready; repeat: true; interval: 200
        onTriggered: {
            const button = find(detail)
            if (!button) { console.error("UX_TEST_FAIL overwrite button"); Qt.quit(); return }
            if (phase === 0) { button.clicked(); phase++; }
            else if (phase === 1) {
                if (!detail.confirmOverwrite || detail.overwritten || Presets.operationRunning) { console.error("UX_TEST_FAIL first confirmation"); Qt.quit(); return }
                button.clicked(); phase++
            } else if (phase === 2) {
                if (!Presets.operationRunning || detail.overwritten) { console.error("UX_TEST_FAIL premature success"); Qt.quit(); return }
                Presets.operationRunning = false
                Presets.operationFinished("overwrite", "fixture", false)
                if (detail.overwritten || detail.pendingOperation !== "") { console.error("UX_TEST_FAIL failure shown as success"); Qt.quit(); return }
                detail.pendingOperation = "overwrite"
                Presets.operationFinished("overwrite", "fixture", true)
                if (!detail.overwritten) { console.error("UX_TEST_FAIL missing completion"); Qt.quit(); return }
                console.log("UX_TEST_PASS"); Qt.quit()
            }
        }
    }
''')
        self.assert_pass(result)

    def test_real_preset_service_reports_process_failure(self):
        shutil.copy2(ROOT / 'services/Presets.qml', self.runtime.root / 'services/Presets.qml')
        script = self.runtime.root / 'presetsScriptPath'
        script.write_text('#!/bin/bash\nsleep 0.1\necho "fixture failure" >&2\nexit 9\n')
        result = self.runtime.run('''
    property bool observed: false
    property bool outcome: true
    Connections {
        target: Presets
        function onOperationFinished(operation, name, success) {
            if (operation === "export" && name === "fixture") { observed = true; outcome = success; }
        }
    }
    Timer { running: Config.ready; interval: 100; onTriggered: Presets.exportZip("fixture") }
    Timer {
        running: true; repeat: true; interval: 100
        onTriggered: {
            if (!observed) return
            if (outcome || Presets.operationRunning) console.error("UX_TEST_FAIL service completion")
            else console.log("UX_TEST_PASS")
            Qt.quit()
        }
    }
''')
        self.assert_pass(result)

    def test_diagnostic_failure_is_not_displayed_as_completed(self):
        result = self.runtime.run('''
    Timer {
        running: Config.ready; interval: 100
        onTriggered: { Directories.scriptPath = "/fixture/missing-scripts"; SettingsDiagnostics.run(); }
    }
    Timer {
        running: true; repeat: true; interval: 100
        onTriggered: {
            if (!SettingsDiagnostics.error) return
            if (SettingsDiagnostics.completed || SettingsDiagnostics.checks.length) console.error("UX_TEST_FAIL false completion")
            else console.log("UX_TEST_PASS")
            Qt.quit()
        }
    }
''')
        self.assert_pass(result)

    def test_narrow_style_card_contains_its_buttons_and_help_wraps(self):
        body = '''
    Item { id: pager; property string searchQuery: ""; signal pageExitRequested() }
    Window {
        visible: true; width: TEST_WIDTH; height: TEST_HEIGHT
        DashboardSettingsPage { id: page; anchors.fill: parent; anchors.margins: 16; pager: pager }
        StyledToolTipContent {
            id: tip; maximumWidth: 320
            text: "Uma descrição longa de transparência e wallpaper que deve quebrar em várias linhas para continuar legível em uma janela pequena."
        }
    }
    Component.onCompleted: { Translation.portuguese = true; GlobalStates.dashboardGroup = "general"; }
    function find(item) {
        if (item.modelData?.id === "hero:style") return item.item
        for (let child of item.children ?? []) { const found = find(child); if (found) return found }
        return null
    }
    function contained(item, card) {
        if (typeof item.click === "function") {
            const point = item.mapToItem(card, 0, 0)
            if (point.x < -1 || point.x + item.width > card.width + 1) return false
        }
        return Array.from(item.children ?? []).every(child => contained(child, card))
    }
    Timer {
        running: Config.ready; interval: 1000
        onTriggered: {
            const style = find(page)
            if (!style || !contained(style, style) || tip.implicitWidth > 320 || tip.implicitHeight < 25) console.error("UX_TEST_FAIL responsive bounds")
            else console.log("UX_TEST_PASS")
            Qt.quit()
        }
    }
'''
        for width, height, scale in [(900,600,'1'), (1100,680,'1'), (1366,768,'1.25'), (900,600,'2')]:
            with self.subTest(width=width, height=height, scale=scale):
                self.runtime.env['QT_SCALE_FACTOR'] = scale
                result = self.runtime.run(body.replace('TEST_WIDTH',str(width)).replace('TEST_HEIGHT',str(height)))
                self.assert_pass(result)
        self.assertEqual(json.loads(self.runtime.config.read_text())['settings']['style'], 'dashboard')

    def test_real_controls_refresh_after_external_json_and_keep_manual_values(self):
        result = self.runtime.run('''
    Window {
        visible: true; width: 900; height: 600
        DashboardSliderCard {
            id: slider; width: 400; height: 140
            title: "Background"; controlKey: "interface:Transparency/Background"
        }
    }
    Process {
        id: writer
        command: ["python3","-c","import json,sys;p=sys.argv[1];d=json.load(open(p));d['appearance']['transparency']['automatic']=False;d['appearance']['transparency']['backgroundTransparency']=0.23;json.dump(d,open(p,'w'))",Directories.shellConfigPath]
        onExited: code => verify.restart()
    }
    Timer {
        running: Config.ready; interval: 250
        onTriggered: {
            if (!slider.unavailableReason || slider.current !== 0.11) { console.error("UX_TEST_FAIL automatic values"); Qt.quit(); return }
            writer.running = true
        }
    }
    Timer {
        id: verify; interval: 300
        onTriggered: {
            if (slider.unavailableReason || slider.current !== 0.23) { console.error("UX_TEST_FAIL external reload"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit()
        }
    }
''')
        self.assert_pass(result)
