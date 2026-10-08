# RESULTS — analytical and computational findings

## Reproduce

```bash
pip install -r requirements.txt          # numpy, scipy, pytest
python3 -m pytest -q tests                # 6 regression/independent-check tests
for s in scaling face_motor power_network structure isl budget; do python3 sims/$s.py; done
# full outputs are written to results/*.md
```

Runtime is about 15 s in total. The models are deterministic; the S6 random test uses seed = 1.

> **Session 2:** S2, S3 and S7 below are partly superseded by [AUDIT.md](AUDIT.md). Audit scripts are in `sims/audit/`, outputs in `results/audit_*.md`, and Track B requirements in `results/track_b.md`. The test suite now has 9 tests.
>
> Retracted or revised:
> - S2: ~7 kPa → 5.7 kPa; open-air particle sensitivity added.
> - S3: "height-only" is valid only for the ideal case.
> - S7: 4 nJ per step → 15–40 nJ. "60 s per 10 cm rod" → ~150 s with a thick-slab feed.

## S1 — Force scaling (`results/scaling_table.md`, DERIVED)

- **Below 1 mm, interface forces dominate.** A 10 V thin-film electrostatic clamp exceeds weight by 8.6×10⁵ at 100 µm. Capillary force exceeds weight by 2×10³.
- **EPM switching current density scales as 1/L:** 5.3×10⁸ A/m² at 10 mm, 5.3×10¹⁰ at 100 µm. **EPMs are excluded below ~1 mm.**

## S2 — Electrostatic face motor (`results/face_motor.md`, DERIVED + SIMULATED)

- **Formulas validated.** The analytic τ(s) and p(s) match an independent finite-difference Laplace solution to within **1.4 %** over 5 phase points.
- **Optimum pitch** λ = 3.281 g. τ_max = 1.105·ε₀V²/(2g²) (12.1 kPa at 50 V/µm). Discrete 3-phase stripes give 0.57–0.60 of the ideal.
- **Near-zero net normal force** is achievable while keeping ~7 kPa shear.
- **Sliding margin** (thrust / resistance) with humid capillary adhesion on 9 bumps and μ = 0.4:

  | L | 1 mm | 100 µm | 30 µm | 10 µm |
  |---|---|---|---|---|
  | Margin | 360 | 25 | 2.3 | 0.3 |

  The size floor is **L ≈ 20 µm** humid and **≈ 10 µm** dry.
- **Scale invariance confirmed.** 50 V / 1 µm and 5 V / 100 nm give identical stresses when pitch scales with gap.
- **Pitch mismatch is fatal.** A 2 µm pitch with a 100 nm gap gives margin 1.8; with a 30 nm gap, 0.4.
- **Gap tolerance.** With the phase tuned for the nominal gap, a ±20 % gap error reduces the margin from 25 to 12–17.

## S3 — Power network (`results/power_network.md`, SIMULATED)

- The sparse nodal solver reproduces ΔV = IRh(h+1)/2 exactly for chains of 10, 100 and 1000 modules.
- **Uniform towers** of width 1, 5 and 20 have identical maximum drop: width does not help.
- **Root-fed arms** with cross-sections 1², 4² and 10² behave exactly like a single chain.
- **Electrical reach** h_max ≈ √(0.2V²/(PR)). Capacitive face coupling at 100 µm has |Z| = 12 kΩ (100 MHz, 100 nm gap) to 1.2 MΩ, which rules it out as the power bus.
- **Hold-up energy** at 100 µm is 1.45 nJ, about 1.45 ms at 1 µW.
- **Swarm power:** 10 cm³ at 100 µm is 10⁷ modules: 10 W at 1 µW each, 0.1 W at 10 nW each.

## S5 — Structure (`results/structure.md`, DERIVED)

- **Bond strength** of 600 kPa is needed for 1 N at 10 cm on a 1 cm square arm. A 6 kPa latch (the Karagozler value) limits a single-file 100 µm chain to 3 mm of reach.

## S6 — Interlocked Sliding Lattice kinematics (`results/isl.md`, SIMULATED)

