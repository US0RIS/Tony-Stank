# ARCHITECTURE_COMPETITION — session 3

All rows use equal assumptions: humid adhesion (9 bumps, 4.1 µN), μ = 0.4, Br = 1.0 T, 2D bounded searches with the same window, N and start.

Evidence labels:
- **N** = NUMERICAL SIMULATION
- **M** = MATHEMATICAL DERIVATION
- **H** = ENGINEERING HYPOTHESIS
- **S** = LITERATURE-SNIPPET

## 1. Candidates entering the competition (≥ 3 survived screening)

| ID | Architecture | Mover actuation | Attachment | Power in transit |
|---|---|---|---|---|
| ISL-PE | Interlocked sliding lattice, port extrusion (sessions 1–2) | Electrostatic face drive (sleeves only) | Undercut interlocks + cam latches (H) | Continuous contact |
| SISL | Sliding cubes, electrostatic face drive + bolts | Face drive; convex moves need a second actuator | Bolts (H) | Continuous on slides, broken on convex moves |
| **NEPL** | Neighbour-actuated EPM pivoting lattice (new formulation) | Stationary neighbours' EPM push–pull | EPM (switchable) + conical pins | Not needed (passive mover) |
| FC | Folding chain (moteins) | Hinge actuator per unit (EPM pivot physics) | Hinges + latches | Wired, continuous |
| ACPL | Active carriers on passive voxels | Carrier pairs using NEPL physics | Passive snap/pin bonds | Carriers powered via voxels (two conductors needed) |

## 2. Scored comparison at L = 100 µm (and 300 µm where it differs)

| Criterion | ISL-PE | SISL | NEPL | FC | ACPL |
|---|---|---|---|---|---|
| Force margin per move | Sealed 5.7 kPa, margin ~20 (N); open air with particles ≪ 1 (M) | Same as ISL-PE for slides; convex moves unexecutable without a pivot actuator (N) | 90°: 4.5, 180°: 2.0 (300 µm: 36/16) (N, 3D derate H) | Pivot of a whole sub-chain: ≤ NEPL (M) | Like NEPL (M) |
| Attachment tension | Interlock: material-limited (H) | Bolts ~3 MPa (M, H) | ~100 kPa clean, 62 kPa with 5 µm particle (M, derated H) | Hinges + latches (H) | Snap bonds (H) |
| Attachment shear | Slip planes ~10 kPa unless cam latches (M) | Bolts (H) | Pins 9.4 MPa (M) | Hinges (H) | Snap / pins (H) |
| Particle tolerance | exp(−k·d): needs sealing (M) | Same | Linear in gap/l_m (M) | Hinged: moderate (H) | Like NEPL |
| Wear mode | Sliding, ~10⁵ cycles in air (S) | Sliding (S) | Rolling + normal landing; impact (M, unverified) | Hinge rotation | Rolling (carriers) |
| Power continuity | Yes | Gaps at convex moves | Mover passive; all actuators stay powered (N) | Wired | Carriers need hold-up or voxel contacts |
| Energy per move | 15–40 nJ (M) | 15–40 nJ + pivot | 145 nJ (M) | ≥ NEPL | ≥ NEPL |
| Reachable configurations (2D, N = 8) | 19 (N) | 62,255 (N, complete) | 62,227, which is 99.95 % of SISL (N) | 639 conformations (all that exist); 26 % of single-component shapes (N) | Universal in theory (S) |
| Branch / cavity / cantilever (depth) | None from the common start; branches from a port start (session 2) | 1 / 1 / 2 | 1 / 3 / 4 | 1 / 2 / 1 | — |
| Transform TOWER-ARM ↔ ARCH | No path (N) | 6 moves, 4 of them convex (N) | 9 moves each way, all checked, power continuous (N) | Both shapes traceable (N) | — |
| Active-module fraction | Sleeves and base only | 100 % | 100 % (passive voxels possible in a hybrid) | 100 % | ≪ 1 % |
| Most likely fatal flaw | Sliding wear + particles (sealing) | Same + convex moves | **Microfabricated switchable magnet film** | Series reliability, shape class | Same material risk as NEPL; carrier traffic |
| Credible scale today | 1 mm (sealed) | 1 mm (sealed) | 1 mm–300 µm | 1 cm (Milli-Motein) | macro |

## 3. Verdict

1. **Strongest surviving architecture for the actual objective: NEPL.** It is the only candidate that simultaneously:
   - executes general reconfiguration with physically modelled moves, reaching the same 2D state space as sliding within 0.05 %;
   - keeps power available, with a passive mover and powered actuators;
   - tolerates micrometre particles, with linear rather than exponential degradation;
   - carries shear through pins and tension through a switchable magnetic circuit;
   - avoids sliding contacts.
   
   Its single most likely fatal flaw is a materials question (a switchable magnet film), not a physics question. It is credible at 300 µm and marginal at 100 µm.
2. **Strongest alternative: ISL-PE**, which stays the Track-A path. It needs no undemonstrated material but is sealed, sliding and restricted in shape. For reducing the active fraction, the **NEPL + ACPL hybrid** (active skin, passive bulk) is the strongest Track-B alternative.
3. **Comparison with ISL-PE under equal assumptions:**
   - NEPL reaches 62,227 configurations versus 19 from the same start.
   - It completes the TOWER-ARM ↔ ARCH transformation, which ISL cannot.
   - It trades ISL's material-limited tension for about 50–100 kPa.
   - It needs every module to be active unless hybridised.

Limitations are stated in GENERALITY.md: the 2D bounded searches are not proofs.
