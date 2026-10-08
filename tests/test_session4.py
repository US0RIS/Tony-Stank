"""Tests pinning session-4 conclusions. Run: python3 -m pytest -q tests"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sims", "s4"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sims", "s3"))
import module_geometry as mg
import demag_contacts as dc
import switching as sw
import pins
import magfd as fd

def test_geometry_has_no_interference():
    for L in (100, 300, 1000):
        assert mg.check(mg.build(L)) == []

def test_aharoni_cube_and_bar():
    assert abs(dc.aharoni_Nz(1, 1, 1) - 1 / 3) < 1e-9
    N = dc.aharoni_Nz(6, 2, 29)            # 58 x 12 x 4 um bar, length axis
    assert 0.045 < N < 0.055               # independent review R1: 0.044-0.050

def test_pinwheel_mates_all_rotations_single_pin_does_not():
    assert all(pins.compatible({(29.0, 18.0), (-18.0, 29.0), (-29.0, -18.0), (18.0, -29.0)}).values())
    assert not all(pins.compatible({(0.0, -29.5)}).values())

def test_coil_field_matches_independent_review():
    d = sw.design_coil(100, 3.0, 3.0, 1.0, 1.5, "CoP (plated)")
    assert 2.9e5 < d["Hctr1"] < 3.4e5      # R2: 3.07e5 (edge turns) / 3.24e5 (true pitch)
    assert 0.7e5 < d["Hmin1"] < 0.95e5     # R2: 0.81e5 with true pitch

def test_100um_pivot_fails_by_large_factor():
    d = json.load(open(os.path.join(os.path.dirname(__file__), "..", "results", "s4_pivot_real_100.json")))
    worst = min(v[0] for v in d["summary"].values() if True)
    assert worst < 0.05                    # session-3 claimed 4.5 / 2.0

def test_fd_force_sign_translation():
    # two magnets in line attract (negative force on the upper one along +y)
    L = 40e-6; h = 1e-6
    import numpy as np
    xs = np.arange(-40e-6, 80e-6 + h / 2, h); ys = xs.copy()
    a = fd.Part(10e-6, 30e-6, 0, 10e-6, "mag", (0.0, 5e5), 1.0)
    b = fd.Part(10e-6, 30e-6, 13e-6, 23e-6, "mag", (0.0, 5e5), 1.0)
    mu, Mx, My = fd.rasterize([(a, (0, 0), 0, (0, 0)), (b, (0, 0), 0, (0, 0))], xs, ys)
    psi = fd.solve(xs, ys, mu, Mx, My); Hx, Hy = fd.fields(psi, h)
    poly = [(8e-6, 11.5e-6), (32e-6, 11.5e-6), (32e-6, 25e-6), (8e-6, 25e-6)]
    Fx, Fy, T = fd.stress_force(Hx, Hy, xs, ys, poly, (0, 0))
    assert Fy < 0
