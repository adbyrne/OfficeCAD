#!/usr/bin/env python3
"""
Parametric 10-inch Rack Panel Generator for Raspberry Pi Boxes

Generates a three-piece 1U rack panel (center panel + 2 end tabs) in FreeCAD
via the XML-RPC bridge at localhost:9875.

Usage:
    python3 generate_rack_panel.py [--output-dir DIR] [--no-export]

Requires: FreeCAD running with the Robust MCP bridge active on port 9875.
"""

import xmlrpc.client
import json
import math
import argparse
import sys

# ─── Parameters ──────────────────────────────────────────────────────────────
# All dimensions in mm. Edit these to customise the design.

# Rack standard
RACK_1U_HEIGHT = 44.45          # 1U = 1.75"
PANEL_WIDTH = 212.0             # Between tab overlaps (252mm hole-to-hole - 2×20mm)
FACE_PLATE_THICKNESS = 4.0      # Z=0 to Z=4
WALL_THICKNESS = 4.0            # Top and bottom wall thickness (Y)
SHELF_DEPTH = 34.0              # Wall depth behind face plate (Z=4 to Z=38)

# Lip (front perimeter frame)
LIP_DEPTH = 3.0                 # Z=-3 to Z=0 (protrudes forward)
LIP_INSET = 3.0                 # Inset from panel edges (X and Y)

# Pi box openings (inside center panel)
BOX_WIDTH = 62.0                # Physical box width
BOX_TOLERANCE = 1.0             # Extra clearance per box opening
BOX_OPENING = BOX_WIDTH + BOX_TOLERANCE  # 63mm
BOX_LEFT_X = 33.0              # Left box opening starts at X=33
BOX_RIGHT_X = 116.0            # Right box opening starts at X=116
BOX_GAP = 20.0                 # Gap between boxes (X=96 to X=116)
BOX_HEIGHT = 37.0              # Physical box height
BOX_Y_START = WALL_THICKNESS   # Box sits on bottom wall top surface (Y=4)
BOX_Y_END = BOX_Y_START + BOX_HEIGHT  # Y=41
CUTOUT_LIP = 3.0               # Lip around each box cutout in face plate

# End tab
TAB_RAIL_WIDTH = 15.0           # Width extending beyond panel for rail mounting
TAB_OVERLAP_WIDTH = 12.0        # Width overlapping inside the panel lip
TAB_DEPTH = 7.0                 # Z=-7 to Z=0 (tab face at Z=-7)
TAB_LIP_GROOVE_WIDTH = 3.0      # Groove for panel lip (matches LIP_INSET)
TAB_LIP_GROOVE_DEPTH = 3.0      # Groove depth (matches LIP_DEPTH)

# Joint screws (tab to panel connection)
JOINT_SCREW_X = 7.0            # Distance from panel edge in X
JOINT_SCREW_Y_POSITIONS = [11.0, 33.45]  # Y positions for 2 screws per side
M3_CLEARANCE_RADIUS = 1.6      # 3.2mm diameter
COUNTERBORE_RADIUS = 3.0       # 6mm diameter
COUNTERBORE_DEPTH = 3.5        # Screw head recess depth
NUT_ACROSS_FLATS = 5.5         # M3 hex nut
NUT_RECESS_DEPTH = 1.5         # Shallow recess on panel back

# EIA-310 rail mounting holes (1U, 3-hole pattern)
RAIL_HOLE_CENTER_DIA = 6.3     # Center hole (may be slotted)
RAIL_HOLE_OUTER_DIA = 4.6      # Top and bottom holes
RAIL_HOLE_SPACING = 16.0       # Between center and outer holes
RAIL_HOLE_CENTER_Y = RACK_1U_HEIGHT / 2  # 22.225mm

# Fillets
WALL_FILLET_RADIUS = 2.0       # Wall-to-faceplate inside corners

# ─── Derived values ──────────────────────────────────────────────────────────
TOTAL_DEPTH = LIP_DEPTH + FACE_PLATE_THICKNESS + SHELF_DEPTH  # 41mm
TAB_TOTAL_WIDTH = TAB_RAIL_WIDTH + TAB_OVERLAP_WIDTH  # 27mm
RAIL_HOLE_X_CENTER = -(TAB_RAIL_WIDTH / 2)  # Centered in rail section
HEX_CIRCUMRADIUS = NUT_ACROSS_FLATS / (2 * math.cos(math.radians(30)))


# ─── FreeCAD execution helpers ───────────────────────────────────────────────

