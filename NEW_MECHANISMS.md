# NEW_MECHANISMS — original candidate mechanisms (session 3)

## NEPL — Neighbour-actuated Electropermanent Pivoting Lattice

**Status: ENGINEERING HYPOTHESIS.** Supported by MATHEMATICAL DERIVATION and NUMERICAL SIMULATION. No experiment exists.

**Novelty: not claimed for the mechanism class.**
- Prior art: Kubits (EPM pivoting cubes, 25 mm), M-Blocks (edge magnets), Pebbles (EPM attachment, power and data through EPM faces).
- What this work adds:
  1. The microscale feasibility analysis: torque, hinge, energy, heat and contaminant budgets from 1 mm to 10 µm.
  2. The passive-mover formulation: only stationary neighbours act.
  3. Pin-carried shear, compatible with pivots.
  4. The finding that pivoting loses about 0.05 % of sliding's reachable set (2D, bounded).

### Operating principle
1. Each face carries an electropermanent magnet: a hard NdFeB film in parallel with a switchable semi-hard core, a planar coil and NiFe pole pieces.
2. **Attachment:** both facing EPMs on. The flux closes through the neighbour's pole pieces; up to ~100 kPa (derated) holds the faces together.
3. **Locomotion:** the mover is **passive** during transit.
   - The source neighbour S switches its contact face to **repel** the mover's face.
   - The destination neighbour D switches its face to **attract** the mover's leading face.
   - The mover pivots 90° (or 180° around a convex corner) about an edge shared with S and D.
   - Rolling about the edge makes friction the no-slip constraint, not a loss. This is how NEPL escapes the sliding reluctance stepper's friction lock (M4).
4. **Hinge capture:** edge EPM strips at the pivot edge hold against the push transient: 112–125 µN required at 100 µm, about 1.6× available.
5. **Shear strength:** a conical Si pin and socket on each face engage along the face normal at the end of the pivot. Pivots arrive and depart along the normal, so the pins never block NEPL's own moves. They do block slides.
6. **Power and data:** through pole pieces and pin contact pads clamped by the magnet. That is about 100 µN per pad at 100 µm, giving about 0.6 Ω per pad by Holm with a ×10 film factor.
   - Contacts are made and broken cold.
   - The mover needs no power in transit: nonvolatile state, and its magnets keep their set polarity.

### Geometry (at L = 300 µm, the recommended first microscale size)

| Element | Dimensions |
|---|---|
| Body | Si cube, DRIE |
| Face EPM | pole pitch ≤ 50 µm, magnet length about 0.4 L = 120 µm; NdFeB film ≤ 50 µm |
| Coil | electroplated Cu, multilayer |
| Shear pin | one per face (genderless: pin and socket in a rotationally symmetric pair); diameter 60 µm, cone 30°, capture range ±17 µm |
| Edge hinge strips | 12, each 0.1 L wide |

### Movement sequence (one 90° pivot)
1. Mover M sets its own face polarities. It is powered via S at this point.
2. M's other attachments are switched off.
3. D's top face is switched to attract and S's top face to repel, using 1 µs pulses.
4. M rotates. The inertial transit is about 64 µs at 100 µm and about 190 µs at 300 µm.
5. At about 60° D reverse-pulses to brake. Squeeze-film damping absorbs the rest (ESTIMATE).
6. The pin seats. D and M switch to attach. Electrical contact is re-made cold.

**Energy:** about 4 face switches per move: 145 nJ at 100 µm, 1.3 µJ at 300 µm.

### Force and energy budgets (from `results/s3_mag_pivot.md`, `s3_cycle_compare.md`, `s3_nepl_design.md`)

| L | 90° margin (3D-derated) | 180° margin | Attachment, clean / 5 µm particle | Pin shear | Contact R per face | Energy per move |
|---|---|---|---|---|---|---|
| 1 mm | 90 | 40 | 99 / 94 kPa | 9.4 MPa | 0.015 Ω | 14.5 µJ |
| 300 µm | 36 | 16 | 99 / 84 kPa | 9.4 MPa | 0.05 Ω | 1.3 µJ |
| 100 µm | 4.5 | 2.0 | 98 / 62 kPa | 9.4 MPa | 0.16 Ω | 145 nJ |
| 30 µm | 0.4 | 0.2 | — | — | — | — |

### Manufacturing requirements
- Sputtered NdFeB with a ≥ 650 °C anneal (literature, snippet), so magnets must be made on a separate die from the CMOS (chiplet assembly).
- Semi-hard switchable film with Hc ≤ 20 kA/m and a square loop: **not found in the literature**.
- Pulsed coils at 1–2×10¹⁰ A/m² for 1 µs.
- Six-face assembly.

Assessment: credible at 1 mm, plausible at 300 µm, unproven at 100 µm, infeasible at ≤ 30 µm (torque margin < 1).

### Failure modes, ranked
1. **No microfabricable switchable magnet material** (single most likely fatal flaw).
2. Pulsed coil failure above the 3.6×10⁹ A/m² DC failure value.
3. Landing impact: an undamped edge speed of about 2 m/s at every size could chip Si pins.
4. Ferrous-dust accumulation on on-state faces.
5. 3D derate worse than ×0.5, so 180° pivots at 100 µm fail (margin 2.0 → < 1).
6. Tensile strength (about 50 kPa derated) is too low for large cantilever loads. Needs sections ≥ 2.3 cm for 1 N at 10 cm.
7. Hinge margin of only 1.6.

### Decisive falsification experiment: E9 (EXPERIMENTS.md)
1. Fabricate a single EPM face at 1 mm and at 300 µm.
2. Measure:
   - switching with ≤ 1 µs pulses, and the coil temperature;
   - on/off attachment pressure with 0, 1, 5 and 15 µm spacers;
   - the push–pull pivot torque profile on a torsion pendulum, compared with `mag_pivot.py`.
3. Kill criteria (any one):
   - no semi-hard film with Br ≥ 0.5 T switches reliably at Hc ≤ 20 kA/m;
   - measured minimum torque < 30 % of the model;
   - attachment with a 5 µm spacer < 40 kPa at 300 µm.

### Comparison against existing alternatives
See ARCHITECTURE_COMPETITION.md.

## Mechanisms proposed and rejected this session
- **EPM-switched sliding reluctance stepper:** friction-locked (τ/p ≤ 0.19 < μ). NUMERICAL SIMULATION.
- **Neighbour Lorentz drive of permanent-magnet movers:** coil force is 4–11 % of magnet–magnet forces. MATHEMATICAL DERIVATION.
- **Rigid electrostatic zipping pivot:** torque/peel < 0.04 at 90°. MATHEMATICAL DERIVATION.

---

> **Session-4 correction (FEASIBILITY_VERDICT.md):** the NEPL margins above (4.5 / 2.0 at 100 µm) and the ~100 kPa switchable attachment assumed face-normal 1 T magnets, which a switchable material cannot hold.
> - With an integrated, buildable face (in-plane CoP bars, NiFe pole pieces, coils and pins all occupying space), the 100 µm margins are 0.022 / 0.006 and the clamp is 0.2 kPa.
> - Verdict: 100 µm infeasible (D), 300 µm C, ~0.6–1 mm B.
>
> The text above is preserved as the historical session-3 record.
