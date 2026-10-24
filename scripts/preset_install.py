#!/usr/bin/env python3
"""Install validated cached assets without searching or overwriting user pictures."""
import json
from pathlib import Path
import re
import shutil
import sys

from preset_bundle import digest
from preset_resources import atomic_write, describe, local_path, map_assets, read_object, validate


def install(json_path, asset_dir, local_dir, origin, display):
    source = Path(json_path)
    assets = Path(asset_dir)
    data = read_object(source)

    def resolve(value, field):
        if not value:
            return value
        path = local_path(value, assets)
        if path.is_file():
            return str(path)
        bundled = assets / path.name
        return str(bundled) if bundled.is_file() else str(path)

    data = map_assets(data, resolve)
    issues = validate(data, assets)
    if issues:
        raise ValueError(describe(issues))
    home = Path.home()
    created = []

    def place(value, field):
        if not value:
            return value
        src = Path(value)
        if field.endswith('avatarPicture'):
            folder = home / 'Pictures/avatar'
        elif field.startswith('background.') and ('wallpaper' in field.lower() or 'lockWall' in field or '.collage.' in field):
            folder = home / 'Pictures/Wallpapers'
        else:
            folder = home / 'Pictures/preset-assets'
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / src.name
        sha = digest(src)
        if target.exists() and digest(target) != sha:
            target = folder / f'{src.stem}-{sha}{src.suffix}'
        if target.exists() and digest(target) != sha:
            raise ValueError(f'Asset collision / colisão: {target}')
        if not target.exists():
            with target.open('xb') as output, src.open('rb') as input_file:
                created.append(target)
                shutil.copyfileobj(input_file, output)
        return str(target)

    try:
        data = map_assets(data, place)
        meta = data.get('_presetMeta') if isinstance(data.get('_presetMeta'), dict) else {}
        meta.pop('source', None)
        meta['origin'] = origin
        data['_presetMeta'] = meta
        safe = re.sub(r'[^\w.-]+', '_', display).strip('._') or 'preset'
        folder = Path(local_dir)
        folder.mkdir(parents=True, exist_ok=True)
        out = folder / f'{safe}.json'
        index = 2
        while out.exists():
            out = folder / f'{safe}_{index}.json'
            index += 1
        atomic_write(out, (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode())
    except BaseException:
        for path in created:
            path.unlink(missing_ok=True)
        raise
    print(out)


if __name__ == '__main__':
    try:
        install(*sys.argv[1:6])
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f'Install failed / instalação falhou: {error}', file=sys.stderr)
        sys.exit(2)
