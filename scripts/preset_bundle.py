#!/usr/bin/env python3
"""Portable, offline preset bundles. Legacy meta.json and flat archives supported."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

from preset_resources import atomic_write, backup, describe, local_path, map_assets, read_object, validate

MAX_UNPACKED = 256 * 1024 * 1024
MAX_FILES = 2048
METADATA = {'meta.json', 'asset-manifest.json'}


def safe_name(name):
    if not name or name.startswith('.') or '/' in name or '\\' in name or '\n' in name:
        raise ValueError('Invalid preset name / nome inválido')
    return name


def filtered(path, program):
    read_object(path)
    result = subprocess.run(['jq', '-e', program, str(path)], check=True, capture_output=True)
    return json.loads(result.stdout)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def prepare_export(preset, folder, program, preview=None):
    original = read_object(preset)
    if original.get('_presetMeta', {}).get('origin'):
        raise ValueError('Preset belongs to its gallery author / preset pertence ao autor da galeria')
    data = filtered(preset, program)
    issues = validate(data, preset.parent)
    if issues:
        raise ValueError(describe(issues))
    assets = []
    used = {}

    def collect(value, field):
        if not value:
            return value
        source = local_path(value, preset.parent)
        sha = digest(source)
        # Never overwrite different images that happen to share a basename.
        name = source.name
        if name in {preset.name, *METADATA, 'preview.png'} or (name in used and used[name] != sha):
            name = f'{source.stem}-{sha[:16]}{source.suffix}'
        if name in used and used[name] != sha:
            raise ValueError(f'Asset collision / colisão: {name}')
        used[name] = sha
        shutil.copy2(source, folder / name)
        assets.append({'field': field, 'file': name, 'sha256': sha})
        return name

    data = map_assets(data, collect)

    def scrub(node):
        # Maintain upstream's privacy behavior for non-asset config values.
        if isinstance(node, dict):
            return {key: scrub(value) for key, value in node.items()}
        if isinstance(node, list):
            return [scrub(value) for value in node]
        if isinstance(node, str):
            if '://' in node:
                return ''
            if node.startswith(('/', '~/')):
                return Path(node.rstrip('/')).name
        return node

    data = scrub(data)
    meta = {'preview': '', 'screenshots': [], 'wallpapers': []}
    roles = {'profile.avatarPicture': 'avatar', 'sidebar.bannerImage': 'banner',
             'background.lockWall': 'lockWall', 'background.widgets.customImage.path': 'customImage'}
    for item in assets:
        field = item['field']
        if field == 'background.wallpaperPath' or '.collage.' in field:
            meta['wallpapers'].append(item['file'])
        if field in roles:
            meta[roles[field]] = item['file']
    if preview:
        if not shutil.which('magick'):
            raise ValueError('ImageMagick is needed to prepare a preview / necessário para preparar preview')
        subprocess.run(['magick', str(preview), '-auto-orient', '-resize', '1920x1080>', f'png:{folder / "preview.png"}'], check=True, capture_output=True, timeout=30)
        meta['preview'] = 'preview.png'
    for path in folder.iterdir():
        if path.stat().st_size > 9 * 1024 * 1024 + 512 * 1024:
            raise ValueError(f'{path.name}: image exceeds gallery limit; resize an explicit copy before exporting')
    for name, value in ((preset.name, data), ('meta.json', meta),
                        ('asset-manifest.json', {'version': 1, 'assets': assets})):
        atomic_write(folder / name, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())


def import_zip(archive, destination, program):
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.import-', dir=destination) as temporary:
        stage = Path(temporary)
        with zipfile.ZipFile(archive) as bundle:
            infos = bundle.infolist()
            if len(infos) > MAX_FILES or sum(i.file_size for i in infos) > MAX_UNPACKED:
                raise ValueError('Archive too large / arquivo compactado excede limite')
            seen = set()
            for info in infos:
                path = PurePosixPath(info.filename)
                if (path.is_absolute() or '..' in path.parts or '\\' in info.filename
                        or stat.S_ISLNK(info.external_attr >> 16) or info.filename in seen):
                    raise ValueError('Unsafe archive member / entrada insegura no ZIP')
                seen.add(info.filename)
            bundle.extractall(stage)
        presets = sorted(p for p in stage.rglob('*.json') if p.name not in METADATA)
        if len(presets) != 1:
            raise ValueError('ZIP must contain exactly one preset JSON / ZIP deve conter exatamente um preset')
        preset = presets[0]
        name = safe_name(preset.stem)
        data = filtered(preset, program)
        root = preset.parent
        manifest = root / 'asset-manifest.json'
        manifest_fields = {}
        if manifest.exists():
            meta = read_object(manifest)
            if meta.get('version') != 1:
                raise ValueError('Unsupported asset manifest version')
            for item in meta['assets']:
                asset = local_path(item['file'], root).resolve()
                if not asset.is_relative_to(root.resolve()) or not asset.is_file() or digest(asset) != item['sha256']:
                    raise ValueError(f'Manifest asset mismatch / asset inválido: {item["file"]}')
                manifest_fields[item['field']] = asset
        files = [p for p in root.rglob('*') if p.is_file() and p.suffix.lower() != '.json']

        def resolve(value, field):
            if not value:
                return value
            if not isinstance(value, str):
                raise ValueError(f'{field}: expected string')
            if field in manifest_fields:
                return str(manifest_fields[field])
            # Legacy files may contain another user's absolute paths. Only an
            # unambiguous bundled basename is eligible, never arbitrary Pictures.
            base = local_path(value, root).name
            candidates = [p for p in files if p.name == base]
            if len(candidates) != 1:
                raise ValueError(f'{field}: missing or ambiguous bundled asset / ausente ou ambíguo: {value}')
            return str(candidates[0])

        data = map_assets(data, resolve)
        issues = validate(data, root)
        if issues:
            raise ValueError(describe(issues))
        # Fresh asset directory makes re-import non-destructive and reversible.
        target = destination / f'{name}.json'
        n = 2
        while target.exists():
            target = destination / f'{name}_{n}.json'
            n += 1
        assets_root = destination / 'assets'
        assets_root.mkdir(exist_ok=True)
        cached = Path(tempfile.mkdtemp(prefix=f'{target.stem}-', dir=assets_root))
        try:
            shutil.copytree(root, cached, dirs_exist_ok=True)
            data = map_assets(data, lambda value, field: str(cached / Path(value).relative_to(root)) if value else value)
            data['_presetMeta'] = {'source': 'imported'}
            atomic_write(target, (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode())
        except BaseException:
            shutil.rmtree(cached)
            raise
        print(f'Imported / importado: {target}')


def export(preset, destination, program, folder_output=False, preview=None):
    name = safe_name(preset.stem)
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.export-', dir=destination) as temporary:
        stage = Path(temporary)
        content = stage / 'content'
        content.mkdir()
        prepare_export(preset, content, program, preview)
        if folder_output:
            target = destination / name
            if target.exists():
                raise ValueError(f'{target}: already exists; move it aside explicitly before preparing again')
            os.replace(content, target)
        else:
            target = destination / f'{name}.zip'
            zipped = stage / 'bundle.zip'
            with zipfile.ZipFile(zipped, 'w', zipfile.ZIP_DEFLATED) as bundle:
                for path in sorted(content.iterdir()):
                    bundle.write(path, path.name)
            if target.exists():
                backup(target)
            os.replace(zipped, target)
        print(f'Exported / exportado: {target}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['import', 'export'])
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('filter')
    parser.add_argument('--folder', action='store_true')
    parser.add_argument('--preview', type=Path)
    args = parser.parse_args()
    if args.action == 'import':
        import_zip(args.source, args.destination, args.filter)
    else:
        export(args.source, args.destination, args.filter, args.folder, args.preview)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, AttributeError, zipfile.BadZipFile, subprocess.SubprocessError) as error:
        print(f'Preset bundle error / erro no pacote: {error}', file=sys.stderr)
        sys.exit(2)
