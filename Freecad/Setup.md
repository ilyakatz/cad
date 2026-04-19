# FreeCAD setup

**FreeCAD Version:** 1.1.1

## Back up config and addon list

From this directory (`Freecad/`), run:

```bash
./backup-freecad-config.sh
```

That writes `user.cfg.backup`, `system.cfg.backup`, and `freecad_addons_only.txt` next to the script. Run it whenever you want the repo to reflect your current FreeCAD install.

---

## Addons (`freecad_addons_only.txt`)

[`freecad_addons_only.txt`](./freecad_addons_only.txt) lists Addon Manager package names (one per line)—a checklist from a previous install. There is no bulk import; use the file as a manual list.

1. Open **Tools → Addon Manager**
2. For each non-empty line in the file, search for that exact name → **Install** or **Update**
3. Restart FreeCAD when prompted (or after several installs)

**Optional — reuse folders from an old Mac:** Add-ons live under `~/Library/Application Support/FreeCAD/Mod/` (one directory per add-on). You can copy trusted folders from a backup or old machine into that path, then restart FreeCAD.

**Note:** Omit any line you do not want (for example **Telemetry** if you prefer not to install it).

---

## CommandPalette macro

**Macro:** [FreeCAD-CommandPalette](https://github.com/ddfisher/FreeCAD-CommandPalette)

### 1. Set Up Macros Folder

1. Go to **Macro → Macros**
2. Update **User Macros Location** to your preferred path:
   ```
   /Users/katzo/ws/cad/Freecad/macros
   ```

### 2. Install the Macro (Manual)

The macro is not available in the Addon Manager, so install manually:

1. Go to [https://github.com/ddfisher/FreeCAD-CommandPalette](https://github.com/ddfisher/FreeCAD-CommandPalette)
2. Click on `CommandPalette.FCMacro`
3. Click **Raw** → right-click → **Save As**
4. Save the file to your macros folder (`/Users/katzo/ws/cad/Freecad/macros`)
5. Restart FreeCAD

### 3. Verify Installation

1. Go to **Macro → Macros**
2. **CommandPalette** should appear in the list
3. Select it and click **Execute** to test

### 4. Add to Global Toolbar

1. Go to **Tools → Customize**
2. Click the **Macros** tab
3. Find **CommandPalette** and select it
4. Click **Add/Apply** to register it
5. Switch to the **Toolbars** tab
6. Set the right-side dropdown to **Global**
7. Click **New** → name it (e.g. "MyMacros")
8. On the left, set **Category** to **Macros**
9. Select **CommandPalette** → click the **→** arrow to add it to the toolbar
10. Click **Close**

### 5. (Optional) Assign Keyboard Shortcut

1. Go to **Tools → Customize → Keyboard** tab
2. Search for **CommandPalette**
3. Set a shortcut (e.g. `Ctrl+Shift+P`)
4. Click **Assign** → **Close**
