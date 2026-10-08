# S7 energy / speed / build-time budget (DERIVED)

| design | C_face | cycles per step | E per lattice step | step time @ f=10 kHz | speed | power while moving |
|---|---|---|---|---|---|---|
| L=100 um, g=1 um, 50 V, lam=3.3 um | 0.0531 pF | 30 | 4.02 nJ | 3.03 ms | 33 mm/s | 1.33 uW |
| L=100 um, g=100 nm, 5 V, lam=0.33 um | 0.531 pF | 303 | 4.02 nJ | 30.3 ms | 3.3 mm/s | 0.133 uW |
| L=1 mm, g=1 um, 50 V, lam=3.3 um | 5.31 pF | 303 | 4.02e+03 nJ | 30.3 ms | 33 mm/s | 133 uW |
| L=10 um, g=100 nm, 5 V, lam=0.33 um | 0.00531 pF | 30 | 0.00402 nJ | 3.03 ms | 3.3 mm/s | 0.00133 uW |

Compare: EPM switching pulse at 100 um ~37 uJ per switch (S1) = ~10^4 x the face-motor step energy.

Mechanical work per step against resistance ~2 uN (S2) over 100 um = 0.2 nJ -> electrical efficiency without charge recovery ~1-10 %.

## Build time for a rod by port extrusion (each port advances one module per 2 steps)

| rod | L | modules | ports (one per column) | step time | growth speed | time to full length | total energy |
|---|---|---|---|---|---|---|---|
| 5 mm sq x 10 cm | 100 um | 2.50e+06 | 2500 | 30 ms | 1.67 mm/s | 60 s | 10.1 J |
| 5 mm sq x 10 cm | 1000 um | 2.50e+03 | 25 | 30 ms | 16.67 mm/s | 6 s | 1.01 J |
| 10 mm sq x 10 cm | 100 um | 1.00e+07 | 10000 | 30 ms | 1.67 mm/s | 60 s | 40.2 J |
| 10 mm sq x 10 cm | 1000 um | 1.00e+04 | 100 | 30 ms | 16.67 mm/s | 6 s | 4.02 J |
| 20 mm sq x 30 cm | 100 um | 1.20e+08 | 40000 | 30 ms | 1.67 mm/s | 180 s | 1.45e+03 J |
| 20 mm sq x 30 cm | 1000 um | 1.20e+05 | 400 | 30 ms | 16.67 mm/s | 18 s | 145 J |

Note: in port extrusion every module already in the column moves on every lift (~N H/2 module-steps) and the feeder conveyors move a similar number, so total ~N H module-steps; growth speed per column is L/(2 t_step), independent of cross-section. Speed scales with L at fixed step time: smaller modules extrude more slowly unless t_step shrinks proportionally.

Telescoping (nested ports in series) multiplies speed by the number of stages k at the cost of k x energy.

