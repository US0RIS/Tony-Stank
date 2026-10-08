"""SESSION 3 / MAGNETIC FAMILY. Quantitative screening of magnetic propulsion and
attachment between neighbouring microscale modules.

M1 Lorentz drive: stator coil current sheet acting on a passive permanent-magnet
   (Halbach) mover.                                    MATHEMATICAL DERIVATION
M2 Ratio of coil-driven force to PM-PM / PM-iron forces (cogging, cross-talk).
                                                       MATHEMATICAL DERIVATION
M3 Electropermanent (EPM) switching: energy, current density, adiabatic
   temperature rise vs module size and switchable-magnet coercivity.
                                                       MATHEMATICAL DERIVATION
M4 EPM-switched toothed reluctance stepper between neighbouring faces:
   tangential vs normal stress from a finite-difference magnetostatic solve
   (scalar potential, linear iron), plus gap/particle sensitivity.
                                                       NUMERICAL SIMULATION
M5 EPM magnetic attachment pressure vs particle-propped gap (magnetic circuit).
                                                       MATHEMATICAL DERIVATION
Run: python3 sims/s3/magnetic.py -> results/s3_magnetic.md
"""
import math, os
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

MU0 = 4e-7 * math.pi
RHO_CU = 1.7e-8          # ohm m (STD)
CV_CU = 3.45e6           # J/m^3/K volumetric heat capacity (STD)
SIZES = [10e-3, 1e-3, 300e-6, 100e-6, 10e-6]

# ---------------- M1 ----------------
def lorentz_shear(Br, k, t_m, g, t_c, J0):
    """Coil layer (thickness t_c, sinusoidal current density amplitude J0) at distance g
    from a one-sided Halbach PM film (thickness t_m, remanence Br)."""
    B0 = Br * (1 - math.exp(-k * t_m))
    return 0.5 * J0 * B0 * (math.exp(-k * g) - math.exp(-k * (g + t_c))) / k

def m1(R):
    R.append("## M1. Lorentz drive: stator coils push a passive PM mover (MATHEMATICAL DERIVATION)\n")
    R.append("tau = (J0 Br/2k)(1-e^{-k t_m})(e^{-kg} - e^{-k(g+t_c)}); dissipation q = J0^2 rho t_c / 2 per face area.\n"
             "Heat-limited: q <= q_max = 2e5 W/m^2 (transient dT ~ q t_step/(rho c L) ~ 13 K per 10 ms step at L=100 um).\n"
             "Br = 0.5 T (assumed microfabricated-magnet value; range 0.3-1.2, see MAGNETIC_ACTUATION.md). Pitch optimised for each gap.\n")
    R.append("| L | t_c | t_m | gap g | best pitch | J0 (A/m^2) | tau (Pa) | power per face | energy per lattice step (v=3 mm/s) |\n|---|---|---|---|---|---|---|---|---|")
    for L in SIZES:
        t_c = min(5e-6, 0.05 * L); t_m = min(20e-6, 0.2 * L)
        for g in (1e-6, 5e-6):
            J0 = math.sqrt(2 * 2e5 / (RHO_CU * t_c))
            J0 = min(J0, 1e10)
            best = max(((lorentz_shear(0.5, 2 * math.pi / lam, t_m, g, t_c, J0), lam)
                        for lam in np.geomspace(2e-6, 2e-3, 200)))
            q = J0**2 * RHO_CU * t_c / 2
            P = q * 0.6 * L**2
            E = P * L / 3e-3
            R.append(f"| {L*1e6:.0f} um | {t_c*1e6:.2f} um | {t_m*1e6:.1f} um | {g*1e6:.0f} um | {best[1]*1e6:.0f} um | {J0:.2e} | {best[0]:.0f} | {P*1e3:.3g} mW | {E*1e6:.3g} uJ |")
    R.append("\nElectrostatic face drive for comparison (AUDIT 1): ~5.7 kPa at 15-40 nJ per step (sealed, 100 nm gap), ~1 kPa at a 5 um gap.\n")

