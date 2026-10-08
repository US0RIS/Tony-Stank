"""SESSION 4. 2D finite-difference magnetostatics of a NEPL pivot with real EPM face geometry.

Formulation (NUMERICAL SIMULATION): scalar potential psi, H = -grad psi,
  div( mu grad psi ) = div( mu0 M )      (B = mu H + mu0 M; M = remanent magnetisation)
on a node grid with cell-centred materials (4x4 supersampled rasterisation, so rotated
parts are anti-aliased). psi = 0 on the outer boundary. Force/torque on the mover from the
Maxwell stress tensor integrated on a closed contour in the air gap surrounding the mover.
Linear soft iron (mu_r = 1000); saturation and irreversible demagnetisation are CHECKED
post hoc (|B| in iron vs B_sat; reverse H in magnets vs Hc), not modelled.

2D model: everything is uniform along the pivot axis (depth). Results are per metre of depth
and are multiplied by an effective depth chosen by the caller (see MAGNETIC_CIRCUIT.md for the
3D correction bound).
"""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

MU0 = 4e-7 * math.pi

class Part:
    """Rectangle in module-local coordinates (metres): [x0,x1]x[y0,y1].
    kind: 'iron' or 'mag' (with magnetisation vector m (A/m) in local frame, recoil mu_r) ."""
    def __init__(self, x0, x1, y0, y1, kind, m=(0.0, 0.0), mur=1.0):
        self.b = (x0, x1, y0, y1); self.kind = kind; self.m = m; self.mur = mur

def place(parts, origin, ang, pivot):
    """Module placed with local origin at `origin` (lower-left corner), then rotated by `ang`
    (counter-clockwise positive) about `pivot`. Returns list of (part, transform)."""
    return [(p, origin, ang, pivot) for p in parts]

def rasterize(placed, xs, ys, ss=4):
    """Return mu (relative) and Mx, My arrays on cells (ny, nx)."""
    nx, ny = len(xs) - 1, len(ys) - 1
    h = xs[1] - xs[0]
    mu = np.ones((ny, nx)); Mx = np.zeros((ny, nx)); My = np.zeros((ny, nx))
    off = (np.arange(ss) + 0.5) / ss
    for part, origin, ang, pivot in placed:
        x0, x1, y0, y1 = part.b
        ca, sa = math.cos(ang), math.sin(ang)
        # corners in world coordinates to get bounding box
        cs = []
        for (px, py) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            wx, wy = px + origin[0], py + origin[1]
            dx, dy = wx - pivot[0], wy - pivot[1]
            cs.append((pivot[0] + ca * dx - sa * dy, pivot[1] + sa * dx + ca * dy))
        bx0 = min(c[0] for c in cs); bx1 = max(c[0] for c in cs)
        by0 = min(c[1] for c in cs); by1 = max(c[1] for c in cs)
        i0 = max(0, int((bx0 - xs[0]) / h) - 1); i1 = min(nx, int((bx1 - xs[0]) / h) + 2)
        j0 = max(0, int((by0 - ys[0]) / h) - 1); j1 = min(ny, int((by1 - ys[0]) / h) + 2)
        if i1 <= i0 or j1 <= j0: continue
        I, J = np.meshgrid(np.arange(i0, i1), np.arange(j0, j1))
        frac = np.zeros(I.shape)
        for a in off:
            for b in off:
                wx = xs[0] + (I + a) * h; wy = ys[0] + (J + b) * h
                dx, dy = wx - pivot[0], wy - pivot[1]
                lx = pivot[0] + ca * dx + sa * dy - origin[0]   # inverse rotation
                ly = pivot[1] - sa * dx + ca * dy - origin[1]
                frac += ((lx >= x0) & (lx <= x1) & (ly >= y0) & (ly <= y1))
        frac /= ss * ss
        sl = (slice(j0, j1), slice(i0, i1))
        if part.kind == "iron":
            mu[sl] = np.maximum(mu[sl], 1.0 + frac * 999.0)          # harmonic mixing ignored (iron fraction-weighted)
        else:
            mu[sl] = np.where(frac > 0, 1.0 + frac * (part.mur - 1.0), mu[sl])
            mx = ca * part.m[0] - sa * part.m[1]; my = sa * part.m[0] + ca * part.m[1]
            Mx[sl] += frac * mx; My[sl] += frac * my
    return mu, Mx, My

