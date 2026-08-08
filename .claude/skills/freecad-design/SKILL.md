---
name: freecad-design
description: Create, revise, validate, and export parametric mechanical designs with FreeCAD Python macros and native .FCStd documents. Use for new FreeCAD parts or assemblies, photo- or drawing-based reconstruction, manufacturable injection-molded or machined solids, STEP/STL exports, geometry corrections, and validation of FreeCAD shape integrity.
---

# FreeCAD Design

Create reproducible CAD from a parameterized Python macro. Treat photographs as shape references, not dimensional evidence.

## FreeCAD 2.x Environment

**Critical: FreeCAD 2.x (conda build) has a heavily stripped headless Python API.**

- **Headless Python API WORKS for**: `Part.makeBox()`, `Part.makeCylinder()`, `.cut()`, `.fuse()`, `.removeSplitter()`, `doc.addObject("Part::Feature", name)`, `doc.saveAs()`, `Part.export()`. All topology operations are available.
- **Headless Python API DOES NOT WORK for**: `doc.newView()`, `doc.ActiveView`, `view.saveImage()`, `FreeCADGui`, all visualization (`OCC.Core.OpenGl`, `OCC.Core.Visualisation`). These are compiled out of the headless build.
- **FreeCAD CLI binary has NO headless mode**: Running `FreeCAD <script.py>` crashes on exit regardless of content. Always use Python directly with the correct paths.

On macOS (conda FreeCAD 2.app):
```
PYTHONPATH: /Applications/FreeCAD 2.app/Contents/Resources/lib/python3.1/site-packages
            /Applications/FreeCAD 2.app/Contents/Resources/lib
PYTHONHOME: /Applications/FreeCAD 2.app/Contents/Resources
PATH:       /Applications/FreeCAD 2.app/Contents/Resources/libexec
            /Applications/FreeCAD 2.app/Contents/Resources/bin
DYLD_LIBRARY_PATH: /Applications/FreeCAD 2.app/Contents/Resources/lib
```

## Workflow

1. Inspect the project and reference inputs. Preserve existing user files and unrelated edits.
2. Establish part boundaries, axes, origin, units, manufacturing process, material, fits, and critical dimensions. If the user permits assumptions, record them explicitly and expose them as named parameters.
3. Locate FreeCAD Python (not the CLI binary) at `/Applications/FreeCAD 2.app/Contents/Resources`. Set `PYTHONPATH` and `DYLD_LIBRARY_PATH` as above. **Do not use `FreeCAD <script.py>` CLI invocation** — it crashes.
4. Create a `.FCMacro` as the source of truth. Use millimetres, named parameters, deterministic object names, and one final `PartDesign::Feature` or `Part::Feature` per requested solid.
5. Keep components separate. Fuse geometry that belongs to one manufactured part; never use visual color as a substitute for correct solid ownership.
6. Add a parameter spreadsheet and design-notes object to the document. State assumed materials, tolerances, clearances, attachment details, and omitted hidden features.
7. Build geometry headlessly via Python's `Part` module (works), save `.FCStd`, export STEP files (`Part.export()` works). Do NOT attempt STL meshing headlessly — `BRepMesh_FastDiscreteExplorer` was removed in FreeCAD 2.x, and `MeshPart` API changed.
8. Run `scripts/validate_fcstd.py` with FreeCAD's Python executable (headless). Correct every failure before delivery.
9. If the user needs a visual, generate an SVG from the Python geometry using an isometric projection renderer (see `/freecad-generate-image` skill). Do not attempt FreeCAD GUI rendering headlessly.
10. Deliver clickable paths to the native document, macro, and exports. Summarize material and dimensional assumptions concisely.

## Modeling rules

- Prefer robust primitives, extrusions, revolutions, and conservative booleans over fragile topological edge references.
- Call `removeSplitter()` after completed boolean chains when appropriate.
- Extend cutting tools beyond the target in both directions to avoid coincident-face failures.
- Do not claim spreadsheet-driven behavior unless expressions or a persistent proxy actually drive recomputation. A macro parameter table is parameterized regeneration, not live spreadsheet parametrics.
- Model nominal geometry. Apply resin shrink at tooling/export stage unless the user requests shrink-scaled parts.
- Add draft only when the pull direction and tooling intent are known or explicitly assumed.
- Use general tolerances only for non-mating features. Specify functional clearances separately.
- Avoid threads, knurling, and dense cosmetic detail unless required; represent them with manufacturable simplified geometry.

## Headless API notes

- **Shape validation**: Use `obj.Shape.isValid()` (on the Feature's Shape property), NOT `solid.IsValid()` (TopoDS_Solid has no Python-exposed IsValid in FreeCAD 2.x).
- **STL export headless**: Not possible in FreeCAD 2.x. `BRepMesh_FastDiscreteExplorer` was removed, and `MeshPart` API signature changed. Export STEP or save FCStd and let the user mesh in the GUI if needed.
- **SVG rendering workaround**: For visual output, use a Python isometric projection renderer (see `/freecad-generate-image`). This is the recommended approach for delivering images without the GUI.
- **Solid count check**: `obj.Shape.Solids` returns a list of TopoDS_Solid objects. Check `len(obj.Shape.Solids) == 1` instead of `isValid()`.

## Photo reconstruction

- Use at least two views before inferring depth or feature ownership.
- Use color, occlusion, tangent continuity, and silhouette changes together when separating parts.
- Never derive precise scale from an uncalibrated photograph.
- When the user asks for best judgment, choose coherent nominal dimensions and list them in the macro rather than pausing.
- After a user identifies a mismatch, revise the underlying solid ownership or profile instead of applying a cosmetic patch.

## Validation

Run:

```bash
<freecadcmd> scripts/validate_fcstd.py path/to/model.FCStd ObjectNameA ObjectNameB
```

The validator opens the saved document, recomputes it, and checks that named objects exist, have valid non-null shapes, and each contain exactly one solid.

For injection-molded or machined production reviews, read [references/manufacturing-checks.md](references/manufacturing-checks.md).
