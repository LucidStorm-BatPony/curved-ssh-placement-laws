"""The placement asymmetry and its N-scaling (paper 1, section 4.3).

Even chain, both edges host a mode.  Each edge's responsivity d ln rho/d sigma
is measured by finite difference and compared with the per-edge form of the law:
  left  mode (A sublattice): ratio -t1(k)/t2(k)     -> Phi_L from f1(k) - f2(k)
  right mode (B sublattice): ratio -t1(m)/t2(m-1)   -> Phi_R from f1(m) - f2(m-1)
Expected (sigma=0.5, r=0.5): left +0.203 at every N; right -0.00339 / -0.00134 /
-0.000669 at N = 100/250/500, i.e. asymmetry 60x / 151x / 304x, linear in N.
The right-edge value is broadening-independent (mode physics, not background).
"""
import numpy as np
from ssh_common import bonds, hamiltonian, ldos


def run(Nc, sig=0.5, r=0.5, eta=1e-3, ds=1e-4):
    ns = 2 * Nc
    tp, tm = bonds(Nc, sig + ds, r, odd=False), bonds(Nc, sig - ds, r, odd=False)
    Hp, Hm = hamiltonian(tp), hamiltonian(tm)
    mL = (np.log(ldos(Hp, 0, eta)) - np.log(ldos(Hm, 0, eta))) / (2 * ds)
    mR = (np.log(ldos(Hp, ns - 1, eta)) - np.log(ldos(Hm, ns - 1, eta))) / (2 * ds)

    # law, left mode
    lw, wL, PhiL = 0.0, [1.0], [0.0]
    for n in range(1, Nc):
        x1, x2 = (2 * n - 1) / (2 * Nc - 1), (2 * n) / (2 * Nc - 1)
        lw += 2 * (np.log(np.sqrt(r) * x1 ** sig) - np.log(x2 ** sig / np.sqrt(r)))
        wL.append(np.exp(lw))
        PhiL.append(PhiL[-1] + np.log(x1) - np.log(x2))
    wL, PhiL = np.array(wL), np.array(PhiL)
    pL = -2 * np.sum(wL * PhiL) / np.sum(wL)

    # law, right mode
    lw, wR, PhiR = 0.0, [1.0], [0.0]
    for m in range(Nc, 1, -1):
        x1, x2 = (2 * m - 1) / (2 * Nc - 1), (2 * (m - 1)) / (2 * Nc - 1)
        lw += 2 * (np.log(np.sqrt(r) * x1 ** sig) - np.log(x2 ** sig / np.sqrt(r)))
        wR.append(np.exp(lw))
        PhiR.append(PhiR[-1] + np.log(x1) - np.log(x2))
    wR, PhiR = np.array(wR), np.array(PhiR)
    pR = -2 * np.sum(wR * PhiR) / np.sum(wR)
    return mL, pL, mR, pR


for Nc in [100, 250, 500]:
    mL, pL, mR, pR = run(Nc)
    print(f"N={Nc:4d}: LEFT meas {mL:+.5f} law {pL:+.5f} ratio {mL/pL:.4f} | "
          f"RIGHT meas {mR:+.6f} law {pR:+.6f} ratio {mR/pR:.4f} | "
          f"asym meas {abs(mL/mR):6.1f}x law {abs(pL/pR):6.1f}x")

print("\nbroadening test, right edge, N=250:")
for eta in [1e-3, 1e-4]:
    print(f"  eta={eta:.0e}: right-edge responsivity {run(250, eta=eta)[2]:+.6f}")
