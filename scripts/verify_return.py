"""Independent reproduction of warp-shift-computation.md claims.

NOTE (17 Oct 2026, labels only, physics untouched): the "claims" quoted in the
section headers below are session-one numbers in the t1*t2=1 convention.  This
script uses t2=1.  The two agree by the 1/t2^2 gauge factor (x2) only for w <~ 0.02;
above that the raw-w numbers diverge nonperturbatively (see paper 2, Appendix A).
The bubble-wall numbers depend on wall geometry; the quoted 70x was later
corrected to 85x (session one) / 72x (this convention), see warp-shift-computation.md.
Odd chain, 201 sites (100 cells + 1), power-law curved-SSH profile,
r = t1/t2 = 0.5, sigma = 0.5, eta = 1e-3 broadening, exact diagonalization
and direct linear solve for edge LDOS. Written from scratch; no access to
the original scripts (tilt_cost*.py, bubble.py).
"""
import numpy as np

NS = 201            # sites (odd)
NC = 100            # full cells
T1, T2 = 0.5, 1.0   # r = 0.5, topological
ETA = 1e-3

def build_H(sigma=0.5, w=None, tprime=0.0, nn_disorder=None):
    """w: None, scalar (uniform imaginary NNN), or array over NNN bonds i=0..NS-3
       (bond i connects sites i and i+2, amplitude evaluated per bond).
       nn_disorder: multiplicative array over NN bonds (len NS-1)."""
    H = np.zeros((NS, NS), dtype=complex)
    # NN SSH bonds with power-law profile
    tb = np.zeros(NS - 1)
    for m in range(1, NC + 1):
        x1 = (2 * m - 1) / (2 * NC - 1)
        x2 = (2 * m) / (2 * NC - 1)
        tb[2 * m - 2] = T1 * x1**sigma          # intra-cell bond (2m-1)-(2m)
        if 2 * m - 1 < NS - 1:
            tb[2 * m - 1] = T2 * x2**sigma      # inter-cell bond (2m)-(2m+1)
    if nn_disorder is not None:
        tb = tb * nn_disorder
    for i in range(NS - 1):
        H[i, i + 1] = tb[i]
        H[i + 1, i] = tb[i]
    # real NNN (the naive/dangerous term)
    if tprime != 0.0:
        for i in range(NS - 2):
            H[i, i + 2] += tprime
            H[i + 2, i] += tprime
    # imaginary (current-like) NNN: i*w (c^dag_{n+2} c_n - h.c.)
    if w is not None:
        warr = np.full(NS - 2, w) if np.isscalar(w) else np.asarray(w)
        for i in range(NS - 2):
            H[i + 2, i] += 1j * warr[i]
            H[i, i + 2] += -1j * warr[i]
    return H

def E0_and_mode(H):
    ev, vec = np.linalg.eigh(H)
    k = np.argmin(np.abs(ev))
    return ev[k], vec[:, k], ev

def pairing_deviation(ev):
    s = np.sort(ev)
    return np.max(np.abs(s + s[::-1]))

def rho_edge(H, E=0.0, eta=ETA):
    A = (E + 1j * eta) * np.eye(NS) - H
    e1 = np.zeros(NS, dtype=complex); e1[0] = 1.0
    g00 = np.linalg.solve(A, e1)[0]
    return -g00.imag / np.pi

def lnrho(sigma=0.5, w=None, tprime=0.0, nn_disorder=None):
    return np.log(rho_edge(build_H(sigma, w, tprime, nn_disorder)))

print("=" * 72)
print("A. NAIVE REAL NNN: linear unpinning  (claim: E0 = -0.73 t', linear)")
for tp in [1e-4, 1e-3, 1e-2, 1e-1]:
    e0, _, _ = E0_and_mode(build_H(0.5, None, tp))
    print(f"  t'={tp:8.0e}   E0={e0:+.6e}   E0/t'={e0/tp:+.4f}")

print("=" * 72)
print("B. IMAGINARY NNN: pinning + pairing  (claim: |E0|<=1e-17, pairing ~1e-15 at w=0.1)")
for w in [0.02, 0.05, 0.1]:
    e0, _, ev = E0_and_mode(build_H(0.5, w))
    print(f"  w={w:4.2f}   |E0|={abs(e0):.2e}   max pairing dev={pairing_deviation(ev):.2e}")

print("=" * 72)
print("C. DISORDER, 200 realizations, 1% NN hopping disorder")
rng = np.random.default_rng(7)
e_im, e_re = [], []
for _ in range(200):
    dis = 1.0 + 0.01 * rng.standard_normal(NS - 1)
    e0i, _, _ = E0_and_mode(build_H(0.5, 0.1, 0.0, dis))
    e0r, _, _ = E0_and_mode(build_H(0.5, None, 0.02, dis))
    e_im.append(abs(e0i)); e_re.append(abs(e0r))
print(f"  imaginary w=0.10 : median |E0| = {np.median(e_im):.2e}   (claim ~5e-17)")
print(f"  real     t'=0.02: median |E0| = {np.median(e_re):.2e}   (claim ~1.5e-2)")

