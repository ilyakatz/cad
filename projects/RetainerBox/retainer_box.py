# FreeCAD Python Macro - Retainer Box with Flat Hinged Lid
# Rectangular base + flat cover lid, barrel hinge across the back
# Open in FreeCAD: Macro > Macros > select this file > Execute

import FreeCAD
import Part

doc = FreeCAD.newDocument("Retainer_Box")

# ============================================
# DIMENSIONS (mm) - adjust as needed
# ============================================
W       = 80.0    # box width left-right (X); Y=0 = back/hinge side
D       = 70.0    # box depth front-to-back (Y)
rect_h  = 28.0    # height of rectangular base (Z)
t       = 2.5     # wall thickness
lid_t   = 4.0     # lid cap thickness (set > hinge_r so top remains flat)
lip     = 1.2     # inner rim lip height

# Lid fit/clearance
fit_clearance = 0.35   # radial clearance between lid skirt and box opening
skirt_wall = 1.2       # skirt ring wall thickness
skirt_drop = 1.8       # how far skirt drops below lid plate

# Hinge (barrel, runs along X axis at back top of box)
hinge_r      = 3.5
pin_r        = 1.3
num_knuckles = 5
knuckle_gap  = 0.4
hinge_length = W

# Hinge end-stop inserts (to trap the hinge pin)
end_stop_len = 2.4
end_stop_clearance = 0.08
end_stop_head_r = hinge_r * 0.9
end_stop_head_t = 1.2

# ============================================
# HELPER: barrel hinge knuckle along X axis
# ============================================
def make_knuckle(x_start, x_len, outer_r, inner_r):
    outer = Part.makeCylinder(outer_r, x_len,
                              FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0))
    inner = Part.makeCylinder(inner_r, x_len + 1,
                              FreeCAD.Vector(-0.5, 0, 0), FreeCAD.Vector(1, 0, 0))
    k = outer.cut(inner)
    k.translate(FreeCAD.Vector(x_start, 0, 0))
    return k

knuckle_len = (hinge_length - (num_knuckles - 1) * knuckle_gap) / num_knuckles

# ============================================
# 1. BOX BASE (rectangular shell, open at top)
# ============================================
box_outer = Part.makeBox(W, D, rect_h)
box_inner = Part.makeBox(W - 2*t, D - 2*t, rect_h - t)
box_inner.translate(FreeCAD.Vector(t, t, t))
box_shell = box_outer.cut(box_inner)

# Inner rim at top so lid sits flush
rim_outer = Part.makeBox(W, D, lip)
rim_outer.translate(FreeCAD.Vector(0, 0, rect_h))
rim_inner = Part.makeBox(W - 2*(t + lip), D - 2*(t + lip), lip)
rim_inner.translate(FreeCAD.Vector(t + lip, t + lip, rect_h))
rim = rim_outer.cut(rim_inner)

# Remove rim on hinge side so lid can rotate
rim_hinge_cut = Part.makeBox(W, t + lip + 1, lip + 2)
rim_hinge_cut.translate(FreeCAD.Vector(0, -0.5, rect_h - 1))
rim = rim.cut(rim_hinge_cut)

box_body = box_shell.fuse(rim)

# Front latch ridge on exterior of front wall
latch_w, latch_d, latch_h = 18, 4, 6
latch = Part.makeBox(latch_w, latch_d, latch_h)
latch.translate(FreeCAD.Vector(W / 2 - latch_w / 2, D, rect_h / 2 - latch_h / 2))
box_body = box_body.fuse(latch)

# ============================================
# 2. BOX HINGE KNUCKLES (even indices: 0, 2, 4)
#    Positioned at back (Y=0), top of box (Z=rect_h)
# ============================================
box_knuckles = None
for i in range(num_knuckles):
    if i % 2 == 0:
        k = make_knuckle(i * (knuckle_len + knuckle_gap), knuckle_len, hinge_r, pin_r)
        k.translate(FreeCAD.Vector(0, 0, rect_h))
        box_knuckles = k if box_knuckles is None else box_knuckles.fuse(k)

# Arm from box back wall to knuckle center
arm_box = Part.makeBox(W, t, hinge_r)
arm_box.translate(FreeCAD.Vector(0, -t, rect_h - hinge_r))

box_final = box_body.fuse(box_knuckles).fuse(arm_box)

