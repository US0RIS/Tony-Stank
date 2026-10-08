# ARCHITECTURES — candidates, an original proposal, and comparison

## 1. Screening of mechanisms for a 100 µm module (onboard electrical drive)

| Mechanism | Verdict at 100 µm | Reason (tag) |
|---|---|---|
| Electropermanent magnets | **Reject below ~1 mm** | At 100 µm, switching needs J ~5×10¹⁰ A/m² (above electromigration and thermal limits) and ~37 µJ per pulse, about 10⁴× the energy budget of a step (DERIVED, S1/S7). They work at 1 cm (Pebbles, VERIFIED-META). |
| Onboard coils (magnetic drive) | Reject | Force ∝ L⁴ at fixed current density (DERIVED). |
| Electrothermal | Reject as main drive | W-level power for mm-class strokes (SNIPPET). Thermal bandwidth falls as L². |
| SMA films | Reject | Hysteresis and heating power; 20–300 Hz (SNIPPET). |
| Electrochemical (Miskin) | Keep for single microrobots | nW power and µm scale demonstrated, but force not established and needs a liquid environment (VERIFIED-META / CONFLICTING). |
| Piezo (AlN) | Secondary | ~1 µm strokes at tens of V (SNIPPET). Needs a stepping mechanism, and no microscale blocked-force data was found. |
| Capillary bonding | Reject for wearables | Needs controlled liquid. It also sets the adhesion floor that every dry design must beat (DERIVED). |
| Electroadhesion, thick polymer | Reject for strength | ~1–10 kPa (DERIVED/SNIPPET). Air-gap physics caps it at ~11 kPa (PHYSICS §4). |
| **Electrostatic multiphase face drive (DEMED type)** | **Primary actuator** | Scale-invariant stress of ~7 kPa (after the discrete-electrode factor) at 5 V/100 nm or 50 V/1 µm. Phase control cancels the normal force. ~4 nJ per step. Sliding margin ~25 at 100 µm (DERIVED + SIMULATED, S2). DEMED itself works at 320 µm pitch (VERIFIED-META). |
| Electrostatic inchworm (Pister/Bergbreiter) | Secondary | mN at ~100 V with 10⁷-cycle data (SNIPPET). Needs a dedicated shuttle and gap-closers, so it is bulkier than a face drive. |
| **Undercut mechanical interlock** | **Primary attachment** | Tensile strength comes from Si fracture strength rather than from fields (HYPOTHETICAL magnitude, 1–100 MPa nominal). It is the only option found that meets the 100–700 kPa structural requirement (S5) at small scale. |

## 2. Architecture A — "Universal crawler" (the brief's architecture)

Every module is a full robot. It crawls over the garment and over other modules, and attaches and detaches anywhere (sliding-cube model). Detaching along a face normal needs a switchable attachment.

- **Strength:** sliding cubes are universal, O(n²) moves (Abel et al. 2024, VERIFIED-META).
- **Fatal-flaw candidate (DERIVED):** a switchable attachment strong enough for human-scale structures (≥ 0.1–0.7 MPa) and also able to slide does not exist in the mechanisms screened:
  - Air-gap electrostatics: ≤ 11 kPa.
  - Contact electrostatics: MPa, but cannot slide (van der Waals plus friction).
  - EPMs: infeasible below 1 mm.
  
  A crawler swarm of 100 µm modules is therefore limited to structures of roughly mm to cm scale (S5: 3–8 mm single-file reach at 6–50 kPa). Convex transitions also break face contact (pivot), and a hold-up capacitor covers only ~0.36 of a step at 100 µm.
- **Status:** physically plausible for small, weak, slow structures. **Not a credible route to the user experience.**

## 3. Architecture B (original proposal) — Interlocked Sliding Lattice with Port Extrusion (ISL-PE)

### B.1 How it works (HYPOTHETICAL design, SIMULATED kinematics)
1. **Modules.** Cubic Si blocks, edge L (1 mm → 100 µm). Every face carries an undercut T-slot grid plus mushroom-head keys arranged genderlessly. Adjacent faces are **permanently interlocked**: they can slide relative to each other along the face but cannot separate or approach along the normal.
2. **Motion.** A move translates a whole straight run of modules by one lattice pitch along its own axis.
   - Thrust comes from DEMED-type 3-phase electrodes on the sliding faces, phase-tuned for near-zero net normal force.
   - Undercut geometry forbids head-on separation and head-on arrival (rules R1–R5 in `sims/isl.py`).
3. **Attachment.**
   - Tension and peel: carried by the interlock (mechanical).
   - Shear along the rail (holding position): electrostatic shear lock at ~7 kPa, plus optional detents.
