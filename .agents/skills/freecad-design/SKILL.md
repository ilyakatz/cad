---
name: freecad-design
description: Create, revise, validate, and export parametric mechanical designs with FreeCAD Python macros and native .FCStd documents. Use for new FreeCAD parts or assemblies, photo- or drawing-based reconstruction, manufacturable injection-molded or machined solids, STEP/STL exports, geometry corrections, and validation of FreeCAD shape integrity.
---

# FreeCAD Design

Create reproducible CAD from a parameterized Python macro. Treat photographs as shape references, not dimensional evidence.

## Workflow

1. Inspect the project and reference inputs. Preserve existing user files and unrelated edits.
2. Establish part boundaries, axes, origin, units, manufacturing process, material, fits, and critical dimensions. If the user permits assumptions, record them explicitly and expose them as named parameters.
3. Locate FreeCAD with `command -v freecadcmd`, `command -v FreeCADCmd`, or common application paths. On macOS, also check `/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd`.
4. Create a `.FCMacro` as the source of truth. Use millimetres, named parameters, deterministic object names, and one final `PartDesign::Feature` or `Part::Feature` per requested solid.
5. Keep components separate. Fuse geometry that belongs to one manufactured part; never use visual color as a substitute for correct solid ownership.
6. Add a parameter spreadsheet and design-notes object to the document. State assumed materials, tolerances, clearances, attachment details, and omitted hidden features.
7. Recompute, verify each requested object is valid and contains the expected number of solids, save `.FCStd`, then export separate STEP files. Export STL only when requested.
8. Run `scripts/validate_fcstd.py` with FreeCAD's command-line executable. Correct every failure before delivery.
9. Compare front, top, left, right, and isometric silhouettes against the references. Pay special attention to lobes, notches, overhangs, part interfaces, and which component owns each feature.
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
