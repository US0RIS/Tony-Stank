"""SESSION 3 / PHASE 4. Reconfiguration generality on common ground.

All models: 2D vertical slice, garment = fixed row z = -1, window x in [-2,5], z in [0,5],
N = 8 modules, identical start (6 on the garment row + 2 on top). Exhaustive BFS
(capped; cap reported). NUMERICAL SIMULATION; limitations observed in a bounded search
are NOT proofs.

Models (move rules encode the physical mechanism):
  SL   sliding squares (electrostatic face drive; straight slides + convex transitions)
  PVs  magnetic pivots, STRICT: 90/180 deg pivots about a corner; swept cells free;
       destination support D (touches pivot corner, shares an edge with the target) AND
       source S (touches corner, shares an edge with the start cell) must exist
       -> push+pull, torque margin 4-9 at 100 um (sims/s3/mag_pivot.py)
  PVl  magnetic pivots, LENIENT: only D required (pull only; margin 1.7-2 at 100 um)
  ISL  interlocked sliding lattice (sessions 1-2)
  FC   folding chain anchored at (0,0): rotate the sub-chain beyond unit i by +-90 deg
       about unit i, with swept-area collision checking
Metrics: reachable configurations, max height, branch, cavity, cantilever (>=2), BFS
depth to first occurrence, and fraction of moves whose reverse is also legal.
Run: python3 sims/s3/generality.py -> results/s3_generality.md
"""
import math, os, sys
from collections import deque
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "audit"))
from isl3d import World3, sliding_successors

XMIN, XMAX, ZMAX = -2, 5, 5
CAP = 200000

def inwin(c): return XMIN <= c[0] <= XMAX and 0 <= c[1] <= ZMAX

def connected(cells):
    cells = set(cells)
    start = [c for c in cells if c[1] == 0]
    seen = set(start); dq = deque(start)
    while dq:
        x, z = dq.popleft()
        for q in ((x+1, z), (x-1, z), (x, z+1), (x, z-1)):
            if q in cells and q not in seen: seen.add(q); dq.append(q)
    return len(seen) == len(cells)

def occ(c, cells): return c in cells or c[1] < 0

# ---------- pivot model ----------
def square_pts(cx, cz, s=0.96):
    h = s / 2
    return [(cx + a * h, cz + b * h) for a in (-1, 0, 1) for b in (-1, 0, 1)]

def rot_pt(p, c, ang):
    dx, dz = p[0] - c[0], p[1] - c[1]
    ca, sa = math.cos(ang), math.sin(ang)
    return (c[0] + ca * dx - sa * dz, c[1] + sa * dx + ca * dz)

def swept_cells(A, c, ang, steps=12):
    a = (A[0] + 0.5, A[1] + 0.5); out = set()
    for k in range(steps + 1):
        t = ang * k / steps
        for p in square_pts(*rot_pt(a, c, t)):
            out.add((math.floor(p[0]), math.floor(p[1])))
    return out

def touches(cell, c):
    return cell[0] <= c[0] <= cell[0] + 1 and cell[1] <= c[1] <= cell[1] + 1

def edge_adj(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

def pivot_successors(cells, strict):
    cells = set(cells); out = set()
    for A in cells:
        rest = cells - {A}
        if not connected(rest) and rest: continue
        for c in ((A[0], A[1]), (A[0] + 1, A[1]), (A[0], A[1] + 1), (A[0] + 1, A[1] + 1)):
            for ang in (math.pi / 2, -math.pi / 2, math.pi, -math.pi):
                a = (A[0] + 0.5, A[1] + 0.5); b = rot_pt(a, c, ang)
                B = (math.floor(b[0] + 1e-9 - 0.5 + 0.5), math.floor(b[1] + 1e-9 - 0.5 + 0.5))
                B = (round(b[0] - 0.5), round(b[1] - 0.5))
                if not inwin(B) or occ(B, rest): continue
                sw = swept_cells(A, c, ang) - {A, B}
                if any(occ(q, rest) for q in sw): continue
                # neighbours touching the pivot corner (modules or garment cells)
                cand = [q for q in list(rest) + [(x, -1) for x in range(XMIN - 1, XMAX + 2)] if touches(q, c)]
                D = [q for q in cand if edge_adj(q, B)]
                S = [q for q in cand if edge_adj(q, A)]
                if not D: continue
                if strict and not S: continue
                new = rest | {B}
                if connected(new): out.add(frozenset(new))
    return out

# ---------- chain model ----------
def chain_successors(chain):
    """chain: tuple of cells, chain[0] anchored. Rotate tail beyond unit i about unit i centre."""
    out = set(); n = len(chain)
    for i in range(n - 1):
        piv = (chain[i][0] + 0.5, chain[i][1] + 0.5)
        fixed = set(chain[:i + 1])
        blockers = set(chain[:i])          # unit i is the hinge partner; its overlap is resolved by the hinge geometry
        for ang in (math.pi / 2, -math.pi / 2):
            new_tail = []
            ok = True
            for cell in chain[i + 1:]:
                p = rot_pt((cell[0] + 0.5, cell[1] + 0.5), piv, ang)
                q = (round(p[0] - 0.5), round(p[1] - 0.5))
                if not inwin(q) or q in fixed: ok = False; break
                new_tail.append(q)
            if not ok or len(set(new_tail)) != len(new_tail): continue
            # swept-area collision: tail squares at intermediate angles vs fixed squares/garment
            for k in range(1, 12):
                t = ang * k / 12
                for cell in chain[i + 1:]:
                    for p in square_pts(*rot_pt((cell[0] + 0.5, cell[1] + 0.5), piv, t), s=0.9):
                        q = (math.floor(p[0]), math.floor(p[1]))
                        if q in blockers or q[1] < 0: ok = False; break
                    if not ok: break
                if not ok: break
            if ok: out.add(tuple(chain[:i + 1]) + tuple(new_tail))
    return out

# ---------- metrics ----------
def metrics(shape):
    s = set(shape)
    maxh = max(c[1] for c in s)
    branch = any(c[1] >= 1 and sum((c[0] + dx, c[1] + dz) in s for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 3 for c in s)
    # cavity: empty in-window cells unreachable from the border/outside
    W = [(x, z) for x in range(XMIN - 1, XMAX + 2) for z in range(0, ZMAX + 2)]
    seen = set(); dq = deque([(XMIN - 1, ZMAX + 1)])
    while dq:
        p = dq.popleft()
        if p in seen or p in s: continue
        if not (XMIN - 1 <= p[0] <= XMAX + 1 and 0 <= p[1] <= ZMAX + 1): continue
        seen.add(p)
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)): dq.append((p[0] + d[0], p[1] + d[1]))
    cavity = any(p not in s and p not in seen for p in W if 0 <= p[1])
    cant = False
    for z in range(1, ZMAX + 1):
        run = 0
        for x in range(XMIN, XMAX + 1):
            if (x, z) in s and (x, z - 1) not in s: run += 1; cant |= run >= 2
            else: run = 0
    return maxh, branch, cavity, cant

