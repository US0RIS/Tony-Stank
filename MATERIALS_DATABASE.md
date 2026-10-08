# MATERIALS_DATABASE — magnetic materials for NEPL (session 4)

**Evidence status:** every value below was seen only in search-result summaries (SNIPPET). The proxy blocked publisher full text for all sources. **No value is a verified primary measurement.** Values marked "bulk" must not be used for films without justification.

## 1. Switchable (semi-hard) candidates

| Material | Jr / Br | Hc | Squareness | Thickness | Process | Source | Status |
|---|---|---|---|---|---|---|---|
| Electroplated CoP | ≈ 0.65 T | ≈ 28 kA/m | not reported | not reported | plated, no anneal | Metals (MDPI) Jan 2022, doaj 83ac5564b92243b49c01d299d1b561f5 | SNIPPET |
| Electroplated CoNiP | ≈ 0.40 T | ≈ 45 kA/m | not reported | not reported | plated | same | SNIPPET |
| Co-rich CoPtP | ≈ 0.35 T (unit ambiguous) | ≈ 92 kA/m | not reported | 82 µm | plated | UCC research portal (2010 JMMM) | SNIPPET |
| CoPtP after 300 °C anneal | Mr 379 → 486 emu/cc | 174 → 242 kA/m | — | — | anneal | source unidentified | SNIPPET |
| Sputtered FeCoV (Vicalloy) | not found | ≈ 24 kA/m in-plane | not found | — | sputtered | source URL not captured | SNIPPET |
| AlNiCo films | **not found** | — | — | — | — | — | NOT FOUND |
| Microfabricated EPM (UF, 2020 poster): plated CoPt hard + screen-printed AlNiCo | no numbers | — | — | 60–80 µm | hybrid | eng.ufl.edu/nimet/?p=6149 | SNIPPET (qualitative) |

**Answer to the gating question:** no demonstrated microfabricated film combining Br ≥ 0.5 T, Hc 10–150 kA/m and squareness ≥ 0.8 was found.
- CoP is used as the **best available substitute**. It has Jr 0.65 T, but its squareness is **unknown** and is swept over 0.5–1.0 in the models.
- This is an explicit substitution: CoP is not a demonstrated EPM material.

## 2. Hard (non-switchable) films

| Material | Br | Hc | Max thickness | Anneal | Source | Status |
|---|---|---|---|---|---|---|
| Sputtered NdFeB (Institut Néel) | 1.3–1.4 T | μ₀Hc ≈ 1.6–2 T (≈ 1.3–1.6 MA/m) | ≤ 50 µm | ≥ 650 °C | arXiv cond-mat/0703785; magneticsmag 2021 | SNIPPET |
| Electroplated L1₀ CoPt (Arnold) | ≈ 0.8 T | ≈ 800–1000 kA/m | 6 µm (squareness 0.9) to 100 µm | 675 °C, 30 min | doi:10.1016/j.jmmm.2016.05.044; UF IMG | SNIPPET |
| Sputtered SmCo | ≈ 0.8 T (ambiguous) | — | 5 µm | 350 °C | arXiv 0804.1992 | SNIPPET |
| Bonded NdFeB powder | 0.36–0.69 T | 680–720 kA/m | — | low-T | doi:10.1109/MEMSYS.2012.6170220 | SNIPPET |

Hard films cannot be switched by on-chip coils: Hc ≈ 1 MA/m needs about 25× the field of CoP. They can serve only as fixed-polarity elements (ON/OFF EPM with a semi-hard partner), which **cannot reverse polarity**, so they cannot push.

## 3. Bulk reference values (NOT film values)

| Material | Br | Hc | Source |
|---|---|---|---|
| AlNiCo 5 | 1.25–1.28 T | 45–51 kA/m | Eclipse Magnetics datasheet (SNIPPET) |
| AlNiCo 9 | 1.06 T | ≈ 119 kA/m | MCE Products (SNIPPET) |
| FeCrCo | 0.8–1.3 T | 40–52 kA/m (vendors disagree: 50–300) | All Star Magnetics; Eclipse (SNIPPET) |

## 4. Soft magnetic and conductor values (handbook, ASSUMED representative)

| Material | Property | Value | Use |
|---|---|---|---|
| NiFe 80/20 (plated) | B_sat | ≈ 0.8–1.0 T | pole pieces (saturation check) |
| NiFe 45/55 | B_sat | ≈ 1.5–1.6 T | alternative |
| Cu (plated) | ρ | 1.7×10⁻⁸ Ω·m; c_v 3.45 MJ/m³K | coils |
| Au | ρ | 2.2×10⁻⁸ Ω·m; H ≈ 1 GPa; softening ≈ 0.08 V, melting ≈ 0.43 V (Holm, textbook) | contacts |
| Polyimide | k | ≈ 0.15 W/m·K | coil insulation (thermal bottleneck) |

## 5. Missing properties and required improvements

These are quantified in FEASIBILITY_VERDICT.md, which takes them from the integrated model:
1. Squareness and reversal time of plated CoP/CoNiP elements at 4 × 12 × 58 µm: not measured anywhere found.
2. Remanence × thickness product achievable in a switchable film inside a 12 µm skin. It sets the face flux, and the integrated model shows it is the binding constraint.
3. Minor-loop stability under 2–8 kA/m cross-talk fields.
4. Pulsed current-density limit of 3 µm-pitch Cu micro-solenoids (only DC failure ≈ 3.6×10⁹ A/m² found).
