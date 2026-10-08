# Session 3 — NEPL design budgets (MATHEMATICAL DERIVATION; numbers marked ASSUMED are engineering hypotheses)

## 1. Attachment pressure with contaminants (closed-circuit EPM, Br = 1.0 T, pole fraction 0.5, x0.5 leakage derate ASSUMED)

| L | clean (0.1 um) | 1 um particle | 5 um particle | 15 um lint fibre |
|---|---|---|---|---|
| 1000 um | 99 kPa | 98 kPa | 94 kPa | 85 kPa |
| 300 um | 99 kPa | 96 kPa | 84 kPa | 62 kPa |
| 100 um | 98 kPa | 90 kPa | 62 kPa | 31 kPa |

Structural use (session-1 S5 formula): 1 N at the tip of a 10 cm arm needs p = 6Fl/h^3: 75 kPa for a 2 cm square section, 600 kPa for 1 cm. NEPL tension capacity (~50 kPa derated) supports ~1 N at 10 cm only for sections >= ~2.3 cm, or lighter loads. Weaker than ISL interlocks, but switchable and particle-tolerant.

## 2. Shear pins (Si, conical, diameter 0.2 L, design shear strength 300 MPa)

- L = 1000 um: pin shear capacity 9.42e+03 mN = 9.42 MPa face-equivalent; lateral capture range with 30 deg cone of height 0.1 L: +-57.7 um
- L = 300 um: pin shear capacity 848 mN = 9.42 MPa face-equivalent; lateral capture range with 30 deg cone of height 0.1 L: +-17.3 um
- L = 100 um: pin shear capacity 94.2 mN = 9.42 MPa face-equivalent; lateral capture range with 30 deg cone of height 0.1 L: +-5.8 um

Pins remove ISL's slip-plane weakness (shear ~9.4 MPa face-equivalent >> 0.1 MPa need). They forbid sliding moves, which NEPL never uses.

## 3. Electrical contacts clamped by the magnet (Holm, Au, H = 1 GPa, x10 film factor ASSUMED; 4 pads per face, each 5 % of face area)

| L | force per pad (clean) | R per pad | face R (4 pads parallel) | reach h_max (hops) at 10 nW, 3 V, G = 5 |
|---|---|---|---|---|
| 1000 um | 9937 uN | 0.06 ohm | 0.015 ohm | 34119 |
| 300 um | 892 uN | 0.21 ohm | 0.052 ohm | 18676 |
| 100 um | 98 uN | 0.62 ohm | 0.155 ohm | 10764 |

The magnet supplies 10^1-10^4 uN contact force that electrostatic attachment cannot, giving sub-ohm landed contacts. Contacts are made and broken cold (power to that face switched off during transit), avoiding hot-switching wear.

## 4. Hinge capture (edge EPM strips; required 112-125 uN at 100 um from mag_pivot.py)

- L = 1000 um: edge strip (0.1 L x L, Br 1 T, x0.5 derate) holds ~19894 uN vs 12500 uN required -> margin 1.6
- L = 300 um: edge strip (0.1 L x L, Br 1 T, x0.5 derate) holds ~1790 uN vs 1120 uN required -> margin 1.6
- L = 100 um: edge strip (0.1 L x L, Br 1 T, x0.5 derate) holds ~199 uN vs 125 uN required -> margin 1.6

Margin ~1.6 at all sizes: hinge capture is geometric (same scaling as the push), so it neither improves nor fails with size. A mechanical knuckle hook (Si, 15 mN-class at 100 um) is the fallback.

## 5. Landing impact (inertial pivot, from cycle_compare.py)

- L = 1000 um: landing energy 4.62e+03 nJ -> edge speed ~1.99 m/s if undamped. Requires braking: switch the pull off at ~60 deg (reverse-pulse) and rely on squeeze-film damping in the last ~1 um (ESTIMATE; rarefied-gas effects below ~0.1 um reduce it).
- L = 300 um: landing energy 125 nJ -> edge speed ~1.99 m/s if undamped. Requires braking: switch the pull off at ~60 deg (reverse-pulse) and rely on squeeze-film damping in the last ~1 um (ESTIMATE; rarefied-gas effects below ~0.1 um reduce it).
- L = 100 um: landing energy 4.62 nJ -> edge speed ~1.99 m/s if undamped. Requires braking: switch the pull off at ~60 deg (reverse-pulse) and rely on squeeze-film damping in the last ~1 um (ESTIMATE; rarefied-gas effects below ~0.1 um reduce it).

Landing speed is size-independent (torque ~L^3, energy ~L^3, mass ~L^3), so braking is needed at every scale.


## 6. Energy and heat for a garment-scale reconfiguration

- L = 300 um, 10 cm^3 object: 3.70e+05 modules; reshaping 10 % of them by 10 moves each = 3.70e+05 moves, 0.485 J of switching energy (battery 15 Wh = 54 kJ).
- L = 100 um, 10 cm^3 object: 1.00e+07 modules; reshaping 10 % of them by 10 moves each = 1.00e+07 moves, 1.45 J of switching energy (battery 15 Wh = 54 kJ).

## 7. Fabrication requirements (ENGINEERING HYPOTHESIS)
- Sputtered NdFeB (Br ~1.3-1.4 T, up to 50 um thick, 650 C anneal; Dempsey/Grenoble, SNIPPET) -> magnets must be made before CMOS or on a separate die (chiplet assembly).
- Switchable (semi-hard, Hc <= 20 kA/m, square loop) microfabricated film: NOT FOUND in literature search -> the single most uncertain material.
- Electroplated Cu planar/multilayer coils; pulsed 1 us at 1-2e10 A/m^2 (above the 3.6e9 A/m^2 DC failure value found, SNIPPET; adiabatic dT ~2 K computed).
- DRIE Si bodies, conical pins, NiFe pole pieces; 6-face assembly (folding or die stacking). Credible at 1 mm, plausible at 300 um, unproven at 100 um.

