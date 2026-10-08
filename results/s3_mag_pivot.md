# Session 3 — neighbour-driven EPM push-pull pivot (NUMERICAL SIMULATION, 2D magnetic-charge model)

Validation: two long bars end-to-end (gap 0.01 L) give -374 kPa (negative = attraction) vs analytic contact limit Br^2/2mu0 = 398 kPa (Br = 1 T); |ratio| 0.94. Thin face strips (width/thickness ~5) are far weaker than this limit, which is why EPM designs use pole pieces.

Discretisation check (20 vs 40 charges per sheet): max relative torque change 2.3 % (where torque is non-negligible).

## L = 1000 um (Br = 1.0 T; required torque = humid peel 4.07e-09 + gravity 1.62e-08 = 2.02e-08 N m)

| mode | min torque over 1-89 deg (N m) | angle of min | torque margin | min force into pivot (N) | hinge must hold (N) |
|---|---|---|---|---|---|
| push+pull | 3.65e-06 | 45 | 180.2 | -1.12e-02 | 1.12e-02 |
| pull only | 8.20e-07 | 1 | 40.5 | 8.96e-04 | 0.00e+00 |
| push only | 8.20e-07 | 89 | 40.5 | -1.21e-02 | 1.21e-02 |

## L = 300 um (Br = 1.0 T; required torque = humid peel 1.22e-09 + gravity 1.31e-10 = 1.35e-09 N m)

| mode | min torque over 1-89 deg (N m) | angle of min | torque margin | min force into pivot (N) | hinge must hold (N) |
|---|---|---|---|---|---|
| push+pull | 9.84e-08 | 45 | 72.8 | -1.01e-03 | 1.01e-03 |
| pull only | 2.21e-08 | 1 | 16.4 | 8.06e-05 | 0.00e+00 |
| push only | 2.21e-08 | 89 | 16.4 | -1.09e-03 | 1.09e-03 |

## L = 100 um (Br = 1.0 T; required torque = humid peel 4.07e-10 + gravity 1.62e-12 = 4.09e-10 N m)

| mode | min torque over 1-89 deg (N m) | angle of min | torque margin | min force into pivot (N) | hinge must hold (N) |
|---|---|---|---|---|---|
| push+pull | 3.65e-09 | 45 | 8.9 | -1.12e-04 | 1.12e-04 |
| pull only | 8.20e-10 | 1 | 2.0 | 8.96e-06 | 0.00e+00 |
| push only | 8.20e-10 | 89 | 2.0 | -1.21e-04 | 1.21e-04 |

## L = 10 um (Br = 1.0 T; required torque = humid peel 4.07e-11 + gravity 1.62e-16 = 4.07e-11 N m)

| mode | min torque over 1-89 deg (N m) | angle of min | torque margin | min force into pivot (N) | hinge must hold (N) |
|---|---|---|---|---|---|
| push+pull | 3.65e-12 | 45 | 0.1 | -1.12e-06 | 1.12e-06 |
| pull only | 8.20e-13 | 1 | 0.0 | 8.96e-08 | 0.00e+00 |
| push only | 8.20e-13 | 89 | 0.0 | -1.21e-06 | 1.21e-06 |

## Torque and pivot-force profile, push+pull, L = 100 um

| angle (deg) | torque (N m) | force into pivot (N) |
|---|---|---|
| 1 | 1.36e-08 | -1.12e-04 |
| 9 | 7.73e-09 | -6.32e-05 |
| 17 | 5.56e-09 | -4.11e-05 |
| 25 | 4.49e-09 | -2.65e-05 |
| 33 | 3.92e-09 | -1.50e-05 |
| 41 | 3.68e-09 | -4.85e-06 |
| 49 | 3.68e-09 | 4.85e-06 |
| 57 | 3.92e-09 | 1.50e-05 |
| 65 | 4.49e-09 | 2.65e-05 |
| 73 | 5.56e-09 | 4.11e-05 |
| 81 | 7.73e-09 | 6.32e-05 |
| 89 | 1.36e-08 | 1.12e-04 |

## 180-deg convex pivot around a single neighbour (push from its top, pull from its side)

| L | mode | min torque | angle | margin | hinge must hold (N) |
|---|---|---|---|---|---|
| 1000 um | push+pull | 1.62e-06 | 90 | 80.2 | 1.25e-02 |
| 1000 um | pull only | 6.86e-07 | 62 | 33.9 | 1.33e-03 |
| 300 um | push+pull | 4.38e-08 | 90 | 32.4 | 1.12e-03 |
| 300 um | pull only | 1.85e-08 | 62 | 13.7 | 1.20e-04 |
| 100 um | push+pull | 1.62e-09 | 90 | 4.0 | 1.25e-04 |
| 100 um | pull only | 6.86e-10 | 62 | 1.7 | 1.33e-05 |
| 10 um | push+pull | 1.62e-12 | 90 | 0.0 | 1.25e-06 |
| 10 um | pull only | 6.86e-13 | 62 | 0.0 | 1.33e-07 |

2D model with depth = L. A finite-depth 3D strip is weaker (estimate x0.5, UNVERIFIED), so 100 um margins of 2-9 become ~1-4.5.


Scaling (MATHEMATICAL DERIVATION): magnetic torque ~ (Br^2/mu0) L^3 (same geometry), peel torque ~ F_adh L ~ L, gravity torque ~ rho g L^4. Torque margin vs adhesion therefore scales as L^2, and vs gravity as 1/L.

