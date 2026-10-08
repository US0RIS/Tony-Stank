"""Tests pinning session-3 conclusions. Run: python3 -m pytest -q tests"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sims", "s3"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sims", "audit"))
import magnetic as mg
import mag_pivot as mp
import generality as g

def test_magnetic_charge_model_contact_limit():
    p_num, p_ana = mp.check_pressure()
    assert 0.85 < abs(p_num) / p_ana < 1.05 and p_num < 0

def test_coil_vs_pm_ratio_small():
    t_c = 5e-6
    J = min(math.sqrt(2 * 2e5 / (mg.RHO_CU * t_c)), 1e10)
    assert mg.MU0 * J * t_c / 0.12 < 0.15

def test_epm_switch_heating_scaling():
    _, E1, dT1 = mg.epm_switch(50e-6, 20e3)
    _, E2, dT2 = mg.epm_switch(5e-6, 20e3)
    assert dT1 < 5 and dT2 > 100          # 100 um modules OK, 10 um modules overheat

def test_reluctance_stepper_friction_locked():
    lam = 20e-6
    t, p, _ = mg.toothed_fd(lam, 0.05 * lam, lam / 2, 0.4, lam / 8, nx=80, dz=0.25e-6)
    assert abs(t) / p < 0.2

def test_pivot_margin_scaling():
    req100, _, _ = mp.requirements(100e-6); req10, _, _ = mp.requirements(10e-6)
    m100 = min(r[1] for r in mp.pivot_profile(True, True, L=100e-6, n=20)) / req100
    m10 = min(r[1] for r in mp.pivot_profile(True, True, L=10e-6, n=20)) / req10
    assert m100 > 3 and m10 < 1

def test_chain_shapes_need_hamiltonian_path():
    # a plus-shaped pentomino (no Hamiltonian path) cannot be a chain
    plus = {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}
    def has_path(sh):
        for a in sh:
            st = [(a, (a,))]
            while st:
                c, p = st.pop()
                if len(p) == len(sh): return True
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (c[0] + d[0], c[1] + d[1])
                    if q in sh and q not in p: st.append((q, p + (q,)))
        return False
    assert not has_path(plus)

def test_pivot_rule_requires_supports():
    # a lone module on the garment can roll along it (garment supplies S and D)
    succ = g.pivot_successors(frozenset({(0, 0), (1, 0), (1, 1)}), True)
    assert len(succ) > 0
