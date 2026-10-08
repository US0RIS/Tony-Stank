# INTEGRATED_MODULE_DESIGN — dimensioned NEPL module (session 4)

## Sources
- Code: `sims/s4/module_geometry.py` (axis-aligned box CAD, interference checker, volume budget, drawings).
- Outputs:
  - `results/s4_geometry_{100,300,1000}.md`
  - `results/s4_cad/nepl_*um.json`: every component as a box, with material.
  - `results/s4_cad/nepl_*um_{XZ_ymid,XZ_y0.35L,XY_z6,exploded}.png`

All dimensions follow from an explicit, asserted stack. They are not free parameters. Evidence class: ENGINEERING DESIGN + NUMERICAL interference check.

## Layout at L = 100 µm (dimensions in µm)

**Edges and corners.**
- 12 edge zones of 10 × 10 µm cross-section carry the hinge knuckles. They are reserved, but no workable hinge design was found (MECHANICAL_CYCLE.md).
- 8 corner blocks of 12 µm.

**Face window.** Each face's active window is 74 × 74 µm, with a 13 µm margin from every edge. The face skin is 12 µm deep; the 1 µm gap left before the margin is the clearance to the orthogonal skins.

**Per-face stack, across the window (v):**

| Band | v position (µm) |
|---|---|
| Pin band | 13.5–27.5 |
| Coil envelope 0 | 28.5–48.5 |
| Coil envelope 1 | 49.5–69.5 |
| Socket band | 70.5–86.5 |

All bands are separated by 1 µm clearances.

**Per-face EPM:**

| Component | Size / position | Material |
|---|---|---|
| Switchable bars (2) | 58 × 12 × 4 µm, at depth 5–9 µm | CoP |
| Solenoid per bar | 54 µm long, 4 µm winding envelope on every side | Cu + insulation |
| Pole pieces (2) | 8 × 41 × 12 µm, reaching to 1 µm below the face | NiFe |

**Other face features:**

| Feature | Size | Material / note |
|---|---|---|
| Pin | base 14 µm, tip 6 µm, protruding 8 µm | Si |
| Socket | 16 × 16 × 9 µm | — |
| Contact pads (4) | 8 × 8 µm | Ti/Au |
| Via bundle | 6 × 2.5 µm | to the core |

**Core** (14–86 µm in each axis):
- two thinned CMOS dies, 72 × 72 × 7 µm;
- deep-trench capacitor, 72 × 72 × 27 µm;
- TSV/redistribution layer.

**Interference check:** 108 components, **0 undeclared overlaps**. The declared integrations are: bar inside its own coil envelope; cover patterned around the pin, socket and pads.

The first-pass layout had 54 flagged overlaps: **18 real** (socket × coil and via × bar/coil, three on each face) and 36 intended cover openings. Fixing them forced the explicit band stack, which **fixed the bar width at 12 µm**. A 90°-symmetric (chiral 4+4) pin pattern, which identical modules need in order to mate in arbitrary orientations (`pins.py`), further **reduces the bars to 9.5 µm**.

### Volume budget (100 µm)

| Component | Fraction of L³ |
|---|---|
| Coils | 15.6 % |
| Routing | 14.9 % |
| Trench capacitor | 14.8 % |
| Hinge zones | 9.1 % |
| CMOS | 7.7 % |
| Pole pieces | 4.7 % |
| **Switchable magnet** | **3.3 %** (5,568 µm³ per face) |
| Insulation, pins, sockets, structure, pads | ~6 % |

The switchable magnet is a small fraction because coils, pole pieces, pins/sockets and clearances must share the 12 µm skin.

## Electronics that must fit

- **Drivers:** 12 coil select switches + H-bridge, sized for the pulse current (`switching.py`).
  - 3 µm coil pitch: needs 31,000 µm² of silicon against 10,952 µm² available (two die layers). **Does not fit.**
  - 1.5 µm pitch: 6,500 µm². Fits, at 2× the energy per switch.
- **Local energy storage for a pulse:** needs 35–1100 module volumes of trench capacitor. **Impossible.** Pulses must come through the contacts (SWITCHING_AND_THERMALS.md).
- **Centralised drivers** (in neighbours or the pocket controller) do not remove the per-coil select switch rated for the full pulse current: each coil must still be individually selected.

## Larger scales

The same stack scales self-similarly:
- **300 µm:** bars 36 × 12 × 174 µm; 3 µm clearances.
- **1 mm:** bars 120 × 40 × 580 µm. 40 µm is within demonstrated plated/sputtered film thickness (≤ 50–100 µm).

There are 0 interferences at both scales. Driver area is no longer constraining at 300 µm or above (7,000 µm² needed vs 98,600 µm² available).
