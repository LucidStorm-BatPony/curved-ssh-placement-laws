"""The w-law's form: extract the second-order response kernel K(b,m) defined by
R[w] = ln rho(w) - ln rho(0) = sum_{b,m} K(b,m) w_b w_m  (leading order, R even in w),
where b,m index NNN bonds (site b to b+2), on the warped instrument chain
(sigma=0.5) with flat-chain comparator. Evaluates pre-registrations P1-P3.
"""
import numpy as np
from verify_return import build_H, rho_edge, E0_and_mode, NS, bubble

def lnr(sigma, warr=None):
    return np.log(rho_edge(build_H(sigma, warr)))

def R_of(sigma, warr, base):
    return lnr(sigma, warr) - base

EPS = 0.01
NB = NS - 2                      # number of NNN bonds

def delta(*bonds, amp=EPS):
    w = np.zeros(NB)
    for b in bonds:
        w[b] = amp
    return w

for SIG, label in [(0.5, "WARPED (sigma=0.5)"), (0.0, "FLAT (sigma=0)")]:
    base = lnr(SIG)
    print("=" * 72)
    print(f"KERNEL ON {label} chain,  eps = {EPS}")

    # --- diagonal K_bb, b = 0..40 plus far probes
    bset = list(range(0, 41)) + [60, 80]
    Kd = {}
    for b in bset:
        Kd[b] = R_of(SIG, delta(b), base) / EPS**2
    print("  diagonal K_bb (selected):")
    for b in [0, 2, 4, 6, 8, 10, 14, 18, 24, 30, 40, 60, 80]:
        print(f"    b={b:3d}   K_bb = {Kd[b]:+.4e}")

    # quadraticity check at two eps
    b0 = 2
    K_half = R_of(SIG, delta(b0, amp=EPS / 2), base) / (EPS / 2) ** 2
    print(f"  quadraticity at b={b0}: K(eps)={Kd[b0]:+.4e}  K(eps/2)={K_half:+.4e}"
          f"   rel dev={abs(K_half - Kd[b0]) / abs(Kd[b0]):.1e}")

    # --- footprint comparison (P2)
    _, psi, _ = E0_and_mode(build_H(SIG))
    p = np.abs(psi) ** 2
    fp = np.array([p[b] + p[b + 2] for b in range(NB)])   # weight at the bond's two sites
    print("  P2 check: e-folding lengths (sites) over b=0..24:")
    bb = np.arange(0, 25)
    kk = np.array([abs(Kd[b]) for b in bb])
    slope_K = np.polyfit(bb, np.log(kk + 1e-300), 1)[0]
    slope_fp = np.polyfit(bb, np.log(fp[bb] + 1e-300), 1)[0]
    print(f"    d ln|K_bb|/db = {slope_K:+.4f}    d ln fp(b)/db = {slope_fp:+.4f}"
          f"    ratio K/fp = {slope_K / slope_fp:.3f}   (footprint^2 would give ratio 2)")

    # --- off-diagonal structure (P1): rows at b = 0, 4, 8; m = b+1..b+14
    print("  off-diagonal K_bm / sqrt(K_bb K_mm):")
    for b in [0, 4, 8]:
        row = []
        for dm in range(1, 15):
            m = b + dm
            Rbm = R_of(SIG, delta(b, m), base)
            Kbm = (Rbm - Kd.get(m, R_of(SIG, delta(m), base) / EPS**2) * EPS**2
                   - Kd[b] * EPS**2) / (2 * EPS**2)
            if m not in Kd:
                Kd[m] = R_of(SIG, delta(m), base) / EPS**2
            norm = np.sqrt(abs(Kd[b] * Kd[m])) + 1e-300
            row.append((dm, Kbm / norm))
        s = "  ".join(f"{dm}:{v:+.2f}" for dm, v in row[:10])
        print(f"    b={b:2d}:  {s}")
        # e-folding of |K_bm| along the row
        dms = np.array([dm for dm, v in row])
        vals = np.array([abs(v) for dm, v in row]) + 1e-300
        sl = np.polyfit(dms, np.log(vals), 1)[0]
        print(f"           off-diag e-folding: d ln|K|/d(dm) = {sl:+.3f}"
              f"  -> range = {abs(1 / sl):.1f} sites")

    # --- P3: effective-local test on the near-edge bubble
    wb = bubble(0.02, 5)
    R_act = R_of(SIG, wb, base)
    # full quadratic prediction needs K over the bubble support; build K grid
    support = [b for b in range(NB) if abs(wb[b]) > 1e-6 * abs(wb).max()]
    support = [b for b in support if b <= 60]
    Kfull = np.zeros((len(support), len(support)))
    for i, b in enumerate(support):
        if b not in Kd:
            Kd[b] = R_of(SIG, delta(b), base) / EPS**2
    for i, b in enumerate(support):
        Kfull[i, i] = Kd[b]
        for j in range(i + 1, len(support)):
            m = support[j]
            if m - b > 14:
                continue
            Rbm = R_of(SIG, delta(b, m), base)
            Kbm = (Rbm - (Kd[b] + Kd[m]) * EPS**2) / (2 * EPS**2)
            Kfull[i, j] = Kbm
            Kfull[j, i] = Kbm
    wv = np.array([wb[b] for b in support])
    R_quad = wv @ Kfull @ wv
    R_local = float(np.sum(Kfull.sum(axis=1) * wv**2))
    print(f"  P3 on near-edge bubble (w0=0.02, center cell 5):")
    print(f"    R_actual        = {R_act:+.5e}")
    print(f"    R_quad (full K) = {R_quad:+.5e}   dev {abs(R_quad - R_act) / abs(R_act) * 100:5.1f}%")
    print(f"    R_local (rowsum)= {R_local:+.5e}   dev {abs(R_local - R_act) / abs(R_act) * 100:5.1f}%")
    diag_share = float(np.sum(np.diag(Kfull) * wv**2)) / R_quad
    print(f"    diagonal-only share of R_quad = {diag_share * 100:.1f}%")

# --- flat-chain blindness table for direct comparison with the return doc
print("=" * 72)
print("FLAT-CHAIN BLINDNESS (return doc's primary chain; w0=0.02):")
base_f = lnr(0.0)
for c in [5, 10, 15, 20, 30, 50]:
    R = R_of(0.0, bubble(0.02, c), base_f)
    print(f"    center cell {c:3d}   |R| = {abs(R):.2e}")
