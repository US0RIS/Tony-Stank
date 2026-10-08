"""SESSION 4 / PHASE 10. Minimum module size and required material improvement (MATHEMATICAL, from the
NUMERICAL 100 um FD start-torque ratios). Exact relations used:
  start ratio(L) = r100 * (L/100um)^2 * (Jr*sq / 0.52 T)^2 * derate / (F_adh / F_adh,humid)
(similarity scaling: magnetic torque ~ L^3, peel torque ~ F_adh L; linear magnetics: torque ~ (Jr*sq)^2).
Requirement: start ratio >= 2. Thin-film limit: bars <= 50 um thick (geometry scales; at 1 mm bars are 40 um).
Run: python3 sims/s4/verdict_numbers.py -> results/s4_verdict_numbers.md"""
import json, math, os

def main():
    d = json.load(open("results/s4_pivot_real_100.json"))
    st = d["states"]
    r100 = {}
    for kind in ("90", "180"):
        a0 = sorted(float(a) for a in st[kind])[0]
        best = max(v[0] for v in st[kind][str(a0)].values())
        r100[kind] = best / (4.07e-6 * 100e-6)
    r = min(r100.values())
    R = ["# Session 4 — verdict numbers (MATHEMATICAL from NUMERICAL start-torque ratios)\n",
         f"Start torque / humid peel torque at 100 um (CoP Jr 0.65 T, squareness 0.8 -> Jr*sq = 0.52 T): 90 deg {r100['90']:.3f}, 180 deg {r100['180']:.3f}; governing (worse) = {r:.3f}\n",
         "## Minimum module size L_min for start margin >= 2\n",
         "| material Jr*sq (T) | adhesion | 3D derate | L_min (um) |\n|---|---|---|---|"]
    rows = {}
    for jr, lab in ((0.52, "CoP sq 0.8 (best available, SNIPPET)"), (1.0, "1.0 T switchable film (NOT DEMONSTRATED)"), (2.4, "2.4 T (FeCo saturation; physical ceiling)")):
        for fa, flab in ((1.0, "humid"), (0.1, "engineered dry, 10x lower (ASSUMED)")):
            for der in (1.0, 0.5):
                ratio100 = r * (jr / 0.52)**2 * der / fa
                Lmin = 100 * math.sqrt(2 / ratio100)
                rows[(jr, fa, der)] = Lmin
                R.append(f"| {jr} ({lab}) | {flab} | {der} | {Lmin:.0f} |")
    need = 2 / r
    R.append(f"\n## What 100 um would require (humid, derate 1.0)\nTorque must rise x{need:.0f}. With linear magnetics this needs Jr*sq = {0.52*math.sqrt(need):.2f} T, "
             f"which exceeds the saturation polarisation of every known material (max ~2.4 T, FeCo). With the 2.4 T ceiling, adhesion must also fall by "
             f"x{need/(2.4/0.52)**2:.1f}.")
    need2 = 2 / (r / 0.1)
    R.append(f"With engineered 10x-lower adhesion: Jr*sq >= {0.52*math.sqrt(max(need2,1)):.2f} T switchable film needed (no film found above 0.65 T Jr; squareness unknown).\n")
    txt = "\n".join(R) + "\n"
    open("results/s4_verdict_numbers.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
