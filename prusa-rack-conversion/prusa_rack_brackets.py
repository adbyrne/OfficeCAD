#!/usr/bin/env python3
"""
Prusa Frame to 6U Rack Mount Brackets - FreeCAD Design Script

This script generates 3D-printable L-brackets to mount standard 6U rack rails
to a Prusa MK3S/MK4S 3D printer frame using the z-axis screw locations.

Requirements:
    - FreeCAD 0.21+ with Python 3.11
    - Run from FreeCAD's Python console or as a macro

Usage:
    exec(open("prusa_rack_brackets.py").read())

    Or import as module:
    import prusa_rack_brackets
    prusa_rack_brackets.create_all_brackets()

License: GNU General Public License v3.0
Author: adbyrne
Repository: https://github.com/adbyrne/OfficeCAD
"""

import FreeCAD
import Part
import Sketcher
import PartDesign
import MeshPart
import os

# =============================================================================
# DESIGN PARAMETERS
# =============================================================================

# Frame leg dimensions
FRAME_LEG_DEPTH = 45.0      # mm - depth into frame
FRAME_LEG_WIDTH = 40.0      # mm - width of bracket base
FRAME_LEG_THICKNESS = 4.0   # mm - material thickness

# Rail leg dimensions
RAIL_LEG_HEIGHT = 39.0      # mm - matches 6U rail L-angle depth
RAIL_LEG_THICKNESS = 4.0    # mm - material thickness

# Rail extensions (for 6U centering in frame)
TOP_RAIL_EXTENSION = 97.0   # mm - total rail leg length (40 base + 57 extension)
BOTTOM_RAIL_EXTENSION = 95.0  # mm - total rail leg length (40 base + 55 extension)

# Angle brace (structural reinforcement at inside corner)
ANGLE_BRACE_SIZE = 10.0     # mm - leg length of triangular brace

# Frame mounting holes (M3)
FRAME_HOLE_DIAMETER = 3.2   # mm - M3 clearance hole
FRAME_HOLE_SPACING = 20.0   # mm - between holes

# Top bracket frame holes
TOP_FRAME_HOLE_INNER = 17.5  # mm - inner hole distance from inside edge
TOP_FRAME_HOLE_OUTER = 37.5  # mm - outer hole distance from inside edge
TOP_FRAME_HOLE_Z = 10.0      # mm - Z position from bracket base

# Bottom bracket frame holes (triangle pattern)
BOTTOM_FRAME_HOLE_TOP_INNER = 17.5   # mm - from inside edge (X direction)
BOTTOM_FRAME_HOLE_TOP_OUTER = 37.5   # mm - from inside edge (X direction)
BOTTOM_FRAME_HOLE_TOP_Z = 10.0       # mm - Z position
BOTTOM_FRAME_HOLE_APEX_X = 27.5      # mm - from inside edge
BOTTOM_FRAME_HOLE_APEX_Z = 30.0      # mm - Z position

# Rail mounting holes (EIA-310 standard pattern)
RAIL_HOLE_CENTER_DIA = 6.3   # mm - center hole (slotted)
RAIL_HOLE_OUTER_DIA = 4.6    # mm - outer holes
RAIL_HOLE_SPACING = 16.0     # mm - between holes
RAIL_HOLE_Y_CENTER = 19.5    # mm - centered on rail leg

# Top bracket rail holes (Z positions)
TOP_RAIL_HOLE_BOTTOM = 54.0  # mm
TOP_RAIL_HOLE_CENTER = 70.0  # mm
TOP_RAIL_HOLE_TOP = 86.0     # mm

