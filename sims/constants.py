"""Physical constants and baseline material parameters (SI units).

Every parameter carries a provenance tag:
  STD   - textbook physical constant / handbook material value
  ASSUM - modelling assumption chosen by us (vary it in sensitivity runs)
"""
EPS0 = 8.8541878128e-12      # F/m            STD
MU0 = 1.25663706212e-6       # H/m            STD
G = 9.81                     # m/s^2          STD
RHO_SI = 2330.0              # kg/m^3         STD (silicon)
RHO_AU = 2.2e-8              # ohm*m          STD (bulk gold resistivity, 20 C)
RHO_AL = 2.7e-8              # ohm*m          STD
GAMMA_WATER = 0.072          # N/m            STD
HAMAKER_SI = 1.0e-19         # J              STD order of magnitude (Si/SiO2 ~0.7-2e-19)
D0_VDW = 0.4e-9              # m              STD (vdW cutoff separation)

SIZES = {"10 mm": 10e-3, "1 mm": 1e-3, "100 um": 100e-6, "10 um": 10e-6}