4. **Power and data.**
   - Power: a pair of low-force sliding ohmic contacts (Au/Ru brushes) on rail flanks. Because faces never separate, every module stays connected at every instant.
   - Data: capacitive, over the same electrodes at MHz frequencies, multiplexed with the kHz drive.
5. **Shape change by extrusion.**
   - The garment carries a base layer of modules with **ports**: holes with a sleeve of driver modules on one side.
   - Columns are extruded through ports. Each cycle the column is lifted one pitch by the sleeve, and a feeder row slides the next module under it.
   - Feeder rows run on the base layer like conveyors.
   - Retraction is the reverse cycle.
   - This is the microscale, lattice-addressable counterpart of the rigid-chain actuator (VERIFIED-META macro prior art).
6. **Most modules can be passive.** During extrusion only port and sleeve modules actuate; column modules ride along. Most modules then need only geometry and electrical feed-through: no logic, no drivers. This changes yield and cost (FAILURE_MODES §5).

### B.2 Physical principles
Electrostatic Maxwell stress for thrust; mechanical interlock for tension; Holm sliding contacts for power; capacitive coupling for data; lattice kinematics with connectivity invariants.

### B.3 Constraints derived
- **Sliding margin:** M = 25 at 100 µm (humid), 360 at 1 mm, ~0.3 at 10 µm (S2). Size floor ~10–20 µm.
- **Gap tolerance:** ±20 % gap error leaves M ≥ 12 if pitch = 3.3 g. If the pitch is fixed at 2 µm with a 100 nm gap, M ≈ 1.6–1.9 (fails with any margin) (S2).
- **Power reach:** brush R ≤ 100 Ω gives ≥ 1.3 cm at 1 µW and 3 V, and ≥ 13 cm at 30 V or at 10 nW static (S3).
- **Strength:** interlock ≥ 0.6 MPa supports 1 N on a 10 cm × 1 cm arm (S5).
- **Build:** 10 cm rod with a 1 cm section in ~60 s and ~40 J at 100 µm; ~6 s at 1 mm (S7).

### B.4 Kinematic validation (SIMULATED, 2D slice)
- A 30-module tower was extruded from a 2-module seed with all 56 moves legal and every state connected to the garment.
- **Ablations.** If a sleeve is present on both sides, the feed is blocked by the head-on-arrival rule, so the port must be asymmetric. Without the upper sleeve, the lifted column loses traction and connection.
- **Proven invariant** (test and argument): the number of modules touching the garment never changes. Leaving the garment requires head-on separation, which is forbidden. Modules therefore enter and leave the structure only through the base layer's conveyors and ports.

### B.5 Most likely fatal flaw
**Particles and wear in the interlock and face-drive gaps.**
- The design needs gaps of 0.1–1 µm with ~±20 % uniformity over every face, while sliding for ~10⁶–10⁸ steps.
- Ordinary dust (1–10 µm) and Si wear debris both exceed these gaps.
- Polysilicon MEMS sliding interfaces have a reputation for wear-debris failure (not verified in this session).

Close behind: **slot seam alignment**. A key crossing from one module's slot into the neighbour's requires lattice registration finer than the slot clearance, and tolerances stack across the lattice.

### B.6 Decisive tests
EXPERIMENTS E1 (face-drive coupon), E3 (interlock strength + wear + particle challenge), E4 (seam crossing). E3 is the most likely to kill the architecture.

### B.7 Comparison

| | A: universal crawler | B: ISL-PE | Macro rigid chain |
|---|---|---|---|
| Shape class | Any (in theory) | Extruded prisms and stepped profiles; branching and bending untested | 1D column |
| Structural strength | ≤ 11 kPa interface (electrostatic) | Material-limited interlock (MPa, HYPOTHETICAL) | High |
| Power continuity | Broken at convex transitions | Continuous by construction (SIMULATED) | N/A |
| Fraction of modules that must be active | 100 % | Ports and sleeves only (~1/h) | Motor only |
| Smallest credible L | ~20 µm for sliding; strength kills human scale | ~20 µm for sliding; tolerance and particles likely set ~100 µm–1 mm | cm |
| Prior art | Claytronics, 3D Catoms (unrealised) | Combination not found (search limited) | Industrial |

## 4. Recommendation

1. Abandon the "every module crawls anywhere" premise for human-scale structures.
2. Pursue **ISL-PE at 1 mm first**, then 100 µm. It is the simplest architecture found that meets requirements A–G at once.
3. The garment becomes a **magazine plus port array**: an addressable, two-dimensional, rigid-chain actuator built from identical microscale blocks.
4. **What this gives up:** arbitrary 3D shapes. Universality of the ISL rule set (with branching ports, or columns re-entering ports) is an open computational question (EXPERIMENTS S-E6).
