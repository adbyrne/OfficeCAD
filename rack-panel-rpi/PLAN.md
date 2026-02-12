# 10-Inch Rack Panel for Raspberry Pi Boxes

## Project Overview

Design a 1U 10-inch rack panel to hold two Raspberry Pi enclosures, printable on a Prusa Core One (250mm × 210mm bed) using multi-part assembly.

---

## Specifications

### Rack Dimensions (10-inch / EIA-310)

| Dimension | Value | Notes |
|-----------|-------|-------|
| Rail hole-to-hole (horizontal) | 252mm | Mounting screw centers |
| Rail outer edge-to-edge | 267mm | Total panel width with flanges |
| 1U height | 44.45mm (1.75") | Standard rack unit |
| Mounting hole pattern | EIA-310 3-hole | 6.3mm center (slotted), 4.6mm outer, 16mm spacing |

### Raspberry Pi Box Dimensions

**Product:** SPROG DCC 3D-printed enclosures ([sprog-dcc.co.uk](https://www.sprog-dcc.co.uk/accessories/enclosures))
- Pi-SPROG 3 Case - R-Pi 4
- Pi-SPROG 3 Plus Case - R-Pi 4

*Note: Official dimensions not published. Measurements taken from physical units.*

| Dimension | Value | Notes |
|-----------|-------|-------|
| Height | 37mm | Fits within 1U (44.45mm) with 7.45mm clearance |
| Width | 62mm | Two boxes = 124mm total |
| Total depth | 93mm | Full box depth (extends behind panel) |
| **Front clearance** | **32mm** | Required depth for side connector access |

### Box Detail Measurements

```
TOP VIEW (box):
                    ← 93mm total depth →
    ┌─────────────────────────────────────┐
    │                                     │
    │  vent (14.8mm from side)            │  ← 62mm wide
    │                                     │
    └─────────────────────────────────────┘
       ↑
    12.3mm to vent

SIDE VIEW (box):
                    ← 93mm total depth →
    ┌─────────────────────────────────────┐
    │  side vent    │ connector opening   │
    │  ┌───┐        │      at 32mm        │  ← 37mm high
    │  │   │ 10.4mm │                     │
    └──┴───┴────────┴─────────────────────┘
       ↑   ↑
    9.7mm  2.9mm from bottom
    from front

FRONT VIEW (box face at panel):
    ┌─────────────────────────────────────┐
    │         vent (5.8mm from top)       │
    │                                     │  ← 37mm high
    │    connector (4.3mm from side)      │
    └─────────────────────────────────────┘
              ↑
           6mm from bottom
              ← 62mm wide →
```

| Feature | Measurement | Notes |
|---------|-------------|-------|
| **Bottom** | | |
| Front to vent | 7.2mm | |
| Side to vent | 15mm | |
| **Top** | | |
| Front to vent | 12.3mm | |
| Side to vent | 14.8mm | |
| **Front face** | | |
| Bottom to connector | 6mm | |
| Side to connector | 4.3mm | |
| Top to vent | 5.8mm | |
| **Side** | | |
| Front to connector | 32mm | **Key clearance depth** |
| Side vent from front | 9.7mm | Small vent opening |
| Side vent from bottom | 2.9mm | |
| Side vent height | 10.4mm | |
| Side vent depth | 12.2mm | |

### Print Bed Constraints

| Constraint | Value | Impact |
|------------|-------|--------|
| Bed X (width) | 250mm | Panel 252-267mm exceeds this |
| Bed Y (depth) | 210mm | Panel depth should fit |
| **Conclusion** | Multi-part required | Cannot print full width in one piece |

---

## Design Challenges

### 1. Panel Width Exceeds Print Bed
- **Problem:** 252mm hole-to-hole > 250mm bed width
- **Solutions:**
  - A) Two-piece split down the middle (~126mm each)
  - B) Three-piece: end flanges + center panel
  - C) Angled print orientation (limited benefit)

### 2. Assembly Rigidity
- **Problem:** Multi-part panel must be rigid when assembled
- **Solutions:**
  - Screw joints with alignment features
  - Dovetail/tongue-and-groove interlocks
  - Backing plate or reinforcement bar

