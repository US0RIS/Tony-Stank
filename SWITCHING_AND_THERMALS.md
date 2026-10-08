# SWITCHING_AND_THERMALS — EPM switching coil, pulses, heat, drivers (session 4)

Code:
- `sims/s4/switching.py` → `results/s4_switching.md`
- `sims/s4/demag_contacts.py` → `results/s4_demag_contacts.md`

Evidence: MATHEMATICAL DERIVATION, plus NUMERICAL 3D Biot–Savart of the actual rectangular solenoid. All materials are LITERATURE-SNIPPET (MATERIALS_DATABASE.md).

## 1. Field requirement (H, not B)

- The switching field must reach **H_sw = k_sw·Hc throughout the bar**.
- k_sw = 1.5–3 is ASSUMED, because loop squareness is unknown.
- For CoP (Hc ≈ 28 kA/m) that is 42–84 kA/m. CoNiP needs 68–135 kA/m; CoPtP 138–276 kA/m.

## 2. Field actually produced (NUMERICAL, Biot–Savart, air core)

- At 100 µm, 18 turns at 3 µm pitch: H per ampere is 3.0×10⁵ A/m/A at the bar centre but only **1.3×10⁵ A/m/A minimum** over the bar volume, at the bar ends where they enter the pole pieces.
- The design current is set by the minimum, divided by an assumed 0.8 MMF efficiency for the iron return path.
- In a real closed iron circuit the field becomes more uniform, so this is a conservative bound. An optimistic bound, uniform H = ηNI/l_bar, gives a 2.4× lower current.

## 3. Coil, pulse, heat (L = 100 µm, CoP, k_sw = 1.5–3)

| Coil | I (A) | J (A/m²) | R (Ω) | V (V) | ΔT coil, 1 µs / 10 µs | Energy, 1 µs / 10 µs |
|---|---|---|---|---|---|---|
| 3 µm pitch, 18 turns | 0.41–0.81 | 0.7–1.4×10¹¹ | 3.1 | 1.3–2.5 | 28–112 K / 246–985 K | 0.5–2 / 5–20 µJ |
| 1.5 µm pitch, 36 turns | 0.25–0.50 | 0.8–1.7×10¹¹ | 14.7 | 3.7–7.4 | 51–203 K / 447–1789 K | 0.9–3.7 / 9–37 µJ |

- Inductance is 1–4 nH, so L/R ≈ 0.3–1 ns. Inductive rise is not limiting.
- The thermal bottleneck is the 1 µm polyimide insulation (k = 0.15 W/m·K). The coil time constant is ~70 µs, so pulses ≤ 10 µs are near-adiabatic.
- Current density is 20–60× the only measured microcoil failure value found (3.6×10⁹ A/m², DC, SNIPPET). Pulsed limits are unknown.
- **Magnetisation-reversal time: no measurement found.**
  - If 1 µs suffices: heating is tolerable (28 K at k_sw = 1.5).
  - If reversal needs ≥ 10 µs: coil temperature rises by 250–1000 K per pulse. That is **unacceptable** for polyimide and probably for CoP's magnetic properties.

Larger scales (same material):
- **300 µm:** 0.55–1.1 A; ΔT 9–38 K at 1 µs, 90–360 K at 10 µs.
- **1 mm:** 1.1–2.3 A; ΔT 1–4 K at 1 µs, 10–42 K at 10 µs.

**Thermally comfortable switching therefore needs about 1 mm**, or a demonstrated sub-µs reversal.

## 4. Cross-talk and unintended switching

- An energised coil produces 1.7–4.9 kA/m at the parallel bar on the same face and 2.4–7.8 kA/m at the facing neighbour's bar (CoP/CoNiP at k_sw 1.5–3).
- That is **6–28 % of Hc**.
- Independent reviewer R1 computed the bar's open-circuit self-demagnetising field as 23–26 kA/m (N = 0.044–0.050), against Hc 28 kA/m. Our Aharoni calculation agrees: N = 0.050 and 25.8 kA/m.
- **The margin before reversal is only 2–5 kA/m. Cross-talk is the same size as that margin.** Unintended partial switching of neighbouring bars is a credible failure mode unless the loop is very square, which is unmeasured.

## 5. Energy source

| Option | Result |
|---|---|
| Local storage | 0.5–37 µJ per pulse needs 35–1100 module volumes of trench capacitor at 100 µm–1 mm. **Impossible.** |
| Through the lattice contacts in real time | Requires 0.2–0.8 A through Au pads clamped by the magnetic attachment. The integrated attachment clamp is only **~2 µN per face** at 100 µm, about 0.25 µN per pad (NUMERICAL). That gives Holm a-spots of ~9 nm, R ≈ 1.2 Ω clean or ~12 Ω with films. At 0.2–0.8 A the contact voltage exceeds the Au softening voltage (0.08 V) in essentially every configuration. **Contacts would weld or degrade.** |

Reviewer R4 independently gets 0.1–0.4 V per contact at 0.2–0.8 A (R ≈ 0.5 Ω), with spot temperatures of 400–1300 K.

## 6. Drivers

- Silicon area for the select switches and H-bridge: 31,000 µm² at 3 µm pitch versus 10,952 µm² available at 100 µm. It does not fit.
- At 1.5 µm pitch it fits (6,500 µm²) but doubles the switching energy.
- At ≥ 300 µm the drivers fit easily.

## Conclusion of this file

At 100 µm, switching is constrained on four independent axes, each beyond any demonstrated capability:
1. Pulse current density (20–60× above the measured DC failure value).
2. Unknown reversal time, which decides between 30 K and 1000 K of heating.
3. Pulse delivery through contacts that the weak clamp cannot load.
4. A demagnetisation margin smaller than the cross-talk.

**At 1 mm, items 1 and 2 relax by 10–100×. Items 3 and 4 remain material- and contact-design questions.**
