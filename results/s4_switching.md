# Session 4 — EPM switching, thermals, drivers (MATHEMATICAL DERIVATION + NUMERICAL Biot-Savart)

Material values are LITERATURE-SNIPPET (no squareness reported). k_sw = switching field / Hc (ASSUMED range 1.5-3).

Corrections after independent review R2: turns centred at true pitch; R(T) feedback (alpha = 0.0039/K, constant current); driver density 1-2 um^2 per um of gate width; flags: HEAT@1us = >150 K rise for a 1 us pulse, heat@10us likewise, DRIVER = does not fit the two-die core, J>1e11 A/m^2. Temperatures capped at 9999 K for display (i.e. melting).


## L = 100 um, coil pitch 3.0 um, metal thickness 3.0 um

| material | k_sw | N | H/A min over bar (A/m per A) | I (A) | J (A/m^2) | R (ohm) | V (V) | P (W) | L_coil (H) | dT coil 1us / 10us (K) | E 1us / 10us | driver area (um^2, 1-2 um^2/um) vs die area | crosstalk: same face / facing bar (kA/m) | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CoP (plated) | 1.5 | 18 | 8.1e+04 (centre 3.2e+05) | 0.648 | 1.08e+11 | 3.06 | 1.98 | 1.285 | 9.7e-10 | 82 / 2663 | 1.28 / 12.85 uJ | 62092-124183 vs 10952 | 3.0 / 3.9 | heat@10us DRIVER J>1e11 |
| CoP (plated) | 3.0 | 18 | 8.1e+04 (centre 3.2e+05) | 1.296 | 2.16e+11 | 3.06 | 3.97 | 5.139 | 9.7e-10 | 517 / 9999 | 5.14 / 51.39 uJ | 62092-124183 vs 10952 | 6.0 / 7.8 | HEAT@1us heat@10us DRIVER J>1e11 |
| CoNiP (plated) | 1.5 | 18 | 8.1e+04 (centre 3.2e+05) | 1.041 | 1.74e+11 | 3.06 | 3.19 | 3.319 | 9.7e-10 | 267 / 9999 | 3.32 / 33.19 uJ | 62092-124183 vs 10952 | 4.9 / 6.3 | HEAT@1us heat@10us DRIVER J>1e11 |
| CoNiP (plated) | 3.0 | 18 | 8.1e+04 (centre 3.2e+05) | 2.083 | 3.47e+11 | 3.06 | 6.37 | 13.275 | 9.7e-10 | 4190 / 9999 | 13.27 / 132.75 uJ | 62092-124183 vs 10952 | 9.7 / 12.6 | HEAT@1us heat@10us DRIVER J>1e11 |
| CoPtP (plated) | 1.5 | 18 | 8.1e+04 (centre 3.2e+05) | 2.129 | 3.55e+11 | 3.06 | 6.52 | 13.871 | 9.7e-10 | 4799 / 9999 | 13.87 / 138.71 uJ | 62092-124183 vs 10952 | 9.9 / 12.8 | HEAT@1us heat@10us DRIVER J>1e11 |
| CoPtP (plated) | 3.0 | 18 | 8.1e+04 (centre 3.2e+05) | 4.258 | 7.10e+11 | 3.06 | 13.03 | 55.484 | 9.7e-10 | 9999 / 9999 | 55.48 / 554.84 uJ | 62092-124183 vs 10952 | 19.8 / 25.7 | HEAT@1us heat@10us DRIVER J>1e11 |

## L = 100 um, coil pitch 1.5 um, metal thickness 3.0 um

