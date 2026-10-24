import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='end4-ux-backend-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        folder = self.root / 'config/illogical-impulse'
        folder.mkdir(parents=True)
        self.config = folder / 'config.json'
        self.config.write_text('{"dock":{"enable":true}}')
        self.presets = folder / 'presets'
        self.env = {**os.environ, 'HOME': str(self.root), 'XDG_CONFIG_HOME': str(self.root / 'config'),
                    'XDG_CACHE_HOME': str(self.root / 'cache'), 'XDG_STATE_HOME': str(self.root / 'state')}

    def command(self, *args):
        return ['bash', str(ROOT / 'scripts/presets.sh'), *args]

    def test_create_only_refuses_existing_and_legacy_overwrite_keeps_working(self):
        subprocess.run(self.command('--save', 'Persona', '--create-only'), env=self.env, check=True, capture_output=True)
        preset = self.presets / 'Persona.json'
        before = preset.read_bytes()
        self.config.write_text('{"dock":{"enable":false}}')
        failed = subprocess.run(self.command('--save', 'Persona', '--create-only'), env=self.env, capture_output=True)
        self.assertEqual(failed.returncode, 3)
        self.assertEqual(preset.read_bytes(), before)
        subprocess.run(self.command('--save', 'Persona'), env=self.env, check=True, capture_output=True)
        self.assertFalse(json.loads(preset.read_text())['dock']['enable'])
        self.assertEqual(next((self.presets / 'backups').glob('*.bak')).read_bytes(), before)

    def test_concurrent_create_does_not_overwrite(self):
        processes = [subprocess.Popen(self.command('--save', 'same', '--create-only'), env=self.env,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for process in processes:
            process.communicate(timeout=10)
        self.assertEqual(sorted(p.returncode for p in processes), [0, 3])
        self.assertTrue(json.loads((self.presets / 'same.json').read_text())['dock']['enable'])

    def test_local_diagnostics_are_read_only_and_report_stays_sanitized(self):
        self.config.write_text(json.dumps({'background': {'wallpaperPath': str(self.root / 'private-wallpaper.png')}}))
        before = self.config.read_bytes()
        def run(flag):
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/doctor.py'), '--config', str(self.config), flag], env=self.env, capture_output=True, text=True)
            self.assertIn(result.returncode, (0, 1), result.stderr)
            return json.loads(result.stdout)
        local = run('--local-json')
        self.assertEqual(local['assets'][0]['path'], str(self.root / 'private-wallpaper.png'))
        report = run('--report')
        self.assertNotIn('assets', report)
        self.assertNotIn(str(self.root), json.dumps(report))
        self.assertEqual(self.config.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
