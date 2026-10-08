# Tony-Stank — microscopic programmable matter: research workspace

**Objective.** Find a physically realisable mechanism by which sub-mm robotic modules can:
- pass power and data through their contacts,
- attach reversibly and strongly,
- move over one another under onboard control,
- stay powered while moving,
- and collectively form useful 3D structures from a garment.

Module sizes 10 mm → 1 mm → 100 µm → 10 µm are analysed throughout.

## Session 2 audit — read this first ([AUDIT.md](AUDIT.md), [TRACKS.md](TRACKS.md))

Evidence classes: MATH = derivation or proof · NUM = simulation · EXP = experiment. **No experiments have been done in this project.**

1. **Face motor, revised.**
   - A realistic dielectric stack gives **5.7 kPa** (not ~7) (NUM).
   - The 50 V / 1 µm design is at the micro-gap breakdown limit and must be derated to ~2.1 kPa (NUM, plus unverified literature).
   - **New flaw:** thrust ∝ exp(−k·d_particle). One 0.3 µm particle removes 98 % of the 5 V design's thrust (MATH). No open-air operating point is simultaneously breakdown-safe, particle-tolerant and above ~1–2 kPa, so **electrostatic sliding needs a sealed volume**.
   - Step energy is 15–40 nJ, not 4. The sliding size floor is ~22–37 µm, not 10–20.
2. **Power claim is false in general.** "Drop depends only on height" holds only for uniform load, a full footprint and an ideal garment. Real geometry factors are 1–10×, and a separate return conductor doubles the drop (NUM). Width provides redundancy.
3. **ISL-PE is kinematically sound and reversible, but session 1 overstated it.**
   - Confirmed: 3D slab-feed extrusion is legal (NUM). **Every ISL shape change is exactly reversible** (MATH proof + NUM).
   - **New flaw:** every interface is a slip plane, so a 1 cm rod slips plastically above ~0.7 N (MATH). The proposed fix, port-engaged cam latches, is untested.
   - Jamming needs clearance ≳ 10σ (NUM).
   - Build time was wrong: about 150 s for a 10 cm rod, not 60 s (MATH).
   - **Branching is possible:** search found a 6-module horizontal cantilever in 13 legal moves (NUM).
4. **Two tracks** ([TRACKS.md](TRACKS.md)).
   - Track A: revised ISL-PE (sealed magazine, port wiper seals, cam latches, extend-then-lock).
   - Track B: nine quantified breakthroughs. The deepest is **B3: particle-tolerant actuation in open air**. The proposed target architecture is a Switchable-Interlock Sliding Lattice (ISL with retractable bolts, whose MPa strength is independent of module size, MATH).

## Session 1 findings (superseded where the audit above disagrees)

Tags: DERIVED = analytic · SIMULATED = code in `sims/` · HYPOTHETICAL = proposed design, untested.

1. **The weak link at small scale is structural strength, not actuation.**
   - Human-scale structures (1 N at the tip of a 10 cm × 1 cm arm) need **≥ 0.6 MPa** tensile strength at every interface.
   - Air-gap electrostatic attachment is capped at **~11 kPa** (DERIVED).
   - The best switchable latch found in the literature holds 6 kPa (Karagozler 2007).
   - Electropermanent magnets cannot be switched below ~1 mm: J ~5×10¹⁰ A/m² at 100 µm (DERIVED).
2. **A phase-tuned multiphase electrostatic face drive can slide one module along another with near-zero net clamping force.**
   - Validated against finite differences to 1.4 % (SIMULATED).
   - Stress is scale-invariant at constant field, so **5 V across a 100 nm gap at 0.33 µm pitch (CMOS-compatible, below gas-breakdown threshold) gives the same ~7 kPa shear as 50 V at 1 µm**.
   - Sliding margin is ~25 at 100 µm in humid air. Floor: **L ≈ 10–20 µm**, because thrust ∝ L² loses to adhesion.
3. **Power must flow through continuous ohmic contacts.**
   - Capacitive face coupling at 100 µm has |Z| of 10⁴–10⁶ Ω. On-chip storage covers only ~1/3 of a step.
   - Voltage drop depends only on height in hops: reach ≈ √(0.2V²/(PR)) hops (SIMULATED).
   - Standby power must be ≤ 10 nW per module for a 10⁷-module garment.
4. **Proposed architecture: Interlocked Sliding Lattice with Port Extrusion (ISL-PE)** (HYPOTHETICAL; kinematics SIMULATED).
   - Faces are permanently interlocked by undercut rails, so tension is carried mechanically.
   - Electrostatic face drives provide shear only.
   - Structures are extruded through ports in a garment-borne magazine, like a microscale, addressable rigid-chain actuator.
   - In a 2D lattice simulation, a 30-module tower was extruded with every state connected to the garment.
   - Most modules can be passive; only port and sleeve modules need to be active.
5. **Most likely fatal flaw of ISL-PE:** particles and wear in the 0.1–1 µm sliding gaps, plus slot-seam alignment. These are tested first by experiments E3 and E4.
6. **The brief's architecture of fully active modules crawling anywhere is not supported** for human-scale structures. See ARCHITECTURES.md §2 for the reasoning.

**Honest bottom line.** Nothing here shows that 100 µm programmable matter in clothing is buildable today. A 1 mm interlocking-block extrusion system that produces real, load-bearing rods and blades from a cuff looks reachable with existing fabrication. It is the shortest credible path, and it tests the physics that the smaller scales depend on.

## Navigation

| File | Contents |
|---|---|
| [AUDIT.md](AUDIT.md) | Session-2 audit of the three key claims and the generalisation study |
| [TRACKS.md](TRACKS.md) | Track A (prototype path) and Track B (breakthroughs required) |
| [LITERATURE.md](LITERATURE.md) | Sources with explicit verification status. Full-text access was blocked this session. |
| [PHYSICS.md](PHYSICS.md) | Equations, scaling laws, assumptions |
| [ARCHITECTURES.md](ARCHITECTURES.md) | Mechanism screening; Architecture A vs ISL-PE |
| [FAILURE_MODES.md](FAILURE_MODES.md) | Negative results N1–N10, risks, open questions |
| [EXPERIMENTS.md](EXPERIMENTS.md) | Ranked falsification tests E1–E5, S-E6 |
| [RESULTS.md](RESULTS.md) | Numerical results and reproduction steps |
| [ROADMAP.md](ROADMAP.md) | Phased path to a first prototype |
| `sims/` | `scaling.py`, `face_motor.py`, `power_network.py`, `structure.py`, `isl.py`, `budget.py`, `track_b.py` |
| `sims/audit/` | `face_motor_realistic.py`, `power_audit.py`, `isl3d.py`, `isl_audit.py`, `branch_probe.py` |
| `results/` | Generated outputs (markdown tables) |
| `tests/` | Regression and independent-check tests (`python3 -m pytest -q tests`) |

## Method notes

- Four parallel literature subagents covered prior art, actuation, docking/kinematics, and power/storage. Their outputs were cross-checked and several premises corrected; LITERATURE.md records what was confirmed.
- Agreement between agents was not treated as evidence.
- No simulation output in these documents was written by hand. Every number in RESULTS.md is produced by the scripts.
