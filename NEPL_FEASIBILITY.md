# NEPL_FEASIBILITY — Phase 1: reconstruction and assumption register (session 4)

## 1. Reproduction of the session-3 result

`sims/s3/mag_pivot.py` was rerun at L = 100 µm:
- 90° push+pull minimum torque / requirement = **8.92** (2D), giving 4.5 after the assumed ×0.5 derate.
- 180° = **3.97**, giving 2.0 after derate.
- Requirement = 4.09×10⁻¹⁰ N·m (humid peel 4.07 µN × L + gravity). **Reproduced exactly.**

The session-4 finite-difference solver (`sims/s4/magfd.py`) was validated against that same charge model for the legacy geometry. It agrees to within 0.3–6 % at 21°, 45° and 69°, mesh-stable from h = 1.0 to 0.6 µm (NUMERICAL). The solver is therefore trustworthy. The *geometry and material inputs* of session 3 are what fail the audit.

## 2. Assumption register (session-3 NEPL model)

Classes:
- **E** = experimentally established (primary measurement) — none in this project
- **L** = literature-derived (snippet level here)
- **X** = extrapolated
- **A** = assumed
- **U** = unknown

| # | Input | Session-3 value | Class | Audit finding |
|---|---|---|---|---|
| 1 | Face magnet remanence | Br = 1.0 T | A | No switchable microfabricated film reaches 1 T. The best switchable film found is plated CoP, Jr 0.65 T, squareness unknown (L). Br = 1 T is reachable only with **hard** films (NdFeB 1.3–1.4 T, L), which cannot be switched. **Incompatible with switching.** |
| 2 | Magnetisation direction | Normal to the face, 15 µm-thick plate | A | A semi-hard plate magnetised through its thickness has N ≈ 0.8, giving a self-field ≈ 400 kA/m ≫ Hc 28 kA/m. **Physically impossible for a switchable element.** Switchable bars must lie in-plane with pole pieces, which gives two-pole faces (MATHEMATICAL, `demag_contacts.py`). |
| 3 | Magnet volume | Strip 0.15 L × 0.8 L × L on each active face | A | The integrated layout leaves room for 2 bars of 12 × 4 × 58 µm per face, i.e. **3.3 %** of the module volume for all six faces together (`module_geometry.py`). That is about 4× less magnet per face than assumed, and the flux reaches the face only through 8 µm pole pieces. |
| 4 | Polarity reversal (push) | S switches to repel | A | A standard EPM (hard + semi-hard) switches ON/OFF only. Reversal requires an all-switchable design, which removes the high-Br hard magnet from the force path. |
| 5 | Mover passivity | Mover magnets fixed ON in transit | A | Requires the mover's switchable bars to hold remanence in open circuit and under the reverse field of a pushing neighbour. Bare-bar self-field for CoP is 25.8 kA/m against Hc 28 kA/m: **8 % margin** before any external reverse field (MATHEMATICAL). |
| 6 | Soft iron, pole pieces, leakage | none (µr = 1 everywhere) | A | Not modelled in session 3. Included in session 4. |
| 7 | 2D → 3D | ×0.5 derate | A | Unverified. Session 4 uses 2D × pole depth and states the bound separately. |
| 8 | Peel requirement | 9 bumps R = 0.5 µm, full meniscus, 4.07 µN | A | Retained as the reference load. Adhesion engineering could lower it (Track B item B4). |
| 9 | Hinge | Ideal pivot, no friction, no clearance | A | Needs a physical hinge (MECHANICAL_CYCLE.md). |
| 10 | Switching energy | 36 nJ/pole, 4 switches per move, 1 µs | X | After review R2's corrections the integrated coil needs **1.3–5 µJ per switch at 1 µs** (CoP, k_sw 1.5–3), 35–140× more. The 1 µs reversal time is unverified. |
| 11 | Pulse current density | 1–2×10¹⁰ A/m² | X | The integrated coil needs 1.1–2.2×10¹¹ A/m² at 100 µm (CoP), 30–60× the DC failure value found (3.6×10⁹, L). Heating with R(T): 82–517 K at 1 µs; melting-class at 10 µs. |
| 12 | Energy source for pulses | implicit | U | Local storage needs 35–1100 module volumes of trench capacitor, so it is **impossible**. Pulses must come through contacts. |
| 13 | Contact force for power pads | from ~100 kPa magnetic clamp | A | The integrated FD clamp is **2 µN per face (0.2 kPa)** at 100 µm (NUMERICAL), giving 0.25 µN per pad. Switching pulses of ≥ 0.2 A soften Au contacts (MATHEMATICAL, Holm). |
| 14 | Pins | single conical pin, "genderless" | A | Single pin/socket pairs mate at only one relative rotation. A chiral 4+4 pinwheel is required, which shrinks the bars to 9.5 µm (MATHEMATICAL, `pins.py`). |
| 15 | Landing | undamped ~2 m/s; braking proposed | A | Requires torque tables for braking. See MECHANICAL_CYCLE.md. |

## 3. Implicit-incompatibility findings

1. **Strong magnets vs switchability.** Session 3 put hard-magnet remanence (1 T) on switchable faces in a geometry (face-normal plates) that a switchable material cannot hold. Fixing either assumption alone already reduces the face flux by an order of magnitude.
2. **The flux return path was absent.** Real EPM faces close flux through pole pieces on the same face (two-pole faces). Their field decays over about the pole spacing, so long-range push/pull at mid-pivot is much weaker than the face-normal-sheet model implies.
3. **The coil did not occupy space** in session 3. In the integrated layout the coil, bar, pole pieces, pins, sockets, pads and vias compete for a 74 × 74 × 12 µm skin per face.
4. **The energy source was not identified** (items 12–13).

The quantitative consequences are in MAGNETIC_CIRCUIT.md, SWITCHING_AND_THERMALS.md and FEASIBILITY_VERDICT.md.
