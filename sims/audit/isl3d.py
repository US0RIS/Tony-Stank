"""3D generalisation of the ISL rule checker (rules R1-R5 of sims/isl.py) plus a
sliding-cube reference model, used by AUDIT 3 and the generalisation study."""
from collections import deque

AXES = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}
NB6 = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

def add(p, d, k=1): return (p[0]+k*d[0], p[1]+k*d[1], p[2]+k*d[2])

class World3:
    """ISL in 3D. Garment = fixed plane z=-1 (interlocked). `ports`: optional set of
    garment cells (x,y) that are holes (not occupied) — unused by default."""
    def __init__(self, cells, dims=3):
        self.c = set(cells); self.dims = dims
    def occ(self, p): return p in self.c or p[2] == -1
    def run(self, p, d):
        lo = p
        while add(lo, d, -1) in self.c: lo = add(lo, d, -1)
        seg = [lo]
        while add(seg[-1], d) in self.c: seg.append(add(seg[-1], d))
        return seg
    def lateral(self, seg, d):
        s = set(seg)
        for p in seg:
            for e in NB6:
                if e == d or e == (-d[0], -d[1], -d[2]): continue
                if self.dims == 2 and e[1] != 0: continue
                q = add(p, e)
                if self.occ(q) and q not in s: return True
        return False
    def connected(self, cells=None):
        cells = self.c if cells is None else cells
        start = [p for p in cells if p[2] == 0]
        seen = set(start); dq = deque(start)
        while dq:
            p = dq.popleft()
            for e in NB6:
                q = add(p, e)
                if q in cells and q not in seen: seen.add(q); dq.append(q)
        return len(seen) == len(cells)
    def move(self, p, axis, sgn, apply=True):
        d = tuple(sgn * v for v in AXES[axis])
        if p not in self.c: return False, "empty", None
        seg = self.run(p, d)
        lead, trail = seg[-1], seg[0]
        if self.occ(add(trail, d, -1)): return False, "R2", None
        if self.occ(add(lead, d)): return False, "blocked", None
        if self.occ(add(lead, d, 2)): return False, "R3", None
        if not self.lateral(seg, d): return False, "R5", None
        new = (self.c - set(seg)) | {add(q, d) for q in seg}
        w = World3(new, self.dims)
        if not w.lateral([add(q, d) for q in seg], d): return False, "R5", None
        if not w.connected(): return False, "R4", None
        if apply: self.c = new
        return True, "ok", frozenset(new)
    def successors(self):
        out, done = [], set()
        axes = ("x", "z") if self.dims == 2 else ("x", "y", "z")
        for p in self.c:
            for a in axes:
                d = AXES[a]
                key = (min(self.run(p, d)), a)
                if key in done: continue
                done.add(key)
                for s in (1, -1):
                    ok, _, st = self.move(p, a, s, apply=False)
                    if ok: out.append(st)
        return out

def sliding_successors(cells, dims=2):
    """Sliding-cube model: a single module slides to an adjacent empty cell along a
    neighbour (both side cells occupied) or makes a convex transition around a
    neighbour's edge. Garment plane z=-1 counts as a fixed neighbour. Connectivity to
    the garment (z=0 contact) must hold after the move."""
    occ = lambda p, S: p in S or p[2] == -1
    dirs = [d for d in NB6 if not (dims == 2 and d[1] != 0)]
    out = set()
    for p in cells:
        rest = cells - {p}
        for d in dirs:
            for u in dirs:
                if u == d or u == (-d[0], -d[1], -d[2]) or u[0]*d[0]+u[1]*d[1]+u[2]*d[2] != 0: continue
                t = add(p, d)
                # straight slide along a neighbour
                if not occ(t, rest) and occ(add(p, u), rest) and occ(add(t, u), rest):
                    new = rest | {t}
                    if t[2] >= 0 and World3(new).connected(): out.add(frozenset(new))
                # convex transition around the edge of the neighbour at p+u
                c = add(t, u)
                if occ(add(p, u), rest) and not occ(t, rest) and not occ(c, rest) and not occ(add(t, u, 0), rest):
                    # p -> t -> c rounding the corner of neighbour at p+u... (c must touch something)
                    pass
                if occ(add(p, d), rest) and not occ(add(p, u), rest) and not occ(add(add(p, u), d), rest):
                    c2 = add(add(p, u), d)
                    new = rest | {c2}
                    if c2[2] >= 0 and World3(new).connected(): out.add(frozenset(new))
    return list(out)

def bfs(start, succ, limit=2_000_000, window=None):
    start = frozenset(start)
    seen = {start}; dq = deque([start])
    while dq and len(seen) < limit:
        s = dq.popleft()
        for t in succ(s):
            if window and not all(window(p) for p in t): continue
            if t not in seen: seen.add(t); dq.append(t)
    return seen
