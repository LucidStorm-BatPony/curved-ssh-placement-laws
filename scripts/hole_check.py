"""Two robustness checks that closed audit holes (paper 1 appendix A; paper 2 section 6).

1. Near-critical responsivity curve d ln rho/d sigma vs r: stable across a 100x
   range of broadening and a doubling of chain length?  (expect yes, to a few %)
2. Disentangling the (sigma, w^2) channels: angle between the normalized response
   vectors of a flat and a warped element (expect tens of degrees) vs two elements
   differing only in shift bias (expect a fraction of a degree).  Raw condition
   numbers are convention-dependent and are not the quoted quantity.
"""
import numpy as np
from ssh_common import bonds, hamiltonian, ldos

print("CHECK 1: d ln rho/d sigma vs r -- eta and N robustness")
print(f"{'r':>6} {'N=250,e=1e-3':>13} {'N=250,e=1e-5':>13} {'N=500,e=1e-5':>13}")
ds = 1e-4
for r in [0.5, 0.8, 0.9, 0.95, 0.97]:
    row = []
    for Nc, eta in [(250, 1e-3), (250, 1e-5), (500, 1e-5)]:
        m = (np.log(ldos(hamiltonian(bonds(Nc, 0.5 + ds, r)), eta=eta))
             - np.log(ldos(hamiltonian(bonds(Nc, 0.5 - ds, r)), eta=eta))) / (2 * ds)
        row.append(m)
    print(f"{r:6.2f} {row[0]:+13.4f} {row[1]:+13.4f} {row[2]:+13.4f}")

print("\nCHECK 2: channel disentangling (angular, convention-invariant)")
Nc, eta, w0 = 100, 1e-3, 0.02
ns = 2 * Nc + 1


def respvec(sig, w):
    ds = 1e-4
    tb0 = bonds(Nc, sig, 0.5)
    wa = np.full(ns - 2, w)
    dsig = (np.log(ldos(hamiltonian(bonds(Nc, sig + ds, 0.5), warr=wa), eta=eta))
            - np.log(ldos(hamiltonian(bonds(Nc, sig - ds, 0.5), warr=wa), eta=eta))) / (2 * ds)
    dw2 = (w * 1.05) ** 2 - (w * 0.95) ** 2
    dw = (np.log(ldos(hamiltonian(tb0, warr=np.full(ns - 2, w * 1.05)), eta=eta))
          - np.log(ldos(hamiltonian(tb0, warr=np.full(ns - 2, w * 0.95)), eta=eta))) / dw2
    return np.array([dsig, dw])


def angle(u, v):
    return np.degrees(np.arccos(abs(u @ v) / np.linalg.norm(u) / np.linalg.norm(v)))


vF, vW, vW2 = respvec(0.0, w0), respvec(0.5, w0), respvec(0.5, 2 * w0)
print(f"  flat   element: dlnr/dsig={vF[0]:+.4f}  dlnr/dw2={vF[1]:+.3f}")
print(f"  warped element: dlnr/dsig={vW[0]:+.4f}  dlnr/dw2={vW[1]:+.3f}")
print(f"  curvature-bias pair (flat vs warped): angle = {angle(vF, vW):.1f} deg")
print(f"  shift-bias pair (w=0.02 vs 0.04, same sigma): angle = {angle(vW, vW2):.2f} deg")
