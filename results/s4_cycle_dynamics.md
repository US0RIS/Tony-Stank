# Session 4 — pivot cycle dynamics from the FD torque tables (L = 100 um; larger L by exact similarity scaling)

## 90 deg pivot (CoP Jr 0.65 T, squareness 0.8; 2D x pole depth; best neighbour state per angle)

- torque range over the swing: 9.17e-12 to 5.23e-11 N m; angles with negative best torque: []
- inward hinge force (best states): min -0.13 uN (needs captive hinge)

| s (L) | adhesion case | start torque / peel torque | stalls at (deg) | transit time | landing edge speed | verdict |
|---|---|---|---|---|---|---|
| 100 um | humid (9 bumps, full meniscus) | 0.060 | does not start | - | - | FAIL (cannot peel) |
| 100 um | dry SAM-coated sharp bumps (ASSUMED 10x lower) | 0.597 | does not start | - | - | FAIL (cannot peel) |
| 300 um | humid (9 bumps, full meniscus) | 0.537 | does not start | - | - | FAIL (cannot peel) |
| 300 um | dry SAM-coated sharp bumps (ASSUMED 10x lower) | 5.37 | - | 5020 us | 0.24 m/s | OK |
| 1000 um | humid (9 bumps, full meniscus) | 5.97 | - | 16732 us | 0.24 m/s | OK |
| 1000 um | dry SAM-coated sharp bumps (ASSUMED 10x lower) | 59.68 | - | 16732 us | 0.24 m/s | OK |

## 180 deg pivot (CoP Jr 0.65 T, squareness 0.8; 2D x pole depth; best neighbour state per angle)

- torque range over the swing: 2.28e-12 to 5.05e-11 N m; angles with negative best torque: []
- inward hinge force (best states): min -0.17 uN (needs captive hinge)

| s (L) | adhesion case | start torque / peel torque | stalls at (deg) | transit time | landing edge speed | verdict |
|---|---|---|---|---|---|---|
| 100 um | humid (9 bumps, full meniscus) | 0.052 | does not start | - | - | FAIL (cannot peel) |
| 100 um | dry SAM-coated sharp bumps (ASSUMED 10x lower) | 0.520 | does not start | - | - | FAIL (cannot peel) |
| 300 um | humid (9 bumps, full meniscus) | 0.468 | does not start | - | - | FAIL (cannot peel) |
| 300 um | dry SAM-coated sharp bumps (ASSUMED 10x lower) | 4.68 | - | 9468 us | 0.25 m/s | OK |
| 1000 um | humid (9 bumps, full meniscus) | 5.20 | - | 31561 us | 0.25 m/s | OK |
| 1000 um | dry SAM-coated sharp bumps (ASSUMED 10x lower) | 52.04 | - | 31561 us | 0.25 m/s | OK |

Pin fracture (reviewer R3): pin-tip stress ~2-4 GPa at 2 m/s, scaling ~v; DRIE Si fracture ~1-3 GPa -> landing speed must be < ~0.3-0.5 m/s.


## Hinge-free schedule (only states that press the mover into its pivot edge; NUMERICAL)

- 90 deg: angles with NO admissible state: [3.0]; min admissible torque 3.38e-13 N m
  3:none, 9:0,-1, 15:0,-1, 21:0,-1, 27:0,-1, 33:0,-1, 39:1,-1, 45:1,-1, 51:1,-1, 57:1,-1, 63:1,-1, 69:1,-1, 75:1,-1, 81:1,-1, 87:1,-1
- 180 deg: angles with NO admissible state: [5.0]; min admissible torque 2.70e-13 N m
  5:none, 15:0,1, 25:0,1, 35:0,1, 45:1,1, 55:1,1, 65:1,1, 75:1,1, 85:1,1, 95:1,1, 105:1,1, 115:1,1, 125:1,1, 135:1,1, 145:1,1, 155:1,1, 165:1,1, 175:1,1
