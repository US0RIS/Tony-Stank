# TRACK B — requirements for fully mobile microscopic modules (ANALYTIC)

## B1. Bolt latch: holding pressure vs module size

Si bolt of width b = 0.1 L, thickness t = 0.05 L, design shear strength 300 MPa (Si fracture 1-3 GPa, x3-10 safety); two bolts per face. Equivalent interface tensile pressure = 2 tau b t / L^2.

| L | bolt b x t | holding force | equivalent pressure | vs 0.6 MPa need |
|---|---|---|---|---|
| 1000 um | 100.0 x 50.0 um | 3e+03 mN | 3.0 MPa | x5 |
| 100 um | 10.0 x 5.0 um | 30 mN | 3.0 MPa | x5 |
| 30 um | 3.0 x 1.5 um | 2.7 mN | 3.0 MPa | x5 |
| 10 um | 1.0 x 0.5 um | 0.3 mN | 3.0 MPa | x5 |

Geometric scaling: pressure = 2 tau (b/L)(t/L) is size-INDEPENDENT; bolts keep MPa-class strength at any L that lithography can resolve.

## B2. Can an onboard electrostatic actuator stroke the bolt (unloaded)?

Resistance = guide adhesion/friction ~ mu x (capillary at 2 contacts, R_asp=0.2 um) -> F_res ~ 0.4 x 2 x 4 pi R gamma. Comb drive force = N x eps0 t V^2 / g (both sides).

F_res ~ 145 nN (humid); x3 margin -> 434 nN.

| L | finger t = 0.05 L | gap | V | fingers needed | comb area (fraction of L^2 face) |
|---|---|---|---|---|---|
| 1000 um | 50.0 um | 0.5 um | 5 V | 20 | 0.00 |
| 1000 um | 50.0 um | 1.0 um | 30 V | 2 | 0.00 |
| 100 um | 5.0 um | 0.5 um | 5 V | 197 | 0.59 |
| 100 um | 5.0 um | 1.0 um | 30 V | 11 | 0.04 |
| 30 um | 1.5 um | 0.5 um | 5 V | 655 | 21.83 |
| 30 um | 1.5 um | 1.0 um | 30 V | 37 | 1.64 |

At 100 um a 30 V comb fits (~4 % of a face); a 5 V comb needs ~60 % of a face per bolt -> bolts on all six faces do not fit at 5 V below ~100 um. Requirement: >=20-30 V local actuation or a force-amplifying (inchworm/ratchet) bolt drive.

## B3. Adhesion budget for sliding below 20 um (face drive at 5.7 kPa realistic, margin 5, mu 0.4)

| L | thrust | max total adhesion | bump R if capillary (3 bumps) | bump R if dry SAM, W=0.02 J/m^2 (3 bumps) |
|---|---|---|---|---|
| 30 um | 3078 nN | 1539 nN | 567 nm | 5443 nm |
| 20 um | 1368 nN | 684 nN | 252 nm | 2419 nm |
| 10 um | 342 nN | 171 nN | 63 nm | 605 nm |
| 5 um | 86 nN | 43 nN | 16 nm | 151 nm |

Below ~20 um, humid capillary bridges must be eliminated (bump radii < ~50 nm are not robust); hydrophobic SAM-coated sub-um standoffs are the minimum requirement; at 5 um dry bumps must be ~150 nm radius (marginal).

## B4. Power through a convex transition (module loses face contact for t_tr)

| L | hold-up (trench, 1 face) | logic-only power 10 nW | logic + self-actuation 1 uW |
|---|---|---|---|
| 1000 um | 144 nJ | 14.4 s | 145 ms |
| 100 um | 1.45 nJ | 0.145 s | 1.45 ms |
| 10 um | 0.0145 nJ | 0.00145 s | 0.0145 ms |

If the transit is ACTUATED BY NEIGHBOURS (the moving module is passive cargo, state held in nonvolatile memory), only retention power is needed during the break; at 10 nW even 10 um modules ride through ~1.5 ms. Requirement: neighbour-actuated transport or edge contacts; self-powered convex transitions are infeasible below ~100 um.

