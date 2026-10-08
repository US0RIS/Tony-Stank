"""SESSION 3. Neighbour-driven electropermanent PIVOT (push-pull) at micro scale.

Geometry (2D cross-section, units of L): mover M = [0,1]x[1,2] sits on base B1 = [0,1]x[0,1]
next to B2 = [1,2]x[0,1]. M pivots clockwise 90 deg about the shared corner P = (1,1)
and lands on top of B2. Every face carries a magnet strip (thickness t_m, width w_m,
recessed by d_r) magnetised normal to the face; stationary EPM faces can be set to
+1 (out), -1 (in) or 0 (off). The mover's magnets are fixed during transit.

Model: magnetic surface charges (sigma = M.n) on strip faces, 2D line-charge interaction
U = -(mu0/2pi) sum q_i q_j ln r per unit depth, times depth D = L (2D approximation,
overestimates finite-depth forces). Torque about P = -dU/dtheta; net force = -grad U.
Checks: (i) facing-strip pressure vs B^2/2mu0 analytic limit; (ii) discretisation convergence.
Requirements (MATHEMATICAL DERIVATION): torque > adhesion peel torque + gravity torque at
every angle; the net force must keep the mover pressed on the pivot (hinge reaction >= 0)
or a hinge latch must supply the deficit.
NUMERICAL SIMULATION. Run: python3 sims/s3/mag_pivot.py -> results/s3_mag_pivot.md
"""
import math, os
import numpy as np

MU0 = 4e-7 * math.pi

def face_strips(cx, cy, faces, t_m=0.15, w_m=0.8, d_r=0.02, n=40):
    """Return list of (points (k,2), charges-per-unit-M (k,)) for each face polarity entry.
    faces: dict face_name -> polarity (+1 out, -1 in). Square cell [cx,cx+1]x[cy,cy+1]."""
    out = []
    normals = {"top": (0, 1), "bottom": (0, -1), "left": (-1, 0), "right": (1, 0)}
    for f, pol in faces.items():
        if pol == 0: continue
        nx, ny = normals[f]
        # face centre
        fx = cx + 0.5 + 0.5 * nx; fy = cy + 0.5 + 0.5 * ny
        tx, ty = -ny, nx
        s = (np.arange(n) + 0.5) / n * w_m - w_m / 2
        ds = w_m / n
        for depth, sign in ((d_r, +1), (d_r + t_m, -1)):
            px = fx - nx * depth + tx * s; py = fy - ny * depth + ty * s
            out.append((np.stack([px, py], 1), np.full(n, sign * pol * ds)))
    if not out: return np.zeros((0, 2)), np.zeros(0)
    P = np.concatenate([o[0] for o in out]); Q = np.concatenate([o[1] for o in out])
    return P, Q

def energy(Pa, Qa, Pb, Qb, M, L):
    """Interaction energy (J) of charge sets in units of L, magnetisation M (A/m), depth L."""
    if len(Qa) == 0 or len(Qb) == 0: return 0.0
    d = Pa[:, None, :] - Pb[None, :, :]
    r = np.sqrt((d**2).sum(-1)) * L
    qq = (Qa[:, None] * Qb[None, :]) * (M * L)**2
    return float(-(MU0 / (2 * math.pi)) * (qq * np.log(r)).sum() * L)

def rot(P, th, c=(1.0, 1.0)):
    c = np.array(c); R = np.array([[math.cos(th), math.sin(th)], [-math.sin(th), math.cos(th)]])  # clockwise
    return (P - c) @ R.T + c

def check_pressure(M=1.0 / MU0, L=100e-6, n=200):
    """Validation: two long bars (width 1, length 20, units of L) end-to-end, both magnetised +y,
    gap 0.01. Analytic contact limit: pressure -> mu0 M^2 / 2 = Br^2/2mu0 (attraction)."""
    xs = (np.arange(n) + 0.5) / n - 0.5
    def bar(y_bottom, length=20.0):
        P = np.concatenate([np.stack([xs, np.full(n, y_bottom + length)], 1), np.stack([xs, np.full(n, y_bottom)], 1)])
        Q = np.concatenate([np.full(n, 1.0 / n), np.full(n, -1.0 / n)])
        return P, Q
    Pa, Qa = bar(-20.0); g = 0.01; dy = 1e-4
    Pb, Qb = bar(g); Pb2, _ = bar(g + dy)
    F = -(energy(Pa, Qa, Pb2, Qb, M, L) - energy(Pa, Qa, Pb, Qb, M, L)) / (dy * L)   # force on B along +y
    area = 1.0 * L * L                                                                # width L x depth L
    return F / area, (MU0 * M)**2 / (2 * MU0)

