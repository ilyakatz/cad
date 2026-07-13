"""Validate named single-solid objects in a saved FreeCAD document.

Usage: freecadcmd validate_fcstd.py model.FCStd ObjectA [ObjectB ...]
"""

import os
import sys
import FreeCAD as App


def fail(message):
    print("VALIDATION FAILED: " + message)
    raise SystemExit(1)


args = [arg for arg in sys.argv[1:] if arg != "--"]
model_index = next((i for i, arg in enumerate(args) if arg.lower().endswith(".fcstd")), None)
if model_index is None:
    fail("provide a .FCStd path followed by one or more object names")

model_path = os.path.abspath(args[model_index])
object_names = args[model_index + 1:]
if not object_names:
    fail("provide at least one object name")
if not os.path.isfile(model_path):
    fail("file not found: " + model_path)

doc = App.openDocument(model_path)
doc.recompute()

for name in object_names:
    obj = doc.getObject(name)
    if obj is None:
        fail("missing object: " + name)
    if not hasattr(obj, "Shape") or obj.Shape.isNull():
        fail(name + " has no shape")
    if not obj.Shape.isValid():
        fail(name + " has an invalid shape")
    if len(obj.Shape.Solids) != 1:
        fail("%s contains %d solids; expected 1" % (name, len(obj.Shape.Solids)))
    print("VALID: %s | volume %.2f mm^3" % (name, obj.Shape.Volume))

App.closeDocument(doc.Name)
print("VALIDATION PASSED: " + model_path)
