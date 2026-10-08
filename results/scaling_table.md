# S1 force scaling (DERIVED)

| quantity | 10 mm | 1 mm | 100 um | 10 um | scaling |
|---|---|---|---|---|---|
| weight W (N) | 2.29e-02 | 2.29e-05 | 2.29e-08 | 2.29e-11 | L^3 |
| face area (m^2) | 1.00e-04 | 1.00e-06 | 1.00e-08 | 1.00e-10 | L^2 |
| electroadhesion, 100 V, 10 um polymer eps_r=3, 1 um air (N) | 2.36e-01 | 2.36e-03 | 2.36e-05 | 2.36e-07 | L^2 |
| e-static clamp, 10 V, 100 nm HfO2 eps_r=20, 10 nm rough gap (N) | 1.97e+02 | 1.97e+00 | 1.97e-02 | 1.97e-04 | L^2 |
| same clamp / weight | 8.61e+03 | 8.61e+04 | 8.61e+05 | 8.61e+06 | 1/L |
| capillary, R=L/2 water (N) | 4.52e-03 | 4.52e-04 | 4.52e-05 | 4.52e-06 | L |
| capillary / weight | 1.98e-01 | 1.98e+01 | 1.98e+03 | 1.98e+05 | 1/L^2 |
| vdW sphere-plane R=L/2 (N) | 5.21e-04 | 5.21e-05 | 5.21e-06 | 5.21e-07 | L |
| vdW flat faces, 5 nm rough gap (N) | 4.24e+00 | 4.24e-02 | 4.24e-04 | 4.24e-06 | L^2 |
| vdW flat faces, 50 nm rough gap (N) | 4.24e-03 | 4.24e-05 | 4.24e-07 | 4.24e-09 | L^2 |
| permanent-magnet contact, B=1 T (N) | 3.98e+01 | 3.98e-01 | 3.98e-03 | 3.98e-05 | L^2 (ideal; real fringing worse at small L) |
| EPM switching current density (A/m^2) | 5.33e+08 | 5.33e+09 | 5.33e+10 | 5.33e+11 | 1/L |
| EPM switching energy per pulse (J) | 3.69e-03 | 3.69e-04 | 3.69e-05 | 3.69e-06 | L (at fixed pulse time) |

Pressures: thin-film clamp 1968 kPa; electroadhesion 2.36 kPa; magnet B=1T 398 kPa.
EPM current density limit for copper/gold windings is ~1e9-1e10 A/m^2 for us pulses (electromigration DC limit ~1e9-5e9 A/m^2, ASSUM/UNVERIFIED).