def pivot_profile(push=True, pull=True, Br=1.0, L=100e-6, n=40, hinge=0.0):
    M = Br / MU0
    # mover: bottom face out (+1) pointing down, right face out (+1)
    Pm0, Qm0 = face_strips(0, 1, {"bottom": +1, "right": +1}, n=n)
    # B1 top: to REPEL mover bottom (which presents + charge facing down), B1 top must present + charge facing up: polarity +1
    Ps1, Qs1 = face_strips(0, 0, {"top": +1 if push else 0}, n=n)
    # B2 top: to ATTRACT mover's right face (+ charge outward), B2 top must present - : polarity -1
    Ps2, Qs2 = face_strips(1, 0, {"top": -1 if pull else 0}, n=n)
    Ps = np.concatenate([Ps1, Ps2]) if len(Qs1) or len(Qs2) else np.zeros((0, 2))
    Qs = np.concatenate([Qs1, Qs2])
    ths = np.radians(np.linspace(1, 89, 45)); dth = 1e-4
    rows = []
    for th in ths:
        U = lambda t: energy(rot(Pm0, t), Qm0, Ps, Qs, M, L)
        tau = -(U(th + dth) - U(th - dth)) / (2 * dth)                 # N m, positive = drives rotation
        h = 1e-4
        Pm = rot(Pm0, th)
        def Ut(dx, dy):
            P2 = Pm + np.array([dx, dy]); return energy(P2, Qm0, Ps, Qs, M, L)
        Fx = -(Ut(h, 0) - Ut(-h, 0)) / (2 * h * L); Fy = -(Ut(0, h) - Ut(0, -h)) / (2 * h * L)
        # mover centre relative to pivot; force toward pivot = -(F . u) with u = unit(centre - P)
        cxy = rot(np.array([[0.5, 1.5]]), th)[0]; u = (cxy - np.array([1, 1])); u /= np.linalg.norm(u)
        F_into_pivot = -(Fx * u[0] + Fy * u[1])
        rows.append((math.degrees(th), tau, F_into_pivot))
    return rows

def requirements(L, humid=True):
    W = 2330 * L**3 * 9.81
    g_torque = W * L / math.sqrt(2)
    F_adh = 9 * 4 * math.pi * 0.5e-6 * 0.072 if humid else 9 * 1.5 * math.pi * 0.05 * 0.5e-6
    return F_adh * L + g_torque, F_adh, W

