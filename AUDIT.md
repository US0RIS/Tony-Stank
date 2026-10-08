# AUDIT — independent re-examination of session-1 claims (session 2)

Evidence classes used here:
- **MATH**: closed-form derivation or proof from stated assumptions.
- **NUM**: numerical simulation in this repository.
- **EXP**: experimental evidence. **No experiment has been performed in this project.** EXP entries only cite literature, with that literature's verification status.

Reproduce everything with:

```bash
python3 sims/audit/face_motor_realistic.py
python3 sims/audit/power_audit.py
python3 sims/audit/isl_audit.py
python3 sims/audit/branch_probe.py
python3 sims/track_b.py
python3 -m pytest -q tests
```

Outputs go to `results/audit_*.md` and `results/track_b.md`.

---

## Claim 1 — "The face motor gives ~7 kPa shear, scale-invariant, CMOS-compatible at 5 V"

| Sub-claim | Session-1 basis | Audit finding | Class | Status |
|---|---|---|---|---|
| Stress formulas τ(s), p(s) | MATH + FD check (1.4 %) | Still correct for the idealised surface-potential model | MATH, NUM | **Holds** |
| ~7 kPa after the discrete-electrode factor | NUM (0.59 factor) | Full stack (grounded Si, oxide, buried electrodes, coatings) gives 0.30–0.54 of ideal: **5.7 kPa** at zero net normal with a 0.1 µm SiO₂ coat, 3.5 kPa with a protective 0.3 µm coat. Stresses mesh-converged within 1 %. | NUM | **Revised down 20–50 %** |
| The 50 V / 1 µm design is usable | MATH | Opposite-phase facing electrodes see up to 100 V across about 1.2 µm. Measured micro-gap breakdown is ~65–110 V/µm × d (Slade & Taylor 2001, secondary citation). Must derate to about 30 V, giving **2.1 kPa**. Peak edge fields are a mesh-dependent singularity and are not used. | NUM + EXP (literature, unverified) | **Fails as designed** |
| The 5 V / 100 nm design avoids breakdown | MATH | Holds: 10 V peak-to-peak is below the O₂/N₂ ionisation potential | MATH | **Holds** |
| Tolerance to ±20 % gap error | NUM | Holds: margin 25 → 21 (wedge ±20 %); → 7 at ±60 % | MATH (local integration) | **Holds** |
| Contamination | Not modelled | Thrust ∝ ~exp(−k·d_particle). One 0.3 µm particle cuts the 5 V design's thrust to **2 %**; one 1 µm particle to 4×10⁻⁸. The 50 V design survives particles ≤ 1 µm but loses 98 % at 3 µm. | MATH | **NEW FATAL FLAW for open-air operation** |
| Trapped charge / patch potentials | Not modelled | A 2 V offset reduces the 5 V design's margin 21 → 4.8. The 50 V design is barely affected. | MATH | New weakness |
| ~4 nJ per step | MATH | Substrate capacitance raises it to **15–40 nJ** unless charge is recovered | MATH | **Revised up 4–10×** |
| Sliding size floor 10–20 µm | NUM | With realistic thrust: **~22 µm** (5 V design) to **~37 µm** (derated 50 V design), humid air | NUM | **Revised up** |

**Consequence (MATH, combining Paschen/Slade–Taylor breakdown with the exp(−k·d) particle law).** No open-air operating point exists that is simultaneously breakdown-safe, tolerant of µm-scale particles, and above ~1–2 kPa. A particle-tolerant gap of ≥ 5–10 µm needs pitch ≥ 15–30 µm. The field must then stay below the open-air breakdown envelope (≲ 15–30 V/µm at those gaps), and stress ∝ E² drops to ≲ 0.5–1 kPa. **Electrostatic sliding interfaces must operate in a sealed, particle-controlled volume.**

- For Track A this is manageable. With slab-feed extrusion, the only interfaces that slide are slab/base (inside the magazine) and rod perimeter/sleeve (at the port). A rod-wiper seal at the port, the standard hydraulic-cylinder solution, guards the only exposed sliding surface.
- For Track B (modules sliding over each other anywhere, in open air) this is a fundamental blocker.

---

## Claim 2 — "Lattice voltage drop depends only on structure height"

| Case (10×10×40 tower, 10 Ω contacts, 1 µW, 3 V) | Max drop / height-only formula | Class |
|---|---|---|
| Uniform load, full footprint, ideal garment (session-1 case) | 1.00 | NUM |
| 1 % of modules at 100× load (random) | 2.06 | NUM |
| 27-module hotspot at the top corner | 2.73 (a single column with one hot module: 5.9) | NUM / MATH |
| Footprint only the central 2×2 | 2.77 | NUM |
| Footprint a single corner module | 8.76 | NUM |
| Failed contacts 10 / 30 / 60 % | 1.17 / 1.82 / 9.74 (0 / 6 / 463 modules unpowered) | NUM |
| Lognormal R with median fixed (σ = 1, 2) | 0.91 / 0.70 in 3D. A series column scales with the mean, ×1.65 / ×7.4. | NUM / MATH |
| Garment segment resistance 0.01 / 1 / 10 Ω, fed from one edge | 1.00 / 1.20 / 2.94 | NUM |
| Two-conductor supply and return | ×2 | MATH |

