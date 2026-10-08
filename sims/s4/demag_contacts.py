"""SESSION 4. (1) Open-circuit self-demagnetisation of the switchable bars (Aharoni prism formula,
MATHEMATICAL) and the irreversible remanence loss for a linear-recoil / square-knee loop model.
(2) Attached-state clamping force between two faces from the FD model (NUMERICAL) -> contact force per
Au pad -> Holm resistance -> contact voltage during switching pulses vs softening/melting voltages.
Run: python3 sims/s4/demag_contacts.py -> results/s4_demag_contacts.md
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
MU0 = 4e-7 * math.pi

def aharoni_Nz(a, b, c):
    """Demagnetising factor along c for a prism 2a x 2b x 2c (Aharoni, J. Appl. Phys. 83, 3432 (1998))."""
    a2, b2, c2 = a * a, b * b, c * c
    abc = math.sqrt(a2 + b2 + c2); ab = math.sqrt(a2 + b2); bc = math.sqrt(b2 + c2); ac = math.sqrt(a2 + c2)
    t = ((b2 - c2) / (2 * b * c)) * math.log((abc - a) / (abc + a))
    t += ((a2 - c2) / (2 * a * c)) * math.log((abc - b) / (abc + b))
    t += (b / (2 * c)) * math.log((ab + a) / (ab - a))
    t += (a / (2 * c)) * math.log((ab + b) / (ab - b))
    t += (c / (2 * a)) * math.log((bc - b) / (bc + b))
    t += (c / (2 * b)) * math.log((ac - a) / (ac + a))
    t += 2 * math.atan(a * b / (c * abc))
    t += (a**3 + b**3 - 2 * c**3) / (3 * a * b * c)
    t += (a2 + b2 - 2 * c2) / (3 * a * b * c) * abc
    t += (c / (a * b)) * (ac + bc)
    t -= (ab**3 + bc**3 + ac**3) / (3 * a * b * c)
    return t / math.pi

def remanence_after_open(Jr, Hc, N, mur=1.2):
    """Linear recoil line B = Jr + mu0*mur*H down to the knee at H = -Hc (square-knee model, OPTIMISTIC).
    Open-circuit operating point: H = -N M_total with M_total ~ Jr/mu0 + (mur-1) H. If |H| > Hc the bar
    demagnetises down to the point where |H| = Hc (irreversible)."""
    M = Jr / MU0
    H = -N * M / (1 + N * (mur - 1))
    if -H <= Hc:
        return Jr, H, False
    # irreversibly reduced remanence such that the self field equals -Hc
    M_new = Hc * (1 + N * (mur - 1)) / N
    return MU0 * M_new, -Hc, True

def main():
    R = ["# Session 4 — open-circuit demagnetisation and contact current capacity\n"]
    R.append("## 1. Self-demagnetisation of a switchable bar in open circuit (MATHEMATICAL; square-knee loop = optimistic)\n")
    R.append("| L | bar (l x w x t, um) | N along length | material | self field |H| (kA/m) | Hc (kA/m) | retained Jr (T) | irreversible loss |\n|---|---|---|---|---|---|---|---|---|")
    mats = {"CoP": (0.65, 28e3), "CoNiP": (0.40, 45e3), "CoPtP": (0.35, 92e3), "AlNiCo-5 (bulk ref.)": (1.25, 50e3)}
    for L, (l, w, t) in ((100, (58, 12, 4)), (100, (58, 9.5, 4)), (300, (174, 36, 12)), (1000, (580, 120, 40))):
        N = aharoni_Nz(w / 2, t / 2, l / 2)
        for m, (Jr, Hc) in mats.items():
            Jn, H, lost = remanence_after_open(Jr, Hc, N)
            R.append(f"| {L} | {l} x {w} x {t} | {N:.4f} | {m} | {-H/1e3:.1f} | {Hc/1e3:.0f} | {Jn:.2f} | {'YES -> ' + format(100*(1-Jn/Jr), '.0f') + ' %' if lost else 'no'} |")
    R.append("\nNote: pole pieces at the bar ends reduce the effective N (flux closes partly through iron); the bare-bar value is the open-circuit "
             "worst case. During a pivot the mover's faces and the pushing neighbour's face are in open circuit or opposed by a like pole "
             "(push), which adds a reverse field (see pivot_real reverse-H column).\n")
    # ---------------- contacts ----------------
    import pivot_real as pr, magfd as fd
    R.append("## 2. Attached-state clamp force and contact voltage during switching pulses\n")
    for Lum in (100, 300):
        L = Lum * 1e-6; D = pr.design(L)
        h = 0.75e-6 if Lum == 100 else 2e-6
        mover = pr.face_parts(D, "bottom", +1, 0.65, 0.8)
        best = None
        for sS in (+1, -1):
            S = pr.face_parts(D, "top", sS, 0.65, 0.8)
            T, Fx, Fy, Bi, Hr = pr.run_angle(L, mover, S, [], 0.0, (L, L + D["c"]), h, D["c"])
            Fn = -Fy * D["depth_pole"]          # attraction pulls mover down (negative Fy)
            if best is None or Fn > best[0]: best = (Fn, sS, Bi)
        Fn = best[0]
        p_face = Fn / L**2
        F_pad = max(Fn, 0) * 0.5 / 4         # ASSUMED: half of the clamp force carried by the 4 pads (rest by pole pieces/standoffs)
        H_au = 1e9; rho = 2.2e-8
        a = math.sqrt(F_pad / (math.pi * H_au)) if F_pad > 0 else 0
        R_clean = rho / (2 * a) if a > 0 else float("inf")
        R.append(f"### L = {Lum} um: clamp force {Fn*1e6:.1f} uN (face-averaged {p_face/1e3:.2f} kPa; CoP, sq 0.8, 2D x pole depth); force per pad {F_pad*1e6:.2f} uN; "
                 f"Holm a-spot radius {a*1e9:.0f} nm; R (clean, bulk) {R_clean:.2f} ohm, x10 film factor {10*R_clean:.1f} ohm\n")
        R.append("| pulse current into module (A) | pads sharing (attached faces x 4) | current per pad (mA) | contact voltage clean / film (V) | vs Au softening 0.08 V / melting 0.43 V |\n|---|---|---|---|---|")
        for I in (0.2, 0.4, 0.8):
            for nf in (1, 3):
                ip = I / (4 * nf)
                v1, v2 = ip * R_clean, ip * 10 * R_clean
                verdict = "MELT" if v1 > 0.43 else ("SOFTEN" if v1 > 0.08 else ("film soften" if v2 > 0.08 else "ok"))
                R.append(f"| {I} | {4*nf} | {ip*1e3:.0f} | {v1:.3f} / {v2:.2f} | {verdict} |")
        R.append("")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s4_demag_contacts.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
