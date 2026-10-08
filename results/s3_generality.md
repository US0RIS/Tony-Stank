# Session 3 — reconfiguration generality on common ground (NUMERICAL SIMULATION, bounded BFS)

2D slice, window x in [-2,5], z in [0,5], N = 8, start = 6 on garment + 2 on top. Cap 200000 states.

| model | states | distinct shapes | max height | branch (depth) | cavity (depth) | cantilever>=2 (depth) | height>=4 (depth) | reverse-move fraction |
|---|---|---|---|---|---|---|---|---|
| SL sliding | 62255 | 62255 | 5 | 1 | 1 | 2 | 8 | 1.00 |
| PVs pivot strict | 62227 | 62227 | 5 | 1 | 3 | 4 | 8 | 1.00 |
| PVl pivot lenient | 62229 | 62229 | 5 | 1 | 3 | 4 | 8 | 0.97 |
| ISL | 19 | 19 | 1 | - | - | - | - | 1.00 |
| FC folding chain (anchored at (0,0)) | 639 | 538 | 5 | 1 | 2 | 1 | 1 | 1.00 |

FC completeness: 639 conformations reached of 639 self-avoiding 8-unit chains anchored at (0,0) in the window (all).

'-' = not found within the bounded search. Depth = minimum number of moves from the start.

Notes: FC starts as an L-shaped chain anchored at (0,0) because a chain cannot share SL's start configuration; its garment contact is only the anchored unit (garment contact of other units is not required for connectivity). ISL conserves the garment-contact count (proven), so from this start it cannot lift anything; see audit_isl.md for ISL from a port-equipped start.

