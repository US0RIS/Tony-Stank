"""SESSION 3 / PHASE 3. Executable transformation between two unrelated shapes, with the
actuator for every move modelled explicitly, power continuity checked, and moves packed
into collision-free parallel steps.

Shapes (2D slice, N = 8, same window as generality.py):
  TOWER-ARM : column of 3 on the garment with a 2-module cantilever arm at its top
  ARCH      : arch enclosing a cavity
Architectures compared under the same assumptions (L, humidity, Br, mu):
  MPL  neighbour-driven electropermanent pivoting lattice (passive mover, push+pull pivots)
  SISL sliding lattice with electrostatic face drive (+ bolts); convex transitions need a
       second actuator
  ISL / FC: reachability only (ISL cannot reach these shapes from this start; FC only if
       the shapes are single-path traceable from its anchor)
NUMERICAL SIMULATION (planning + per-move physics from mag_pivot.py, face_motor results).
Run: python3 sims/s3/cycle_compare.py -> results/s3_cycle_compare.md
"""
import math, os, sys
from collections import deque
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "audit"))
import generality as g
import mag_pivot as mp
from isl3d import sliding_successors

TOWER_ARM = frozenset({(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3)})
ARCH = frozenset({(0, 0), (2, 0), (3, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)})

def bfs_path(a, b, succ):
    par = {a: None}; dq = deque([a])
    while dq:
        s = dq.popleft()
        if s == b: break
        for t in succ(s):
            if t not in par: par[t] = s; dq.append(t)
    if b not in par: return None
    path = [b]
    while par[path[-1]] is not None: path.append(par[path[-1]])
    return path[::-1]

def classify_pivot(s, t):
    """Identify the pivot move s->t: mover A, target B, corner, angle, S/D supports."""
    A = next(iter(s - t)); B = next(iter(t - s)); rest = s - {A}
    best = None
    for c in ((A[0], A[1]), (A[0] + 1, A[1]), (A[0], A[1] + 1), (A[0] + 1, A[1] + 1)):
        for ang in (math.pi / 2, -math.pi / 2, math.pi, -math.pi):
            b = g.rot_pt((A[0] + 0.5, A[1] + 0.5), c, ang)
            if (round(b[0] - 0.5), round(b[1] - 0.5)) != B: continue
            sw = g.swept_cells(A, c, ang) - {A, B}
            if any(g.occ(q, rest) for q in sw): continue
            cand = [q for q in list(rest) + [(x, -1) for x in range(g.XMIN - 1, g.XMAX + 2)] if g.touches(q, c)]
            D = [q for q in cand if g.edge_adj(q, B)]; S = [q for q in cand if g.edge_adj(q, A)]
            if D and S:
                best = dict(A=A, B=B, c=c, ang=ang, S=S, D=D, sweep=sw)
                break
        if best: break
    return best

def pivot_physics(L, factor3d=0.5):
    req, _, _ = mp.requirements(L)
    m90 = min(r[1] for r in mp.pivot_profile(True, True, L=L)) * factor3d / req
    m180 = min(r[1] for r in mp.convex_profile(L=L, push=True)) * factor3d / req
    h90 = max(0, -min(r[2] for r in mp.pivot_profile(True, True, L=L)))
    h180 = max(0, -min(r[2] for r in mp.convex_profile(L=L, push=True)))
    # dynamics: rotation time under mean torque with rotational inertia (air damping neglected: upper speed bound)
    I = 2330 * L**3 * L**2 / 6
    Tmean = sum(r[1] for r in mp.pivot_profile(True, True, L=L)) / 45 * factor3d
    t90 = math.sqrt(2 * I * (math.pi / 2) / Tmean)
    E_land = Tmean * math.pi / 2
    pole = min(L / 2, 50e-6)
    n_poles = max(1.0, (L / (2 * pole)) ** 2)          # poles per face (2x2 for L <= 100 um is folded into 'pole' size)
    E_sw = mp_switch_energy(pole) * n_poles
    return dict(m90=m90, m180=m180, h90=h90, h180=h180, t90=t90, E_land=E_land, E_sw=E_sw)

def mp_switch_energy(pole, Hc=20e3):
    sys.path.insert(0, os.path.dirname(__file__))
    import magnetic
    return magnetic.epm_switch(pole, Hc)[1]

def schedule(path, footprint):
    """Greedy list scheduling of a sequential plan into parallel steps: a move joins the
    current step if its footprint is disjoint from every move already in the step and
    from every footprint of moves it must follow (all earlier moves in the step)."""
    steps = []; cur = []; cur_fp = set()
    for i in range(len(path) - 1):
        fp = footprint(path[i], path[i + 1])
        if cur and not (fp & cur_fp):
            cur.append(i); cur_fp |= fp
        else:
            if cur: steps.append(cur)
            cur = [i]; cur_fp = set(fp)
    if cur: steps.append(cur)
    return steps

