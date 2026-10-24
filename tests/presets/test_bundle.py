import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import preset_bundle as bundle
import preset_install
from preset_resources import read_object, validate

SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8"><rect width="8" height="8" fill="red"/></svg>'


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='end4-bundle-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.preset = self.root / 'Persona teste.json'
        self.exports = self.root / 'exports'
        self.imports = self.root / 'imports'
        self.wall = self.root / 'wall paper.svg'
        self.wall.write_text(SVG)
        self.preset.write_text(json.dumps({'background': {'wallpaperPath': str(self.wall)}}))

    def roundtrip(self):
        bundle.export(self.preset, self.exports, '.')
        bundle.import_zip(self.exports / f'{self.preset.stem}.zip', self.imports, '.')
        return read_object(next(self.imports.glob('*.json')))

    def test_portable_manifest_and_roundtrip(self):
        data = self.roundtrip()
        self.assertEqual(validate(data), [])
        with zipfile.ZipFile(self.exports / f'{self.preset.stem}.zip') as archive:
            portable = archive.read(self.preset.name).decode()
            self.assertNotIn(str(self.root), portable)
            self.assertEqual(json.loads(archive.read('asset-manifest.json'))['version'], 1)

    def test_same_basename_different_files_not_overwritten(self):
        other = self.root / 'another' / self.wall.name
        other.parent.mkdir()
        other.write_text(SVG.replace('red', 'blue'))
        self.preset.write_text(json.dumps({'background': {'wallpaperPath': str(self.wall), 'lockWall': str(other)}}))
        data = self.roundtrip()
        background = data['background']
        self.assertNotEqual(background['wallpaperPath'], background['lockWall'])
        self.assertNotEqual(Path(background['wallpaperPath']).read_bytes(), Path(background['lockWall']).read_bytes())

    def test_legacy_foreign_path_relocated_only_to_bundle(self):
        archive = self.root / 'legacy.zip'
        with zipfile.ZipFile(archive, 'w') as output:
            output.writestr('legacy/Persona.json', json.dumps({'background': {'wallpaperPath': '/home/foreign/wall.svg'}}))
            output.writestr('legacy/wall.svg', SVG)
            output.writestr('legacy/meta.json', '{}')
        bundle.import_zip(archive, self.imports, '.')
        self.assertEqual(validate(read_object(self.imports / 'Persona.json')), [])

    def test_zip_traversal_and_ambiguous_json_refused(self):
        for members in ({'../escape': 'bad', 'preset.json': '{}'}, {'one.json': '{}', 'two.json': '{}'}):
            archive = self.root / 'bad.zip'
            with zipfile.ZipFile(archive, 'w') as output:
                for name, data in members.items():
                    output.writestr(name, data)
            with self.assertRaises(ValueError):
                bundle.import_zip(archive, self.imports, '.')
            self.assertFalse(list(self.imports.glob('*.json')))

    def test_import_twice_does_not_replace_first(self):
        self.roundtrip()
        before = (self.imports / self.preset.name).read_bytes()
        bundle.import_zip(self.exports / f'{self.preset.stem}.zip', self.imports, '.')
        self.assertEqual((self.imports / self.preset.name).read_bytes(), before)
        self.assertTrue((self.imports / f'{self.preset.stem}_2.json').exists())

    def test_avatar_directory_tracks_portable_image(self):
        self.preset.write_text(json.dumps({'profile': {'avatarPicture': str(self.wall), 'avatarPath': str(self.root)}}))
        data = self.roundtrip()
        self.assertEqual(Path(data['profile']['avatarPicture']).parent, Path(data['profile']['avatarPath']))

    def test_prepare_folder_twice_keeps_previous_bundle(self):
        bundle.export(self.preset, self.exports, '.', folder_output=True)
        old = (self.exports / self.preset.stem / self.preset.name).read_bytes()
        bundle.export(self.preset, self.exports, '.', folder_output=True)
        saved = next((self.exports / 'backups').iterdir())
        self.assertEqual((saved / self.preset.name).read_bytes(), old)

    def test_manifest_detects_tampering(self):
        bundle.export(self.preset, self.exports, '.')
        archive = self.exports / f'{self.preset.stem}.zip'
        tampered = self.root / 'tampered.zip'
        with zipfile.ZipFile(archive) as input_zip, zipfile.ZipFile(tampered, 'w') as output:
            for name in input_zip.namelist():
                data = SVG.replace('red', 'blue').encode() if name == self.wall.name else input_zip.read(name)
                output.writestr(name, data)
        with self.assertRaisesRegex(ValueError, 'Manifest'):
            bundle.import_zip(tampered, self.imports, '.')

    def test_install_keeps_personal_images(self):
        home = self.root / 'home'
        pictures = home / 'Pictures/Wallpapers'
        pictures.mkdir(parents=True)
        personal = pictures / self.wall.name
        personal.write_text(SVG.replace('red', 'blue'))
        old = personal.read_bytes()
        with patch.dict(os.environ, {'HOME': str(home)}):
            preset_install.install(str(self.preset), str(self.root), str(home / 'presets'), 'gallery', 'Persona')
        self.assertEqual(personal.read_bytes(), old)
        installed = read_object(home / 'presets/Persona.json')
        self.assertNotEqual(installed['background']['wallpaperPath'], str(personal))

    def test_script_save_export_import_respects_xdg_and_blacklist(self):
        home = self.root / 'home'
        config_root = self.root / 'custom-config'
        cache = self.root / 'custom-cache'
        config = config_root / 'illogical-impulse'
        config.mkdir(parents=True)
        (config / 'config.json').write_text(json.dumps({'background': {'wallpaperPath': str(self.wall)}, 'ai': {'secret': 'never-share'}, 'appearance': {'fonts': {'main': 'local-font'}}}))
        env = {**os.environ, 'HOME': str(home), 'XDG_CONFIG_HOME': str(config_root), 'XDG_CACHE_HOME': str(cache)}
        def run(*args):
            subprocess.run(['bash', str(ROOT / 'scripts/presets.sh'), *args], env=env, check=True, capture_output=True)
        run('--save', 'Persona')
        saved = read_object(config / 'presets/Persona.json')
        self.assertNotIn('ai', saved)
        self.assertNotIn('fonts', saved.get('appearance', {}))
        run('--export-zip', 'Persona')
        run('--import-zip', str(config / 'presets/Persona.zip'))
        self.assertTrue((cache / 'quickshell/presets_imported/Persona.json').exists())
        # A save/overwrite must also preserve the filter semantics.
        run('--save', 'Persona', 'description')


if __name__ == '__main__':
    unittest.main()
