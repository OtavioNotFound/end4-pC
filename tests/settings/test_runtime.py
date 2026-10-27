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
        for error in ('TypeError', 'ReferenceError', 'Unable to assign', 'Cannot assign', 'Binding loop', 'UX_TEST_FAIL', 'Failed to load configuration', 'is not installed'):
            self.assertNotIn(error, output, output)

    def test_real_first_run_service_loads_without_launching_welcome(self):
        shutil.copy2(ROOT / 'services/FirstRunExperience.qml', self.runtime.root / 'services/FirstRunExperience.qml')
        marker = self.runtime.root / 'state/user/first_run.txt'
        marker.parent.mkdir(parents=True)
        marker.write_text('Existing user fixture')
        result = self.runtime.run('''
    Component.onCompleted: FirstRunExperience.load()
    Timer {
        running: true; interval: 400
        onTriggered: {
            if (FirstRunExperience.welcomePending) { console.error("UX_TEST_FAIL unexpected welcome"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit()
        }
    }
''')
        self.assert_pass(result)
        self.assertEqual(marker.read_text(), 'Existing user fixture')

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


    def test_bar_editor_moves_configures_and_undoes_without_dragging(self):
        result = self.runtime.run('''
    Window { visible: true; width: 1100; height: 1000
        DashboardBarLayoutCard { id: editor; anchors.fill: parent; title: "Bar" }
    }
    property int phase: 0
    Timer { running: Config.ready; interval: 200; repeat: true
        onTriggered: {
            if (phase === 0) {
                editor.selectItem("workspaces", "left", 1);
                if (!editor.selectedEntries.length) { console.error("UX_TEST_FAIL no inline options"); Qt.quit(); return }
                editor.actOnSelection("right", 0);
                if (!BarLayout.lists.right.includes("workspaces") || !BarLayout.canUndo) { console.error("UX_TEST_FAIL move"); Qt.quit(); return }
                phase = 1; return;
            }
            if (phase === 1) {
                const control = SettingsQuickControls.controls["bar:Workspaces shown"];
                control.set(6);
                if (Config.options.bar.workspaces.shown !== 6) { console.error("UX_TEST_FAIL configure"); Qt.quit(); return }
                BarLayout.undo();
                if (BarLayout.lists.left[1] !== "workspaces" || Config.options.bar.workspaces.shown !== 6) { console.error("UX_TEST_FAIL scoped undo"); Qt.quit(); return }
                editor.selectItem("media", "tray", 0); editor.actOnSelection("right", 0);
                Config.options.bar.layouts.leftLayout = ["unknown-future-item"];
                if (BarLayout.undo() || !BarLayout.lists.left.includes("unknown-future-item")) { console.error("UX_TEST_FAIL external conflict"); Qt.quit(); return }
                console.log("UX_TEST_PASS"); Qt.quit();
            }
        }
    }
''')
        self.assert_pass(result)

    def test_bar_editor_explains_unavailable_items_and_blocks_preset_writes(self):
        result = self.runtime.run('''
    Window { visible: true; width: 900; height: 1100
        DashboardBarLayoutCard { id: editor; anchors.fill: parent }
    }
    Timer { running: Config.ready; interval: 250
        onTriggered: {
            Config.options.bar.vertical = true;
            editor.selectItem("dynamicIsland", "tray", 0);
            if (!editor.trayIds.includes("dynamicIsland") || !BarLayout.reason("dynamicIsland", "middle", true)) { console.error("UX_TEST_FAIL restriction"); Qt.quit(); return }
            const before = BarLayout.signature;
            editor.actOnSelection("middle", 0);
            if (before !== BarLayout.signature) { console.error("UX_TEST_FAIL incompatible edit"); Qt.quit(); return }
            Config.blockWrites = true;
            if (BarLayout.clear() || before !== BarLayout.signature) { console.error("UX_TEST_FAIL preset lock"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit();
        }
    }
''')
        self.assert_pass(result)


    def test_dock_page_and_pinned_apps_keep_unknown_entries(self):
        result = self.runtime.run('''
    Window { visible: true; width: 1000; height: 720
        Loader { id: dockPage; anchors.fill: parent; source: "modules/ii/settings/pages/DockConfig.qml" }
    }
    Timer { running: Config.ready; interval: 300
        onTriggered: {
            if (!dockPage.item) { console.error("UX_TEST_FAIL dock page"); Qt.quit(); return }
            Config.options.dock.pinnedApps = ["unknown-future-app", "kitty"];
            if (!TaskbarApps.movePinned("kitty", -1) || Config.options.dock.pinnedApps[1] !== "unknown-future-app") { console.error("UX_TEST_FAIL reorder"); Qt.quit(); return }
            TaskbarApps.togglePin("kitty");
            if (Config.options.dock.pinnedApps.length !== 1 || Config.options.dock.pinnedApps[0] !== "unknown-future-app") { console.error("UX_TEST_FAIL unpin"); Qt.quit(); return }
            Config.blockWrites = true;
            TaskbarApps.togglePin("blocked");
            if (Config.options.dock.pinnedApps.length !== 1) { console.error("UX_TEST_FAIL preset lock"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit();
        }
    }
''')
        self.assert_pass(result)
        self.assertNotIn('Error loading', result.stdout + result.stderr)

    def test_monitor_selection_preserves_disconnected_names_and_never_selects_none(self):
        result = self.runtime.run('''
    Window { visible: true; width: 800; height: 500
        SettingsScreenSelection { id: selector; anchors.fill: parent; configPath: "dock.screenList"; screenNames: ["DP-1", "HDMI-A-1"] }
    }
    Timer { running: Config.ready; interval: 250
        onTriggered: {
            if (selector.selected.length) { console.error("UX_TEST_FAIL old preset default"); Qt.quit(); return }
            selector.setScreen("DP-1", false);
            if (JSON.stringify(selector.selected) !== '["HDMI-A-1"]') { console.error("UX_TEST_FAIL select"); Qt.quit(); return }
            selector.setScreen("HDMI-A-1", false);
            if (selector.selected.length !== 1 || !selector.message) { console.error("UX_TEST_FAIL none"); Qt.quit(); return }
            Config.options.dock.screenList = ["disconnected"];
            if (!selector.names.includes("disconnected")) { console.error("UX_TEST_FAIL lost disconnected"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit();
        }
    }
''')
        self.assert_pass(result)

    def test_widget_page_keeps_content_and_recovers_only_position(self):
        result = self.runtime.run('''
    Window { visible: true; width: 900; height: 700
        Loader { id: page; anchors.fill: parent; source: "modules/ii/settings/pages/WidgetsConfig.qml" }
    }
    property int phase: 0
    Timer { running: Config.ready; interval: 200; repeat: true
        onTriggered: {
            if (!page.item) { console.error("UX_TEST_FAIL page load"); Qt.quit(); return }
            const key = ["clock", "weather", "resources", "media", "customText"][phase];
            if (key) {
                DesktopWidgets.select(key);
                if (!page.item.entries.length) { console.error("UX_TEST_FAIL missing widget controls " + key); Qt.quit(); return }
                phase++; return;
            }
            const entry = Config.options.background.widgets.customText;
            entry.content = "Personal fixture text"; entry.x = 9999; entry.y = -100; entry.placementStrategy = "free";
            DesktopWidgets.setEnabled("customText", true);
            DesktopWidgets.setStarred("customText", false);
            if (!entry.enable || DesktopWidgets.isStarred("customText")) { console.error("UX_TEST_FAIL state"); Qt.quit(); return }
            DesktopWidgets.recoverPosition("customText");
            if (entry.x !== 24 || entry.content !== "Personal fixture text" || !DesktopWidgets.canUndoPosition) { console.error("UX_TEST_FAIL recovery"); Qt.quit(); return }
            DesktopWidgets.undoPosition();
            if (entry.x !== 9999 || entry.content !== "Personal fixture text") { console.error("UX_TEST_FAIL position undo"); Qt.quit(); return }
            DesktopWidgets.recoverPosition("customText"); entry.x = 200;
            if (DesktopWidgets.undoPosition()) { console.error("UX_TEST_FAIL external conflict"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit();
        }
    }
''')
        self.assert_pass(result)


    def test_native_bar_buttons_have_labels_and_control_the_actual_editor(self):
        result = self.runtime.run('''
    Window { visible: true; width: 900; height: 1100
        DashboardBarLayoutCard { id: editor; anchors.fill: parent }
    }
    function find(item, predicate) {
        if (predicate(item)) return item;
        for (const child of item.children ?? []) { const match = find(child, predicate); if (match) return match; }
        return null;
    }
    property int phase: 0
    Timer { running: Config.ready; interval: 250; repeat: true
        onTriggered: {
            if (phase === 0) { editor.selectItem("workspaces", "left", 1); phase++; return }
            if (phase === 1) {
                const button = find(editor, item => item.buttonText === "Move to Right");
                if (!button || button.width < 50 || button.height < 20 || !button.enabled) { console.error("UX_TEST_FAIL invisible movement button"); Qt.quit(); return }
                button.click(); phase++; return;
            }
            if (phase === 2) {
                if (!BarLayout.lists.right.includes("workspaces")) { console.error("UX_TEST_FAIL actual click"); Qt.quit(); return }
                const spin = find(editor, item => item.text === "Workspaces shown" && typeof item.valueModified === "function");
                if (!spin) { console.error("UX_TEST_FAIL inline spin"); Qt.quit(); return }
                spin.value = 7; spin.valueModified();
                if (Config.options.bar.workspaces.shown !== 7) { console.error("UX_TEST_FAIL actual spin"); Qt.quit(); return }
                editor.selectItem("resources", "tray", 0); editor.actOnSelection("right", 0); phase++; return;
            }
            const toggle = find(editor, item => item.text === "CPU" && typeof item.click === "function");
            if (!toggle) { console.error("UX_TEST_FAIL inline switch"); Qt.quit(); return }
            toggle.click();
            if (Config.options.bar.resources.alwaysShowCpu) { console.error("UX_TEST_FAIL switch off"); Qt.quit(); return }
            toggle.click();
            if (!Config.options.bar.resources.alwaysShowCpu) { console.error("UX_TEST_FAIL switch on"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit();
        }
    }
''')
        self.assert_pass(result)


    def test_resource_widget_renders_new_choices_with_original_defaults(self):
        self.runtime.stub('ResourceUsage', 'property int consumers: 0\nproperty real cpuUsage: 0.25\nproperty real memoryUsedPercentage: 0.5\nproperty real diskUsedPercentage: 0.4')
        self.runtime.stub('Battery', 'property bool available: false\nproperty real percentage: 0.7')
        result = self.runtime.run('''
    Window { visible: true; width: 900; height: 700
        Loader {
            id: preview
            Component.onCompleted: setSource("modules/ii/background/widgets/resources/ResourcesWidget.qml", {
                screenWidth: 900, screenHeight: 700, scaledScreenWidth: 900, scaledScreenHeight: 700, wallpaperScale: 1
            })
        }
    }
    property int phase: 0
    Timer { running: Config.ready; interval: 300; repeat: true
        onTriggered: {
            if (!preview.item) { console.error("UX_TEST_FAIL resource load"); Qt.quit(); return }
            if (phase === 0) {
                if (preview.item.implicitWidth !== 420 || preview.item.implicitHeight !== 120) { console.error("UX_TEST_FAIL original dimensions"); Qt.quit(); return }
                Config.options.background.widgets.resources.showCpu = false;
                Config.options.background.widgets.resources.thirdMetric = "none";
                phase++; return;
            }
            if (phase === 1) {
                if (preview.item.implicitWidth >= 420) { console.error("UX_TEST_FAIL hidden measurements"); Qt.quit(); return }
                Config.options.background.widgets.resources.vertical = true;
                Config.options.background.widgets.resources.showCpu = true;
                Config.options.background.widgets.resources.thirdMetric = "disk";
                phase++; return;
            }
            if (preview.item.implicitHeight <= 120 || preview.item.implicitWidth >= 420) { console.error("UX_TEST_FAIL vertical layout"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit();
        }
    }
''', imports='import qs.modules.ii.background.widgets.resources\nimport qs.modules.ii.background.widgets\nimport qs.modules.common.widgets.widgetCanvas')
        self.assert_pass(result)


    def test_widget_combo_shows_current_value_and_handles_native_selection(self):
        result = self.runtime.run('''
    Window { visible: true; width: 900; height: 700
        Loader { id: page; anchors.fill: parent; source: "modules/ii/settings/pages/WidgetsConfig.qml" }
    }
    function find(item, name) {
        if (item.objectName === name) return item;
        for (const child of item.children ?? []) { const match = find(child, name); if (match) return match; }
        return null;
    }
    property int phase: 0
    Timer { running: Config.ready; interval: 200; repeat: true
        onTriggered: {
            if (phase === 0) { DesktopWidgets.select("resources"); phase++; return }
            const combo = find(page, "inline:desktop:Resources third metric");
            if (!combo) { console.error("UX_TEST_FAIL resource combo"); Qt.quit(); return }
            if (phase === 1) {
                if (combo.displayText !== "Automatic: battery or disk") { console.error("UX_TEST_FAIL missing current label " + combo.displayText); Qt.quit(); return }
                combo.activated(3); phase++; return;
            }
            if (combo.displayText !== "Hidden" || Config.options.background.widgets.resources.thirdMetric !== "none") { console.error("UX_TEST_FAIL native selection"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit();
        }
    }
''')
        self.assert_pass(result)


    def test_bar_actions_fit_narrow_native_page_and_dashboard(self):
        for width in (600, 810, 1100):
            with self.subTest(width=width):
                result = self.runtime.run('''
    Window { visible: true; width: WIDTH; height: 1100
        DashboardBarLayoutCard { id: editor; anchors.fill: parent }
    }
    function visit(item) {
        if (item.objectName === "barAction" && item.visible) {
            const point = item.mapToItem(editor, 0, 0);
            if (point.x < -1 || point.x + item.width > editor.width + 1 || item.height < 20) return false;
        }
        return (item.children ?? []).every(visit);
    }
    Timer { running: Config.ready; interval: 150; onTriggered: { Translation.portuguese = true; editor.selectItem("workspaces", "left", 1); } }
    Timer { running: true; interval: 600; onTriggered: {
        if (!visit(editor)) { console.error("UX_TEST_FAIL clipped actions"); Qt.quit(); return }
        console.log("UX_TEST_PASS"); Qt.quit();
    } }
'''.replace('WIDTH', str(width)))
                self.assert_pass(result)


    def test_media_layout_tracks_config_after_desktop_resize(self):
        self.runtime.stub('MprisController', 'property var activePlayer: null\nproperty var players: []')
        self.runtime.stub('LyricsService', 'property var slots: []\nproperty int before: 3\nproperty string status: "empty"')
        dirs = self.runtime.root / 'modules/common/Directories.qml'
        dirs.write_text(dirs.read_text().replace('Singleton {', 'Singleton {\nproperty string coverArt: "' + str(self.runtime.root / 'cover-art') + '"'))
        result = self.runtime.run('''
    Window { visible: true; width: 900; height: 700
        Loader { id: preview; Component.onCompleted: setSource("modules/ii/background/widgets/media/MediaWidget.qml", {
            screenWidth: 900, screenHeight: 700, scaledScreenWidth: 900, scaledScreenHeight: 700, wallpaperScale: 1
        }) }
    }
    function findHandle(item) {
        if (typeof item.resizedXY === "function") return item;
        for (const child of item.children ?? []) { const match = findHandle(child); if (match) return match; }
        return null;
    }
    property int phase: 0
    Timer { running: Config.ready; interval: 250; repeat: true
        onTriggered: {
            if (!preview.item) { console.error("UX_TEST_FAIL media load"); Qt.quit(); return }
            if (phase === 0) {
                const handle = findHandle(preview.item);
                if (!handle) { console.error("UX_TEST_FAIL resize handle"); Qt.quit(); return }
                handle.resizedXY(-300, 0, 420); handle.resizeFinished();
                Config.options.background.widgets.media.sizeMode = "2x3";
                phase++; return;
            }
            if (preview.item.sizeMode !== "2x3" || preview.item.widgetWidth !== preview.item.snapWidth3) { console.error("UX_TEST_FAIL media config binding"); Qt.quit(); return }
            console.log("UX_TEST_PASS"); Qt.quit();
        }
    }
''', imports='import qs.modules.ii.background.widgets.media\nimport qs.modules.common.models\nimport qs.modules.ii.background.widgets\nimport qs.modules.common.widgets.widgetCanvas')
        self.assert_pass(result)
