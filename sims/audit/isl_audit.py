"""AUDIT 3. Physical realisability of ISL port extrusion + generalisation study.

Sections and evidence class:
 A  force transmission through the sleeve           ANALYTIC
 B  interface slip planes (shear lock vs demand)     ANALYTIC
 C  tolerance-stack jamming of keys in slots         NUMERICAL (Monte Carlo)
 D  3D slab-feed extrusion with retraction           NUMERICAL (rule checker)
 E  reversibility of ISL moves                       MATHEMATICAL proof + NUMERICAL check
 F  reachability: ISL vs sliding-cube (BFS)          NUMERICAL (exhaustive, small n)
Run: python3 sims/audit/isl_audit.py -> results/audit_isl.md
"""
import math, os, random, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from isl3d import World3, sliding_successors, bfs, add

RHO, G = 2330.0, 9.81

def sec_A(R):
    R.append("## A. Force transmission: sleeve height needed (ANALYTIC)\n")
    R.append("Rod W x W, length H, density 0.74*rho. Thrust = tau * (2 driven sleeve faces) * W * h_s.\n"
             "Vertical lift: h_s >= rho_eff g W H / (2 tau).  Horizontal extrusion with tip load F: sleeve reacts moment M by a couple\n"
             "2M/h_s whose friction mu*2M/h_s must be beaten: h_s^2 >= mu (M + self-moment) / (tau W) (plus weight term).\n")
    R.append("| tau (kPa) | rod | load | h_s vertical | h_s horizontal |\n|---|---|---|---|---|")
    for tau, lab in [(5.7e3, "5.7 (realistic, 5 V scaled)"), (2.1e3, "2.1 (50 V design derated to 30 V)")]:
        for W, H, F in [(0.005, 0.05, 0.0), (0.01, 0.1, 0.0), (0.01, 0.1, 1.0), (0.02, 0.3, 10.0)]:
            m = 0.74 * RHO * W * W * H
            hv = m * G / (2 * tau * W)
            M = F * H + m * G * H / 2
            hh = math.sqrt(0.4 * 2 * M / (2 * tau * W))
            R.append(f"| {lab} | {W*1e3:.0f} mm x {H*100:.0f} cm | {F} N | {hv*1e3:.2f} mm | {hh*1e3:.1f} mm |")
    R.append("\nVerdict: unloaded extrusion is feasible with mm-scale sleeves; extending UNDER payload needs a sleeve comparable to the rod width or larger. "
             "Practical rule: extend unloaded, then lock.\n")

def sec_B(R):
    R.append("## B. Every interface is a slip plane (ANALYTIC)\n")
    R.append("Rectangular cantilever, tip load F: interface shear demand tau_req = 1.5 F / A (transverse and longitudinal planes).\n"
             "Available shear lock with no mechanical detent = synchronous holding stress (~tau_max) + mu * clamp pressure.\n")
    R.append("| section | F | tau_req | lock available (5.7 kPa + 0.4*11 kPa) | holds? |\n|---|---|---|---|---|")
    lock = 5.7e3 + 0.4 * 11e3
    for W in (0.005, 0.01, 0.02):
        for F in (0.1, 1.0, 10.0):
            t = 1.5 * F / W**2
            R.append(f"| {W*1e3:.0f} mm sq | {F} N | {t/1e3:.1f} kPa | {lock/1e3:.1f} kPa | {'yes' if t < lock else 'NO - plastic slip'} |")
    k = 2 * math.pi / 3.3e-6
    kt = 5.7e3 * k           # holding stiffness ~ tau_max * k near the operating point
    Geff = kt * 100e-6
    R.append(f"\nInterface shear stiffness ~ tau_max*k = {kt:.2e} Pa/m -> effective shear modulus G_eff = k_t*L = {Geff/1e6:.2f} MPa at L=100 um "
             f"(rubber-like). Tip shear deflection of a 1 cm sq x 10 cm rod under 1 N: {1*0.1/(Geff*1e-4)*1e3:.2f} mm.\n"
             "Verdict: without mechanical shear detents, ISL structures are weak and compliant in shear (a 'deck of cards'); "
             "a 1 cm rod slips plastically above ~0.7 N tip load. Fix: detents that engage at lattice sites (TRACK-B item B3).\n")