def execute(proxy, code):
    """Execute Python code in FreeCAD, return result or raise on error."""
    result = proxy.execute(code)
    if not result.get('success'):
        err = result.get('error_message', 'Unknown error')
        tb = result.get('error_traceback', '')
        raise RuntimeError(f"FreeCAD error: {err}\n{tb}")
    return result.get('result')


def make_rectangle_lines(points_str):
    """Return FreeCAD code to add a closed rectangle from 4 corner vectors."""
    return f"""
pts = {points_str}
for i in range(4):
    sketch.addGeometry(Part.LineSegment(pts[i], pts[(i+1)%4]), False)
for i in range(4):
    sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1)%4, 1))
"""


# ─── Build functions ─────────────────────────────────────────────────────────

def create_document(proxy):
    """Step 1: Create document and center panel body."""
    execute(proxy, """
doc = FreeCAD.newDocument("RackPanel")
doc.Label = "RackPanel"
FreeCAD.setActiveDocument("RackPanel")
doc.recompute()
_result_ = {"doc": doc.Name}
""")


def build_center_panel(proxy):
    """Steps 2-7: Build the complete center panel."""
    p = {
        'W': PANEL_WIDTH, 'H': RACK_1U_HEIGHT,
        'FPT': FACE_PLATE_THICKNESS, 'WT': WALL_THICKNESS,
        'SD': SHELF_DEPTH, 'LD': LIP_DEPTH, 'LI': LIP_INSET,
    }

    # Create body
    execute(proxy, """
doc = FreeCAD.ActiveDocument
body = doc.addObject("PartDesign::Body", "CenterPanelBody")
body.Label = "CenterPanelBody"
doc.recompute()
_result_ = {"body": body.Name}
""")

    # Face plate pad
    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
body = doc.getObject("CenterPanelBody")
sketch = body.newObject("Sketcher::SketchObject", "FacePlateSketch")
sketch.AttachmentSupport = [(body.Origin.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"
doc.recompute()
pts = [FreeCAD.Vector(0,0,0), FreeCAD.Vector({p['W']},0,0),
       FreeCAD.Vector({p['W']},{p['H']},0), FreeCAD.Vector(0,{p['H']},0)]
for i in range(4):
    sketch.addGeometry(Part.LineSegment(pts[i], pts[(i+1)%4]), False)
for i in range(4):
    sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1)%4, 1))
doc.recompute()
pad = body.newObject("PartDesign::Pad", "FacePlatePad")
pad.Profile = sketch
pad.Length = {p['FPT']}
pad.Reversed = False
pad.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # Bottom wall
    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
body = doc.getObject("CenterPanelBody")
sketch = body.newObject("Sketcher::SketchObject", "BottomWallSketch")
sketch.AttachmentSupport = [(doc.getObject("FacePlatePad"), "Face6")]
sketch.MapMode = "FlatFace"
doc.recompute()
pts = [FreeCAD.Vector(0,0,0), FreeCAD.Vector({p['W']},0,0),
       FreeCAD.Vector({p['W']},{p['WT']},0), FreeCAD.Vector(0,{p['WT']},0)]
for i in range(4):
    sketch.addGeometry(Part.LineSegment(pts[i], pts[(i+1)%4]), False)
for i in range(4):
    sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1)%4, 1))
doc.recompute()
pad = body.newObject("PartDesign::Pad", "BottomWallPad")
pad.Profile = sketch
pad.Length = {p['SD']}
pad.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # Top wall
    top_y = RACK_1U_HEIGHT - WALL_THICKNESS
    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
body = doc.getObject("CenterPanelBody")
sketch = body.newObject("Sketcher::SketchObject", "TopWallSketch")
sketch.AttachmentSupport = [(doc.getObject("FacePlatePad"), "Face6")]
sketch.MapMode = "FlatFace"
doc.recompute()
pts = [FreeCAD.Vector(0,{top_y},0), FreeCAD.Vector({p['W']},{top_y},0),
       FreeCAD.Vector({p['W']},{p['H']},0), FreeCAD.Vector(0,{p['H']},0)]
for i in range(4):
    sketch.addGeometry(Part.LineSegment(pts[i], pts[(i+1)%4]), False)
for i in range(4):
    sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1)%4, 1))
doc.recompute()
pad = body.newObject("PartDesign::Pad", "TopWallPad")
pad.Profile = sketch
pad.Length = {p['SD']}
pad.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # Lip block (full face, reversed into -Z)
    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