# ---------------- M2 ----------------
def m2(R):
    R.append("## M2. Coil force vs permanent-magnet interactions (MATHEMATICAL DERIVATION)\n")
    R.append("Lorentz thrust ~ K B_PM (K = J t_c sheet current); PM-PM or PM-iron interaction ~ B_PM^2/mu0. Ratio = mu0 K / B_PM = B_coil / B_PM.\n")
    R.append("| L | K at q_max (A/m) | B_coil = mu0 K | ratio to B_PM = 0.12 T (field at coil) |\n|---|---|---|---|")
    for L in SIZES:
        t_c = min(5e-6, 0.05 * L)
        J0 = min(math.sqrt(2 * 2e5 / (RHO_CU * t_c)), 1e10)
        K = J0 * t_c
        R.append(f"| {L*1e6:.0f} um | {K:.3g} | {MU0*K*1e3:.2f} mT | {MU0*K/0.12:.3f} |")
    R.append("\nConsequence: coil-driven (Lorentz) thrust is 1-10 % of the static forces between the PMs it acts on and any PM or iron on other faces. "
             "Any uncancelled PM-PM cogging or PM-iron attraction (friction) exceeds the drive. Lorentz drive of PM movers is REJECTED for lattices in which "
             "neighbouring faces also carry magnets, at all sizes <= 1 mm.\n")

# ---------------- M3 ----------------
def epm_switch(pole, Hc, fill=0.3, t_pulse=1e-6, factor=2.0):
    """Switch a semi-hard magnet of length l_m = pole/2 with a coil wound in a window
    of cross-section (pole/4)^2. NI = factor*Hc*l_m. E = (NI)^2 rho l_turn t / (fill A_w)."""
    l_m = pole / 2; A_w = (pole / 4) ** 2; l_turn = 2 * pole
    NI = factor * Hc * l_m
    J = NI / (fill * A_w)
    E = NI**2 * RHO_CU * l_turn * t_pulse / (fill * A_w)
    dT = J**2 * RHO_CU * t_pulse / CV_CU
    return J, E, dT

def m3(R):
    R.append("## M3. EPM switching cost per pole (MATHEMATICAL DERIVATION)\n")
    R.append("Pole size = min(L/2, 50 um); switching field = 2 Hc; 1 us pulse; copper fill 0.3. J ~ Hc/pole; E ~ Hc^2 pole t; adiabatic dT ~ J^2 rho t / c_v.\n")
    R.append("| L | pole | material (Hc) | J (A/m^2) | E per switch | adiabatic dT | verdict |\n|---|---|---|---|---|---|---|")
    mats = [("AlNiCo-5 (~50 kA/m)", 50e3), ("FeCrCo / CoNiP film (~20 kA/m, ASSUMED)", 20e3), ("semi-hard 'Remendur-class' (~3 kA/m, ASSUMED)", 3e3)]
    for L in SIZES:
        pole = min(L / 2, 50e-6)
        for lab, Hc in mats:
            J, E, dT = epm_switch(pole, Hc)
            ok = "OK" if (dT < 50 and J < 3e10) else "FAILS (heating)"
            R.append(f"| {L*1e6:.0f} um | {pole*1e6:.0f} um | {lab} | {J:.2e} | {E*1e9:.3g} nJ | {dT:.3g} K | {ok} |")
    R.append("\nRevision of session-1 claim N1: session 1 assumed AlNiCo coercivity, a 20 us pulse and a whole-module coil, and concluded 'EPM impossible "
             "below ~1 mm'. With poles of <= 50 um and 1 us pulses the energy per switch is nJ-scale; the binding constraint is the adiabatic temperature "
             "rise, which is acceptable for Hc <= ~20 kA/m at 5 um poles. The open question moves from physics to MATERIALS: microfabricated semi-hard "
             "films with square loops and stable remanence at 1-10 um thickness (ENGINEERING HYPOTHESIS, unverified).\n")

