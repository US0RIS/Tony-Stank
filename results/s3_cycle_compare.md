# Session 3 — executable transformation TOWER-ARM <-> ARCH (NUMERICAL SIMULATION)

- TOWER-ARM: cells [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 3), (2, 0), (2, 3)]; metrics (maxh, branch, cavity, cantilever) = (3, False, False, True)
- ARCH: cells [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0)]; metrics (maxh, branch, cavity, cantilever) = (2, False, True, False)

## MPL (strict push+pull pivots)
- forward plan: 9 moves; reverse plan: 9 moves
- move types: 4 x 90 deg, 5 x 180 deg; every move has source and destination supports (strict rule).
- power: during every move all non-moving modules (incl. both actuating neighbours) stay connected to the garment: True; the mover needs no power in transit (passive magnets, nonvolatile state).
- parallel schedule: 9 sequential moves -> 8 collision-free parallel steps

| L | 90 deg torque margin (3D-derated) | 180 deg margin | hinge load 90/180 | inertial time per pivot | landing energy | EPM energy (4 face switches/move, all poles) | plan energy |
|---|---|---|---|---|---|---|---|
| 1000 um | 90.1 | 40.1 | 11168/12459 uN | 644 us | 4.62e+03 nJ | 1.45e+04 nJ | 1.31e+05 nJ |
| 300 um | 36.4 | 16.2 | 1005/1121 uN | 193 us | 125 nJ | 1.31e+03 nJ | 1.18e+04 nJ |
| 100 um | 4.5 | 2.0 | 112/125 uN | 64 us | 4.62 nJ | 145 nJ | 1.31e+03 nJ |
| 30 um | 0.4 | 0.2 | 10/11 uN | 19 us | 0.125 nJ | 43.5 nJ | 392 nJ |

## SISL (sliding, electrostatic face drive)
- forward plan: 6 moves
- 2 straight slides (face drive), 4 convex transitions (face drive cannot execute; needs a pivot actuator or neighbour transport, and breaks face contact -> power gap)
- per straight slide at L = 100 um: thrust margin ~20 sealed (AUDIT 1); with one 1 um particle in a 100 nm-gap design thrust x4e-8; sliding distance per slide = L; sliding-contact life ~1e5 cycles in air (polysilicon sidewalls, SNIPPET) -> ~1e5 moves per interface.

## ISL: path TOWER-ARM -> ARCH: NONE (bounded search exhausted)
## FC: TOWER-ARM single-path traceable: True; ARCH traceable: True (a chain can only form shapes that admit a Hamiltonian path from its anchor)
## Shape-space fraction (N = 8): of 13309 single-component shapes reachable by MPL, 3503 (26 %) are formable by an anchored folding chain.