def explore(start, succ, key=lambda st: st, shape=lambda st: st):
    depth = {start: 0}; dq = deque([start]); first = {}
    nrev = nedge = 0
    shapes = set()
    while dq and len(depth) < CAP:
        st = dq.popleft(); sh = frozenset(shape(st)); shapes.add(sh)
        mh, br, cv, ca = metrics(sh)
        for name, flag in (("branch", br), ("cavity", cv), ("cantilever", ca), (f"height>=4", mh >= 4)):
            if flag and name not in first: first[name] = depth[st]
        for t in succ(st):
            nedge += 1
            if t not in depth:
                depth[t] = depth[st] + 1; dq.append(t)
    # reversibility sample
    import random
    rnd = random.Random(0); sample = rnd.sample(list(depth), min(300, len(depth)))
    for st in sample:
        for t in list(succ(st))[:5]:
            nrev += 1 if st in succ(t) else 0
    tested = sum(min(5, len(succ(st))) for st in sample)
    return depth, shapes, first, (nrev / tested if tested else float("nan"))

def main():
    start8 = frozenset({(x, 0) for x in range(6)} | {(1, 1), (2, 1)})
    R = ["# Session 3 — reconfiguration generality on common ground (NUMERICAL SIMULATION, bounded BFS)\n",
         f"2D slice, window x in [{XMIN},{XMAX}], z in [0,{ZMAX}], N = 8, start = 6 on garment + 2 on top. Cap {CAP} states.\n",
         "| model | states | distinct shapes | max height | branch (depth) | cavity (depth) | cantilever>=2 (depth) | height>=4 (depth) | reverse-move fraction |",
         "|---|---|---|---|---|---|---|---|---|"]
    to3 = lambda st: {(c[0], 0, c[1]) for c in st}
    from3 = lambda st: frozenset((c[0], c[2]) for c in st)
    models = [
        ("SL sliding", start8, lambda st: {from3(t) for t in sliding_successors(to3(st), dims=2) if all(inwin(c) for c in from3(t))}),
        ("PVs pivot strict", start8, lambda st: pivot_successors(st, True)),
        ("PVl pivot lenient", start8, lambda st: pivot_successors(st, False)),
        ("ISL", start8, lambda st: {from3(t) for t in World3(to3(st), dims=2).successors() if all(inwin(c) for c in from3(t))}),
    ]
    res = {}
    for name, st0, succ in models:
        depth, shapes, first, rev = explore(st0, succ)
        mh = max(metrics(s)[0] for s in shapes)
        capped = " (capped)" if len(depth) >= CAP else ""
        res[name] = (len(depth), len(shapes), first)
        R.append(f"| {name} | {len(depth)}{capped} | {len(shapes)} | {mh} | {first.get('branch','-')} | {first.get('cavity','-')} | {first.get('cantilever','-')} | {first.get('height>=4','-')} | {rev:.2f} |")
    chain0 = ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (5, 2))   # in-window, anchored at (0,0)
    depth, shapes, first, rev = explore(chain0, chain_successors, shape=lambda st: st)
    mh = max(metrics(s)[0] for s in shapes)
    R.append(f"| FC folding chain (anchored at (0,0)) | {len(depth)}{' (capped)' if len(depth) >= CAP else ''} | {len(shapes)} | {mh} | {first.get('branch','-')} | {first.get('cavity','-')} | {first.get('cantilever','-')} | {first.get('height>=4','-')} | {rev:.2f} |")
    allsaw = []
    def rec(path):
        if len(path) == 8: allsaw.append(tuple(path)); return
        x, z = path[-1]
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + d[0], z + d[1])
            if inwin(q) and q not in path: rec(path + [q])
    rec([(0, 0)])
    R.append(f"\nFC completeness: {len(depth)} conformations reached of {len(allsaw)} self-avoiding 8-unit chains anchored at (0,0) in the window "
             f"({'all' if len(depth) == len(allsaw) else 'not all'}).")
    R.append("\n'-' = not found within the bounded search. Depth = minimum number of moves from the start.\n")
    R.append("Notes: FC starts as an L-shaped chain anchored at (0,0) because a chain cannot share SL's start configuration; its garment contact is only the anchored unit "
             "(garment contact of other units is not required for connectivity). ISL conserves the garment-contact count (proven), so from this "
             "start it cannot lift anything; see audit_isl.md for ISL from a port-equipped start.\n")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s3_generality.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