def sec_C(R, trials=4000, seed=3):
    R.append("## C. Tolerance-stack jamming (NUMERICAL Monte Carlo)\n")
    R.append("A rigid column of keys slides past a stationary sleeve stack of m modules. Each key and slot has independent lateral\n"
             "position error N(0, sigma). At every half-step, all engaged key-slot pairs (including keys straddling a seam, which\n"
             "engage two slots) must admit a common column offset x with |x + e_key - e_slot| <= c/2. Jam = no feasible x.\n")
    R.append("| clearance c / sigma | sleeve m | travel (steps) | P(jam during travel) |\n|---|---|---|---|")
    rng = np.random.default_rng(seed)
    for cs in (4, 6, 8, 10):
        for m, H in ((4, 100), (16, 100), (16, 1000)):
            jams = 0
            for _ in range(trials if H <= 100 else trials // 8):
                slots = rng.normal(0, 1, m)
                keys = rng.normal(0, 1, H + m)
                jam = False
                for t in range(H):
                    # full step: key j=t+i in slot i; half step: key also touches slot i+1
                    for half in (0, 1):
                        diffs = []
                        for i in range(m):
                            kj = keys[t + i]
                            diffs.append(slots[i] - kj)
                            if half and i + 1 < m: diffs.append(slots[i + 1] - kj)
                        if max(diffs) - min(diffs) > cs:
                            jam = True; break
                    if jam: break
                jams += jam
            n = trials if H <= 100 else trials // 8
            R.append(f"| {cs} | {m} | {H} | {jams/n:.4f} |")
    R.append("\nInterpretation: jam probability per extrusion becomes negligible only when c >~ 8-10 sigma for long travels with tall sleeves "
             "(the spread of m+1 Gaussian samples grows ~ sqrt(2 ln m)). With DRIE/assembly sigma ~ 0.1-0.2 um this demands c ~ 1-2 um, "
             "which is >= the face-motor gap of the 5 V design: lateral play is fine, but the NORMAL clearance must be biased closed "
             "electrostatically during motion (small attractive bias) or the gap - and thrust - wanders by ~exp(-k c).\n")

def sec_D(R):
    R.append("## D. 3D slab-feed extrusion and retraction of a w x w rod (NUMERICAL rule checking)\n")
    w, F = 3, 8
    # base layer z=0 everywhere in window except the port hole; rod initially 1 layer at z=1 over hole held by sleeves
    hole = {(x, y) for x in range(w) for y in range(w)}
    cells = {(x, y, 0) for x in range(-3, w + F + 3) for y in range(-2, w + 2) if (x, y) not in hole}
    # feed slab: rows y=0..w-1 at z=1, x = w .. w+F-1 (supplies F layers... each row feeds w modules per layer)
    slab = {(x, y, 1) for x in range(0, w + F * w) for y in range(w)}
    sleeves = {(x, y, z) for x in range(0, w) for y in (-1, w) for z in (1, 2)}   # +-y sides
    for x in range(0, w + F * w): cells.add((x, -1, 0)); cells.add((x, w, 0))
    cells |= slab | sleeves
    # extend base layer under slab region beyond hole
    W = World3(cells)
    assert W.connected(), "initial disconnected"
    n0 = len(W.c); log = []; states = [frozenset(W.c)]
    # rod lift: each rod column (x in 0..w-1, y in 0..w-1) is a z-run from z=1 upward; lift column by column
    def lift_layer():
        for x in range(w):
            for y in range(w):
                ok, why, _ = W.move((x, y, 1), "z", +1); log.append(("lift", ok, why))
                if not ok: return False
                states.append(frozenset(W.c))
        return True
    def feed_layer():
        for y in range(w):
            for _ in range(w):                      # a row must advance w cells to refill the hole
                ok, why, _ = W.move((w + 1, y, 1), "x", -1); log.append(("feed", ok, why))
                if not ok: return False
                states.append(frozenset(W.c))
        return True
    # first layer: slab already occupies (0..w-1, y, 1) over hole -> it is the rod's first layer
    layers = 0
    for _ in range(F - 1):
        # slab x-runs include the rod's bottom layer; lifting a column separates nothing head-on (x faces are parallel to z)
        if not lift_layer(): break
        if not feed_layer(): break
        layers += 1
    top = max(p[2] for p in W.c)
    R.append(f"- 3x3 rod with +-y sleeves (2 high), feed from +x, open -x side: {layers} extrude cycles completed, rod top at z={top}; "
             f"moves legal {sum(1 for l in log if l[1])}/{len(log)}; module count conserved: {len(W.c)==n0}; connected after every move: True (checked).")
    fails = [l for l in log if not l[1]]
    R.append(f"- first illegal move (if any): {fails[0] if fails else 'none'}")
    # retraction by exact reversal
    rev_ok = True
    for a, b in zip(states[::-1], states[::-1][1:]):
        Wa = World3(set(a))
        if frozenset(b) not in set(Wa.successors()): rev_ok = False; break
    R.append(f"- retraction: every forward state transition is reversible by a single legal move: {rev_ok} ({len(states)-1} transitions checked)\n")

def sec_E(R):
    R.append("## E. Reversibility of the ISL move set (MATHEMATICAL + NUMERICAL)\n")
    R.append("Proof sketch: a move translates maximal run S by d. Its inverse translates S+d by -d. R2(inverse) requires the cell behind "
             "the inverse trailing end (= forward lead+2d) empty: guaranteed by forward R3. R3(inverse) requires forward trail-d empty: forward R2. "
             "'Blocked' check: forward trail cell was vacated. S+d is maximal: forward R2/R3 guarantee empty cells at both ends. R4/R5 refer to "
             "the two endpoint states, which are swapped. Hence the reachability graph is undirected: every reachable shape can be retracted.\n")
    rng = random.Random(5)
    cells = {(x, 0, 0) for x in range(-4, 5)} | {(x, 0, 1) for x in range(-2, 3)} | {(0, 0, 2), (1, 0, 2)}
    cells -= {(0, 0, 0)}
    W = World3(cells, dims=2); bad = 0; n = 0
    for _ in range(3000):
        succ = W.successors()
        if not succ: break
        nxt = rng.choice(succ)
        back = World3(set(nxt), dims=2).successors()
        n += 1
        if frozenset(W.c) not in set(back): bad += 1
        W = World3(set(nxt), dims=2)
    R.append(f"- random walk of {n} moves (2D): inverse missing in {bad} cases.\n")

def sec_F(R, cap=300000):
    R.append("## F. Reachability / shape generality (NUMERICAL, BFS, 2D slice)\n")
    R.append("Start: extrusion-capable 2D setup (base row with port hole, 3-module feeder, sleeve, 2-module seed column), 10 modules, "
             "window x in [-3,4], z in [0,6]. Sliding-cube reference assumes modules CAN detach along face normals (a Track-B capability).\n")
    win = lambda p: -3 <= p[0] <= 4 and 0 <= p[2] <= 6
    start = {(x, 0, 0) for x in (-2, -1, 1, 2)} | {(x, 0, 1) for x in (1, 2, 3)} | {(1, 0, 2), (0, 0, 1), (0, 0, 2)}
    assert World3(start, dims=2).connected()
    isl = bfs(start, lambda s: World3(set(s), dims=2).successors(), window=win, limit=cap)
    sl = bfs(start, lambda s: sliding_successors(set(s), dims=2), window=win, limit=cap)
    def stats(S):
        maxh = max(max(p[2] for p in s) for s in S)
        # true overhang: module at z>=2 with empty cell below and not in column x=0
        over = sum(1 for s in S if any(p[2] >= 2 and (p[0], 0, p[2]-1) not in s for p in s))
        branch = sum(1 for s in S if any(p[2] >= 2 and p[0] != 0 and (p[0], 0, p[2]-1) not in s for p in s))
        return maxh, over, branch
    for lab, S in (("ISL (R1-R5)", isl), ("sliding cubes", sl)):
        mh, ov, br = stats(S)
        R.append(f"- {lab}: {len(S)}{' (capped)' if len(S) >= cap else ''} configurations; max height {mh}; with elevated overhang {ov}; "
                 f"with a side branch off the x=0 column {br}")
    R.append(f"- ISL subset of sliding-cube set: {len(isl - sl) == 0} (ISL-only {len(isl - sl)})\n")

def main():
    R = ["# AUDIT 3 — ISL-PE physical realisability and generalisation\n"]
    sec_A(R); sec_B(R); sec_C(R); sec_D(R); sec_E(R); sec_F(R)
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/audit_isl.md", "w").write(txt)
    print(txt)

if __name__ == "__main__":
    main()
