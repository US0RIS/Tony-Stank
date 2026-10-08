"""SESSION 4 / PHASE 4. EPM switching coil, field uniformity, thermals, drivers, energy source.

Geometry from module_geometry.build(L) (bar inside a rectangular solenoid of two metal layers + vias).
Field: 3D Biot-Savart of the actual turns (air core; the pole pieces/second bar return path is
represented by an MMF efficiency eta, ASSUMED 0.8). Min |H_axial| over the WHOLE bar volume is used,
not the centre value. Material switching field H_sw = k_sw * Hc with k_sw swept (loop squareness unknown).
Thermal: two-node model (coil -> insulation -> Si module -> neighbours), lumped.
Driver: CMOS H-bridge + per-coil select switch sized for the voltage-drop budget.
Run: python3 sims/s4/switching.py -> results/s4_switching.md
Evidence: MATHEMATICAL DERIVATION / NUMERICAL (Biot-Savart); material values LITERATURE-SNIPPET.
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import module_geometry as mg

RHO_CU = 1.7e-8; CV_CU = 3.45e6; CV_SI = 1.66e6
MATERIALS = {   # (Jr [T], Hc [A/m]) LITERATURE-SNIPPET (Metals 2022; UCC CoPtP), squareness not reported
    "CoP (plated)": (0.65, 28e3), "CoNiP (plated)": (0.40, 45e3), "CoPtP (plated)": (0.35, 92e3)}

def solenoid_H(bar_l, bar_w, bar_t, tw, N, I, pts):
    """Rectangular solenoid, turns uniformly along x in [-coil_l/2, coil_l/2]; each turn a rectangle in the
    y-z plane of half-sizes (bar_w/2 + tw/2, bar_t/2 + tw/2). Returns Hx at pts (n,3)."""
    coil_l = bar_l
    ay, az = bar_w / 2 + tw / 2, bar_t / 2 + tw / 2
    H = np.zeros(len(pts))
    pitch = coil_l / N
    xs = -coil_l / 2 + (np.arange(N) + 0.5) * pitch          # turns centred at true pitch (fix after review R2)
    for x0 in xs:
        corners = [(x0, -ay, -az), (x0, ay, -az), (x0, ay, az), (x0, -ay, az), (x0, -ay, -az)]
        for k in range(4):
            a = np.array(corners[k]); b = np.array(corners[k + 1])
            # Biot-Savart for a straight segment, discretised
            ns = 24
            t = (np.arange(ns) + 0.5) / ns
            P = a + np.outer(t, b - a); dl = (b - a) / ns
            r = pts[:, None, :] - P[None, :, :]
            rn = np.linalg.norm(r, axis=2)[..., None]
            dH = np.cross(np.broadcast_to(dl, r.shape), r) / (4 * math.pi * rn**3)
            H += I * dH[..., 0].sum(axis=1)
    return H

def design_coil(L_um, pitch, metal_t, gap, k_sw, mat, eta=0.8):
    comps = mg.build(L_um); G = mg.build.GEOM
    um = 1e-6
    bar_l, bar_w, bar_t, tw = G["coil_l"] * um, G["bar_w"] * um, G["bar_t"] * um, G["tw"] * um
    Jr, Hc = MATERIALS[mat]
    N = int(bar_l / (pitch * um))
    w = (pitch - gap) * um; t = min(metal_t * um, tw - 1 * um)
    # field per ampere: min over bar volume
    gx = np.linspace(-G["bar_l"] / 2 * um, G["bar_l"] / 2 * um, 13)
    gy = np.linspace(-bar_w / 2, bar_w / 2, 4); gz = np.linspace(-bar_t / 2, bar_t / 2, 3)
    pts = np.array([(x, y, z) for x in gx for y in gy for z in gz])
    H1 = solenoid_H(bar_l, bar_w, bar_t, tw, N, 1.0, pts)
    Hmin1, Hctr1 = H1.min(), H1[len(H1) // 2]
    H_sw = k_sw * Hc
    I = H_sw / (eta * Hmin1)
    A_tr = w * t
    l_turn = 2 * (bar_w + tw) + 2 * (bar_t + tw)
    R = RHO_CU * N * l_turn / A_tr + 2 * N * RHO_CU * tw / (w * w)       # turns + vias
    Lind = 4e-7 * math.pi * N**2 * (bar_w + tw) * (bar_t + tw) / bar_l
    J = I / A_tr
    return dict(N=N, w=w, t=t, I=I, R=R, Lind=Lind, J=J, V=I * R, P=I * I * R, Hmin1=Hmin1, Hctr1=Hctr1, H_sw=H_sw,
                Cu_vol=N * l_turn * A_tr, l_turn=l_turn, G=G, L=L_um * um)

ALPHA_CU = 0.0039   # 1/K temperature coefficient of resistivity

def thermal(d, t_pulse, k_ins=0.15, t_ins=1e-6):
    """Coil node: C_c = Cu volume * cv; to module through insulation over the coil surface."""
    G = d["G"]; um = 1e-6
    area = 2 * G["coil_l"] * um * (G["bar_w"] + G["bar_t"] + 4 * G["tw"]) * um
    R_th = t_ins / (k_ins * area)
    C_c = d["Cu_vol"] * CV_CU
    tau = R_th * C_c
    P = d["P"]
    dT0 = P * R_th * (1 - math.exp(-t_pulse / tau))           # constant-R value
    dT_coil = (math.exp(ALPHA_CU * dT0) - 1) / ALPHA_CU         # constant-current R(T) feedback (review R2)
    E = P * t_pulse
    dT_mod = E / (CV_SI * d["L"]**3)
    return dT_coil, dT_mod, E, tau

def driver_area(I, V_budget, RonW_n=1.0e3, RonW_p=2.5e3, area_per_um=1.0):
    """um^2 for an H-bridge (2 NMOS + 2 PMOS) with total on-drop <= V_budget, plus one NMOS select switch per coil (12)."""
    R_sw = (V_budget / I) / 3.0          # bridge high + low + select switch in series
    Wn = RonW_n / R_sw; Wp = RonW_p / R_sw
    bridge = 2 * (Wn + Wp) * area_per_um
    select = 12 * Wn * area_per_um
    return bridge + select, R_sw

def crosstalk(d):
    """H from an energised coil at (a) the parallel bar of the same face (centre-to-centre bar_w + 2tw + clr), and
    (b) the facing neighbour's bar (across 2 skins: depth 2*(cover + tw + bar_t/2) + 1 um clearance)."""
    G = d["G"]; um = 1e-6
    bar_l, bar_w, bar_t, tw = G["coil_l"] * um, G["bar_w"] * um, G["bar_t"] * um, G["tw"] * um
    sep_par = bar_w + 2 * tw + 1 * um
    sep_face = 2 * (1 * um + tw + bar_t / 2) + 1 * um
    pts = np.array([(0, sep_par, 0), (bar_l * 0.4, sep_par, 0), (0, 0, sep_face), (bar_l * 0.4, 0, sep_face)])
    H = solenoid_H(bar_l, bar_w, bar_t, tw, d["N"], d["I"], pts)
    return abs(H[:2]).max(), abs(H[2:]).max()