# Bottom bracket rail holes (Z positions, negative = below base)
BOTTOM_RAIL_HOLE_TOP = -11.5     # mm
BOTTOM_RAIL_HOLE_CENTER = -27.5  # mm
BOTTOM_RAIL_HOLE_BOTTOM = -43.5  # mm


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_l_profile_sketch(body, name="LProfileSketch"):
    """
    Create the L-profile sketch with integrated angle brace.

    Profile vertices (counterclockwise from bottom-left):
    (-45, -4) -> (-45, 0) -> (-10, 0) -> (0, 10) -> (0, 39) ->
    (4, 39) -> (4, 0) -> (4, -4) -> close
    """
    sketch = body.newObject("Sketcher::SketchObject", name)
    sketch.AttachmentSupport = [(body.Origin.OriginFeatures[3], "")]  # XY_Plane
    sketch.MapMode = "FlatFace"

    # Define vertices
    vertices = [
        (-FRAME_LEG_DEPTH, -FRAME_LEG_THICKNESS),           # 0: bottom-left
        (-FRAME_LEG_DEPTH, 0),                               # 1: top-left of frame leg
        (-ANGLE_BRACE_SIZE, 0),                              # 2: start of angle brace
        (0, ANGLE_BRACE_SIZE),                               # 3: end of angle brace
        (0, RAIL_LEG_HEIGHT),                                # 4: top of rail leg (inner)
        (RAIL_LEG_THICKNESS, RAIL_LEG_HEIGHT),               # 5: top of rail leg (outer)
        (RAIL_LEG_THICKNESS, 0),                             # 6: base of rail leg (outer)
        (RAIL_LEG_THICKNESS, -FRAME_LEG_THICKNESS),          # 7: bottom-right
    ]

    # Create lines
    for i in range(len(vertices)):
        p1 = FreeCAD.Vector(vertices[i][0], vertices[i][1], 0)
        p2 = FreeCAD.Vector(vertices[(i+1) % len(vertices)][0], vertices[(i+1) % len(vertices)][1], 0)
        sketch.addGeometry(Part.LineSegment(p1, p2), False)

    # Add constraints (simplified - full constraints would be added for parametric design)
    sketch.recompute()
    return sketch


def create_frame_holes_sketch(body, base_feature, holes_config, name="FrameHolesSketch"):
    """
    Create frame mounting holes sketch on the bottom face of frame leg.

    holes_config: list of (x_from_inside_edge, z_position) tuples
    """
    sketch = body.newObject("Sketcher::SketchObject", name)

    # Attach to bottom face of frame leg (Y = -4 face)
    sketch.AttachmentSupport = [(base_feature, "Face")]  # Will need face selection
    sketch.MapMode = "FlatFace"

    for x_pos, z_pos in holes_config:
        # X is negative (from inside edge toward outside)
        sketch.addGeometry(Part.Circle(
            FreeCAD.Vector(-x_pos, z_pos, 0),
            FreeCAD.Vector(0, 0, 1),
            FRAME_HOLE_DIAMETER / 2
        ), False)

    sketch.recompute()
    return sketch


def create_rail_holes_sketch(body, base_feature, holes_config, name="RailHolesSketch"):
    """
    Create rail mounting holes sketch on the outer face of rail leg.

    holes_config: list of (z_position, diameter) tuples
    """
    sketch = body.newObject("Sketcher::SketchObject", name)
    sketch.MapMode = "FlatFace"

    for z_pos, diameter in holes_config:
        sketch.addGeometry(Part.Circle(
            FreeCAD.Vector(-RAIL_HOLE_Y_CENTER, z_pos, 0),
            FreeCAD.Vector(0, 0, 1),
            diameter / 2
        ), False)

    sketch.recompute()
    return sketch


# =============================================================================
# MAIN BRACKET CREATION FUNCTIONS
# =============================================================================

