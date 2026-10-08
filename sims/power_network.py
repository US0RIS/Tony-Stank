"""S3. Power delivery through a lattice of touching modules.

Each module is a node; face contacts are resistors R_c (or |Z| of a capacitive
coupling); modules on the garment layer connect to the supply V_bus through R_c;
each module sinks constant current I = P/V_bus (linearised; valid while the drop
is small). Solves the sparse nodal equations exactly (SIMULATED), compares with
the DERIVED chain formula dV = I R h(h+1)/2, and derives electrical reach.

Run: python3 sims/power_network.py -> results/power_network.md
"""
import math, os, sys, itertools
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def solve(cells, grounded, R, I):
    """cells: list of (x,y,z) occupied; grounded: set of cells touching garment.
    Returns dict cell -> voltage drop below V_bus."""
    index = {c: i for i, c in enumerate(cells)}
    n = len(cells)
    g = 1.0 / R
    rows, cols, vals = [], [], []
    diag = np.zeros(n)
    for c, i in index.items():
        x, y, z = c
        for d in ((1,0,0),(0,1,0),(0,0,1)):
            nb = (x+d[0], y+d[1], z+d[2])
            j = index.get(nb)
            if j is not None:
                rows += [i, j]; cols += [j, i]; vals += [-g, -g]
                diag[i] += g; diag[j] += g
        if c in grounded:
            diag[i] += g
    A = sp.csr_matrix((vals, (rows, cols)), shape=(n, n)) + sp.diags(diag)
    b = np.full(n, I)               # drop u satisfies A u = I (u = V_bus - v)
    u = spla.spsolve(A.tocsc(), b)
    return {c: u[index[c]] for c in cells}

def chain_formula(h, R, I):
    # h modules stacked, bottom one connected to garment via R: drop at top
    return I * R * h * (h + 1) / 2

def main():
    rep = ["# S3 power distribution through contact lattices (SIMULATED + DERIVED)\n"]
    R, P, V = 10.0, 1e-6, 3.0
    I = P / V
    rep.append(f"Baseline: R_contact={R} ohm, P_module={P*1e6} uW, V_bus={V} V, I={I*1e6:.3f} uA\n")
    rep.append("## 1. Validation: vertical chain vs analytic\n")
    for h in (10, 100, 1000):
        cells = [(0, 0, z) for z in range(h)]
        u = solve(cells, {(0, 0, 0)}, R, I)
        rep.append(f"- h={h}: simulated top drop {u[(0,0,h-1)]:.6e} V, formula {chain_formula(h,R,I):.6e} V")
    rep.append("\n## 2. Does lateral parallelism help? Uniform tower w x w x h on the garment\n")
    rep.append("| w | h | max drop (V) | chain formula (V) |\n|---|---|---|---|")
    for w, h in [(1, 100), (5, 100), (20, 100)]:
        cells = list(itertools.product(range(w), range(w), range(h)))
        gr = {c for c in cells if c[2] == 0}
        u = solve(cells, gr, R, I)
        rep.append(f"| {w} | {h} | {max(u.values()):.4e} | {chain_formula(h,R,I):.4e} |")
    rep.append("\nResult: for uniform load on a ground plane, columns are electrically independent: drop depends on height in hops only.\n")
    rep.append("## 3. Horizontal arm fed through a narrow root (current funnelling)\n")
    rep.append("Arm cross-section a x a, length Lh, attached to a garment patch only at its root column.\n")
    rep.append("| a | arm length (hops) | max drop (V) | chain formula for same hop count (V) | ratio |\n|---|---|---|---|---|")
    for a, Lh in [(1, 200), (4, 200), (10, 200)]:
        cells = list(itertools.product(range(Lh), range(a), range(a)))
        gr = {c for c in cells if c[0] == 0}       # garment at x = -1 face of root slice
        u = solve(cells, gr, R, I)
        rep.append(f"| {a} | {Lh} | {max(u.values()):.4e} | {chain_formula(Lh,R,I):.4e} | {max(u.values())/chain_formula(Lh,R,I):.3f} |")
    rep.append("\nA root-fed prismatic arm behaves like a single chain of the same length (cross-section cancels: a^2 more current, a^2 more paths).\n")
    # reach table
    rep.append("## 4. Electrical reach h_max (hops) for drop <= 10 % of V_bus: h_max ~ sqrt(0.2 V^2 / (P R))\n")
    rep.append("| R_contact (ohm) | P (W) | V_bus (V) | h_max (hops) | reach @100 um | reach @10 um |\n|---|---|---|---|---|---|")
    for Rc in (1, 100, 1e4):
        for Pm in (1e-8, 1e-6, 1e-5):
            for Vb in (3, 30):
                h = math.sqrt(0.2 * Vb**2 / (Pm * Rc))
                rep.append(f"| {Rc:g} | {Pm:g} | {Vb} | {h:.0f} | {h*100e-6*100:.2f} cm | {h*10e-6*100:.3f} cm |")
    # capacitive coupling impedance
    rep.append("\n## 5. Capacitive face coupling as the 'contact'\n")
    eps0 = 8.854e-12
    for L, gap, frac in [(100e-6, 100e-9, 0.3), (100e-6, 1e-6, 0.3), (1e-3, 1e-6, 0.3)]:
        C = eps0 * frac * L**2 / gap / 2      # two plates in series (signal + return)
        for f in (1e7, 1e8):
            Z = 1 / (2 * math.pi * f * C)
            rep.append(f"- L={L*1e6:.0f} um, gap={gap*1e9:.0f} nm, f={f/1e6:.0f} MHz: C={C*1e12:.3f} pF, |Z|={Z:.0f} ohm")
    # hold-up capacitor
    rep.append("\n## 6. Hold-up energy for loss of contact (trench capacitor 57.8 nF/mm^2, VERIFIED snippet; area = one face)\n")
    for L in (1e-3, 100e-6, 10e-6):
        C = 57.8e-9 * (L * 1e3) ** 2
        E = 0.5 * C * (3.0**2 - 2.0**2)
        rep.append(f"- L={L*1e6:.0f} um: C={C*1e9:.3g} nF, usable E(3V->2V)={E*1e9:.3g} nJ, "
                   f"ride-through @1 uW={E/1e-6*1e3:.3g} ms, @10 nW={E/1e-8:.3g} s")
    # swarm budget
    rep.append("\n## 7. Swarm power budget (battery 15 Wh, ~phone class)\n")
    rep.append("| volume | L | N modules | P/module | total P | battery life |\n|---|---|---|---|---|---|")
    for vol in (1e-6, 1e-5, 1e-4):
        for L in (1e-3, 100e-6, 10e-6):
            N = vol / L**3
            for Pm in (1e-8, 1e-6):
                Pt = N * Pm
                rep.append(f"| {vol*1e6:.0f} cm^3 | {L*1e6:.0f} um | {N:.1e} | {Pm:g} W | {Pt:.3g} W | {15/Pt:.3g} h |")
    txt = "\n".join(rep) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/power_network.md", "w").write(txt)
    print(txt)

if __name__ == "__main__":
    main()
