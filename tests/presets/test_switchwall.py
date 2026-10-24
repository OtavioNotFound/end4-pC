"""Run switchwall with isolated paths and fake system commands, never the desktop."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class SwitchwallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='end4-switchwall-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        scripts = self.root / 'scripts'
        (scripts / 'colors').mkdir(parents=True)
        (scripts / 'lib').mkdir()
        self.script = scripts / 'colors/switchwall.sh'
        shutil.copy2(ROOT / 'scripts/colors/switchwall.sh', self.script)
        shutil.copy2(ROOT / 'scripts/lib/config.sh', scripts / 'lib/config.sh')
        binary = self.root / 'bin'
        binary.mkdir()
        for name in ('gsettings', 'bc', 'pkill', 'notify-send', 'matugen'):
            self.binary(binary / name, '#!/bin/bash\nexit 0\n')
        self.binary(binary / 'hyprctl', f'#!{sys.executable}\nimport json,sys\nprint(json.dumps([{{"focused":True,"scale":1,"x":0,"y":0,"width":1920,"height":1080,"name":"test"}}] if sys.argv[1]=="monitors" else {{"x":1,"y":1}}))\n')
        config_home = self.root / 'config'
        config_dir = config_home / 'illogical-impulse'
        config_dir.mkdir(parents=True)
        (config_home / 'hypr/custom/scripts').mkdir(parents=True)
        image = self.root / 'wall.svg'
        image.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>')
        (config_dir / 'config.json').write_text(json.dumps({
            'background': {'wallpaperPath': str(image), 'widgets': {'clock': {'cookie': {'aiStyling': False}}}},
            'appearance': {'palette': {'type': 'scheme-tonal-spot'}, 'wallpaperTheming': {'enableAppsAndShell': True}}}))
        self.env = {**os.environ, 'HOME': str(self.root), 'PATH': str(binary) + os.pathsep + os.environ['PATH'],
                    'XDG_CONFIG_HOME': str(config_home), 'XDG_STATE_HOME': str(self.root / 'state'),
                    'XDG_CACHE_HOME': str(self.root / 'cache'), 'XDG_RUNTIME_DIR': str(self.root / 'runtime'),
                    'ILLOGICAL_IMPULSE_VIRTUAL_ENV': str(self.root / 'venv')}
        self.bin = binary

    def binary(self, path, content):
        path.write_text(content)
        path.chmod(0o755)

    def test_matugen_failure_is_returned_to_preset_transaction(self):
        self.binary(self.bin / 'matugen', '#!/bin/bash\necho "fixture failure" >&2\nexit 41\n')
        result = subprocess.run(['bash', str(self.script), '--noswitch'], env=self.env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 41, result.stderr)
        self.assertIn('matugen failed', result.stderr)

    def test_python_color_failure_keeps_previous_scss(self):
        venv = self.root / 'venv/bin'
        venv.mkdir(parents=True)
        (venv / 'activate').write_text('deactivate() { :; }\n')
        generated = self.root / 'state/quickshell/user/generated'
        generated.mkdir(parents=True)
        scss = generated / 'material_colors.scss'
        scss.write_text('last valid palette')
        (self.script.parent / 'generate_colors_material.py').write_text('raise SystemExit(23)\n')
        result = subprocess.run(['bash', str(self.script), '--noswitch'], env=self.env, capture_output=True, text=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('previous SCSS preserved', result.stderr)
        self.assertEqual(scss.read_text(), 'last valid palette')
