# Two research tracks

The ultimate objective is unchanged: independently mobile, fully reconfigurable microscopic modules worn on clothing, which are discreet, effortless, observable, universal and authentic. ISL-PE is kept as a **candidate** for Track A only. Its limitations do not redefine the objective.

---

## TRACK A — shortest credible path to a demonstrable wearable prototype

**Candidate:** ISL-PE, revised after the audit (AUDIT.md).

| Element | Session-1 version | Revised version | Why |
|---|---|---|---|
| Feed | Single feeder row | Thick slab feed from a sealed magazine | Growth ≈ v × t_mag / W (AUDIT 3) |
| Environment | Open lattice | Sealed magazine plus rod-wiper seal at each port | Open-air electrostatic sliding is not particle tolerant (AUDIT 1) |
| Interior shear | Electrostatic | Cam-engaged passive latches closed by port geometry | Slip planes (AUDIT 3) |
| Load case | Any | Extend unloaded, then lock | Sleeve-height scaling (AUDIT 3) |
| Drive | Face motor everywhere | Face motor only in base stators and sleeves; everything else passive | Yield; power (AUDIT 2) |

**Gates, in order (each one is experimental and can kill Track A):**

| Gate | Test | Pass criterion |
|---|---|---|
| A0 | Full-text literature check (ROADMAP Phase 0) | — |
| A1 | E5: 10 mm printed blocks, motorised port, cam latches | Extrude/retract 100×; 0.5 N tip load on a 10-block rod without slip |
| A2 | E6: cam-latch shear test at 1 mm | Interface shear ≥ 100 kPa locked; ≤ 1 kPa resistance unlocked |
| A3 | E1′: face-drive coupon in a sealed dry-N₂ cell vs lab air with seeded particles | Predicts ≥ 3 kPa sealed and collapse in open air. If open air works, AUDIT 1 is wrong in our favour. |
| A4 | 1 mm Si module port array | Extrude a 5 mm square × 5 cm rod in < 60 s |

**Honest expected outcome.** A cuff that extrudes and retracts rods and blades of 1 mm blocks in tens of seconds, load-bearing to about 1 N once locked. It is observable and authentic, partially discreet, not universal in shape, and needs a sealed magazine.

---

## TRACK B — breakthroughs required for independently mobile, fully reconfigurable microscopic modules

Each requirement below is a quantitative target derived in `sims/track_b.py`, AUDIT.md or PHYSICS.md. "Open" means no known solution.

| ID | Breakthrough needed | Quantitative target | Current best candidate | Evidence | Status |
|---|---|---|---|---|---|
| B1 | **Switchable attachment that is both strong and slidable** | ≥ 0.6 MPa tensile and ≥ 0.1 MPa shear when locked; ≈ 0 normal force when sliding | Retractable Si bolts: 3 MPa equivalent at any L, since pressure = 2τ(b/L)(t/L) is size-independent. MEMS latch components exist (patents US6865313, US20070001542; CA 2421755 on latches holding more than their switching force). | MATH; EXP for components only | Plausible, untested in a module |
| B2 | **Bolt actuation inside the module** | ≥ 0.4 µN over 5–10 µm stroke within ≤ 5 % of a face | 30 V comb drive: 11 fingers at 100 µm, 37 at 30 µm (~1.6 face areas, does not fit). At 5 V it does not fit below ~100 µm. Needs force amplification (ratchet/inchworm) or local HV. | MATH | Open below 100 µm |
| B3 | **Particle-tolerant actuation in open air** | ≥ 2 kPa shear with ≥ 5 µm particles present | None. Rigid electrostatic faces fail (AUDIT 1). Candidates: compliant/conformal electrode skins (stress no longer limited by the rigid-gap prop); self-sealing micro-environments; actuation not limited by gap (mechanical ratchets driven by internal actuators). | MATH (negative result) | **Fundamental blocker** |
| B4 | **Adhesion engineering below 20 µm** | Total adhesion ≤ 170 nN at L = 10 µm (margin 5) | Capillary bridges eliminated. Hydrophobic SAM standoffs of radius ≤ 0.6 µm at 10 µm, ≤ 0.15 µm at 5 µm. MEMS anti-stiction SAMs are established practice (literature not yet verified here). | MATH | Plausible to ~10 µm, marginal at 5 µm |
| B5 | **Power during convex transitions** | Survive a 1–10 ms loss of contact | Self-powered transit is infeasible below ~100 µm (1.45 nJ hold-up at 100 µm, 0.0145 nJ at 10 µm). Neighbour-actuated passive transit with nonvolatile state needs only retention power (10 nW for 1.5 ms at 10 µm). | MATH | Architectural change: "the lattice moves the module" |
| B6 | **Standby power and addressing** | ≤ 10 nW per module; 10⁷-node addressing | Subthreshold or power-gated logic (literature SNIPPET level) | MATH | Open (no module-scale data) |
| B7 | **Shear rigidity of a reconfigurable lattice** | Interface shear lock ≥ 0.1 MPa, releasable per interface | Same bolts as B1 | MATH | Same as B1 |
| B8 | **Manufacturability / fault tolerance** | Function with ≥ 1 % dead modules | Passive-cargo transit (B5) lets dead modules be carried; route power around failures (AUDIT 2: 3D lattices tolerate 30 % contact failure) | MATH, NUM | Plausible |
| B9 | **Universality with physical rules** | Reconfiguration universal under connectivity + powered + traction constraints | Sliding cubes are universal in the abstract (Abel et al. 2024). ISL is not universal over all shapes (garment-contact invariant). SISL (ISL + bolts) inherits sliding-cube universality only if bolts give normal detachment and convex transitions are neighbour-actuated. | MATH | Open for physical rule sets |

