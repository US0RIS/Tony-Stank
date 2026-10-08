"""SESSION 4 / PHASE 8. Process-flow temperature ordering check and yield model per scale.
MATHEMATICAL (bookkeeping); step yields are ASSUMED ranges, not data.
Run: python3 sims/s4/fab_yield.py -> results/s4_fab_yield.md"""
import math, os

# (step, max process temperature C, demonstrated individually? , notes)
FLOW = [
    ("Face-tile wafer: Si DRIE pockets for poles/bars/sockets", 25, "yes", "standard DRIE"),
    ("Hard magnet (only if ON/OFF EPM variant): NdFeB sputter + anneal", 650, "yes (films)", "must precede Cu/polyimide/CoP"),
    ("Bottom coil metal (plated Cu) + SiO2/polyimide insulation", 350, "yes", "polyimide cure ~350 C"),
    ("NiFe pole pieces (plated, through-mask)", 90, "yes", ""),
    ("CoP switchable bars (plated, field-assisted)", 90, "films yes; patterned 4x12x58 um bars NO data", "no anneal; squareness unknown"),
    ("Top coil metal + vias closing the 3D solenoid", 350, "3D solenoids yes (larger pitch); around semi-hard core NO", ""),
    ("Pins (DRIE Si), pads (Ti/Au), cover", 300, "yes", ""),
    ("Tile release + thinning to 12 um", 25, "yes (thinning)", "fragile 12 um tiles"),
    ("Core: 2 thinned CMOS dies + trench capacitor + TSV redistribution", 400, "yes (3D stacking)", "die 74x74 um at 100 um scale"),
    ("Six-sided assembly: tiles bonded to core + edge/corner blocks", 250, "NO (no 6-sided microassembly of 100 um parts demonstrated)", "placement +-1-2 um (3 sigma) vs 1 um clearances"),
    ("Magnetisation set (on-chip coils)", 25, "NO for CoP micro-bars", ""),
    ("Test + sort", 25, "yes", "per-module probing"),
]

def yield_model(n_steps, p, n_bonds, p_bond, n_faces=6, p_face_align=None):
    Y = p**n_steps * p_bond**n_bonds
    if p_face_align is not None: Y *= p_face_align**n_faces
    return Y

def p_align(clearance, sigma):
    """Probability a single face is within clearance given placement error N(0, sigma) in 2 axes."""
    z = clearance / sigma
    p1 = math.erf(z / math.sqrt(2))
    return p1 * p1

def main():
    R = ["# Session 4 — fabrication flow and yield (MATHEMATICAL bookkeeping; yields ASSUMED)\n",
         "## Process flow and temperature ordering\n", "| # | step | max T (C) | demonstrated individually? | note |\n|---|---|---|---|---|"]
    for i, (s, T, d, n) in enumerate(FLOW, 1):
        R.append(f"| {i} | {s} | {T} | {d} | {n} |")
    R.append("\nTemperature ordering is consistent only if the hard-magnet anneal (650 C) happens first on bare tiles and every later step stays "
             "<= 400 C; CoP needs no anneal (favourable). No integrated device combining all steps has been demonstrated at any scale <= 1 mm.\n")
    R.append("## Face alignment probability (placement sigma vs layout clearance)\n| L | clearance (um) | placement sigma (um) | P(face OK) | P(all 6 faces OK) |\n|---|---|---|---|---|")
    for L, clr, sig in ((100, 1.0, 0.5), (100, 1.0, 0.67), (300, 3.0, 0.67), (1000, 10.0, 1.0)):
        pf = p_align(clr, sig)
        R.append(f"| {L} | {clr} | {sig} | {pf:.3f} | {pf**6:.3f} |")
    R.append("\n## Module yield (100 process steps, bonds as listed)\n| scale | step yield | bonds | bond yield | alignment (6 faces) | module yield | good modules in 1e4 / 1e7 |\n|---|---|---|---|---|---|---|")
    for L, nb, clr, sig in ((100, 36, 1.0, 0.67), (300, 36, 3.0, 0.67), (1000, 36, 10.0, 1.0)):
        for p in (0.999, 0.995):
            Y = yield_model(100, p, nb, 0.999, p_face_align=p_align(clr, sig))
            R.append(f"| {L} um | {p} | {nb} | 0.999 | {p_align(clr, sig)**6:.3f} | {Y:.3f} | {Y*1e4:.0f} / {Y*1e7:.2e} |")
    R.append("\nThe 100 um design's 1 um clearances against ~+-2 um (3 sigma) six-tile placement leave most modules misaligned (reviewer 3 finding, reproduced here). "
             "At 300 um and 1 mm the clearances scale with L while placement accuracy does not, so alignment stops dominating.\n")
    txt = "\n".join(R) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/s4_fab_yield.md", "w").write(txt); print(txt)

if __name__ == "__main__":
    main()
