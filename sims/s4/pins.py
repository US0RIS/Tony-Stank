"""SESSION 4 / PHASE 6a. Pin/socket kinematics during a pivot and genderless pin-pattern compatibility.

(1) Kinematics (NUMERICAL, 2D section through the pin axis, perpendicular to the pivot axis):
    a frustum pin (base d_b, tip d_t, height h) anchored on the mover face at distance r from the pivot
    edge rotates out of a cylindrical socket (diameter d_s, depth h_s) in the stationary face. Report the
    worst interference between pin outline and socket walls as the mover rotates 0 -> 30 deg, and the
    minimum socket diameter / chamfer that gives zero interference.
(2) Pattern compatibility (MATHEMATICAL): faces meet with relative in-plane rotation phi in {0,90,180,270}.
    A pattern P of pins with sockets S = mirror(P) mates for every phi iff P is invariant under 90 deg rotation.
    Checks the single pin/socket layout (session-4 geometry) and a chiral pinwheel layout.
Run: python3 sims/s4/pins.py -> results/s4_pins.md
"""
import math, os
import numpy as np

def interference(r, d_b, d_t, h, d_s, h_s, chamfer=0.0, deg_max=40, n=400):
    """Mover face initially at y=0 (pin points down into the socket, y<0); pivot at x=0, y=0.
    Pin axis at x=r. Socket walls at x = r +- d_s/2 for y in [-h_s, 0] (chamfer widens the mouth linearly
    over its depth). Returns the max penetration (um) of pin outline into walls over the rotation."""
    worst = 0.0
    ys = np.linspace(0, -h, 40)
    left = np.stack([r - (d_b / 2 + (d_t - d_b) / 2 * (-ys / h)), ys], 1)
    right = np.stack([r + (d_b / 2 + (d_t - d_b) / 2 * (-ys / h)), ys], 1)
    pts = np.vstack([left, right])
    for deg in np.linspace(0, deg_max, n):
        a = math.radians(deg)                       # mover rotates about origin, lifting the face (counter-clockwise for x>0)
        R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
        P = pts @ R.T
        inside = P[:, 1] < 0                         # below the stationary face
        if not inside.any(): break
        Q = P[inside]
        depth = -Q[:, 1]
        half = d_s / 2 + chamfer * np.clip(1 - depth / h_s, 0, 1)
        pen = np.maximum(0, np.abs(Q[:, 0] - r) - half)
        pen = np.where(depth <= h_s, pen, np.maximum(pen, 0))
        worst = max(worst, pen.max())
    return worst

def rot(p, k): x, y = p; return [(x, y), (-y, x), (-x, -y), (y, -x)][k % 4]

def compatible(P):
    """Facing face sees partner pattern mirrored (x -> -x) and rotated by phi; sockets S = mirror(P)."""
    S = {(-x, y) for (x, y) in P}
    res = {}
    for k in range(4):
        partner_pins = {(-rot(p, k)[0], rot(p, k)[1]) for p in P}
        res[90 * k] = partner_pins == S
    return res

def main():
    R = ["# Session 4 — pins: kinematics and orientation compatibility\n"]
    R.append("## 1. Withdrawal/insertion kinematics (NUMERICAL)\nPin: base 14 um, tip 6 um, height 8 um; socket depth 9 um. r = distance of pin axis from the pivot edge.\n")
    R.append("| r (um) | socket 16 um, no chamfer: worst interference (um) | socket diameter needed (no chamfer) | chamfer needed with 16 um socket |\n|---|---|---|---|")
    for r in (20.5, 29.5, 50.0, 70.5, 79.5):
        w = interference(r, 14, 6, 8, 16, 9)
        ds = 16.0
        while interference(r, 14, 6, 8, ds, 9) > 1e-3 and ds < 60: ds += 0.5
        ch = 0.0
        while interference(r, 14, 6, 8, 16, 9, chamfer=ch) > 1e-3 and ch < 30: ch += 0.25
        R.append(f"| {r} | {w:.2f} | {ds:.1f} | {ch:.2f} |")
    R.append("\nInterpretation: with a 14 -> 6 um taper, socket clearance (1 um at the mouth, 5 um at the tip) exceeds the arc's lateral sweep "
             "(<= ~1.5 um at the tip for r = 20.5 um), so withdrawal and insertion are collision-free for every pivot edge. The taper limits the pin's "
             "shear engagement to the tapered flank (see MECHANICAL_CYCLE.md for cam-out).\n")
    R.append("## 2. Orientation compatibility of pin patterns (MATHEMATICAL)\n")
    single = {(0.0, -29.5)}
    R.append(f"- Session-4 single pin + single socket layout: mates for relative rotations {[k for k, v in compatible(single).items() if v]} only. "
             "After pivots change a module's orientation, other pairings put pin against pin -> blocked attachment or broken pins.")
    a, b = 29.0, 18.0
    pin_w = {(a, b), (-b, a), (-a, -b), (b, -a)}
    R.append(f"- Chiral pinwheel (4 pins at (+-{a},+-{b}) rotated set, sockets = mirror): mates for {[k for k, v in compatible(pin_w).items() if v]}.")
    sock = {(-x, y) for (x, y) in pin_w}
    allp = list(pin_w) + list(sock)
    dmin = min(math.dist(p, q) for i, p in enumerate(allp) for q in allp[i + 1:])
    R.append(f"  Minimum spacing between the 8 sites: {dmin:.1f} um (needs >= socket size). Sites lie at |u|,|v| in {{{b},{a}}} um from the face centre: "
             f"they fall inside the coil envelopes (|v| <= 22 um) for the 4 sites with |v| = {b} um -> the 100 um face layout must be re-partitioned (coil length or bar width reduced). ")
    R.append("\n## 3. Can a pinwheel coexist with the coils at L = 100 um? (search, MATHEMATICAL)\n")
    R.append("Sites must lie outside the coil band |v| <= c_half (+1 um clearance), inside the window |u|,|v| <= 37 - site/2, and be >= site + 1 um apart (site = 10 um socket).\n")
    R.append("| coil band half-width c_half (um) | feasible pinwheel (a, b) found | resulting bar width each (um) | magnet cross-section vs session-4 layout |\n|---|---|---|---|")
    for c_half in (22.0, 20.0, 18.0, 16.0, 14.0):
        found = None
        for a in np.arange(5, 32.01, 0.5):
            for b in np.arange(-32, 32.01, 0.5):
                P = {(a, b), (-b, a), (-a, -b), (b, -a)}
                S = {(-x, y) for (x, y) in P}
                pts = list(P) + list(S)
                if len(set(pts)) < 8: continue
                ok = all(abs(v) >= c_half + 1 + 5 and abs(u) <= 32 and abs(v) <= 32 for (u, v) in pts)
                ok = ok and min(math.dist(p, q) for i, p in enumerate(pts) for q in pts[i + 1:]) >= 11
                if ok: found = (a, b); break
            if found: break
        bar_w = max(0.0, (2 * c_half - 1) / 2 - 8)
        R.append(f"| {c_half} | {found if found else 'none'} | {bar_w:.1f} | {bar_w/12:.2f} |")
    R.append("\nA pinwheel needs both coordinates of every site outside the coil band, which is impossible unless the band shrinks; any feasible band "
             "reduces bar width (and switchable magnet volume) as listed. A 90-deg-symmetric pattern can also be placed inside the coil band only by "
             "interrupting the bars, which cuts their flux path.\n")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s4_pins.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
