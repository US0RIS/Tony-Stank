# Session 4 — pivot torque with buildable EPM faces, L = 100 um (NUMERICAL SIMULATION, 2D FD)

## V1. Validation vs session-3 charge model (legacy face-normal strips, Br = 1 T, non-magnetic bodies)

| angle | FD torque x depth L (N m) | charge model (N m) | ratio |
|---|---|---|---|
| 21 | 4.887e-09 | 4.939e-09 | 0.99 |
| 45 | 3.647e-09 | 3.646e-09 | 1.00 |
| 69 | 4.635e-09 | 4.939e-09 | 0.94 |

## 90 deg, CoP Jr = 0.65 T, squareness 0.8 (ASSUMED), best neighbour state per angle

| angle | driving torque (N m) | S state | D state | margin vs peel | max B in iron (T) | max reverse H in magnets (kA/m) |
|---|---|---|---|---|---|---|
| 3 | 2.43e-11 | +1 | -1 | 0.06 | 0.52 | 43 |
| 9 | 1.81e-11 | +1 | -1 | 0.04 | 0.49 | 42 |
| 15 | 1.41e-11 | +1 | -1 | 0.03 | 0.45 | 41 |
| 21 | 1.16e-11 | +1 | -1 | 0.03 | 0.39 | 41 |
| 27 | 1.04e-11 | +1 | -1 | 0.03 | 0.38 | 40 |
| 33 | 9.33e-12 | +1 | -1 | 0.02 | 0.32 | 40 |
| 39 | 9.17e-12 | +1 | -1 | 0.02 | 0.34 | 40 |
| 45 | 9.20e-12 | +1 | -1 | 0.02 | 0.30 | 40 |
| 51 | 1.02e-11 | +1 | -1 | 0.02 | 0.44 | 40 |
| 57 | 1.11e-11 | +1 | -1 | 0.03 | 0.45 | 40 |
| 63 | 1.35e-11 | +1 | -1 | 0.03 | 0.34 | 40 |
| 69 | 1.56e-11 | +1 | -1 | 0.04 | 0.31 | 40 |
| 75 | 2.08e-11 | +1 | -1 | 0.05 | 0.29 | 40 |
| 81 | 2.98e-11 | +1 | -1 | 0.07 | 0.31 | 40 |
| 87 | 5.23e-11 | +1 | -1 | 0.13 | 0.33 | 40 |

Worst-case margin 0.022 at 39 deg (requirement = humid peel + gravity = 4.09e-10 N m; hinge friction not included).

## 180 deg convex, CoP Jr = 0.65 T, squareness 0.8 (ASSUMED), best neighbour state per angle

| angle | driving torque (N m) | S state | D state | margin vs peel | max B in iron (T) | max reverse H in magnets (kA/m) |
|---|---|---|---|---|---|---|
| 5 | 2.12e-11 | +1 | +0 | 0.05 | 0.52 | 41 |
| 15 | 1.26e-11 | +1 | +0 | 0.03 | 0.48 | 40 |
| 25 | 8.07e-12 | +1 | +0 | 0.02 | 0.41 | 39 |
| 35 | 5.68e-12 | +1 | +0 | 0.01 | 0.52 | 39 |
| 45 | 3.82e-12 | +1 | +1 | 0.01 | 0.37 | 40 |
| 55 | 3.44e-12 | +1 | +1 | 0.01 | 0.49 | 40 |
| 65 | 2.63e-12 | +1 | +1 | 0.01 | 0.39 | 40 |
| 75 | 2.59e-12 | +1 | +1 | 0.01 | 0.34 | 41 |
| 85 | 2.47e-12 | +1 | +1 | 0.01 | 0.44 | 41 |
| 95 | 2.28e-12 | +1 | +1 | 0.01 | 0.43 | 41 |
| 105 | 2.59e-12 | +1 | +1 | 0.01 | 0.37 | 41 |
| 115 | 3.30e-12 | +1 | +1 | 0.01 | 0.33 | 41 |
| 125 | 4.60e-12 | +1 | +1 | 0.01 | 0.35 | 41 |
| 135 | 6.42e-12 | +1 | +1 | 0.02 | 0.26 | 41 |
| 145 | 9.39e-12 | +1 | +1 | 0.02 | 0.25 | 41 |
| 155 | 1.44e-11 | +1 | +1 | 0.04 | 0.33 | 41 |
| 165 | 2.36e-11 | +1 | +1 | 0.06 | 0.28 | 41 |
| 175 | 5.05e-11 | +1 | +1 | 0.12 | 0.21 | 40 |

Worst-case margin 0.006 at 95 deg (requirement = humid peel + gravity = 4.09e-10 N m; hinge friction not included).

## Summary (linear model: torque scales exactly as (Jr*sq)^2; other squareness values rescaled)

- 90 deg, squareness 0.8: worst margin 0.022 at 39 deg; max iron B 0.52 T; max reverse H in magnets 43 kA/m (CoP Hc ~28 kA/m, SNIPPET)
- 180 deg convex, squareness 0.8: worst margin 0.006 at 95 deg; max iron B 0.52 T; max reverse H in magnets 41 kA/m (CoP Hc ~28 kA/m, SNIPPET)
- 90 deg, squareness 0.5: worst margin 0.009 at 39 deg; max iron B 0.33 T; max reverse H in magnets 27 kA/m (CoP Hc ~28 kA/m, SNIPPET)
- 90 deg, squareness 1.0: worst margin 0.035 at 39 deg; max iron B 0.65 T; max reverse H in magnets 53 kA/m (CoP Hc ~28 kA/m, SNIPPET)
- 180 deg convex, squareness 0.5: worst margin 0.002 at 95 deg; max iron B 0.33 T; max reverse H in magnets 26 kA/m (CoP Hc ~28 kA/m, SNIPPET)
- 180 deg convex, squareness 1.0: worst margin 0.009 at 95 deg; max iron B 0.65 T; max reverse H in magnets 51 kA/m (CoP Hc ~28 kA/m, SNIPPET)
