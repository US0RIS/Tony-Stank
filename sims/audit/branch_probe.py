"""Probe ISL 2D reachable set for genuine cantilever branches (NUMERICAL, BFS).
Cantilever arm = maximal horizontal run at height z>=2 whose modules all have empty
cells below them. Prints the longest arm found and the move sequence to reach it.
Run: python3 sims/audit/branch_probe.py -> results/audit_branch.md"""
import os, sys
from collections import deque
sys.path.insert(0, os.path.dirname(__file__))
from isl3d import World3

def arms(s):
    best = 0
    for z in range(2, 8):
        row = sorted(p[0] for p in s if p[2] == z and (p[0], 0, z - 1) not in s)
        run = 1
        for a, b in zip(row, row[1:]):
            run = run + 1 if b == a + 1 else 1
            best = max(best, run)
        if row: best = max(best, 1 if best == 0 else best)
    return best

def draw(s):
    xs = [p[0] for p in s]; zs = [p[2] for p in s]
    lines = []
    for z in range(max(zs), -2, -1):
        lines.append("".join("#" if (x, 0, z) in s else ("=" if z == -1 else ".") for x in range(min(xs) - 1, max(xs) + 2)))
    return "\n".join(lines)

def main(F=5):
    win = lambda p: -4 <= p[0] <= 6 and 0 <= p[2] <= 7
    start = frozenset({(x, 0, 0) for x in (-3, -2, -1, 1, 2, 3)} | {(x, 0, 1) for x in range(1, F + 1)} | {(1, 0, 2), (0, 0, 1), (0, 0, 2)})
    parent = {start: None}; dq = deque([start]); best = (0, start)
    while dq and len(parent) < 400000:
        s = dq.popleft()
        a = arms(s)
        if a > best[0]: best = (a, s)
        for t in World3(set(s), dims=2).successors():
            if t not in parent and all(win(p) for p in t):
                parent[t] = s; dq.append(t)
    path = []; s = best[1]
    while s is not None: path.append(s); s = parent[s]
    out = ["# Branch probe (NUMERICAL BFS, 2D ISL)\n",
           f"States explored: {len(parent)}{' (capped)' if len(parent) >= 400000 else ''}. Longest cantilever arm at z>=2: {best[0]} modules; reached in {len(path)-1} moves.\n",
           "Start (# module, = garment):\n```\n" + draw(start) + "\n```\nBest:\n```\n" + draw(best[1]) + "\n```\n"]
    txt = "\n".join(out)
    os.makedirs("results", exist_ok=True)
    open("results/audit_branch.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
