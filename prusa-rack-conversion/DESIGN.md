# Prusa Frame to 6U Rack Mount Brackets - Design Document

## Overview

This project provides 3D-printable L-brackets to mount standard 6U vertical rack rails to a Prusa MK3S/MK4S 3D printer frame. The brackets utilize the existing z-axis motor screw locations on the frame corners, requiring no modifications to the printer frame.

## Design Goals

1. **Non-destructive mounting** - Use existing frame screw holes
2. **Standard rack compatibility** - Support EIA-310 6U (10.5") rack rails
3. **Centered rail positioning** - Rails centered in the available frame opening
4. **Structural integrity** - Reinforced corners for load-bearing capacity
5. **Print-friendly geometry** - No supports required, flat surfaces for bed adhesion

## Frame Measurements

### Prusa MK3S/MK4S Frame

| ID | Value | Description |
|----|-------|-------------|
| T1 | 20mm | Top corner hole spacing (horizontal) |
| T2 | 9.8mm | Top corner edge to outer hole |
| T3 | 9.8mm | Top edge to holes |
| B1 | 20mm | Bottom corner upper holes spacing |
| B2 | 20mm | Triangle height (upper to apex) |
| B3 | 9.8mm | Bottom corner edge to outer hole |
| B4 | 22.5mm | Bottom edge to apex hole |
| V1 | 320mm | Vertical span (top to bottom holes) |

### Available Mounting Space

- Top bracket overhang above frame: 5mm
- Frame width at mounting point: 40mm
- Angle cut to open space: 5mm each end
- **Usable open space: 275mm**

## 6U Rack Rail Specifications

- **Standard:** EIA-310-D
- **Rail height:** 266.7mm (10.5 inches / 6 rack units)
- **L-angle depth:** 39mm
- **L-angle width:** 16mm
- **Mounting slot width:** ~7mm

### Rail Centering Calculation

```
Open space:     275.0mm
Rail height:    266.7mm
Gap each end:   (275.0 - 266.7) / 2 = 4.15mm
```

## Bracket Specifications

### Common Dimensions

| Parameter | Value | Notes |
|-----------|-------|-------|
| Frame leg depth | 45mm | Into the frame cavity |
| Frame leg width | 40mm | Bracket base width |
| Material thickness | 4mm | Wall thickness throughout |
| Rail leg height | 39mm | Matches rail L-angle depth |
| Angle brace | 10mm x 10mm | Triangular reinforcement at inside corner |

### Top Bracket (Left/Right Mirror Pair)

- **Overall dimensions:** 45mm x 40mm x 97mm
- **Rail leg extension:** 97mm total (extends upward into frame)
- **Frame mounting:** 2x M3 holes
  - Spacing: 20mm horizontal
  - Distance from inside edge: 17.5mm and 37.5mm
  - Z-position: 10mm from base
- **Rail mounting:** 3-hole EIA-310 pattern
  - Hole positions (Z): 54mm, 70mm, 86mm
  - Center hole: 6.3mm diameter (slotted clearance)
  - Outer holes: 4.6mm diameter
  - Spacing: 16mm between holes
  - Y-position: 19.5mm (centered on rail leg)

### Bottom Bracket (Left/Right Mirror Pair)

- **Overall dimensions:** 45mm x 40mm x 95mm
- **Rail leg extension:** 95mm total (extends downward into frame)
- **Frame mounting:** 3x M3 holes (triangle pattern)
  - Top holes: 17.5mm and 37.5mm from inside edge, Z=10mm
  - Apex hole: 27.5mm from inside edge, Z=30mm
  - Pattern: 2 holes at top, apex pointing toward bottom edge
- **Rail mounting:** 3-hole EIA-310 pattern
  - Hole positions (Z): -11.5mm, -27.5mm, -43.5mm
  - Center hole: 6.3mm diameter
  - Outer holes: 4.6mm diameter
  - Y-position: 19.5mm (centered on rail leg)

## L-Profile Geometry

The bracket cross-section is an L-shape with an integrated triangular angle brace:

```
                    (4, 39)
                      |
    Rail Leg          |
    (4mm thick)       |
                      |
(-10, 0)_____(0, 10)  |
        \     |       |
         \    |       |
  Frame   \   |       |
  Leg      \__|_______|
(-45, 0)     (0, 0)  (4, 0)
    |                  |
    |__________________|
(-45, -4)            (4, -4)

    Frame Leg: 45mm deep, 4mm thick
    Rail Leg:  39mm tall, 4mm thick
    Angle Brace: 10mm x 10mm triangle
```

### Profile Vertices (Counterclockwise)

1. (-45, -4) - Bottom-left corner
2. (-45, 0) - Top-left of frame leg
3. (-10, 0) - Start of angle brace
4. (0, 10) - End of angle brace
5. (0, 39) - Top of rail leg (inner)
6. (4, 39) - Top of rail leg (outer)
7. (4, 0) - Junction point
8. (4, -4) - Bottom-right corner

## Hole Patterns

### Frame Holes (M3 Clearance)

**Top Bracket (2-hole linear pattern):**
```
    Inside Edge (X=0)
         |
    [O]  |  17.5mm from edge
         |
    [O]  |  37.5mm from edge
         |
    Outside Edge (X=-45)

    Both holes at Z=10mm
    Diameter: 3.2mm
```

**Bottom Bracket (3-hole triangle pattern):**
```
    Inside Edge (X=0)
         |
    [O]  |  17.5mm    Z=10mm
         |
    [O]  |  37.5mm    Z=10mm
         |
      [O]|  27.5mm    Z=30mm (apex)
         |
    Outside Edge (X=-45)

    Diameter: 3.2mm
```

### Rail Holes (EIA-310 Pattern)

```
    Top Bracket:           Bottom Bracket:

    [o] 4.6mm  Z=86mm      [o] 4.6mm  Z=-11.5mm
         |                      |
    [O] 6.3mm  Z=70mm      [O] 6.3mm  Z=-27.5mm
         |                      |
    [o] 4.6mm  Z=54mm      [o] 4.6mm  Z=-43.5mm

    All holes at Y=19.5mm (centered on 39mm rail leg)
    Spacing: 16mm between holes
```

## Hardware Requirements

| Item | Quantity | Specification |
|------|----------|---------------|
| M3 x 8mm screws | 10 | For frame mounting |
| M3 washers | 10 | Recommended |
| 12-24 screws | 8-16 | For rail attachment (rack standard) |

## Print Settings

### Recommended Settings

| Parameter | Value |
|-----------|-------|
| Material | PETG or ABS |
| Layer height | 0.2mm |
| Infill | 40-50% |
| Perimeters | 3-4 |
| Top/Bottom layers | 4-5 |
| Supports | None required |

### Print Orientation

- **Top brackets:** Rail leg pointing UP (+Z)
- **Bottom brackets:** Rail leg pointing DOWN (-Z)
- Both orientations allow flat frame leg on print bed

### Material Notes

- **PETG:** Good balance of strength and ease of printing
- **ABS:** Higher heat resistance, better for warm environments
- **PLA:** Not recommended for load-bearing applications

## Assembly

1. Remove the existing screws from the Prusa frame z-axis motor mounts
2. Position top brackets at upper frame corners
3. Position bottom brackets at lower frame corners
4. Secure brackets with M3 screws through frame holes
5. Attach 6U rack rails to bracket rail legs using 12-24 screws
6. Verify rail alignment and tighten all fasteners

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-27 | Initial design, basic L-brackets |
| 1.1 | 2026-01-30 | Fixed bottom bracket rail leg depth |
| 2.0 | 2026-01-30 | Extended rail legs for 6U centering |
| 3.0 | 2026-01-31 | Added angle braces, fixed frame leg depth, rotated bottom hole pattern |
| 3.1 | 2026-02-02 | Aligned top bracket holes with bottom bracket (17.5mm from inside edge) |

## Files

| File | Description |
|------|-------------|
| `BracketsV3.FCStd` | FreeCAD source file (PartDesign workflow) |
| `prusa_rack_brackets.py` | Python script to recreate design |
| `top_bracket_left_v3.stl` | Top-left bracket for printing |
| `top_bracket_right_v3.stl` | Top-right bracket for printing |
| `bottom_bracket_left_v3.stl` | Bottom-left bracket for printing |
| `bottom_bracket_right_v3.stl` | Bottom-right bracket for printing |

## License

This design is released under the GNU General Public License v3.0.