### 3. Pi Box Mounting
- **Problem:** Secure mounting with tolerance for insertion/removal
- **Solutions:**
  - Shelf + top retention clips
  - Slide-in channels
  - Snap-fit with flexures

---

## Design Options

### Option A: Two-Piece Center Split

```
┌─────────────────────┬─────────────────────┐
│  LEFT HALF          │         RIGHT HALF  │
│  ○         [PI BOX] │ [PI BOX]         ○  │
│  ○    ───┐    ┌───  │  ───┐    ┌───    ○  │
│  ○       └────┘     │     └────┘       ○  │
└─────────────────────┴─────────────────────┘
         ~126mm              ~126mm
```

**Pros:**
- Simpler design (2 parts)
- Symmetric, can mirror in CAD
- Each Pi box contained in one piece

**Cons:**
- Joint runs through visible center
- Alignment critical for clean appearance
- Each half still ~126mm + flange

### Option B: Three-Piece (End Tabs + Center Panel)

```
┌────┬────────────────────────────────┬────┐
│RAIL│                                │RAIL│
│TAB │  [PI BOX]           [PI BOX]   │TAB │
│ ○  │  ───────────────────────────   │ ○  │
│ ○  │                                │ ○  │
│ ○  │                                │ ○  │
└────┴────────────────────────────────┴────┘
~20mm          ~212-220mm            ~20mm
```

**Pros:**
- Center panel fully printable (~220mm < 250mm)
- Rail interface isolated to end tabs
- Joints hidden behind rack rails
- End tabs can be smaller/stronger

**Cons:**
- More parts (3 vs 2)
- More assembly hardware
- Center panel has no direct rail attachment

### Option C: Hybrid - Split Center + End Tabs

```
┌────┬───────────────┬───────────────┬────┐
│RAIL│  CENTER LEFT  │ CENTER RIGHT  │RAIL│
│TAB │   [PI BOX]    │   [PI BOX]    │TAB │
└────┴───────────────┴───────────────┴────┘
```

**Pros:**
- Maximum flexibility in print orientation
- Redundant joint strength
- Each center piece ~100-110mm

**Cons:**
- Most complex (4 parts)
- Most assembly hardware

---

## Selected Approach: Option B (Three-Piece) ✓

### Rationale
1. **Cleanest aesthetics** - joints hidden by rails
2. **Strongest rail interface** - dedicated end tabs
3. **Optimal print orientation** - center panel flat, end tabs upright
4. **Modularity** - center panels interchangeable for different uses

### Confirmed Decisions
- **Hardware:** M3 screws and nuts (from Prusa upgrade supply)
- **Pi retention:** Screw-attached top clips (printed flexures)
- **Future-proofing:** Top clip design allows different box heights

### Part Breakdown

#### Part 1 & 2: Rail End Tabs (×2, mirrored)
- **Dimensions:** ~20mm wide × 44.45mm tall × panel depth
- **Features:**
  - EIA-310 3-hole pattern (1U)
  - Screw holes for center panel attachment
  - Alignment pins/features
- **Print orientation:** Upright (holes horizontal)

#### Part 3: Center Panel
- **Dimensions:** ~212-220mm wide × 44.45mm tall × panel depth
- **Features:**
  - Two Pi box mounting positions (shelves + top clips)
  - Screw holes for end tab attachment
  - Optional ventilation cutouts
- **Print orientation:** Flat (face down)

---

## Pi Box Mounting Design

### Selected: Shelf + Screw-Attached Top Clips ✓

```
SIDE VIEW:                      FRONT VIEW:

    ┌───────┐  ← Top clip       ══╤═══════════╤══  ← Top clip bar
    │ ┌───┐ │    (screw-          │  [PI BOX] │
    │ │ PI│ │     attached)       │           │
    │ │BOX│ │                     ╧═══════════╧  ← Shelf lip
    │ └───┘ │                   ════════════════  ← Panel base
    ═════════  ← Shelf
```

---

## Structural Improvements

### 1. Border Lip (Perimeter Flange)

