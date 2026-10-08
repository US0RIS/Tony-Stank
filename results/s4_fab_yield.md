# Session 4 — fabrication flow and yield (MATHEMATICAL bookkeeping; yields ASSUMED)

## Process flow and temperature ordering

| # | step | max T (C) | demonstrated individually? | note |
|---|---|---|---|---|
| 1 | Face-tile wafer: Si DRIE pockets for poles/bars/sockets | 25 | yes | standard DRIE |
| 2 | Hard magnet (only if ON/OFF EPM variant): NdFeB sputter + anneal | 650 | yes (films) | must precede Cu/polyimide/CoP |
| 3 | Bottom coil metal (plated Cu) + SiO2/polyimide insulation | 350 | yes | polyimide cure ~350 C |
| 4 | NiFe pole pieces (plated, through-mask) | 90 | yes |  |
| 5 | CoP switchable bars (plated, field-assisted) | 90 | films yes; patterned 4x12x58 um bars NO data | no anneal; squareness unknown |
| 6 | Top coil metal + vias closing the 3D solenoid | 350 | 3D solenoids yes (larger pitch); around semi-hard core NO |  |
| 7 | Pins (DRIE Si), pads (Ti/Au), cover | 300 | yes |  |
| 8 | Tile release + thinning to 12 um | 25 | yes (thinning) | fragile 12 um tiles |
| 9 | Core: 2 thinned CMOS dies + trench capacitor + TSV redistribution | 400 | yes (3D stacking) | die 74x74 um at 100 um scale |
| 10 | Six-sided assembly: tiles bonded to core + edge/corner blocks | 250 | NO (no 6-sided microassembly of 100 um parts demonstrated) | placement +-1-2 um (3 sigma) vs 1 um clearances |
| 11 | Magnetisation set (on-chip coils) | 25 | NO for CoP micro-bars |  |
| 12 | Test + sort | 25 | yes | per-module probing |

Temperature ordering is consistent only if the hard-magnet anneal (650 C) happens first on bare tiles and every later step stays <= 400 C; CoP needs no anneal (favourable). No integrated device combining all steps has been demonstrated at any scale <= 1 mm.

## Face alignment probability (placement sigma vs layout clearance)
| L | clearance (um) | placement sigma (um) | P(face OK) | P(all 6 faces OK) |
|---|---|---|---|---|
| 100 | 1.0 | 0.5 | 0.911 | 0.572 |
| 100 | 1.0 | 0.67 | 0.747 | 0.174 |
| 300 | 3.0 | 0.67 | 1.000 | 1.000 |
| 1000 | 10.0 | 1.0 | 1.000 | 1.000 |

## Module yield (100 process steps, bonds as listed)
| scale | step yield | bonds | bond yield | alignment (6 faces) | module yield | good modules in 1e4 / 1e7 |
|---|---|---|---|---|---|---|
| 100 um | 0.999 | 36 | 0.999 | 0.174 | 0.152 | 1520 / 1.52e+06 |
| 100 um | 0.995 | 36 | 0.999 | 0.174 | 0.102 | 1017 / 1.02e+06 |
| 300 um | 0.999 | 36 | 0.999 | 1.000 | 0.873 | 8727 / 8.73e+06 |
| 300 um | 0.995 | 36 | 0.999 | 1.000 | 0.584 | 5843 / 5.84e+06 |
| 1000 um | 0.999 | 36 | 0.999 | 1.000 | 0.873 | 8728 / 8.73e+06 |
| 1000 um | 0.995 | 36 | 0.999 | 1.000 | 0.584 | 5843 / 5.84e+06 |

The 100 um design's 1 um clearances against ~+-2 um (3 sigma) six-tile placement leave most modules misaligned (reviewer 3 finding, reproduced here). At 300 um and 1 mm the clearances scale with L while placement accuracy does not, so alignment stops dominating.

