"""SESSION 4. Pivot torque with a physically buildable EPM face (NUMERICAL SIMULATION, 2D FD).

Validation V1: legacy session-3 geometry (face-normal strips, non-magnetic bodies) vs the
session-3 magnetic-charge model. Validation V2: mesh refinement.
Design D(L): every face that participates carries an EPM whose switchable bars lie IN the face
plane (bar axis along the face, in the cross-section plane), terminated by NiFe pole pieces that
reach the face surface. Recess r below the face; standoff clearance c between modules.
Bars: electroplated CoP class, Jr = 0.65 T (LITERATURE-SNIPPET), squareness s (UNKNOWN; swept),
recoil mu_r 1.2 (ASSUMED). Bars fill a fraction f_b of the pole-piece depth extent (smeared in 2D).
Neighbour states per angle: each stationary face may be ON+, ON- or OFF (polarity-reversible EPM),
mover faces fixed ON (passive mover).
Run: python3 sims/s4/pivot_real.py [L_um] -> results/s4_pivot_real_<L>.md
"""
import math, os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "s3"))
import magfd as fd

MU0 = fd.MU0

def design(L):
    """Dimensions (m) of the face EPM for module size L. See INTEGRATED_MODULE_DESIGN.md."""
    um = 1e-6
    if L <= 150e-6:   # D100 integrated layout
        return dict(L=L, e=12 * um, p=8 * um, r=1 * um, tw=4 * um, tb=4 * um, c=1 * um,
                    depth_pole=40 * um, fb=0.6)
    s = L / 100e-6
    tb = min(4 * um * s, 50 * um)          # film-thickness limit ~50 um (plated/sputtered magnets)
    tw = min(4 * um * s, 30 * um)
    return dict(L=L, e=12 * um * s, p=8 * um * s, r=1 * um, tw=tw, tb=tb, c=1 * um,
                depth_pole=0.4 * L, fb=0.6)

def face_parts(D, face, state, Jr=0.65, sq=0.8, mur=1.2):
    """Parts of one face EPM in module-local coords. state: +1, -1 (bar magnetisation along +u/-u) or 0."""
    L, e, p, r, tw, tb = D["L"], D["e"], D["p"], D["r"], D["tw"], D["tb"]
    M = state * Jr * sq * D["fb"] / MU0
    parts = []
    u0, u1 = e, L - e
    def box(ua, ub, da, db, kind, m=(0.0, 0.0)):
        # face-local (u along face, d depth into module) -> module-local rectangle
        if face == "bottom": return fd.Part(ua, ub, da, db, kind, m, mur)
        if face == "top":    return fd.Part(ua, ub, L - db, L - da, kind, m, mur)
        if face == "left":   return fd.Part(da, db, ua, ub, kind, (m[1], m[0]), mur)
        if face == "right":  return fd.Part(L - db, L - da, ua, ub, kind, (m[1], m[0]), mur)
    hp = tw + tb + tw
    parts.append(box(u0, u0 + p, r, r + hp, "iron"))
    parts.append(box(u1 - p, u1, r, r + hp, "iron"))
    if state != 0:
        parts.append(box(u0 + p, u1 - p, r + tw, r + tw + tb, "mag", (M, 0.0)))
    return parts

def legacy_parts(L, face, pol, Br=1.0):
    """Session-3 geometry: strip thickness 0.15L, width 0.8L, recess 0.02L, magnetised along the face normal."""
    t, w, d = 0.15 * L, 0.8 * L, 0.02 * L
    M = pol * Br / MU0
    a, b = 0.1 * L, 0.9 * L
    if face == "bottom": return [fd.Part(a, b, d, d + t, "mag", (0.0, -M), 1.0)]
    if face == "top":    return [fd.Part(a, b, L - d - t, L - d, "mag", (0.0, M), 1.0)]
    if face == "right":  return [fd.Part(L - d - t, L - d, a, b, "mag", (M, 0.0), 1.0)]
    if face == "left":   return [fd.Part(d, d + t, a, b, "mag", (-M, 0.0), 1.0)]

