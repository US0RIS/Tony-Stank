# Session 4 — integrated NEPL module geometry, L = 100 um (dimensions in um)

Components: 108. Interference violations (overlaps not declared as process-integrated): 0


## Volume budget (fraction of the L^3 envelope; pins protrude and sockets are voids inside the skin)

| kind | volume (um^3) | fraction |
|---|---|---|
| coil | 155520 | 0.156 |
| routing | 148842 | 0.149 |
| capacitor | 147852 | 0.148 |
| hinge | 91200 | 0.091 |
| electronics | 76664 | 0.077 |
| pole | 47232 | 0.047 |
| magnet | 33408 | 0.033 |
| insulation | 16428 | 0.016 |
| pin | 14112 | 0.014 |
| socket | 13824 | 0.014 |
| structure | 13824 | 0.014 |
| pad | 1536 | 0.002 |

Per-face EPM geometry (derived from the stack, not chosen): bar_w = 12.0 um, bar_t = 4.0 um, bar_l = 58.0 um, coil_l = 54.0 um, tw = 4.0 um, pole_depth = 41.0 um, window = 74.0 um, skin = 12.0 um

Switchable magnet volume per module: 33408 um^3 (3.3 %); per face: 5568 um^3.

## Key dimensions (per face)

- z-:cover: x[13.0,87.0] y[13.0,87.0] z[0.0,0.5] (SiO2)
- z-:pole1: x[13.0,21.0] y[28.5,69.5] z[1.0,13.0] (NiFe)
- z-:pole2: x[79.0,87.0] y[28.5,69.5] z[1.0,13.0] (NiFe)
- z-:bar0: x[21.0,79.0] y[32.5,44.5] z[5.0,9.0] (CoP (semi-hard))
- z-:coil0: x[23.0,77.0] y[28.5,48.5] z[1.0,13.0] (Cu + polyimide)
- z-:bar1: x[21.0,79.0] y[53.5,65.5] z[5.0,9.0] (CoP (semi-hard))
- z-:coil1: x[23.0,77.0] y[49.5,69.5] z[1.0,13.0] (Cu + polyimide)
- z-:pin: x[43.0,57.0] y[13.5,27.5] z[-8.0,4.0] (Si (DRIE))
- z-:socket: x[42.0,58.0] y[70.5,86.5] z[0.0,9.0] (void)
- z-:pad0: x[14.0,22.0] y[13.5,21.5] z[0.0,1.0] (Au on Ti)
- z-:pad1: x[78.0,86.0] y[13.5,21.5] z[0.0,1.0] (Au on Ti)
- z-:pad2: x[14.0,22.0] y[74.5,82.5] z[0.0,1.0] (Au on Ti)
- z-:pad3: x[78.0,86.0] y[74.5,82.5] z[0.0,1.0] (Au on Ti)
- z-:via: x[14.0,20.0] y[71.5,74.0] z[1.0,12.0] (Cu via bundle)

Drawings: results/s4_cad/nepl_100um_*.png ; geometry JSON: results/s4_cad/nepl_100um.json
