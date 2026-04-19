#!/usr/bin/env bash
# Copy FreeCAD user/system config and list installed Addon Manager packages into this repo folder.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FREECAD_PREFS="${HOME}/Library/Preferences/FreeCAD/v1-2"
FREECAD_MOD="${HOME}/Library/Application Support/FreeCAD/v1-2/Mod"

cp "${FREECAD_PREFS}/user.cfg" "${SCRIPT_DIR}/user.cfg.backup"
cp "${FREECAD_PREFS}/system.cfg" "${SCRIPT_DIR}/system.cfg.backup"

shopt -s nullglob
{
  for d in "${FREECAD_MOD}"/*/; do
    basename "${d%/}"
  done
} >"${SCRIPT_DIR}/freecad_addons_only.txt"