def run_angle(L, mover, S_parts, D_parts, ang, pivot, h, c, convex=False, margin=None):
    """mover: list of parts at local origin (0, L+c) (sits above S). S at (0,0); D at (L,0) (if any).
    Domain contains the full swing (mover corner reaches ~ (1 + sqrt 2) L) plus a margin (default 0.6 L)."""
    margin = 0.6 * L if margin is None else margin
    lo = -L * 0.45 - margin; hi = L * 2.45 + c + margin
    xs = np.arange(lo, hi + h / 2, h); ys = np.arange(lo, hi + h / 2, h)
    placed = [(p, (0.0, L + c), ang, pivot) for p in mover]
    placed += [(p, (0.0, 0.0), 0.0, (0.0, 0.0)) for p in S_parts]
    placed += [(p, (L, 0.0), 0.0, (0.0, 0.0)) for p in D_parts]
    mu, Mx, My = fd.rasterize(placed, xs, ys)
    psi = fd.solve(xs, ys, mu, Mx, My)
    Hx, Hy = fd.fields(psi, h)
    # contour: mover outline offset by c/2, rotated
    o = c / 2
    loc = [(-o, -o), (L + o, -o), (L + o, L + o), (-o, L + o)]
    ca, sa = math.cos(ang), math.sin(ang)
    poly = []
    for (lx, ly) in loc:
        wx, wy = lx, ly + L + c
        dx, dy = wx - pivot[0], wy - pivot[1]
        poly.append((pivot[0] + ca * dx - sa * dy, pivot[1] + sa * dx + ca * dy))
    Fx, Fy, T = fd.stress_force(Hx, Hy, xs, ys, poly, pivot)
    # post-hoc checks on cell fields
    Hxc = 0.25 * (Hx[:-1, :-1] + Hx[1:, :-1] + Hx[:-1, 1:] + Hx[1:, 1:])
    Hyc = 0.25 * (Hy[:-1, :-1] + Hy[1:, :-1] + Hy[:-1, 1:] + Hy[1:, 1:])
    Bx = MU0 * (mu * Hxc + Mx); By = MU0 * (mu * Hyc + My)
    Bmag = np.hypot(Bx, By)
    # interior cells only (all 8 neighbours of the same material): avoids interface averaging artefacts
    from scipy.ndimage import minimum_filter
    iron = minimum_filter((mu > 500).astype(int), size=3) == 1
    Bmax_iron = float(Bmag[iron].max()) if iron.any() else 0.0
    mag = minimum_filter((np.hypot(Mx, My) > 0).astype(int), size=3) == 1
    Hpar = (Hxc * Mx + Hyc * My) / np.where(mag, np.hypot(Mx, My), 1.0)
    Hrev = float((-Hpar[mag]).max()) if mag.any() else 0.0
    return T, Fx, Fy, Bmax_iron, Hrev

def legacy_validation(L=100e-6, h=0.5e-6):
    import mag_pivot as mp
    c = 0.0
    mover = legacy_parts(L, "bottom", +1) + legacy_parts(L, "right", +1)
    S = legacy_parts(L, "top", +1); D = legacy_parts(L, "top", -1)
    out = []
    ref = {round(r[0]): r[1] for r in mp.pivot_profile(True, True, L=L, n=40)}
    for deg in (21, 45, 69):
        ang = -math.radians(deg)
        T, *_ = run_angle(L, mover, S, D, ang, (L, L + 2e-6), h, 2e-6)
        out.append((deg, -T * L, ref.get(deg)))   # 2D per depth x depth L ; clockwise rotation => driving torque = -T
    return out

def profile(L, h, sq=0.8, Jr=0.65, convex=False, angles=None, fixed=None):
    D = design(L); c = D["c"]
    mover = face_parts(D, "bottom", +1, Jr, sq) + face_parts(D, "right", +1, Jr, sq)
    if convex:
        pivot = (L, L + c / 2)
    else:
        pivot = (L, L + c)
    angles = angles if angles is not None else (np.linspace(3, 87, 15) if not convex else np.linspace(5, 175, 18))
    rows = []
    states = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] if fixed is None else [fixed]
    for deg in angles:
        ang = -math.radians(deg)
        best = None; allst = {}
        for sS, sD in states:
            if convex:
                S = face_parts(D, "top", sS, Jr, sq) + face_parts(D, "right", sD, Jr, sq)
                Dp = []
            else:
                S = face_parts(D, "top", sS, Jr, sq); Dp = face_parts(D, "top", sD, Jr, sq)
            T, Fx, Fy, Bi, Hr = run_angle(L, mover, S, Dp, ang, pivot, h, c)
            drive = -T * D["depth_pole"]
            allst[f"{sS},{sD}"] = (drive, Fx * D["depth_pole"], Fy * D["depth_pole"], Bi, Hr)
            if best is None or drive > best[0]:
                best = (drive, sS, sD, Bi, Hr, Fx * D["depth_pole"], Fy * D["depth_pole"])
        rows.append((deg,) + best)
        ALL.setdefault((L, convex), {})[float(deg)] = allst
    return D, rows

