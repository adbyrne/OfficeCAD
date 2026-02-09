# Blank 1U 10-Inch Rack Panel Template

A reusable blank panel template for 10-inch rack projects. Three-piece assembly (center panel + 2 end tabs) designed for printing on a Prusa Core One.

![Blank Panel](images/blank_panel_iso.png)

## Assembly Overview

| Part | Dimensions | Description |
|------|-----------|-------------|
| Center Panel | 216 x 44.45 x 18mm | Solid face plate with U-channel walls, no cutouts |
| End Tab (x2) | 27 x 44.45 x 18mm | L-shaped with gussets, EIA-310 3-hole rail mounting |

**Assembled width:** 270mm (252mm hole-to-hole, EIA-310 standard)

## Key Specs

- **Rack standard:** EIA-310, 10-inch, 1U
- **Face plate:** 4mm thick
- **Walls:** 14mm deep (top, bottom, left side, right side)
- **Wall thickness:** 4mm
- **Tab connection:** M3 x 10mm socket head cap screws through side flanges
- **Rail mounting:** 3-hole pattern (6.3mm center, 4.6mm outer)
- **Inside fillets:** 2mm radius at wall-to-faceplate junctions

## How to Use as Template

1. Copy `freecad_files/BlankPanel.FCStd` to your new project
2. Open in FreeCAD and add your custom cutouts/features to the CenterPanelBody
3. Sketches should be placed on the face plate front face (Z=0) or rear face (Z=4)
4. Export STLs for printing

### Coordinate System
- **X:** Panel width (0 to 216mm)
- **Y:** Panel height (0=bottom, 44.45=top)
- **Z:** Depth (0=face plate front, positive=into rack)

### Interior Usable Area
- **X:** 4mm to 212mm (between side walls)
- **Y:** 4mm to 40.45mm (between top/bottom walls)
- **Face plate cutout area:** Full 216 x 44.45mm face

## Hardware

- 4x M3 x 10mm socket head cap screws (tab-to-panel joints)
- 4x M3 hex nuts (in panel side wall recesses)
- 6x rack mounting screws (through EIA-310 holes)

## Print Settings

- **Material:** PETG
- **Orientation:** Face down (largest area on bed)
- **Printer:** Prusa Core One (250 x 210mm bed)

## Files

```
freecad_files/
  BlankPanel.FCStd      # FreeCAD source (all 3 parts)
printed_files/
  BlankCenterPanel.stl   # Center panel (no cutouts)
  LeftTab.stl            # Left end tab
  RightTab.stl           # Right end tab
images/
  blank_panel_iso.png    # Isometric view
```

## Projects Using This Template

- [rack-panel-rpi](../rack-panel-rpi/) - SPROG DCC Raspberry Pi enclosure panel
