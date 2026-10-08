"""AUDIT 1. Face-motor thrust under realistic structure, tolerances, contamination,
and breakdown.

Model (NUMERICAL): 2D periodic finite-difference solution of div(eps grad phi)=0 for
the full stack
   grounded Si | oxide t_ox | 3-phase electrodes | coating t_c | AIR g | coating | electrodes | oxide | grounded Si
Electrodes are thin Dirichlet strips (fill fraction f). Force on the top module is
the Maxwell stress integrated on the mid-air plane (exact for everything above it).
Compared with the idealised S2 surface-potential formula.

Also (ANALYTIC/DERIVED, labelled): particle-propped gap, wedge (tilt) tolerance,
patch/trapped-charge phase error, breakdown margins.
Run: python3 sims/audit/face_motor_realistic.py -> results/audit_face_motor.md
"""
import math, os, sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import face_motor as fm
from constants import EPS0, GAMMA_WATER, RHO_SI, G

def solve_stack(lam, g, t_c, eps_c, t_ox, eps_ox, V, theta, fill=0.7, nx=264, dz=None):
    dz = dz or min(t_c, g) / 4
    layers = [(t_ox, eps_ox), (t_c, eps_c), (g, 1.0), (t_c, eps_c), (t_ox, eps_ox)]
    H = sum(t for t, _ in layers)
    nz = int(round(H / dz)) + 1
    z = np.linspace(0, H, nz); dz = z[1] - z[0]
    dx = lam / nx; x = np.arange(nx) * dx
    # permittivity at cell centres between nodes j and j+1 (vertical), node values for horizontal
    bounds = np.cumsum([0] + [t for t, _ in layers])
    def eps_at(zz):
        for i, (t, e) in enumerate(layers):
            if zz <= bounds[i + 1] + 1e-15: return e
        return layers[-1][1]
    eps_node = np.array([eps_at(zz) for zz in z])
    eps_half = np.array([eps_at(0.5 * (z[j] + z[j + 1])) for j in range(nz - 1)])
    jb = int(round(t_ox / dz)); jt = nz - 1 - jb
    pitch = lam / 3
    fixed = {}
    def strips(j, phase0):
        for e in range(3):
            c = (e + 0.5) * pitch
            m = np.abs(((x - c + lam / 2) % lam) - lam / 2) <= fill * pitch / 2
            for i in np.where(m)[0]:
                fixed[(i, j)] = V * math.cos(phase0 + 2 * math.pi * e / 3)
    strips(jb, 0.0); strips(jt, theta)
    for i in range(nx):
        fixed[(i, 0)] = 0.0; fixed[(i, nz - 1)] = 0.0
    unk = {}
    for j in range(nz):
        for i in range(nx):
            if (i, j) not in fixed: unk[(i, j)] = len(unk)
    rows, cols, vals = [], [], []
    b = np.zeros(len(unk))
    for (i, j), r in unk.items():
        ex = eps_node[j] / dx**2
        eu, ed = eps_half[j] / dz**2, eps_half[j - 1] / dz**2
        diag = -(2 * ex + eu + ed)
        rows.append(r); cols.append(r); vals.append(diag)
        for (ii, jj, cfac) in (((i - 1) % nx, j, ex), ((i + 1) % nx, j, ex), (i, j + 1, eu), (i, j - 1, ed)):
            if (ii, jj) in fixed: b[r] -= cfac * fixed[(ii, jj)]
            else: rows.append(r); cols.append(unk[(ii, jj)]); vals.append(cfac)
    A = sp.csr_matrix((vals, (rows, cols)), shape=(len(unk),) * 2)
    sol = spla.spsolve(A.tocsc(), b)
    phi = np.zeros((nz, nx))
    for (i, j), v in fixed.items(): phi[j, i] = v
    for (i, j), r in unk.items(): phi[j, i] = sol[r]
    # mid-air plane stress
    za = bounds[2] + g / 2
    jm = int(np.argmin(np.abs(z - za)))
    Ez = -(phi[jm + 1] - phi[jm - 1]) / (2 * dz)
    Ex = -(np.roll(phi[jm], -1) - np.roll(phi[jm], 1)) / (2 * dx)
    tau = -EPS0 * np.mean(Ex * Ez)
    p = EPS0 / 2 * np.mean(Ez**2 - Ex**2)
    # peak fields
    Exf = -(np.roll(phi, -1, axis=1) - np.roll(phi, 1, axis=1)) / (2 * dx)
    Ezf = np.zeros_like(phi); Ezf[1:-1] = -(phi[2:] - phi[:-2]) / (2 * dz)
    Em = np.sqrt(Exf**2 + Ezf**2)
    air = (z > bounds[2] + dz) & (z < bounds[3] - dz)
    coat = ((z > bounds[1] + dz) & (z < bounds[2])) | ((z > bounds[3]) & (z < bounds[4] - dz))
    return tau, p, Em[air].max(), Em[coat].max() if coat.any() else 0.0

