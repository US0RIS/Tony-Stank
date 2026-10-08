"""S6. Interlocked Sliding Lattice (ISL): kinematic rule checker + extrusion protocol.

HYPOTHETICAL architecture under test: every face pair of adjacent modules is
mechanically interlocked by undercut rails (T-slot / dovetail grid). Consequences
encoded as rules:
  R1  A move translates a maximal straight run ('segment') of modules by one cell
      along its own axis.  (A sub-run cannot move: it would separate head-on from
      the rest of the run.)
  R2  No head-on separation: the cell behind the trailing end must be empty or
      the move is illegal (this is automatic for a maximal run, except the garment).
  R3  No head-on arrival: the cell two ahead of the leading end must be empty
      (an undercut key cannot enter a slot along the face normal).
  R4  Connectivity: after the move every module is face-connected to the garment
      (z = -1 plane, fixed and interlocked like a module).  This is also the
      power/data path.
  R5  Traction: the moving segment must have >= 1 lateral (side) contact before
      and after the move (the face motor pushes against a neighbour).
2D vertical slice (x, z) for tractability.

Outputs results/isl.md. Run: python3 sims/isl.py
"""
import os, random
from collections import deque

AX = {"x": (1, 0), "z": (0, 1)}

class World:
    def __init__(self, cells):
        self.c = set(cells)

    def occ(self, p):
        return p in self.c or p[1] == -1          # garment plane is fixed & occupied

    def run(self, p, axis):
        dx, dz = AX[axis]
        lo = p
        while (lo[0]-dx, lo[1]-dz) in self.c:
            lo = (lo[0]-dx, lo[1]-dz)
        hi = p
        while (hi[0]+dx, hi[1]+dz) in self.c:
            hi = (hi[0]+dx, hi[1]+dz)
        seg, q = [], lo
        while True:
            seg.append(q)
            if q == hi: break
            q = (q[0]+dx, q[1]+dz)
        return seg

    def lateral(self, seg, axis):
        dx, dz = AX[axis]
        ox, oz = dz, dx                            # perpendicular axis in 2D
        s = set(seg)
        for p in seg:
            for sgn in (1, -1):
                q = (p[0]+sgn*ox, p[1]+sgn*oz)
                if self.occ(q) and q not in s:
                    return True
        return False

    def connected(self):
        seen, dq = set(), deque(p for p in self.c if p[1] == 0)
        seen.update(dq)
        while dq:
            p = dq.popleft()
            for d in ((1,0),(-1,0),(0,1),(0,-1)):
                q = (p[0]+d[0], p[1]+d[1])
                if q in self.c and q not in seen:
                    seen.add(q); dq.append(q)
        return len(seen) == len(self.c)

    def try_move(self, p, axis, sgn, apply=True):
        """Return (ok, reason). Moves the maximal run containing p."""
        if p not in self.c: return False, "empty"
        dx, dz = AX[axis]; dx, dz = dx*sgn, dz*sgn
        seg = self.run(p, axis)
        lead = max(seg, key=lambda q: q[0]*dx + q[1]*dz)
        trail = min(seg, key=lambda q: q[0]*dx + q[1]*dz)
        if self.occ((trail[0]-dx, trail[1]-dz)):
            return False, "R2 head-on separation (garment)"
        if self.occ((lead[0]+dx, lead[1]+dz)):
            return False, "blocked"
        if self.occ((lead[0]+2*dx, lead[1]+2*dz)):
            return False, "R3 head-on arrival"
        if not self.lateral(seg, axis):
            return False, "R5 no traction before"
        new = (self.c - set(seg)) | {(q[0]+dx, q[1]+dz) for q in seg}
        w = World(new)
        if not w.lateral([(q[0]+dx, q[1]+dz) for q in seg], axis):
            return False, "R5 no traction after"
        if not w.connected():
            return False, "R4 disconnects"
        if apply: self.c = new
        return True, f"moved {len(seg)}"

