"""SESSION 3 / MECHANICAL-MEMS FAMILY: kill-parameter screening at 10 mm ... 10 um.

Each mechanism is tested against the requirement that dominates at small scale:
the peel/adhesion load F_adh (humid capillary at 9 standoff bumps, R = 0.5 um, ~4.1 uN total;
scaled bumps for L < 100 um noted), plus a lattice-step energy and heat
budget for a 10^7-module swarm.
Evidence class: MATHEMATICAL DERIVATION using literature values marked SNIPPET
(see MECHANICAL_ACTUATION.md). Run: python3 sims/s3/mechanical.py -> results/s3_mechanical.md
"""
import math, os
EPS0 = 8.854e-12
SIZES = [10e-3, 1e-3, 300e-6, 100e-6, 10e-6]
F_ADH = 9 * 4 * math.pi * 0.5e-6 * 0.072          # 4.1e-6 N humid (9 bumps, full meniscus)

def zip_torque(L, V, theta, t=0.1e-6, er=4.0):
    """Electrostatic zipping between two rigid plates hinged at an edge, opening angle theta:
    T = eps0 V^2 w / (2 theta^2) ln(1 + L theta er / t)."""
    return EPS0 * V**2 * L / (2 * theta**2) * math.log(1 + L * theta * er / t)

def main():
    R = ["# Session 3 — mechanical / MEMS mechanisms: kill-parameter screen (MATHEMATICAL DERIVATION)\n"]
    R.append(f"Reference resistance: humid peel/adhesion F_adh ~ {F_ADH*1e6:.1f} uN at 9 bumps (constant with L unless bumps are scaled); "
             "peel torque = F_adh L; weight = rho g L^3.\n")
    R.append("## 1. Electrostatic zipping hinge (rigid plates) - torque at 90 deg and 10 deg opening vs peel torque\n")
    R.append("| L | V | T(90 deg) | T(10 deg) | peel torque | margin @90 | margin @10 |\n|---|---|---|---|---|---|---|")
    for L in SIZES:
        for V in (30, 100):
            T90 = zip_torque(L, V, math.pi / 2); T10 = zip_torque(L, V, math.radians(10))
            pt = F_ADH * L + 2330 * L**3 * 9.81 * L / 2
            R.append(f"| {L*1e6:.0f} um | {V} | {T90:.2e} | {T10:.2e} | {pt:.2e} | {T90/pt:.2g} | {T10/pt:.2g} |")
    R.append("\nKill parameter: torque at large opening angle. Rigid zipping cannot start a 90 deg fold against adhesion at any size "
             "(<1e-1 margin); it works only for the last ~10 deg (closing/latching) or with compliant curved electrodes.\n")
    R.append("## 2. Gap-closing electrostatic inchworm with ratchet pawls on a neighbour's rack\n")
    R.append("Force density 1.38-1.8 mN/mm^2 at 100-110 V (Penskiy/Contreras, SNIPPET), ~V^2 scaling; actuator footprint 20 % of one face.\n")
    R.append("| L | F at 100 V | F at 30 V | resistance (adhesion) | margin @30 V |\n|---|---|---|---|---|")
    for L in SIZES:
        A = 0.2 * L**2 * 1e6           # mm^2
        F100 = 1.5e-3 * A; F30 = F100 * (30 / 100)**2
        R.append(f"| {L*1e6:.0f} um | {F100*1e6:.3g} uN | {F30*1e6:.3g} uN | {F_ADH*1e6:.1f} uN | {F30/F_ADH:.2g} |")
    R.append("\nKill parameter: force density x footprint vs adhesion -> inchworms fail below ~300 um at CMOS-like voltages; need ~100 V. "
             "Strength advantage: pawls on rack teeth carry shear by tooth strength (no slip planes).\n")
    R.append("## 3. Electrothermal (chevron/bimorph) - energy and swarm heat\n")
    R.append("Force per power ~10 mN/W (50 mN at 4.75 W chevron, SNIPPET; optimistic for scaling). Required force 3x adhesion; 10 ms per step.\n")
    R.append("| L | power per actuator | energy per step | swarm heat, 1 % of 1e7 modules moving |\n|---|---|---|---|")
    for L in SIZES:
        F = 3 * F_ADH + 2330 * L**3 * 9.81
        P = F / 1e-2
        R.append(f"| {L*1e6:.0f} um | {P*1e3:.3g} mW | {P*1e-2*1e6:.3g} uJ | {P*1e5:.3g} W |")
    R.append("\nKill parameter: energy per step (~1e3x electrostatic). 1 % duty of a 1e7 swarm dissipates ~1 W - feasible only for small swarms or rare moves.\n")
    R.append("## 4. Piezoelectric thin film (AlN) stepping\n")
    R.append("Stroke ~1.3 um at +-60 V (SNIPPET); stepping a lattice pitch L needs L/1.3um strokes, each requiring clamp/release.\n")
    for L in SIZES:
        R.append(f"- L = {L*1e6:.0f} um: {L/1.3e-6:.0f} strokes per lattice step")
    R.append("\nKill parameter: stroke per volt (needs a clutch/ratchet; adds the inchworm's clamp problem). Kept only as a clutch actuator candidate.\n")
    R.append("## 5. Capillary / microfluidic actuation and bonding\n")
    for L in SIZES:
        tevap = (L * 0.1)**2 / (2 * 2.5e-5 * 0.5 * 0.02)   # crude diffusion-limited evaporation of a meniscus of size 0.1 L at 50 % RH
        R.append(f"- L = {L*1e6:.0f} um: meniscus of 0.1 L evaporates in ~{tevap:.2g} s at 50 % RH (order-of-magnitude, diffusion-limited)")
    R.append("\nKill parameter: liquid retention in ordinary air (seconds or less at <= 100 um). Rejected outside sealed/liquid environments.\n")
    R.append("## 6. Shape-memory alloy films\n")
    R.append("Work density high (>=5e6 J/m^3, SNIPPET) but cycle time thermally limited (20-300 Hz in films) and efficiency low; shares the electrothermal energy problem. "
             "Kept only as a one-shot or rare-event latch actuator.\n")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s3_mechanical.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
