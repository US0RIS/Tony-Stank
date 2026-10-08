# Session 3 — magnetic family screening

Evidence classes: MATHEMATICAL DERIVATION (M1, M2, M3, M5), NUMERICAL SIMULATION (M4). Material values are ASSUMED unless cited in MAGNETIC_ACTUATION.md.

## M1. Lorentz drive: stator coils push a passive PM mover (MATHEMATICAL DERIVATION)

tau = (J0 Br/2k)(1-e^{-k t_m})(e^{-kg} - e^{-k(g+t_c)}); dissipation q = J0^2 rho t_c / 2 per face area.
Heat-limited: q <= q_max = 2e5 W/m^2 (transient dT ~ q t_step/(rho c L) ~ 13 K per 10 ms step at L=100 um).
Br = 0.5 T (assumed microfabricated-magnet value; range 0.3-1.2, see MAGNETIC_ACTUATION.md). Pitch optimised for each gap.

| L | t_c | t_m | gap g | best pitch | J0 (A/m^2) | tau (Pa) | power per face | energy per lattice step (v=3 mm/s) |
|---|---|---|---|---|---|---|---|---|
| 10000 um | 5.00 um | 20.0 um | 1 um | 64 um | 2.17e+09 | 1670 | 1.2e+04 mW | 4e+07 uJ |
| 10000 um | 5.00 um | 20.0 um | 5 um | 94 um | 2.17e+09 | 1217 | 1.2e+04 mW | 4e+07 uJ |
| 1000 um | 5.00 um | 20.0 um | 1 um | 64 um | 2.17e+09 | 1670 | 120 mW | 4e+04 uJ |
| 1000 um | 5.00 um | 20.0 um | 5 um | 94 um | 2.17e+09 | 1217 | 120 mW | 4e+04 uJ |
| 300 um | 5.00 um | 20.0 um | 1 um | 64 um | 2.17e+09 | 1670 | 10.8 mW | 1.08e+03 uJ |
| 300 um | 5.00 um | 20.0 um | 5 um | 94 um | 2.17e+09 | 1217 | 10.8 mW | 1.08e+03 uJ |
| 100 um | 5.00 um | 20.0 um | 1 um | 64 um | 2.17e+09 | 1670 | 1.2 mW | 40 uJ |
| 100 um | 5.00 um | 20.0 um | 5 um | 94 um | 2.17e+09 | 1217 | 1.2 mW | 40 uJ |
| 10 um | 0.50 um | 2.0 um | 1 um | 13 um | 6.86e+09 | 291 | 0.012 mW | 0.04 uJ |
| 10 um | 0.50 um | 2.0 um | 5 um | 40 um | 6.86e+09 | 101 | 0.012 mW | 0.04 uJ |

Electrostatic face drive for comparison (AUDIT 1): ~5.7 kPa at 15-40 nJ per step (sealed, 100 nm gap), ~1 kPa at a 5 um gap.

## M2. Coil force vs permanent-magnet interactions (MATHEMATICAL DERIVATION)

Lorentz thrust ~ K B_PM (K = J t_c sheet current); PM-PM or PM-iron interaction ~ B_PM^2/mu0. Ratio = mu0 K / B_PM = B_coil / B_PM.

| L | K at q_max (A/m) | B_coil = mu0 K | ratio to B_PM = 0.12 T (field at coil) |
|---|---|---|---|
| 10000 um | 1.08e+04 | 13.63 mT | 0.114 |
| 1000 um | 1.08e+04 | 13.63 mT | 0.114 |
| 300 um | 1.08e+04 | 13.63 mT | 0.114 |
| 100 um | 1.08e+04 | 13.63 mT | 0.114 |
| 10 um | 3.43e+03 | 4.31 mT | 0.036 |

Consequence: coil-driven (Lorentz) thrust is 1-10 % of the static forces between the PMs it acts on and any PM or iron on other faces. Any uncancelled PM-PM cogging or PM-iron attraction (friction) exceeds the drive. Lorentz drive of PM movers is REJECTED for lattices in which neighbouring faces also carry magnets, at all sizes <= 1 mm.

