# S5 structural reach (DERIVED)

## (a) single-file horizontal chain: reach = sqrt(p L / (3 rho g))

| bond strength p | L=10 mm | 1 mm | 100 um | 10 um |
|---|---|---|---|---|
| 6 kPa (Karagozler 2007 latch, VERIFIED) | 29.58 mm | 9.35 mm | 2.96 mm | 0.94 mm |
| 50 kPa (dry adhesive) | 85.39 mm | 27.00 mm | 8.54 mm | 2.70 mm |
| 400 kPa (B=1 T magnet) | 241.52 mm | 76.38 mm | 24.15 mm | 7.64 mm |
| 2 MPa (thin-film e-static clamp, DERIVED) | 540.06 mm | 170.78 mm | 54.01 mm | 17.08 mm |
| 100 MPa (Si interlock, DERIVED) | 3818.80 mm | 1207.61 mm | 381.88 mm | 120.76 mm |

Smaller modules -> shorter single-file reach (reach ~ sqrt(L)).

## (b) solid beam, packing phi=0.74: self-weight limit l_max = sqrt(p h / (3 phi rho g))

| p | h=1 mm | h=5 mm | h=10 mm | h=30 mm |
|---|---|---|---|---|
| 6 kPa | 1.1 cm | 2.4 cm | 3.4 cm | 6.0 cm |
| 50 kPa | 3.1 cm | 7.0 cm | 9.9 cm | 17.2 cm |
| 400 kPa | 8.9 cm | 19.9 cm | 28.1 cm | 48.6 cm |
| 2000 kPa | 19.9 cm | 44.4 cm | 62.8 cm | 108.7 cm |

## (c) bond strength needed to hold a payload at the tip (beam b = h)

| payload | arm length | section | required p |
|---|---|---|---|
| 1.0 N | 10 cm | 10 mm square | 600 kPa |
| 1.0 N | 10 cm | 20 mm square | 75 kPa |
| 10.0 N | 30 cm | 30 mm square | 667 kPa |
| 0.1 N | 10 cm | 5 mm square | 480 kPa |

## (d) stiffness of a preloaded electrostatic joint

The clamp pressure p preloads the standoff bumps. While applied tension < p the bumps stay compressed and the joint
is as stiff as the bumps: k_i ~ f_b E_Si / g. When tension exceeds p, the electrostatic force falls with gap
(negative stiffness -2p/g) and the joint snaps open: brittle, no warning. Design rule: working load << p.

- f_b=0.01, g=1000 nm: k_i=1.70e+15 Pa/m -> E_eff(L=100 um) = k_i L = 170 GPa (bump-limited upper bound)
- f_b=0.001, g=100 nm: k_i=1.70e+15 Pa/m -> E_eff(L=100 um) = k_i L = 170 GPa (bump-limited upper bound)
