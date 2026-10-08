"""SESSION 4 / PHASE 3. Dimensioned 3D layout of a complete NEPL module (axis-aligned boxes),
interference checking, volume budget, and drawings (cross-sections + exploded view).

Every component occupies real space. Overlaps are errors unless the pair is listed in
INTEGRATED (process-integrated by design, e.g. a magnetic bar inside its own coil envelope).
Run: python3 sims/s4/module_geometry.py [L_um] -> results/s4_geometry_<L>.md, results/s4_cad/*.png, *.json
"""
import json, math, os, sys, itertools

def build(L=100.0):
    s = L / 100.0                       # all dims in um, scaled from the 100 um layout
    e = 13 * s                          # face window margin (edge-hinge band); skin depth below must be < e
    skin = 12 * s
    comps = []
    def add(name, kind, x0, x1, y0, y1, z0, z1, material):
        comps.append(dict(name=name, kind=kind, box=[x0, x1, y0, y1, z0, z1], material=material))
    # face frame: returns function mapping (u,v,d) box in face-local coords to module box
    faces = {
        "z-": lambda u0, u1, v0, v1, d0, d1: (u0, u1, v0, v1, d0, d1),
        "z+": lambda u0, u1, v0, v1, d0, d1: (u0, u1, v0, v1, L - d1, L - d0),
        "y-": lambda u0, u1, v0, v1, d0, d1: (u0, u1, d0, d1, v0, v1),
        "y+": lambda u0, u1, v0, v1, d0, d1: (u0, u1, L - d1, L - d0, v0, v1),
        "x-": lambda u0, u1, v0, v1, d0, d1: (d0, d1, u0, u1, v0, v1),
        "x+": lambda u0, u1, v0, v1, d0, d1: (L - d1, L - d0, u0, u1, v0, v1),
    }
    pp_w = 8 * s; gap_coil = 2 * s
    tw, tb, cover = 4 * s, 4 * s, 1 * s
    clr = 1 * s                                       # manufacturing clearance between unrelated parts
    pin_d = 14 * s; pin_h = 8 * s; sock_w = pin_d + 2 * s
    a, b = e, L - e
    # v-stack across the face window [a, b]: pin band | coil envelope 0 | coil envelope 1 | socket band
    avail = (b - a) - (pin_d + clr) - (sock_w + clr) - 2 * clr       # left for two coil envelopes
    bar_w = (avail / 2) - 2 * tw
    assert bar_w > 0, "no room for switchable bars"
    v_pin = a + 0.5 * clr
    v_c0 = v_pin + pin_d + clr
    v_c1 = v_c0 + bar_w + 2 * tw + clr
    v_sock = v_c1 + bar_w + 2 * tw + clr
    assert v_sock + sock_w <= b + 1e-9, "face stack does not fit"
    for f, T in faces.items():
        add(f"{f}:cover", "insulation", *T(a, b, a, b, 0, cover * 0.5), "SiO2")
        add(f"{f}:pole1", "pole", *T(a, a + pp_w, v_c0, v_c1 + bar_w + 2 * tw, cover, cover + 2 * tw + tb), "NiFe")
        add(f"{f}:pole2", "pole", *T(b - pp_w, b, v_c0, v_c1 + bar_w + 2 * tw, cover, cover + 2 * tw + tb), "NiFe")
        for k, v0 in enumerate((v_c0 + tw, v_c1 + tw)):
            add(f"{f}:bar{k}", "magnet", *T(a + pp_w, b - pp_w, v0, v0 + bar_w, cover + tw, cover + tw + tb), "CoP (semi-hard)")
            add(f"{f}:coil{k}", "coil", *T(a + pp_w + gap_coil, b - pp_w - gap_coil, v0 - tw, v0 + bar_w + tw, cover, cover + 2 * tw + tb), "Cu + polyimide")
        add(f"{f}:pin", "pin", *T(L / 2 - pin_d / 2, L / 2 + pin_d / 2, v_pin, v_pin + pin_d, -pin_h, 4 * s), "Si (DRIE)")
        add(f"{f}:socket", "socket", *T(L / 2 - sock_w / 2, L / 2 + sock_w / 2, v_sock, v_sock + sock_w, 0, pin_h + 1 * s), "void")
        for k, (u0, v0) in enumerate(((a + 1 * s, v_pin), (b - 9 * s, v_pin), (a + 1 * s, v_sock + 4 * s), (b - 9 * s, v_sock + 4 * s))):
            add(f"{f}:pad{k}", "pad", *T(u0, u0 + 8 * s, v0, v0 + 8 * s, 0, cover), "Au on Ti")
        add(f"{f}:via", "routing", *T(a + 1 * s, a + 7 * s, v_sock + 1 * s, v_sock + 3.5 * s, cover, skin), "Cu via bundle")
    GEOM = dict(bar_w=bar_w, bar_t=tb, bar_l=(b - pp_w) - (a + pp_w), coil_l=(b - pp_w - gap_coil) - (a + pp_w + gap_coil),
                tw=tw, pole_depth=(v_c1 + bar_w + 2 * tw) - v_c0, window=b - a, skin=skin)
    # edge hinge knuckles (12 edges), between corner blocks
    kn = 10 * s; cb = 12 * s
    for ax in range(3):
        for p in (0, 1):
            for q in (0, 1):
                lo = [0, 0, 0]; hi = [0, 0, 0]
                o = [i for i in range(3) if i != ax]
                lo[ax], hi[ax] = cb, L - cb
                lo[o[0]], hi[o[0]] = (0, kn) if p == 0 else (L - kn, L)
                lo[o[1]], hi[o[1]] = (0, kn) if q == 0 else (L - kn, L)
                add(f"edge{ax}{p}{q}:knuckle", "hinge", lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], "Si + edge contact (Au)")
    for cx, cy, cz in itertools.product((0, 1), repeat=3):
        x0 = 0 if cx == 0 else L - cb; y0 = 0 if cy == 0 else L - cb; z0 = 0 if cz == 0 else L - cb
        add(f"corner{cx}{cy}{cz}", "structure", x0, x0 + cb, y0, y0 + cb, z0, z0 + cb, "Si")
    # core: CMOS die stack + capacitor + routing
    c0, c1 = skin + 1 * s, L - skin - 1 * s
    add("core:cmos_die_1", "electronics", c0, c1, c0, c1, L / 2 - 8 * s, L / 2 - 1 * s, "CMOS (thinned)")
    add("core:cmos_die_2", "electronics", c0, c1, c0, c1, L / 2 + 1 * s, L / 2 + 8 * s, "CMOS (thinned)")
    add("core:trench_cap", "capacitor", c0, c1, c0, c1, c0, L / 2 - 10 * s, "deep-trench Si capacitor")
    add("core:routing", "routing", c0, c1, c0, c1, L / 2 + 10 * s, c1, "TSV / redistribution")
    build.GEOM = GEOM
    return comps