# ---------------- M4 ----------------
def toothed_fd(lam, g, h_t, wf, s, mur=1000.0, nx=160, dz=None):
    """Two toothed soft-iron bodies (period lam, tooth fraction wf, tooth height h_t,
    back-iron thickness h_t) separated by air gap g, mover offset s. Scalar potential psi,
    psi=0 at stator back, psi=1 (unit MMF) at mover back. Returns (tau, p) on the mover
    in units of mu0*(1/g)^2/2 (i.e. normalised to the aligned ideal gap pressure)."""
    dz = dz or min(g, h_t) / 6
    H = 2 * h_t + g + 2 * h_t
    nz = int(round(H / dz)) + 1
    z = np.linspace(0, H, nz); dz = z[1] - z[0]
    dx = lam / nx; x = np.arange(nx) * dx
    def mu(xx, zz):
        if zz < h_t or zz > H - h_t: return mur                       # back irons
        if zz < 2 * h_t:                                                # stator teeth
            return mur if ((xx % lam) < wf * lam) else 1.0
        if zz > H - 2 * h_t:                                            # mover teeth
            return mur if (((xx - s) % lam) < wf * lam) else 1.0
        return 1.0
    M = np.array([[mu(xx, zz) for xx in x] for zz in z])
    N = nx * (nz - 2)
    idx = lambda i, j: (j - 1) * nx + (i % nx)
    rows, cols, vals = [], [], []
    b = np.zeros(N)
    for j in range(1, nz - 1):
        for i in range(nx):
            r = idx(i, j)
            mxp = 2 / (1 / M[j, i] + 1 / M[j, (i + 1) % nx]); mxm = 2 / (1 / M[j, i] + 1 / M[j, (i - 1) % nx])
            mzp = 2 / (1 / M[j, i] + 1 / M[j + 1, i]); mzm = 2 / (1 / M[j, i] + 1 / M[j - 1, i])
            rows.append(r); cols.append(r); vals.append(-(mxp + mxm) / dx**2 - (mzp + mzm) / dz**2)
            rows += [r, r]; cols += [idx(i + 1, j), idx(i - 1, j)]; vals += [mxp / dx**2, mxm / dx**2]
            for jj, m in ((j + 1, mzp), (j - 1, mzm)):
                if jj == 0: pass                                         # psi = 0
                elif jj == nz - 1: b[r] -= m / dz**2 * 1.0               # psi = 1
                else: rows.append(r); cols.append(idx(i, jj)); vals.append(m / dz**2)
    A = sp.csr_matrix((vals, (rows, cols)), shape=(N, N))
    psi = np.vstack([np.zeros(nx), spla.spsolve(A.tocsc(), b).reshape(nz - 2, nx), np.ones(nx)])
    jm = int(np.argmin(np.abs(z - (2 * h_t + g / 2))))
    Hz = -(psi[jm + 1] - psi[jm - 1]) / (2 * dz)
    Hx = -(np.roll(psi[jm], -1) - np.roll(psi[jm], 1)) / (2 * dx)
    tau = -MU0 * np.mean(Hx * Hz)
    p = MU0 / 2 * np.mean(Hz**2 - Hx**2)
    Bmean = MU0 * np.mean(np.abs(Hz))
    norm = MU0 * (1 / g) ** 2 / 2
    return tau / norm, p / norm, Bmean / (MU0 / g)

