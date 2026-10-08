# PHYSICS — governing equations, scaling, constraints

Claim tags: **VERIFIED** (literature, see LITERATURE.md for its strength) · **DERIVED** (analytic, from stated assumptions) · **SIMULATED** (numerical code in `sims/`) · **HYPOTHETICAL** · **SPECULATIVE**.

## 0. Problem statement

A module of edge L and mass m = ρL³ (ρ = 2330 kg/m³, Si) must do six things:

| Capability | Requirement |
|---|---|
| (A) Power | Draw power P_m from neighbours through a contact impedance Z_c, with drop ΔV ≤ 0.1 V_bus across the whole structure. |
| (B) Data | Exchange data over the same interfaces. |
| (C) Attachment | Hold the interface in tension at pressure p_bond ≥ p_req, where p_req is set by the structure (§5). |
| (D) Motion | Produce interface shear τ with margin M = τA / [μ(F_N + F_adh) + W] > 1. A = active area, μ = friction coefficient, F_N = net electrostatic normal force, F_adh = adhesion, W = weight. |
| (E) Power during motion | Keep a powered path, or store E_hold ≥ P_m t_gap. |
| (F) Endurance | Repeat for ≥ 10⁶–10⁸ steps without contact or wear failure. |
| (G) Global | Keep the configuration connected to the garment after every move (power, data and structure all travel this way). |

## 1. Size scaling (DERIVED; `sims/scaling.py` → `results/scaling_table.md`)

| Effect | Law | 100 µm module (example) |
|---|---|---|
| Weight | ρgL³ | 2.3×10⁻⁸ N |
| Electrostatic pressure | ε₀V² / [2(g + t/ε_r)²], independent of L, force ∝ L² | 10 V across 10 nm air + 100 nm HfO₂ → 2 MPa; at 50 V/µm in air → 11 kPa |
| Capillary (sphere–plane) | 4πRγcosθ ∝ L | ~2000× weight at R = L/2 |
| van der Waals between flat faces | A/(6πD³) per area | 42 Pa at D = 50 nm, 660 kPa at D = 2 nm. Flat-on-flat contact sticks permanently. |
| Permanent magnet at contact | B²/2µ₀ ≈ 400 kPa at 1 T | Ideal case; fringing makes small magnets worse |
| EPM switching current density | J ≈ H_c·l_path / (fill·A_window) ∝ 1/L | 5×10¹⁰ A/m² at 100 µm, about 10–50× above the electromigration and thermal limits (~10⁹ A/m²). Energy ~37 µJ per pulse. **EPMs are excluded below about 1 mm.** |

Consequence: below about 1 mm, weight is irrelevant. The design is controlled by interface forces (adhesion, friction, clamp), by electrical limits, and by contamination.

## 2. Electrostatic face motor (DERIVED; validated by FD to 1.4 % in SIMULATED `sims/face_motor.py`)

**Geometry.** Two faces separated by an air gap g. The bottom surface potential is V₁cos(kx). The top surface potential is V₂cos(k(x−s)), with k = 2π/λ.

**Stresses on the top body** (from the Maxwell stress tensor):

  τ(s) = ε₀k²V₁V₂ sin(ks) / (2 sinh kg)
  p(s) = ε₀k²[V₁² + V₂² − 2V₁V₂ cosh(kg) cos(ks)] / (4 sinh² kg)   (p > 0 is attraction)

**Consequences:**
1. τ/p ≤ sinh(kg) at ks = π/2. If the pitch λ is much larger than the gap, normal force dominates, and friction wins unless the phase is tuned.
2. The phase s can be set so that p = 0 while τ remains about 0.6–0.9 of τ_max, because the like-potential overlap term cancels the self-attraction. Thrust then comes with essentially no friction-generating clamp.
3. At fixed V and g, shear is largest at kg = 1.915, so **λ ≈ 3.3 g**. There, τ_max = 1.105·ε₀V²/(2g²).
4. **Scale invariance.** Stress depends only on the field V/g and on kg. Two designs give the same ~7 kPa (after the discrete-electrode factor):
   - 50 V, 1 µm gap, 3.3 µm pitch
   - 5 V, 100 nm gap, 0.33 µm pitch (CMOS-compatible)
5. **No gas breakdown below about 12 V.** Below the ionisation potential of O₂/N₂ (~12–15 V), an electron cannot gain enough energy across the whole gap to start an avalanche. The 5 V design is therefore safe from gas breakdown. The 50 V / 1 µm design lies in the regime where Paschen's law fails (Torres & Dhariwal), so it is UNCERTAIN.
6. **Discrete electrodes.** 3-phase stripes give 0.57–0.60 of the ideal sinusoidal shear (SIMULATED, FD).

**Sliding size floor.** Thrust scales as L², while adhesion at a fixed number of standoff bumps is roughly constant, so the margin M ∝ L². With 9 bumps of radius 0.5 µm, μ = 0.4 and 50 V/µm:
- M = 1 at L ≈ 20 µm in humid air (capillary) and ≈ 10 µm dry.
- M ≈ 25 at L = 100 µm in humid air (SIMULATED).

