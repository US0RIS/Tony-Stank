# LITERATURE — verified sources, prior art, experimental evidence

## Evidence status (read first)

Four literature subagents and the lead researcher searched the web on 2026-10-08. **Every attempt to fetch full text from a primary publisher failed: the session's egress proxy blocked nature.com, science.org, arxiv.org, ncbi, iopscience, dspace.mit.edu and others.** As a result:

- **VERIFIED-META**: the title, authors, venue and identifier were confirmed in search results that showed the URL or DOI. Numbers in these rows come from abstracts or search-result summaries. Nobody read the full text.
- **SNIPPET**: the number appeared only in a search snippet, a press article, a patent or a secondary page. Treat it as a lead, not as evidence.
- **UNVERIFIED**: the item could not be confirmed, or sources conflict.

No row in this file is VERIFIED in the strong sense (number checked against the paper's full text). Closing that gap is task 0 in `ROADMAP.md`.

## 1. Modular, self-reconfiguring and microscopic robots

| System | Size | Attach / move / power path | Key numbers | Source | Status |
|---|---|---|---|---|---|
| Karagozler et al., "Electrostatic latching for inter-module adhesion, power transfer, and communication in modular robots", IROS 2007, pp. 2779–2786 | 28 cm cube modules | Electrostatic latch based on capacitive coupling, which also carries power and data | Holds >0.6 N/cm² (6 kPa) with almost zero static power | [CMU KiltHub](https://kilthub.cmu.edu/articles/journal_contribution/Electrostatic_Latching_for_Inter-module_Adhesion_Power_Transfer_and_Communication_in_Modular_Robots/6605150) | VERIFIED-META |
| Karagozler et al., Claytronics latch demo, AAAI WS 2006 | 30 cm | Electrostatic flap latch, 450 V | ≈0.5 N/cm² | [AAAI PDF](https://cdn.aaai.org/Workshops/2006/WS-06-15/WS06-15-004.pdf) | SNIPPET |
| Gilpin, Knaian, Rus, "Robot Pebbles", ICRA 2010 | 1 cm (12 mm later) | Electropermanent (EP) magnets; power and data through the EP contacts | 9600 bps; connector holds >85× module weight | doi:10.1109/ROBOT.2010.5509817 | VERIFIED-META; numbers SNIPPET |
| Gilpin & Rus, "What's in the Bag" (Smart Sand), RSS 2012 | ~12 mm | EP magnets | Simulation >1400 modules | [RSS08 p12](http://www.roboticsproceedings.org/rss08/p12.html) | VERIFIED-META |
| Romanishin, Gilpin, Rus, M-Blocks, IROS 2013; 3D M-Blocks | 50 mm (3D) | Flywheel pivoting; permanent magnets | Modules leave contact during a pivot | [MIT DSpace](https://dspace.mit.edu/handle/1721.1/124967) | VERIFIED-META |
| DILI module (arXiv 1904.09889) | cm, 12 g | EPM actuator that both connects and slides | ~20 mm/s; stepwise rather than continuous | [arXiv](https://arxiv.org/pdf/1904.09889) | VERIFIED-META |
| Datom (Piranda, Bourgeois et al., arXiv 2005.03402) | mm target | Deformable module that keeps its connectors in contact during the move | Motivation: a rigid catom can lose its connection mid-move | [arXiv](https://arxiv.org/pdf/2005.03402) | VERIFIED-META |
| 3D Catoms (Piranda & Bourgeois, DARS 2016) | ~1 mm target | Electrostatic, FCC lattice rotations | No hardware result | [FEMTO-ST](https://projects.femto-st.fr/programmable-matter/node/73) | VERIFIED-META |
| Miskin et al., Nature 584:557 (2020) | 40–70 µm | Electrochemical legs; laser onto on-chip photovoltaics; no attachment | ~200 mV, ~10 nW (sources conflict between µV and mV); >1 M robots per 4" wafer | doi:10.1038/s41586-020-2626-9 | VERIFIED-META; numbers CONFLICTING |
| Reynolds et al., Sci. Robot. 2022 | 100–250 µm | Light-powered; ~1000-transistor onboard clock | >10 µm/s | doi:10.1126/scirobotics.abq2296 | VERIFIED-META |
| Contreras & Pister, silicon inchworm walkers (2017–2019) | 5×6×0.5 mm, 18 mg | Electrostatic inchworm; off-chip wires | ~1.8 mN/mm² at 100 V; drive 1 mW | [HMC PDF](https://uro.hmc.edu/sites/default/files/publications/2021-11/dsc_first_steps_of_a_millimeter-scale_walking_silicon_robot.pdf) | SNIPPET |
| Rubenstein et al., Kilobots, Science 345:795 (2014) | ~3 cm | No attachment | 1024 robots formed 2D shapes | doi:10.1126/science.1254295 | VERIFIED-META |
| Yoshida et al., SMA micro unit (2001) | 2 cm, 15 g | SMA rotation | — | J. Robot. Mechatron. 13(2) | VERIFIED-META |

**Smallest demonstrations found.** Nothing below about 1 cm combines module-to-module locomotion, reversible attachment and power through contacts. The power-and-data-through-contacts row with numbers is Pebbles at 1 cm. Sub-mm robots (Miskin, Reynolds) move alone, unattached, and run on optical power.

## 2. Reconfiguration theory

| Result | Source | Status |
|---|---|---|
| Sliding cubes: universal in-place reconfiguration, O(n²) moves, asymptotically tight (Abel, Akitaya, Kominers, Korman, Stock) | SoCG 2024, LIPIcs 293, [doi:10.4230/LIPIcs.SoCG.2024.1](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2024.1); [arXiv 0802.3414](https://arxiv.org/pdf/0802.3414) | VERIFIED-META |
| Pivoting squares: universal with a constant number of helper modules ("musketeers"), O(n²); some configurations are rigid without them (Akitaya et al.) | ESA 2019, [arXiv 1908.07880](https://arxiv.org/pdf/1908.07880) | VERIFIED-META |
| Crystalline atoms (expand/contract): O(log n) parallel steps | [arXiv 0908.2440](https://arxiv.org/pdf/0908.2440) | VERIFIED-META |
| Tunneling-based reconfiguration of sliding-only cubic modules (Kawano, ICRA 2017; RA-L 2023 linear time) | doi:10.1109/ICRA.2017.7989100 | VERIFIED-META |
| Lattice models in which alignment bumps forbid squeezing into a one-cell gap (MIT–NASA) | [SWAT 2024 PDF](https://erikdemaine.org/papers/SpaceRobots_SWAT2024/paper.pdf) | VERIFIED-META |
| "No hardware implements the sliding-cube model in the general 3D case" | Patent text (US10857669) | SNIPPET (an opinion, not a measurement) |

## 3. Actuation

| Item | Numbers | Source | Status |
|---|---|---|---|
| DEMED: Dual Excitation Multiphase Electrostatic Drive (Univ. Tokyo / Higuchi lab). Both slider and stator carry 3-phase electrodes. | 320 µm pitch, flexible printed circuit film; 7 g prototype gave 4.4 N and 1.6 W; stacked version gave 310 N | [Higuchi lab page](https://am.t.u-tokyo.ac.jp/research/es_motor/demed_e.html); [OSTI 415524](https://www.osti.gov/biblio/415524) | VERIFIED-META |
| DEMED force ripple; electrode skew suppresses it | IEEJ 1997 | [doi:10.1541/ieejias.117.1139](https://doi.org/10.1541/ieejias.117.1139) | VERIFIED-META |
| Electrostatic inchworm (Penskiy & Bergbreiter) | 1.88 mN at 110 V; 23.6 M cycles; 8.75 % efficiency | [UMD thesis](https://drum.lib.umd.edu/items/5f9dd990-4132-44d9-a751-aa6ae73dc0fd) | SNIPPET |
| Electroadhesion, thin parylene | 120 kPa shear at 50 V with <0.8 µm dielectric (shear, not normal) | Chen & Bergbreiter (PMC10359345) | SNIPPET |
| Electrothermal chevron | 50 mN at ~19 V, ~4.75 W | US patent 8539854 | SNIPPET |
| AlN piezo out-of-plane actuator | 1.3 µm stroke at ±60 V | [MDPI Micromachines](https://www.mdpi.com/2072-666X/13/4/625/html) | SNIPPET |
| EPM (Knaian MIT thesis) | No switching-energy figure retrieved | [DSpace 1721.1/60151](https://dspace.mit.edu/handle/1721.1/60151) | UNVERIFIED |

## 4. Breakdown, contacts, storage, power

| Item | Numbers | Source | Status |
|---|---|---|---|
| Torres & Dhariwal, "Electric field breakdown at micrometre separations", Nanotechnology 10 (1999) 102 | Paschen's law fails below about 4 µm (attributed to field emission plus microprotrusions); gaps of 0.5–25 µm studied | [HW portal](https://researchportal.hw.ac.uk/en/publications/electric-field-breakdown-at-micrometre-separations-in-air-and-vac/) | VERIFIED-META |
| Au–Au microcontact at 200 µN | ~0.1 Ω rising to ~1 Ω at 10⁷ cycles; open at ~2×10⁷ | Ewha DSpace | SNIPPET |
| Pt-on-Au dual-material contact | R < 0.3 Ω, up to 40× longer life | [KAIST](https://dspace.kaist.ac.kr/handle/10203/209384) | SNIPPET |
| Deep-trench Si capacitor | 57.8 nF/mm² (25 nm Si₃N₄) | [Springer, Microsyst. Technol.](https://link.springer.com/article/10.1007/s00542-015-2681-6) | SNIPPET |
| On-chip micro-supercapacitor (porous Au + PANI) | 60 mF/cm², 5.44 µWh/cm² | PMC11378337 | SNIPPET |
| Electromigration limits | Al <2×10⁵ A/cm², Au <5×10⁵ A/cm² (vendor rule of thumb) | rfessentials.com | SNIPPET |

## 5. Macro prior art for the extrusion concept (ARCHITECTURES §B)

| Item | Relevance | Source | Status |
|---|---|---|---|
| Rigid chain actuators, zip-chain, Spiralift | Flexible stored links lock into a rigid column as they are pushed out of a housing. This is the macroscopic analogue of port extrusion. | [Wikipedia: Rigid chain actuator](https://en.wikipedia.org/wiki/Rigid_chain_actuator); [Hizook on Spiralift](https://hizook.com/spiralift-ultimate-telescoping-linear-actuator/) | VERIFIED-META |

## 6. Prior-art check for this project's proposals

- **A single electrode set used for clamping, power and data**: prior art. Karagozler 2007 does all three, though not with sliding locomotion.
- **Multiphase electrode arrays on both bodies producing thrust**: prior art (DEMED, about 1995).
- **A sliding module that keeps its connection during the move**: prior art as a goal (Datom, DILI).
- **Combination proposed here**: DEMED-type drive between faces of adjacent sub-mm modules, phase-controlled to give near-zero net normal force, with all tension carried by permanent undercut interlocks, and growth by extrusion through ports in a garment layer. The searches above did not find this combination. That is weak evidence of novelty, because full-text search was blocked. **Do not claim novelty until a patent search (CPC B25J 9/08, H02N 1/00) and a full-text review are done.**

## 7. Session-3 additions (four subagents + lead; full text blocked again, so everything is SNIPPET unless noted)

| Item | Value | Source |
|---|---|---|
| Sputtered NdFeB thick films (Dempsey) | Br ≈ 1.3–1.4 T, Hc ≈ 1.6–2 T, ≤ 50 µm, ≥ 650 °C anneal | arXiv cond-mat/0703785 |
| Electroplated CoPt (Arnold, UF) | Hc ≤ 850–1000 kA/m, Br ≤ 0.8 T, ≤ 100 µm | UF IMG listing |
| Parylene-bonded NdFeB | Br 0.69 T | doi:10.1109/MEMSYS.2012.6170220 |
| CoPtP pulse-reverse plating | Hc 268 kA/m, Br 0.4 T | cora.ucc.ie/handle/10468/7756 |
| Microcoil failure (150–300 µm OD) | 3600 A/mm² max, 610 A/mm² safe (unit conflict in source) | ebuah.uah.es/dspace/handle/10017/64267 |
| Knaian EPM thesis | Title confirmed; numbers not obtained | dspace.mit.edu/handle/1721.1/60151 |
| Kubits (EPM pivoting cubes, 25 mm) | prior art for magnetic pivoting | doi:10.1109/LRA.2020.3013884 |
| Milli-Motein | 1 cm, EPM wobble motor, 2.6 W, holds shape unpowered | MIT News 2012 |
| Moteins universality | Cheung, Demaine, Bachrach, Griffith, IEEE T-RO 27(4):718–729, 2011, doi:10.1109/TRO.2011.2132951 | VERIFIED-META |
| ARMADAS | Gregg et al., Science Robotics 9(86) 2024, doi:10.1126/scirobotics.adi2746; 256 voxels in 4.2 days | NASA NTRS 20230005194 |
| Hybrid programmable matter: one active agent suffices in 3D | Hinnenthal, Rudolph, Scheideler | arXiv 2401.17734 |
| Hybrid-model algorithms for targets with holes | Friemel, Liedtke, Scheffer | arXiv 2501.08663 |
| Polysilicon sidewall wear in air | 3 of 7 failed at ~10⁵ cycles; μ 0.11 → 0.20 | lbl.gov/ritchie MEMS wear page |
| Sandia microengine wear and humidity | wear-dominated; debris rises at low RH | osti.gov/biblio/3325 |
| Polyimide hinge fatigue | 7×10⁴ (RoboBee) to 3×10⁵ cycles | smrl.mit.edu iros14_malka.pdf; par.nsf.gov 10567610 |
| Si snap fastener insertion | ~30 µN (50×2 µm beams) | UW MEMS ASME-IMECE 1995 |
| Indoor microfibre deposition | ~1960 fibres/m²/day | Front. Built Environ. 2025 (doi 10.3389/fbuil.2025.1556698) |
| Hot-switched Au–Pt contact degradation in air | rose after ~100 cycles; N₂ much better | Sandia 2005 publication page |
| **Not found** | microfabricated semi-hard switchable magnet films; pulsed microcoil limits; MEMS latch mating-cycle life; size-resolved particle deposition flux | — |
