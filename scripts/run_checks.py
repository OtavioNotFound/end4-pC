#!/usr/bin/env python3
"""Offline checks with synthetic fixtures. Does not launch the full desktop shell."""
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
QML_FILES = [
    'modules/common/Config.qml', 'modules/common/Appearance.qml',
    'modules/common/widgets/WindowGlass.qml', 'modules/ii/background/Background.qml',
    'modules/ii/background/CenteredWallpaper.qml', 'modules/ii/settings/DashboardToggleCard.qml',
    'modules/ii/settings/DashboardSettingsPage.qml',
    'services/WallpaperResources.qml', 'services/SystemAppearance.qml', 'services/Presets.qml',
    'services/PresetsOnline.qml', 'services/MaterialThemeLoader.qml', 'services/Cliphist.qml',
    'services/Wallpapers.qml', 'services/Weather.qml',
]
QML_FILES += [
    'GlobalStates.qml', 'services/SettingsHelp.qml', 'services/SettingsDiagnostics.qml',
    'services/SettingsQuickControls.qml', 'services/SettingsSearchIndex.qml',
    'services/LauncherSearch.qml', 'services/HyprlandOptions.qml', 'services/FirstRunExperience.qml',
    'modules/common/widgets/ConfigSwitch.qml', 'modules/common/widgets/ConfigSlider.qml',
    'modules/common/widgets/PresetPopup.qml', 'modules/common/widgets/StyledToolTip.qml',
    'modules/common/widgets/StyledToolTipContent.qml', 'modules/ii/overview/SearchItem.qml',
]
QML_FILES += [str(path.relative_to(ROOT)) for path in sorted((ROOT / 'modules/ii/settings').rglob('*.qml'))]
QML_FILES = list(dict.fromkeys(QML_FILES))


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
    if result.returncode:
        print(result.stdout + result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result


def main():
    missing = [command for command in ('bash', 'jq', 'magick') if not shutil.which(command)]
    if missing:
        print('Missing test dependencies / dependências ausentes: ' + ', '.join(missing), file=sys.stderr)
        return 2
    for directory in ('tests/icon_theme_manager', 'tests/presets', 'tests/settings'):
        result = run([sys.executable, '-m', 'unittest', 'discover', '-s', directory, '-q'])
        print(f'{directory}: {result.stderr.strip()}')
    count = 0
    for path in ROOT.rglob('*.json'):
        if '.git' not in path.parts:
            json.loads(path.read_text(encoding='utf-8'))
            count += 1
    print(f'JSON: {count} valid files')
    for path in (ROOT / 'scripts').rglob('*.py'):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    print('Python scripts: syntax OK')
    for path in (ROOT / 'scripts').rglob('*.sh'):
        run(['bash', '-n', str(path)])
    print('Bash scripts: syntax OK')
    qmlformat = shutil.which('qmlformat')
    if not qmlformat and Path('/usr/lib/qt6/bin/qmlformat').is_file():
        qmlformat = '/usr/lib/qt6/bin/qmlformat'
    if qmlformat:
        for path in QML_FILES:
            # Parse without writing. Upstream MaxColumnWidth triggers a local
            # Qt formatter crash on some files, unrelated to their QML syntax.
            run([qmlformat, '--ignore-settings', path])
        print(f'QML: {len(QML_FILES)} settings and related files parsed; no files reformatted')
    else:
        print('QML parser skipped: qmlformat unavailable')
    run(['git', 'diff', '--check'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
