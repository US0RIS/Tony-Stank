# Session 4 — integrated NEPL module geometry, L = 300 um (dimensions in um)

Components: 108. Interference violations (overlaps not declared as process-integrated): 0


## Volume budget (fraction of the L^3 envelope; pins protrude and sockets are voids inside the skin)

| kind | volume (um^3) | fraction |
|---|---|---|
| coil | 4199040 | 0.156 |
| routing | 4018734 | 0.149 |
| capacitor | 3992004 | 0.148 |
| hinge | 2462400 | 0.091 |
| electronics | 2069928 | 0.077 |
| pole | 1275264 | 0.047 |
| magnet | 902016 | 0.033 |
| insulation | 443556 | 0.016 |
| pin | 381024 | 0.014 |
| socket | 373248 | 0.014 |
| structure | 373248 | 0.014 |
| pad | 41472 | 0.002 |

Per-face EPM geometry (derived from the stack, not chosen): bar_w = 36.0 um, bar_t = 12.0 um, bar_l = 174.0 um, coil_l = 162.0 um, tw = 12.0 um, pole_depth = 123.0 um, window = 222.0 um, skin = 36.0 um

Switchable magnet volume per module: 902016 um^3 (3.3 %); per face: 150336 um^3.

## Key dimensions (per face)

- z-:cover: x[39.0,261.0] y[39.0,261.0] z[0.0,1.5] (SiO2)
- z-:pole1: x[39.0,63.0] y[85.5,208.5] z[3.0,39.0] (NiFe)
- z-:pole2: x[237.0,261.0] y[85.5,208.5] z[3.0,39.0] (NiFe)
- z-:bar0: x[63.0,237.0] y[97.5,133.5] z[15.0,27.0] (CoP (semi-hard))
- z-:coil0: x[69.0,231.0] y[85.5,145.5] z[3.0,39.0] (Cu + polyimide)
- z-:bar1: x[63.0,237.0] y[160.5,196.5] z[15.0,27.0] (CoP (semi-hard))
- z-:coil1: x[69.0,231.0] y[148.5,208.5] z[3.0,39.0] (Cu + polyimide)
- z-:pin: x[129.0,171.0] y[40.5,82.5] z[-24.0,12.0] (Si (DRIE))
- z-:socket: x[126.0,174.0] y[211.5,259.5] z[0.0,27.0] (void)
- z-:pad0: x[42.0,66.0] y[40.5,64.5] z[0.0,3.0] (Au on Ti)
- z-:pad1: x[234.0,258.0] y[40.5,64.5] z[0.0,3.0] (Au on Ti)
- z-:pad2: x[42.0,66.0] y[223.5,247.5] z[0.0,3.0] (Au on Ti)
- z-:pad3: x[234.0,258.0] y[223.5,247.5] z[0.0,3.0] (Au on Ti)
- z-:via: x[42.0,60.0] y[214.5,222.0] z[3.0,36.0] (Cu via bundle)

Drawings: results/s4_cad/nepl_300um_*.png ; geometry JSON: results/s4_cad/nepl_300um.json
