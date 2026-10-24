"""Search actual settings sources, not a duplicate catalog or parser."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('node'), 'Node required for settings JavaScript tests')
class SearchTests(unittest.TestCase):
    def run_js(self, script):
        prelude = '''const fs = require('fs'), vm = require('vm'), assert = require('assert');
const rootPath = ROOT;
function load(name) {
 const scope = {};
 vm.createContext(scope);
 vm.runInContext(fs.readFileSync(rootPath + '/services/' + name, 'utf8').replace(/^\\.pragma library\\s*/, ''), scope);
 return scope;
}
const Search = load('SettingsSearch.js'), Metadata = load('SettingsMetadata.js');
'''.replace('ROOT', json.dumps(str(ROOT)))
        result = subprocess.run(['node', '-e', prelude + script], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_normalization_and_all_tokens(self):
        self.run_js('''
assert.equal(Search.normalize('  Transparência_Automática/VIDRO '), 'transparencia automatica vidro');
assert(Search.score('Hyprland monitors resolução', Search.tokens('monitor resolução')) >= 0);
assert.equal(Search.score('Hyprland monitor', Search.tokens('monitor unicorn')), -1);
assert.equal(Search.score('anything', []), -1);
''')

    def test_parser_ignores_literals_comments_and_preserves_nested_context(self):
        fixture = '''ContentSection {
title: Translation.tr("Wallpaper")
// ConfigSwitch { text: Translation.tr("Ghost") }
/* ContentSection { title: Translation.tr("Ghost section")
} */
ConfigTextArea {
placeholderText: `{"key": "value"}`
text: Translation.tr("Image path")
description: Translation.tr("Choose a local file")
}
ContentSubsection {
title: Translation.tr("Lock screen")
ConfigSwitch {
text: Translation.tr("Enabled")
}
}
ConfigSwitch {
text: Translation.tr("Preview")
}
}'''
        self.run_js('''
const entries = Search.parsePage(FIXTURE, ['ConfigTextArea', 'ConfigSwitch', 'ContentSubsection']);
assert.deepEqual(Array.from(entries, entry => entry.label), ['Wallpaper','Image path','Lock screen','Enabled','Preview']);
assert.equal(entries[1].description, 'Choose a local file');
assert.equal(entries[3].section, 'Wallpaper');
assert.equal(entries[3].subsection, 'Lock screen');
assert.equal(entries[4].subsection, '');
'''.replace('FIXTURE', json.dumps(fixture)))

    def test_real_pages_include_monitors_dock_fonts_and_transparency(self):
        self.run_js('''
const types = ['ConfigSwitch','ConfigSpinBox','ConfigTextArea','ConfigSelectionArray','ConfigComboBox','ConfigSlider','ConfigSelectionShapeArray','ConfigRow','ColorSelectionArray','ContentSubsection'];
for (const [file, expected] of [
 ['HyprlandConfig.qml', ['Displays','Resolution & Refresh Rate','Scale']],
 ['InterfaceConfig.qml', ['Transparency','Automatic (from wallpaper)','Dock','Main font']],
 ['ServicesConfig.qml', ['Weather','City name']]]) {
 const source = fs.readFileSync(rootPath+'/modules/ii/settings/pages/'+file,'utf8');
 const labels = Search.parsePage(source, types).map(entry => entry.label);
 for (const label of expected) assert(labels.includes(label), file + ': ' + label);
}
''')

    def test_dashboard_finds_glass_and_conditional_widget_without_duplicates(self):
        self.run_js('''
const Translation = {tr: text => text};
let source = fs.readFileSync(rootPath+'/modules/ii/settings/DashboardSettingsCatalog.qml','utf8');
let array = source.slice(source.indexOf('readonly property var sections:') + 'readonly property var sections:'.length);
array = array.slice(0, array.lastIndexOf(']')+1);
const sections = vm.runInNewContext(array, {Translation});
source = fs.readFileSync(rootPath+'/modules/ii/settings/DashboardSettingsPage.qml','utf8');
array = source.slice(source.indexOf('readonly property var heroEntries:')+'readonly property var heroEntries:'.length);
array = array.slice(0, array.indexOf(String.fromCharCode(10)+'    ]')+6);
const heroes = vm.runInNewContext(array, {Translation, WM:{compositor:'hyprland'}});
const allEntries = heroes.map(entry => ({...entry, kind:'card',hero:true}));
sections.forEach(section => section.cards.forEach(card => allEntries.push({...card,kind:'card',section:section.title,group:section.page, requires:section.requires})));
const code = source.slice(source.indexOf('function matches('),source.indexOf('function isEnableCard('));
const SettingsHelp = {compatible: () => true};
const find = new Function('allEntries','Metadata','Search','Translation','SettingsHelp','Wallpapers',code+'; return matches;')(allEntries,Metadata,Search,Translation,SettingsHelp,{});
for (const query of ['glassy', 'vidro', 'cliphist', 'levenshtein', 'dock magnify']) {
 const found = find(Search.tokens(query));
 assert(found.length > 0, query);
 assert.equal(new Set(found.map(entry => entry.key || entry.id)).size, found.length, 'duplicate '+query);
}
assert(find(Search.tokens('CPU temperature')).some(entry => entry.requires === 'resources'));
''')

    def test_category_identifiers_are_stable_and_accept_legacy_labels(self):
        self.run_js('''
for (const [label, expected] of [['Interface','interface'],['Aparência','interface'],['Bar','bar'],['Barra','bar'],['Desktop','desktop'],['Services','services']]) {
 assert.equal(Metadata.category(label), expected);
 assert.equal(Metadata.category(expected), expected);
}
assert.equal(Metadata.categoryTitle('bar'), 'Bar & dock');
''')

    def test_units_use_actual_values_and_metadata_is_translated(self):
        self.run_js('''
assert.equal(Metadata.displayValue('interface:Transparency/Background',0.11,true,0,0.6),'11%');
assert.equal(Metadata.displayValue('interface:Transparency/Background',0.6,true,0,0.6),'60%');
assert.equal(Metadata.displayValue('desktop:Blur Size',32,false,1,64),'32 px');
assert.equal(Metadata.displayValue('services:Polling interval (m)',10,false,5,50),'10 min');
const english = JSON.parse(fs.readFileSync(rootPath+'/translations/en_US.json','utf8'));
const portuguese = JSON.parse(fs.readFileSync(rootPath+'/translations/pt_BR.json','utf8'));
for (const data of Object.values(Metadata.entries)) {
 for (const property of ['title','description','effect']) {
  if (!data[property]) continue;
  assert(english[data[property]], 'missing English: '+data[property]);
  assert(portuguese[data[property]], 'missing Portuguese: '+data[property]);
 }
}
''')

    def test_first_run_preserves_existing_wallpaper_and_waits_for_config(self):
        self.run_js('''
const source = fs.readFileSync(rootPath+'/services/FirstRunExperience.qml','utf8');
const body = source.slice(source.indexOf('function handleFirstRun()'),source.indexOf('    Connections {'));
const calls = [];
const root = {welcomePending:false,defaultWallpaperPath:'/default.png',welcomeQmlPath:'/welcome.qml'};
const Config = {ready:false,options:{background:{wallpaperPath:'/existing.jpeg'}}};
const Directories = {wallpaperSwitchScriptPath:'/switchwall.sh'};
const Quickshell = {execDetached: command => calls.push(command)};
const handle = new Function('root','Config','Directories','Quickshell',body+';return handleFirstRun;')(root,Config,Directories,Quickshell);
handle(); assert(root.welcomePending); assert.equal(calls.length,0);
Config.ready = true; handle(); assert.equal(calls.length,1); assert.equal(calls[0][0],'bash');
Config.options.background.wallpaperPath = ''; calls.length = 0; handle();
assert.equal(calls[0][0],'/switchwall.sh');
''')

    def test_section_only_navigation_uses_existing_page_api(self):
        self.run_js('''
const source = fs.readFileSync(rootPath+'/modules/ii/settings/SettingsContent.qml','utf8');
const code = source.slice(source.indexOf('function goToTarget('),source.indexOf('    Connections {'));
const calls = [];
const root = {pages:[{id:'hyprland'}],currentPage:-1,showingProfile:true};
const pagesRepeater = {itemAt: index => ({item:{goTo: (...args) => calls.push(args)}})};
const navigate = new Function('root','pagesRepeater',code+';return goToTarget;')(root,pagesRepeater);
navigate({page:'hyprland',label:'',section:'Displays',subsection:''});
assert.equal(root.currentPage,0);
assert.equal(root.showingProfile,false);
assert.deepEqual(calls,[['','Displays','']]);
''')
