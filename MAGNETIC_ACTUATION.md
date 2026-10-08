# MAGNETIC_ACTUATION — electromagnetic and magnetic propulsion and attachment (session 3)

**Evidence labels:**
- VERIFIED LITERATURE: title, venue and number confirmed from a primary source. **No item reaches this level**: the proxy blocked full text again.
- LITERATURE-SNIPPET: number seen only in a search snippet. Unverified.
- MATHEMATICAL DERIVATION
- NUMERICAL SIMULATION
- ENGINEERING HYPOTHESIS
- UNVERIFIED SPECULATION

**Code:**
- `sims/s3/magnetic.py` → `results/s3_magnetic.md`
- `sims/s3/mag_pivot.py` → `results/s3_mag_pivot.md`
- `sims/s3/nepl_design.py` → `results/s3_nepl_design.md`

## 1. Literature inputs

All values below are LITERATURE-SNIPPET.

| Quantity | Value | Source |
|---|---|---|
| Sputtered NdFeB thick films (Dempsey, Institut Néel) | Br ≈ 1.3–1.4 T, Hc ≈ 1.6–2 T; up to 50 µm; requires ≥ 650 °C anneal | arXiv cond-mat/0703785; Dempsey 2021 trade article |
| Electroplated CoPt (Arnold group, UF) | Hc ≤ 850–1000 kA/m, Br ≤ 0.8 T, up to 100 µm | UF IMG listings |
| CoPtP pulse-reverse plating | Hc 268 kA/m, Br 0.4 T at ~3 µm | cora.ucc.ie/handle/10468/7756 |
| Parylene- or wax-bonded NdFeB powder | Br 0.36–0.69 T | doi:10.1109/MEMSYS.2012.6170220 |
| Multilayer microcoil (150–300 µm OD) | failed at 3600 A/mm² (3.6×10⁹ A/m²) DC; safe 610 A/mm² (unit conflict in source) | ebuah.uah.es/dspace/handle/10017/64267 |
| Microcoil failure mode | thermal (track melting), not electromigration | Moulin et al., Microsyst. Technol. 2007 |
| EPM modules | Pebbles 12 mm; Kubits 25 mm (EPM pivoting cubes, prior art); Milli-Motein 1 cm EPM wobble motor, 2.6 W while reconfiguring | — |
| Sub-mm EPM | No demonstration found. A patent claims 34 mm³ and on/off ratio 784 (US10971292). | — |
| **Gap** | **No microfabricated semi-hard (switchable) magnet film with a square loop was found.** | — |

## 2. Findings

### M1 — Lorentz drive (stator coils push a passive permanent-magnet mover). MATHEMATICAL DERIVATION. **Rejected for lattices.**
- With heating limited to 2×10⁵ W/m², the drive gives 0.1–1.7 kPa at 1–5 µm gaps.
- Cost: 1.2 mW per 100 µm face and about **40 µJ per lattice step**, roughly 10³× the electrostatic face drive.

### M2 — Why Lorentz drive fails. MATHEMATICAL DERIVATION.
- Thrust ~ K·B_PM, while permanent-magnet-to-magnet and magnet-to-iron forces ~ B_PM²/μ₀.
- Their ratio is μ₀K/B_PM = B_coil/B_PM ≈ 0.04–0.11 at every size up to 10 mm.
- So any uncancelled magnet–magnet cogging or magnet–iron friction exceeds the coil drive. This is the quantitative reason "distributed electromagnetic motor" designs with sustained coil current do not scale.

### M3 — Electropermanent (EPM) switching. MATHEMATICAL DERIVATION. **Revises session-1 claim N1.**
- Switching cost scales as E ∝ Hc²·pole·t_pulse and ΔT ∝ (Hc/pole)²·t_pulse.
- With poles ≤ 50 µm and 1 µs pulses:
  - Hc ≈ 20 kA/m: about 36 nJ per pole, ΔT ≈ 2 K.
  - Hc ≈ 3 kA/m: about 0.8 nJ per pole.
- AlNiCo (50 kA/m) overheats at small poles. Every material fails at 5 µm poles (10 µm modules).
- **N1 is retracted:** EPMs are not physically excluded at 100–300 µm. The binding constraint is now a material that has not been demonstrated (a microfabricated semi-hard film) plus a pulsed coil current of 1–2×10¹⁰ A/m², which is above the DC failure value found.

