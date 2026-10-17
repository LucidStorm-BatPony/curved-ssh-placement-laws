"""Shared lattice builders for the curved-spacetime SSH verification scripts.

Convention (session one): t1 * t2 = 1, i.e. t1 = sqrt(r), t2 = 1/sqrt(r).
Power-law warping (Rajbongshi & Modak, arXiv:2504.16200):
    t1(n) = t1 * ((2n-1)/(2N-1))^sigma,   t2(n) = t2 * ((2n)/(2N-1))^sigma
Bond i (0-based, between sites i and i+1) carries x_i = (i+1)/(ns-1).

Odd chains (ns = 2*Nc+1) host exactly one zero mode on the A sublattice.
Even chains (ns = 2*Nc) host one near-zero mode per edge.
"""
import numpy as np


def bonds(Nc, sigma=0.5, r=0.5, odd=True):
    """Return the array of nearest-neighbour hoppings t[i] for bond i."""
    ns = 2 * Nc + 1 if odd else 2 * Nc
    tb = np.zeros(ns - 1)
    for i in range(ns - 1):
        t0 = np.sqrt(r) if i % 2 == 0 else 1 / np.sqrt(r)
        x = (i + 1) / (ns - 1)
        tb[i] = t0 * x ** sigma          # x in (0,1]; sigma=0 gives the flat chain exactly
    return tb


def hamiltonian(tb, warr=None, tp_real=0.0, dis=0.0, rng=None):
    """Chiral NN chain from bonds tb, optionally with:
       warr   -- per-bond imaginary NNN (current-like) shift coupling, i*w (c+_{n+2} c_n - h.c.)
       tp_real-- uniform real NNN hopping (the naive, chiral-breaking form)
       dis    -- fractional Gaussian disorder on NN bonds
    """
    ns = len(tb) + 1
    H = np.zeros((ns, ns), complex)
    t = tb.copy()
    if dis > 0:
        t = t * (1 + dis * rng.standard_normal(len(t)))
    for i in range(ns - 1):
        H[i, i + 1] = t[i]
        H[i + 1, i] = t[i]
    if warr is not None:
        for i in range(ns - 2):
            H[i, i + 2] += 1j * warr[i]
            H[i + 2, i] -= 1j * warr[i]
    if tp_real != 0.0:
        for i in range(ns - 2):
            H[i, i + 2] += tp_real
            H[i + 2, i] += tp_real
    return H


def ldos(H, site=0, eta=1e-3):
    """Local density of states at `site` and E=0 with Lorentzian broadening eta."""
    ns = H.shape[0]
    A = (1j * eta) * np.eye(ns) - H
    e = np.zeros(ns, complex)
    e[site] = 1.0
    return -np.linalg.solve(A, e)[site].imag / np.pi


def zero_mode(H):
    """Eigenvalue closest to zero and its eigenvector."""
    E, V = np.linalg.eigh(H)
    k = np.argmin(np.abs(E))
    return E[k], V[:, k]


def pairing_residual(H):
    """max |E_i + E_{-i}| over the sorted spectrum: 0 means exact +/-E pairing."""
    E = np.sort(np.linalg.eigvalsh(H))
    return np.max(np.abs(E + E[::-1]))
