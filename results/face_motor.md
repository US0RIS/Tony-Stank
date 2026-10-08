# S2 electrostatic face-motor (DERIVED + SIMULATED)

Optimal k*g maximising shear at fixed V,g: 1.9150 -> pitch lam = 3.281 g; tau_max = 1.105 * eps0 V^2/(2 g^2).

## Validation: analytic vs finite difference (sinusoidal electrodes)

| k*s | tau analytic (Pa) | tau FD (Pa) | p analytic (Pa) | p FD (Pa) |
|---|---|---|---|---|
| 0.000 | 0.0 | 0.0 | -9478.7 | -9482.4 |
| 0.500 | 5820.8 | 5819.1 | -7946.7 | -7951.0 |
| 1.571 | 12141.1 | 12137.7 | 3036.3 | 3027.2 |
| 2.000 | 11039.9 | 11036.8 | 8244.3 | 8233.0 |
| 3.142 | 0.0 | 0.0 | 15551.3 | 15536.7 |

Max error relative to |p(pi/2)|: 1.41 %

## Discrete 3-phase stripe electrodes (FD)

Bottom phases (0,120,240 deg); top phases shifted by theta. Peak shear over theta relative to ideal sinusoid of same amplitude.

| electrode fill | peak tau FD (Pa) | ideal tau_max (Pa) | ratio |
|---|---|---|---|
| 0.5 | 6869.4 | 12141.1 | 0.57 |
| 0.7 | 7133.0 | 12141.1 | 0.59 |
| 0.9 | 7290.5 | 12141.1 | 0.60 |

## Sliding feasibility (humid air, capillary at 9 standoff bumps R=0.5 um, mu=0.4, weight normal to face)

Design family at constant field V/g = 50 V/um and lam = 3.3 g (scale-invariant stress).

| gap g | V | pitch | L | thrust (N) | resistance (N) | margin | shear (kPa) | net normal (kPa) |
|---|---|---|---|---|---|---|---|---|
| 1.0 um | 50 | 3.28 um | 1000 um | 4.13e-03 | 1.15e-05 | 359.7 | 6.88 | 0.00 |
| 1.0 um | 50 | 3.28 um | 100 um | 4.13e-05 | 1.64e-06 | 25.1 | 6.88 | 0.00 |
| 1.0 um | 50 | 3.28 um | 30 um | 3.71e-06 | 1.63e-06 | 2.3 | 6.88 | 0.00 |
| 1.0 um | 50 | 3.28 um | 10 um | 4.13e-07 | 1.63e-06 | 0.3 | 6.88 | 0.00 |
| 0.3 um | 15 | 0.98 um | 1000 um | 4.13e-03 | 1.15e-05 | 359.7 | 6.88 | 0.00 |
| 0.3 um | 15 | 0.98 um | 100 um | 4.13e-05 | 1.64e-06 | 25.1 | 6.88 | 0.00 |
| 0.3 um | 15 | 0.98 um | 30 um | 3.71e-06 | 1.63e-06 | 2.3 | 6.88 | 0.00 |
| 0.3 um | 15 | 0.98 um | 10 um | 4.13e-07 | 1.63e-06 | 0.3 | 6.88 | 0.00 |
| 0.1 um | 5 | 0.33 um | 1000 um | 4.13e-03 | 1.15e-05 | 359.7 | 6.88 | 0.00 |
| 0.1 um | 5 | 0.33 um | 100 um | 4.13e-05 | 1.64e-06 | 25.1 | 6.88 | 0.00 |
| 0.1 um | 5 | 0.33 um | 30 um | 3.71e-06 | 1.63e-06 | 2.3 | 6.88 | 0.00 |
| 0.1 um | 5 | 0.33 um | 10 um | 4.13e-07 | 1.63e-06 | 0.3 | 6.88 | 0.00 |

## Pitch mismatch: fixed lithography pitch 2 um with thin gap (normal force dominates)

| gap g | V | k g | margin (L=100 um) | net normal (kPa) |
|---|---|---|---|---|
| 1000 nm | 50.0 | 3.14 | 20.0 | 0.01 |
| 300 nm | 15.0 | 0.94 | 5.5 | 1.43 |
| 100 nm | 5.0 | 0.31 | 1.8 | 1.04 |
| 30 nm | 1.5 | 0.09 | 0.4 | 0.14 |

## Gap tolerance: phase tuned for nominal gap, actual gap +-20% (L=100 um)

| design | margin @0.8g | @1.0g | @1.2g |
|---|---|---|---|
| g=1.0 um V=50.0 lam=3.30 um | 11.90 | 25.05 | 17.00 |
| g=0.1 um V=5.0 lam=0.33 um | 11.90 | 25.05 | 17.00 |
| g=0.1 um V=5.0 lam=2.00 um | 1.55 | 1.77 | 1.91 |

Note: discrete-electrode factor is applied to both shear and normal stress (approximation; FD gave it for shear only).


## Size floor: L at which margin = 1 (thrust ~ L^2, bump adhesion ~ const)

- humid=True: L_min = 19.9 um (9 bumps, R=0.5 um)
- humid=False: L_min = 10.1 um (9 bumps, R=0.5 um)

## Dry vs humid adhesion at L=100 um, g=1 um, V=50 V

- humid=True: margin 25.1
- humid=False: margin 93.5
- with net hold pressure >= 5 kPa during slide: margin 2.9, shear 6.7 kPa