# Final cleanup cut: keep the box hinge bore fully open after arm fusion.
box_hinge_bore_clear = Part.makeCylinder(pin_r, hinge_length + 1,
                                         FreeCAD.Vector(-0.5, 0, rect_h),
                                         FreeCAD.Vector(1, 0, 0))
box_final = box_final.cut(box_hinge_bore_clear)

# ============================================
# 3. FLAT LID  (local coords: hinge at Y=0, Z=0)
# ============================================
# Flat top plate
lid_plate = Part.makeBox(W, D, lid_t)

# Two vent holes in the lid (Z direction) so the box body remains watertight.
for hx in [W / 2 - 15, W / 2 + 15]:
    lid_hole = Part.makeCylinder(2.0, lid_t + 2,
                                 FreeCAD.Vector(hx, D * 0.45, -1),
                                 FreeCAD.Vector(0, 0, 1))
    lid_plate = lid_plate.cut(lid_hole)

# Inner skirt ring: inset so it fits inside the box rim opening with clearance.
skirt_inset = t + lip + fit_clearance
skirt_outer_w = W - 2 * skirt_inset
skirt_outer_d = D - 2 * skirt_inset

skirt_outer = Part.makeBox(skirt_outer_w, skirt_outer_d, skirt_drop)
skirt_outer.translate(FreeCAD.Vector(skirt_inset, skirt_inset, -skirt_drop))

skirt_inner_cut = Part.makeBox(
    skirt_outer_w - 2 * skirt_wall,
    skirt_outer_d - 2 * skirt_wall,
    skirt_drop + 1,
)
skirt_inner_cut.translate(
    FreeCAD.Vector(skirt_inset + skirt_wall, skirt_inset + skirt_wall, -skirt_drop - 0.5)
)
skirt = skirt_outer.cut(skirt_inner_cut)

# Relief near hinge side so the lid can rotate closed without catching on the back edge.
hinge_relief = Part.makeBox(W + 2, skirt_inset + skirt_wall + 2, skirt_drop + 2)
hinge_relief.translate(FreeCAD.Vector(-1, -1, -skirt_drop - 1))
skirt = skirt.cut(hinge_relief)

lid_shell = lid_plate.fuse(skirt)

# ============================================
# 4. LID HINGE KNUCKLES (odd indices: 1, 3)
#    At Y=0, Z=0 in lid local coords
# ============================================
lid_knuckles = None
for i in range(num_knuckles):
    if i % 2 == 1:
        k = make_knuckle(i * (knuckle_len + knuckle_gap), knuckle_len, hinge_r, pin_r)
        lid_knuckles = k if lid_knuckles is None else lid_knuckles.fuse(k)

# Arm from flat lid back edge to knuckle center
arm_lid = Part.makeBox(W, t, hinge_r)
arm_lid.translate(FreeCAD.Vector(0, -t, 0))

lid_local = lid_shell.fuse(lid_knuckles).fuse(arm_lid)

# Final cleanup cut for lid hinge bores in lid local coordinates (Z=0 hinge axis).
lid_hinge_bore_clear = Part.makeCylinder(pin_r, hinge_length + 1,
                                         FreeCAD.Vector(-0.5, 0, 0),
                                         FreeCAD.Vector(1, 0, 0))
lid_local = lid_local.cut(lid_hinge_bore_clear)

# Place lid in CLOSED position (hinge center at Y=0, Z=rect_h)
lid_final = lid_local.copy()
lid_final.translate(FreeCAD.Vector(0, 0, rect_h))

# ============================================
# 5. HINGE PIN + END-STOP INSERTS
# ============================================
# shorten pin so end-stop stems and heads can sit outside the pin's axial region
pin_len = hinge_length - 2 * (end_stop_len + end_stop_head_t)
pin_start = end_stop_len + end_stop_head_t
pin = Part.makeCylinder(pin_r - 0.15, pin_len,
                        FreeCAD.Vector(pin_start, 0, rect_h),
                        FreeCAD.Vector(1, 0, 0))

# Two separate inserts that press into the outer hinge bores to trap the pin.
def make_end_stop(x_pos):
    stem_r = pin_r - end_stop_clearance
    stem = Part.makeCylinder(stem_r, end_stop_len,
                             FreeCAD.Vector(0, 0, rect_h),
                             FreeCAD.Vector(1, 0, 0))
    head = Part.makeCylinder(end_stop_head_r, end_stop_head_t,
                             FreeCAD.Vector(end_stop_len, 0, rect_h),
                             FreeCAD.Vector(1, 0, 0))
    stop = stem.fuse(head)
    stop.translate(FreeCAD.Vector(x_pos, 0, 0))
    return stop

