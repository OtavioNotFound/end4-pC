"""Execute actual QML JavaScript functions with narrow host API stubs."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]


def function(file, start, end):
    text = (ROOT / file).read_text()
    return text[text.index(f'function {start}'):text.index(f'function {end}')].strip()


@unittest.skipUnless(shutil.which('node'), 'Node unavailable')
class QmlFunctionTests(unittest.TestCase):
    def test_icon_fallback_prefers_theme_then_bundled_svg(self):
        actual = function('services/SystemAppearance.qml', 'defaultIconPath', 'iconPath')
        script = '''const assert = require('assert');
const fs = require('fs');
const root = {};
const Directories = {assetsPath: ASSETS};
const Qt = {resolvedUrl: value => value};
const Quickshell = {iconPath: (name, check) => name === 'theme-present' ? 'image://theme/present' : ''};
root.defaultIconPath = ACTUAL;
assert.equal(root.defaultIconPath('theme-present'), 'image://theme/present');
for (const name of ['cachyos', 'cachyos-symbolic', 'arch-symbolic', 'user-desktop', 'image-missing']) {
  assert(fs.existsSync(root.defaultIconPath(name)));
}
assert.equal(root.defaultIconPath('unknown', true), '');
assert.equal(root.defaultIconPath('unknown', 'theme-present'), 'image://theme/present');
assert(fs.existsSync(root.defaultIconPath('unknown')));
'''.replace('ASSETS', json.dumps(str(ROOT / 'assets'))).replace('ACTUAL', actual)
        subprocess.run(['node', '-e', script], check=True, capture_output=True)

    def test_invalid_palette_never_partially_updates_colors(self):
        actual = function('services/MaterialThemeLoader.qml', 'applyColors', 'resetFilePathNextTime')
        script = '''const assert = require('assert');
const root = {filePath: 'fixture'};
const Appearance = {m3colors: {m3primary: '#123456', m3background: '#000000', darkmode: true}};
let applied = 0;
const HyprlandConfig = {applyBorderColors: () => applied++};
const apply = ACTUAL;
for (const invalid of ['', '{', '[]', '{}', '{"primary":"#abcdef","background":"bad"}']) {
  const before = JSON.stringify(Appearance.m3colors);
  apply(invalid);
  assert.equal(JSON.stringify(Appearance.m3colors), before);
}
assert.equal(applied, 0);
apply('{"primary":"#abcdef"}');
assert.equal(Appearance.m3colors.m3primary, '#abcdef');
assert.equal(applied, 1);
'''.replace('ACTUAL', actual)
        subprocess.run(['node', '-e', script], check=True, capture_output=True)