ALL = {}

def requirement(L, F_hinge=0.0, mu_h=0.4, r_h=5e-6):
    F_adh = 9 * 4 * math.pi * 0.5e-6 * 0.072
    return F_adh * L + 2330 * L**3 * 9.81 * L / math.sqrt(2) + mu_h * F_hinge * r_h

def main():
    Lum = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
    L = Lum * 1e-6
    h = 0.75e-6 if L <= 150e-6 else (2.0e-6 if L <= 400e-6 else 6e-6)
    R = [f"# Session 4 — pivot torque with buildable EPM faces, L = {Lum:.0f} um (NUMERICAL SIMULATION, 2D FD)\n"]
    if L <= 150e-6:
        val = legacy_validation(L)
        R.append("## V1. Validation vs session-3 charge model (legacy face-normal strips, Br = 1 T, non-magnetic bodies)\n")
        R.append("| angle | FD torque x depth L (N m) | charge model (N m) | ratio |\n|---|---|---|---|")
        for d, t, ref in val:
            R.append(f"| {d} | {t:.3e} | {ref:.3e} | {t/ref:.2f} |")
    res = {}
    for label, convex in (("90 deg", False), ("180 deg convex", True)):
        for sq in (0.8,):
            D, rows = profile(L, h, sq=sq, convex=convex)
            req = requirement(L)
            R.append(f"\n## {label}, CoP Jr = 0.65 T, squareness {sq} (ASSUMED), best neighbour state per angle\n")
            R.append("| angle | driving torque (N m) | S state | D state | margin vs peel | max B in iron (T) | max reverse H in magnets (kA/m) |\n|---|---|---|---|---|---|---|")
            for r in rows:
                R.append(f"| {r[0]:.0f} | {r[1]:.2e} | {r[2]:+d} | {r[3]:+d} | {r[1]/req:.2f} | {r[4]:.2f} | {r[5]/1e3:.0f} |")
            mn = min(rows, key=lambda r: r[1])
            res[(label, sq)] = (mn[1] / req, mn[0], max(r[4] for r in rows), max(r[5] for r in rows))
            R.append(f"\nWorst-case margin {mn[1]/req:.3f} at {mn[0]:.0f} deg (requirement = humid peel + gravity = {req:.2e} N m; hinge friction not included).")
    R.append("\n## Summary (linear model: torque scales exactly as (Jr*sq)^2; other squareness values rescaled)\n")
    for k, v in list(res.items()):
        for sq2 in (0.5, 1.0):
            res[(k[0], sq2)] = (v[0] * (sq2 / k[1])**2, v[1], v[2] * sq2 / k[1], v[3] * sq2 / k[1])
    for k, v in res.items():
        R.append(f"- {k[0]}, squareness {k[1]}: worst margin {v[0]:.3f} at {v[1]:.0f} deg; max iron B {v[2]:.2f} T; max reverse H in magnets {v[3]/1e3:.0f} kA/m (CoP Hc ~28 kA/m, SNIPPET)")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open(f"results/s4_pivot_real_{Lum:.0f}.md", "w").write(txt); print(txt)
    json.dump({"summary": {f"{k[0]}|{k[1]}": v for k, v in res.items()},
               "states": {f"{'180' if k[1] else '90'}": {str(a): st for a, st in v.items()} for k, v in ALL.items()},
               "design": {k: v for k, v in design(L).items()}}, open(f"results/s4_pivot_real_{Lum:.0f}.json", "w"))

if __name__ == "__main__":
    main()
