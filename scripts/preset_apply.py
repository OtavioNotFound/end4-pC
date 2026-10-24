#!/usr/bin/env python3
"""Validate and apply an existing preset, keeping a recoverable config snapshot."""
import argparse
import fcntl
import json
from pathlib import Path
import subprocess
import sys

from preset_resources import atomic_write, backup, describe, map_assets, local_path, read_object, validate


def apply(config, preset, filter_program, switchwall):
    # This lock serializes this fork's preset transactions. QML separately pauses
    # its debounced writes; other tools do not yet participate in this lock.
    with config.with_suffix('.json.preset.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        original = config.read_bytes()
        read_object(config)
        read_object(preset)
        filtered = subprocess.run(['jq', '-e', filter_program, str(preset)],
                                  check=True, capture_output=True).stdout
        # Normalize only known asset paths, never shell commands or arbitrary text.
        incoming = map_assets(json.loads(filtered), lambda value, field:
                              str(local_path(value, preset.parent)) if isinstance(value, str) and value else value)
        merged = subprocess.run(['jq', '-s', '.[0] * .[1] | del(._presetMeta)', str(config), '-'],
                                input=json.dumps(incoming).encode(), check=True, capture_output=True).stdout
        candidate = json.loads(merged)
        issues = validate(candidate, preset.parent)
        if issues:
            raise ValueError(describe(issues) + '\nUse preset_resources.py FILE --repair-missing to explicitly accept a unique correction.')
        if config.read_bytes() != original:
            raise ValueError('Config changed during validation / configuração alterada durante a validação; tente novamente')
        saved = backup(config)
        atomic_write(config, merged)
        try:
            result = subprocess.run([str(switchwall), '--noswitch'], capture_output=True, timeout=120)
            if result.returncode:
                # Detailed output stays in a private local file, not an issue report.
                log = saved.with_suffix('.log')
                atomic_write(log, result.stdout + result.stderr)
                raise RuntimeError(f'switchwall.sh failed / falhou (exit {result.returncode}); private log / log privado: {log}')
            after = read_object(config)
            # switchwall may update thumbnail/accent; verify preset fields still
            # persisted instead of accepting an unrelated concurrent replacement.
            if after.get('background', {}).get('wallpaperPath') != candidate.get('background', {}).get('wallpaperPath'):
                raise RuntimeError('Wallpaper verification failed / falha na verificação do wallpaper')
            if validate(after, preset.parent):
                raise RuntimeError('Resource verification failed / falha na verificação dos recursos')
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
            atomic_write(config, original)
            raise RuntimeError(f'{error}; config restored / configuração restaurada; backup: {saved}') from error
        print(f'Applied / aplicado: {preset.name}; backup: {saved}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path)
    parser.add_argument('preset', type=Path)
    parser.add_argument('filter')
    parser.add_argument('switchwall', type=Path)
    args = parser.parse_args()
    apply(args.config, args.preset, args.filter, args.switchwall)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, AttributeError, RuntimeError, subprocess.SubprocessError) as error:
        print(f'Preset not applied / preset não aplicado: {error}', file=sys.stderr)
        sys.exit(2)
