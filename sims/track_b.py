"""TRACK B. Quantitative requirements for independently mobile, fully
reconfigurable microscopic modules. ANALYTIC throughout (no experiment exists).

B1 switchable mechanical bolt latch (decouples holding force from actuation force)
B2 bolt actuator: can an onboard electrostatic actuator move it?
B3 adhesion engineering needed to slide below 20 um
B4 power across convex transitions: hold-up vs neighbour-actuated passive transit
Run: python3 sims/track_b.py -> results/track_b.md
"""
import math, os
EPS0, GAMMA = 8.854e-12, 0.072

def main():
    R = ["# TRACK B — requirements for fully mobile microscopic modules (ANALYTIC)\n"]
    R.append("## B1. Bolt latch: holding pressure vs module size\n")
    R.append("Si bolt of width b = 0.1 L, thickness t = 0.05 L, design shear strength 300 MPa (Si fracture 1-3 GPa, x3-10 safety); "
             "two bolts per face. Equivalent interface tensile pressure = 2 tau b t / L^2.\n")
    R.append("| L | bolt b x t | holding force | equivalent pressure | vs 0.6 MPa need |\n|---|---|---|---|---|")
    for L in (1e-3, 100e-6, 30e-6, 10e-6):
        b, t = 0.1 * L, 0.05 * L
        F = 2 * 300e6 * b * t
        p = F / L**2
        R.append(f"| {L*1e6:.0f} um | {b*1e6:.1f} x {t*1e6:.1f} um | {F*1e3:.3g} mN | {p/1e6:.1f} MPa | x{p/0.6e6:.0f} |")
    R.append("\nGeometric scaling: pressure = 2 tau (b/L)(t/L) is size-INDEPENDENT; bolts keep MPa-class strength at any L that lithography can resolve.\n")
    R.append("## B2. Can an onboard electrostatic actuator stroke the bolt (unloaded)?\n")
    R.append("Resistance = guide adhesion/friction ~ mu x (capillary at 2 contacts, R_asp=0.2 um) -> F_res ~ 0.4 x 2 x 4 pi R gamma. "
             "Comb drive force = N x eps0 t V^2 / g (both sides).\n")
    Fres = 0.4 * 2 * 4 * math.pi * 0.2e-6 * GAMMA
    R.append(f"F_res ~ {Fres*1e9:.0f} nN (humid); x3 margin -> {3*Fres*1e9:.0f} nN.\n")
    R.append("| L | finger t = 0.05 L | gap | V | fingers needed | comb area (fraction of L^2 face) |\n|---|---|---|---|---|---|")
    for L in (1e-3, 100e-6, 30e-6):
        t = 0.05 * L
        for V, g in ((5, 0.5e-6), (30, 1e-6)):
            f1 = EPS0 * t * V**2 / g
            N = math.ceil(3 * Fres / f1)
            area = N * 2 * (g + 1e-6) * 10e-6          # pitch ~2(g+w), finger length 10 um
            R.append(f"| {L*1e6:.0f} um | {t*1e6:.1f} um | {g*1e6:.1f} um | {V} V | {N} | {area/L**2:.2f} |")
    R.append("\nAt 100 um a 30 V comb fits (~4 % of a face); a 5 V comb needs ~60 % of a face per bolt -> bolts on all six faces do not fit at 5 V "
             "below ~100 um. Requirement: >=20-30 V local actuation or a force-amplifying (inchworm/ratchet) bolt drive.\n")
    R.append("## B3. Adhesion budget for sliding below 20 um (face drive at 5.7 kPa realistic, margin 5, mu 0.4)\n")
    R.append("| L | thrust | max total adhesion | bump R if capillary (3 bumps) | bump R if dry SAM, W=0.02 J/m^2 (3 bumps) |\n|---|---|---|---|---|")
    for L in (30e-6, 20e-6, 10e-6, 5e-6):
        T = 5.7e3 * 0.6 * L**2
        Fmax = T / (5 * 0.4)
        Rc = Fmax / 3 / (4 * math.pi * GAMMA)
        Rd = Fmax / 3 / (1.5 * math.pi * 0.02)
        R.append(f"| {L*1e6:.0f} um | {T*1e9:.0f} nN | {Fmax*1e9:.0f} nN | {Rc*1e9:.0f} nm | {Rd*1e9:.0f} nm |")
    R.append("\nBelow ~20 um, humid capillary bridges must be eliminated (bump radii < ~50 nm are not robust); hydrophobic SAM-coated "
             "sub-um standoffs are the minimum requirement; at 5 um dry bumps must be ~150 nm radius (marginal).\n")
    R.append("## B4. Power through a convex transition (module loses face contact for t_tr)\n")
    R.append("| L | hold-up (trench, 1 face) | logic-only power 10 nW | logic + self-actuation 1 uW |\n|---|---|---|---|")
    for L in (1e-3, 100e-6, 10e-6):
        E = 0.5 * 57.8e-9 * (L * 1e3)**2 * (9 - 4)
        R.append(f"| {L*1e6:.0f} um | {E*1e9:.3g} nJ | {E/1e-8:.3g} s | {E/1e-6*1e3:.3g} ms |")
    R.append("\nIf the transit is ACTUATED BY NEIGHBOURS (the moving module is passive cargo, state held in nonvolatile memory), only "
             "retention power is needed during the break; at 10 nW even 10 um modules ride through ~1.5 ms. "
             "Requirement: neighbour-actuated transport or edge contacts; self-powered convex transitions are infeasible below ~100 um.\n")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/track_b.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
