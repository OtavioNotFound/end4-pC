#!/usr/bin/env bash
# presets.sh - manage shell config presets | just for fun I could have done it from quickshell directly =P
# Usage:
#   presets.sh --save <name> [description]
#   presets.sh --remove <name> [--online]
#   presets.sh --apply <name> [--online]
#   presets.sh --rename <name> <new_name>
#   presets.sh --export-zip <name>
#   presets.sh --import-zip <zip_path>

set -euo pipefail

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/illogical-impulse"
CONFIG_FILE="$CONFIG_DIR/config.json"
LOCAL_PRESETS_DIR="$CONFIG_DIR/presets"
ONLINE_PRESETS_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/quickshell/presets"
IMPORTED_PRESETS_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/quickshell/presets_imported"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SWITCHWALL="$SCRIPT_DIR/colors/switchwall.sh"
# shellcheck source=lib/config.sh
source "$SCRIPT_DIR/lib/config.sh"

mkdir -p "$LOCAL_PRESETS_DIR" "$ONLINE_PRESETS_DIR" "$IMPORTED_PRESETS_DIR"

# Blacklist: appearance.fonts (UI font families can break the layout) + General (time/battery/audio/sounds/language/workSafety) + Services (ai/networking/musicRecognition/search/screenRecord/screenSnip/updates/bar.weather) + Hyprland non-styling
# Keep: appearance/background/bar(non-weather)/dock/lock/overview/panelFamily etc. + hyprland.decoration/gaps/animations
# Note: apps/profile/wallpaperSelector are NOT blacklisted here (would make preset look empty) - only General+Services per Settings tabs
BLACKLIST_FILTER='del(._presetMeta)
  | del(.time, .battery, .audio, .sounds, .language, .workSafety)
  | del(.ai, .networking, .musicRecognition, .search, .screenRecord, .screenSnip, .updates)
  | del(.bar.weather)
  | del(.appearance.fonts)
  | del(.profile.onlinePresets, .profile.uploadGuideSeen)
  | del(.hyprland.input, .hyprland.autostartApps, .hyprland.general.layout)
  | del(.dock.pinnedApps, .launcher.pinnedApps, .tray.pinnedItems)
  | del(.sidebar.booru, .wallpaperSelector.userPath)
  | walk(if type == "object" then with_entries(select(.key | test("^(.*api[-_]?key|secret|password|token|username|e-?mail)$"; "i") | not)) else . end)'

SHARE_FILTER='with_entries(select(.key as $k | ["appearance","background","bar","calendar","crosshair","dock","interactions","launcher","light","lock","media","notifications","osd","osk","overlay","overview","panelFamily","profile","regionSelector","resources","settings","sidebar","tray","wallpaperSelector","windows","hyprland"] | index($k)))
  | if (.hyprland | type) == "object" then .hyprland |= with_entries(select(.key as $k | ["decoration","gaps","animations","general"] | index($k))) else . end'

action="${1:-}"
[ -n "$action" ] || { echo 'Error: missing action' >&2; exit 1; }
shift

