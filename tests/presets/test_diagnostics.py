import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import doctor


class DiagnosticTests(unittest.TestCase):
    def test_report_does_not_expose_paths_tokens_ssids_or_log_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / 'config.json'
            config.write_text(json.dumps({'background': {'wallpaperPath': '/home/private-person/secret-wall.png'},
                'ai': {'token': 'top-secret-token'}, 'networking': {'ssid': 'private-ssid'}}))
            log = root / 'private.log'
            log.write_text('Could not load icon private-person secret-SSID\ncliphist top-secret-token\n')
            with patch.dict(os.environ, {'XDG_STATE_HOME': str(root / 'state')}):
                report, private = doctor.report(config, log)
            text = json.dumps(report)
            for secret in ('private-person', 'top-secret-token', 'private-ssid', 'secret-SSID', str(root), 'secret-wall.png'):
                self.assertNotIn(secret, text)
            self.assertTrue(private)
            self.assertIn('log:missing-icon', text)

    def test_type_and_range_checks(self):
        issues = doctor.config_issues({'appearance': {'transparency': {'enable': 'true', 'backgroundTransparency': 9}}})
        self.assertEqual(len(issues), 2)

    def test_recover_corrupted_config_preserves_bytes_in_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / 'config.json'
            config.write_text('broken JSON')
            saved = root / 'snapshot.bak'
            saved.write_text('{"background":{"wallpaperPath":""}}')
            subprocess.run([sys.executable, str(ROOT / 'scripts/preset_recover.py'), str(saved), str(config)], check=True, capture_output=True)
            self.assertEqual(config.read_bytes(), saved.read_bytes())
            self.assertEqual(next((root / 'backups').iterdir()).read_text(), 'broken JSON')

    def test_safe_default_is_explicit_and_backed_up(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / 'config.json'
            config.write_text('broken JSON')
            subprocess.run([sys.executable, str(ROOT / 'scripts/preset_recover.py'), '--safe-default', str(config)], check=True, capture_output=True)
            self.assertEqual(json.loads(config.read_text()), {})
            self.assertEqual(next((config.parent / 'backups').iterdir()).read_text(), 'broken JSON')
