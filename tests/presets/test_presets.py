import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import preset_resources as resources
import preset_apply

# A real, tiny SVG; fixtures never depend on private user images.
SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8"><rect width="8" height="8" fill="red"/></svg>'


class PresetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='end4-preset-test-')
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.config = self.home / 'config.json'
        self.original = {'background': {'wallpaperPath': ''}, 'profile': {'displayName': 'local'}}
        self.config.write_text(json.dumps(self.original))
        self.preset = self.home / 'Persona.json'
        self.switch = self.home / 'switchwall.sh'
        self.switch.write_text('#!/bin/bash\nexit 0\n')
        self.switch.chmod(0o755)

    def image(self, name):
        path = self.home / name
        path.parent.mkdir(parents=True, exist_ok=True)
        # Use a real JPEG for the reported PNG/JPEG mismatch.
        svg = self.home / 'fixture.svg'
        svg.write_text(SVG)
        subprocess.run(['magick', str(svg), str(path)], check=True, capture_output=True)
        return path

    def write_preset(self, wallpaper='', **background):
        self.preset.write_text(json.dumps({'background': {'wallpaperPath': str(wallpaper), **background}}))

    def apply(self):
        preset_apply.apply(self.config, self.preset, '.', self.switch)

    def test_png_missing_jpeg_exists_is_suggested_never_automatic(self):
        jpeg = self.image('assets with spaces/wallpaper.jpeg')
        missing = jpeg.with_suffix('.png')
        self.write_preset(missing)
        issues = resources.validate(resources.read_object(self.preset))
        self.assertEqual(issues[0]['candidates'], [str(jpeg)])
        with self.assertRaises(ValueError):
            self.apply()
        self.assertEqual(resources.read_object(self.config), self.original)
        self.assertFalse((self.home / 'backups').exists())

    def test_explicit_repair_backed_up(self):
        jpeg = self.image('wallpaper.jpeg')
        self.write_preset(jpeg.with_suffix('.png'))
        old = self.preset.read_bytes()
        subprocess.run([sys.executable, str(ROOT / 'scripts/preset_resources.py'), str(self.preset), '--repair-missing'], check=True, capture_output=True)
        self.assertEqual(resources.read_object(self.preset)['background']['wallpaperPath'], str(jpeg))
        self.assertEqual(next((self.home / 'backups').iterdir()).read_bytes(), old)

    def test_ambiguous_repair_refused(self):
        self.image('wallpaper.jpeg')
        self.image('wallpaper.webp')
        self.write_preset(self.home / 'wallpaper.png')
        old = self.preset.read_bytes()
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/preset_resources.py'), str(self.preset), '--repair-missing'], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.preset.read_bytes(), old)

    def test_missing_lockwall_blocks_before_commit(self):
        self.write_preset(self.image('wall.jpg'), lockWall=str(self.home / 'lockscreen.png'))
        with self.assertRaisesRegex(ValueError, 'lockWall'):
            self.apply()
        self.assertEqual(resources.read_object(self.config), self.original)
        # A missing asset inherited from the active config must point the user
        # to that file, rather than telling them to repair an unrelated preset.
        self.original['background']['lockWall'] = str(self.home / 'inherited-lockscreen.png')
        self.config.write_text(json.dumps(self.original))
        self.write_preset(self.image('wall.jpg'))
        with self.assertRaises(ValueError) as caught:
            self.apply()
        self.assertIn(str(self.config), str(caught.exception))
        self.assertEqual(resources.read_object(self.config), self.original)

    def test_corrupt_image_refused(self):
        bad = self.home / 'wallpaper.png'
        bad.write_bytes(b'not an image')
        self.write_preset(bad)
        with self.assertRaisesRegex(ValueError, 'imagem inválida'):
            self.apply()

    def test_foreign_user_path_not_guessed(self):
        self.image('wallpaper.jpeg')
        self.write_preset('/home/another-user/wallpaper.jpeg')
        with self.assertRaises(ValueError):
            self.apply()

    def test_switch_failure_restores_exact_bytes(self):
        self.write_preset(self.image('wall paper.jpeg'))
        self.switch.write_text('#!/bin/bash\nexit 19\n')
        before = self.config.read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'restaurada'):
            self.apply()
        self.assertEqual(self.config.read_bytes(), before)
        self.assertEqual(next((self.home / 'backups').glob('*.bak')).read_bytes(), before)

    def test_repeated_alternation_preserves_unrelated_settings(self):
        images = [self.image('Persona/wallpaper.jpeg'), self.image('Maomao v2/wallpaper.png')]
        for i in range(6):
            self.write_preset(images[i % 2], widgets={'glass': {'enable': bool(i % 2)}})
            self.apply()
            data = resources.read_object(self.config)
            self.assertEqual(data['background']['wallpaperPath'], str(images[i % 2]))
            self.assertEqual(data['profile'], self.original['profile'])
            self.assertEqual(data['background']['widgets']['glass']['enable'], bool(i % 2))
        self.assertEqual(len(list((self.home / 'backups').iterdir())), 6)

    def test_success_exit_with_wrong_wallpaper_is_rolled_back(self):
        self.write_preset(self.image('wallpaper.jpeg'))
        self.switch.write_text(f'#!{sys.executable}\nfrom pathlib import Path\nPath({str(self.config)!r}).write_text(\'{{"background":{{"wallpaperPath":"wrong"}}}}\')\n')
        before = self.config.read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'verification'):
            self.apply()
        self.assertEqual(self.config.read_bytes(), before)

    def test_success_exit_with_wrong_glass_setting_is_rolled_back(self):
        self.write_preset(self.image('wallpaper.jpeg'), widgets={'glass': {'enable': True}})
        self.switch.write_text(f'#!{sys.executable}\nimport json\np={str(self.config)!r}\nd=json.load(open(p)); d["background"]["widgets"]["glass"]["enable"]=False\njson.dump(d,open(p,"w"))\n')
        before = self.config.read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'Setting verification'):
            self.apply()
        self.assertEqual(self.config.read_bytes(), before)

    def test_concurrent_applications_are_serialized(self):
        self.write_preset(self.image('wallpaper.jpeg'))
        events = self.home / 'events'
        self.switch.write_text(f'#!{sys.executable}\nimport time\nwith open({str(events)!r}, "a") as f:\n f.write("start\\n"); f.flush(); time.sleep(0.1); f.write("end\\n")\n')
        command = [sys.executable, str(ROOT / 'scripts/preset_apply.py'), str(self.config), str(self.preset), '.', str(self.switch)]
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for process in processes:
            _, stderr = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, stderr)
        self.assertEqual(events.read_text().splitlines(), ['start', 'end', 'start', 'end'])

    def test_shared_sources_skip_missing_file_and_encode_spaces(self):
        image = self.image('space folder/wall.jpeg')
        missing = str(image.with_suffix('.png'))
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/preset_resources.py'), '--sources', json.dumps([str(image), missing, missing])], check=True, capture_output=True, text=True)
        records = json.loads(result.stdout)
        self.assertEqual(records[str(image)]['source'], image.as_uri())
        self.assertEqual(records[missing]['source'], '')
        self.assertEqual(records[missing]['issue']['candidates'], [str(image)])

    def test_collage_and_widget_paths_checked_without_rewriting_text(self):
        data = {'background': {'collage': {'tree': json.dumps({'t': 'leaf', 'img': '/missing.png'})},
                               'widgets': {'imageCard': {'path': '/missing2.png'}}},
                'profile': {'descriptionText': '/this-is-text.png'}}
        self.assertEqual(len(resources.validate(data)), 2)

    def test_file_urls_tilde_and_spaces(self):
        image = self.image('folder with spaces/wall.jpeg')
        self.assertIsNone(resources.inspect_asset(image.as_uri(), 'wallpaper'))
        self.assertEqual(resources.local_path('~/wall.png'), Path.home() / 'wall.png')

    def test_invalid_json_does_not_change_config(self):
        for value in ('', '[]', '{} {}', '{'):
            self.preset.write_text(value)
            with self.assertRaises(ValueError):
                self.apply()
            self.assertEqual(resources.read_object(self.config), self.original)

    def test_shell_writer_rejects_empty_scalar_multiple_and_invalid_json(self):
        before = self.config.read_bytes()
        for value in ('', 'null', '[]', '{} {}', '{'):
            result = subprocess.run(['bash', '-c', 'source "$1"; config_json_replace "$2"', 'test', str(ROOT / 'scripts/lib/config.sh'), str(self.config)], input=value.encode())
            self.assertNotEqual(result.returncode, 0, value)
            self.assertEqual(self.config.read_bytes(), before)

    def test_shell_filter_empty_output_preserves_file(self):
        before = self.config.read_bytes()
        result = subprocess.run(['bash', '-c', 'source "$1"; config_json_update "$2" empty', 'test', str(ROOT / 'scripts/lib/config.sh'), str(self.config)])
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.config.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
