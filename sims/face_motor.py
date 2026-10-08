"""S2. Electrostatic 'face motor': shear vs normal stress between two facing
multiphase electrode arrays (one on each module face), and whether the shear can
beat friction + adhesion so one module can slide along another.

Model (DERIVED): 2D, air gap 0<z<g, x-periodic with wavelength lam = 2*pi/k.
Bottom surface potential V1 cos(kx); top surface V2 cos(k(x-s)). Field is
confined to the gap (surface-potential idealisation). Maxwell stress on the
top body gives

  shear   tau(s) = eps0 k^2 V1 V2 sin(ks) / (2 sinh(kg))
  normal  p(s)   = eps0 k^2 [V1^2 + V2^2 - 2 V1 V2 cosh(kg) cos(ks)] / (4 sinh^2(kg))
                   (p > 0 = attraction)

Validation: independent finite-difference Laplace solve (validate()).
Discrete 3-phase electrodes are also solved by FD to get the fundamental
'fill factor' penalty relative to the ideal sinusoid.

Run: python3 sims/face_motor.py   -> results/face_motor.md
"""
import math, os, sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
sys.path.insert(0, os.path.dirname(__file__))
from constants import EPS0, RHO_SI, G, GAMMA_WATER

# ---------------- analytic -----------------
def tau(V1, V2, k, g, s):
    return EPS0 * k**2 * V1 * V2 * np.sin(k * s) / (2 * np.sinh(k * g))

def pnorm(V1, V2, k, g, s):
    return EPS0 * k**2 * (V1**2 + V2**2 - 2 * V1 * V2 * np.cosh(k * g) * np.cos(k * s)) / (4 * np.sinh(k * g) ** 2)

def kg_opt():
    """maximise x^2/sinh(x): tanh x = x/2."""
    x = 2.0
    for _ in range(60):
        f = math.tanh(x) - x / 2
        df = 1 / math.cosh(x) ** 2 - 0.5
        x -= f / df
    return x

# ---------------- finite-difference validation -----------------
def fd_solve(bottom, top, lam, g, nx, nz):
    """Solve Laplace on periodic-x strip. bottom/top: arrays (nx,) of potentials.
    Returns (tau, p) on the top body averaged over one period."""
    dx, dz = lam / nx, g / (nz - 1)
    n_int = nz - 2
    N = nx * n_int
    idx = lambda i, j: (j - 1) * nx + (i % nx)
    rows, cols, vals = [], [], []
    b = np.zeros(N)
    cx, cz = 1 / dx**2, 1 / dz**2
    for j in range(1, nz - 1):
        for i in range(nx):
            r = idx(i, j)
            rows.append(r); cols.append(r); vals.append(-2 * cx - 2 * cz)
            rows += [r, r]; cols += [idx(i - 1, j), idx(i + 1, j)]; vals += [cx, cx]
            for jj in (j - 1, j + 1):
                if jj == 0:
                    b[r] -= cz * bottom[i]
                elif jj == nz - 1:
                    b[r] -= cz * top[i]
                else:
                    rows.append(r); cols.append(idx(i, jj)); vals.append(cz)
    A = sp.csr_matrix((vals, (rows, cols)), shape=(N, N))
    phi_int = spla.spsolve(A, b).reshape(n_int, nx)
    phi = np.vstack([bottom, phi_int, top])
    # second-order one-sided dphi/dz at top
    dphidz = (3 * phi[-1] - 4 * phi[-2] + phi[-3]) / (2 * dz)
    dphidx = (np.roll(top, -1) - np.roll(top, 1)) / (2 * dx)
    Ex, Ez = -dphidx, -dphidz
    tau_fd = -EPS0 * np.mean(Ex * Ez)
    p_fd = EPS0 / 2 * np.mean(Ez**2 - Ex**2)
    return tau_fd, p_fd

def three_phase(x, lam, phases, amps, fill):
    """Discrete stripe electrodes, 3 per period, width fill*lam/3; potential in the
    inter-electrode gaps interpolated linearly (idealised insulating gap)."""
    n = len(x)
    pitch = lam / 3
    V = np.full(n, np.nan)
    for e in range(3):
        c = (e + 0.5) * pitch
        m = np.abs(((x - c + lam / 2) % lam) - lam / 2) <= fill * pitch / 2
        V[m] = amps * math.cos(phases[e])
    # periodic linear interpolation over gaps
    good = ~np.isnan(V)
    xg = np.concatenate([x[good] - lam, x[good], x[good] + lam])
    vg = np.concatenate([V[good]] * 3)
    return np.interp(x, xg, vg)