## M3. EPM switching cost per pole (MATHEMATICAL DERIVATION)

Pole size = min(L/2, 50 um); switching field = 2 Hc; 1 us pulse; copper fill 0.3. J ~ Hc/pole; E ~ Hc^2 pole t; adiabatic dT ~ J^2 rho t / c_v.

| L | pole | material (Hc) | J (A/m^2) | E per switch | adiabatic dT | verdict |
|---|---|---|---|---|---|---|
| 10000 um | 50 um | AlNiCo-5 (~50 kA/m) | 5.33e+10 | 227 nJ | 14 K | FAILS (heating) |
| 10000 um | 50 um | FeCrCo / CoNiP film (~20 kA/m, ASSUMED) | 2.13e+10 | 36.3 nJ | 2.24 K | OK |
| 10000 um | 50 um | semi-hard 'Remendur-class' (~3 kA/m, ASSUMED) | 3.20e+09 | 0.816 nJ | 0.0505 K | OK |
| 1000 um | 50 um | AlNiCo-5 (~50 kA/m) | 5.33e+10 | 227 nJ | 14 K | FAILS (heating) |
| 1000 um | 50 um | FeCrCo / CoNiP film (~20 kA/m, ASSUMED) | 2.13e+10 | 36.3 nJ | 2.24 K | OK |
| 1000 um | 50 um | semi-hard 'Remendur-class' (~3 kA/m, ASSUMED) | 3.20e+09 | 0.816 nJ | 0.0505 K | OK |
| 300 um | 50 um | AlNiCo-5 (~50 kA/m) | 5.33e+10 | 227 nJ | 14 K | FAILS (heating) |
| 300 um | 50 um | FeCrCo / CoNiP film (~20 kA/m, ASSUMED) | 2.13e+10 | 36.3 nJ | 2.24 K | OK |
| 300 um | 50 um | semi-hard 'Remendur-class' (~3 kA/m, ASSUMED) | 3.20e+09 | 0.816 nJ | 0.0505 K | OK |
| 100 um | 50 um | AlNiCo-5 (~50 kA/m) | 5.33e+10 | 227 nJ | 14 K | FAILS (heating) |
| 100 um | 50 um | FeCrCo / CoNiP film (~20 kA/m, ASSUMED) | 2.13e+10 | 36.3 nJ | 2.24 K | OK |
| 100 um | 50 um | semi-hard 'Remendur-class' (~3 kA/m, ASSUMED) | 3.20e+09 | 0.816 nJ | 0.0505 K | OK |
| 10 um | 5 um | AlNiCo-5 (~50 kA/m) | 5.33e+11 | 22.7 nJ | 1.4e+03 K | FAILS (heating) |
| 10 um | 5 um | FeCrCo / CoNiP film (~20 kA/m, ASSUMED) | 2.13e+11 | 3.63 nJ | 224 K | FAILS (heating) |
| 10 um | 5 um | semi-hard 'Remendur-class' (~3 kA/m, ASSUMED) | 3.20e+10 | 0.0816 nJ | 5.05 K | FAILS (heating) |

Revision of session-1 claim N1: session 1 assumed AlNiCo coercivity, a 20 us pulse and a whole-module coil, and concluded 'EPM impossible below ~1 mm'. With poles of <= 50 um and 1 us pulses the energy per switch is nJ-scale; the binding constraint is the adiabatic temperature rise, which is acceptable for Hc <= ~20 kA/m at 5 um poles. The open question moves from physics to MATERIALS: microfabricated semi-hard films with square loops and stable remanence at 1-10 um thickness (ENGINEERING HYPOTHESIS, unverified).

## M4. EPM-switched toothed reluctance stepper between faces (NUMERICAL SIMULATION, FD magnetostatics)

Linear iron (mu_r = 1000), tooth fraction 0.4, tooth height = pitch/2. Stresses normalised to the aligned-gap pressure B0^2/2mu0 with B0 = mu0 MMF/g. Columns: maximum tangential stress over offset, normal stress at that offset, ratio, and the friction coefficient mu* below which the mover can slide.