online=false
args=()
imported=false
preview=""
origin=""
display=""
folder_out=false
create_only=false
while [ $# -gt 0 ]; do
    arg="$1"
    if [ "$arg" = "--online" ]; then
        online=true
    elif [ "$arg" = "--imported" ]; then
        imported=true
    elif [ "$arg" = "--folder" ]; then
        folder_out=true
    elif [ "$arg" = "--create-only" ]; then
        create_only=true
    elif [ "$arg" = "--preview" ]; then
        shift
        preview="${1:?Error: --preview needs a path}"
    elif [ "$arg" = "--origin" ]; then
        shift
        origin="${1:?Error: --origin needs a value}"
    elif [ "$arg" = "--as" ]; then
        shift
        display="${1:?Error: --as needs a name}"
    else
        args+=("$arg")
    fi
    shift
done

name="${args[0]:-}"
description="${args[1]:-}"

if [ "$action" = "--import-zip" ]; then
    if [ -z "$name" ]; then
        echo "Error: missing zip path" >&2
        exit 1
    fi
    zip_path="$name"
    if [ ! -f "$zip_path" ]; then
        echo "Error: zip not found: $zip_path" >&2
        exit 1
    fi
    python3 "$SCRIPT_DIR/preset_bundle.py" import "$zip_path" "$IMPORTED_PRESETS_DIR" "$BLACKLIST_FILTER"
    exit 0
fi

if [ -z "$name" ]; then
    echo "Error: missing preset name" >&2
    exit 1
fi

# Names are file components, never paths (also protects remove/export).
if [[ "$name" == */* || "$name" == .* || "$name" == *$'\n'* ]]; then
    echo 'Error: invalid preset name' >&2
    exit 1
fi

if $imported; then
    PRESETS_DIR="$IMPORTED_PRESETS_DIR"
elif $online; then
    PRESETS_DIR="$ONLINE_PRESETS_DIR"
else
    PRESETS_DIR="$LOCAL_PRESETS_DIR"
fi

case "$action" in
    --save)
        if $create_only && [ -e "$PRESETS_DIR/${name}.json" ]; then
            echo 'A preset with this name already exists. Choose another name or confirm Overwrite in the preset details.' >&2
            exit 3
        fi
        if [ ! -e "$PRESETS_DIR/${name}.json" ]; then
            # Stage first; a failed filter must never create an empty preset.
            tmp=$(mktemp "$PRESETS_DIR/.save.XXXXXX")
            trap 'rm -f "$tmp"' EXIT
            jq -e "$BLACKLIST_FILTER" "$CONFIG_FILE" > "$tmp"
            jq -e -s 'length == 1 and (.[0] | type == "object")' "$tmp" >/dev/null
            if $create_only; then
                # Exclusive link commits the staged file without replacing a
                # concurrently created preset. Staging is on the same filesystem.
                if ! ln -T -- "$tmp" "$PRESETS_DIR/${name}.json"; then
                    echo 'Preset name already exists. Choose another name.' >&2
                    exit 3
                fi
                rm -f "$tmp"
            else
                mv "$tmp" "$PRESETS_DIR/${name}.json"
            fi
            trap - EXIT
        else
            python3 "$SCRIPT_DIR/preset_resources.py" "$PRESETS_DIR/${name}.json" --backup-only >/dev/null
            jq "$BLACKLIST_FILTER" "$CONFIG_FILE" | config_json_replace "$PRESETS_DIR/${name}.json"
        fi
        if [ -n "$description" ]; then
            config_json_update "$PRESETS_DIR/${name}.json" --arg desc "$description" '._presetMeta = {"description": $desc}'
        fi
        ;;
    --remove)
        rm -f "$PRESETS_DIR/${name}.json"
        if $online; then
            rm -rf "$ONLINE_PRESETS_DIR/assets/${name}"
        elif $imported; then
            rm -rf "$IMPORTED_PRESETS_DIR/assets/${name}"
        fi
        ;;
    --rename)
        new_name="${description//[[:space:]]/_}"
        if [[ -z "$new_name" || "$new_name" == */* || "$new_name" == .* ]] || [ ! -f "$PRESETS_DIR/${name}.json" ] || [ -e "$PRESETS_DIR/${new_name}.json" ]; then
            exit 1
        fi
        mv "$PRESETS_DIR/${name}.json" "$PRESETS_DIR/${new_name}.json"
        echo "$new_name"
        ;;
    --apply)
        preset_file="$PRESETS_DIR/${name}.json"
        if [ ! -f "$preset_file" ]; then
            echo "Error: preset not found: $name" >&2
            exit 1
        fi
        python3 "$SCRIPT_DIR/preset_apply.py" "$CONFIG_FILE" "$preset_file" "$BLACKLIST_FILTER" "$SWITCHWALL"
        ;;
    --install)
        preset_file="$PRESETS_DIR/${name}.json"
        if [ ! -f "$preset_file" ]; then
            echo "Error: preset not found: $name" >&2
            exit 1
        fi
        python3 "$SCRIPT_DIR/preset_install.py" "$preset_file" "$PRESETS_DIR/assets/$name" "$LOCAL_PRESETS_DIR" "${origin:-$($imported && echo imported || echo gallery)}" "${display:-$name}"
        ;;
    --export-zip)
        preset_file="$PRESETS_DIR/${name}.json"
        if [ ! -f "$preset_file" ]; then
            echo "Error: preset not found: $name" >&2
            exit 1
        fi
        origin_tag=$(jq -r '._presetMeta.origin // empty' "$preset_file")
        if [ -n "$origin_tag" ]; then
            echo "Error: this preset comes from $origin_tag and can't be exported" >&2
            exit 3
        fi
        export_args=()
        destination="$LOCAL_PRESETS_DIR"
        if $folder_out; then
            destination="${XDG_CACHE_HOME:-$HOME/.cache}/quickshell/presets_share"
            export_args+=(--folder)
        fi
        [ -z "$preview" ] || export_args+=(--preview "$preview")
        python3 "$SCRIPT_DIR/preset_bundle.py" export "$preset_file" "$destination" "$BLACKLIST_FILTER | $SHARE_FILTER" "${export_args[@]}"
        ;;
    *)
        echo "Error: unknown action: $action" >&2
        exit 1
        ;;
esac
