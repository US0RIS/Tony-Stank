# S3 power distribution through contact lattices (SIMULATED + DERIVED)

Baseline: R_contact=10.0 ohm, P_module=1.0 uW, V_bus=3.0 V, I=0.333 uA

## 1. Validation: vertical chain vs analytic

- h=10: simulated top drop 1.833333e-04 V, formula 1.833333e-04 V
- h=100: simulated top drop 1.683333e-02 V, formula 1.683333e-02 V
- h=1000: simulated top drop 1.668333e+00 V, formula 1.668333e+00 V

## 2. Does lateral parallelism help? Uniform tower w x w x h on the garment

| w | h | max drop (V) | chain formula (V) |
|---|---|---|---|
| 1 | 100 | 1.6833e-02 | 1.6833e-02 |
| 5 | 100 | 1.6833e-02 | 1.6833e-02 |
| 20 | 100 | 1.6833e-02 | 1.6833e-02 |

Result: for uniform load on a ground plane, columns are electrically independent: drop depends on height in hops only.

## 3. Horizontal arm fed through a narrow root (current funnelling)

Arm cross-section a x a, length Lh, attached to a garment patch only at its root column.

| a | arm length (hops) | max drop (V) | chain formula for same hop count (V) | ratio |
|---|---|---|---|---|
| 1 | 200 | 6.7000e-02 | 6.7000e-02 | 1.000 |
| 4 | 200 | 6.7000e-02 | 6.7000e-02 | 1.000 |
| 10 | 200 | 6.7000e-02 | 6.7000e-02 | 1.000 |

A root-fed prismatic arm behaves like a single chain of the same length (cross-section cancels: a^2 more current, a^2 more paths).

## 4. Electrical reach h_max (hops) for drop <= 10 % of V_bus: h_max ~ sqrt(0.2 V^2 / (P R))

| R_contact (ohm) | P (W) | V_bus (V) | h_max (hops) | reach @100 um | reach @10 um |
|---|---|---|---|---|---|
| 1 | 1e-08 | 3 | 13416 | 134.16 cm | 13.416 cm |
| 1 | 1e-08 | 30 | 134164 | 1341.64 cm | 134.164 cm |
| 1 | 1e-06 | 3 | 1342 | 13.42 cm | 1.342 cm |
| 1 | 1e-06 | 30 | 13416 | 134.16 cm | 13.416 cm |
| 1 | 1e-05 | 3 | 424 | 4.24 cm | 0.424 cm |
| 1 | 1e-05 | 30 | 4243 | 42.43 cm | 4.243 cm |
| 100 | 1e-08 | 3 | 1342 | 13.42 cm | 1.342 cm |
| 100 | 1e-08 | 30 | 13416 | 134.16 cm | 13.416 cm |
| 100 | 1e-06 | 3 | 134 | 1.34 cm | 0.134 cm |
| 100 | 1e-06 | 30 | 1342 | 13.42 cm | 1.342 cm |
| 100 | 1e-05 | 3 | 42 | 0.42 cm | 0.042 cm |
| 100 | 1e-05 | 30 | 424 | 4.24 cm | 0.424 cm |
| 10000 | 1e-08 | 3 | 134 | 1.34 cm | 0.134 cm |
| 10000 | 1e-08 | 30 | 1342 | 13.42 cm | 1.342 cm |
| 10000 | 1e-06 | 3 | 13 | 0.13 cm | 0.013 cm |
| 10000 | 1e-06 | 30 | 134 | 1.34 cm | 0.134 cm |
| 10000 | 1e-05 | 3 | 4 | 0.04 cm | 0.004 cm |
| 10000 | 1e-05 | 30 | 42 | 0.42 cm | 0.042 cm |

## 5. Capacitive face coupling as the 'contact'

- L=100 um, gap=100 nm, f=10 MHz: C=0.133 pF, |Z|=119837 ohm
- L=100 um, gap=100 nm, f=100 MHz: C=0.133 pF, |Z|=11984 ohm
- L=100 um, gap=1000 nm, f=10 MHz: C=0.013 pF, |Z|=1198366 ohm
- L=100 um, gap=1000 nm, f=100 MHz: C=0.013 pF, |Z|=119837 ohm
- L=1000 um, gap=1000 nm, f=10 MHz: C=1.328 pF, |Z|=11984 ohm
- L=1000 um, gap=1000 nm, f=100 MHz: C=1.328 pF, |Z|=1198 ohm

## 6. Hold-up energy for loss of contact (trench capacitor 57.8 nF/mm^2, VERIFIED snippet; area = one face)

- L=1000 um: C=57.8 nF, usable E(3V->2V)=144 nJ, ride-through @1 uW=145 ms, @10 nW=14.4 s
- L=100 um: C=0.578 nF, usable E(3V->2V)=1.45 nJ, ride-through @1 uW=1.45 ms, @10 nW=0.145 s
- L=10 um: C=0.00578 nF, usable E(3V->2V)=0.0145 nJ, ride-through @1 uW=0.0145 ms, @10 nW=0.00145 s

## 7. Swarm power budget (battery 15 Wh, ~phone class)

| volume | L | N modules | P/module | total P | battery life |
|---|---|---|---|---|---|
| 1 cm^3 | 1000 um | 1.0e+03 | 1e-08 W | 1e-05 W | 1.5e+06 h |
| 1 cm^3 | 1000 um | 1.0e+03 | 1e-06 W | 0.001 W | 1.5e+04 h |
| 1 cm^3 | 100 um | 1.0e+06 | 1e-08 W | 0.01 W | 1.5e+03 h |
| 1 cm^3 | 100 um | 1.0e+06 | 1e-06 W | 1 W | 15 h |
| 1 cm^3 | 10 um | 1.0e+09 | 1e-08 W | 10 W | 1.5 h |
| 1 cm^3 | 10 um | 1.0e+09 | 1e-06 W | 1e+03 W | 0.015 h |
| 10 cm^3 | 1000 um | 1.0e+04 | 1e-08 W | 0.0001 W | 1.5e+05 h |
| 10 cm^3 | 1000 um | 1.0e+04 | 1e-06 W | 0.01 W | 1.5e+03 h |
| 10 cm^3 | 100 um | 1.0e+07 | 1e-08 W | 0.1 W | 150 h |
| 10 cm^3 | 100 um | 1.0e+07 | 1e-06 W | 10 W | 1.5 h |
| 10 cm^3 | 10 um | 1.0e+10 | 1e-08 W | 100 W | 0.15 h |
| 10 cm^3 | 10 um | 1.0e+10 | 1e-06 W | 1e+04 W | 0.0015 h |
| 100 cm^3 | 1000 um | 1.0e+05 | 1e-08 W | 0.001 W | 1.5e+04 h |
| 100 cm^3 | 1000 um | 1.0e+05 | 1e-06 W | 0.1 W | 150 h |
| 100 cm^3 | 100 um | 1.0e+08 | 1e-08 W | 1 W | 15 h |
| 100 cm^3 | 100 um | 1.0e+08 | 1e-06 W | 100 W | 0.15 h |
| 100 cm^3 | 10 um | 1.0e+11 | 1e-08 W | 1e+03 W | 0.015 h |
| 100 cm^3 | 10 um | 1.0e+11 | 1e-06 W | 1e+05 W | 0.00015 h |
