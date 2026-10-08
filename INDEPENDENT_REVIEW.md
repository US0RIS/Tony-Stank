# INDEPENDENT_REVIEW — adversarial review of the integrated NEPL design (session 4)

Four independent reviewers were each instructed to find the strongest failure reason, to compute independently rather than reuse the principal model, and not to modify the repository.

| Reviewer | Responsibility | Model |
|---|---|---|
| R1 | Magnetic materials and switching | Haiku |
| R2 | EM field and thermal calculations | Sonnet |
| R3 | Mechanical integration and fabrication | Sonnet |
| R4 | Independent falsification of the full design | Sonnet |

Their scratch work is outside the repository. The summaries below are the principal investigator's condensation; numbers are the reviewers'.

## R1 — materials and switching

**Strongest failure:** the open-circuit remanence margin.
- An independent surface-charge demagnetisation calculation (cube check N = 0.3334) gives N = 0.044–0.050 for the 58 × 12 × 4 µm bar. The self-field is 23–26 kA/m against Hc 28 kA/m: a margin of 2–5 kA/m (7–18 %).
- An open return through pole pieces and ~100 µm of air could raise the reverse field to about 0.6·M_r, roughly 300 kA/m. That is a bound, not a result.
- Cross-talk (1.7–4.9 kA/m) is the same size as the margin. Minor-loop creep is reported in other Co-based stacks (snippet).
- No squareness, reversal time or thermal coefficient was found for plated CoP or CoNiP (snippet-level search).
- **Required:** knee field ≥ ~40 kA/m with Mr/Ms ≥ 0.9.

**Resolution:** agrees with `demag_contacts.py` (N = 0.050, 25.8 kA/m). **Accepted.**

## R3 — mechanics and fabrication

**Strongest failure: no realisable pivot hinge.**
- Any captured hinge either protrudes on the other edges, blocking face-to-face attachment and other pivot axes, or needs a handed (chiral) bar/hook arrangement. A handed arrangement is incompatible with identical modules in arbitrary orientations; this mirrors the pin result in `pins.py`.
- Magnetic retention near the edge falls from tens of µN at contact to about the module weight within ~5°.

**Second: alignment.**
- Six-tile assembly of 100 µm parts gives ±1.5–2 µm stack-up against 1 µm clearances.
- Reproduced in `fab_yield.py`: 17–57 % of modules have all 6 faces aligned, and module yield is ~10–15 % at 100 µm.

**Also:**
- Pin-tip impact stress is ~2–4 GPa at 2 m/s (fracture 1–3 GPa), so landing speed must stay below ~0.3–0.5 m/s.
- At 1e7 modules, testing and sorting become the bottleneck.

**Resolution:** the hinge finding is accepted. It is consistent with the pivot-model requirement for a hinge reaction (`cycle_dynamics.py` reports whether the mover is pushed off the pivot). The impact-stress scaling is used in MECHANICAL_CYCLE.md.

**Disagreement (preserved):**
- R3's dipole far-field estimate (19 nN at one module spacing) is cruder than the FD model, which resolves pole pieces and gaps.
- The FD near-contact forces (µN scale) and R3's estimate differ in method but agree in order of magnitude near contact.

## R4 — full-design falsification (hand estimates; the FD pivot results were not yet available)

**Ranked failures:**

1. **Force is ~100× lower than session 3 assumed.**
   - Bar flux into 8 µm pole pieces caps B at ≤ 0.19 T over 6.6 % of the face, giving a 5–9 µN face clamp versus the claimed ~1.25 mN.
   - The FD model gives 2 µN (`demag_contacts.py`). Agreement: same order, the FD includes the gaps and leakage.
   - At mid-swing, two-pole-face forces decay on ~21 µm, a further 16–1000× reduction.
2. **Pulse delivery through pads.**
   - With 1–2.5 µN per pad, contacts see 0.1–0.4 V at 0.2–0.8 A, which is softening to melting.
   - The FD clamp is lower still (0.25 µN per pad), so the principal model is *more* pessimistic.
3. **Mover demagnetisation under push.**
   - A like pole 1–10 µm away, concentrated by the mover's pole pieces, applies several times Hc in reverse.
   - The FD model records the maximum reverse H in the magnets (`s4_pivot_real_100.md`).

**Verdicts:** 100 µm needs a breakthrough; 300 µm needs experiment.

**Resolution:** see FEASIBILITY_VERDICT.md. R4's observation that the 0.407 A vs 0.33 A coil currents differ is explained by the assumed 0.8 MMF efficiency (0.33/0.8 = 0.41). **No error.**

## R2 — EM field and thermal calculations (independent code: Biot–Savart, energy-method FD solver)

**Reproduced:**
- Field per ampere: centre 3.07×10⁵, minimum 1.29×10⁵ A/m/A.
- Coil resistance, inductance and thermal time constant.
- Pivot torques within 2–4 %.
- The 45–170× torque shortfall at 100 µm, which R2 rates as the strongest failure.

**Errors found (all flatter the design), and fixes applied:**

| Finding | Effect | Fix |
|---|---|---|
| End-turn placement (`linspace` to the coil edges) | min field 37 % too high, so current 1.6× too low and power 2.5× too low | **FIXED**: turns centred at true pitch |
| No resistivity rise with temperature | adiabatic rise ~1.8× too low | **FIXED**: α = 0.0039/K, constant current |
| Driver silicon density 0.5 µm²/µm optimistic | area 2–4× too low | **FIXED**: 1–2 µm²/µm, giving 62–124k µm² vs 10.9k available |
| Infeasible rows unflagged | — | **FIXED**: flag column |
| Arithmetic iron mixing in partial cells | force +1 % grid-aligned to +12.5 % half-cell offset; pivot torque +2–4 % | **Documented**, not changed. It flatters the design, so the failure verdict is conservative. |
| Stale "max B in iron" (31–36 T) in the first output | — | **FIXED**: interior-cell check, report regenerated (0.33–0.65 T). R2 notes the value still rises at corners, so local saturation cannot be excluded. |
| `legacy_validation` does not exercise iron, recess or gaps | — | Accepted. R2's own iron-terminated test agrees within 1 % grid-aligned. |

**Unresolved (preserved):**
- The η = 0.8 MMF-efficiency constant remains an assumption.
- The humid-peel requirement (9 bumps, full meniscus) was not independently audited.