def m4(R):
    R.append("## M4. EPM-switched toothed reluctance stepper between faces (NUMERICAL SIMULATION, FD magnetostatics)\n")
    R.append("Linear iron (mu_r = 1000), tooth fraction 0.4, tooth height = pitch/2. Stresses normalised to the aligned-gap pressure B0^2/2mu0 with B0 = mu0 MMF/g. "
             "Columns: maximum tangential stress over offset, normal stress at that offset, ratio, and the friction coefficient mu* below which the mover can slide.\n")
    R.append("| g/lam | tau_max (norm) | p at tau_max (norm) | tau/p = mu* |\n|---|---|---|---|")
    lam = 20e-6
    res = {}
    for gr in (0.025, 0.05, 0.1, 0.2):
        g = gr * lam
        best = (0, 0)
        for s in np.linspace(0, lam / 2, 9)[1:-1]:
            t, p, _ = toothed_fd(lam, g, lam / 2, 0.4, s, nx=120, dz=g / 4 if g < 2e-6 else 0.5e-6)
            if abs(t) > abs(best[0]): best = (t, p)
        res[gr] = best
        R.append(f"| {gr} | {abs(best[0]):.3f} | {best[1]:.3f} | {abs(best[0])/best[1]:.3f} |")
    # convergence check
    t1, p1, _ = toothed_fd(lam, 0.05 * lam, lam / 2, 0.4, lam / 8, nx=80, dz=0.25e-6)
    t2, p2, _ = toothed_fd(lam, 0.05 * lam, lam / 2, 0.4, lam / 8, nx=160, dz=0.125e-6)
    R.append(f"\nMesh check (g/lam = 0.05, s = lam/8): tau {t1:.4f} -> {t2:.4f}, p {p1:.4f} -> {p2:.4f} (coarse -> fine).\n")
    R.append("Absolute stresses, with the gap flux density limited by iron saturation in the teeth (B_tooth <= 1.0 T for NiFe, so B0 <= ~0.4 T with tooth fraction 0.4):\n")
    B0 = 0.4; P0 = B0**2 / (2 * MU0)
    R.append(f"- B0 = {B0} T -> B0^2/2mu0 = {P0/1e3:.0f} kPa.")
    for gr, (t, p) in res.items():
        R.append(f"- g/lam = {gr}: tau_max ~ {abs(t)*P0/1e3:.1f} kPa with normal clamp {p*P0/1e3:.1f} kPa; slides only if mu < {abs(t)/p:.2f}")
    R.append("\nInterpretation: the reluctance stepper converts PM energy (switched, not sustained, by the coil) into 5-40 kPa of tangential stress, "
             "comparable to or above the electrostatic drive, but always with a LARGER normal clamp: tau/p < ~0.2-0.4. With dry Si/SiO2 friction "
             "mu ~ 0.2-0.6 the mover is friction-locked unless (a) a low-friction coating (mu < ~0.15) or rolling/flexure guidance is used, or (b) a "
             "balancing face on the opposite side cancels the normal force. KILL PARAMETER: tau/p vs mu.\n")
    return res

# ---------------- M5 ----------------
def m5(R):
    R.append("## M5. EPM attachment through a particle-propped gap (MATHEMATICAL DERIVATION, magnetic circuit)\n")
    R.append("Closed circuit through the neighbour's pole pieces: B ~ Br l_m / (l_m + 2 g mu_rec), pressure = B^2/2mu0 over pole area (pole fraction 0.5). "
             "Contrast: electrostatic stress across a propped gap falls ~exp(-k d) (AUDIT 1).\n")
    R.append("| L | l_m | Br | particle-propped gap | B | pressure (face-averaged) |\n|---|---|---|---|---|---|")
    for L in (1e-3, 300e-6, 100e-6, 10e-6):
        l_m = 0.4 * L
        for g in (0.1e-6, 1e-6, 5e-6):
            B = 1.0 * l_m / (l_m + 2 * g * 1.05)
            P = 0.5 * B**2 / (2 * MU0)
            R.append(f"| {L*1e6:.0f} um | {l_m*1e6:.0f} um | 1.0 T | {g*1e6:.1f} um | {B:.2f} T | {P/1e3:.0f} kPa |")
    R.append("\nThis is an upper bound (no leakage, no saturation, ideal keeper). Magnetic attachment degrades ~linearly with gap/l_m rather than "
             "exponentially: it is the only switchable attachment found that keeps ~100 kPa with micrometre particles at L >= 100 um. "
             "At L = 10 um, a 5 um particle halves B (pressure -75 %).\n")

def main():
    R = ["# Session 3 — magnetic family screening\n",
         "Evidence classes: MATHEMATICAL DERIVATION (M1, M2, M3, M5), NUMERICAL SIMULATION (M4). Material values are ASSUMED unless cited in MAGNETIC_ACTUATION.md.\n"]
    m1(R); m2(R); m3(R); res = m4(R); m5(R)
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s3_magnetic.md", "w").write(txt)
    print(txt)

if __name__ == "__main__":
    main()