def validate(report):
    lam, g, V = 3e-6, 1e-6, 50.0
    k = 2 * math.pi / lam
    nx, nz = 240, 81
    x = np.arange(nx) * lam / nx
    report.append("## Validation: analytic vs finite difference (sinusoidal electrodes)\n")
    report.append("| k*s | tau analytic (Pa) | tau FD (Pa) | p analytic (Pa) | p FD (Pa) |\n|---|---|---|---|---|")
    maxerr = 0
    for ks in [0.0, 0.5, math.pi / 2, 2.0, math.pi]:
        s = ks / k
        bt = V * np.cos(k * x); tp = V * np.cos(k * (x - s))
        tf, pf = fd_solve(bt, tp, lam, g, nx, nz)
        ta, pa = tau(V, V, k, g, s), pnorm(V, V, k, g, s)
        report.append(f"| {ks:.3f} | {ta:.1f} | {tf:.1f} | {pa:.1f} | {pf:.1f} |")
        scale = max(abs(pnorm(V, V, k, g, math.pi / 2)), 1)
        maxerr = max(maxerr, abs(ta - tf) / scale, abs(pa - pf) / scale)
    report.append(f"\nMax error relative to |p(pi/2)|: {maxerr*100:.2f} %\n")
    # discrete 3-phase electrodes: shear amplitude vs ideal sinusoid
    report.append("## Discrete 3-phase stripe electrodes (FD)\n")
    report.append("Bottom phases (0,120,240 deg); top phases shifted by theta. Peak shear over theta relative to ideal sinusoid of same amplitude.\n")
    report.append("| electrode fill | peak tau FD (Pa) | ideal tau_max (Pa) | ratio |\n|---|---|---|---|")
    ideal = tau(V, V, k, g, lam / 4)
    ratios = {}
    for fill in [0.5, 0.7, 0.9]:
        best = 0
        for th in np.linspace(0, math.pi, 13):
            bt = three_phase(x, lam, [0, 2*math.pi/3, 4*math.pi/3], V, fill)
            tp = three_phase(x, lam, [th, th + 2*math.pi/3, th + 4*math.pi/3], V, fill)
            tf, _ = fd_solve(bt, tp, lam, g, nx, nz)
            best = max(best, abs(tf))
        ratios[fill] = best / ideal
        report.append(f"| {fill} | {best:.1f} | {ideal:.1f} | {best/ideal:.2f} |")
    return maxerr, ratios

# ---------------- feasibility of sliding -----------------
def sliding_margin(L, g, V, lam, mu=0.4, eta=0.6, disc=0.8, n_bump=9, R_bump=0.5e-6,
                   humid=True, W_adh=0.05, p_hold=None):
    """Margin = available thrust / resistance for one module sliding on one face.
    eta: electrode area fraction of the face; disc: discrete-electrode penalty.
    Phase s chosen to maximise tau - mu*p subject to p >= p_hold (default 0)."""
    k = 2 * math.pi / lam
    A = eta * L**2
    s = np.linspace(0, lam / 2, 2001)
    t = disc * tau(V, V, k, g, s)
    p = disc * pnorm(V, V, k, g, s)
    ph = 0.0 if p_hold is None else p_hold
    ok = p >= ph
    if not ok.any():
        return 0.0, None
    obj = np.where(ok, t - mu * p, -np.inf)
    i = int(np.argmax(obj))
    if humid:
        F_adh = n_bump * 4 * math.pi * R_bump * GAMMA_WATER
    else:
        F_adh = n_bump * 1.5 * math.pi * W_adh * R_bump
    W = RHO_SI * L**3 * G
    thrust = t[i] * A
    resist = mu * (p[i] * A + F_adh + W)   # worst case: weight normal to face
    return thrust / resist, dict(thrust=thrust, resist=resist, tau=t[i], p=p[i], ks=k*s[i])

def gap_sensitivity(L, g, V, lam, disc, mu=0.4, eta=0.6, err=0.2):
    """Phase tuned for nominal gap, actual gap off by +-err: margin.
    Same adhesion model as sliding_margin (humid, 9 bumps, R=0.5 um).
    Negative net normal (repulsion) is clipped to 0: the module is then held only
    by adhesion, which is the optimistic case for friction."""
    k = 2 * math.pi / lam
    _, d = sliding_margin(L, g, V, lam, mu=mu, eta=eta, disc=disc)
    s = d["ks"] / k
    out = {}
    for f in (1 - err, 1.0, 1 + err):
        ga = g * f
        t = disc * tau(V, V, k, ga, s); p = disc * pnorm(V, V, k, ga, s)
        F_adh = 9 * 4 * math.pi * 0.5e-6 * GAMMA_WATER
        A = eta * L**2
        out[f] = t * A / (mu * (max(p, 0) * A + F_adh + RHO_SI * L**3 * G))
    return out

