# Printables Submission Package

## Model Title
**Prusa MK3S/MK4S Frame to 6U Rack Mount Brackets**

## Summary (for search/preview - max 150 chars)
3D-printable L-brackets to mount 6U rack rails to Prusa MK3S/MK4S frame using existing z-axis screw holes. No frame modifications needed.

---

## Description (copy/paste to Printables)

### Overview
Mount standard 6U (10.5") vertical rack rails to your Prusa MK3S/MK4S 3D printer frame! These brackets use the existing z-axis motor screw locations, requiring **no modifications** to your printer frame.

Perfect for repurposing your old Prusa frame after upgrading to a Core One, or for adding rack-mounted equipment next to your printer.

### Features
- **Non-destructive mounting** - Uses existing frame screw holes
- **Standard compatibility** - Fits any EIA-310 compliant 6U rack rails
- **Centered positioning** - Rails perfectly centered in the 275mm frame opening
- **Reinforced design** - Triangular angle braces at stress points
- **No supports needed** - Print flat on the bed

### What's Included
- 2x Top brackets (left/right mirror pair)
- 2x Bottom brackets (left/right mirror pair)
- FreeCAD source file for modifications
- Python script for parametric regeneration

### Compatibility
- **Frames:** Prusa MK3S, MK3S+, MK4S (and likely MK4)
- **Rails:** Any EIA-310 standard 6U vertical rack rails (10.5" / 266.7mm)

### Hardware Required
| Item | Quantity | Notes |
|------|----------|-------|
| M3 x 8mm screws | 10 | For frame mounting |
| M3 washers | 10 | Recommended |
| 12-24 screws | 8-16 | Standard rack screws for rail attachment |

### Assembly
1. Remove existing screws from Prusa frame z-axis motor mount locations
2. Position top brackets at upper frame corners
3. Position bottom brackets at lower frame corners
4. Secure brackets with M3 screws
5. Attach 6U rack rails using 12-24 rack screws
6. Verify alignment and tighten all fasteners

### Design Details
- **Top brackets:** 45mm × 40mm × 97mm, 2-hole linear mounting pattern
- **Bottom brackets:** 45mm × 40mm × 95mm, 3-hole triangle mounting pattern
- **Wall thickness:** 4mm throughout
- **Rail leg:** Matches 39mm rack rail L-angle depth

### Source Files
Full FreeCAD source and Python parametric script available on GitHub:
https://github.com/adbyrne/OfficeCAD

---

## Print Settings (for Printables form)

| Setting | Value |
|---------|-------|
| Printer | Prusa (any) |
| Rafts | No |
| Supports | No |
| Resolution | 0.2mm |
| Infill | 40-50% |
| Filament | PETG (recommended) or ABS |
| Perimeters | 3-4 |

### Notes for Print Settings Field
```
Material: PETG or ABS recommended (PLA not recommended for load-bearing)
Layer height: 0.2mm
Infill: 40-50%
Perimeters: 3-4
Top/Bottom layers: 4-5
Supports: None required
Orientation: Print with frame leg flat on bed
```

---

## Categories (select on Printables)
- Primary: **3D Printer Accessories** → **Prusa**
- Secondary: **Tools** → **Organization**

## Tags (enter on Printables)
```
prusa, mk3s, mk4s, rack mount, 6U, server rack, frame, bracket, L-bracket, EIA-310, organization, repurpose, upgrade
```

---

## Files to Upload

### STL Files (required)
- [ ] `stl/top_bracket_left_v3.stl`
- [ ] `stl/top_bracket_right_v3.stl`
- [ ] `stl/bottom_bracket_left_v3.stl`
- [ ] `stl/bottom_bracket_right_v3.stl`

### Source Files (optional but recommended)
- [ ] `freecad/BracketsV3.FCStd`
- [ ] `prusa_rack_brackets.py`

### Images to Upload (select 3-5)
Recommended order:
1. [ ] `images/all_brackets_constrained.png` - Main image showing all 4 brackets
2. [ ] `images/v1_all_brackets_final.png` - Alternative view
3. [ ] `images/top_bracket_left.png` - Detail of top bracket
4. [ ] `images/bottom_bracket_left.png` - Detail of bottom bracket
5. [ ] `images/prusa_frame.jpg` - Reference photo of frame (if useful)

**Note:** Photos of the printed/installed brackets would significantly improve the listing. Consider adding these after installation.

---

## License Selection
Select: **GNU General Public License v3.0 (GPL-3.0)**

---

## Upload Steps

1. Go to https://www.printables.com/model/new
2. Enter title and summary
3. Upload STL files (drag & drop)
4. Upload images (drag & drop, reorder as needed)
5. Paste description (supports markdown)
6. Fill in print settings
7. Select categories and enter tags
8. Select license (GPL-3.0)
9. Optionally upload source files
10. Click "Publish"

Estimated time: 10-15 minutes
