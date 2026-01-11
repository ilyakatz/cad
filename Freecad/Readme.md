cp ~/Library/Preferences/FreeCAD/v1-2/user.cfg user.cfg.backup
cp ~/Library/Preferences/FreeCAD/v1-2/system.cfg system.cfg.backup
for d in "$HOME/Library/Application Support/FreeCAD/v1-2/Mod"/*/; do basename "$d"; done > ./freecad_addons_only.txt