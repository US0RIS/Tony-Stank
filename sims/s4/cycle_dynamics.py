"""SESSION 4 / PHASE 6. Full pivot dynamics using the FD torque tables (results/s4_pivot_real_<L>.json).

Physics (MATHEMATICAL + NUMERICAL):
 - rigid cube rotating about an edge: I = (2/3) m L^2 (exact for a cube about an edge)
 - departure: capillary/adhesion peel must be overcome at theta ~ 0 (bridge rupture within ~0.1 um,
   i.e. ~1e-3 rad): START condition tau_mag(first angle) > F_adh * L
 - swing: theta'' = (tau_mag(theta, schedule) - tau_hinge_friction)/I ; air damping neglected
   (rotational damping time ~ I/(10 mu L^3) ~ 85 ms >> transit, MATHEMATICAL estimate)
 - schedule: at each tabulated angle the best (S, D) state; braking: optional switch to the most
   negative-torque state beyond theta_b to limit landing speed
 - hinge: required inward force = -(force component along the pivot->centre direction); a negative
   value means the mover is pushed off the pivot and needs a captive hinge (none realizable, see review)
 - landing: pin-tip impact stress from reviewer R3 scaling sigma ~ 2-4 GPa at 2 m/s (sigma ~ v)
Similarity scaling (MATHEMATICAL, exact for geometrically similar magnetostatics with fixed materials):
 torque x s^3, forces x s^2, inertia x s^5, peel torque x s (fixed adhesion force).
Run: python3 sims/s4/cycle_dynamics.py -> results/s4_cycle_dynamics.md
"""
import json, math, os
import numpy as np

F_ADH = {"humid (9 bumps, full meniscus)": 4.07e-6, "dry SAM-coated sharp bumps (ASSUMED 10x lower)": 4.07e-7}

def load(L_um=100):
    d = json.load(open(f"results/s4_pivot_real_{L_um}.json"))
    return d

def tables(d, kind):
    st = d["states"][kind]
    angs = sorted(float(a) for a in st)
    best = []; brake = []; Fin = []
    for a in angs:
        S = st[str(a)] if str(a) in st else st[repr(a)]
        items = list(S.items())
        b = max(items, key=lambda kv: kv[1][0]); w = min(items, key=lambda kv: kv[1][0])
        best.append(b[1][0]); brake.append(w[1][0])
        # inward force for the best state (pivot -> mover centre direction)
        th = math.radians(a) if kind == "90" else math.radians(a)
        Fx, Fy = b[1][1], b[1][2]
        # mover centre relative to pivot rotates clockwise from (-0.5,0.5)L
        ang = -th
        cx, cy = -0.5, 0.5
        ux = math.cos(ang) * cx - math.sin(ang) * cy; uy = math.sin(ang) * cx + math.cos(ang) * cy
        n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
        Fin.append(-(Fx * ux + Fy * uy))
    return np.array(angs), np.array(best), np.array(brake), np.array(Fin)

def simulate(angs, tq, brake_tq, L, theta_end, s=1.0, mu_h=0.4, r_h=5e-6, theta_b=None, Fin=None):
    m = 2330 * (L * s)**3; I = (2 / 3) * m * (L * s)**2
    T = lambda th: np.interp(th, np.radians(angs), tq) * s**3
    Tb = lambda th: np.interp(th, np.radians(angs), brake_tq) * s**3
    th, w, t, dt = math.radians(angs[0]), 0.0, 0.0, 1e-8 * s
    stall = None
    while th < math.radians(theta_end):
        tau = Tb(th) if (theta_b is not None and th > math.radians(theta_b)) else T(th)
        fric = 0.0
        if Fin is not None:
            fin = abs(np.interp(th, np.radians(angs), Fin)) * s**2
            fric = mu_h * fin * r_h * s
        acc = (tau - fric) / I
        w += acc * dt; th += w * dt; t += dt
        if w <= 0:
            stall = math.degrees(th); break
        if t > 1.0: stall = math.degrees(th); break
    v_edge = w * L * s * math.sqrt(2)
    return stall, t, w, v_edge