**Track B target architecture (HYPOTHETICAL): Switchable-Interlock Sliding Lattice (SISL).**
- ISL faces with retractable bolts (B1, B2, B7).
- Phase-tuned face drive in a sealed or compliant interface (B3).
- Hydrophobic sharp standoffs (B4).
- Passive cargo transport by neighbours across convex transitions (B5).
- Sweet spot ≈ 30–100 µm. Below ~20 µm, B3 and B4 dominate; below ~10 µm, B2 and B4 fail with known methods.

**Most decisive Track B experiments:**
- **E7:** bolt latch at 1 mm and 100 µm. Strength, actuation force, and alignment capture range when guided by a synchronous face drive, whose positioning resolution is a fraction of the pitch.
- **E8:** compliant-electrode face drive under particle challenge. This directly attacks B3, the deepest blocker.

---

## Session-3 revision

**Track B now has a concrete leading architecture: NEPL** (NEW_MECHANISMS.md).
- It answers B1/B7 (switchable attachment plus pin shear), B3 in part (particle-tolerant attachment, linear degradation), and B5 (passive mover, no power needed in transit).
- B2 is reformulated: bolt actuation is no longer needed, because pins work with pivots.
- B3 for locomotion is answered by **removing sliding**: there is no exponential gap sensitivity in rolling pivots.
- New gating item, **B10: a microfabricated switchable (semi-hard) magnet film plus pulsed microcoils.** This is the single most decisive open question; experiment E9.
- Scale window: credible 300 µm–1 mm; marginal 100 µm (180° pivot margin 2.0 after a ×0.5 3D derate); infeasible at ≤ 30 µm.
- **The ≤ 100 µm goal therefore needs adhesion reduction or a stronger force mechanism.** Margin ∝ L² against adhesion.

**Track A stays ISL-PE**, with three changes:
- ISL-PE is not the final architecture. Its shape space is 19 states versus about 62,000 for NEPL/SISL in the common test.
- New risk E13: sliding wear (~10⁵ cycles in air for bare polysilicon, snippet).
- Proposed hybrid: ISL-PE ports deliver bulk material, and NEPL surface modules form branches, cavities and joints. This lets the Track-A hardware feed Track B.

**Shortest path to a demonstrable general-reconfiguration prototype (new):**
1. 10 mm NEPL blocks using macro EPMs (Kubits-class) in passive-mover mode, with pins and pole-piece contacts. Demonstrate a TOWER-ARM ↔ ARCH transformation (9 moves each way, already planned in `s3_cycle_compare.md`) while every module stays powered.
2. E9 at 1 mm.
3. 1 mm NEPL blocks.
4. 300 µm.

Each step is falsifiable by E10 and E12.

---

## Session-4 revision (FEASIBILITY_VERDICT.md)

**NEPL is not realisable at 100 µm** with thin-film switchable magnets: verdict D (flux starvation against adhesion).
- At 300 µm it requires specific advances: verdict C.
- At about 0.6–1 mm it is plausible but needs experiments: verdict B.

**Track A** (wearable demonstrator): a 1 mm NEPL is now a candidate alongside ISL-PE. Its first experiments are:
- **E9′:** a CoP-bar EPM face at 1 mm. Measure loop squareness, reversal time, attached clamp vs the FD prediction (~200 µN at 1 mm by similarity), and cross-talk creep.
- **E10′:** pivot torque profile at 1 mm vs `cycle_dynamics.py`.
- **E15:** a departure hinge compatible with identical modules (chiral edge pattern).

**Track B** (≤ 100 µm): magnetic body-force actuation of switchable-attachment lattices is now **excluded at 100 µm**. The required Jr·sq (3.2 T humid) exceeds every known material.
- Remaining routes must change the force law: surface-force actuators that scale with contact area, such as the electrostatic face drive (sealed) or electroadhesion/electrostatic clamps.
- Or they must remove the adhesion barrier: sealed low-humidity environments, engineered sub-10 nN contacts.
- Or they must use externally assisted actuation, such as a global field from the garment.
- Session 3's "strongest surviving architecture" ranking is **revised**: NEPL survives only at ≥ ~0.6 mm.