| g/lam | tau_max (norm) | p at tau_max (norm) | tau/p = mu* |
|---|---|---|---|
| 0.025 | 0.020 | 0.107 | 0.188 |
| 0.05 | 0.026 | 0.142 | 0.183 |
| 0.1 | 0.035 | 0.197 | 0.176 |
| 0.2 | 0.069 | 0.486 | 0.143 |

Mesh check (g/lam = 0.05, s = lam/8): tau -0.0228 -> -0.0266, p 0.2124 -> 0.2568 (coarse -> fine).

Absolute stresses, with the gap flux density limited by iron saturation in the teeth (B_tooth <= 1.0 T for NiFe, so B0 <= ~0.4 T with tooth fraction 0.4):

- B0 = 0.4 T -> B0^2/2mu0 = 64 kPa.
- g/lam = 0.025: tau_max ~ 1.3 kPa with normal clamp 6.8 kPa; slides only if mu < 0.19
- g/lam = 0.05: tau_max ~ 1.7 kPa with normal clamp 9.0 kPa; slides only if mu < 0.18
- g/lam = 0.1: tau_max ~ 2.2 kPa with normal clamp 12.5 kPa; slides only if mu < 0.18
- g/lam = 0.2: tau_max ~ 4.4 kPa with normal clamp 30.9 kPa; slides only if mu < 0.14

Interpretation: the reluctance stepper converts PM energy (switched, not sustained, by the coil) into 5-40 kPa of tangential stress, comparable to or above the electrostatic drive, but always with a LARGER normal clamp: tau/p < ~0.2-0.4. With dry Si/SiO2 friction mu ~ 0.2-0.6 the mover is friction-locked unless (a) a low-friction coating (mu < ~0.15) or rolling/flexure guidance is used, or (b) a balancing face on the opposite side cancels the normal force. KILL PARAMETER: tau/p vs mu.

## M5. EPM attachment through a particle-propped gap (MATHEMATICAL DERIVATION, magnetic circuit)

Closed circuit through the neighbour's pole pieces: B ~ Br l_m / (l_m + 2 g mu_rec), pressure = B^2/2mu0 over pole area (pole fraction 0.5). Contrast: electrostatic stress across a propped gap falls ~exp(-k d) (AUDIT 1).

| L | l_m | Br | particle-propped gap | B | pressure (face-averaged) |
|---|---|---|---|---|---|
| 1000 um | 400 um | 1.0 T | 0.1 um | 1.00 T | 199 kPa |
| 1000 um | 400 um | 1.0 T | 1.0 um | 0.99 T | 197 kPa |
| 1000 um | 400 um | 1.0 T | 5.0 um | 0.97 T | 189 kPa |
| 300 um | 120 um | 1.0 T | 0.1 um | 1.00 T | 198 kPa |
| 300 um | 120 um | 1.0 T | 1.0 um | 0.98 T | 192 kPa |
| 300 um | 120 um | 1.0 T | 5.0 um | 0.92 T | 168 kPa |
| 100 um | 40 um | 1.0 T | 0.1 um | 0.99 T | 197 kPa |
| 100 um | 40 um | 1.0 T | 1.0 um | 0.95 T | 180 kPa |
| 100 um | 40 um | 1.0 T | 5.0 um | 0.79 T | 125 kPa |
| 10 um | 4 um | 1.0 T | 0.1 um | 0.95 T | 180 kPa |
| 10 um | 4 um | 1.0 T | 1.0 um | 0.66 T | 86 kPa |
| 10 um | 4 um | 1.0 T | 5.0 um | 0.28 T | 15 kPa |

This is an upper bound (no leakage, no saturation, ideal keeper). Magnetic attachment degrades ~linearly with gap/l_m rather than exponentially: it is the only switchable attachment found that keeps ~100 kPa with micrometre particles at L >= 100 um. At L = 10 um, a 5 um particle halves B (pressure -75 %).

