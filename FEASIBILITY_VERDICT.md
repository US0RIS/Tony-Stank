# FEASIBILITY_VERDICT — NEPL (session 4)

## Central question

Can a complete NEPL module with a 100 × 100 × 100 µm envelope be built from materials and processes that exist, and produce enough controllable magnetic torque to execute its movements?

## Verdict at 100 µm: **D — physically infeasible under the tested constraints**

The tested constraints are: an ordinary humid environment, the best demonstrated switchable magnetic film, and an integrated geometry in which every component occupies space.

**Decisive limiting mechanism: flux starvation of switchable thin-film magnets against surface adhesion.**
- Inside a 12 µm face skin shared with coils, pole pieces, pins, pads and clearances, each face can hold two 4 µm-thick switchable bars.
- Their flux reaches the neighbour through pole pieces covering 6.6 % of the face. The attached clamp is 2 µN (0.2 kPa) and the start torque is 5–6 % of the humid peel torque (NUMERICAL, mesh-checked, and confirmed in order of magnitude by reviewers R2 and R4).
- Magnetic torque scales as L³ while adhesion scales as L.

**Evidence:**
- 90° and 180° worst margins of 0.022 and 0.006, against session-3 claims of 4.5 and 2.0.
- The solver error found by R2 inflates torque by 2–12 %, so correcting it makes the result slightly worse.

**Why no material fixes it (MATHEMATICAL, `verdict_numbers.py`):**
- Recovering a 2× start margin at 100 µm in humid air needs Jr·squareness ≈ **3.2 T**. That exceeds the saturation polarisation of every known material (~2.4 T, FeCo).
- Even with engineered 10×-lower adhesion, it needs a **≥ 1.0 T switchable film**. No such microfabricated film was found: the best is CoP at 0.65 T with unknown squareness.

**Independent failures at 100 µm, each sufficient on its own (with R2's corrections):**
1. **Switching drivers:** 62,000–124,000 µm² of silicon needed, against 10,952 µm² available.
2. **Coil current density:** ≥ 1×10¹¹ A/m², about 30× the measured DC failure value.
3. **Pulse delivery:** must come through contacts clamped at 0.25 µN per pad. That exceeds the Au softening voltage. Local storage would need ~2,900 module volumes.
4. **Alignment:** six-sided assembly tolerance (±1.5–2 µm) against 1 µm clearances: 10–15 % module yield.
5. **Demagnetisation margin:** 2–5 kA/m, comparable to the coil cross-talk (R1).

## Larger sizes (integration analysis repeated, not inferred)

| Size | Verdict | Basis |
|---|---|---|
| **300 µm** | **C — requires specific advances** | Humid start margin 0.47–0.54 (× 3D derate 0.5–1), so it **fails** in ordinary air. It works only with (a) engineered surfaces cutting humid adhesion ~10× (start margin 4.7–5.4) or (b) a switchable film with Jr·sq ≥ ~1 T. It also needs magnetisation reversal ≤ ~1 µs (otherwise 154 K per pulse), the unmeasured CoP loop squareness, and a departure hinge compatible with identical modules (unresolved). Drivers, alignment and yield (58–87 %) pass. |
| **~0.6–0.9 mm** | **B — plausible, requires experimental validation** | Smallest size with a ≥ 2× humid start margin using CoP (620 µm at derate 1.0; 880 µm at 0.5). |
| **1 mm** | **B — plausible, requires experimental validation** | Humid start margin 5.2–6.0 × derate. Switching is thermally comfortable (≤ 13 K at 10 µs), drivers fit, current density 1.2×10¹⁰ A/m², alignment is not limiting, landing 0.25 m/s. **Remaining unverified:** CoP loop squareness and reversal time; contact design for 1–2 A pulses; the departure hinge; a six-sided assembly route (hybrid assembly with sintered micro-magnets is plausible but is a substitution). |

**Smallest size for which a defensible design exists: about 0.6–1 mm in ordinary humid air, verdict B.** Around 0.2–0.3 mm becomes reachable only with engineered low-adhesion surfaces or a ≥ 1 T switchable film, verdict C.

## Comparison with the session-3 claims (retractions)

| Session-3 claim | Status |
|---|---|
| NEPL torque margins 4.5 / 2.0 at 100 µm | **Retracted.** Integrated value 0.022 / 0.006. |
| "Credible at 300 µm" | **Downgraded** to C. |
| ~100 kPa magnetic attachment, particle-tolerant (M5) | **Retracted for switchable faces.** It holds only for hard-magnet face-normal sheets, which cannot be switched. The integrated switchable face gives 0.2 kPa at 100 µm. |
| 145 nJ per move at 100 µm | **Retracted.** 1.3–5 µJ per switch, several switches per move. |
| Landing at ~2 m/s requiring braking | **Superseded.** With realistic torques, ~0.25 m/s. |
| Mover passivity | **Survives** at the magnetics level (isolated mover: no magnet volume above Hc mid-pivot). Departure needs a captive hinge. |

## What would change the verdict at 100 µm

All of these would be required together:
1. A switchable film with Jr·sq ≥ 1 T and a square loop, about 2× beyond the best film found.
2. Surface adhesion reduced ≥ 10× in ordinary air.
3. A coil/driver technology delivering about 0.3–0.6 A pulses within about 10⁴ µm² of silicon.
4. A pulse-delivery path that does not depend on 0.25 µN contacts.
5. ±0.3 µm six-sided assembly.

Items 1 and 2 alone are not sufficient because of items 3–5. **The architecture-level conclusion is that magnetically actuated, switchable-attachment lattices do not scale to 100 µm with thin-film magnets.** The 100 µm goal needs a different force mechanism: one whose force density does not depend on magnet volume fraction, or that does not have to overcome adhesion with body forces.

## Evidence classes

- NUMERICAL: torque, clamp, dynamics, geometry, pins.
- MATHEMATICAL: scaling, thermal, demagnetisation, Holm contacts, yield bookkeeping.
- LITERATURE-SNIPPET: all material properties.
- **No experiment was performed.**