def main():
    R = ["# Session 4 — EPM switching, thermals, drivers (MATHEMATICAL DERIVATION + NUMERICAL Biot-Savart)\n",
         "Material values are LITERATURE-SNIPPET (no squareness reported). k_sw = switching field / Hc (ASSUMED range 1.5-3).\n",
         "Corrections after independent review R2: turns centred at true pitch; R(T) feedback (alpha = 0.0039/K, constant current); driver density 1-2 um^2 per um of gate width; flags: HEAT@1us = >150 K rise for a 1 us pulse, heat@10us likewise, DRIVER = does not fit the two-die core, J>1e11 A/m^2. Temperatures capped at 9999 K for display (i.e. melting).\n"]
    for L_um, pitch, mt in ((100, 3.0, 3.0), (100, 1.5, 3.0), (300, 3.0, 8.0), (1000, 6.0, 20.0)):
        R.append(f"\n## L = {L_um} um, coil pitch {pitch} um, metal thickness {mt} um\n")
        R.append("| material | k_sw | N | H/A min over bar (A/m per A) | I (A) | J (A/m^2) | R (ohm) | V (V) | P (W) | L_coil (H) | dT coil 1us / 10us (K) | E 1us / 10us | driver area (um^2, 1-2 um^2/um) vs die area | crosstalk: same face / facing bar (kA/m) | flag |")
        R.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for mat in MATERIALS:
            for k in (1.5, 3.0):
                d = design_coil(L_um, pitch, mt, gap=0.5 if pitch < 2 else 1.0, k_sw=k, mat=mat)
                t1 = thermal(d, 1e-6); t10 = thermal(d, 10e-6)
                Adrv, Rsw = driver_area(d["I"], 0.3 * max(d["V"], 0.5))
                die = 2 * ((d["G"]["window"] + 0) ** 2)
                ct = crosstalk(d)
                flags = []
                if t1[0] > 150: flags.append("HEAT@1us")
                if t10[0] > 150: flags.append("heat@10us")
                if Adrv > die: flags.append("DRIVER")
                if d["J"] > 1e11: flags.append("J>1e11")
                R.append(f"| {mat} | {k} | {d['N']} | {d['Hmin1']:.3g} (centre {d['Hctr1']:.3g}) | {d['I']:.3f} | {d['J']:.2e} | {d['R']:.2f} | {d['V']:.2f} | {d['P']:.3f} | {d['Lind']:.1e} | "
                         f"{min(t1[0],9999):.0f} / {min(t10[0],9999):.0f} | {t1[2]*1e6:.2f} / {t10[2]*1e6:.2f} uJ | {Adrv:.0f}-{2*Adrv:.0f} vs {die:.0f} | {ct[0]/1e3:.1f} / {ct[1]/1e3:.1f} | {' '.join(flags) or 'ok'} |")
    R.append("\n## Energy source for a switching pulse\n")
    for L_um in (100, 300, 1000):
        d = design_coil(L_um, 3.0 if L_um < 1000 else 6.0, 3.0 if L_um == 100 else (8.0 if L_um == 300 else 20.0), 1.0, 2.0, "CoP (plated)")
        E = d["P"] * 10e-6
        C = 2 * E / (3.3**2 - 2.0**2)
        vol_cap = C / 2.3e-15            # um^3 at deep-trench volumetric density (57.8 nF/mm^2 over ~25 um depth)
        R.append(f"- L = {L_um} um: 10 us pulse at k_sw = 2 needs {E*1e6:.2f} uJ -> local capacitor {C*1e9:.0f} nF -> {vol_cap:.2e} um^3 of trench capacitor = {vol_cap/L_um**3:.1f} module volumes")
    R.append("\nConclusion: local storage cannot supply switching pulses at any size <= 1 mm with on-chip trench capacitors; pulse current must arrive through the lattice contacts in real time (see MECHANICAL_CYCLE.md / power section).\n")
    R.append("## Magnetisation-reversal time\nNo measured reversal time for plated CoP/CoNiP elements was found (LITERATURE gap). Domain-wall-mediated reversal over a 58 um bar at "
             "assumed wall speeds of 10-100 m/s takes 0.6-6 us; 10 us pulses are used as the conservative case. This is an UNVERIFIED ASSUMPTION.\n")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s4_switching.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
