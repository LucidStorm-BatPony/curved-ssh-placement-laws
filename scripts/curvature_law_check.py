"""Direct verification of the curvature placement law (paper 1, section 4.2):

    d ln rho_edge / d eps = -2 <Phi>,   Phi(n) = sum_{k<n} [f1(k) - f2(k)]

with <.> the zero-mode footprint average.  Three tests on the odd chain:
  1. power-law family: d ln rho/d sigma vs law with f = ln x, across sigma and r
  2. generic smooth random metric perturbations
  3. responsivity at both edges (even chain is handled in asym_check.py)
Expected: ratio measured/law = 1.000 to ~1e-3, degrading to a few percent
near sigma=1 where soft local gaps approach the broadening scale.
"""
import numpy as np
from ssh_common import bonds, hamiltonian, ldos

Nc = 100


def law_prediction(tb, dlnt):
    """-2<Phi> from the zero-mode product and per-bond log-derivatives dlnt."""
    n_cells = (len(tb) + 1) // 2
    w = np.zeros(n_cells + 1)
    Phi = np.zeros(n_cells + 1)
    w[0] = 1.0
    lw = 0.0
    for n in range(1, n_cells):
        lw += 2 * (np.log(tb[2 * n - 2]) - np.log(tb[2 * n - 1]))
        w[n] = np.exp(lw)
        Phi[n] = Phi[n - 1] + (dlnt[2 * n - 2] - dlnt[2 * n - 1])
    return -2 * np.sum(w * Phi) / np.sum(w)


def measured(sig, r, ds=1e-4):
    lp = np.log(ldos(hamiltonian(bonds(Nc, sig + ds, r))))
    lm = np.log(ldos(hamiltonian(bonds(Nc, sig - ds, r))))
    return (lp - lm) / (2 * ds)


print("1. POWER-LAW FAMILY: d ln rho/d sigma vs -2<Phi>, f = ln x")
print(f"{'sigma':>6} {'r':>5} {'measured':>12} {'law':>12} {'ratio':>8}")
for sig in [0.25, 0.5, 1.0]:
    for r in [0.5, 0.7]:
        tb = bonds(Nc, sig, r)
        lx = np.log(np.arange(1, len(tb) + 1) / len(tb))
        m, law = measured(sig, r), law_prediction(tb, lx)
        print(f"{sig:6.2f} {r:5.2f} {m:+12.5f} {law:+12.5f} {m/law:8.5f}")

print("\n2. GENERIC RANDOM SMOOTH METRIC PERTURBATION")
rng = np.random.default_rng(11)
t0 = bonds(Nc, 0.5, 0.5)
kx = np.arange(len(t0)) / len(t0)
for trial in range(3):
    f = np.zeros(len(t0))
    for h in range(1, 4):
        f += rng.standard_normal() * np.sin(np.pi * h * kx) + rng.standard_normal() * np.cos(np.pi * h * kx)
    eps = 1e-5
    m = (np.log(ldos(hamiltonian(t0 * (1 + eps * f)))) - np.log(ldos(hamiltonian(t0 * (1 - eps * f))))) / (2 * eps)
    law = law_prediction(t0, f)
    print(f"  trial {trial}: measured {m:+.5f}   law {law:+.5f}   ratio {m/law:.5f}")