INTEGRATED = {("magnet", "coil"), ("insulation", "pin"), ("insulation", "socket"), ("insulation", "pad")}   # bar in its own coil; cover patterned around pin/socket/pads

def overlap(a, b, tol=1e-9):
    A, B = a["box"], b["box"]
    d = [min(A[2 * i + 1], B[2 * i + 1]) - max(A[2 * i], B[2 * i]) for i in range(3)]
    return all(x > tol for x in d), (d[0] * d[1] * d[2] if all(x > 0 for x in d) else 0.0)

def check(comps):
    bad = []
    for a, b in itertools.combinations(comps, 2):
        ok, vol = overlap(a, b)
        if not ok: continue
        pair = tuple(sorted((a["kind"], b["kind"])))
        same_face = a["name"].split(":")[0] == b["name"].split(":")[0]
        if pair in {tuple(sorted(p)) for p in INTEGRATED} and same_face:
            if pair != ("coil", "magnet") or a["name"][-1] == b["name"][-1]:
                continue
        bad.append((a["name"], b["name"], vol))
    return bad

def vol(c):
    B = c["box"]; return (B[1] - B[0]) * (B[3] - B[2]) * (B[5] - B[4])

def draw(comps, L, tag):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    colors = {"pole": "#7f7f7f", "magnet": "#d62728", "coil": "#ff7f0e", "pin": "#2ca02c", "socket": "#ffffff",
              "pad": "#bcbd22", "hinge": "#9467bd", "structure": "#c7c7c7", "electronics": "#1f77b4",
              "capacitor": "#17becf", "routing": "#8c564b", "insulation": "#e7e7e7"}
    os.makedirs("results/s4_cad", exist_ok=True)
    for plane, (ia, ib, ic), cut in (("XZ@y=mid", (0, 2, 1), L / 2), ("XZ@y=0.35L", (0, 2, 1), 0.35 * L), ("XY@z=6", (0, 1, 2), 0.06 * L)):
        fig, ax = plt.subplots(figsize=(6, 6))
        order = ["structure", "insulation", "hinge", "capacitor", "routing", "electronics", "coil", "pole", "magnet", "pad", "pin", "socket"]
        for kind in order:
            for c in comps:
                if c["kind"] != kind: continue
                B = c["box"]
                if not (B[2 * ic] <= cut <= B[2 * ic + 1]): continue
                ax.add_patch(Rectangle((B[2 * ia], B[2 * ib]), B[2 * ia + 1] - B[2 * ia], B[2 * ib + 1] - B[2 * ib],
                                       facecolor=colors[kind], edgecolor="k", lw=0.4, alpha=0.9 if kind != "coil" else 0.5))
        ax.add_patch(Rectangle((0, 0), L, L, fill=False, lw=1.2, ls="--"))
        ax.set_xlim(-0.12 * L, 1.12 * L); ax.set_ylim(-0.12 * L, 1.12 * L); ax.set_aspect("equal")
        ax.set_xlabel("um"); ax.set_ylabel("um"); ax.set_title(f"NEPL module L={L:.0f} um, section {plane}")
        handles = [Rectangle((0, 0), 1, 1, facecolor=colors[k], edgecolor="k") for k in order]
        ax.legend(handles, order, fontsize=6, loc="upper right", bbox_to_anchor=(1.32, 1))
        fig.savefig(f"results/s4_cad/{tag}_{plane.replace('@','_').replace('=','')}.png", dpi=130, bbox_inches="tight"); plt.close(fig)
    # exploded view: shift each face's parts outward along its normal
    fig = plt.figure(figsize=(7, 7)); ax = fig.add_subplot(111, projection="3d")
    shift = {"z-": (0, 0, -0.6), "z+": (0, 0, 0.6), "y-": (0, -0.6, 0), "y+": (0, 0.6, 0), "x-": (-0.6, 0, 0), "x+": (0.6, 0, 0)}
    for c in comps:
        f = c["name"].split(":")[0]
        d = shift.get(f, (0, 0, 0))
        B = c["box"]
        if c["kind"] in ("structure", "insulation", "socket", "hinge"): continue
        x0, y0, z0 = B[0] + d[0] * L, B[2] + d[1] * L, B[4] + d[2] * L
        ax.bar3d(x0, y0, z0, B[1] - B[0], B[3] - B[2], B[5] - B[4], color=colors[c["kind"]], alpha=0.6, shade=True)
    ax.set_title(f"NEPL L={L:.0f} um exploded (faces offset 0.6 L)"); ax.set_box_aspect((1, 1, 1))
    fig.savefig(f"results/s4_cad/{tag}_exploded.png", dpi=120, bbox_inches="tight"); plt.close(fig)

