# EXPERIMENTS — ranked falsification tests

Ranking: the probability that a test kills the leading architecture (ISL-PE), weighed against its cost. Run the cheap killers first.

| Rank | ID | Question | Kills ISL-PE if… |
|---|---|---|---|
| 1 | E3 | Do microscale undercut interlocks give ≥ 1 MPa nominal tensile strength **and** slide 10⁵ pitches without debris lock-up? | Pull-out < 0.3 MPa, or friction rises > 3× / jams within 10⁵ cycles in lab air |
| 2 | E1 | Does a phase-tuned 3-phase face drive produce sliding with net normal force ≈ 0? | Measured shear at zero normal < 1 kPa, or the module cannot slide at 50 V/µm in 40–60 % RH |
| 3 | E4 | Can a key cross a seam between two modules' slots? | Required alignment < 0.5 µm at 100 µm scale (not achievable passively) |
| 4 | E2 | Do sliding microbrushes keep R ≤ 100 Ω over 10 m of travel at ≤ 10 µN? | R > 1 kΩ or open circuits > 10⁻⁴ per step |
| 5 | E5 | Does a 10 mm-module ISL-PE prototype extrude a 20-module column with continuous power? | Any systematic jam, or power interruption at the port |
| — | S-E6 | (computational) Is the ISL move set universal in 3D with ports on the structure? | A proof of locked configurations for useful target shapes |

## E1 — Face-drive coupon (tests PHYSICS §2, S2)
- **Build.** Two Si chips (2 × 2 mm active area), each with 3-phase Al stripes at λ = 3.3 µm under 100 nm SiO₂, plus 1 µm SiO₂ standoff bumps (9 per 100 µm cell). The top chip sits on a calibrated flexure (shear) and a load cell (normal).
- **Measure.** τ and p versus phase offset θ at 10–50 V, at 10 % and 60 % RH. Then free sliding over 1 mm.
- **Predictions (SIMULATED).** τ_peak ≈ 0.59 × 12.1 kPa ≈ 7 kPa at 50 V. A zero-normal phase exists at cos(ks) = 1/cosh(kg) (exact for V₁ = V₂; ks ≈ 1.28 rad at kg = 1.915). Sliding margin ≈ 25 (humid), ≈ 94 (dry) for 100 µm-equivalent cells.
- **Success:** τ ≥ 3 kPa at |p| ≤ 1 kPa; sustained sliding.
- **Failure means:** the friction or adhesion model is wrong. Re-fit μ and F_adh; revise the size floor.
- **Variant:** a 5 V / 100 nm / 0.33 µm-pitch coupon, which tests scale invariance and the gap-uniformity requirement.

## E2 — Sliding power contacts
Au, Ru and Pt-on-Au cantilever brushes at 1–10 µN on Au rails. Reciprocating 100 µm strokes for 10⁵ cycles (10 m of travel) in lab air. Log R(t) at 1 µA and 10 µA, and image debris.
**Success:** median R ≤ 100 Ω and no opens longer than 1 ms.

## E3 — Interlock strength, friction, wear, particle challenge (highest kill probability)
- **Build.** DRIE Si T-slot / mushroom-key pairs at module scales of 1 mm and 100 µm. Clearances of 0.5, 1 and 2 µm. Coatings: bare, SiO₂, DLC, and fluorosilane SAM.
- **Measure:**
  1. Pull-out strength (normal tension) and peel moment.
  2. Sliding friction versus cycles over 10⁵ cycles.
  3. Tolerance to seeded 0.5–5 µm alumina particles.
- **Success:** ≥ 1 MPa nominal; friction coefficient stable within 2× over 10⁵ cycles; tolerates particles smaller than the clearance.

## E4 — Seam crossing
Two interlocked 1 mm modules on a micrometer stage, with a third module whose key must cross between them. Sweep the misalignment (lateral and angular) and record the crossing force.
**Success:** crossing tolerant to ≥ 2 µm misalignment at the 1 mm scale (≥ 0.2 µm at 100 µm with self-centring chamfers).

## E5 — 10 mm macro prototype of ISL-PE (kinematics, power continuity)
- 3D-printed or machined interlocking blocks with copper-tape brush contacts on the rails.
- The port uses a conventional micro-stepper and lead screw for lift and feed. Only the port is active, which is exactly the passive-module hypothesis.
- Extrude and retract a 20-block column 100 times while powering an LED in the top block.
- **Success:** no jams in 100 cycles, LED never drops out, and the column holds a 0.5 N tip load at 10 blocks.

## S-E6 — Computational: 3D ISL universality
Extend `sims/isl.py` to 3D. Search (BFS / A*) for move sequences between small configurations under R1–R5, with ports allowed on the structure itself. Either find a constructive universal strategy (for example, ports that relocate) or exhibit locked configurations.

## Already executed this session (computational)
- S1–S7, listed in RESULTS.md. All are reproducible with `python3 -m pytest -q tests` and `python3 sims/<name>.py`.
