"""SESSION 3. 3D check of pivot-vs-sliding generality (NUMERICAL SIMULATION, exhaustive BFS,
small N). Cubes on a garment plane z = -1; window x,y in [0,2], z in [0,2].
Pivot rule (strict): rotate a cube +-90 or 180 deg about one of its 12 edges; swept cells free;
destination support D (shares a face with target, contains the pivot edge) and source support S
(shares a face with start, contains the pivot edge) required; connectivity before (rest) and after.
Sliding rule: isl3d.sliding_successors (straight slides + convex transitions).
Run: python3 sims/s3/generality3d.py -> results/s3_generality3d.md
"""
import itertools, math, os, sys
from collections import deque
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "audit"))
from isl3d import World3, sliding_successors

LO, HI, ZH = 0, 2, 2
def inwin(c): return LO <= c[0] <= HI and LO <= c[1] <= HI and 0 <= c[2] <= ZH
def occ(c, S): return c in S or c[2] < 0
def connected(S): return World3(set(S)).connected()

def rotm(axis, ang):
    c, s = math.cos(ang), math.sin(ang)
    if axis == 0: return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == 1: return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

PTS = np.array(list(itertools.product((-0.48, 0, 0.48), repeat=3)))

ROT = {(a, ang): np.array([rotm(a, ang * k / 12) for k in range(1, 12)]) for a in range(3) for ang in (math.pi / 2, -math.pi / 2, math.pi)}

def edges(A):
    """Edges of cube A as (axis, point on edge line)."""
    out = []
    for axis in range(3):
        o = [i for i in range(3) if i != axis]
        for a in (0, 1):
            for b in (0, 1):
                p = [A[0], A[1], A[2]]
                p[o[0]] += a; p[o[1]] += b
                out.append((axis, tuple(p)))
    return out

def contains_edge(cell, axis, p):
    o = [i for i in range(3) if i != axis]
    return all(cell[i] <= p[i] <= cell[i] + 1 for i in o) and cell[axis] == p[axis] - 0 if False else \
           all(cell[i] <= p[i] <= cell[i] + 1 for i in o) and cell[axis] == math.floor(p[axis])

def face_adj(a, b): return sum(abs(a[i] - b[i]) for i in range(3)) == 1

def pivot_succ(S):
    S = set(S); out = set()
    ground = [(x, y, -1) for x in range(LO - 1, HI + 2) for y in range(LO - 1, HI + 2)]
    for A in S:
        rest = S - {A}
        if rest and not connected(rest): continue
        ctr = np.array(A) + 0.5
        for axis, p in edges(A):
            P = np.array(p, float); P[axis] = ctr[axis]
            for ang in (math.pi / 2, -math.pi / 2, math.pi):
                Bc = rotm(axis, ang) @ (ctr - P) + P
                B = tuple(int(round(v - 0.5)) for v in Bc)
                if not inwin(B) or occ(B, rest): continue
                Q = np.einsum('kij,nj->kni', ROT[(axis, ang)], (ctr + PTS) - P) + P
                sw = set(map(tuple, np.floor(Q.reshape(-1, 3)).astype(int).tolist()))
                sw -= {A, B}
                if any(occ(q, rest) for q in sw): continue
                cand = [q for q in list(rest) + ground if contains_edge(q, axis, p)]
                D = [q for q in cand if face_adj(q, B)]; Ss = [q for q in cand if face_adj(q, A)]
                if not D or not Ss: continue
                new = rest | {B}
                if connected(new): out.add(frozenset(new))
    return out

def bfs(start, succ, cap=300000):
    seen = {start}; dq = deque([start])
    while dq and len(seen) < cap:
        s = dq.popleft()
        for t in succ(s):
            if t not in seen: seen.add(t); dq.append(t)
    return seen

def main():
    R = ["# Session 3 — 3D generality check (NUMERICAL SIMULATION, exhaustive within window 3x3x3)\n",
         "| N | sliding states | strict EPM-pivot states | pivot subset of sliding | sliding-only states | max height (sl/pv) |\n|---|---|---|---|---|---|"]
    starts = {5: frozenset({(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0), (1, 0, 1)}),
              6: frozenset({(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 0)})}
    mh = lambda S: max(max(c[2] for c in s) for s in S)
    for n, start in starts.items():
        sl = bfs(start, lambda s: {frozenset(t) for t in sliding_successors(set(s), dims=3) if all(inwin(c) for c in t)})
        pv = bfs(start, pivot_succ)
        R.append(f"| {n} | {len(sl)} | {len(pv)} | {pv <= sl} | {len(sl - pv)} ({100*len(sl - pv)/len(sl):.2f} %) | {mh(sl)}/{mh(pv)} |")
    R.append("\nBounded search only: not a universality proof. Window edges cause the missing pivot states (swept volume leaves the window).\n")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s3_generality3d.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