def extrusion_demo(F=30, B=40):
    """Grow a tower at x=0 from a feeder row at z=1, x=1..F, on base row z=0.
    Port: (0,0) empty; left sleeve absent at (-1,1) (required by R3);
    right sleeve module at (1,2) rides on the feeder row."""
    cells = {(x, 0) for x in range(-B, B+1) if x != 0}
    cells |= {(x, 1) for x in range(1, F+1)}
    cells |= {(1, 2)}                    # sleeve (initially sits on feeder head)
    cells |= {(0, 1), (0, 2)}            # seed column of 2 at the port
    cells.discard((1, 1)); cells |= {(1, 1)}
    # the feeder head is at x=1 below the sleeve; the seed column occupies x=0
    w = World(cells)
    assert w.connected()
    log, n0 = [], len(w.c)
    for cyc in range(F - 2):
        top_h = max(z for (x, z) in w.c if x == 0)
        ok, why = w.try_move((0, 1), "z", +1)
        log.append(("lift", ok, why))
        if not ok: break
        ok, why = w.try_move((2, 1), "x", -1)      # shift whole feeder run left
        log.append(("feed", ok, why))
        if not ok: break
        # sleeve must stay on the new feeder head (it does: feeder slides under it)
    h = max(z for (x, z) in w.c if x == 0)
    assert len(w.c) == n0
    return w, log, h

def invariant_test(n_trials=20000, seed=1):
    """Random legal moves from a random-ish configuration; check that the set of
    garment-contact modules (z=0) is invariant in count, and connectivity holds."""
    rnd = random.Random(seed)
    cells = {(x, 0) for x in range(-6, 7)} | {(x, 1) for x in range(-4, 5)} | {(x, 2) for x in range(-2, 3)} | {(0,3),(1,3)}
    cells -= {(0, 0), (3, 1)}
    w = World(cells)
    assert w.connected()
    z0 = sum(1 for p in w.c if p[1] == 0)
    moves, reasons = 0, {}
    maxz = max(p[1] for p in w.c)
    for _ in range(n_trials):
        p = rnd.choice(sorted(w.c)); ax = rnd.choice("xz"); s = rnd.choice((1, -1))
        ok, why = w.try_move(p, ax, s)
        reasons[why.split()[0] if ok else why] = reasons.get(why.split()[0] if ok else why, 0) + 1
        if ok:
            moves += 1
            assert w.connected()
            assert sum(1 for q in w.c if q[1] == 0) == z0
            maxz = max(maxz, max(q[1] for q in w.c))
    return moves, reasons, z0, maxz

def main():
    out = ["# S6 Interlocked Sliding Lattice: kinematic simulation (SIMULATED)\n"]
    w, log, h = extrusion_demo()
    nlift = sum(1 for l in log if l[0] == "lift" and l[1])
    nfeed = sum(1 for l in log if l[0] == "feed" and l[1])
    out.append("## Extrusion through a port (2D slice)\n")
    out.append(f"- cycles attempted: {len(log)//2}; legal lifts {nlift}, legal feeds {nfeed}; final tower height {h} modules (z=1..{h}) "
               f"(from seed 2); every intermediate state connected to garment (R4 checked each move).")
    fails = [l for l in log if not l[1]]
    out.append(f"- first failure: {fails[0] if fails else 'none'}")
    # rule necessity: what breaks if left sleeve present
    cells = set(w.c)
    out.append("\n## Ablations (why each geometric feature is required)\n")
    for label, mod in [("left sleeve at (-1,1) present", lambda c: c | {(-1, 1)}),
                       ("right sleeve (1,2) absent", lambda c: c - {(1, 2)})]:
        F, B = 10, 15
        c = {(x, 0) for x in range(-B, B+1) if x != 0} | {(x, 1) for x in range(1, F+1)} | {(1, 2), (0, 1), (0, 2)}
        c = mod(c)
        ww = World(c)
        if not ww.connected():
            out.append(f"- {label}: initial state disconnected"); continue
        ok1, r1 = ww.try_move((0, 1), "z", +1)
        ok2, r2 = ww.try_move((2, 1), "x", -1) if ok1 else (False, "-")
        out.append(f"- {label}: lift -> {ok1} ({r1}); feed -> {ok2} ({r2})")
    moves, reasons, z0, maxz = invariant_test()
    out.append("\n## Random legal-move invariant test (20000 proposals)\n")
    out.append(f"- legal moves executed: {moves}; garment-contact count invariant held ({z0}); connectivity held; max height reached {maxz}")
    out.append(f"- outcome counts: {reasons}")
    txt = "\n".join(out) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/isl.md", "w").write(txt)
    print(txt)

if __name__ == "__main__":
    main()
