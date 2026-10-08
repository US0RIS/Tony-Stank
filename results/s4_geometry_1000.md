# Session 4 — integrated NEPL module geometry, L = 1000 um (dimensions in um)

Components: 108. Interference violations (overlaps not declared as process-integrated): 0


## Volume budget (fraction of the L^3 envelope; pins protrude and sockets are voids inside the skin)

| kind | volume (um^3) | fraction |
|---|---|---|
| coil | 155520000 | 0.156 |
| routing | 148842000 | 0.149 |
| capacitor | 147852000 | 0.148 |
| hinge | 91200000 | 0.091 |
| electronics | 76664000 | 0.077 |
| pole | 47232000 | 0.047 |
| magnet | 33408000 | 0.033 |
| insulation | 16428000 | 0.016 |
| pin | 14112000 | 0.014 |
| socket | 13824000 | 0.014 |
| structure | 13824000 | 0.014 |
| pad | 1536000 | 0.002 |

Per-face EPM geometry (derived from the stack, not chosen): bar_w = 120.0 um, bar_t = 40.0 um, bar_l = 580.0 um, coil_l = 540.0 um, tw = 40.0 um, pole_depth = 410.0 um, window = 740.0 um, skin = 120.0 um

Switchable magnet volume per module: 33408000 um^3 (3.3 %); per face: 5568000 um^3.

## Key dimensions (per face)

- z-:cover: x[130.0,870.0] y[130.0,870.0] z[0.0,5.0] (SiO2)
- z-:pole1: x[130.0,210.0] y[285.0,695.0] z[10.0,130.0] (NiFe)
- z-:pole2: x[790.0,870.0] y[285.0,695.0] z[10.0,130.0] (NiFe)
- z-:bar0: x[210.0,790.0] y[325.0,445.0] z[50.0,90.0] (CoP (semi-hard))
- z-:coil0: x[230.0,770.0] y[285.0,485.0] z[10.0,130.0] (Cu + polyimide)
- z-:bar1: x[210.0,790.0] y[535.0,655.0] z[50.0,90.0] (CoP (semi-hard))
- z-:coil1: x[230.0,770.0] y[495.0,695.0] z[10.0,130.0] (Cu + polyimide)
- z-:pin: x[430.0,570.0] y[135.0,275.0] z[-80.0,40.0] (Si (DRIE))
- z-:socket: x[420.0,580.0] y[705.0,865.0] z[0.0,90.0] (void)
- z-:pad0: x[140.0,220.0] y[135.0,215.0] z[0.0,10.0] (Au on Ti)
- z-:pad1: x[780.0,860.0] y[135.0,215.0] z[0.0,10.0] (Au on Ti)
- z-:pad2: x[140.0,220.0] y[745.0,825.0] z[0.0,10.0] (Au on Ti)
- z-:pad3: x[780.0,860.0] y[745.0,825.0] z[0.0,10.0] (Au on Ti)
- z-:via: x[140.0,200.0] y[715.0,740.0] z[10.0,120.0] (Cu via bundle)

Drawings: results/s4_cad/nepl_1000um_*.png ; geometry JSON: results/s4_cad/nepl_1000um.json