def main():
    L = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
    comps = build(L)
    bad = check(comps)
    tag = f"nepl_{L:.0f}um"
    os.makedirs("results/s4_cad", exist_ok=True)
    json.dump(comps, open(f"results/s4_cad/{tag}.json", "w"), indent=0)
    total = L**3
    by = {}
    for c in comps:
        if c["kind"] in ("pin",): v = vol(c)        # protrudes; counted separately
        by[c["kind"]] = by.get(c["kind"], 0) + vol(c)
    R = [f"# Session 4 — integrated NEPL module geometry, L = {L:.0f} um (dimensions in um)\n",
         f"Components: {len(comps)}. Interference violations (overlaps not declared as process-integrated): {len(bad)}\n"]
    for a, b, v in bad[:40]:
        R.append(f"- OVERLAP {a} x {b}: {v:.2f} um^3")
    R.append("\n## Volume budget (fraction of the L^3 envelope; pins protrude and sockets are voids inside the skin)\n")
    R.append("| kind | volume (um^3) | fraction |\n|---|---|---|")
    for k, v in sorted(by.items(), key=lambda kv: -kv[1]):
        R.append(f"| {k} | {v:.0f} | {v/total:.3f} |")
    mag = by.get("magnet", 0)
    R.append(f"\nPer-face EPM geometry (derived from the stack, not chosen): " + ", ".join(f"{k} = {v:.1f} um" for k, v in build.GEOM.items()))
    R.append(f"\nSwitchable magnet volume per module: {mag:.0f} um^3 ({mag/total*100:.1f} %); per face: {mag/6:.0f} um^3.")
    R.append("\n## Key dimensions (per face)\n")
    for c in comps:
        if c["name"].startswith("z-:"):
            B = c["box"]
            R.append(f"- {c['name']}: x[{B[0]:.1f},{B[1]:.1f}] y[{B[2]:.1f},{B[3]:.1f}] z[{B[4]:.1f},{B[5]:.1f}] ({c['material']})")
    draw(comps, L, tag)
    R.append(f"\nDrawings: results/s4_cad/{tag}_*.png ; geometry JSON: results/s4_cad/{tag}.json")
    txt = "\n".join(R) + "\n"
    open(f"results/s4_geometry_{L:.0f}.md", "w").write(txt); print(txt)
    return bad

if __name__ == "__main__":
    main()