**10 µm modules cannot slide electrostatically in humid air** unless adhesion is engineered down by about 10× (hydrophobic surfaces, fewer or sharper bumps).

## 3. Power through contact lattices (SIMULATED nodal solve, `sims/power_network.py`)

- **Chain.** ΔV = I·R·h(h+1)/2, reproduced exactly by the solver.
- **Uniform 3D block on the garment.** Columns are electrically independent, so ΔV depends only on the height h in hops, not on width (SIMULATED for w = 1, 5, 20).
- **Root-fed horizontal arm.** It behaves exactly like a single chain of the same length: the cross-section cancels.
- **Electrical reach:** h_max ≈ √(0.2·V_bus² / (P_m·R_c)). Physical reach = h_max·L.
  - Ohmic contact, 1 Ω, 1 µW, 3 V: 13 cm at L = 100 µm.
  - 100 Ω at the same power and voltage: 1.3 cm.
  - Capacitive face coupling (|Z| ≈ 12 kΩ at 100 MHz, 100 nm gap, 100 µm face): ~1 mm.
  
  **Capacitive coupling cannot be the power bus at 100 µm.** It remains usable for data.
- **Hold-up.** A deep-trench capacitor on one face (57.8 nF/mm²) stores 1.45 nJ usable at L = 100 µm. That is about 0.36 of one lattice step (4 nJ, §6). **Stored energy cannot bridge a full step at 100 µm; contact must be continuous during motion.**
- **Swarm standby power.** 10⁷ modules × 1 µW = 10 W, which drains a 15 Wh battery in 1.5 h. Static power must be ≤ 10 nW per module (0.1 W total).

## 4. Interfaces: friction vs adhesion vs strength (DERIVED)

There is a fundamental conflict:
- **Sliding** needs a gap of ≥ 50 nm held by sparse standoffs. Otherwise van der Waals and capillary forces between flat faces (hundreds of kPa at 2 nm) make friction prohibitive.
- **Tensile strength** from electrostatics across that air gap is capped at the field limit: p ≈ ε₀E²/2 ≈ 11 kPa at 50 V/µm.
- MPa-level electrostatic clamping requires intimate contact through a thin high-κ dielectric, which is exactly the state that cannot slide.

**Resolution adopted:** carry tension mechanically with undercut interlocks. Silicon's fracture strength is GPa-class, so ~10–100 MPa nominal is plausible after neck-area and stress-concentration knock-downs (HYPOTHETICAL until E3). Electrostatics then supplies only shear for motion and the shear lock.

**A preloaded electrostatic joint fails without warning.** While the applied tension is below p, the joint is as stiff as its compressed standoffs. Above p, the force falls with gap (negative stiffness −2p/g) and the joint snaps open.

## 5. Structural requirements (DERIVED; `sims/structure.py`)

- **Single-file chain:** reach = √(pL / 3ρg) ∝ √L. Smaller modules give shorter reach. At p = 6 kPa (Karagozler latch) the reach is 3 mm for 100 µm modules.
- **Solid beam:** l_max = √(p·h / 3φρg), independent of L. A 10 mm-thick beam needs 400 kPa to reach 28 cm under its own weight.
- **Payload:** 1 N at the end of a 10 cm arm with a 10 mm square section needs **600 kPa** interface tensile strength.
- **Verdict:** air-gap electrostatic attachment (≤ 11 kPa) is 10–60× too weak for human-scale structures. Interlocks or another MPa mechanism are mandatory.

## 6. Energy, speed, build time (DERIVED; `sims/budget.py`)

- **Energy per lattice step** (no charge recovery) is about 4 nJ at L = 100 µm, independent of the design within the constant-field family. EPM switching costs ~37 µJ, about 10⁴× more.
- **Speed** = λ·f_drive: 3.3 mm/s at 0.33 µm pitch and 10 kHz; 33 mm/s at 3.3 µm pitch.
- **Port extrusion growth speed** = L / (2 t_step), independent of cross-section. A 10 mm × 10 mm × 10 cm rod of 100 µm modules (10⁷ modules, 10⁴ ports, 30 ms steps) takes ~60 s and ~40 J. With 1 mm modules it takes 6 s.
- **Speed and module size trade off.** Smaller modules extrude more slowly unless step frequency rises proportionally. Telescoping (k stages in series) multiplies speed by k.

## 7. Assumptions to attack first

| Assumption | Why it matters |
|---|---|
| μ = 0.4 | Si–Si and SiO₂ sliding could be 0.2–0.8. Wear debris could raise it. |
| Adhesion model: 9 hemispherical bumps of R = 0.5 µm, full capillary meniscus | Sets the sliding size floor. |
| 50 V/µm field in air at a 1 µm gap is sustainable | Uncertain (§2 point 5). |
| Gap held to ±20 % | Must hold across the face: about ±20 nm flatness for the 100 nm design. |
| Field confined to the gap (surface-potential idealisation) | Fringing and back-side fields are ignored. |
| Discrete-electrode factor applied to both τ and p | Approximation: the FD factor was computed for τ only. |
