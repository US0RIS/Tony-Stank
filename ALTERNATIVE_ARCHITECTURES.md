# ALTERNATIVE_ARCHITECTURES — non-cubic, hybrid and continuous designs (session 3)

Labels as in MAGNETIC_ACTUATION.md. Sources are LITERATURE-SNIPPET unless stated; the proxy blocked full text.

## 1. Candidates examined

| Architecture | Literature status | Active parts | Generality | Key physics finding this session | Verdict |
|---|---|---|---|---|---|
| **Folding chain (moteins)** — Cheung, Demaine, Bachrach, Griffith, IEEE T-RO 27(4) 2011, doi:10.1109/TRO.2011.2132951; Milli-Motein (1 cm, EPM wobble motor, 2.6 W) | Universality theorem for polyhedra via subdivision, needing arbitrarily long strings (snippet) | 1–2 DOF per unit (every unit active) | Within the bounded window, the pivot moves reach **all 639** anchored conformations (NUMERICAL). The shape class is topologically limited: only Hamiltonian-path shapes, **26 %** of the single-component shapes MPL reaches at N = 8 (NUMERICAL). Subdivision (moteins) recovers universality at the cost of more units per voxel. | Power continuity is ideal: wired, no contacts. A single hinge failure severs everything downstream (series reliability). The folding torque problem is the same as MPL's, plus whole sub-chain sweeps. | **Strong for power and environment, weak for generality and fault tolerance.** Kept as a Track-A/B hybrid option (§3). |
| **Active carriers on passive voxels (ACPL)** — BILL-E/relative robots (RA-L 2019); ARMADAS (Science Robotics 9(86) 2024, doi:10.1126/scirobotics.adi2746: 256 voxels of 304.8 mm in 4.2 days); hybrid programmable-matter theory: one active agent suffices in 3D (Hinnenthal, Rudolph, Scheideler, arXiv 2401.17734) | Macro demonstrations only | ≪ 1 % active | Universal in the abstract hybrid model (theory, snippet) | Carriers can walk over passive soft-iron voxels as NEPL **pairs**. A attaches to the voxel iron; B pivots, pushed by A and pulled by B's own EPM toward the voxel iron (MATHEMATICAL DERIVATION). Passive voxels need permanent snap/pin bonds placed by carriers, and two conductors for power. | **Strongest alternative for manufacturability and yield.** Speed: about 17 s to place 3.7×10⁵ voxels of 300 µm with 1 % carriers at 0.3 m/s (ESTIMATE, ignoring congestion). |
| **Sliding lattice (SISL), electrostatic** | Abel et al. SoCG 2024 (universal). Kawano RA-L 2023: sliding-only, linear time with meta-modules (snippet) | All active | Equal to the sliding model | Two thirds of the moves in the test transformation were convex transitions, which a face drive cannot execute (NUMERICAL). Sliding-only meta-module schemes avoid them but multiply sliding distance. Sliding-contact life in air ~10⁵ (snippet). Particle intolerance (AUDIT N11). | Viable only **sealed**, with wear-resistant coatings |
| **Spherical modules (3D Catoms-like)** | No hardware below mm | All active | Rotations on an FCC lattice | Point or small-area contacts: attachment pressure × contact area collapses, and power contacts are small. Rolling avoids sliding wear. | Not pursued: the strength-per-contact penalty is severe |
| **Tetrahedral / truss (Variable Topology Truss, Odin)** | Macro only | Every member a linear actuator | Topology change by node merge/split; planning open | Needs high-stroke linear actuators: the micro stroke problem (piezo 1.3 µm) | Rejected at < 1 mm |
| **Self-folding sheets / origami (Felton 2014; Gracias micro-origami)** | Demonstrated, one-shot or few-shot | Hinges only | One sheet gives a family of shapes, not arbitrary ones | Polyimide hinge life 10⁴–10⁵ cycles (snippet) | Good for Track-A garment features (pop-up structures), not for general reconfiguration |
| **Continuous materials (LCE, jamming)** | Programmable 2D→3D deformation; arbitrary targets not shown | Continuous | Deformation family set at fabrication | Not reconfigurable into unrelated topologies | Rejected for the generality goal; useful as an actuated skin |
| **Hierarchical / meta-modules** | Crystalline O(log n) parallel steps (theory) | — | Recovers universality for restricted move sets | Multiplies the number of moves | Kept as a planning tool |

## 2. The question "dramatically fewer actuated parts"

- **ACPL** is the only family that reduces the active fraction by orders of magnitude while keeping theoretical universality (hybrid model, snippet-level).
- Its physical feasibility rests on the **same** NEPL pivot physics for the carriers, so it shares NEPL's material risk (semi-hard EPM films).
- It removes most of NEPL's yield risk: passive voxels have no electronics.

## 3. Hybrid proposals worth testing

1. **NEPL + ACPL** ("active skin, passive bulk"). Interior voxels are passive and pinned; NEPL-active modules form the surface and act as carriers. This sets the active fraction to about the surface-to-volume ratio: 6L/W, about 6 % for a 1 cm object of 100 µm modules (MATHEMATICAL DERIVATION).
2. **ISL-PE + NEPL.** Port extrusion delivers bulk material fast as rods. NEPL surface modules then reshape the rod ends into branches, joints and cavities (ENGINEERING HYPOTHESIS).
3. **Chain + lattice.** The chain gives the power backbone (wired); lattice modules attach to it. UNVERIFIED SPECULATION.
