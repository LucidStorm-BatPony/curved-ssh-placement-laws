"""Test the conjectured closed form for the shift-response law:
    d ln rho_edge / d(w_b^2) = - |psi_0(site b)|^2 / t2(cell)^2
for the A-sublattice NNN bond b (even, sites b -> b+2), bridging the
inter-cell hopping t2 of that cell. Both chains. Then: bias-diversity
channel separation for (sigma, w^2) disentangling.
"""
import numpy as np
from verify_return import build_H, rho_edge, E0_and_mode, NS, NC, T1, T2

def lnr(sigma, warr=None):
    return np.log(rho_edge(build_H(sigma, warr)))

def t2_of_cell(m, sigma):          # m = 1..NC, bridged by A-A bond b = 2(m-1)
    return T2 * ((2 * m) / (2 * NC - 1)) ** sigma

EPS = 0.005                        # smaller eps: cleaner quadratic regime
print("=" * 72)
print("CLOSED-FORM TEST:  K_bb  vs  -|psi(b)|^2 / t2^2   (even b, both chains)")
for SIG, label in [(0.0, "FLAT"), (0.5, "WARPED")]:
    base = lnr(SIG)
    _, psi, _ = E0_and_mode(build_H(SIG))
    p = np.abs(psi) ** 2
    devs = []
    print(f"  {label}:")
    for b in range(0, 31, 2):
        w = np.zeros(NS - 2); w[b] = EPS
        K = (lnr(SIG, w) - base) / EPS**2
        m = b // 2 + 1
        pred = -p[b] / t2_of_cell(m, SIG) ** 2
        rel = abs(K - pred) / abs(pred)
        devs.append(rel)
        if b <= 10 or b in (20, 30):
            print(f"    b={b:2d}  K={K:+.6e}   -p/t2^2={pred:+.6e}   rel dev={rel:.2e}")
    print(f"    max rel deviation over b=0..30: {max(devs):.2e}")

print("=" * 72)
print("ODD (B-SUBLATTICE) BOND DIAGONALS for completeness (warped):")
base = lnr(0.5)
for b in [1, 3, 5, 9, 15]:
    w = np.zeros(NS - 2); w[b] = EPS
    K = (lnr(0.5, w) - base) / EPS**2
    print(f"    b={b:2d}  K_bb = {K:+.4e}")

print("=" * 72)
print("BIAS DIVERSITY: response vectors v = (dlnrho/dsigma, dlnrho/d(w^2))")
ds, wt = 1e-4, 0.005
def vec(sig, wbias=0.0):
    wb = np.full(NS - 2, wbias) if wbias else None
    dsg = (lnr(sig + ds, wb) - lnr(sig - ds, wb)) / (2 * ds)
    # d/d(w^2): uniform small signal on top of bias
    if wbias:
        w1 = np.full(NS - 2, np.sqrt(wbias**2 + wt**2))
        dw2 = (lnr(sig, w1) - lnr(sig, wb)) / wt**2
    else:
        w1 = np.full(NS - 2, wt)
        dw2 = (lnr(sig, w1) - lnr(sig)) / wt**2
    return np.array([dsg, dw2])

biases = [("A: flat sigma=0      ", vec(0.0)),
          ("B: warped sigma=0.5  ", vec(0.5)),
          ("C: warped + wbar=0.03", vec(0.5, 0.03))]
for name, v in biases:
    print(f"  {name}:  v = ({v[0]:+.4e}, {v[1]:+.4e})")
import itertools
print("  pairwise separation angle (deg) between normalized response vectors:")
for (n1, v1), (n2, v2) in itertools.combinations(biases, 2):
    c = abs(v1 @ v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    ang = np.degrees(np.arccos(min(c, 1.0)))
    M = np.vstack([v1 / np.linalg.norm(v1), v2 / np.linalg.norm(v2)])
    print(f"    {n1[:1]}-{n2[:1]}: angle = {ang:5.2f} deg   cond(normalized M) = {np.linalg.cond(M):8.1f}")