A raised lip around the panel edge significantly increases rigidity by acting as a beam flange.

```
CROSS SECTION (side view):

With lip (stiff):          Without lip (flexible):
    ┌─┐         ┌─┐
    │ └─────────┘ │            ───────────────
    └─────────────┘              (flat plate)
```

**Recommendations:**
| Option | Lip Height | Location | Benefit |
|--------|------------|----------|---------|
| A | 3-4mm | Front only | Clean look, hides box edges |
| B | 3-4mm | Front + back | Maximum rigidity, cable tray effect |
| C | 3-4mm | Top + bottom only | Rigidity without depth increase |
| **D (suggested)** | 3-4mm | Full perimeter, front side | Tray-like, professional appearance |

**Note:** Back lip could double as cable retention/guide.

### 2. Fillets on Inside Corners

Inside corners are stress concentrators. Fillets distribute load and improve print quality.

```
WITHOUT FILLET:              WITH FILLET:

    │                            │
    │                            │
    └────                        ╰────
    Sharp corner               Radiused corner
    (stress point)             (load distributed)
```

**Recommendations:**
| Location | Radius | Reason |
|----------|--------|--------|
| Shelf to panel junction | 2-3mm | High stress from box weight |
| Lip to panel junction | 1-2mm | Prevents layer separation |
| Nut trap corners | 0.5-1mm | Print quality, nut insertion |
| Top clip flexures | 1-2mm | Fatigue resistance |

**Print benefits:**
- Sharp inside corners can cause layer adhesion issues
- Fillets print more reliably with fewer artifacts
- FreeCAD PartDesign `Fillet` tool handles this well

### 3. Combined Approach (Recommended)

```
CROSS SECTION with both features:

        ╭─╮                     ╭─╮
        │ ╰───── shelf ─────────╯ │  ← 2mm fillet at shelf junction
        │    ╭───────────╮        │
        │    │  PI BOX   │        │
    ╭───╯    ╰───────────╯        ╰───╮
    │          panel base              │  ← 3mm front lip
    ╰──────────────────────────────────╯  ← 1mm fillet at lip junction
```

---

### Design Benefits
- **Adjustable height:** Different top clips for different box heights
- **Replaceable:** Broken clip = print new one, not whole panel
- **Tool-free swap:** Loosen screws, swap box, retighten
- **Future-proof:** Same panel works with 37mm, 45mm, or other heights

### Design Constraint: Front Connector Access
The box has a connector opening **6mm from the bottom** on the front face. The shelf must not block this:
- **Option A:** Thin shelf lip (< 5mm tall at front)
- **Option B:** Shelf with front cutout for connector area
- **Option C:** Shelf only at rear/sides, box overhangs front

### Top Clip Design Concept
- Printed flexure/bar spanning box width
- M3 screw attachment points on each side
- Slight downward pressure to hold box on shelf
- Vertical slots in panel allow height adjustment

### Tolerances
| Feature | Nominal | Tolerance | Actual |
|---------|---------|-----------|--------|
| Shelf width | 62mm | +1mm | 63mm opening |
| Shelf height (current box) | 37mm | +1-2mm | 38-39mm clearance |
| **Depth (connector access)** | **32mm** | +2mm | **34mm clearance** |
| Top clip screw slots | - | 5-10mm travel | Adjustable height |

---

## Assembly Hardware

### Confirmed: M3 Hardware from Prusa Supply

Using M3 screws and nuts from Prusa MK4S/MK3S upgrade parts.

### Estimated Bill of Materials
| Item | Quantity | Purpose |
|------|----------|---------|
| M3 × 8-10mm screws | 8-12 | End tab to center panel joints |
| M3 nuts | 8-12 | Captive in nut traps |
| M3 × 6-8mm screws | 4-8 | Top clip attachment |
| M3 nuts | 4-8 | Top clip nut traps |
| 12-24 × 1/2" screws | 4-6 | Rail mounting (rack standard) |

### Joint Design: Nut Traps ✓
- Clearance hole (3.2mm) in one part
- Captive nut trap (5.5mm hex) in mating part
- Simple, strong, reusable - matches Prusa hardware

