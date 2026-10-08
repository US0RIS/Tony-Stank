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
