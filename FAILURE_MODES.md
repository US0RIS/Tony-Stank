# FAILURE MODES, impossibility results, open questions

## 1. Established (DERIVED) negative results

| # | Result | Basis |
|---|---|---|
| N1 | EPMs cannot be switched by onboard coils at ≤ 100 µm. Required J ~5×10¹⁰ A/m² vs ~10⁹ limit; ~37 µJ per switch. | S1, PHYSICS §1. The rough model (window, path, pulse time) could shift J by ~3×; the conclusion survives that. |
| N2 | Air-gap electrostatic attachment cannot carry human-scale structural loads. ≤ ~11 kPa at 50 V/µm vs ≥ 100–700 kPa needed. | S5 + PHYSICS §4 |
| N3 | Sliding and MPa contact clamping are incompatible on the same flat interface. van der Waals between flat faces is ~660 kPa at 2 nm separation, falling to 42 Pa at 50 nm. | PHYSICS §4 |
| N4 | Capacitive face coupling cannot be the power bus at 100 µm (|Z| ~10⁴–10⁶ Ω). Reach ~1 mm. | S3 |
| N5 | At 100 µm, on-chip storage cannot bridge a full lattice step (1.45 nJ vs 4 nJ). | S3, S7 |
| N6 | Electrostatic sliding fails below L ≈ 10–20 µm (margin ∝ L²) unless adhesion is engineered down ~10×. | S2 |
| N7 | Single-file chain reach scales as √L: smaller modules mean shorter cantilevers at fixed bond strength. | S5 |
| N8 | In a uniformly loaded lattice, adding width does not reduce voltage drop. Only height in hops, R and P matter. | S3 |
| N9 | Standby power ≥ 1 µW per module is incompatible with 10⁷-module wearables (10 W). Need ≤ 10 nW per module. | S3 |
| N10 | With permanent interlocks, modules touching the garment can never leave it, and contacts never form or break along a normal. Shape change must go through ports and conveyors. | S6 (invariant test, 6863 random legal moves) |

## 2. Physical risks to ISL-PE, ranked

1. **Particles and wear debris** in 0.1–1 µm gaps. The "universal environment" requirement conflicts with an open lattice. Mitigations (all HYPOTHETICAL):
   - A sealed garment magazine and a sealed skin layer of modules on extruded structures.
   - Deliberately large interlock clearances, with the gap set by compliant standoffs.
   - Hydrophobic, low-surface-energy coatings.
2. **Slot seam alignment and tolerance stack-up** across thousands of modules. The required registration is finer than the slot clearance, and errors accumulate.
3. **Wear of sliding interlocks and power brushes** over 10⁶–10⁸ steps. The only microcontact lifetime data seen is ~10⁷ cycles for Au–Au at 200 µN, and that is switching, not sliding (SNIPPET).
4. **Dielectric charging** (drift in the face drive). Mitigation: bipolar/AC drive (DEMED is AC by nature).
5. **Humidity.** Capillary adhesion and charging both rise with it. Sliding margin at 100 µm is 25 in humid air vs 94 dry (S2).
6. **Field limits.** 50 V/µm in air at a 1 µm gap is uncertain (Paschen's law fails there). The 5 V / 100 nm design avoids gas breakdown but needs ±20 nm gap control.
7. **High-voltage drivers on chip** if the 50 V design is used: area and leakage. The 5 V design avoids this.
8. **Brittle failure.** Interlocks in Si fail suddenly. Electrostatic shear locks snap without warning above their load.
9. **Heat.** 0.7 W average during a 60 s build of 10⁷ modules is acceptable. 10 W standby is not (N9).

## 3. System-level obstacles to the full vision

- **"Discreet":** a 1 cm³ magazine of 100 µm modules holds 10⁶ modules, enough for only ~0.1 of a 10 cm × 1 cm rod. The garment must carry tens of cm³ of material, which adds mass (Si 2.3 g/cm³) and stiffness to clothing.
- **"Rapid":** extrusion growth ≈ L/(2t_step), about 1.7 mm/s at 100 µm. Telescoping or faster steps are needed for sub-second effects.
- **"Universal environment":** dust, water and skin oils are all incompatible with sub-µm sliding gaps unless sealed.
- **Shape class:** ISL-PE without further mechanisms gives extrusions only.

## 4. Open questions (not resolved this session)

1. Is the ISL move set (R1–R5) universal in 3D when ports can be placed on the structure itself? Or is there an impossibility result analogous to locked pivoting configurations?
2. Can an interlock geometry be both genderless and seam-tolerant at 100 µm in DRIE silicon? This needs CAD plus contact simulation.
3. What are sliding friction and debris generation for Si/SiO₂/DLC-coated undercut rails at 10 µN–1 mN loads over 10 m of travel?
4. Does a 3-phase face drive with standoffs keep its margin with realistic fringing fields and back-side fields? The model idealises field confinement.
5. What are the measured contact resistance and wear of Au/Ru sliding microbrushes at 1–10 µN?

## 5. Yield (DERIVED)

If every module must be active and functional, a column of 1000 modules at 99 % per-die yield has a 0.99¹⁰⁰⁰ ≈ 4×10⁻⁵ chance of being defect-free. **Fully active homogeneous swarms are not manufacturable without fault tolerance.** ISL-PE helps because column modules are passive passengers: a non-functional module is carried, not fatal. Only port and sleeve drivers need to work, and they can be tested and replaced at the garment level.

## 6. Session-2 audit additions (see AUDIT.md)

| # | Result | Class |
|---|---|---|
| N11 | Rigid electrostatic sliding faces are not particle tolerant: thrust ∝ exp(−k·d). No open-air operating point is simultaneously breakdown-safe, tolerant of µm particles, and above ~1–2 kPa. | MATH |
| N12 | The 50 V / 1 µm face drive sits inside the measured micro-gap breakdown band. Derate to ~30 V (2.1 kPa). | NUM + literature (unverified) |
| N13 | In ISL, every interface is a slip plane. Without mechanical shear locks, structures slip above ~1.5 F/A ≈ 10 kPa (≈ 0.7 N on a 1 cm rod). | MATH |
| N14 | The S3 "height-only" law fails for narrow footprints (×2.8–8.8), hotspots (×2–6), resistive garments (×3) and failed contacts (×1.2–9.7). | NUM |
| N15 | Self-powered convex transitions are infeasible below ~100 µm. Neighbour-actuated passive transit is required. | MATH |
| N16 | Bolt actuation at 5 V does not fit below ~100 µm (comb area > face area). | MATH |

**Retracted:** S7's 60 s build time (now ~150 s with thick-slab feed); S2's ~7 kPa (now 5.7 kPa); 4 nJ per step (now 15–40 nJ).

**Strengthened:**
- Every ISL shape change is reversible (MATH proof).
- Extrusion is legal in 3D (NUM).
- ISL can form cantilever branches (NUM).
