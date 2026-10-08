# Session 3 — mechanical / MEMS mechanisms: kill-parameter screen (MATHEMATICAL DERIVATION)

Reference resistance: humid peel/adhesion F_adh ~ 4.1 uN at 9 bumps (constant with L unless bumps are scaled); peel torque = F_adh L; weight = rho g L^3.

## 1. Electrostatic zipping hinge (rigid plates) - torque at 90 deg and 10 deg opening vs peel torque

| L | V | T(90 deg) | T(10 deg) | peel torque | margin @90 | margin @10 |
|---|---|---|---|---|---|---|
| 10000 um | 30 | 2.16e-10 | 1.46e-08 | 1.14e-04 | 1.9e-06 | 0.00013 |
| 10000 um | 100 | 2.40e-09 | 1.62e-07 | 1.14e-04 | 2.1e-05 | 0.0014 |
| 1000 um | 30 | 1.78e-11 | 1.16e-09 | 1.55e-08 | 0.0012 | 0.075 |
| 1000 um | 100 | 1.98e-10 | 1.29e-08 | 1.55e-08 | 0.013 | 0.83 |
| 300 um | 30 | 4.77e-12 | 3.00e-10 | 1.31e-09 | 0.0036 | 0.23 |
| 300 um | 100 | 5.30e-11 | 3.33e-09 | 1.31e-09 | 0.04 | 2.5 |
| 100 um | 30 | 1.41e-12 | 8.57e-11 | 4.08e-10 | 0.0035 | 0.21 |
| 100 um | 100 | 1.57e-11 | 9.52e-10 | 4.08e-10 | 0.038 | 2.3 |
| 10 um | 30 | 1.04e-13 | 5.57e-12 | 4.07e-11 | 0.0026 | 0.14 |
| 10 um | 100 | 1.16e-12 | 6.19e-11 | 4.07e-11 | 0.028 | 1.5 |

Kill parameter: torque at large opening angle. Rigid zipping cannot start a 90 deg fold against adhesion at any size (<1e-1 margin); it works only for the last ~10 deg (closing/latching) or with compliant curved electrodes.

## 2. Gap-closing electrostatic inchworm with ratchet pawls on a neighbour's rack

Force density 1.38-1.8 mN/mm^2 at 100-110 V (Penskiy/Contreras, SNIPPET), ~V^2 scaling; actuator footprint 20 % of one face.

| L | F at 100 V | F at 30 V | resistance (adhesion) | margin @30 V |
|---|---|---|---|---|
| 10000 um | 3e+04 uN | 2.7e+03 uN | 4.1 uN | 6.6e+02 |
| 1000 um | 300 uN | 27 uN | 4.1 uN | 6.6 |
| 300 um | 27 uN | 2.43 uN | 4.1 uN | 0.6 |
| 100 um | 3 uN | 0.27 uN | 4.1 uN | 0.066 |
| 10 um | 0.03 uN | 0.0027 uN | 4.1 uN | 0.00066 |

Kill parameter: force density x footprint vs adhesion -> inchworms fail below ~300 um at CMOS-like voltages; need ~100 V. Strength advantage: pawls on rack teeth carry shear by tooth strength (no slip planes).

## 3. Electrothermal (chevron/bimorph) - energy and swarm heat

Force per power ~10 mN/W (50 mN at 4.75 W chevron, SNIPPET; optimistic for scaling). Required force 3x adhesion; 10 ms per step.

| L | power per actuator | energy per step | swarm heat, 1 % of 1e7 modules moving |
|---|---|---|---|
| 10000 um | 2.29e+03 mW | 2.29e+04 uJ | 2.29e+05 W |
| 1000 um | 3.51 mW | 35.1 uJ | 351 W |
| 300 um | 1.28 mW | 12.8 uJ | 128 W |
| 100 um | 1.22 mW | 12.2 uJ | 122 W |
| 10 um | 1.22 mW | 12.2 uJ | 122 W |

Kill parameter: energy per step (~1e3x electrostatic). 1 % duty of a 1e7 swarm dissipates ~1 W - feasible only for small swarms or rare moves.

## 4. Piezoelectric thin film (AlN) stepping

Stroke ~1.3 um at +-60 V (SNIPPET); stepping a lattice pitch L needs L/1.3um strokes, each requiring clamp/release.

- L = 10000 um: 7692 strokes per lattice step
- L = 1000 um: 769 strokes per lattice step
- L = 300 um: 231 strokes per lattice step
- L = 100 um: 77 strokes per lattice step
- L = 10 um: 8 strokes per lattice step

Kill parameter: stroke per volt (needs a clutch/ratchet; adds the inchworm's clamp problem). Kept only as a clutch actuator candidate.

## 5. Capillary / microfluidic actuation and bonding

- L = 10000 um: meniscus of 0.1 L evaporates in ~2 s at 50 % RH (order-of-magnitude, diffusion-limited)
- L = 1000 um: meniscus of 0.1 L evaporates in ~0.02 s at 50 % RH (order-of-magnitude, diffusion-limited)
- L = 300 um: meniscus of 0.1 L evaporates in ~0.0018 s at 50 % RH (order-of-magnitude, diffusion-limited)
- L = 100 um: meniscus of 0.1 L evaporates in ~0.0002 s at 50 % RH (order-of-magnitude, diffusion-limited)
- L = 10 um: meniscus of 0.1 L evaporates in ~2e-06 s at 50 % RH (order-of-magnitude, diffusion-limited)

Kill parameter: liquid retention in ordinary air (seconds or less at <= 100 um). Rejected outside sealed/liquid environments.

## 6. Shape-memory alloy films

Work density high (>=5e6 J/m^3, SNIPPET) but cycle time thermally limited (20-300 Hz in films) and efficiency low; shares the electrothermal energy problem. Kept only as a one-shot or rare-event latch actuator.

