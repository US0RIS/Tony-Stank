"""SESSION 4. Sensitivity of attached clamp and mid-pivot torque to clearance c and recess r at L = 100 um
(NUMERICAL). Used to bound the benefit of keeping absolute clearances at 1 um when scaling up
(similarity scaling would otherwise scale them with L).
Run: python3 sims/s4/gap_sensitivity.py -> results/s4_gap_sensitivity.md"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pivot_real as pr

def clamp_and_torque(c, r, h=0.5e-6, deg=45.0):
    L = 100e-6; D = pr.design(L); D["c"] = c; D["r"] = r
    mover = pr.face_parts(D, "bottom", +1) + pr.face_parts(D, "right", +1)
    best_clamp = 0.0
    for sS in (1, -1):
        S = pr.face_parts(D, "top", sS)
        _, Fx, Fy, _, _ = pr.run_angle(L, pr.face_parts(D, "bottom", +1), S, [], 0.0, (L, L + c), h, c)
        best_clamp = max(best_clamp, -Fy * D["depth_pole"])
    best_t = -1e9
    for sS in (1, 0, -1):
        for sD in (1, 0, -1):
            S = pr.face_parts(D, "top", sS); Dp = pr.face_parts(D, "top", sD)
            T, *_ = pr.run_angle(L, mover, S, Dp, -math.radians(deg), (L, L + c), h, c)
            best_t = max(best_t, -T * D["depth_pole"])
    return best_clamp, best_t

def main():
    R = ["# Session 4 — clearance/recess sensitivity at L = 100 um (NUMERICAL)\n",
         "| c (um) | r (um) | grid (um) | attached clamp (uN) | best torque at 45 deg (N m) |\n|---|---|---|---|---|"]
    for c, r, h in ((1e-6, 1e-6, 0.5e-6), (1e-6, 1e-6, 0.75e-6), (2e-6, 2e-6, 0.75e-6), (0.5e-6, 0.5e-6, 0.25e-6)):
        try:
            cl, t = clamp_and_torque(c, r, h)
            R.append(f"| {c*1e6:.1f} | {r*1e6:.1f} | {h*1e6:.2f} | {cl*1e6:.2f} | {t:.2e} |")
        except MemoryError:
            R.append(f"| {c*1e6:.1f} | {r*1e6:.1f} | {h*1e6:.2f} | memory | - |")
    txt = "\n".join(R) + "\n"
    open("results/s4_gap_sensitivity.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