body = doc.getObject("CenterPanelBody")
sketch = body.newObject("Sketcher::SketchObject", "LipBlockSketch")
sketch.AttachmentSupport = [(body.Origin.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"
doc.recompute()
pts = [FreeCAD.Vector(0,0,0), FreeCAD.Vector({p['W']},0,0),
       FreeCAD.Vector({p['W']},{p['H']},0), FreeCAD.Vector(0,{p['H']},0)]
for i in range(4):
    sketch.addGeometry(Part.LineSegment(pts[i], pts[(i+1)%4]), False)
for i in range(4):
    sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1)%4, 1))
doc.recompute()
pad = body.newObject("PartDesign::Pad", "LipBlockPad")
pad.Profile = sketch
pad.Length = {p['LD']}
pad.Reversed = True
pad.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # Lip pocket (remove center to leave frame)
    li = LIP_INSET
    inner_w = PANEL_WIDTH - 2 * li
    inner_h = RACK_1U_HEIGHT - 2 * li
    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
body = doc.getObject("CenterPanelBody")
sketch = body.newObject("Sketcher::SketchObject", "LipPocketSketch")
sketch.AttachmentSupport = [(body.Origin.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"
sketch.AttachmentOffset = FreeCAD.Placement(
    FreeCAD.Vector(0, 0, -{p['LD']}), FreeCAD.Rotation(0, 0, 0))
doc.recompute()
pts = [FreeCAD.Vector({li},{li},0), FreeCAD.Vector({li + inner_w},{li},0),
       FreeCAD.Vector({li + inner_w},{li + inner_h},0), FreeCAD.Vector({li},{li + inner_h},0)]
for i in range(4):
    sketch.addGeometry(Part.LineSegment(pts[i], pts[(i+1)%4]), False)
for i in range(4):
    sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1)%4, 1))
