# GENERALITY — quantitative reconfiguration comparison (session 3)

Code:
- `sims/s3/generality.py` → `results/s3_generality.md`
- `sims/s3/cycle_compare.py` → `results/s3_cycle_compare.md`
- `sims/s3/generality3d.py` → `results/s3_generality3d.md`

Sessions 1–2: `results/audit_isl.md`, `results/audit_branch.md`.

## Framework

Every architecture gets the same treatment:
- the same window (2D: x ∈ [−2, 5], z ∈ [0, 5]);
- the same module count (N = 8) and garment boundary;
- the same start (6 on the garment + 2 on top), except the chain, which must start as a chain.

Each move rule encodes the physical mechanism: support requirements, swept-volume collisions, and the connectivity that is also the power path.

**Metrics:** reachable configurations; branch; enclosed cavity (the garment counts as a wall); cantilever ≥ 2; height ≥ 4; minimum moves to the first occurrence; fraction of moves whose reverse is legal; ability to transform between two unrelated shapes (TOWER-ARM ↔ ARCH); active fraction; load capacity; power robustness (from the audit-2 lattice model).

## Results

| Model | States | Branch / cavity / cantilever / h ≥ 4 (min moves) | Reverse fraction | TOWER-ARM ↔ ARCH | Class |
|---|---|---|---|---|---|
| Sliding (SISL) | 62,255 (complete) | 1 / 1 / 2 / 8 | 1.00 | 6 moves (4 convex) | N |
| NEPL strict push+pull pivots | 62,227 (complete) | 1 / 3 / 4 / 8 | 1.00 | 9 / 9 moves | N |
| NEPL lenient (pull-only allowed) | 62,229 | 1 / 3 / 4 / 8 | 0.97 | — | N |
| ISL | 19 | none | 1.00 | impossible (exhausted) | N |
| Folding chain (anchored at (0,0)) | 639 conformations = all existing ones; 538 shapes | 1 / 2 / 1 / 1 | 1.00 | both shapes traceable | N |

**Containment:** the NEPL-strict set is a subset of the sliding set. It lacks 28 states (0.045 %), all at the window edge where a pivot's swept volume would leave the boundary (N).

**Chain shape fraction:** of the 13,309 single-component shapes reachable by NEPL at N = 8, 26 % admit a Hamiltonian path from a garment anchor. Those are the only ones an anchored chain can form (N enumeration; the path condition itself is MATHEMATICAL).

**3D check (exhaustive in a 3×3×3 window), N = 5 and 6:** the strict EPM-pivot set is a subset of the sliding set in both cases.
- N = 5: 3,288 of 3,300 sliding states reached (99.6 %).
- N = 6: 13,005 of 13,021 (99.88 %).

The missing states are window-edge cases (N). Pivot ≈ sliding therefore also holds in 3D within these bounds.

## Proven vs bounded

| Statement | Status |
|---|---|
| ISL conserves the garment-contact count; ISL moves are reversible | **Proven** (session 2, MATH) |
| A chain forms only shapes with a Hamiltonian path from its anchor | **Proven** (topology) |
| Sliding cubes are universal | **Literature** (Abel et al. 2024; snippet-level access) |
| 2D pivoting with a constant number of helper modules is universal | **Literature** (Akitaya et al. ESA 2019; snippet) |
| NEPL ≈ sliding in reachable set; NEPL forms branches, cavities and cantilevers; NEPL executes TOWER-ARM ↔ ARCH | **Bounded numerical** (2D N = 8; 3D N = 5, 6). Not a universality proof. |
| NEPL physical move rule (push+pull supports) is sufficient for the torque budget | **Numerical**, 2D magnetic model + assumed 3D derate |

## Active fraction, load capacity, power robustness

- **Active fraction:** SISL, NEPL and FC need 100 %. ACPL needs ≪ 1 %. A NEPL skin over a passive core needs about 6L/W (≈ 6 % for W = 1 cm at L = 100 µm).
- **Load capacity:**
  - ISL interlocks are material-limited in tension but have slip planes in shear (unless cam latches work).
  - NEPL gives 50–100 kPa in tension and 9.4 MPa in shear.
  - Bolted SISL gives about 3 MPa.
- **Power robustness:** lattice architectures inherit audit-2 redundancy (a 10×10 tower tolerates 30 % contact failures). Chains do not: P(40-unit chain intact) = 0.67 at 1 % joint failure.

## Moving joints

NEPL and FC can form moving joints directly: a pivot is a joint, so a module held mid-swing by D's attraction behaves as an actuated hinge. SISL forms sliding joints. ISL forms only telescoping joints. This is a qualitative engineering assessment, not simulated.
