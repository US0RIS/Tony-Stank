"""S1. Force scaling across module sizes L = 10 mm ... 10 um.

Compares, for a cube of edge L (silicon density), the module weight with the
maximum force available from each attachment/actuation physics acting over one
face (area L^2) or, for point-like effects, over a characteristic radius L/2.

Output: results/scaling_table.md  (DERIVED claims, analytic)
Run:    python3 sims/scaling.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from constants import *

def weight(L):                      # N
    return RHO_SI * L**3 * G

def electrostatic_pressure(V, g_air, t_diel, eps_r):
    """Parallel plate with series air gap g_air and dielectric t_diel (Pa).
    p = eps0 V^2 / (2 (g_air + t/eps_r)^2). Valid for g << L."""
    return EPS0 * V**2 / (2 * (g_air + t_diel / eps_r) ** 2)

def capillary_force(R, gamma=GAMMA_WATER, theta=0.0):
    """Sphere-plane capillary bridge, small-meniscus limit: F = 4 pi R gamma cos(theta)."""
    return 4 * math.pi * R * gamma * math.cos(theta)

def vdw_sphere_plane(R, A=HAMAKER_SI, D=D0_VDW):
    return A * R / (6 * D**2)

def vdw_rough_flat(L, rq, A=HAMAKER_SI):
    """Flat faces separated by an effective roughness gap rq: pressure A/(6 pi rq^3)."""
    return A / (6 * math.pi * rq**3) * L**2

def magnet_contact_force(L, B=1.0):
    """Two face-contacting magnets, saturated-face estimate: F = B^2 A / (2 mu0)."""
    return B**2 * L**2 / (2 * MU0)

def epm_switch(L, Hc=50e3, fill=0.3, path_factor=4.0, rho=RHO_AU*0.8e0 / 0.8):
    """Electropermanent magnet switching estimate for a module of edge L.

    Must drive H >= Hc (AlNiCo-5 coercivity ~50 kA/m, STD order) through a
    magnetic path of length ~path_factor*L/2.  Winding window ~ (L/4)^2 with copper
    fill factor `fill`.  Ampere-turns NI = Hc * l_path.
    Current density J = NI / (fill * A_window); scales as 1/L.
    Energy per pulse (resistive) E = J^2 rho * V_winding * t_pulse.
    t_pulse ASSUM 20 us (Knaian-type EPMs use ~tens of us pulses; UNVERIFIED).
    """
    l_path = path_factor * L / 2
    NI = Hc * l_path
    A_win = (L / 4) ** 2
    J = NI / (fill * A_win)
    vol_cu = fill * A_win * (math.pi * L / 2)   # one turn length ~ pi*L/2 times window
    t = 20e-6
    E = J**2 * RHO_AU * vol_cu * t
    return J, E

def table():
    rows = []
    hdr = ("| quantity | " + " | ".join(SIZES) + " | scaling |\n|---|" +
           "---|" * (len(SIZES) + 1) + "\n")
    def row(name, f, scal):
        vals = []
        for L in SIZES.values():
            v = f(L)
            vals.append(f"{v:.2e}")
        rows.append(f"| {name} | " + " | ".join(vals) + f" | {scal} |")
    row("weight W (N)", weight, "L^3")
    row("face area (m^2)", lambda L: L**2, "L^2")
    row("electroadhesion, 100 V, 10 um polymer eps_r=3, 1 um air (N)",
        lambda L: electrostatic_pressure(100, 1e-6, 10e-6, 3) * L**2, "L^2")
    row("e-static clamp, 10 V, 100 nm HfO2 eps_r=20, 10 nm rough gap (N)",
        lambda L: electrostatic_pressure(10, 10e-9, 100e-9, 20) * L**2, "L^2")
    row("same clamp / weight", lambda L: electrostatic_pressure(10, 10e-9, 100e-9, 20) * L**2 / weight(L), "1/L")
    row("capillary, R=L/2 water (N)", lambda L: capillary_force(L / 2), "L")
    row("capillary / weight", lambda L: capillary_force(L / 2) / weight(L), "1/L^2")
    row("vdW sphere-plane R=L/2 (N)", lambda L: vdw_sphere_plane(L / 2), "L")
    row("vdW flat faces, 5 nm rough gap (N)", lambda L: vdw_rough_flat(L, 5e-9), "L^2")
    row("vdW flat faces, 50 nm rough gap (N)", lambda L: vdw_rough_flat(L, 50e-9), "L^2")
    row("permanent-magnet contact, B=1 T (N)", lambda L: magnet_contact_force(L), "L^2 (ideal; real fringing worse at small L)")
    row("EPM switching current density (A/m^2)", lambda L: epm_switch(L)[0], "1/L")
    row("EPM switching energy per pulse (J)", lambda L: epm_switch(L)[1], "L (at fixed pulse time)")
    return hdr + "\n".join(rows) + "\n"

if __name__ == "__main__":
    out = table()
    p_clamp = electrostatic_pressure(10, 10e-9, 100e-9, 20)
    p_ea = electrostatic_pressure(100, 1e-6, 10e-6, 3)
    notes = (f"\nPressures: thin-film clamp {p_clamp/1e3:.0f} kPa; electroadhesion {p_ea/1e3:.2f} kPa; "
             f"magnet B=1T {1/(2*MU0)/1e3:.0f} kPa.\n"
             "EPM current density limit for copper/gold windings is ~1e9-1e10 A/m^2 for us pulses "
             "(electromigration DC limit ~1e9-5e9 A/m^2, ASSUM/UNVERIFIED).\n")
    os.makedirs("results", exist_ok=True)
    with open("results/scaling_table.md", "w") as f:
        f.write("# S1 force scaling (DERIVED)\n\n" + out + notes)
    print(out + notes)
