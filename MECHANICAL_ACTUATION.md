# MECHANICAL_ACTUATION — MEMS and mechanical locomotion (session 3)

Labels follow MAGNETIC_ACTUATION.md. Code: `sims/s3/mechanical.py` → `results/s3_mechanical.md`.

Reference load: the humid adhesion peel force, ≈ 4.1 µN at 9 standoff bumps of radius 0.5 µm. Below about 1 mm this load, not gravity, decides feasibility.

## 1. Literature inputs (LITERATURE-SNIPPET unless stated)

- **Polysilicon sidewall wear in air (Alsem/Ritchie):** 3 of 7 devices failed at about 10⁵ cycles after friction spiked to 3× its initial value. Steady-state μ ≈ 0.20 ± 0.05 from an initial 0.11; debris 50–100 nm.
- **Sandia microengines:** wear dominates failure. Humidity effects run in both directions across studies.
- **Sandia friction stepper:** μ rose from 0.2 to 0.45 with wear; life > 7×10⁵ cycles.
- **Polyimide hinges:** about 7×10⁴ cycles (RoboBee flapping) to 3×10⁵ cycles (sub-gram flyer). The 10⁷ figure applies only at stress ≤ 50 MPa.
- **Freestanding Au film:** failure strain < 1.5 % (bulge test).
- **Si snap fastener:** about 30 µN insertion force for 50×2 µm beams. Retention and mating-cycle life: **not found**.
- **SUMMiT ratchets:** 4 µm tooth pitch, 8 µm per actuation.
- **Electrostatic inchworms:** 1.38–1.8 mN/mm² at 100–110 V; 2.4×10⁷ cycles (session 1).
- **Chevron electrothermal:** 50 mN at about 4.75 W.

## 2. Kill-parameter screen (MATHEMATICAL DERIVATION)

| Mechanism | Kill parameter | Result | Verdict |
|---|---|---|---|
| Rigid electrostatic zipping hinge (fold or pivot) | Torque at large opening angle | At 90°, torque/peel < 0.04 at every size, even at 100 V. At 10° it is 0.2–2.5. | **Rejected as a fold or pivot actuator.** Keep only for final-approach latching. |
| Gap-closing inchworm + ratchet pawls on a neighbour's rack | Force density × footprint at ≤ 30 V | Margin 6.6 at 1 mm, 0.6 at 300 µm, 0.07 at 100 µm. Needs about 100 V below 300 µm. | Viable at ≥ 1 mm. Below that, only with on-chip high voltage. |
| Electrothermal (chevron, bimorph) | Energy per step | 1–10³ µJ per step; ~1 W per 10⁵ moving modules | Rare-event latch only |
| Piezoelectric (AlN) | Stroke per volt (1.3 µm at 60 V) | 77–7700 strokes per lattice step | Clutch actuator only |
| Capillary / microfluidic | Liquid retention in air | A 0.1 L meniscus evaporates in ≪ 1 s at ≤ 100 µm (order of magnitude) | **Rejected** for ordinary environments |
| SMA films | Energy and cycle rate | Electrothermal-class energy; 20–300 Hz | Rare-event latch only |
| **Any sliding-contact locomotion in air** | Wear life | About 10⁵ cycles in polysilicon (SNIPPET), against 10⁶–10⁸ moves of programmable-matter duty | **Major new risk** for SISL and ISL-PE. Coatings (DLC, W, SAM) need testing. |

## 3. Separating propulsion from load-bearing attachment

The brief asked whether a strong passive connection can coexist with a weak actuator. The analysis found three ways:

1. **Pivot + pins (NEPL, NEW_MECHANISMS.md).**
   - Conical pins carry shear: about 9.4 MPa face-equivalent.
   - The pins engage and disengage only along the face normal, which is the direction a pivot approaches and leaves.
   - The actuator must overcome only peel adhesion: about 4 µN, against about 94 mN of pin strength at 100 µm.
   - This separation is geometric, not material.
   - MATHEMATICAL DERIVATION + NUMERICAL SIMULATION.
2. **Inchworm with ratchet pawls (≥ 1 mm).** Rack teeth carry shear, and one pawl set is always engaged. The weak actuator moves only the unloaded pawl. MATHEMATICAL DERIVATION.
3. **Port-engaged cam latches (ISL-PE, session 2).** Still untested.

## 4. What remains unverified

- Wear and debris for pin landings, as opposed to sliding.
- Snap-fit retention and cycle life.
- Real zipping devices with compliant electrodes: the analysis assumed rigid plates, and compliant designs may do better.
- Coatings that move sliding-contact life past 10⁷ cycles.