| material | k_sw | N | H/A min over bar (A/m per A) | I (A) | J (A/m^2) | R (ohm) | V (V) | P (W) | L_coil (H) | dT coil 1us / 10us (K) | E 1us / 10us | driver area (um^2, 1-2 um^2/um) vs die area | crosstalk: same face / facing bar (kA/m) | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CoP (plated) | 1.5 | 36 | 1.68e+05 (centre 6.49e+05) | 0.312 | 1.04e+11 | 14.69 | 4.58 | 1.429 | 3.9e-09 | 92 / 3578 | 1.43 / 14.29 uJ | 12936-25871 vs 10952 | 2.9 / 3.8 | heat@10us DRIVER J>1e11 |
| CoP (plated) | 3.0 | 36 | 1.68e+05 (centre 6.49e+05) | 0.624 | 2.08e+11 | 14.69 | 9.16 | 5.716 | 3.9e-09 | 620 / 9999 | 5.72 / 57.16 uJ | 12936-25871 vs 10952 | 5.8 / 7.5 | HEAT@1us heat@10us DRIVER J>1e11 |
| CoNiP (plated) | 1.5 | 36 | 1.68e+05 (centre 6.49e+05) | 0.501 | 1.67e+11 | 14.69 | 7.36 | 3.691 | 3.9e-09 | 310 / 9999 | 3.69 / 36.91 uJ | 12936-25871 vs 10952 | 4.7 / 6.1 | HEAT@1us heat@10us DRIVER J>1e11 |
| CoNiP (plated) | 3.0 | 36 | 1.68e+05 (centre 6.49e+05) | 1.003 | 3.34e+11 | 14.69 | 14.73 | 14.763 | 3.9e-09 | 5867 / 9999 | 14.76 / 147.63 uJ | 12936-25871 vs 10952 | 9.3 / 12.1 | HEAT@1us heat@10us DRIVER J>1e11 |
| CoPtP (plated) | 1.5 | 36 | 1.68e+05 (centre 6.49e+05) | 1.025 | 3.42e+11 | 14.69 | 15.05 | 15.427 | 3.9e-09 | 6805 / 9999 | 15.43 / 154.27 uJ | 12936-25871 vs 10952 | 9.5 / 12.4 | HEAT@1us heat@10us DRIVER J>1e11 |
| CoPtP (plated) | 3.0 | 36 | 1.68e+05 (centre 6.49e+05) | 2.050 | 6.83e+11 | 14.69 | 30.11 | 61.706 | 3.9e-09 | 9999 / 9999 | 61.71 / 617.06 uJ | 12936-25871 vs 10952 | 19.1 / 24.8 | HEAT@1us heat@10us DRIVER J>1e11 |

## L = 300 um, coil pitch 3.0 um, metal thickness 8.0 um

| material | k_sw | N | H/A min over bar (A/m per A) | I (A) | J (A/m^2) | R (ohm) | V (V) | P (W) | L_coil (H) | dT coil 1us / 10us (K) | E 1us / 10us | driver area (um^2, 1-2 um^2/um) vs die area | crosstalk: same face / facing bar (kA/m) | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CoP (plated) | 1.5 | 53 | 8.32e+04 (centre 3.19e+05) | 0.631 | 3.94e+10 | 13.52 | 8.53 | 5.381 | 2.5e-08 | 13 / 154 | 5.38 / 53.81 uJ | 14058-28117 vs 98568 | 3.0 / 4.8 | heat@10us |
| CoP (plated) | 3.0 | 53 | 8.32e+04 (centre 3.19e+05) | 1.262 | 7.89e+10 | 13.52 | 17.06 | 21.524 | 2.5e-08 | 56 / 1434 | 21.52 / 215.24 uJ | 14058-28117 vs 98568 | 6.0 / 9.5 | heat@10us |
| CoNiP (plated) | 1.5 | 53 | 8.32e+04 (centre 3.19e+05) | 1.014 | 6.34e+10 | 13.52 | 13.71 | 13.899 | 2.5e-08 | 35 / 610 | 13.90 / 138.99 uJ | 14058-28117 vs 98568 | 4.8 / 7.6 | heat@10us |
| CoNiP (plated) | 3.0 | 53 | 8.32e+04 (centre 3.19e+05) | 2.028 | 1.27e+11 | 13.52 | 27.41 | 55.595 | 2.5e-08 | 171 / 9999 | 55.59 / 555.95 uJ | 14058-28117 vs 98568 | 9.6 / 15.3 | HEAT@1us heat@10us J>1e11 |
| CoPtP (plated) | 1.5 | 53 | 8.32e+04 (centre 3.19e+05) | 2.073 | 1.30e+11 | 13.52 | 28.02 | 58.093 | 2.5e-08 | 181 / 9999 | 58.09 / 580.93 uJ | 14058-28117 vs 98568 | 9.8 / 15.6 | HEAT@1us heat@10us J>1e11 |
| CoPtP (plated) | 3.0 | 53 | 8.32e+04 (centre 3.19e+05) | 4.147 | 2.59e+11 | 13.52 | 56.04 | 232.373 | 2.5e-08 | 1921 / 9999 | 232.37 / 2323.73 uJ | 14058-28117 vs 98568 | 19.6 / 31.2 | HEAT@1us heat@10us J>1e11 |

