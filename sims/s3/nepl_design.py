"""SESSION 3 / PHASE 5. NEPL design budgets (MATHEMATICAL DERIVATION; ENGINEERING HYPOTHESIS
where marked). Neighbour-actuated Electropermanent Pivoting Lattice:
  - movers are passive in transit; stationary neighbours' EPM faces push (repel) and pull (attract)
  - switchable EPM attachment (closed magnetic circuit through the neighbour's pole pieces)
  - conical Si shear pins engage along the face normal at the end of each pivot
  - edge-hinge EPM strips capture the pivot edge during rotation
  - power/data through pole pieces and pin contacts, clamped by the magnetic attachment (no sliding contacts)
Run: python3 sims/s3/nepl_design.py -> results/s3_nepl_design.md
"""
import math, os
MU0 = 4e-7 * math.pi

def attach_pressure(L, gap, Br=1.0, frac=0.5, derate=0.5):
    l_m = 0.4 * L
    B = Br * l_m / (l_m + 2 * gap * 1.05)
    return derate * frac * B**2 / (2 * MU0)

def holm_R(F, rho=2.2e-8, H=1e9, film_factor=10.0):
    a = math.sqrt(F / (math.pi * H))
    return film_factor * rho / (2 * a)

def main():
    R = ["# Session 3 — NEPL design budgets (MATHEMATICAL DERIVATION; numbers marked ASSUMED are engineering hypotheses)\n"]
    R.append("## 1. Attachment pressure with contaminants (closed-circuit EPM, Br = 1.0 T, pole fraction 0.5, x0.5 leakage derate ASSUMED)\n")
    R.append("| L | clean (0.1 um) | 1 um particle | 5 um particle | 15 um lint fibre |\n|---|---|---|---|---|")
    for L in (1e-3, 300e-6, 100e-6):
        R.append(f"| {L*1e6:.0f} um | " + " | ".join(f"{attach_pressure(L, g)/1e3:.0f} kPa" for g in (0.1e-6, 1e-6, 5e-6, 15e-6)) + " |")
    R.append("\nStructural use (session-1 S5 formula): 1 N at the tip of a 10 cm arm needs p = 6Fl/h^3: 75 kPa for a 2 cm square section, 600 kPa for 1 cm. "
             "NEPL tension capacity (~50 kPa derated) supports ~1 N at 10 cm only for sections >= ~2.3 cm, or lighter loads. Weaker than ISL interlocks, "
             "but switchable and particle-tolerant.\n")
    R.append("## 2. Shear pins (Si, conical, diameter 0.2 L, design shear strength 300 MPa)\n")
    for L in (1e-3, 300e-6, 100e-6):
        F = 300e6 * math.pi * (0.1 * L)**2
        h = 0.1 * L; cap = h * math.tan(math.radians(30))
        R.append(f"- L = {L*1e6:.0f} um: pin shear capacity {F*1e3:.3g} mN = {F/L**2/1e6:.2f} MPa face-equivalent; "
                 f"lateral capture range with 30 deg cone of height 0.1 L: +-{cap*1e6:.1f} um")
    R.append("\nPins remove ISL's slip-plane weakness (shear ~9.4 MPa face-equivalent >> 0.1 MPa need). They forbid sliding moves, which NEPL never uses.\n")
    R.append("## 3. Electrical contacts clamped by the magnet (Holm, Au, H = 1 GPa, x10 film factor ASSUMED; 4 pads per face, each 5 % of face area)\n")
    R.append("| L | force per pad (clean) | R per pad | face R (4 pads parallel) | reach h_max (hops) at 10 nW, 3 V, G = 5 |\n|---|---|---|---|---|")
    for L in (1e-3, 300e-6, 100e-6):
        F = attach_pressure(L, 0.1e-6) * 0.05 * L**2 / 0.5      # pad sees full pole pressure ASSUMED
        Rp = holm_R(F); Rf = Rp / 4
        h = math.sqrt(0.2 * 9 / (1e-8 * 2 * Rf * 5))
        R.append(f"| {L*1e6:.0f} um | {F*1e6:.0f} uN | {Rp:.2f} ohm | {Rf:.3f} ohm | {h:.0f} |")
    R.append("\nThe magnet supplies 10^1-10^4 uN contact force that electrostatic attachment cannot, giving sub-ohm landed contacts. "
             "Contacts are made and broken cold (power to that face switched off during transit), avoiding hot-switching wear.\n")
    R.append("## 4. Hinge capture (edge EPM strips; required 112-125 uN at 100 um from mag_pivot.py)\n")
    for L, need in ((1e-3, 12.5e-3), (300e-6, 1.12e-3), (100e-6, 125e-6)):
        area = 0.1 * L * L
        cap = 0.5 * 1.0**2 / (2 * MU0) * area
        R.append(f"- L = {L*1e6:.0f} um: edge strip (0.1 L x L, Br 1 T, x0.5 derate) holds ~{cap*1e6:.0f} uN vs {need*1e6:.0f} uN required -> margin {cap/need:.1f}")
    R.append("\nMargin ~1.6 at all sizes: hinge capture is geometric (same scaling as the push), so it neither improves nor fails with size. "
             "A mechanical knuckle hook (Si, 15 mN-class at 100 um) is the fallback.\n")
    R.append("## 5. Landing impact (inertial pivot, from cycle_compare.py)\n")
    for L, E in ((1e-3, 4.62e-6), (300e-6, 1.25e-7), (100e-6, 4.62e-9)):
        m = 2330 * L**3
        v = math.sqrt(2 * E / m)
        R.append(f"- L = {L*1e6:.0f} um: landing energy {E*1e9:.3g} nJ -> edge speed ~{v:.2f} m/s if undamped. Requires braking: switch the pull off at ~60 deg "
                 "(reverse-pulse) and rely on squeeze-film damping in the last ~1 um (ESTIMATE; rarefied-gas effects below ~0.1 um reduce it).")
    R.append("\nLanding speed is size-independent (torque ~L^3, energy ~L^3, mass ~L^3), so braking is needed at every scale.\n")
    R.append("\n## 6. Energy and heat for a garment-scale reconfiguration\n")
    for L, Emove in ((300e-6, 1.31e-6), (100e-6, 1.45e-7)):
        N = 1e-5 / L**3
        moves = 0.1 * N * 10
        E = moves * Emove
        R.append(f"- L = {L*1e6:.0f} um, 10 cm^3 object: {N:.2e} modules; reshaping 10 % of them by 10 moves each = {moves:.2e} moves, "
                 f"{E:.3g} J of switching energy (battery 15 Wh = 54 kJ).")
    R.append("\n## 7. Fabrication requirements (ENGINEERING HYPOTHESIS)\n"
             "- Sputtered NdFeB (Br ~1.3-1.4 T, up to 50 um thick, 650 C anneal; Dempsey/Grenoble, SNIPPET) -> magnets must be made before CMOS or on a separate die (chiplet assembly).\n"
             "- Switchable (semi-hard, Hc <= 20 kA/m, square loop) microfabricated film: NOT FOUND in literature search -> the single most uncertain material.\n"
             "- Electroplated Cu planar/multilayer coils; pulsed 1 us at 1-2e10 A/m^2 (above the 3.6e9 A/m^2 DC failure value found, SNIPPET; adiabatic dT ~2 K computed).\n"
             "- DRIE Si bodies, conical pins, NiFe pole pieces; 6-face assembly (folding or die stacking). Credible at 1 mm, plausible at 300 um, unproven at 100 um.\n")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s3_nepl_design.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
