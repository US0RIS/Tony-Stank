"""S7. Energy, speed and build-time budget for the face-motor + ISL architecture.

DERIVED estimates (no charge recovery assumed: worst case).
 E_step  = n_cycles * n_phases * (1/2) C_phase V^2 * 2   (charge+discharge loss per phase per cycle)
 n_cycles = L / lam  (one electrical period advances one pitch, synchronous drive)
 v = lam * f_drive
Extrusion: each port advances one module per (lift + feed) = 2 steps.
Run: python3 sims/budget.py -> results/budget.md
"""
import math, os
EPS0 = 8.854e-12

def design(L, g, V, lam, eta=0.6):
    C_face = EPS0 * eta * L**2 / g          # all electrodes of one face vs partner
    C_phase = C_face / 3
    n_cyc = L / lam
    E_step = n_cyc * 3 * C_phase * V**2     # 1/2 CV^2 lost on charge and on discharge
    return C_face, n_cyc, E_step

def main():
    r = ["# S7 energy / speed / build-time budget (DERIVED)\n"]
    r.append("| design | C_face | cycles per step | E per lattice step | step time @ f=10 kHz | speed | power while moving |\n|---|---|---|---|---|---|---|")
    rows = [("L=100 um, g=1 um, 50 V, lam=3.3 um", 100e-6, 1e-6, 50, 3.3e-6),
            ("L=100 um, g=100 nm, 5 V, lam=0.33 um", 100e-6, 1e-7, 5, 0.33e-6),
            ("L=1 mm, g=1 um, 50 V, lam=3.3 um", 1e-3, 1e-6, 50, 3.3e-6),
            ("L=10 um, g=100 nm, 5 V, lam=0.33 um", 10e-6, 1e-7, 5, 0.33e-6)]
    for lab, L, g, V, lam in rows:
        C, n, E = design(L, g, V, lam)
        f = 1e4
        t = n / f
        r.append(f"| {lab} | {C*1e12:.3g} pF | {n:.0f} | {E*1e9:.3g} nJ | {t*1e3:.3g} ms | {lam*f*1e3:.3g} mm/s | {E/t*1e6:.3g} uW |")
    r.append("\nCompare: EPM switching pulse at 100 um ~37 uJ per switch (S1) = ~10^4 x the face-motor step energy.\n")
    r.append("Mechanical work per step against resistance ~2 uN (S2) over 100 um = 0.2 nJ -> electrical efficiency without charge recovery ~1-10 %.\n")
    r.append("## Build time for a rod by port extrusion (each port advances one module per 2 steps)\n")
    r.append("| rod | L | modules | ports (one per column) | step time | growth speed | time to full length | total energy |\n|---|---|---|---|---|---|---|---|")
    for (w, length) in [(5e-3, 0.1), (1e-2, 0.1), (2e-2, 0.3)]:
        for L, Es, ts in [(100e-6, design(100e-6, 1e-7, 5, 0.33e-6)[2], 30e-3), (1e-3, design(1e-3, 1e-6, 50, 3.3e-6)[2], 30e-3)]:
            cols = (w / L) ** 2
            N = cols * length / L
            v = L / (2 * ts)
            T = length / v
            Etot = N * (length / L) / 2 * 2 * Es   # each module in a column is lifted (H/2 avg) times
            r.append(f"| {w*1e3:.0f} mm sq x {length*100:.0f} cm | {L*1e6:.0f} um | {N:.2e} | {cols:.0f} | {ts*1e3:.0f} ms | {v*1e3:.2f} mm/s | {T:.0f} s | {Etot:.3g} J |")
    r.append("\nNote: in port extrusion every module already in the column moves on every lift (~N H/2 module-steps) and the feeder conveyors move a similar number, so total ~N H module-steps;"
             " growth speed per column is L/(2 t_step), independent of cross-section. Speed scales with L at fixed step time:"
             " smaller modules extrude more slowly unless t_step shrinks proportionally.\n")
    r.append("Telescoping (nested ports in series) multiplies speed by the number of stages k at the cost of k x energy.\n")
    txt = "\n".join(r) + "\n"
    os.makedirs("results", exist_ok=True)
    open("results/budget.md", "w").write(txt)
    print(txt)

if __name__ == "__main__":
    main()