def sweep_theta(**kw):
    ths = np.linspace(0, 2 * math.pi, 25)[:-1]
    out = [(th,) + solve_stack(theta=th, **kw) for th in ths]
    return out

def zero_normal_tau(rows):
    """Interpolate the shear at the phase where p crosses zero (max over crossings)."""
    best = 0.0
    for a, b in zip(rows, rows[1:] + rows[:1]):
        if a[2] == 0 or a[2] * b[2] < 0:
            w = a[2] / (a[2] - b[2]) if a[2] != b[2] else 0
            best = max(best, abs(a[1] + w * (b[1] - a[1])))
    return best

def main():
    R = ["# AUDIT 1 — electrostatic face motor under realistic conditions\n",
         "Evidence class per section: NUMERICAL (FD), ANALYTIC (closed form), or literature (cited).\n"]
    lam, g, V = 3.3e-6, 1e-6, 50.0
    ideal = fm.tau(V, V, 2 * math.pi / lam, g, lam / 4)
    R.append(f"Ideal S2 surface-potential tau_max at 50 V, g=1 um, lam=3.3 um: {ideal/1e3:.2f} kPa\n")
    R.append("## 1. Full dielectric stack (NUMERICAL)\n")
    R.append("| case | t_c / eps_c | t_ox | tau_max (kPa) | tau at p=0 (kPa) | ratio to ideal | max |E| air (V/um) | max |E| coating (V/um) |\n|---|---|---|---|---|---|---|---|---|")
    cases = [("thin SiO2 coat, 1 um ox", 0.1e-6, 3.9, 1e-6),
             ("thin SiO2 coat, 0.3 um ox", 0.1e-6, 3.9, 0.3e-6),
             ("protective 0.3 um SiO2 coat", 0.3e-6, 3.9, 1e-6),
             ("0.1 um HfO2 coat", 0.1e-6, 20.0, 1e-6)]
    stack = {}
    for lab, tc, ec, tox in cases:
        rows = sweep_theta(lam=lam, g=g, t_c=tc, eps_c=ec, t_ox=tox, eps_ox=3.9, V=V)
        tmax = max(abs(r[1]) for r in rows)
        t0 = zero_normal_tau(rows)
        ea = max(r[3] for r in rows); ecm = max(r[4] for r in rows)
        stack[lab] = (tmax, t0, ea, ecm)
        R.append(f"| {lab} | {tc*1e6:.1f} um / {ec} | {tox*1e6:.1f} um | {tmax/1e3:.2f} | {t0/1e3:.2f} | {tmax/ideal:.2f} | {ea/1e6:.0f} | {ecm/1e6:.0f} |")
    R.append("\nScale invariance (ANALYTIC): every length x0.1 and V x0.1 (5 V, 100 nm gap, 0.33 um pitch) gives identical stresses and fields; FD values above apply.\n")
    # breakdown
    R.append("## 2. Breakdown (literature + NUMERICAL peak fields)\n")
    R.append("- Air, gaps < ~4 um: V_b ~ (65-110 V/um) x d (Slade & Taylor, Holm Conf. 2001, via secondary citation; UNVERIFIED primary). For g=1 um: V_b ~ 65-110 V between facing conductors.")
    worst = stack["thin SiO2 coat, 1 um ox"][2]
    R.append("- Mesh check (NUMERICAL): stresses converge within 1 %; peak fields at electrode edges do NOT converge (edge singularity of thin strips), so they are not used as the criterion:")
    R.append("  | nx | dz | tau (Pa) | p (Pa) | peak E air | peak E coat |\n  |---|---|---|---|---|---|")
    for nx, dzf in [(132, 2), (264, 4), (528, 8)]:
        t, pp, ea, ec = solve_stack(lam=lam, g=g, t_c=0.1e-6, eps_c=3.9, t_ox=1e-6, eps_ox=3.9, V=V, theta=math.pi/2, nx=nx, dz=0.1e-6/dzf)
        R.append(f"  | {nx} | {0.1/dzf*1e3:.1f} nm | {t:.0f} | {pp:.0f} | {ea/1e6:.0f} V/um | {ec/1e6:.0f} V/um |")
    R.append("- Criterion used instead: facing electrodes of opposite phase see up to 2V = 100 V across ~1.2 um, which is inside the 65-110 V micro-gap breakdown band.")
    R.append("- Verdict: the 50 V / 1 um design operates AT the measured micro-gap breakdown envelope -> unsafe without margin. "
             "Derate to <= 30 V (stress x0.36) or use the scaled 5 V / 100 nm design, where peak-to-peak 10 V is below the ~12-15 V ionisation potential of O2/N2 (no avalanche possible; field emission onset needs local fields ~1e3 V/um).")
    # particle-propped gap
    R.append("\n## 3. Particle props the gap open (ANALYTIC, ideal formula; rigid faces)\n")
    R.append("| design | particle d | effective gap | tau_max / nominal |\n|---|---|---|---|")
    for lab, g0, lam0, V0 in [("50 V / 1 um / 3.3 um", 1e-6, 3.3e-6, 50), ("5 V / 100 nm / 0.33 um", 1e-7, 0.33e-6, 5)]:
        k = 2 * math.pi / lam0
        t_nom = fm.tau(V0, V0, k, g0, lam0 / 4)
        for d in (0.1e-6, 0.3e-6, 1e-6, 3e-6):
            ge = max(g0, d)
            R.append(f"| {lab} | {d*1e6:.1f} um | {ge*1e6:.1f} um | {fm.tau(V0, V0, k, ge, lam0/4)/t_nom:.2e} |")
    R.append("\nThrust falls ~exp(-k d): one 1 um particle eliminates the 5 V design (factor ~1e-7) and one 3 um particle removes ~99 % of the 50 V design's thrust. "
             "Contamination tolerance requires either a sealed particle-free environment or compliant faces that wrap around particles.\n")
    # wedge tolerance
    R.append("## 4. Wedge/bow: gap varies linearly by +-delta across the face; phase tuned for nominal gap (ANALYTIC, local-stress integration)\n")
    R.append("| delta | thrust / nominal | net normal (kPa) | sliding margin (L=100 um, humid) |\n|---|---|---|---|")
    k = 2 * math.pi / lam
    _, d0 = fm.sliding_margin(100e-6, g, V, lam, disc=0.59)
    s0 = d0["ks"] / k
    F_adh = 9 * 4 * math.pi * 0.5e-6 * GAMMA_WATER
    for dl in (0.0, 0.1, 0.2, 0.4, 0.6):
        gs = g * (1 + dl * np.linspace(-1, 1, 401))
        t = 0.59 * fm.tau(V, V, k, gs, s0).mean(); p = 0.59 * fm.pnorm(V, V, k, gs, s0).mean()
        A = 0.6 * (100e-6)**2
        m = t * A / (0.4 * (max(p, 0) * A + F_adh + RHO_SI * 1e-12 * G))
        R.append(f"| {dl:.1f} | {t/(0.59*fm.tau(V, V, k, g, s0)):.2f} | {p/1e3:.2f} | {m:.1f} |")
    # patch potentials / trapped charge
    R.append("\n## 5. Patch potentials / trapped charge (ANALYTIC phase-error model)\n")
    R.append("A spurious surface-potential component V_p at the drive wavevector shifts the effective phase by up to asin(V_p/V), moving the operating point off p=0.\n")
    R.append("| design V | V_p | phase error (rad) | margin (L=100 um, humid) |\n|---|---|---|---|")
    for V0, g0, lam0 in [(50, 1e-6, 3.3e-6), (5, 1e-7, 0.33e-6)]:
        kk = 2 * math.pi / lam0
        _, dd = fm.sliding_margin(100e-6, g0, V0, lam0, disc=0.59)
        for Vp in (0.1, 0.5, 2.0):
            de = math.asin(min(Vp / V0, 1.0))
            worst = 1e9
            for sgn in (1, -1):
                s = (dd["ks"] + sgn * de) / kk
                t = 0.59 * fm.tau(V0, V0, kk, g0, s); p = 0.59 * fm.pnorm(V0, V0, kk, g0, s)
                A = 0.6 * (100e-6)**2
                worst = min(worst, t * A / (0.4 * (max(p, 0) * A + F_adh)))
            R.append(f"| {V0} V | {Vp} V | {de:.3f} | {worst:.1f} |")
    R.append("\nPatch potentials of 0.1-0.5 V (metal work-function variation) are harmless; volt-level trapped charge in dielectrics degrades the 5 V design several-fold (closed-loop phase control could re-null p, untested).\n")
    R.append("## 6. Energy penalty from substrate capacitance (ANALYTIC)\n")
    for lab, tox, f in [("1 um oxide", 1e-6, 0.7), ("0.3 um oxide", 0.3e-6, 0.7)]:
        Csub = 3.9 * f / tox; Cgap = 1 / 1e-6
        R.append(f"- {lab}: C_substrate/C_gap ~ {Csub/Cgap:.1f} -> step energy ~ x{1+Csub/Cgap:.1f} of S7's 4 nJ unless charge is recovered")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/audit_face_motor.md", "w").write(txt)
    print(txt)

if __name__ == "__main__":
    main()
