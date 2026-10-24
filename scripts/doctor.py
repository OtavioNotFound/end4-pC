#!/usr/bin/env python3
"""Read-only integrity checks. Reports contain only allowlisted diagnostics."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

from preset_resources import describe, read_object, validate

ROOT = Path(__file__).resolve().parents[1]


def get(data, key):
    for part in key.split('.'):
        if not isinstance(data, dict) or part not in data:
            return None
        data = data[part]
    return data


def config_issues(data):
    issues = []
    # Targeted schema checks, not a replacement for the complete QML adapter.
    booleans = ['appearance.transparency.enable', 'appearance.transparency.automatic',
                'background.widgets.glass.enable', 'bar.weather.enableGPS']
    strings = ['background.wallpaperPath', 'background.lockWall', 'background.thumbnailPath',
               'background.centeredWallpaperImage', 'profile.avatarPicture', 'profile.avatarPath', 'sidebar.bannerImage']
    for field in booleans + strings:
        value = get(data, field)
        expected = bool if field in booleans else str
        if value is not None and type(value) is not expected:
            issues.append({'field': field, 'reason': 'type / tipo'})
    for field in ('appearance.transparency.backgroundTransparency', 'appearance.transparency.contentTransparency'):
        value = get(data, field)
        if value is not None and (type(value) not in (int, float) or not 0 <= value <= 1):
            issues.append({'field': field, 'reason': 'range 0..1 / faixa 0..1'})
    declared = set(re.findall(r'^            property \S+ (\w+):', (ROOT / 'modules/common/Config.qml').read_text(), re.M))
    unknown = set(data) - declared - {'_presetMeta'}
    if unknown:
        # Names themselves can be user content, so only the count is reportable.
        issues.append({'field': 'config', 'reason': 'unknown top-level keys / chaves de topo desconhecidas', 'count': len(unknown)})
    return issues


def report(config, log=None):
    checks = []

    def add(name, status, detail=''):
        checks.append({'check': name, 'status': status, 'detail': detail})

    for command, required in (('qs', True), ('hyprctl', True), ('python3', True), ('jq', True),
                              ('magick', True), ('cliphist', False), ('matugen', False),
                              ('ffmpeg', False), ('mpvpaper', False), ('fc-match', False)):
        add(command, 'ok' if shutil.which(command) else ('error' if required else 'optional-missing'))
    if shutil.which('qs'):
        result = subprocess.run(['qs', '--version'], capture_output=True, text=True, timeout=5)
        match = re.search(r'\d+\.\d+\.\d+', result.stdout)
        add('quickshell-version', 'info', match[0] if match else 'unknown')
    if shutil.which('hyprctl'):
        result = subprocess.run(['hyprctl', 'version'], capture_output=True, text=True, timeout=5)
        match = re.search(r'\d+\.\d+\.\d+', result.stdout)
        add('hyprland-version', 'info' if result.returncode == 0 else 'warning', match[0] if match else 'unavailable')
    add('wayland-session', 'ok' if os.environ.get('WAYLAND_DISPLAY') else 'warning')
    private_issues = []
    try:
        data = read_object(config)
        add('config-json', 'ok')
        for issue in config_issues(data):
            add(issue['field'], 'warning', issue['reason'])
        private_issues = validate(data, config.parent)
        if get(data, 'background.widgets.glass.enable') is True and not get(data, 'background.wallpaperPath'):
            add('glass-wallpaper', 'warning', 'Glassy UI requires a wallpaper image / Glassy UI precisa de uma imagem de wallpaper')
        wallpaper = get(data, 'background.wallpaperPath')
        if isinstance(wallpaper, str) and Path(wallpaper).suffix.lower() in {'.mp4', '.webm', '.mkv', '.avi', '.mov'} and not get(data, 'background.thumbnailPath'):
            add('video-thumbnail', 'warning', 'thumbnail not generated yet / thumbnail ainda não gerada')
        for issue in private_issues:
            # No paths, candidate filenames or arbitrary configuration values.
            add('asset', 'error', f"{issue['reason'].split(' (')[0]}; candidates={len(issue['candidates'])}")
        avatar_dir = get(data, 'profile.avatarPath')
        if isinstance(avatar_dir, str) and avatar_dir and not Path(os.path.expanduser(avatar_dir)).is_dir():
            add('avatar-directory', 'warning', 'missing / ausente')
        if shutil.which('fc-match'):
            for role, family in (get(data, 'appearance.fonts') or {}).items():
                if isinstance(family, str) and family:
                    result = subprocess.run(['fc-match', '-f', '%{family}', family], capture_output=True, text=True, timeout=5)
                    if family.casefold() not in result.stdout.casefold():
                        add('font-substitution', 'warning')
    except (OSError, ValueError, TypeError, AttributeError):
        add('config-json-or-schema', 'error', 'invalid or unreadable / inválido ou inacessível')
    for filename in ('cachyos-symbolic.svg', 'arch-symbolic.svg', 'desktop-symbolic.svg'):
        add(f'bundled-icon:{filename}', 'ok' if (ROOT / 'assets/icons' / filename).is_file() else 'error')
    state = Path(os.environ.get('XDG_STATE_HOME', Path.home() / '.local/state'))
    colors = state / 'quickshell/user/generated/colors.json'
    if not colors.exists():
        add('generated-colors', 'info', 'not generated yet; default palette / ainda não gerado; paleta padrão')
    else:
        try:
            read_object(colors)
            add('generated-colors', 'ok')
        except (OSError, ValueError):
            add('generated-colors', 'warning', 'invalid JSON; keep last palette / JSON inválido; manter última paleta')
    add('wallpaper-order', 'ok' if (config.parent / 'wallpaper_order.json').exists() else 'info', 'optional / opcional')
    geoclue_installed = Path('/usr/share/dbus-1/system-services/org.freedesktop.GeoClue2.service').is_file()
    add('geoclue', 'info' if geoclue_installed else 'optional-missing', 'descriptor only; manual city available / apenas instalação; cidade manual disponível')
    portal = shutil.which('xdg-desktop-portal') or Path('/usr/lib/xdg-desktop-portal').is_file()
    add('desktop-portal', 'info' if portal else 'optional-missing', 'installation check only / apenas presença, não saúde do serviço')
    if log:
        # Group known causes only. Never emit raw log lines or arbitrary matches.
        patterns = {'wallpaper-load': r'WindowGlass|Cannot open:.*wallpaper|Error decoding',
                    'missing-icon': r'Could not load icon', 'clipboard': r'cliphist|Cliphist',
                    'location': r'geoclue|GPS backend', 'undefined-string': r'undefined.*QString'}
        text = log.read_text(errors='replace')
        for cause, pattern in patterns.items():
            count = len(re.findall(pattern, text, re.I))
            if count:
                add(f'log:{cause}', 'warning', f'count={count}')
    return {'format': 1, 'privacy': 'allowlisted; no raw config, paths or logs', 'checks': checks}, private_issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')) / 'illogical-impulse/config.json')
    parser.add_argument('--log', type=Path)
    output = parser.add_mutually_exclusive_group()
    output.add_argument('--report', action='store_true', help='sanitized JSON for issues')
    output.add_argument('--local-json', action='store_true', help='private UI output including asset paths; never share as an issue report')
    parser.add_argument('--lang', choices=['pt', 'en'], default='pt')
    args = parser.parse_args()
    result, issues = report(args.config, args.log)
    if args.local_json:
        result['privacy'] = 'private local UI; contains asset paths; do not share'
        result['assets'] = issues
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.report:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print('Verificador end4-pC (somente leitura)' if args.lang == 'pt' else 'end4-pC integrity checker (read only)')
        labels = {'ok': 'ok', 'error': 'erro', 'warning': 'aviso', 'info': 'info', 'optional-missing': 'opcional ausente'} if args.lang == 'pt' else {}
        for check in result['checks']:
            print(f"[{labels.get(check['status'], check['status'])}] {check['check']} {check['detail']}")
        if issues:
            print('\n' + describe(issues))
            print('Correção explícita / explicit repair: python3 scripts/preset_resources.py FILE --repair-missing')
    return 1 if any(c['status'] == 'error' for c in result['checks']) else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError) as error:
        # Do not leak an arbitrary file path into a shareable report.
        print(json.dumps({'error': type(error).__name__}))
        sys.exit(2)