def main():
    R = ["# Session 3 — executable transformation TOWER-ARM <-> ARCH (NUMERICAL SIMULATION)\n"]
    for nm, sh in (("TOWER-ARM", TOWER_ARM), ("ARCH", ARCH)):
        R.append(f"- {nm}: cells {sorted(sh)}; metrics (maxh, branch, cavity, cantilever) = {g.metrics(sh)}")
    # ---------- MPL ----------
    piv = lambda s: g.pivot_successors(s, True)
    fwd = bfs_path(TOWER_ARM, ARCH, piv); back = bfs_path(ARCH, TOWER_ARM, piv)
    R.append(f"\n## MPL (strict push+pull pivots)\n- forward plan: {len(fwd)-1 if fwd else 'NONE'} moves; reverse plan: {len(back)-1 if back else 'NONE'} moves")
    if fwd:
        moves = [classify_pivot(fwd[i], fwd[i + 1]) for i in range(len(fwd) - 1)]
        n90 = sum(1 for m in moves if abs(abs(m["ang"]) - math.pi / 2) < 1e-6); n180 = len(moves) - n90
        R.append(f"- move types: {n90} x 90 deg, {n180} x 180 deg; every move has source and destination supports (strict rule).")
        # power continuity: rest connected (guaranteed by rule) -> S and D powered; mover passive
        ok_power = all(g.connected(fwd[i] - {moves[i]["A"]}) for i in range(len(moves)))
        R.append(f"- power: during every move all non-moving modules (incl. both actuating neighbours) stay connected to the garment: {ok_power}; "
                 "the mover needs no power in transit (passive magnets, nonvolatile state).")
        fp = lambda s, t: (lambda m: {m["A"], m["B"]} | set(m["sweep"]) | set(q for q in m["S"] + m["D"] if q[1] >= 0))(classify_pivot(s, t))
        st = schedule(fwd, fp)
        R.append(f"- parallel schedule: {len(fwd)-1} sequential moves -> {len(st)} collision-free parallel steps")
        R.append("\n| L | 90 deg torque margin (3D-derated) | 180 deg margin | hinge load 90/180 | inertial time per pivot | landing energy | EPM energy (4 face switches/move, all poles) | plan energy |\n|---|---|---|---|---|---|---|---|")
        for L in (1e-3, 300e-6, 100e-6, 30e-6):
            ph = pivot_physics(L)
            Emove = 4 * ph["E_sw"]
            R.append(f"| {L*1e6:.0f} um | {ph['m90']:.1f} | {ph['m180']:.1f} | {ph['h90']*1e6:.0f}/{ph['h180']*1e6:.0f} uN | {ph['t90']*1e6:.0f} us | {ph['E_land']*1e9:.3g} nJ | {Emove*1e9:.3g} nJ | {Emove*(len(fwd)-1)*1e9:.3g} nJ |")
    # ---------- SISL ----------
    to3 = lambda st: {(c[0], 0, c[1]) for c in st}; from3 = lambda st: frozenset((c[0], c[2]) for c in st)
    sl = lambda s: {from3(t) for t in sliding_successors(to3(s), dims=2) if all(g.inwin(c) for c in from3(t))}
    p2 = bfs_path(TOWER_ARM, ARCH, sl)
    R.append(f"\n## SISL (sliding, electrostatic face drive)\n- forward plan: {len(p2)-1 if p2 else 'NONE'} moves")
    if p2:
        conv = 0
        for i in range(len(p2) - 1):
            A = next(iter(p2[i] - p2[i + 1])); B = next(iter(p2[i + 1] - p2[i]))
            if abs(A[0] - B[0]) + abs(A[1] - B[1]) == 2: conv += 1
        R.append(f"- {len(p2)-1-conv} straight slides (face drive), {conv} convex transitions (face drive cannot execute; needs a pivot actuator or neighbour transport, and breaks face contact -> power gap)")
        R.append("- per straight slide at L = 100 um: thrust margin ~20 sealed (AUDIT 1); with one 1 um particle in a 100 nm-gap design thrust x4e-8; "
                 "sliding distance per slide = L; sliding-contact life ~1e5 cycles in air (polysilicon sidewalls, SNIPPET) -> ~1e5 moves per interface.")
    # ---------- ISL / FC ----------
    isl = lambda s: {from3(t) for t in g.World3(to3(s), dims=2).successors() if all(g.inwin(c) for c in from3(t))}
    p3 = bfs_path(TOWER_ARM, ARCH, isl)
    R.append(f"\n## ISL: path TOWER-ARM -> ARCH: {'found' if p3 else 'NONE (bounded search exhausted)'}")
    # FC: is each shape traceable as a self-avoiding path from an anchor on the garment?
    def traceable(shape):
        for a in shape:
            if a[1] != 0: continue
            stack = [(a, (a,))]
            while stack:
                cur, path = stack.pop()
                if len(path) == len(shape): return True
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (cur[0] + d[0], cur[1] + d[1])
                    if q in shape and q not in path: stack.append((q, path + (q,)))
        return False
    R.append(f"## FC: TOWER-ARM single-path traceable: {traceable(TOWER_ARM)}; ARCH traceable: {traceable(ARCH)} "
             "(a chain can only form shapes that admit a Hamiltonian path from its anchor)")
    # FC shape-space fraction among single-component shapes reachable by MPL (N = 8)
    allpv = set()
    dq = deque([TOWER_ARM]); allpv.add(TOWER_ARM)
    while dq:
        st = dq.popleft()
        for t in piv(st):
            if t not in allpv: allpv.add(t); dq.append(t)
    def one_component(sh):
        sh = set(sh); a = next(iter(sh)); seen = {a}; q = [a]
        while q:
            c = q.pop()
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + d[0], c[1] + d[1])
                if n in sh and n not in seen: seen.add(n); q.append(n)
        return len(seen) == len(sh)
    single = [sh for sh in allpv if one_component(sh)]
    tr = sum(1 for sh in single if traceable(sh))
    R.append(f"## Shape-space fraction (N = 8): of {len(single)} single-component shapes reachable by MPL, {tr} ({100*tr/len(single):.0f} %) are formable by an anchored folding chain.")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s3_cycle_compare.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
