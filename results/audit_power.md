# AUDIT 2 — lattice power: does drop depend only on height?

Baseline R=10.0 ohm, P=1 uW, V=3 V. 'ratio' = max drop / height-only chain formula for the same height. NUMERICAL unless stated.

| case (10x10x40 tower unless stated) | max drop (V) | ratio | unpowered modules |
|---|---|---|---|
| uniform load, full footprint (S3 claim) | 2.733e-03 | 1.00 | 0 |
| 1 % of modules at 100x load (random), +99 % total power | 5.621e-03 | 2.06 | 0 |
| hotspot: 27 modules at top corner x100 | 7.472e-03 | 2.73 | 0 |
|  (reference: single column with one 100x module on top, ANALYTIC) | 1.607e-02 | 5.88 | - |
| footprint only central 2x2 of 10x10 | 7.575e-03 | 2.77 | 0 |
| footprint single corner module | 2.395e-02 | 8.76 | 0 |
| lognormal R sigma=1.0, failed contacts 0 % | 2.477e-03 | 0.91 | 0 |
| lognormal R sigma=2.0, failed contacts 0 % | 1.916e-03 | 0.70 | 0 |
| lognormal R sigma=0.0, failed contacts 10 % | 3.199e-03 | 1.17 | 0 |
| lognormal R sigma=0.0, failed contacts 30 % | 4.967e-03 | 1.82 | 6 |
| lognormal R sigma=0.0, failed contacts 60 % | 2.662e-02 | 9.74 | 463 |
| lognormal R sigma=1.0, failed contacts 30 % | 5.147e-03 | 1.88 | 7 |

Notes: lognormal cases hold the MEDIAN at R0; in a 3D lattice, spread is averaged out (ratio < 1). In a series column the expected drop scales with the MEAN R = R0 exp(sigma^2/2) (x1.65 at sigma=1, x7.4 at sigma=2) (ANALYTIC).
- single 1x1x40 column, contact failure prob 0.001: P(whole column powered) = (1-p)^40 = 0.961 (ANALYTIC); 10x10 tower survives 30 % failures with ~6 isolated modules (NUMERICAL above). Redundant paths, not height, set robustness.
- single 1x1x40 column, contact failure prob 0.01: P(whole column powered) = (1-p)^40 = 0.669 (ANALYTIC); 10x10 tower survives 30 % failures with ~6 isolated modules (NUMERICAL above). Redundant paths, not height, set robustness.
- single 1x1x40 column, contact failure prob 0.02: P(whole column powered) = (1-p)^40 = 0.446 (ANALYTIC); 10x10 tower survives 30 % failures with ~6 isolated modules (NUMERICAL above). Redundant paths, not height, set robustness.

## Resistive garment sheet (supply enters at one garment edge)

| garment R per segment | max drop in tower (V) | ratio to height-only |
|---|---|---|
| 0.01 ohm | 7.014e-04 | 1.00 |
| 1.0 ohm | 8.385e-04 | 1.20 |
| 10.0 ohm | 2.055e-03 | 2.94 |

## Two-conductor reality (ANALYTIC)
Supply and return both traverse the lattice: drop doubles (x2) for identical contact pairs; data and power share these paths.

