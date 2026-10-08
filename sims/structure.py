"""S5. Mechanical reach of structures built from modules held by interface bonds.

DERIVED models:
 (a) single-module-wide horizontal chain: root moment M = rho g L^4 N^2/2 must be
     carried by a face bond of tensile strength p acting over L^2 with lever ~L/2
     (peeling about one edge, linear stress distribution: M_cap = p L^3 / 6).
     -> N_max = sqrt(p / (3 rho g L)),  reach = N L = sqrt(p L / (3 rho g)).
 (b) solid prismatic beam of depth h (many modules thick), joints = material with
     tensile strength p, effective density phi*rho:  sigma = 3 phi rho g l^2 / h
     -> l_max = sqrt(p h / (3 phi rho g))   (independent of module size L)
 (c) tip payload F at length l: required p = 6 F l / (b h^2).
 (d) joint stiffness: preloaded standoffs until tension exceeds clamp p, then snap-open;
     effective modulus E_eff = k_i * L.
Run: python3 sims/structure.py -> results/structure.md
"""
import math, os
RHO, G = 2330.0, 9.81

def chain_reach(p, L):
    return math.sqrt(p * L / (3 * RHO * G))

def beam_length(p, h, phi=0.74):
    return math.sqrt(p * h / (3 * phi * RHO * G))

def p_for_payload(F, l, b, h):
    return 6 * F * l / (b * h**2)

def main():
    r = ["# S5 structural reach (DERIVED)\n"]
    r.append("## (a) single-file horizontal chain: reach = sqrt(p L / (3 rho g))\n")
    r.append("| bond strength p | L=10 mm | 1 mm | 100 um | 10 um |\n|---|---|---|---|---|")
    for p, lab in [(6e3, "6 kPa (Karagozler 2007 latch, VERIFIED)"), (50e3, "50 kPa (dry adhesive)"),
                   (400e3, "400 kPa (B=1 T magnet)"), (2e6, "2 MPa (thin-film e-static clamp, DERIVED)"),
                   (100e6, "100 MPa (Si interlock, DERIVED)")]:
        r.append(f"| {lab} | " + " | ".join(f"{chain_reach(p, L)*1e3:.2f} mm" for L in (1e-2, 1e-3, 1e-4, 1e-5)) + " |")
    r.append("\nSmaller modules -> shorter single-file reach (reach ~ sqrt(L)).\n")
    r.append("## (b) solid beam, packing phi=0.74: self-weight limit l_max = sqrt(p h / (3 phi rho g))\n")
    r.append("| p | h=1 mm | h=5 mm | h=10 mm | h=30 mm |\n|---|---|---|---|---|")
    for p in (6e3, 50e3, 400e3, 2e6):
        r.append(f"| {p/1e3:.0f} kPa | " + " | ".join(f"{beam_length(p, h)*100:.1f} cm" for h in (1e-3, 5e-3, 1e-2, 3e-2)) + " |")
    r.append("\n## (c) bond strength needed to hold a payload at the tip (beam b = h)\n")
    r.append("| payload | arm length | section | required p |\n|---|---|---|---|")
    for F, l, h in [(1.0, 0.1, 0.01), (1.0, 0.1, 0.02), (10.0, 0.3, 0.03), (0.1, 0.1, 0.005)]:
        r.append(f"| {F} N | {l*100:.0f} cm | {h*1e3:.0f} mm square | {p_for_payload(F,l,h,h)/1e3:.0f} kPa |")
    r.append("\n## (d) stiffness of a preloaded electrostatic joint\n")
    r.append("The clamp pressure p preloads the standoff bumps. While applied tension < p the bumps stay compressed and the joint\n"
             "is as stiff as the bumps: k_i ~ f_b E_Si / g. When tension exceeds p, the electrostatic force falls with gap\n"
             "(negative stiffness -2p/g) and the joint snaps open: brittle, no warning. Design rule: working load << p.\n")
    for fb, g in [(0.01, 1e-6), (0.001, 1e-7)]:
        ki = fb * 170e9 / g
        r.append(f"- f_b={fb}, g={g*1e9:.0f} nm: k_i={ki:.2e} Pa/m -> E_eff(L=100 um) = k_i L = {ki*1e-4/1e9:.0f} GPa (bump-limited upper bound)")
    txt = "\n".join(r) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/structure.md", "w").write(txt)
    print(txt)

if __name__ == "__main__":
    main()
