"""AUDIT 2. Is lattice voltage drop really a function of height only?

NUMERICAL: sparse nodal solves of resistor lattices (sims/power_network.solve
generalised to per-edge resistances, per-node loads, failed contacts and a
resistive garment sheet). Compared against the S3 'height-only' formula
dV = I R h(h+1)/2.
Run: python3 sims/audit/power_audit.py -> results/audit_power.md
"""
import itertools, math, os, random
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.sparse.csgraph import connected_components

def solve(cells, loads, edge_R, ground_R):
    """cells: list; loads: dict cell->A; edge_R: dict (c1,c2)->ohm (missing = open);
    ground_R: dict cell->ohm to the supply (garment). Returns drop per cell, n_unpowered."""
    idx = {c: i for i, c in enumerate(cells)}
    n = len(cells)
    r, cidx, v = [], [], []
    diag = np.zeros(n)
    for (a, b), R in edge_R.items():
        g = 1 / R; i, j = idx[a], idx[b]
        r += [i, j]; cidx += [j, i]; v += [-g, -g]; diag[i] += g; diag[j] += g
    for c, R in ground_R.items():
        diag[idx[c]] += 1 / R
    A = (sp.csr_matrix((v, (r, cidx)), shape=(n, n)) + sp.diags(diag)).tocsr()
    # islands without ground are unpowered: remove them
    adj = sp.csr_matrix((np.ones(len(r)), (r, cidx)), shape=(n, n))
    ncomp, lab = connected_components(adj, directed=False)
    grounded_labels = {lab[idx[c]] for c in ground_R}
    keep = np.array([lab[i] in grounded_labels for i in range(n)])
    b = np.array([loads.get(c, 0.0) for c in cells])
    u = np.full(n, np.inf)
    ki = np.where(keep)[0]
    u[ki] = spla.spsolve(A[ki][:, ki].tocsc(), b[ki])
    return {c: u[idx[c]] for c in cells}, int((~keep).sum())

def lattice_edges(cells, R, rng=None, sigma=0.0, p_fail=0.0):
    s = set(cells); E = {}
    for c in cells:
        for d in ((1,0,0),(0,1,0),(0,0,1)):
            nb = (c[0]+d[0], c[1]+d[1], c[2]+d[2])
            if nb in s:
                if rng and rng.random() < p_fail: continue
                E[(c, nb)] = R * (math.exp(rng.gauss(0, sigma)) if (rng and sigma) else 1.0)
    return E

def formula(h, R, I):
    return I * R * h * (h + 1) / 2

def main():
    R0, P, V = 10.0, 1e-6, 3.0
    I = P / V
    out = ["# AUDIT 2 — lattice power: does drop depend only on height?\n",
           f"Baseline R={R0} ohm, P=1 uW, V=3 V. 'ratio' = max drop / height-only chain formula for the same height. NUMERICAL unless stated.\n"]
    w, h = 10, 40
    tower = list(itertools.product(range(w), range(w), range(h)))
    base = {c: R0 for c in tower if c[2] == 0}
    uni = {c: I for c in tower}
    f0 = formula(h, R0, I)
    def row(label, u, nun, ref=f0):
        finite = [x for x in u.values() if np.isfinite(x)]
        out.append(f"| {label} | {max(finite):.3e} | {max(finite)/ref:.2f} | {nun} |")
    out.append("| case (10x10x40 tower unless stated) | max drop (V) | ratio | unpowered modules |\n|---|---|---|---|")
    u, nun = solve(tower, uni, lattice_edges(tower, R0), base); row("uniform load, full footprint (S3 claim)", u, nun)
    rng = random.Random(0)
    act = {c: (100 * I if rng.random() < 0.01 else I) for c in tower}
    tot = sum(act.values()); act_scaled = act
    u, nun = solve(tower, act, lattice_edges(tower, R0), base); row("1 % of modules at 100x load (random), +99 % total power", u, nun)
    hot = {c: I for c in tower}
    for c in tower:
        if c[2] >= h - 3 and c[0] < 3 and c[1] < 3: hot[c] = 100 * I
    u, nun = solve(tower, hot, lattice_edges(tower, R0), base); row("hotspot: 27 modules at top corner x100", u, nun)
    hot_f = formula(h, R0, I) + 100 * I * R0 * h  # single column carrying a 100x module at top (ANALYTIC reference)
    out.append(f"|  (reference: single column with one 100x module on top, ANALYTIC) | {hot_f:.3e} | {hot_f/f0:.2f} | - |")
    narrow = {c: R0 for c in tower if c[2] == 0 and 4 <= c[0] <= 5 and 4 <= c[1] <= 5}
    u, nun = solve(tower, uni, lattice_edges(tower, R0), narrow); row("footprint only central 2x2 of 10x10", u, nun)
    one = {c: R0 for c in tower if c == (0, 0, 0)}
    u, nun = solve(tower, uni, lattice_edges(tower, R0), one); row("footprint single corner module", u, nun)
    # random contact resistance and failures
    for sig, pf in [(1.0, 0.0), (2.0, 0.0), (0.0, 0.1), (0.0, 0.3), (0.0, 0.6), (1.0, 0.3)]:
        rr = random.Random(1)
        u, nun = solve(tower, uni, lattice_edges(tower, R0, rr, sig, pf), base)
        row(f"lognormal R sigma={sig}, failed contacts {int(pf*100)} %", u, nun)
    out.append("\nNotes: lognormal cases hold the MEDIAN at R0; in a 3D lattice, spread is averaged out (ratio < 1). "
               "In a series column the expected drop scales with the MEAN R = R0 exp(sigma^2/2) (x1.65 at sigma=1, x7.4 at sigma=2) (ANALYTIC).")
    for pf in (0.001, 0.01, 0.02):
        out.append(f"- single 1x1x40 column, contact failure prob {pf}: P(whole column powered) = (1-p)^40 = {(1-pf)**40:.3f} (ANALYTIC); "
                   f"10x10 tower survives 30 % failures with ~6 isolated modules (NUMERICAL above). Redundant paths, not height, set robustness.")
    # resistive garment sheet: 30x30 garment nodes, tower 6x6x20 in middle, fed at one garment edge
    out.append("\n## Resistive garment sheet (supply enters at one garment edge)\n")
    out.append("| garment R per segment | max drop in tower (V) | ratio to height-only |\n|---|---|---|")
    G = 30; hh = 20
    tw = [(x, y, z) for x in range(12, 18) for y in range(12, 18) for z in range(1, hh + 1)]
    gnodes = [(x, y, 0) for x in range(G) for y in range(G)]
    cells = gnodes + tw
    for Rg in (0.01, 1.0, 10.0):
        E = lattice_edges(tw, R0)
        for x in range(G):
            for y in range(G):
                if x + 1 < G: E[((x, y, 0), (x + 1, y, 0))] = Rg
                if y + 1 < G: E[((x, y, 0), (x, y + 1, 0))] = Rg
        for c in tw:
            if c[2] == 1: E[((c[0], c[1], 0), c)] = R0
        feed = {(0, y, 0): 1e-3 for y in range(G)}
        u, _ = solve(cells, {c: I for c in tw}, E, feed)
        out.append(f"| {Rg} ohm | {max(u[c] for c in tw):.3e} | {max(u[c] for c in tw)/formula(hh, R0, I):.2f} |")
    out.append("\n## Two-conductor reality (ANALYTIC)\nSupply and return both traverse the lattice: drop doubles (x2) for identical contact pairs; data and power share these paths.\n")
    txt = "\n".join(out) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/audit_power.md", "w").write(txt)
    print(txt)

if __name__ == "__main__":
    main()