- **Port extrusion** grew a 30-module tower from a 2-module seed with 28 lift-and-feed cycles: 56 legal moves, connected to the garment at every step.
- **Ablations:**
  - A sleeve on both sides blocks the feed (rule R3, head-on arrival).
  - Removing the upper sleeve kills traction and connection.
- **Random legal-move test:** 20,000 proposed moves gave 6,863 legal moves. The garment-contact count stayed invariant and every state remained connected. Height grew from 3 to 9, so telescoping segment moves can enlarge the structure.
- **Limitation:** 2D slice only; lateral (y) interlocks are not represented.

## S7 — Energy, speed, build time (`results/budget.md`, DERIVED)

- **Energy per lattice step** is about 4 nJ at 100 µm, with no charge recovery. Speed is 3.3–33 mm/s at a 10 kHz drive.
- **Build time:** a 10 mm × 10 mm × 10 cm rod takes about 60 s and 40 J with 100 µm modules (10⁷ modules), or about 6 s and 4 J with 1 mm modules.

## What these results do not show

- Nothing here demonstrates manufacturability, wear life, tolerance to particles, or a real fringing-field geometry.
- All literature numbers are snippet-level (see LITERATURE.md).

## Session 3 results (reproduce: `python3 sims/s3/<name>.py`; outputs in `results/s3_*.md`)

| Result | Class | File |
|---|---|---|
| Lorentz drive of permanent-magnet movers by neighbour coils: 0.1–1.7 kPa at ~40 µJ/step (100 µm); coil/PM field ratio 0.04–0.11 at all sizes ≤ 10 mm → rejected for lattices | MATH | s3_magnetic.md (M1, M2) |
| EPM switching at ≤ 50 µm poles, 1 µs: 36 nJ per pole (Hc 20 kA/m), ΔT ≈ 2 K → **retracts session-1 N1** ("EPM impossible below 1 mm"); material-limited instead | MATH | s3_magnetic.md (M3) |
| EPM reluctance stepper with sliding faces: τ/p = 0.14–0.19 (ratio mesh-converged at 0.10 at fixed offset) → friction-locked for μ ≥ 0.2 | NUM | s3_magnetic.md (M4) |
| Magnetic attachment degrades linearly with particle gap (≈ 62 kPa of 98 kPa with a 5 µm particle at 100 µm, derated) | MATH | s3_magnetic.md (M5), s3_nepl_design.md |
| Neighbour-driven push–pull EPM pivot: 2D torque margins 180/73/8.9/0.1 (90°) and 80/32/4.0/0.0 (180°) at 1 mm/300/100/10 µm; hinge load 112–125 µN at 100 µm. Model validated against the contact limit (0.94) and discretisation (2.3 %). | NUM | s3_mag_pivot.md |
| Mechanical screen: rigid zipping torque/peel < 0.04 at 90°; inchworm margin 0.07 at 100 µm (30 V); capillary rejected; sliding wear ~10⁵ cycles (SNIPPET) | MATH | s3_mechanical.md |
| Common-ground generality (2D, N = 8): sliding 62,255; NEPL 62,227 (subset; 99.95 %); ISL 19; chain: all 639 conformations, 26 % of single-component shapes | NUM | s3_generality.md, s3_cycle_compare.md |
| Executable TOWER-ARM ↔ ARCH: NEPL 9 + 9 moves, every move with modelled actuator, power continuous, 8 parallel steps; SISL 6 moves of which 4 convex (face drive cannot execute); ISL impossible | NUM | s3_cycle_compare.md |
| NEPL budgets: pins 9.4 MPa shear; contacts 0.015–0.16 Ω per face; hinge margin 1.6; landing speed ~2 m/s at every size (braking required); 145 nJ per move at 100 µm | MATH | s3_nepl_design.md |
| 3D pivot vs sliding (3×3×3 exhaustive): pivot set ⊂ sliding set; 99.6 % (N = 5), 99.88 % (N = 6) | NUM | s3_generality3d.md |

Nothing in this section is experimental. All literature numbers are snippet-level.
