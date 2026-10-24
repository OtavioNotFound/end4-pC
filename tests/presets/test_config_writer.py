from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ConfigWriterTests(unittest.TestCase):
    def test_invalid_input_never_replaces_valid_config(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / 'config.json'
            original = b'{"preserve":true}\n'
            config.write_bytes(original)
            for value in ('', 'null', '[]', '{} {}', '{'):
                result = subprocess.run(['bash', '-c', 'source "$1"; config_json_replace "$2"', 'test', str(ROOT / 'scripts/lib/config.sh'), str(config)], input=value.encode())
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(config.read_bytes(), original)

    def test_valid_object_can_be_saved(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / 'config.json'
            config.write_text('{}')
            subprocess.run(['bash', '-c', 'source "$1"; config_json_replace "$2"', 'test', str(ROOT / 'scripts/lib/config.sh'), str(config)], input=b'{"valid":true}', check=True)
            self.assertEqual(config.read_bytes(), b'{"valid":true}')
