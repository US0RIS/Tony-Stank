# AUDIT 1 — electrostatic face motor under realistic conditions

Evidence class per section: NUMERICAL (FD), ANALYTIC (closed form), or literature (cited).

Ideal S2 surface-potential tau_max at 50 V, g=1 um, lam=3.3 um: 12.23 kPa

## 1. Full dielectric stack (NUMERICAL)

| case | t_c / eps_c | t_ox | tau_max (kPa) | tau at p=0 (kPa) | ratio to ideal | max |E| air (V/um) | max |E| coating (V/um) |
|---|---|---|---|---|---|---|---|---|
| thin SiO2 coat, 1 um ox | 0.1 um / 3.9 | 1.0 um | 5.89 | 5.71 | 0.48 | 162 | 204 |
| thin SiO2 coat, 0.3 um ox | 0.1 um / 3.9 | 0.3 um | 5.45 | 5.28 | 0.45 | 162 | 305 |
| protective 0.3 um SiO2 coat | 0.3 um / 3.9 | 1.0 um | 3.61 | 3.51 | 0.30 | 75 | 134 |
| 0.1 um HfO2 coat | 0.1 um / 20.0 | 1.0 um | 6.56 | 6.33 | 0.54 | 179 | 207 |

Scale invariance (ANALYTIC): every length x0.1 and V x0.1 (5 V, 100 nm gap, 0.33 um pitch) gives identical stresses and fields; FD values above apply.

## 2. Breakdown (literature + NUMERICAL peak fields)

- Air, gaps < ~4 um: V_b ~ (65-110 V/um) x d (Slade & Taylor, Holm Conf. 2001, via secondary citation; UNVERIFIED primary). For g=1 um: V_b ~ 65-110 V between facing conductors.
- Mesh check (NUMERICAL): stresses converge within 1 %; peak fields at electrode edges do NOT converge (edge singularity of thin strips), so they are not used as the criterion:
  | nx | dz | tau (Pa) | p (Pa) | peak E air | peak E coat |
  |---|---|---|---|---|---|
  | 132 | 50.0 nm | -5936 | 1875 | 169 V/um | 206 V/um |
  | 264 | 25.0 nm | -5892 | 1845 | 161 V/um | 204 V/um |
  | 528 | 12.5 nm | -5910 | 1848 | 192 V/um | 428 V/um |
- Criterion used instead: facing electrodes of opposite phase see up to 2V = 100 V across ~1.2 um, which is inside the 65-110 V micro-gap breakdown band.
- Verdict: the 50 V / 1 um design operates AT the measured micro-gap breakdown envelope -> unsafe without margin. Derate to <= 30 V (stress x0.36) or use the scaled 5 V / 100 nm design, where peak-to-peak 10 V is below the ~12-15 V ionisation potential of O2/N2 (no avalanche possible; field emission onset needs local fields ~1e3 V/um).

## 3. Particle props the gap open (ANALYTIC, ideal formula; rigid faces)

| design | particle d | effective gap | tau_max / nominal |
|---|---|---|---|
| 50 V / 1 um / 3.3 um | 0.1 um | 1.0 um | 1.00e+00 |
| 50 V / 1 um / 3.3 um | 0.3 um | 1.0 um | 1.00e+00 |
| 50 V / 1 um / 3.3 um | 1.0 um | 1.0 um | 1.00e+00 |
| 50 V / 1 um / 3.3 um | 3.0 um | 3.0 um | 2.17e-02 |
| 5 V / 100 nm / 0.33 um | 0.1 um | 0.1 um | 1.00e+00 |
| 5 V / 100 nm / 0.33 um | 0.3 um | 0.3 um | 2.17e-02 |
| 5 V / 100 nm / 0.33 um | 1.0 um | 1.0 um | 3.53e-08 |
| 5 V / 100 nm / 0.33 um | 3.0 um | 3.0 um | 1.02e-24 |

Thrust falls ~exp(-k d): one 1 um particle eliminates the 5 V design (factor ~1e-7) and one 3 um particle removes ~99 % of the 50 V design's thrust. Contamination tolerance requires either a sealed particle-free environment or compliant faces that wrap around particles.

## 4. Wedge/bow: gap varies linearly by +-delta across the face; phase tuned for nominal gap (ANALYTIC, local-stress integration)

| delta | thrust / nominal | net normal (kPa) | sliding margin (L=100 um, humid) |
|---|---|---|---|
| 0.0 | 1.00 | 0.00 | 25.2 |
| 0.1 | 1.01 | 0.04 | 23.9 |
| 0.2 | 1.03 | 0.17 | 20.8 |
| 0.4 | 1.13 | 0.80 | 13.1 |
| 0.6 | 1.32 | 2.44 | 7.3 |

## 5. Patch potentials / trapped charge (ANALYTIC phase-error model)

A spurious surface-potential component V_p at the drive wavevector shifts the effective phase by up to asin(V_p/V), moving the operating point off p=0.

| design V | V_p | phase error (rad) | margin (L=100 um, humid) |
|---|---|---|---|
| 50 V | 0.1 V | 0.002 | 24.8 |
| 50 V | 0.5 V | 0.010 | 22.9 |
| 50 V | 2.0 V | 0.040 | 17.9 |
| 5 V | 0.1 V | 0.020 | 21.0 |
| 5 V | 0.5 V | 0.100 | 12.5 |
| 5 V | 2.0 V | 0.412 | 4.8 |

Patch potentials of 0.1-0.5 V (metal work-function variation) are harmless; volt-level trapped charge in dielectrics degrades the 5 V design several-fold (closed-loop phase control could re-null p, untested).

## 6. Energy penalty from substrate capacitance (ANALYTIC)

- 1 um oxide: C_substrate/C_gap ~ 2.7 -> step energy ~ x3.7 of S7's 4 nJ unless charge is recovered
- 0.3 um oxide: C_substrate/C_gap ~ 9.1 -> step energy ~ x10.1 of S7's 4 nJ unless charge is recovered
