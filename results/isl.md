# S6 Interlocked Sliding Lattice: kinematic simulation (SIMULATED)

## Extrusion through a port (2D slice)

- cycles attempted: 28; legal lifts 28, legal feeds 28; final tower height 30 modules (z=1..30) (from seed 2); every intermediate state connected to garment (R4 checked each move).
- first failure: none

## Ablations (why each geometric feature is required)

- left sleeve at (-1,1) present: lift -> True (moved 2); feed -> False (R3 head-on arrival)
- right sleeve (1,2) absent: lift -> False (R5 no traction after); feed -> False (-)

## Random legal-move invariant test (20000 proposals)

- legal moves executed: 6863; garment-contact count invariant held (12); connectivity held; max height reached 9
- outcome counts: {'moved': 6863, 'blocked': 3209, 'R2 head-on separation (garment)': 3129, 'R3 head-on arrival': 1731, 'R4 disconnects': 3622, 'R5 no traction after': 1446}
