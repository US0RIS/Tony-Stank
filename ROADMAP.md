# ROADMAP — shortest credible path to a first physical prototype

**Principle:** Falsify the riskiest physics at the cheapest scale first. Shrink only after each scale passes.

| Phase | Goal | Exit criterion | Indicative cost / time |
|---|---|---|---|
| 0 | **Verify the literature.** Read full texts (Karagozler 2007; DEMED 1995; Torres & Dhariwal 1999; Penskiy/Bergbreiter; Miskin 2020; Abel et al. 2024; Kawano 2017–2023). Replace SNIPPET values. Run a patent search on the ISL-PE combination. | Every number used in `sims/` is traced to a primary source or flagged | Days |
| 1 | **E5: 10 mm ISL-PE macro prototype.** Passive interlocking blocks with brush contacts; one motorised port (lead screw, not electrostatic). | 20-block column extrudes and retracts 100×; LED in the top block stays lit; holds 0.5 N at 10 blocks | Weeks, desktop FDM/SLA printer plus a CNC mill |
| 2 | **Electrostatic drive at 1 mm.** DEMED-style 3-phase flex-PCB electrodes (pitch ~100–320 µm, as already demonstrated) on block faces. Port thrust becomes electrostatic. Tests E1 at large pitch. | Column lift by face drive with margin > 3 | 1–2 months; flex PCB fab |
| 3 | **Microfabricated interface coupons (E1, E3, E4, E2)** at 100 µm-equivalent pitch and gap. Si DRIE plus surface electrodes (an MPW or university cleanroom). | E3: ≥ 1 MPa pull-out and 10⁵-cycle sliding. E1: shear ≥ 3 kPa at zero normal. E4: seam crossing. E2: R ≤ 100 Ω | 3–6 months |
| 4 | **1 mm Si modules**, passive bodies with active port chips. CMOS 3-phase driver chiplet only in port and sleeve modules. | Extrude a 5 × 5 × 50-module rod from a 2D port array | 6–12 months |
| 5 | **Garment magazine.** Sealed conveyor sleeve; particle-exclusion skin. | 1 h of operation in ordinary indoor air without jams | — |
| 6 | **Shrink to 300 → 100 µm.** Use the 5 V / 100 nm / 0.33 µm-pitch face drive (CMOS-compatible). Static power ≤ 10 nW per module. | Margins from Phase 3 coupons hold at module scale | Years |

## Decision gates
- **If E3 fails** (interlocks jam or wear): fall back to Architecture A for small structures only. Look for an MPa-class switchable attachment, for example a zipping thin-film clamp that leaves sliding mode by deforming. This is an open research problem.
- **If E1 fails** at microscale: use electrostatic inchworms in port modules only. They need not be in every module.
- **If S-E6 shows locked configurations:** restrict the target to extrudable shape families, which is still useful (rods, blades, walls, braces, grippers built from opposing extrusions).

## What a first wearable demo honestly looks like
A cuff or forearm patch holding a sealed magazine of 1 mm interlocking blocks. A port array extrudes a 5–10 cm rigid rod or blade on a gesture command in a few seconds, and retracts it again. It is genuinely physical and load-bearing, with no illusion involved. It is not yet "invisible clothing" (blocks of 1 mm are visible), and the shape class is limited to extrusions.

## Session-2 update
The roadmap above is now **Track A**. Phase 3 must start with E1′ (sealed vs open-air face drive with particles), and Phase 1 must include cam latches (E6). **Track B** runs in parallel, with its own gates E7 (bolt latch) and E8 (compliant electrodes): see TRACKS.md. Track B is not deferred: E7 and E8 share fabrication runs with Track A's Phase 3 coupons.
