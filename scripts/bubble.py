"""Bubble-wall run (paper 2, sections 4-5): position-dependent shift w(x) --
a 1+1 Alcubierre-style top-hat with tanh walls, flat inside and outside.

Tests (flat chain r=0.5 primary; warped sigma=0.5 cross-check), all odd, 201 sites:
  0. pinning + spectral pairing with a full bubble present     (expect ~1e-16)
  1. blindness curve: edge response vs bubble centre            (expect machine zero by cell 30)
  2. evenness: response quadratic in w0                          (slope 2 per doubling)
  3. curvature preamplification: warped/flat response ratio     (expect ~70x)
  4. detectability with the companion paper's hardware          (expect SNR ~16 at 100 s)
"""
import numpy as np
from ssh_common import bonds, hamiltonian, zero_mode, pairing_residual, ldos

Nc = 100
ns = 2 * Nc + 1


def bubble(center, width=20.0, w0=0.02, steep=0.5):
    x = np.arange(ns - 2) / 2.0
    return w0 / 2 * (np.tanh(steep * (x - (center - width / 2))) - np.tanh(steep * (x - (center + width / 2))))


def resp(prof, sig=0.0):
    tb = bonds(Nc, sig, 0.5)
    return np.log(ldos(hamiltonian(tb, warr=prof))) - np.log(ldos(hamiltonian(tb)))


tb0 = bonds(Nc, 0.0, 0.5)
H = hamiltonian(tb0, warr=bubble(50))
E, _ = zero_mode(H)
print(f"bubble mid-chain: |E0|={abs(E):.2e}  +/-E pairing residual={pairing_residual(H):.2e}")

print(f"\n{'bubble center (cell)':>20} {'|d ln rho| (flat)':>18}")
for c in [5, 10, 15, 20, 30, 50, 80]:
    print(f"{c:>20} {abs(resp(bubble(c))):18.3e}")

print(f"\n{'w0':>8} {'d ln rho (bubble at cell 8)':>28}")
for w0 in [0.005, 0.01, 0.02, 0.04, 0.08]:
    print(f"{w0:8.3f} {resp(bubble(8, w0=w0)):+28.4e}")

flat, warped = resp(bubble(8)), resp(bubble(8), sig=0.5)
print(f"\nnear-edge bubble w0=0.02: flat {flat:+.3e}   warped {warped:+.3e}   preamplification {warped/flat:.1f}x")
print(f"warped chain, bubble mid-chain (cell 50): {resp(bubble(50), sig=0.5):+.3e}")

P, NEP, tau = 3.3e-18, 30e-21, 100.0
dP = abs(warped) * P
print(f"\ndetectability: dP = {dP*1e21:.1f} zW vs NEP {NEP*1e21:.0f} zW/sqrt(Hz) -> SNR = {dP*np.sqrt(tau)/NEP:.1f} at {tau:.0f} s")