left_end_stop = make_end_stop(0)
right_end_stop = make_end_stop(hinge_length - end_stop_len - end_stop_head_t)

# Exploded-view controls (assembly links only; part geometry stays unchanged)
exploded_view = False
explode_preset = "presentation"  # "compact" or "presentation"

explode_presets = {
    "compact": {
        "lid_z": 12.0,
        "pin_y": -6.0,
        "stop_x": 5.0,
        "stop_y": -8.0,
    },
    "presentation": {
        "lid_z": 22.0,
        "pin_y": -10.0,
        "stop_x": 8.0,
        "stop_y": -14.0,
    },
}

explode = explode_presets.get(explode_preset, explode_presets["presentation"])

# Create functional assembly joints (recommended to keep exploded_view = False)
use_assembly_joints = True

# View preference
hide_source_parts = True  # hide Box_Base/Lid_Flat/etc. and keep assembly links visible

# Print layout (separate arrangement for STL export)
create_print_layout = True
show_print_layout = True

# ============================================
# 6. BUILD PARTS AND ASSEMBLY
# ============================================
def make_part(doc, name, shape):
    part = doc.addObject("App::Part", name)
    feat = doc.addObject("Part::Feature", name + "_Shape")
    feat.Shape = shape
    part.addObject(feat)
    return part

box_part = make_part(doc, "Box_Base", box_final)
lid_part = make_part(doc, "Lid_Flat", lid_final)
pin_part = make_part(doc, "Hinge_Pin", pin)
left_stop_part = make_part(doc, "Hinge_End_Stop_Left", left_end_stop)
right_stop_part = make_part(doc, "Hinge_End_Stop_Right", right_end_stop)

assembly = doc.addObject("Assembly::AssemblyObject", "Assembly")
assembly.Type = "Assembly"
joint_group = assembly.newObject("Assembly::JointGroup", "Joints")

box_lnk = assembly.newObject("App::Link", box_part.Label + "_Link")
box_lnk.LinkedObject = box_part
box_lnk.LinkTransform = True

lid_lnk = assembly.newObject("App::Link", lid_part.Label + "_Link")
lid_lnk.LinkedObject = lid_part
lid_lnk.LinkTransform = True

pin_lnk = assembly.newObject("App::Link", pin_part.Label + "_Link")
pin_lnk.LinkedObject = pin_part
pin_lnk.LinkTransform = True

left_stop_lnk = assembly.newObject("App::Link", left_stop_part.Label + "_Link")
left_stop_lnk.LinkedObject = left_stop_part
left_stop_lnk.LinkTransform = True

right_stop_lnk = assembly.newObject("App::Link", right_stop_part.Label + "_Link")
right_stop_lnk.LinkedObject = right_stop_part
right_stop_lnk.LinkTransform = True

if hide_source_parts:
    try:
        for src_part in (box_part, lid_part, pin_part, left_stop_part, right_stop_part):
            src_part.Visibility = False
    except Exception:
        pass

if create_print_layout:
    print_layout = doc.addObject("App::Part", "Print_Layout")

    box_print = doc.addObject("App::Link", "Box_Base_Print")
    box_print.LinkedObject = box_part
    box_print.LinkTransform = True
    box_print.Placement.Base = FreeCAD.Vector(0, 0, 0)
    print_layout.addObject(box_print)

    lid_print = doc.addObject("App::Link", "Lid_Flat_Print")
    lid_print.LinkedObject = lid_part
    lid_print.LinkTransform = True
    lid_print.Placement.Base = FreeCAD.Vector(W + 20, 0, -rect_h)
    print_layout.addObject(lid_print)

    pin_bed_z = pin_r - 0.15
    pin_print = doc.addObject("App::Link", "Hinge_Pin_Print")
    pin_print.LinkedObject = pin_part
    pin_print.LinkTransform = True
    pin_print.Placement.Base = FreeCAD.Vector(0, D + 24, -(rect_h - pin_bed_z))
    print_layout.addObject(pin_print)

    # Stand end-stops on their circular end faces (axis vertical) for printing.
    left_stop_print_shape = left_end_stop.copy()
    left_stop_print_shape.rotate(FreeCAD.Vector(0, 0, rect_h), FreeCAD.Vector(0, 1, 0), 90)
    left_bb = left_stop_print_shape.BoundBox
    left_stop_print_shape.translate(
        FreeCAD.Vector((W + 20) - left_bb.XMin, (D + 24) - left_bb.YMin, -left_bb.ZMin)
    )
    left_stop_print = doc.addObject("Part::Feature", "Hinge_End_Stop_Left_Print")
    left_stop_print.Shape = left_stop_print_shape
    print_layout.addObject(left_stop_print)

    right_stop_print_shape = right_end_stop.copy()
    right_stop_print_shape.rotate(FreeCAD.Vector(hinge_length, 0, rect_h), FreeCAD.Vector(0, 1, 0), 90)
    right_bb = right_stop_print_shape.BoundBox
    right_stop_print_shape.translate(
        FreeCAD.Vector((W + 40) - right_bb.XMin, (D + 24) - right_bb.YMin, -right_bb.ZMin)
    )
    right_stop_print = doc.addObject("Part::Feature", "Hinge_End_Stop_Right_Print")
    right_stop_print.Shape = right_stop_print_shape
    print_layout.addObject(right_stop_print)

    print_layout.Visibility = show_print_layout

