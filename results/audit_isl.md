# AUDIT 3 — ISL-PE physical realisability and generalisation

## A. Force transmission: sleeve height needed (ANALYTIC)

Rod W x W, length H, density 0.74*rho. Thrust = tau * (2 driven sleeve faces) * W * h_s.
Vertical lift: h_s >= rho_eff g W H / (2 tau).  Horizontal extrusion with tip load F: sleeve reacts moment M by a couple
2M/h_s whose friction mu*2M/h_s must be beaten: h_s^2 >= mu (M + self-moment) / (tau W) (plus weight term).

| tau (kPa) | rod | load | h_s vertical | h_s horizontal |
|---|---|---|---|---|
| 5.7 (realistic, 5 V scaled) | 5 mm x 5 cm | 0.0 N | 0.37 mm | 2.7 mm |
| 5.7 (realistic, 5 V scaled) | 10 mm x 10 cm | 0.0 N | 1.48 mm | 7.7 mm |
| 5.7 (realistic, 5 V scaled) | 10 mm x 10 cm | 1.0 N | 1.48 mm | 27.6 mm |
| 5.7 (realistic, 5 V scaled) | 20 mm x 30 cm | 10.0 N | 8.90 mm | 107.7 mm |
| 2.1 (50 V design derated to 30 V) | 5 mm x 5 cm | 0.0 N | 1.01 mm | 4.5 mm |
| 2.1 (50 V design derated to 30 V) | 10 mm x 10 cm | 0.0 N | 4.03 mm | 12.7 mm |
| 2.1 (50 V design derated to 30 V) | 10 mm x 10 cm | 1.0 N | 4.03 mm | 45.5 mm |
| 2.1 (50 V design derated to 30 V) | 20 mm x 30 cm | 10.0 N | 24.16 mm | 177.4 mm |

Verdict: unloaded extrusion is feasible with mm-scale sleeves; extending UNDER payload needs a sleeve comparable to the rod width or larger. Practical rule: extend unloaded, then lock.

## B. Every interface is a slip plane (ANALYTIC)

Rectangular cantilever, tip load F: interface shear demand tau_req = 1.5 F / A (transverse and longitudinal planes).
Available shear lock with no mechanical detent = synchronous holding stress (~tau_max) + mu * clamp pressure.

| section | F | tau_req | lock available (5.7 kPa + 0.4*11 kPa) | holds? |
|---|---|---|---|---|
| 5 mm sq | 0.1 N | 6.0 kPa | 10.1 kPa | yes |
| 5 mm sq | 1.0 N | 60.0 kPa | 10.1 kPa | NO - plastic slip |
| 5 mm sq | 10.0 N | 600.0 kPa | 10.1 kPa | NO - plastic slip |
| 10 mm sq | 0.1 N | 1.5 kPa | 10.1 kPa | yes |
| 10 mm sq | 1.0 N | 15.0 kPa | 10.1 kPa | NO - plastic slip |
| 10 mm sq | 10.0 N | 150.0 kPa | 10.1 kPa | NO - plastic slip |
| 20 mm sq | 0.1 N | 0.4 kPa | 10.1 kPa | yes |
| 20 mm sq | 1.0 N | 3.8 kPa | 10.1 kPa | yes |
| 20 mm sq | 10.0 N | 37.5 kPa | 10.1 kPa | NO - plastic slip |

Interface shear stiffness ~ tau_max*k = 1.09e+10 Pa/m -> effective shear modulus G_eff = k_t*L = 1.09 MPa at L=100 um (rubber-like). Tip shear deflection of a 1 cm sq x 10 cm rod under 1 N: 0.92 mm.
Verdict: without mechanical shear detents, ISL structures are weak and compliant in shear (a 'deck of cards'); a 1 cm rod slips plastically above ~0.7 N tip load. Fix: detents that engage at lattice sites (TRACK-B item B3).

## C. Tolerance-stack jamming (NUMERICAL Monte Carlo)

A rigid column of keys slides past a stationary sleeve stack of m modules. Each key and slot has independent lateral
position error N(0, sigma). At every half-step, all engaged key-slot pairs (including keys straddling a seam, which
engage two slots) must admit a common column offset x with |x + e_key - e_slot| <= c/2. Jam = no feasible x.

| clearance c / sigma | sleeve m | travel (steps) | P(jam during travel) |
|---|---|---|---|
| 4 | 4 | 100 | 0.9915 |
| 4 | 16 | 100 | 1.0000 |
| 4 | 16 | 1000 | 1.0000 |
| 6 | 4 | 100 | 0.4840 |
| 6 | 16 | 100 | 0.9872 |
| 6 | 16 | 1000 | 1.0000 |
| 8 | 4 | 100 | 0.0338 |
| 8 | 16 | 100 | 0.3655 |
| 8 | 16 | 1000 | 0.8340 |
| 10 | 4 | 100 | 0.0005 |
| 10 | 16 | 100 | 0.0112 |
| 10 | 16 | 1000 | 0.1000 |

Interpretation: jam probability per extrusion becomes negligible only when c >~ 8-10 sigma for long travels with tall sleeves (the spread of m+1 Gaussian samples grows ~ sqrt(2 ln m)). With DRIE/assembly sigma ~ 0.1-0.2 um this demands c ~ 1-2 um, which is >= the face-motor gap of the 5 V design: lateral play is fine, but the NORMAL clearance must be biased closed electrostatically during motion (small attractive bias) or the gap - and thrust - wanders by ~exp(-k c).

## D. 3D slab-feed extrusion and retraction of a w x w rod (NUMERICAL rule checking)

- 3x3 rod with +-y sleeves (2 high), feed from +x, open -x side: 7 extrude cycles completed, rod top at z=8; moves legal 126/126; module count conserved: True; connected after every move: True (checked).
- first illegal move (if any): none
- retraction: every forward state transition is reversible by a single legal move: True (126 transitions checked)

## E. Reversibility of the ISL move set (MATHEMATICAL + NUMERICAL)

Proof sketch: a move translates maximal run S by d. Its inverse translates S+d by -d. R2(inverse) requires the cell behind the inverse trailing end (= forward lead+2d) empty: guaranteed by forward R3. R3(inverse) requires forward trail-d empty: forward R2. 'Blocked' check: forward trail cell was vacated. S+d is maximal: forward R2/R3 guarantee empty cells at both ends. R4/R5 refer to the two endpoint states, which are swapped. Hence the reachability graph is undirected: every reachable shape can be retracted.

- random walk of 3000 moves (2D): inverse missing in 0 cases.

## F. Reachability / shape generality (NUMERICAL, BFS, 2D slice)

Start: extrusion-capable 2D setup (base row with port hole, 3-module feeder, sleeve, 2-module seed column), 10 modules, window x in [-3,4], z in [0,6]. Sliding-cube reference assumes modules CAN detach along face normals (a Track-B capability).

- ISL (R1-R5): 15319 configurations; max height 5; with elevated overhang 11559; with a side branch off the x=0 column 10606
- sliding cubes: 300000 (capped) configurations; max height 5; with elevated overhang 208696; with a side branch off the x=0 column 187567
- ISL subset of sliding-cube set: False (ISL-only 6359)