print("=" * 72)
print("D. MODE RESHAPING  (claims at w=0 -> 0.1: pol 1.00->0.49,")
print("   footprint 1.3->3.6 cells, edge weight 0.87->0.25)")
for w in [None, 0.02, 0.05, 0.1]:
    e0, psi, _ = E0_and_mode(build_H(0.5, w))
    p = np.abs(psi) ** 2
    polA = p[0::2].sum() - p[1::2].sum()
    pc = np.array([p[2 * m] + (p[2 * m + 1] if 2 * m + 1 < NS else 0.0)
                   for m in range(0, (NS + 1) // 2)])
    prc = (pc.sum() ** 2) / (pc ** 2).sum()
    wl = 0.0 if w is None else w
    print(f"  w={wl:4.2f}  pol={polA:+.3f}  footprint(cells,PR)={prc:5.2f}  |psi(1)|^2={p[0]:.3f}")

print("=" * 72)
print("E. SHIFT RESPONSIVITY d ln rho / dw  (session-one, t1t2=1: -0.9,-1.9,-6.6,-22; x2 gauge factor applies only for w<~0.02)")
dw = 1e-4
for w in [0.01, 0.02, 0.05, 0.08]:
    d = (lnrho(0.5, w + dw) - lnrho(0.5, w - dw)) / (2 * dw)
    print(f"  w={w:4.2f}   d ln rho/dw = {d:+.3f}")

print("=" * 72)
print("F. CROSS-TALK d ln rho / dsigma at sigma=0.5 (session-one, t1t2=1: +0.20, +0.03, -7.3; conventions diverge above w~0.02)")
ds = 1e-4
for w in [None, 0.02, 0.08]:
    d = (lnrho(0.5 + ds, w) - lnrho(0.5 - ds, w)) / (2 * ds)
    wl = 0.0 if w is None else w
    print(f"  w={wl:4.2f}   d ln rho/dsigma = {d:+.4f}")

print("=" * 72)
print("G. BUBBLE-WALL RUN  (top-hat, tanh walls; half-width 5 cells=10 sites, s=3 sites)")

def bubble(w0, center_cell, half_cells=5, s_sites=3.0):
    xc = 2.0 * center_cell          # site coordinate of center
    xL, xR = xc - 2 * half_cells, xc + 2 * half_cells
    x = np.arange(NS - 2) + 1.0     # NNN bond midpoints
    return 0.5 * w0 * (np.tanh((x - xL) / s_sites) - np.tanh((x - xR) / s_sites))

base_w = lnrho(0.5, None); base_f = lnrho(0.0, None)

e0b, _, evb = E0_and_mode(build_H(0.5, bubble(0.02, 20)))
print(f"  G1 pinning under full bubble: |E0|={abs(e0b):.2e}, pairing={pairing_deviation(evb):.2e}")

Rp = lnrho(0.5, bubble(0.02, 5)) - base_w
Rm = lnrho(0.5, bubble(-0.02, 5)) - base_w
print(f"  G2 evenness: R(+w0)={Rp:+.6e}  R(-w0)={Rm:+.6e}  diff={abs(Rp-Rm):.1e}")
print("     quadratic scaling (warped chain, center cell 5):")
prev = None
for w0 in [0.005, 0.01, 0.02, 0.04]:
    R = lnrho(0.5, bubble(w0, 5)) - base_w
    print(f"       w0={w0:5.3f}  R={R:+.4e}" + ("" if prev is None else f"   ratio={R/prev:5.2f}"))
    prev = R

print("  G3 blindness vs center (warped, w0=0.02; claim ~2e-4@5c ... exact 0 by 30c):")
for c in [5, 10, 15, 20, 30, 50]:
    R = lnrho(0.5, bubble(0.02, c)) - base_w
    print(f"       center cell {c:3d}   |R| = {abs(R):.2e}")

Rf = lnrho(0.0, bubble(0.02, 5)) - base_f
Rw = lnrho(0.5, bubble(0.02, 5)) - base_w
print(f"  G4 preamplification: flat R={Rf:+.3e}  warped R={Rw:+.3e}  ratio={Rw/Rf:6.1f}x")
print("     (session-one: flat -1.7e-4, warped -1.44e-2, 85x; this convention 72x; geometry-dependent)")

x = np.arange(NS - 2) + 1.0
w0 = 0.02; c = 20; h = 5; s = 3.0
xc = 2.0 * c; xL, xR = xc - 2 * h, xc + 2 * h
up = 0.5 * w0 * (1 + np.tanh((x - xL) / s))
dn = 0.5 * w0 * (1 - np.tanh((x - xR) / s))
Ru = lnrho(0.0, up) - base_f
Rd = lnrho(0.0, dn) - base_f
Runi = lnrho(0.0, np.full(NS - 2, w0)) - base_f
Rbub = lnrho(0.0, up + dn - w0) - base_f
print(f"  G5 wall decomposition (flat): R_up+R_dn={Ru+Rd:+.5e}  R_uni+R_bub={Runi+Rbub:+.5e}")

print("=" * 72)
print("H. DETECTABILITY: warped, near-edge bubble w0=0.02 as fractional power change")
print(f"   |d ln rho| = {abs(Rw):.3e}  ->  x 3.3 aW = {abs(Rw)*3.3e-18*1e21:.1f} zW")
print("   (claim: 1.4% -> ~47 zW -> SNR ~16 at 100 s vs 30 zW/rtHz)")