def solve(xs, ys, mu, Mx, My):
    """Nodes (ny+1, nx+1); interior unknowns; psi = 0 on boundary."""
    nx, ny = len(xs) - 1, len(ys) - 1
    h = xs[1] - xs[0]
    NX, NY = nx + 1, ny + 1
    idx = -np.ones((NY, NX), dtype=np.int64)
    inner = np.zeros((NY, NX), bool); inner[1:-1, 1:-1] = True
    idx[inner] = np.arange(inner.sum())
    # edge coefficients: x-edge between node (j,i) and (j,i+1) is adjacent to cells (j-1,i) and (j,i)
    mup = np.pad(mu, 1, mode="edge"); Mxp = np.pad(Mx, 1, mode="edge"); Myp = np.pad(My, 1, mode="edge")
    # for node (j,i): cells (j-1,i-1),(j-1,i),(j,i-1),(j,i) -> padded indices +1
    ex_mu = 0.5 * (mup[0:NY, 1:NX] + mup[1:NY + 1, 1:NX])        # x-edge (j, i->i+1): shape (NY, NX-1)
    ex_M = 0.5 * (Mxp[0:NY, 1:NX] + Mxp[1:NY + 1, 1:NX])
    ey_mu = 0.5 * (mup[1:NY, 0:NX] + mup[1:NY, 1:NX + 1])        # y-edge (j->j+1, i): shape (NY-1, NX)
    ey_M = 0.5 * (Myp[1:NY, 0:NX] + Myp[1:NY, 1:NX + 1])
    rows, cols, vals = [], [], []
    rhs = np.zeros(inner.sum())
    J, I = np.where(inner)
    r = idx[J, I]
    diag = np.zeros(len(r))
    # flux balance: sum over edges of [ mu (psi_nb - psi)/h^2 ] = sum of div(M) terms
    for (dj, di, coef, Mterm, sign) in (
        (0, 1, ex_mu[J, I], ex_M[J, I], +1), (0, -1, ex_mu[J, I - 1], ex_M[J, I - 1], -1),
        (1, 0, ey_mu[J, I], ey_M[J, I], +1), (-1, 0, ey_mu[J - 1, I], ey_M[J - 1, I], -1)):
        nb = idx[J + dj, I + di]
        diag -= coef
        m = nb >= 0
        rows.append(r[m]); cols.append(nb[m]); vals.append(coef[m])
        # div(M) source: flux mu0 M through edge in outward direction: B_out = -mu dpsi/dn + mu0 M_n
        rhs += sign * Mterm * h          # (mu0 cancels: equation divided by mu0)
    rows.append(r); cols.append(r); vals.append(diag)
    A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(len(r), len(r)))
    sol = spla.spsolve(A.tocsc(), rhs)
    psi = np.zeros((NY, NX)); psi[inner] = sol
    return psi

def fields(psi, h):
    Hx = np.zeros_like(psi); Hy = np.zeros_like(psi)
    Hx[:, 1:-1] = -(psi[:, 2:] - psi[:, :-2]) / (2 * h)
    Hy[1:-1, :] = -(psi[2:, :] - psi[:-2, :]) / (2 * h)
    return Hx, Hy

def bilinear(F, xs, ys, x, y):
    h = xs[1] - xs[0]
    fx = (x - xs[0]) / h; fy = (y - ys[0]) / h
    i = np.clip(np.floor(fx).astype(int), 0, F.shape[1] - 2); j = np.clip(np.floor(fy).astype(int), 0, F.shape[0] - 2)
    tx = fx - i; ty = fy - j
    return (F[j, i] * (1 - tx) * (1 - ty) + F[j, i + 1] * tx * (1 - ty) + F[j + 1, i] * (1 - tx) * ty + F[j + 1, i + 1] * tx * ty)

def stress_force(Hx, Hy, xs, ys, poly, pivot, npts=4000):
    """Maxwell stress on closed polygon (counter-clockwise, outward normal to the right of travel
    reversed). Returns Fx, Fy (per unit depth) and torque about pivot (per unit depth)."""
    P = np.array(poly + [poly[0]])
    seg = np.diff(P, axis=0); segL = np.hypot(seg[:, 0], seg[:, 1])
    tot = segL.sum()
    Fx = Fy = T = 0.0
    for k in range(len(seg)):
        n = max(8, int(npts * segL[k] / tot))
        t = (np.arange(n) + 0.5) / n
        x = P[k, 0] + t * seg[k, 0]; y = P[k, 1] + t * seg[k, 1]
        dl = segL[k] / n
        nxv, nyv = seg[k, 1] / segL[k], -seg[k, 0] / segL[k]   # outward normal for CCW polygon
        hx = bilinear(Hx, xs, ys, x, y); hy = bilinear(Hy, xs, ys, x, y)
        tx = MU0 * (hx * (hx * nxv + hy * nyv) - 0.5 * (hx**2 + hy**2) * nxv)
        ty = MU0 * (hy * (hx * nxv + hy * nyv) - 0.5 * (hx**2 + hy**2) * nyv)
        Fx += (tx * dl).sum(); Fy += (ty * dl).sum()
        T += (((x - pivot[0]) * ty - (y - pivot[1]) * tx) * dl).sum()
    return Fx, Fy, T