doc.recompute()
pocket = body.newObject("PartDesign::Pocket", "LipPocket")
pocket.Profile = sketch
pocket.Length = {p['LD']}
pocket.Reversed = False
pocket.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # Joint screw holes (through-all in Z) + hex nut recesses
    hole_positions = []
    for y in JOINT_SCREW_Y_POSITIONS:
        hole_positions.append((JOINT_SCREW_X, y))
        hole_positions.append((PANEL_WIDTH - JOINT_SCREW_X, y))
    hp_str = repr([(x, y) for x, y in hole_positions])

    execute(proxy, f"""
import Part, Sketcher, math
doc = FreeCAD.ActiveDocument
body = doc.getObject("CenterPanelBody")

# Clearance holes
sketch = body.newObject("Sketcher::SketchObject", "JointHolesSketch")
sketch.AttachmentSupport = [(body.Origin.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"
doc.recompute()
for x, y in {hp_str}:
    sketch.addGeometry(Part.Circle(FreeCAD.Vector(x, y, 0), FreeCAD.Vector(0,0,1), {M3_CLEARANCE_RADIUS}), False)
doc.recompute()
pocket = body.newObject("PartDesign::Pocket", "JointHolesPocket")
pocket.Profile = sketch
pocket.Type = 1
pocket.Refine = True
doc.recompute()

# Hex nut recesses on back face
sketch_nut = body.newObject("Sketcher::SketchObject", "NutRecessSketch")
sketch_nut.AttachmentSupport = [(doc.getObject("FacePlatePad"), "Face6")]
sketch_nut.MapMode = "FlatFace"
doc.recompute()
hex_r = {HEX_CIRCUMRADIUS}
for idx, (x, y) in enumerate({hp_str}):
    for j in range(6):
        a1 = math.radians(60 * j + 30)
        a2 = math.radians(60 * (j + 1) + 30)
        sketch_nut.addGeometry(Part.LineSegment(
            FreeCAD.Vector(x + hex_r * math.cos(a1), y + hex_r * math.sin(a1), 0),
            FreeCAD.Vector(x + hex_r * math.cos(a2), y + hex_r * math.sin(a2), 0)
        ), False)
    base = idx * 6
    for j in range(6):
        sketch_nut.addConstraint(Sketcher.Constraint("Coincident", base+j, 2, base+(j+1)%6, 1))
doc.recompute()
pocket_nut = body.newObject("PartDesign::Pocket", "NutRecessPocket")
pocket_nut.Profile = sketch_nut
pocket_nut.Length = {NUT_RECESS_DEPTH}
pocket_nut.Reversed = False
pocket_nut.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # Pi box face plate cutouts
    cl = CUTOUT_LIP
    cuts = [
        (BOX_LEFT_X + cl, BOX_Y_START + cl,
         BOX_LEFT_X + BOX_OPENING - cl, BOX_Y_END - cl),
        (BOX_RIGHT_X + cl, BOX_Y_START + cl,
         BOX_RIGHT_X + BOX_OPENING - cl, BOX_Y_END - cl),
    ]
    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
body = doc.getObject("CenterPanelBody")
sketch = body.newObject("Sketcher::SketchObject", "BoxCutoutSketch")
sketch.AttachmentSupport = [(body.Origin.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"
sketch.AttachmentOffset = FreeCAD.Placement(
    FreeCAD.Vector(0, 0, -{LIP_DEPTH}), FreeCAD.Rotation(0, 0, 0))
doc.recompute()
cuts = {cuts}
for ci, (x1, y1, x2, y2) in enumerate(cuts):
    base = ci * 4
    pts = [FreeCAD.Vector(x1,y1,0), FreeCAD.Vector(x2,y1,0),
           FreeCAD.Vector(x2,y2,0), FreeCAD.Vector(x1,y2,0)]
    for i in range(4):
        sketch.addGeometry(Part.LineSegment(pts[i], pts[(i+1)%4]), False)
    for i in range(4):
        sketch.addConstraint(Sketcher.Constraint("Coincident", base+i, 2, base+(i+1)%4, 1))
doc.recompute()
pocket = body.newObject("PartDesign::Pocket", "BoxCutoutPocket")
pocket.Profile = sketch
pocket.Type = 1
pocket.Reversed = True
pocket.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # Fillets on wall-faceplate inside corners
    execute(proxy, f"""
doc = FreeCAD.ActiveDocument
body = doc.getObject("CenterPanelBody")
tip = body.Tip
shape = tip.Shape
fillet_edges = []
for i, edge in enumerate(shape.Edges):
    v1 = edge.Vertexes[0].Point
    v2 = edge.Vertexes[1].Point
    # Bottom wall junction: y≈{WALL_THICKNESS}, z≈{FACE_PLATE_THICKNESS}
    if (abs(v1.y - {WALL_THICKNESS}) < 0.1 and abs(v2.y - {WALL_THICKNESS}) < 0.1 and
        abs(v1.z - {FACE_PLATE_THICKNESS}) < 0.1 and abs(v2.z - {FACE_PLATE_THICKNESS}) < 0.1 and
        edge.Length > 20):
        fillet_edges.append(f"Edge{{i+1}}")
    # Top wall junction: y≈{RACK_1U_HEIGHT - WALL_THICKNESS}, z≈{FACE_PLATE_THICKNESS}
    if (abs(v1.y - {RACK_1U_HEIGHT - WALL_THICKNESS}) < 0.1 and abs(v2.y - {RACK_1U_HEIGHT - WALL_THICKNESS}) < 0.1 and
        abs(v1.z - {FACE_PLATE_THICKNESS}) < 0.1 and abs(v2.z - {FACE_PLATE_THICKNESS}) < 0.1 and
        edge.Length > 20):
        fillet_edges.append(f"Edge{{i+1}}")

if fillet_edges:
    fillet = body.newObject("PartDesign::Fillet", "WallFillets")
    fillet.Base = (tip, fillet_edges)
    fillet.Radius = {WALL_FILLET_RADIUS}
    doc.recompute()
_result_ = {{"fillets": len(fillet_edges)}}
""")

    print("  Center panel complete.")


def build_left_tab(proxy):
    """Steps 8-10: Build the left end tab."""
    li = LIP_INSET
    top_y = RACK_1U_HEIGHT - li
    rail_x = -TAB_RAIL_WIDTH

    # L-shaped tab profile
    pts_str = repr([
        (rail_x, 0), (0, 0), (0, li),
        (TAB_OVERLAP_WIDTH, li), (TAB_OVERLAP_WIDTH, top_y),
        (0, top_y), (0, RACK_1U_HEIGHT), (rail_x, RACK_1U_HEIGHT),
    ])

    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
tab_body = doc.addObject("PartDesign::Body", "LeftTabBody")
tab_body.Label = "LeftTabBody"
doc.recompute()
sketch = tab_body.newObject("Sketcher::SketchObject", "TabProfileSketch")
sketch.AttachmentSupport = [(tab_body.Origin.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"
doc.recompute()
pts_raw = {pts_str}
pts = [FreeCAD.Vector(x, y, 0) for x, y in pts_raw]
n = len(pts)
for i in range(n):
    sketch.addGeometry(Part.LineSegment(pts[i], pts[(i+1)%n]), False)
for i in range(n):
    sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1)%n, 1))
doc.recompute()
pad = tab_body.newObject("PartDesign::Pad", "TabPad")
pad.Profile = sketch
pad.Length = {TAB_DEPTH}
pad.Reversed = True
pad.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # Lip groove pocket
    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
tab_body = doc.getObject("LeftTabBody")
sketch = tab_body.newObject("Sketcher::SketchObject", "LipPocketSketch001")
sketch.AttachmentSupport = [(tab_body.Origin.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"
doc.recompute()
pts = [FreeCAD.Vector(0,{li},0), FreeCAD.Vector({TAB_LIP_GROOVE_WIDTH},{li},0),
       FreeCAD.Vector({TAB_LIP_GROOVE_WIDTH},{top_y},0), FreeCAD.Vector(0,{top_y},0)]
for i in range(4):
    sketch.addGeometry(Part.LineSegment(pts[i], pts[(i+1)%4]), False)
for i in range(4):
    sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1)%4, 1))
doc.recompute()
pocket = tab_body.newObject("PartDesign::Pocket", "LipGroovePocket")
pocket.Profile = sketch
pocket.Length = {TAB_LIP_GROOVE_DEPTH}
pocket.Reversed = False
pocket.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # EIA-310 rail holes
    rail_cx = RAIL_HOLE_X_CENTER
    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
tab_body = doc.getObject("LeftTabBody")
sketch = tab_body.newObject("Sketcher::SketchObject", "RailHolesSketch")
sketch.AttachmentSupport = [(tab_body.Origin.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"
sketch.AttachmentOffset = FreeCAD.Placement(
    FreeCAD.Vector(0, 0, -{TAB_DEPTH}), FreeCAD.Rotation(0, 0, 0))
doc.recompute()
sketch.addGeometry(Part.Circle(FreeCAD.Vector({rail_cx}, {RAIL_HOLE_CENTER_Y - RAIL_HOLE_SPACING}, 0), FreeCAD.Vector(0,0,1), {RAIL_HOLE_OUTER_DIA/2}), False)
sketch.addGeometry(Part.Circle(FreeCAD.Vector({rail_cx}, {RAIL_HOLE_CENTER_Y}, 0), FreeCAD.Vector(0,0,1), {RAIL_HOLE_CENTER_DIA/2}), False)
sketch.addGeometry(Part.Circle(FreeCAD.Vector({rail_cx}, {RAIL_HOLE_CENTER_Y + RAIL_HOLE_SPACING}, 0), FreeCAD.Vector(0,0,1), {RAIL_HOLE_OUTER_DIA/2}), False)
doc.recompute()
pocket = tab_body.newObject("PartDesign::Pocket", "RailHolesPocket")
pocket.Profile = sketch
pocket.Type = 1
pocket.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    # Joint screw clearance holes + counterbores
    jx = JOINT_SCREW_X
    jy_str = repr(JOINT_SCREW_Y_POSITIONS)
    execute(proxy, f"""
import Part, Sketcher
doc = FreeCAD.ActiveDocument
tab_body = doc.getObject("LeftTabBody")

# Clearance holes
sketch = tab_body.newObject("Sketcher::SketchObject", "TabJointClearSketch")
sketch.AttachmentSupport = [(tab_body.Origin.getObject("XY_Plane"), "")]
sketch.MapMode = "FlatFace"
doc.recompute()
for y in {jy_str}:
    sketch.addGeometry(Part.Circle(FreeCAD.Vector({jx}, y, 0), FreeCAD.Vector(0,0,1), {M3_CLEARANCE_RADIUS}), False)
doc.recompute()
pocket = tab_body.newObject("PartDesign::Pocket", "TabJointClearPocket")
pocket.Profile = sketch
pocket.Type = 1
pocket.Refine = True
doc.recompute()

# Counterbores
sketch_cb = tab_body.newObject("Sketcher::SketchObject", "TabCounterboreSketch")
sketch_cb.AttachmentSupport = [(tab_body.Origin.getObject("XY_Plane"), "")]
sketch_cb.MapMode = "FlatFace"
sketch_cb.AttachmentOffset = FreeCAD.Placement(
    FreeCAD.Vector(0, 0, -{TAB_DEPTH}), FreeCAD.Rotation(0, 0, 0))
doc.recompute()
for y in {jy_str}:
    sketch_cb.addGeometry(Part.Circle(FreeCAD.Vector({jx}, y, 0), FreeCAD.Vector(0,0,1), {COUNTERBORE_RADIUS}), False)
doc.recompute()
pocket_cb = tab_body.newObject("PartDesign::Pocket", "TabCounterborePocket")
pocket_cb.Profile = sketch_cb
pocket_cb.Length = {COUNTERBORE_DEPTH}
pocket_cb.Reversed = False
pocket_cb.Refine = True
doc.recompute()
_result_ = {{"ok": True}}
""")

    print("  Left tab complete.")


def build_right_tab(proxy):
    """Step 11: Mirror left tab to create right tab."""
    execute(proxy, f"""
doc = FreeCAD.ActiveDocument
left_tab = doc.getObject("LeftTabBody")
left_shape = left_tab.Shape.copy()
mirror_matrix = FreeCAD.Matrix()
mirror_matrix.A11 = -1
mirror_matrix.A14 = {PANEL_WIDTH}
mirrored_shape = left_shape.transformGeometry(mirror_matrix)
right_tab = doc.addObject("Part::Feature", "RightTabBody")
right_tab.Shape = mirrored_shape
right_tab.Label = "RightTabBody"
doc.recompute()
_result_ = {{"ok": True}}
""")
    print("  Right tab (mirrored) complete.")


def export_stls(proxy, output_dir):
    """Export all parts as STL files."""
    execute(proxy, f"""
import MeshPart
doc = FreeCAD.ActiveDocument
output_dir = "{output_dir}"
for name, label in [("CenterPanelBody", "CenterPanel"),
                     ("LeftTabBody", "LeftTab"),
                     ("RightTabBody", "RightTab")]:
    obj = doc.getObject(name)
    mesh = MeshPart.meshFromShape(Shape=obj.Shape, LinearDeflection=0.1, AngularDeflection=0.5)
    mesh.write(f"{{output_dir}}/{{label}}.stl")
_result_ = {{"exported": 3}}
""")
    print(f"  STLs exported to {output_dir}")


def save_document(proxy, filepath):
    """Save the FreeCAD document."""
    execute(proxy, f"""
doc = FreeCAD.ActiveDocument
doc.saveAs("{filepath}")
_result_ = {{"saved": doc.FileName}}
""")
    print(f"  Document saved to {filepath}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate rack panel in FreeCAD")
    parser.add_argument('--output-dir',
                        default='/home/abyrne/Projects/Office/cad/rack-panel-rpi/printed_files',
                        help='Directory for STL exports')
    parser.add_argument('--fcstd-path',
                        default='/home/abyrne/Projects/Office/cad/rack-panel-rpi/freecad_files/RackPanel.FCStd',
                        help='Path for FreeCAD document')
    parser.add_argument('--no-export', action='store_true',
                        help='Skip STL export')
    parser.add_argument('--port', type=int, default=9875,
                        help='FreeCAD XML-RPC port')
    args = parser.parse_args()

    proxy = xmlrpc.client.ServerProxy(f'http://localhost:{args.port}')

    # Verify connection
    try:
        proxy.ping()
    except Exception as e:
        print(f"Error: Cannot connect to FreeCAD at localhost:{args.port}")
        print(f"  Ensure FreeCAD is running with the MCP bridge active.")
        sys.exit(1)

    print("Generating 10-inch Rack Panel...")
    print(f"  Panel: {PANEL_WIDTH}x{RACK_1U_HEIGHT}mm, depth {TOTAL_DEPTH}mm")
    print(f"  Tabs: {TAB_TOTAL_WIDTH}x{RACK_1U_HEIGHT}x{TAB_DEPTH}mm")

    print("\n1. Creating document...")
    create_document(proxy)

    print("2. Building center panel...")
    build_center_panel(proxy)

    print("3. Building left end tab...")
    build_left_tab(proxy)

    print("4. Building right end tab (mirror)...")
    build_right_tab(proxy)

    print("5. Saving document...")
    save_document(proxy, args.fcstd_path)

    if not args.no_export:
        print("6. Exporting STLs...")
        export_stls(proxy, args.output_dir)

    print("\nDone! Three-piece rack panel generated successfully.")
    print(f"  FreeCAD: {args.fcstd_path}")
    if not args.no_export:
        print(f"  STLs:    {args.output_dir}/")


if __name__ == '__main__':
    main()
