#!/usr/bin/env python3
"""Local preset assets: diagnostics and explicit, reversible repairs. No network."""
import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.avif', '.bmp', '.svg', '.gif'}
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mkv', '.avi', '.mov'}
ASSET_KEYS = {
    'wallpaperPath', 'lockWall', 'thumbnailPath', 'centeredWallpaperImage',
    'avatarPicture', 'bannerImage',
}
ASSET_FIELDS = {
    'background.wallpaperPath', 'background.lockWall', 'background.thumbnailPath',
    'background.centeredWallpaperImage', 'profile.avatarPicture', 'sidebar.bannerImage',
}
WIDGETS = {'customImage', 'imageCard', 'sticker', 'images'}


def read_object(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'{path}: expected one JSON object / esperado um objeto JSON')
    return data


def atomic_write(path, content):
    path = Path(path)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    fd, name = tempfile.mkstemp(prefix=f'.{path.name}.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def backup(path):
    path = Path(path)
    folder = path.parent / 'backups'
    folder.mkdir(mode=0o700, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f'{path.name}.', suffix='.bak', dir=folder)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(path.read_bytes())
        stream.flush()
        os.fsync(stream.fileno())
    return Path(name)


def local_path(value, base=None):
    if value.startswith('file:'):
        url = urlsplit(value)
        if url.netloc not in ('', 'localhost'):
            raise ValueError('non-local file URL')
        value = unquote(url.path)
    elif '://' in value:
        raise ValueError('remote asset unsupported; download explicitly first')
    path = Path(os.path.expanduser(value))
    return path if path.is_absolute() else (Path(base or Path.cwd()).absolute() / path)


def asset_slots(node, trail=()):
    """Yield mutable known asset fields, including serialized collage leaves.

    Collage JSON is handled separately by map_assets so unrelated text/commands
    never get rewritten just because they look like image names.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            current = trail + (key,)
            if '.'.join(current) in ASSET_FIELDS or (key == 'path' and trail[:2] == ('background', 'widgets') and any(x in WIDGETS for x in trail[2:])) or (key == 'img' and trail[:3] == ('background', 'collage', 'tree')):
                yield node, key, current
            else:
                yield from asset_slots(value, current)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from asset_slots(value, trail + (str(index),))


def map_assets(data, transform):
    result = copy.deepcopy(data)
    for owner, key, trail in asset_slots(result):
        owner[key] = transform(owner[key], '.'.join(trail))
    collage = result.get('background', {}).get('collage', {})
    if isinstance(collage, dict) and collage.get('tree'):
        tree = json.loads(collage['tree'])
        for owner, key, trail in asset_slots(tree, ('background', 'collage', 'tree')):
            owner[key] = transform(owner[key], '.'.join(trail))
        collage['tree'] = json.dumps(tree, ensure_ascii=False, separators=(',', ':'))
    return result


def image_problem(path):
    try:
        if not path.is_file():
            return 'missing / ausente'
        with path.open('rb') as stream:
            header = stream.read(512)
        if not header:
            return 'empty / vazio'
        if path.suffix.lower() in VIDEO_EXTENSIONS:
            return ''  # Playback/codec verification is a separate runtime check.
        if shutil.which('magick'):
            checked = subprocess.run(
                ['magick', 'identify', '-regard-warnings', str(path) + '[0]'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            return '' if checked.returncode == 0 else 'undecodable image / imagem inválida'
        # Without a decoder, do not claim to have checked integrity.
        return 'decoder unavailable / instale ImageMagick para validar a imagem'
    except (OSError, subprocess.TimeoutExpired) as error:
        return f'unreadable / inacessível ({type(error).__name__})'


def inspect_asset(value, field, base=None):
    if value == '':
        return None
    issue = {'field': field, 'path': value, 'reason': '', 'candidates': []}
    if not isinstance(value, str):
        issue['reason'] = 'expected string / esperado texto'
        return issue
    try:
        path = local_path(value, base)
        issue['reason'] = image_problem(path)
        if issue['reason'].startswith('missing') and path.parent.is_dir():
            issue['candidates'] = sorted(str(p) for p in path.parent.iterdir()
                if p.stem == path.stem and p.suffix.lower() in IMAGE_EXTENSIONS
                and p != path and not image_problem(p))
    except (OSError, ValueError) as error:
        issue['reason'] = str(error)
    return issue if issue['reason'] else None


def validate(data, base=None):
    issues = []

    def check(value, field):
        issue = inspect_asset(value, field, base)
        if issue:
            issues.append(issue)
        return value

    map_assets(data, check)
    return issues


def describe(issues):
    lines = []
    for issue in issues:
        lines.append(f"{issue['field']}: {issue['path']} — {issue['reason']}")
        if len(issue['candidates']) == 1:
            lines.append(f"  Suggested explicit repair / correção sugerida: {issue['candidates'][0]}")
        elif issue['candidates']:
            lines.append('  Ambiguous / ambíguo: ' + ', '.join(issue['candidates']))
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', nargs='?', type=Path)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--repair-missing', action='store_true', help='explicitly accept unique same-stem repairs; backup first')
    parser.add_argument('--backup-only', action='store_true', help='create a private snapshot without changing the file')
    parser.add_argument('--sources', help='internal: JSON list of local image paths (read only)')
    args = parser.parse_args()
    if args.sources is not None:
        result = {}
        for value in json.loads(args.sources):
            if not value or value in result:
                continue
            issue = inspect_asset(value, 'wallpaper')
            decoder_missing = issue and issue['reason'].startswith('decoder unavailable')
            result[value] = {'source': '' if issue and not decoder_missing else local_path(value).as_uri(), 'issue': issue}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    if not args.file:
        parser.error('file is required')
    if args.backup_only:
        print(backup(args.file))
        return 0
    data = read_object(args.file)
    issues = validate(data, args.file.parent)
    if args.repair_missing:
        unrepairable = [i for i in issues if not i['reason'].startswith('missing') or len(i['candidates']) != 1]
        if unrepairable:
            print(describe(issues), file=sys.stderr)
            return 2
        repairs = {i['field']: i['candidates'][0] for i in issues}
        if repairs:
            data = map_assets(data, lambda value, field: repairs.get(field, value))
            saved = backup(args.file)
            atomic_write(args.file, (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode())
            print(f'Backup: {saved}', file=sys.stderr)
        issues = validate(data, args.file.parent)
    print(json.dumps(issues, ensure_ascii=False) if args.json else describe(issues) or 'OK')
    return 2 if issues else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f'Preset resource error / erro de recurso: {error}', file=sys.stderr)
        sys.exit(2)
