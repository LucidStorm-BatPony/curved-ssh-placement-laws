"""Numerical check of the shift placement-law derivation (paper 2, section 3).

The derivation's central claim: for one shift bond w on the A-A link between
cells m and m+1, the first-order correction to the zero mode is a SINGLE B-site
spike, psi_B(m) = i w a_{m+1} / t1(m), with every other B amplitude zero by
telescoping.  And the two faces of the law are equal:
    -a_{m+1}^2 / t1(m)^2  ==  -a_m^2 / t2(m)^2   (by the mode ratio).
Expected: spike at the predicted site, amplitude ratio 1.00000, neighbours ~1e-16.
"""
import numpy as np
from ssh_common import bonds, hamiltonian, zero_mode

Nc = 100
ns = 2 * Nc + 1
for sig in [0.0, 0.5]:
    tb = bonds(Nc, sig, 0.5)
    _, a = zero_mode(hamiltonian(tb))
    a = a.real
    w, b = 1e-4, 4                      # A-A bond sites 4-6: cells m=3 -> m+1=4
    warr = np.zeros(ns - 2)
    warr[b] = w
    _, psi = zero_mode(hamiltonian(tb, warr=warr))
    psi = psi / (psi[0] / abs(psi[0]))  # gauge: real edge amplitude
    leak = np.abs(psi[1::2])
    top = np.argsort(leak)[::-1][:3]
    pred = w * abs(a[b + 2]) / tb[b]
    print(f"sigma={sig}: top B-site at B-index {top[0]} (predict {b//2}) = {leak[top[0]]:.4e}  predicted {pred:.4e}  ratio {leak[top[0]]/pred:.5f}")
    print(f"   next two B sites: {leak[top[1]]:.2e}, {leak[top[2]]:.2e}")
    f1, f2 = a[b + 2] ** 2 / tb[b] ** 2, a[b] ** 2 / tb[b + 1] ** 2
    print(f"   -a_(m+1)^2/t1^2 = {-f1:.6e}   -a_m^2/t2^2 = {-f2:.6e}   (identical: {np.isclose(f1, f2)})")
