"""Decimation recursion vs direct inversion (paper 1, section 3.1 / appendix A).

Warped even chain (N=250 cells) terminated in a semi-infinite uniform lead
(t_L = 1).  The surface Green's function at the far edge is computed two ways:
by folding the lead and chain site-by-site (O(N)), and by inverting the full
matrix with the lead self-energy on the last site.  Expected agreement ~1e-16.
"""
import numpy as np
from ssh_common import bonds

Nc, r, sig, eta, E = 250, 0.5, 0.5, 1e-7, 0.0
tb = bonds(Nc, sig, r, odd=False)
ns = len(tb) + 1
tL = 1.0
z = E + 1j * eta
g_lead = (z - 1j * np.sqrt(4 * tL * tL - z.real ** 2 + 0j)) / (2 * tL * tL)

# recursion from the lead inward
g, link = g_lead, tL
for i in range(ns - 1, 0, -1):
    g = 1.0 / (z - link * link * g)
    link = tb[i - 1]
g_rec = 1.0 / (z - link * link * g)

# direct inversion
H = np.zeros((ns, ns), complex)
for i in range(ns - 1):
    H[i, i + 1] = tb[i]
    H[i + 1, i] = tb[i]
H[ns - 1, ns - 1] += tL * tL * g_lead
G00 = np.linalg.inv(z * np.eye(ns) - H)[0, 0]

print(f"recursion G00 = {g_rec:.15e}")
print(f"direct    G00 = {G00:.15e}")
print(f"|diff|/|G00|  = {abs(g_rec - G00) / abs(G00):.2e}")