def main():
    R = ["# Session 3 — neighbour-driven EPM push-pull pivot (NUMERICAL SIMULATION, 2D magnetic-charge model)\n"]
    p_num, p_ana = check_pressure()
    R.append(f"Validation: two long bars end-to-end (gap 0.01 L) give {p_num/1e3:.0f} kPa (negative = attraction) vs analytic contact limit Br^2/2mu0 = {p_ana/1e3:.0f} kPa (Br = 1 T); |ratio| {abs(p_num)/p_ana:.2f}. Thin face strips (width/thickness ~5) are far weaker than this limit, which is why EPM designs use pole pieces.\n")
    c1 = pivot_profile(n=20); c2 = pivot_profile(n=40)
    dev = max(abs(a[1] - b[1]) / max(abs(b[1]), 1e-30) for a, b in zip(c1, c2) if abs(b[1]) > 1e-3 * max(abs(x[1]) for x in c2))
    R.append(f"Discretisation check (20 vs 40 charges per sheet): max relative torque change {dev*100:.1f} % (where torque is non-negligible).\n")
    for L in (1e-3, 300e-6, 100e-6, 10e-6):
        req, F_adh, W = requirements(L)
        R.append(f"## L = {L*1e6:.0f} um (Br = 1.0 T; required torque = humid peel {F_adh*L:.2e} + gravity {W*L/math.sqrt(2):.2e} = {req:.2e} N m)\n")
        R.append("| mode | min torque over 1-89 deg (N m) | angle of min | torque margin | min force into pivot (N) | hinge must hold (N) |\n|---|---|---|---|---|---|")
        for lab, push, pull in (("push+pull", True, True), ("pull only", False, True), ("push only", True, False)):
            rows = pivot_profile(push, pull, L=L, n=40)
            tmin = min(rows, key=lambda r: r[1])
            fmin = min(r[2] for r in rows)
            hold = max(0.0, -fmin)
            R.append(f"| {lab} | {tmin[1]:.2e} | {tmin[0]:.0f} | {tmin[1]/req:.1f} | {fmin:.2e} | {hold:.2e} |")
        R.append("")
    rows = pivot_profile(True, True, L=100e-6, n=40)
    R.append("## Torque and pivot-force profile, push+pull, L = 100 um\n")
    R.append("| angle (deg) | torque (N m) | force into pivot (N) |\n|---|---|---|")
    for r in rows[::4]:
        R.append(f"| {r[0]:.0f} | {r[1]:.2e} | {r[2]:.2e} |")
    R.append("\n## 180-deg convex pivot around a single neighbour (push from its top, pull from its side)\n")
    R.append("| L | mode | min torque | angle | margin | hinge must hold (N) |\n|---|---|---|---|---|---|")
    for L in (1e-3, 300e-6, 100e-6, 10e-6):
        req, _, _ = requirements(L)
        for lab, push in (("push+pull", True), ("pull only", False)):
            rr = convex_profile(L=L, push=push)
            tmin = min(rr, key=lambda r: r[1]); hold = max(0.0, -min(r[2] for r in rr))
            R.append(f"| {L*1e6:.0f} um | {lab} | {tmin[1]:.2e} | {tmin[0]:.0f} | {tmin[1]/req:.1f} | {hold:.2e} |")
    R.append("\n2D model with depth = L. A finite-depth 3D strip is weaker (estimate x0.5, UNVERIFIED), so 100 um margins of 2-9 become ~1-4.5.\n")
    R.append("\nScaling (MATHEMATICAL DERIVATION): magnetic torque ~ (Br^2/mu0) L^3 (same geometry), peel torque ~ F_adh L ~ L, gravity torque ~ rho g L^4. "
             "Torque margin vs adhesion therefore scales as L^2, and vs gravity as 1/L.\n")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s3_mag_pivot.md", "w").write(txt)
    print(txt)


def convex_profile(L=100e-6, Br=1.0, n=40, push=True):
    """180-deg convex pivot: mover [0,1]x[1,2] on S=[0,1]x[0,1] rotates clockwise about S's
    top-right corner (1,1) and lands on S's right face. S top pushes (repels mover bottom),
    S right face pulls (attracts mover's right face). Returns (deg, torque, force into pivot)."""
    M = Br / MU0
    Pm0, Qm0 = face_strips(0, 1, {"bottom": +1, "right": +1}, n=n)
    Ps, Qs = face_strips(0, 0, {"top": +1 if push else 0, "right": -1}, n=n)
    rows = []
    for deg in np.linspace(2, 178, 45):
        th = math.radians(deg); d = 1e-4; h = 1e-4
        U = lambda t: energy(rot(Pm0, t), Qm0, Ps, Qs, M, L)
        tau = -(U(th + d) - U(th - d)) / (2 * d)
        Pm = rot(Pm0, th)
        Ut = lambda dx, dy: energy(Pm + np.array([dx, dy]), Qm0, Ps, Qs, M, L)
        Fx = -(Ut(h, 0) - Ut(-h, 0)) / (2 * h * L); Fy = -(Ut(0, h) - Ut(0, -h)) / (2 * h * L)
        c = rot(np.array([[0.5, 1.5]]), th)[0]; u = c - np.array([1.0, 1.0]); u /= np.linalg.norm(u)
        rows.append((deg, tau, -(Fx * u[0] + Fy * u[1])))
    return rows

if __name__ == "__main__":
    main()
