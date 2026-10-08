"""Regression / independent-check tests. Run: python3 -m pytest -q tests"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sims"))
import numpy as np
import face_motor as fm
import power_network as pn
import structure as st
import isl

def test_face_motor_fd_matches_analytic():
    lam, g, V = 3e-6, 1e-6, 50.0
    k = 2 * math.pi / lam
    nx, nz = 160, 61
    x = np.arange(nx) * lam / nx
    s = lam / 4
    tf, pf = fm.fd_solve(V*np.cos(k*x), V*np.cos(k*(x-s)), lam, g, nx, nz)
    assert abs(tf - fm.tau(V, V, k, g, s)) / fm.tau(V, V, k, g, s) < 0.02
    assert abs(pf - fm.pnorm(V, V, k, g, s)) / abs(fm.pnorm(V, V, k, g, s)) < 0.03

def test_face_motor_small_kg_limit():
    # kg -> 0, aligned like potentials, V1=V2: p -> eps0 V^2 ... cancel; check tau/p bound tau/p <= sinh(kg)
    for kg in (0.05, 0.5, 2.0):
        k, g = kg / 1e-6, 1e-6
        r = fm.tau(1, 1, k, g, math.pi/2/k) / fm.pnorm(1, 1, k, g, math.pi/2/k)
        assert r <= math.sinh(kg) + 1e-12

def test_kg_opt():
    x = fm.kg_opt()
    assert abs(math.tanh(x) - x / 2) < 1e-10 and 1.9 < x < 1.93

def test_chain_drop():
    for h in (5, 50):
        u = pn.solve([(0, 0, z) for z in range(h)], {(0, 0, 0)}, 7.0, 1e-6)
        assert math.isclose(u[(0, 0, h-1)], pn.chain_formula(h, 7.0, 1e-6), rel_tol=1e-9)

def test_structure_scaling():
    assert math.isclose(st.chain_reach(1e4, 4e-4) / st.chain_reach(1e4, 1e-4), 2.0)

def test_isl_extrusion_and_rules():
    w, log, h = isl.extrusion_demo(F=12, B=16)
    assert all(ok for _, ok, _ in log) and h == 12
    # a module touching the garment can never lift off
    w2 = isl.World({(0, 0), (1, 0), (1, 1)})
    ok, why = w2.try_move((0, 0), "z", +1, apply=False)
    assert not ok
