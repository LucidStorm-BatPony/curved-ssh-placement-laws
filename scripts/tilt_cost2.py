"""Why the shift encoding keeps E0 pinned: the antiunitary chiral symmetry S o K
(paper 2, section 2).  S flips the sign of the real NN terms, K flips the sign
of the imaginary NNN term, so (S o K) H (S o K)^-1 = -H.  Verified by exact
+/-E pairing of the whole spectrum at w=0.1 with 1% disorder (expected ~1e-15),
and by the mode's reshaping under w (polarization, footprint, edge weight).
"""
import numpy as np
from ssh_common import bonds, hamiltonian, zero_mode, pairing_residual

Nc = 100
tb = bonds(Nc, 0.5, 0.5)
ns = len(tb) + 1
rng = np.random.default_rng(3)
H = hamiltonian(tb, warr=np.full(ns - 2, 0.1), dis=0.01, rng=rng)
print(f"+/-E pairing residual at w=0.1, 1% disorder: {pairing_residual(H):.3e}  (0 = exact antiunitary chiral)")

print(f"\n{'w':>6} {'|E0|':>10} {'A-weight':>10} {'IPR (cells)':>12} {'|psi(1)|^2':>11}")
for w in [0.0, 0.02, 0.05, 0.10]:
    E, v = zero_mode(hamiltonian(tb, warr=np.full(ns - 2, w)))
    p = np.abs(v) ** 2
    print(f"{w:6.2f} {abs(E):10.2e} {np.sum(p[0::2]):10.4f} {1.0/np.sum(p**2):12.2f} {p[0]:11.4f}")
