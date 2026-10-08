# MECHANICAL_CYCLE — complete movement sequence, hinge, pins, landing (session 4)

**Code:**
- `sims/s4/pins.py` → `results/s4_pins.md`
- `sims/s4/cycle_dynamics.py` → `results/s4_cycle_dynamics.md`
- `sims/s4/demag_contacts.py`: contacts

Evidence: NUMERICAL SIMULATION / MATHEMATICAL, as marked.

## Sequence (90° pivot of mover M from source S onto destination D)

| # | Step | Mechanism | Finding |
|---|---|---|---|
| 1 | Attached | M–S faces clamped by EPMs; pins seated; pads touching | Clamp only **2 µN at 100 µm** (NUMERICAL) |
| 2 | Release | M's other faces OFF; S switches to repel, D to attract | Each switch costs 1.3–5 µJ and 0.65–1.3 A **through the same weak contacts** (SWITCHING_AND_THERMALS.md) |
| 3 | Support | The pivot edge must stay seated | In the first ~3–9° **no neighbour state** gives positive torque while pressing M into its pivot (`cycle_dynamics.py`, hinge-free schedule). Departure therefore needs a **captive hinge** holding 0.13–0.17 µN at 100 µm (×s² at larger L). |
| 4 | Torque | Magnetic push/pull | 100 µm: start torque = 0.05–0.06 × humid peel, so **it cannot start**. Larger sizes in MAGNETIC_CIRCUIT.md. |
| 5 | Rotation | Rigid rotation about the edge; I = (2/3)mL² | No dead zones once started. Air damping is negligible (rotational damping time ~85 ms ≫ 5–30 ms transit). |
| 6 | Deceleration | Braking state available (most-negative-torque table) | Not needed: landing edge speed is 0.24–0.25 m/s (scale-invariant) with the realistic torques, below the ~0.3–0.5 m/s pin-fracture limit (R3: 2–4 GPa at 2 m/s ∝ v). **Session 3's 2 m/s came from its overestimated torque.** |
| 7 | Arrival | Pins enter sockets along the arc | Collision-free for every pivot edge with a 14→6 µm taper (NUMERICAL). |
| 8 | Electrical contact | Pads re-touch; cold contact | Contact force 0.25 µN per pad gives R ≈ 1.2–12 Ω. |
| 9 | Re-lock | D and M switch to ATTACH | Again requires pulses through those contacts. |
| 10 | Load transfer | Shear through pins; tension through magnetic clamp | Tension capacity is 0.2 kPa, so **structures cannot carry meaningful tension.** Pins carry shear but cannot resist tension. |

## Pins: orientation and kinematics

- **Kinematics:** collision-free withdrawal and insertion for pins 20–80 µm from the pivot edge. The taper clearance (1–5 µm) exceeds the arc's lateral sweep (≤ 1.5 µm).
- **Orientation:** a single pin/socket pair mates at only one relative rotation. Identical modules need a chiral 4-pin + 4-socket pinwheel (MATHEMATICAL proof in `pins.py`). That fits only if the coil band shrinks to ±18 µm, so the bars drop to 9.5 µm and torque falls by a further ~×0.6.
- **Impact:** at 0.25 m/s, R3's scaling gives ~0.25–0.5 GPa at the pin tip. That is below fracture, but fatigue over ~10⁶ landings is untested.

## Hinge (unresolved at every scale)

- A captive hinge is needed only for the first few degrees of departure, but it is needed at every scale.
- Reviewer R3: any captured hinge on identical modules either protrudes and blocks attachment, or needs a handed layout. A chiral, 90°-symmetric arrangement solved the analogous pin problem. **A corresponding edge-hinge design was not found or tested.**
- **Status: UNRESOLVED engineering problem.** It needs a design and an experiment (E15).

## Stresses and friction

| Item | Value |
|---|---|
| Hinge load (strength) | Trivial: ~1 MPa on a 100 µm² knuckle (R3) |
| Hinge friction | 0.4 × F × 5 µm; included in the dynamics; negligible next to the torque deficit |
| Pin shear capacity | 9.4 MPa face-equivalent (session 3, MATH) |
| Tension | The magnetic clamp is the only tension path: 0.2 kPa at 100 µm |
