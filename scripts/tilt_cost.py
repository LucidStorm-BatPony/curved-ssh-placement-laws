"""The chiral cost of encoding a shift (paper 2, section 2; warp-shift-computation.md).

Odd warped chain, 201 sites, r=0.5, sigma=0.5.  Two same-sublattice couplings:
  real NNN t'  -- k-even identity term; expected to unpin the zero mode linearly
                  (E0 ~ -0.73 t')
  imag NNN w   -- current-like term, 2w sin k; expected to leave E0 at machine zero
                  even under 1% NN hopping disorder (200 realizations)
Then the shift responsivity d ln rho/dw and the curvature cross-talk d ln rho/dsigma.
"""
import numpy as np
from ssh_common import bonds, hamiltonian, zero_mode, ldos

Nc = 100
tb = bonds(Nc, 0.5, 0.5)
ns = len(tb) + 1
E0, v0 = zero_mode(hamiltonian(tb))
print(f"baseline: E0 = {E0:.3e}   A-weight = {np.sum(np.abs(v0[0::2])**2):.6f}   |psi(edge)|^2 = {abs(v0[0])**2:.4f}")

print("\n-- REAL NNN t' (naive tilt attempt) --")
print(f"{'tprime':>10} {'E0':>12} {'E0/tprime':>12}")
for tp in [1e-5, 1e-4, 1e-3, 1e-2]:
    E, _ = zero_mode(hamiltonian(tb, tp_real=tp))
    print(f"{tp:10.0e} {E:12.4e} {E/tp:12.4f}")

print("\n-- IMAG NNN w (the shift encoding) --")
print(f"{'w':>10} {'E0':>12}")
for w in [1e-3, 3e-3, 1e-2, 3e-2, 1e-1]:
    E, _ = zero_mode(hamiltonian(tb, warr=np.full(ns - 2, w)))
    print(f"{w:10.0e} {E:12.4e}")

print("\n-- protection stress: 1% NN hopping disorder, 200 realizations --")
rng = np.random.default_rng(7)
print(f"{'config':>22} {'median|E0|':>12} {'max|E0|':>12}")
for label, kw in [("w=0 (chiral)", {}), ("w=0.02", {'warr': np.full(ns - 2, 0.02)}),
                  ("w=0.05", {'warr': np.full(ns - 2, 0.05)}), ("w=0.10", {'warr': np.full(ns - 2, 0.10)}),
                  ("tp=0.02 (real)", {'tp_real': 0.02})]:
    Es = [abs(zero_mode(hamiltonian(tb, dis=0.01, rng=rng, **kw))[0]) for _ in range(200)]
    print(f"{label:>22} {np.median(Es):12.3e} {np.max(Es):12.3e}")

print("\n-- shift responsivity and curvature cross-talk (eta=1e-3) --")
dw, ds = 1e-3, 1e-3


def rho(w, sig=0.5):
    return ldos(hamiltonian(bonds(Nc, sig, 0.5), warr=np.full(ns - 2, w)))


print(f"{'w':>6} {'dln rho/dw':>12} {'dln rho/dsig':>13}")
for w in [0.0, 0.01, 0.02, 0.05, 0.08]:
    rw = (np.log(rho(w + dw)) - np.log(rho(w - dw))) / (2 * dw)
    rs = (np.log(rho(w, 0.5 + ds)) - np.log(rho(w, 0.5 - ds))) / (2 * ds)
    print(f"{w:6.2f} {rw:+12.3f} {rs:+13.3f}")