if exploded_view:
    lid_lnk.Placement.Base = FreeCAD.Vector(0, 0, explode["lid_z"])
    pin_lnk.Placement.Base = FreeCAD.Vector(0, explode["pin_y"], 0)
    left_stop_lnk.Placement.Base = FreeCAD.Vector(-explode["stop_x"], explode["stop_y"], 0)
    right_stop_lnk.Placement.Base = FreeCAD.Vector(explode["stop_x"], explode["stop_y"], 0)

if use_assembly_joints:
    import JointObject

    def obj_ref(link_obj):
        # Object-level reference: use object placement as the connector frame.
        return [link_obj, [""]]

    # Ground the base so the assembly has a stable reference frame.
    ground = joint_group.newObject("App::FeaturePython", "Ground_Box")
    JointObject.GroundedJoint(ground, box_lnk)

    # Revolute hinge between box and lid. Empty element refs mean object-level reference.
    hinge_joint = joint_group.newObject("App::FeaturePython", "Lid_Hinge_Revolute")
    JointObject.Joint(hinge_joint, 1)  # 1 = Revolute
    hinge_joint.Reference1 = obj_ref(pin_lnk)
    hinge_joint.Reference2 = obj_ref(lid_lnk)

    hinge_axis_rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), FreeCAD.Vector(1, 0, 0))
    hinge_jcs = FreeCAD.Placement(FreeCAD.Vector(0, 0, rect_h), hinge_axis_rot)
    # Keep custom JCS anchored on the hinge axis instead of auto-updating from object refs.
    hinge_joint.Detach1 = True
    hinge_joint.Detach2 = True
    hinge_joint.Placement1 = hinge_jcs
    hinge_joint.Placement2 = hinge_jcs

    # Keep hardware attached to the base with fixed joints.
    def make_fixed_joint(name, moving_link):
        j = joint_group.newObject("App::FeaturePython", name)
        JointObject.Joint(j, 0)  # 0 = Fixed
        j.Reference1 = obj_ref(box_lnk)
        j.Reference2 = obj_ref(moving_link)
        j.Placement1 = FreeCAD.Placement()
        j.Placement2 = FreeCAD.Placement()
        return j

    make_fixed_joint("Pin_Fixed", pin_lnk)
    make_fixed_joint("Left_End_Stop_Fixed", left_stop_lnk)
    make_fixed_joint("Right_End_Stop_Fixed", right_stop_lnk)

    try:
        assembly.solve()
    except Exception:
        pass

doc.recompute()

try:
    import FreeCADGui
    FreeCADGui.ActiveDocument.ActiveView.fitAll()
except Exception:
    pass

print("=== Retainer Box ===")
print("Base:  {}x{}x{} mm".format(W, D, rect_h))
print("Lid:   flat cover, thickness {} mm".format(lid_t))
print("Parts: Box_Base, Lid_Flat, Hinge_Pin, Hinge_End_Stop_Left, Hinge_End_Stop_Right")
print("Exploded view: {} ({})".format(exploded_view, explode_preset if exploded_view else "n/a"))
print("Joints enabled: {}".format(use_assembly_joints))
print("Print layout: {}".format(create_print_layout))
print("Wall:  {} mm, Hinge: {} knuckles, pin dia {} mm".format(t, num_knuckles, pin_r * 2))
