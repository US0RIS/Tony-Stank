# MAGNETIC_CIRCUIT — buildable-face magnetics through the full pivot (session 4)

## Method

**Code:**
- `sims/s4/magfd.py`: solver.
- `sims/s4/pivot_real.py`: pivot model. Outputs `results/s4_pivot_real_100.{md,json}`.
- `sims/s4/gap_sensitivity.py`, `sims/s4/demag_contacts.py`, `sims/s4/cycle_dynamics.py`, `sims/s4/verdict_numbers.py`: supporting analyses.

**Solver** (NUMERICAL SIMULATION): 2D finite-difference magnetostatics, scalar potential with permanent-magnetisation sources.
- Geometry: real rotating geometry, 4×4 supersampled rasterisation.
- Iron: linear NiFe pole pieces (μ_r = 1000).
- Bars: switchable CoP, Jr 0.65 T (SNIPPET), squareness 0.8 (ASSUMED; torque scales exactly as (Jr·sq)², so other values are rescaled).
- Clearances: 1 µm standoff clearance and 1 µm recess.
- Force and torque: Maxwell-stress tensor on a contour in the air gap around the mover.
- **Every neighbour state** (ON+, ON−, OFF for S and D) is evaluated at every angle, and the best is selected, which favours the design.

## Validation and error budget

| Check | Result | Class |
|---|---|---|
| Legacy session-3 geometry vs independent magnetic-charge model | 0.94–1.00 at 21°, 45°, 69° | NUMERICAL vs MATH |
| Mesh refinement (h = 1.0 → 0.6 µm) | < 1 % change | NUMERICAL |
| Independent review R2: energy-method solver, harmonic iron mixing | magfd **overstates** force by 1 % (grid-aligned) to 12.5 % (half-cell gap offset); pivot torque +2–4 % | NUMERICAL (independent) |
| Clearance/recess sensitivity (c = r = 0.5–2 µm) | attached clamp 2.83–1.26 µN; 45° torque 9.7–8.1×10⁻¹² N·m | NUMERICAL |
| Interior pole-piece flux density | 0.33–0.65 T, below NiFe B_sat 0.8–1.0 T. R2: still rises with mesh refinement at corners, so local saturation cannot be excluded. | NUMERICAL |

## Limitations (bounded)

- **2D model.** Results are per metre of depth × the 41 µm pole-piece depth, with bar flux smeared over that depth (f_b = 0.6). Finite 3D fringing reduces force further. This is bounded by the ×0.5–1.0 derate used in `verdict_numbers.py`.
- **Linear materials.** The demagnetisation check is post hoc: reverse H is computed but M is not updated. Saturation is not modelled.
- **No nonlinear 3D FEM solver was available** in this environment; none was installed or validated.

## Results at L = 100 µm (2D × pole depth, CoP, squareness 0.8)

| Quantity | Session-3 claim | Session-4 integrated model |
|---|---|---|
| Attached clamp per face | ~98 kPa (~1 mN) | **2.0 µN (0.20 kPa)** |
| 90° pivot worst margin vs humid peel | 4.5 | **0.022** (at 39°) |
| 180° pivot worst margin | 2.0 | **0.006** (at 95°) |
| Start torque / peel torque | — | 0.060 (90°), 0.052 (180°) |
| Dead zones (negative best torque) | — | none |
| Reverse H in magnets | not modelled | interior max 40–45 kA/m vs Hc 28 kA/m. In the strongest-clamp state, 7 % of magnet volume is above Hc (median 68 % of Hc); at mid-pivot 1 %. |

**Torque profile shape:** torque is highest near contact (θ ≈ 0 or 90° for the 90° pivot) and falls 2.5–6× at mid-swing. This is the two-pole-face decay predicted independently by R4 (length scale ≈ pole spacing/π ≈ 21 µm).

## Why the forces collapsed: flux starvation (MATHEMATICAL)

- The flux a face can deliver is limited by the switchable bar cross-section: Φ ≈ Jr·sq·(bar area).
- That flux reaches the neighbour only through the pole-piece faces, which cover 6.6 % of the face area.
- So B at the pole is ≤ Jr·sq·A_bar/A_pole ≈ 0.15–0.19 T. The pressure is ≈ 10–14 kPa over 6.6 % of the face, at most ~9 µN with zero gap (R4). The FD result with real gaps and leakage is 2 µN.
- Session 3's 98 kPa came from a 1 T face-normal sheet covering 80 % of the face. That geometry cannot be built with a switchable material (NEPL_FEASIBILITY.md items 1–3).

## Scaling to larger modules (exact similarity, MATHEMATICAL)

For geometrically similar designs with fixed materials, torque ∝ L³ while the adhesion peel torque ∝ L, so the margin ∝ L². Bar thickness at 1 mm (40 µm) stays within demonstrated film thickness.

| L | start margin, humid | start margin, dry 10× lower adhesion (ASSUMED) |
|---|---|---|
| 100 µm | 0.05–0.06 | 0.5–0.6 |
| 300 µm | 0.47–0.54 | 4.7–5.4 |
| 1 mm | 5.2–6.0 | 52–60 |

Multiply by the 3D derate of 0.5–1.0, which is bounded but not computed.