def create_top_bracket_left(doc):
    """Create the top-left bracket with all features."""

    # Create PartDesign Body
    body = doc.addObject("PartDesign::Body", "TopBracketLeftBody")

    # 1. L-Profile base sketch and pad
    lprofile = create_l_profile_sketch(body, "LProfileSketch")

    pad = body.newObject("PartDesign::Pad", "LProfilePad")
    pad.Profile = lprofile
    pad.Length = FRAME_LEG_WIDTH
    pad.Refine = True

    # 2. Rail extension sketch and pad
    ext_sketch = body.newObject("Sketcher::SketchObject", "RailExtensionSketch")
    ext_sketch.MapMode = "FlatFace"
    # Rectangle for rail extension on top face
    ext_sketch.addGeometry(Part.LineSegment(
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(RAIL_LEG_THICKNESS, 0, 0)
    ), False)
    ext_sketch.addGeometry(Part.LineSegment(
        FreeCAD.Vector(RAIL_LEG_THICKNESS, 0, 0),
        FreeCAD.Vector(RAIL_LEG_THICKNESS, RAIL_LEG_HEIGHT, 0)
    ), False)
    ext_sketch.addGeometry(Part.LineSegment(
        FreeCAD.Vector(RAIL_LEG_THICKNESS, RAIL_LEG_HEIGHT, 0),
        FreeCAD.Vector(0, RAIL_LEG_HEIGHT, 0)
    ), False)
    ext_sketch.addGeometry(Part.LineSegment(
        FreeCAD.Vector(0, RAIL_LEG_HEIGHT, 0),
        FreeCAD.Vector(0, 0, 0)
    ), False)

    ext_pad = body.newObject("PartDesign::Pad", "RailExtensionPad")
    ext_pad.Profile = ext_sketch
    ext_pad.Length = TOP_RAIL_EXTENSION - FRAME_LEG_WIDTH  # 57mm extension
    ext_pad.Refine = True

    # 3. Frame holes
    frame_holes_config = [
        (TOP_FRAME_HOLE_INNER, TOP_FRAME_HOLE_Z),
        (TOP_FRAME_HOLE_OUTER, TOP_FRAME_HOLE_Z),
    ]
    frame_sketch = create_frame_holes_sketch(body, pad, frame_holes_config, "FrameHolesSketch")

    frame_pocket = body.newObject("PartDesign::Pocket", "FrameHolesPocket")
    frame_pocket.Profile = frame_sketch
    frame_pocket.Type = "ThroughAll"

    # 4. Rail holes
    rail_holes_config = [
        (TOP_RAIL_HOLE_BOTTOM, RAIL_HOLE_OUTER_DIA),
        (TOP_RAIL_HOLE_CENTER, RAIL_HOLE_CENTER_DIA),
        (TOP_RAIL_HOLE_TOP, RAIL_HOLE_OUTER_DIA),
    ]
    rail_sketch = create_rail_holes_sketch(body, ext_pad, rail_holes_config, "RailHolesSketch")

    rail_pocket = body.newObject("PartDesign::Pocket", "RailHolesPocket")
    rail_pocket.Profile = rail_sketch
    rail_pocket.Type = "ThroughAll"

    doc.recompute()
    return body


