# FABRICATION_PLAN — process route, compatibility, yield (session 4)

Code: `sims/s4/fab_yield.py` → `results/s4_fab_yield.md`. Evidence: ENGINEERING ANALYSIS. Step yields are ASSUMED ranges.

## Route (the only credible route found): six face tiles bonded onto a core

Most microfabrication is single-sided and planar. A cube with an EPM, 3D solenoids and pins on all six faces therefore cannot be made monolithically. Folding a net gives ±1–2° fold error, which is 2–4 µm at 100 µm against 1 µm clearances (reviewer R3).

The route is to make six face tiles, a core stack and corner/edge blocks separately, then assemble.

| # | Step | Process type | Max T | Demonstrated individually? |
|---|---|---|---|---|
| 1 | Tile pockets (poles, bars, sockets) | lithography + DRIE | 25 °C | yes |
| 2 | (ON/OFF variant only) NdFeB hard film + anneal | sputtering | **650 °C** | yes, films ≤ 50 µm |
| 3 | Lower coil metal + insulation | electroplating + polyimide | 350 °C | yes |
| 4 | NiFe pole pieces | through-mask electroplating | 90 °C | yes |
| 5 | CoP switchable bars, 12 × 4 × 58 µm | field-assisted electroplating | 90 °C | films yes; **patterned micro-bars with measured loops: NO** |
| 6 | Upper coil metal + vias closing a 3D solenoid around the semi-hard core | electroplating | 350 °C | 3D solenoids yes, at larger pitch; **around a semi-hard core at 3 µm pitch: NO** |
| 7 | Pins, Ti/Au pads, cover | DRIE, evaporation | 300 °C | yes |
| 8 | Tile release and thinning to 12 µm | etch / grind | 25 °C | yes |
| 9 | Core: 2 thinned CMOS dies + trench capacitor + TSVs | CMOS foundry + 3D stacking | 400 °C | yes |
| 10 | Six-sided assembly of tiles onto the core | precision pick-and-place + bonding | 250 °C | **NO**: six-sided microassembly of 100 µm parts not demonstrated |
| 11 | Magnetisation set with on-chip coils | — | 25 °C | **NO** for CoP micro-bars |
| 12 | Test and sort | probing | 25 °C | yes |

**Temperature ordering:** consistent only if the 650 °C hard-magnet anneal (when used) is done first on bare tiles and every later step stays ≤ 400 °C. CoP needs no anneal, which is favourable.

**Integration status:** each component class has been fabricated individually, except items 5, 6 and 11 in this form. **No integrated device combining these steps has been demonstrated at any scale ≤ 1 mm.** The closest is a UF EPM poster at 60–80 µm thickness (snippet, no data).

## Tolerance and yield

| Scale | Clearance | Placement σ | P(all 6 faces aligned) | Module yield (step yield 0.995–0.999) |
|---|---|---|---|---|
| 100 µm | 1 µm | 0.5–0.67 µm | 0.17–0.57 | **10–15 %** |
| 300 µm | 3 µm | 0.67 µm | ≈ 1.0 | 58–87 % |
| 1 mm | 10 µm | 1 µm | ≈ 1.0 | 58–87 % |

- Swarm scale: 1e7 modules at 300 µm means 6e7 tile placements, which is machine-years of pick-and-place (R3). Wafer-level self-assembly (fluidic) is a research topic, not a demonstrated route for six-sided cubes.
- At 100 µm the 1 µm clearances cannot be widened without shrinking the already flux-starved bars.

## Most likely failure points, in order

1. Six-sided assembly alignment (100 µm).
2. 3D solenoid around a plated semi-hard core at 1.5–3 µm pitch.
3. Patterned CoP bar loop quality, which is unmeasured.
4. Contact pads: only 0.25 µN of clamp force per pad at 100 µm.
5. Thinning and handling 12 µm tiles.

## By scale

- **1 mm:** hybrid assembly is plausible today. Tiles could carry bulk-machined or sintered micro-magnets placed by pick-and-place, instead of plated films. This is not equivalent to the microfabricated design, and it is a substitution.
- **300 µm:** plausible with film magnets, but every step from 5 to 11 above is undemonstrated in combination.
- **100 µm:** not credible. Alignment, the coil process and the material all fail simultaneously.
