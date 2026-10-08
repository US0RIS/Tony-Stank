"""Tests pinning the audit conclusions. Run: python3 -m pytest -q tests"""
import math, os, random, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sims"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sims", "audit"))
import face_motor as fm
import face_motor_realistic as fr
import power_audit as pa
from isl3d import World3

def test_realistic_stack_below_ideal():
    t, p, _, _ = fr.solve_stack(lam=3.3e-6, g=1e-6, t_c=0.1e-6, eps_c=3.9, t_ox=1e-6, eps_ox=3.9, V=50, theta=math.pi/2, nx=132, dz=0.05e-6)
    ideal = fm.tau(50, 50, 2*math.pi/3.3e-6, 1e-6, 3.3e-6/4)
    assert 0.3 < abs(t) / ideal < 0.6

def test_narrow_footprint_breaks_height_only_claim():
    tower = list(itertools.product(range(6), range(6), range(15)))
    I, R = 1e-6, 10.0
    full = {c: R for c in tower if c[2] == 0}
    corner = {(0, 0, 0): R}
    u1, _ = pa.solve(tower, {c: I for c in tower}, pa.lattice_edges(tower, R), full)
    u2, _ = pa.solve(tower, {c: I for c in tower}, pa.lattice_edges(tower, R), corner)
    assert math.isclose(max(u1.values()), pa.formula(15, R, I), rel_tol=1e-9)
    assert max(u2.values()) > 2 * max(u1.values())

def test_isl_moves_reversible():
    rng = random.Random(0)
    W = World3({(x, 0, 0) for x in (-2, -1, 1, 2)} | {(x, 0, 1) for x in (1, 2, 3)} | {(1, 0, 2), (0, 0, 1), (0, 0, 2)}, dims=2)
    for _ in range(300):
        nxt = rng.choice(W.successors())
        assert frozenset(W.c) in set(World3(set(nxt), dims=2).successors())
        W = World3(set(nxt), dims=2)