### M4 — EPM-switched toothed reluctance stepper with sliding faces. NUMERICAL SIMULATION (FD magnetostatics). **Falsified.**
- τ_max/p_normal = 0.14–0.19 across g/λ = 0.025–0.2. At fixed offset the ratio is mesh-converged at 0.102–0.107 while the absolute stresses converge slowly.
- Absolute stresses are 1.3–4.4 kPa of shear under a 7–31 kPa clamp.
- The mover is friction-locked unless μ < ~0.15. Literature: polysilicon steady-state friction is 0.20 ± 0.05, rising to 0.45 with wear (SNIPPET).
- **Kill parameter: τ/p versus μ.** Magnetic attraction cannot be phase-cancelled the way electrostatic attraction can (session 1, S2).

### M5 — EPM attachment through a particle-propped gap. MATHEMATICAL DERIVATION (magnetic circuit, upper bound).
- B ≈ Br·l_m / (l_m + 2g), so the degradation is **linear in gap/magnet length, not exponential**.
- At 100 µm the attachment keeps about 125 kPa (ideal) with a 5 µm particle.
- This is the most particle-tolerant switchable attachment found in three sessions. Contrast AUDIT N11: electrostatic thrust falls ~exp(−k·d).

### M6 — Neighbour-driven push–pull EPM pivot. NUMERICAL SIMULATION (2D magnetic-charge model).

The model was validated against the bar-to-bar contact limit (0.94 of Br²/2μ₀) and checked for discretisation (2.3 % change).

| L | 90° push+pull margin | 90° pull-only | 180° push+pull | 180° pull-only | Hinge load (90°) |
|---|---|---|---|---|---|
| 1 mm | 180 | 41 | 80 | 34 | 11 mN |
| 300 µm | 73 | 16 | 32 | 14 | 1.0 mN |
| 100 µm | 8.9 | 2.0 | 4.0 | 1.7 | 112 µN |
| 10 µm | 0.1 | 0.0 | 0.0 | 0.0 | — |

Margins are minimum torque over the whole swing divided by humid peel torque plus gravity, in the 2D model with depth = L. A 3D finite-depth derate of ×0.5 is an assumption, not computed. The scaling law is margin ∝ L² against adhesion (MATHEMATICAL DERIVATION).

- **Mechanism:** the moving module is **passive**. Force comes from the stationary neighbours' switched magnets, which is the user's original "neighbours are the motor" idea in a form that survives the numbers.
- **Friction:** pivoting is rolling about an edge, so friction acts as the no-slip constraint rather than a loss. This is how the method avoids M4's friction lock.
- **Hinge requirement:** push forces lift the mover off the pivot during the first half of the swing. A hinge holding 112–125 µN (at 100 µm) is required. An edge EPM strip provides about 1.6× that at every size (`nepl_design.py`).
- **Prior art:** Kubits (EPM pivoting cubes, 25 mm, RA-L 2020) and M-Blocks (edge magnets). What is new here is the **micro-scale feasibility analysis and the passive-mover / neighbour-actuated formulation**. Novelty of the mechanism itself is **not claimed**.

## 3. Cross-talk, heat, environment

- **Cross-talk:** an EPM in the off state shunts its flux internally, so idle faces do not interact (Knaian design principle, title-level only). By contrast, permanent-magnet faces always interact, which is the M2 failure.
- **Heat:** adiabatic ΔT is about 2 K per 1 µs switch at Hc = 20 kA/m and 50 µm poles. At swarm level, 145 nJ per move at 100 µm.
- **Environment:**
  - Humidity does not affect magnetic forces; it only raises adhesion, which is in the margins.
  - **New risk: ferrous debris is attracted to on-state magnets.** UNVERIFIED SPECULATION about magnitude, needs testing.
  - Above ~80–150 °C, NdFeB coercivity loss may be a problem. Not quantified here.

## 4. What remains unverified

- Every literature number (snippet level).
- The 3D derate factor.
- A microfabricated semi-hard magnet film.
- Pulsed microcoil limits.
- Landing dynamics and braking.
- Ferrous-dust accumulation.
- Fatigue of pins and pole pieces under about 10⁶ landings.