## L = 1000 um, coil pitch 6.0 um, metal thickness 20.0 um

| material | k_sw | N | H/A min over bar (A/m per A) | I (A) | J (A/m^2) | R (ohm) | V (V) | P (W) | L_coil (H) | dT coil 1us / 10us (K) | E 1us / 10us | driver area (um^2, 1-2 um^2/um) vs die area | crosstalk: same face / facing bar (kA/m) | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CoP (plated) | 1.5 | 90 | 4.26e+04 (centre 1.62e+05) | 1.234 | 1.23e+10 | 12.24 | 15.10 | 18.626 | 2.4e-07 | 1 / 13 | 18.63 / 186.26 uJ | 15523-31046 vs 1095200 | 3.0 / 5.3 | ok |
| CoP (plated) | 3.0 | 90 | 4.26e+04 (centre 1.62e+05) | 2.467 | 2.47e+10 | 12.24 | 30.20 | 74.503 | 2.4e-07 | 5 / 54 | 74.50 / 745.03 uJ | 15523-31046 vs 1095200 | 6.0 / 10.6 | ok |
| CoNiP (plated) | 1.5 | 90 | 4.26e+04 (centre 1.62e+05) | 1.983 | 1.98e+10 | 12.24 | 24.27 | 48.109 | 2.4e-07 | 3 / 34 | 48.11 / 481.09 uJ | 15523-31046 vs 1095200 | 4.8 / 8.5 | ok |
| CoNiP (plated) | 3.0 | 90 | 4.26e+04 (centre 1.62e+05) | 3.965 | 3.97e+10 | 12.24 | 48.53 | 192.435 | 2.4e-07 | 13 / 164 | 192.44 / 1924.35 uJ | 15523-31046 vs 1095200 | 9.7 / 17.1 | heat@10us |
| CoPtP (plated) | 1.5 | 90 | 4.26e+04 (centre 1.62e+05) | 4.053 | 4.05e+10 | 12.24 | 49.61 | 201.083 | 2.4e-07 | 14 / 174 | 201.08 / 2010.83 uJ | 15523-31046 vs 1095200 | 9.9 / 17.4 | heat@10us |
| CoPtP (plated) | 3.0 | 90 | 4.26e+04 (centre 1.62e+05) | 8.106 | 8.11e+10 | 12.24 | 99.22 | 804.332 | 2.4e-07 | 60 / 1773 | 804.33 / 8043.32 uJ | 15523-31046 vs 1095200 | 19.8 / 34.9 | heat@10us |

## Energy source for a switching pulse

- L = 100 um: 10 us pulse at k_sw = 2 needs 22.84 uJ -> local capacitor 6630 nF -> 2.88e+09 um^3 of trench capacitor = 2882.8 module volumes
- L = 300 um: 10 us pulse at k_sw = 2 needs 95.66 uJ -> local capacitor 27769 nF -> 1.21e+10 um^3 of trench capacitor = 447.2 module volumes
- L = 1000 um: 10 us pulse at k_sw = 2 needs 331.13 uJ -> local capacitor 96118 nF -> 4.18e+10 um^3 of trench capacitor = 41.8 module volumes

Conclusion: local storage cannot supply switching pulses at any size <= 1 mm with on-chip trench capacitors; pulse current must arrive through the lattice contacts in real time (see MECHANICAL_CYCLE.md / power section).

## Magnetisation-reversal time
No measured reversal time for plated CoP/CoNiP elements was found (LITERATURE gap). Domain-wall-mediated reversal over a 58 um bar at assumed wall speeds of 10-100 m/s takes 0.6-6 us; 10 us pulses are used as the conservative case. This is an UNVERIFIED ASSUMPTION.