def main():
    rep = ["# S2 electrostatic face-motor (DERIVED + SIMULATED)\n"]
    x = kg_opt()
    rep.append(f"Optimal k*g maximising shear at fixed V,g: {x:.4f} -> pitch lam = {2*math.pi/x:.3f} g; "
               f"tau_max = {x**2/math.sinh(x):.3f} * eps0 V^2/(2 g^2).\n")
    err, ratios = validate(rep)
    disc = ratios[0.7]
    rep.append("\n## Sliding feasibility (humid air, capillary at 9 standoff bumps R=0.5 um, mu=0.4, weight normal to face)\n")
    rep.append("Design family at constant field V/g = 50 V/um and lam = 3.3 g (scale-invariant stress).\n")
    rep.append("| gap g | V | pitch | L | thrust (N) | resistance (N) | margin | shear (kPa) | net normal (kPa) |\n|---|---|---|---|---|---|---|---|---|")
    for g, V in [(1e-6, 50.0), (0.3e-6, 15.0), (0.1e-6, 5.0)]:
        lam = 2 * math.pi / x * g
        for L in [1e-3, 100e-6, 30e-6, 10e-6]:
            m, d = sliding_margin(L, g, V, lam, disc=disc)
            rep.append(f"| {g*1e6:.1f} um | {V:.0f} | {lam*1e6:.2f} um | {L*1e6:.0f} um | {d['thrust']:.2e} | {d['resist']:.2e} | {m:.1f} | {d['tau']/1e3:.2f} | {d['p']/1e3:.2f} |")
    rep.append("\n## Pitch mismatch: fixed lithography pitch 2 um with thin gap (normal force dominates)\n")
    rep.append("| gap g | V | k g | margin (L=100 um) | net normal (kPa) |\n|---|---|---|---|---|")
    for g, V in [(1e-6, 50.0), (0.3e-6, 15.0), (0.1e-6, 5.0), (0.03e-6, 1.5)]:
        lam = 2e-6
        m, d = sliding_margin(100e-6, g, V, lam, disc=disc)
        rep.append(f"| {g*1e9:.0f} nm | {V} | {2*math.pi/lam*g:.2f} | {m:.1f} | {d['p']/1e3:.2f} |")
    rep.append("\n## Gap tolerance: phase tuned for nominal gap, actual gap +-20% (L=100 um)\n")
    rep.append("| design | margin @0.8g | @1.0g | @1.2g |\n|---|---|---|---|")
    for g, V, lam in [(1e-6, 50.0, 3.3e-6), (0.1e-6, 5.0, 0.33e-6), (0.1e-6, 5.0, 2e-6)]:
        o = gap_sensitivity(100e-6, g, V, lam, disc)
        rep.append(f"| g={g*1e6:.1f} um V={V} lam={lam*1e6:.2f} um | {o[0.8]:.2f} | {o[1.0]:.2f} | {o[1.2]:.2f} |")
    rep.append("\nNote: discrete-electrode factor is applied to both shear and normal stress (approximation; FD gave it for shear only).\n")
    rep.append("\n## Size floor: L at which margin = 1 (thrust ~ L^2, bump adhesion ~ const)\n")
    for humid in (True, False):
        lo, hi = 1e-6, 1e-3
        for _ in range(60):
            mid = math.sqrt(lo * hi)
            m, _ = sliding_margin(mid, 1e-6, 50, 3.3e-6, disc=disc, humid=humid)
            lo, hi = (mid, hi) if m < 1 else (lo, mid)
        rep.append(f"- humid={humid}: L_min = {hi*1e6:.1f} um (9 bumps, R=0.5 um)")
    rep.append("\n## Dry vs humid adhesion at L=100 um, g=1 um, V=50 V\n")
    for humid in (True, False):
        m, d = sliding_margin(100e-6, 1e-6, 50, 3.3e-6, disc=disc, humid=humid)
        rep.append(f"- humid={humid}: margin {m:.1f}")
    # with holding requirement: keep p >= 5 kPa during slide
    m, d = sliding_margin(100e-6, 1e-6, 50, 3.3e-6, disc=disc, p_hold=5e3)
    rep.append(f"- with net hold pressure >= 5 kPa during slide: margin {m:.1f}, shear {d['tau']/1e3:.1f} kPa")
    txt = "\n".join(rep) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/face_motor.md", "w").write(txt)
    print(txt)
    return err

if __name__ == "__main__":
    main()