---

## Print Settings (Confirmed)

| Setting | Value | Notes |
|---------|-------|-------|
| **Material** | PETG | Strong, heat resistant, from bracket project |
| **Orientation** | Face down | Largest area on bed, lip prints vertically |
| Layer height | 0.2mm | Standard quality |
| Infill | 20-30% | Sufficient for panel rigidity |
| Perimeters | 3-4 | Good wall strength |
| Supports | Likely needed | For shelf overhang, nut traps |

### Orientation Benefits (Face Down)
- **Lip strength:** Layers run vertically through lip height - strong in bending
- **Surface quality:** Visible front face against build plate = smooth finish
- **Shelf overhang:** May need supports depending on angle
- **Nut traps:** Print with bridging or need support

---

## Open Questions

### Deferred to CAD Phase (visual review needed)
These questions will be resolved after initial CAD model review:

| Question | Options | Notes |
|----------|---------|-------|
| Ventilation cutouts | Yes/No, pattern TBD | Between/around Pi boxes |
| Cable routing | Rear cutouts for USB/power/HDMI | Size and position TBD |
| Back lip | Yes/No | Cable retention benefit |
| Front connector clearance | Thin lip / cutout / rear-only shelf | 6mm constraint from box bottom |
| Alignment features | Pins, tongues, or screws only | Between end tabs and center |
| Lip thickness | 4mm (same as base) or thinner | Structural vs weight |

### Resolved Questions

| # | Question | Decision |
|---|----------|----------|
| 1 | Panel depth | ~35-40mm (32mm clearance + margin) |
| 2 | Front bezel/lip | Yes, 3-4mm perimeter lip (front side) |
| 3 | Labeling | None |
| 4 | Hardware | Nut traps with M3 screws/nuts (Prusa supply) |
| 5 | Top clip design | Separate screw-attached clips (height adjustable) |
| 6 | Fillets | Yes, 1-3mm radius depending on location |
| 7 | Panel base thickness | 4mm |
| 8 | Material | PETG |
| 9 | Print orientation | Face down (largest area on bed) |

---

## Next Steps

### Phase 1: Requirements Refinement ✓ COMPLETE
- [x] Measure actual Pi enclosures for exact dimensions
- [x] Decide panel depth → **~35-40mm**
- [x] Confirm mounting style → **Shelf + screw-attached top clips**
- [x] Confirm material and print orientation → **PETG, face down**
- [x] Confirm structural approach → **4mm base, perimeter lip, fillets**

### Phase 2: CAD Implementation (NEXT SESSION)
- [ ] Create FreeCAD document with PartDesign bodies
- [ ] Model center panel (basic shape with shelf positions)
- [ ] Model end tab (one side)
- [ ] **Visual review** - resolve deferred questions (vents, cable routing, lip details)
- [ ] Add Pi box mounting features (shelves, clip attachment points)
- [ ] Design inter-part joints (nut traps, alignment)
- [ ] Mirror end tab for opposite side
- [ ] Design top clips (separate parts)

### Phase 3: Validation
- [ ] Export STL files
- [ ] Test fit in PrusaSlicer (check bed fit, supports needed)
- [ ] Print test pieces for joint fit
- [ ] Iterate on tolerances

### Phase 4: Production
- [ ] Final prints
- [ ] Assembly
- [ ] Document final design

---

## Reference Links

- Previous project: `/home/abyrne/Projects/Office/cad/prusa-rack-conversion/`
- MCP reference: `/home/abyrne/Projects/GENERATED_MCP_REFERENCE.md`
- Reference models: `/home/abyrne/Projects/Office/cad/reference_models/` (includes Pi holders)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-02-06 | Initial plan created |
| 0.2 | 2026-02-06 | Confirmed Option B, M3 hardware, PETG, structural improvements, detailed box measurements |
| 0.3 | 2026-02-06 | Finalized Phase 1 requirements, 4mm base, no labeling, deferred visual questions to CAD phase |
| 0.4 | 2026-02-06 | Added SPROG DCC product reference; official specs not available online |