def main():
    R = ["# Session 4 — pivot cycle dynamics from the FD torque tables (L = 100 um; larger L by exact similarity scaling)\n"]
    d = load(100)
    L = 100e-6
    for kind, theta_end in (("90", 87.0), ("180", 175.0)):
        angs, tq, br, Fin = tables(d, kind)
        R.append(f"## {kind} deg pivot (CoP Jr 0.65 T, squareness 0.8; 2D x pole depth; best neighbour state per angle)\n")
        R.append(f"- torque range over the swing: {tq.min():.2e} to {tq.max():.2e} N m; angles with negative best torque: "
                 f"{[float(a) for a, t in zip(angs, tq) if t < 0]}")
        R.append(f"- inward hinge force (best states): min {Fin.min()*1e6:.2f} uN ({'needs captive hinge' if Fin.min() < 0 else 'pressed into pivot'})")
        R.append("\n| s (L) | adhesion case | start torque / peel torque | stalls at (deg) | transit time | landing edge speed | verdict |\n|---|---|---|---|---|---|---|")
        for s in (1.0, 3.0, 10.0):
            for lab, Fa in F_ADH.items():
                start_ratio = tq[0] * s**3 / (Fa * L * s)
                if start_ratio < 1:
                    R.append(f"| {s*100:.0f} um | {lab} | {start_ratio:.3f} | does not start | - | - | FAIL (cannot peel) |")
                    continue
                stall, t, w, v = simulate(angs, tq, br, L, theta_end, s=s, Fin=Fin)
                verdict = "FAIL (stalls)" if stall is not None else ("OK" if v < 0.5 else "lands too fast (brake)")
                R.append(f"| {s*100:.0f} um | {lab} | {start_ratio:.2f} | {stall if stall else '-'} | {t*1e6:.0f} us | {v:.2f} m/s | {verdict} |")
        R.append("")
    R.append("Pin fracture (reviewer R3): pin-tip stress ~2-4 GPa at 2 m/s, scaling ~v; DRIE Si fracture ~1-3 GPa -> landing speed must be < ~0.3-0.5 m/s.\n")
    txt = "\n".join(R) + "\n"
    open("results/s4_cycle_dynamics.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()

def hinge_free_schedule(d, kind):
    """At each angle, best torque among states whose net force presses the mover INTO the pivot (F_in >= 0).
    Returns list of (angle, torque, F_in, state) or None where no admissible state exists."""
    st = d["states"][kind]; out = []
    for a in sorted(float(x) for x in st):
        S = st[str(a)]
        th = -math.radians(a); cx, cy = -0.5, 0.5
        ux = math.cos(th) * cx - math.sin(th) * cy; uy = math.sin(th) * cx + math.cos(th) * cy
        n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
        adm = [(v[0], -(v[1] * ux + v[2] * uy), k) for k, v in S.items() if -(v[1] * ux + v[2] * uy) >= 0 and v[0] > 0]
        out.append((a,) + (max(adm) if adm else (None, None, None)))
    return out

if __name__ == "__main__":
    d = load(100)
    R = ["\n## Hinge-free schedule (only states that press the mover into its pivot edge; NUMERICAL)\n"]
    for kind in ("90", "180"):
        sch = hinge_free_schedule(d, kind)
        gaps = [a for a, t, f, k in sch if t is None]
        tmin = min((t for a, t, f, k in sch if t is not None), default=None)
        R.append(f"- {kind} deg: angles with NO admissible state: {gaps}; min admissible torque {tmin:.2e} N m" if tmin else f"- {kind} deg: no admissible state anywhere")
        R.append("  " + ", ".join(f"{a:.0f}:{k}" if k else f"{a:.0f}:none" for a, t, f, k in sch))
    open("results/s4_cycle_dynamics.md", "a").write("\n".join(R) + "\n"); print("\n".join(R))