**Verdict: the claim is FALSE as a general statement.** It is exact only for uniform load, full contact footprint and an equipotential garment (MATH: columns then carry no lateral current). Corrected statement:

  ΔV_max ≈ 2 × G × I·R·h(h+1)/2, with a geometry factor G ≈ 1–10 (footprint, hotspots, garment resistance, failed contacts).

Width matters because it supplies redundant paths and spreads concentrated loads. A single 40-module column with a 1 % contact-failure rate is fully powered only 67 % of the time (MATH). A 10×10 tower loses only 6 modules at a 30 % failure rate (NUM).

**Impact on ISL-PE: small.** Column modules are passive, so only port, sleeve and tip devices draw power. The S3 reach table should be divided by about √(2G), roughly 1.4–4.5×.

---

## Claim 3 — "The extrusion simulation shows ISL-PE is realisable"

| Question | Finding | Class | Status |
|---|---|---|---|
| Is extrusion kinematically legal in 3D? | **Yes.** A 3×3 rod extruded through an asymmetric port with ±y sleeves and slab feed from +x: 7 cycles, 126/126 legal moves, connected after every move. | NUM | Holds (session 1 was 2D only) |
| Is retraction always possible? | **Yes, for every ISL state.** Proof: the inverse of any legal move is legal (R2 ↔ R3 swap; R4/R5 are endpoint properties). Checked on a 3000-move random walk and on all 126 extrusion transitions. | MATH + NUM | **Proven** |
| Can the sleeve push the rod? | Vertical, unloaded: sleeve height 1.5 mm (10 mm × 10 cm rod, 5.7 kPa). Horizontal with 1 N tip load: **28 mm** (46 mm at 2.1 kPa). | MATH | **Extend unloaded, then lock** |
| Is the extruded structure strong? | **No, not as specified.** Every interface is a slip plane held only by electrostatic shear (~10 kPa including friction). A 1 cm square rod slips plastically above ~0.7 N tip load. Shear modulus G_eff ≈ 1 MPa (rubber-like). | MATH | **NEW FLAW** (S5's 0.6 MPa tensile analysis ignored shear) |
| Tolerance stack-up and jamming | Monte Carlo of keys sliding past a sleeve, including seam straddling: P(jam) over 1000 steps with a 16-high sleeve is 1.0 / 0.83 / 0.10 at clearance c = 6 / 8 / 10 σ. Needs **c ≳ 10σ**, about 1–2 µm for σ = 0.1–0.2 µm. | NUM | Feasible, but forces electrostatic normal bias during motion |
| Abstract moves vs executable motions | Session 1 omitted three things: (i) the feed is a w-cell traversal, not one step; (ii) traction comes only from sleeve area; (iii) no shear locking. The S7 "10 cm rod in 60 s at 100 µm" was wrong. Corrected growth speed ≈ v_slide × (magazine thickness / rod width): 0.66 mm/s for a 2 mm magazine, 1 cm rod, 3.3 mm/s slide → **~150 s for 10 cm**. With single-layer feed it would take ~50 min. | MATH | **Session-1 build time retracted** |
| Are most modules passive? | Holds with slab feed: only base (stator) and sleeve modules actuate. | NUM (which modules move relative to which) | Holds |

**Repair proposed for the slip-plane flaw (HYPOTHETICAL).**
- Interior rod interfaces never slide after a layer has been inserted. Only the perimeter/sleeve and slab/base interfaces slide.
- Interior interfaces can therefore carry **cam-engaged passive latches** that the port geometry closes as each layer leaves the sleeve and opens on retraction.
- This is the locking principle of macroscopic rigid-chain actuators (VERIFIED-META, LITERATURE §5), applied per lattice interface.
- Needs a mechanism design and experiment E6.

---

## Generalisation study — branching, multiple directions, retraction, reversible 3D shape change

| Capability | Result | Class |
|---|---|---|
| Retraction / reversibility | Every ISL shape change is exactly reversible (proof above) | MATH + NUM |
| Branching / horizontal arms | Exhaustive BFS from a 13-module 2D start (400k states, capped): a **6-module horizontal cantilever arm** at height 2 is reachable in 13 legal moves. Rows can slide out horizontally from elevated supports. | NUM |
| Size of the reachable shape space (10 modules, 2D window) | ISL: 15,319 configurations (complete). Sliding cubes: ≥ 300,000 (search capped). ISL is at least 20× more restricted. | NUM |
| Universality of ISL | Unknown. One invariant is proven: the number of garment-contact modules never changes. ISL is therefore not universal over all connected shapes, only within that invariant class; whether it is universal there is open. | MATH (invariant) / open |
| Load-bearing branches | Each branch is driven and held through its root interface only, so it has the slip-plane weakness at its root | MATH |
| Multiple extrusion directions | Garment curvature puts ports in different orientations. A port on the side of an extruded structure needs its own feed path through the structure; this was not demonstrated. | Open |

**Bridge to Track B (HYPOTHETICAL).** Replace the permanent undercut keys with **retractable bolts** (`sims/track_b.py` B1). With bolts withdrawn, a face can separate along its normal, giving sliding-cube capability, which is universal (Abel et al. 2024). With bolts engaged, the interface has ISL's material-limited strength. Call this the *Switchable-Interlock Sliding Lattice* (SISL). Track A hardware (ISL) is then a direct testbed for Track B components.
