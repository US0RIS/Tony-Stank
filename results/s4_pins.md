# Session 4 — pins: kinematics and orientation compatibility

## 1. Withdrawal/insertion kinematics (NUMERICAL)
Pin: base 14 um, tip 6 um, height 8 um; socket depth 9 um. r = distance of pin axis from the pivot edge.

| r (um) | socket 16 um, no chamfer: worst interference (um) | socket diameter needed (no chamfer) | chamfer needed with 16 um socket |
|---|---|---|---|
| 20.5 | 0.00 | 16.0 | 0.00 |
| 29.5 | 0.00 | 16.0 | 0.00 |
| 50.0 | 0.00 | 16.0 | 0.00 |
| 70.5 | 0.00 | 16.0 | 0.00 |
| 79.5 | 0.00 | 16.0 | 0.00 |

Interpretation: with a 14 -> 6 um taper, socket clearance (1 um at the mouth, 5 um at the tip) exceeds the arc's lateral sweep (<= ~1.5 um at the tip for r = 20.5 um), so withdrawal and insertion are collision-free for every pivot edge. The taper limits the pin's shear engagement to the tapered flank (see MECHANICAL_CYCLE.md for cam-out).

## 2. Orientation compatibility of pin patterns (MATHEMATICAL)

- Session-4 single pin + single socket layout: mates for relative rotations [0] only. After pivots change a module's orientation, other pairings put pin against pin -> blocked attachment or broken pins.
- Chiral pinwheel (4 pins at (+-29.0,+-18.0) rotated set, sockets = mirror): mates for [0, 90, 180, 270].
  Minimum spacing between the 8 sites: 15.6 um (needs >= socket size). Sites lie at |u|,|v| in {18.0,29.0} um from the face centre: they fall inside the coil envelopes (|v| <= 22 um) for the 4 sites with |v| = 18.0 um -> the 100 um face layout must be re-partitioned (coil length or bar width reduced). 

## 3. Can a pinwheel coexist with the coils at L = 100 um? (search, MATHEMATICAL)

Sites must lie outside the coil band |v| <= c_half (+1 um clearance), inside the window |u|,|v| <= 37 - site/2, and be >= site + 1 um apart (site = 10 um socket).

| coil band half-width c_half (um) | feasible pinwheel (a, b) found | resulting bar width each (um) | magnet cross-section vs session-4 layout |
|---|---|---|---|
| 22.0 | none | 13.5 | 1.12 |
| 20.0 | none | 11.5 | 0.96 |
| 18.0 | (np.float64(24.0), np.float64(-32.0)) | 9.5 | 0.79 |
| 16.0 | (np.float64(22.0), np.float64(-32.0)) | 7.5 | 0.62 |
| 14.0 | (np.float64(20.0), np.float64(-32.0)) | 5.5 | 0.46 |

A pinwheel needs both coordinates of every site outside the coil band, which is impossible unless the band shrinks; any feasible band reduces bar width (and switchable magnet volume) as listed. A 90-deg-symmetric pattern can also be placed inside the coil band only by interrupting the bars, which cuts their flux path.