def create_bottom_bracket_left(doc):
    """Create the bottom-left bracket with triangle hole pattern."""

    body = doc.addObject("PartDesign::Body", "BottomBracketLeftBody")

    # Similar to top bracket but with:
    # - Rail extension in -Z direction
    # - Triangle frame hole pattern (2 at top, apex at bottom)

    # 1. L-Profile base (same as top)
    lprofile = create_l_profile_sketch(body, "BottomLProfileSketch")

    pad = body.newObject("PartDesign::Pad", "BottomLProfilePad")
    pad.Profile = lprofile
    pad.Length = FRAME_LEG_WIDTH
    pad.Refine = True

    # 2. Rail extension in -Z direction
    ext_sketch = body.newObject("Sketcher::SketchObject", "BottomRailExtensionSketch")
    ext_sketch.MapMode = "FlatFace"

    ext_pad = body.newObject("PartDesign::Pad", "BottomRailExtensionPad")
    ext_pad.Profile = ext_sketch
    ext_pad.Length = BOTTOM_RAIL_EXTENSION - FRAME_LEG_WIDTH  # 55mm extension
    ext_pad.Reversed = True  # Extend in -Z direction
    ext_pad.Refine = True

    # 3. Frame holes (triangle pattern)
    frame_holes_config = [
        (BOTTOM_FRAME_HOLE_TOP_INNER, BOTTOM_FRAME_HOLE_TOP_Z),
        (BOTTOM_FRAME_HOLE_TOP_OUTER, BOTTOM_FRAME_HOLE_TOP_Z),
        (BOTTOM_FRAME_HOLE_APEX_X, BOTTOM_FRAME_HOLE_APEX_Z),
    ]
    frame_sketch = create_frame_holes_sketch(body, pad, frame_holes_config, "BottomFrameHolesSketch")

    frame_pocket = body.newObject("PartDesign::Pocket", "BottomFrameHolesPocket")
    frame_pocket.Profile = frame_sketch
    frame_pocket.Type = "ThroughAll"

    # 4. Rail holes (in -Z region)
    rail_holes_config = [
        (BOTTOM_RAIL_HOLE_TOP, RAIL_HOLE_OUTER_DIA),
        (BOTTOM_RAIL_HOLE_CENTER, RAIL_HOLE_CENTER_DIA),
        (BOTTOM_RAIL_HOLE_BOTTOM, RAIL_HOLE_OUTER_DIA),
    ]
    rail_sketch = create_rail_holes_sketch(body, ext_pad, rail_holes_config, "BottomRailHolesSketch")

    rail_pocket = body.newObject("PartDesign::Pocket", "BottomRailHolesPocket")
    rail_pocket.Profile = rail_sketch
    rail_pocket.Type = "ThroughAll"

    doc.recompute()
    return body


def mirror_bracket(doc, source_body, new_name):
    """Create a mirrored copy of a bracket body."""
    # Create mirror using Part::Mirroring
    mirror = doc.addObject("Part::Mirroring", new_name)
    mirror.Source = source_body
    mirror.Normal = FreeCAD.Vector(0, 1, 0)  # Mirror across XZ plane
    mirror.Base = FreeCAD.Vector(0, FRAME_LEG_WIDTH / 2, 0)  # Center of bracket
    doc.recompute()
    return mirror


def export_stl(shape, filepath, linear_deflection=0.1, angular_deflection=0.1):
    """Export a shape to STL file."""
    mesh = MeshPart.meshFromShape(
        shape,
        LinearDeflection=linear_deflection,
        AngularDeflection=angular_deflection
    )
    mesh.write(filepath)
    print(f"Exported: {filepath} ({len(mesh.Facets)} facets)")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def create_all_brackets(export_dir=None):
    """
    Create all four brackets and optionally export STL files.

    Args:
        export_dir: Directory for STL export. If None, no export.

    Returns:
        dict: Dictionary of created bracket objects
    """
    # Create new document
    doc = FreeCAD.newDocument("PrusaRackBrackets")

    # Create left brackets
    top_left = create_top_bracket_left(doc)
    bottom_left = create_bottom_bracket_left(doc)

    # Create right brackets (mirrored)
    top_right = mirror_bracket(doc, top_left, "TopBracketRight")
    bottom_right = mirror_bracket(doc, bottom_left, "BottomBracketRight")

    doc.recompute()

    # Export STLs if directory provided
    if export_dir:
        os.makedirs(export_dir, exist_ok=True)
        export_stl(top_left.Shape, os.path.join(export_dir, "top_bracket_left.stl"))
        export_stl(top_right.Shape, os.path.join(export_dir, "top_bracket_right.stl"))
        export_stl(bottom_left.Shape, os.path.join(export_dir, "bottom_bracket_left.stl"))
        export_stl(bottom_right.Shape, os.path.join(export_dir, "bottom_bracket_right.stl"))

    return {
        "document": doc,
        "top_left": top_left,
        "top_right": top_right,
        "bottom_left": bottom_left,
        "bottom_right": bottom_right,
    }


# =============================================================================
# SCRIPT EXECUTION
# =============================================================================

if __name__ == "__main__":
    # When run directly, create brackets and export to current directory
    result = create_all_brackets(export_dir="./stl_export")
    print(f"Created {len(result) - 1} brackets in document: {result['document'].Name}")
