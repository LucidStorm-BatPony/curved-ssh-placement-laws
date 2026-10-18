"""Independent numerical verification of the S∘K derivation's structure
(derive_check.py was not shipped; this replaces it in my convention, t2=1):
  1. Single-spike leak: one B site, predicted location and amplitude (both faces).
  2. Sensitivity = leaked probability: d ln rho = ln(1 - P_B), and its range.
  3. B-B bonds respond at quartic order.
  4. A-sublattice shape invariance to O(w^4).
"""
import numpy as np
from verify_return import build_H, rho_edge, E0_and_mode, NS, NC, T1, T2

SIG = 0.5
def tbonds(sigma=SIG):
    tb = np.zeros(NS - 1)
    for m in range(1, NC + 1):
        tb[2 * m - 2] = T1 * ((2 * m - 1) / (2 * NC - 1)) ** sigma
        if 2 * m - 1 < NS - 1:
            tb[2 * m - 1] = T2 * ((2 * m) / (2 * NC - 1)) ** sigma
    return tb

tb = tbonds()
H0 = build_H(SIG)
_, psi0, _ = E0_and_mode(H0)
psi0 = psi0 * np.sign(psi0[0].real)          # fix global sign; mode is real on A
base = np.log(rho_edge(H0))

print("=" * 72)
print("1. SINGLE-SPIKE LEAK  (A-A bond b=8, cells 5->6; predicted spike at B site 9)")
b = 8; m = b // 2 + 1                        # cell 5
for w in [1e-3, 1e-2]:
    warr = np.zeros(NS - 2); warr[b] = w
    _, psi, _ = E0_and_mode(build_H(SIG, warr))
    Bamp = np.abs(psi[1::2])                 # odd sites = B
    spike_site = 1 + 2 * np.argmax(Bamp)
    pred1 = w * abs(psi0[b + 2]) / tb[b]     # w*a_{m+1}/t1(m)
    pred2 = w * abs(psi0[b]) / tb[b + 1]     # w*a_m/t2(m)  (two-faced identity)
    second = np.sort(Bamp)[-2]
    print(f"  w={w:6.0e}: spike at site {spike_site} (pred 9);"
          f" |amp|={Bamp.max():.6e}  pred(face1)={pred1:.6e}  pred(face2)={pred2:.6e}"
          f"  next-largest B amp={second:.2e}")

print("=" * 72)
print("2. SENSITIVITY = LEAKED PROBABILITY:  d ln rho  vs  ln(1 - P_B)")
print("   (single bond b=8, then uniform w on all bonds)")
for label, mk in [("single b=8", lambda w: (np.zeros(NS - 2), w)),
                  ("uniform   ", lambda w: (None, w))]:
    print(f"   {label}:")
    for w in [1e-2, 3e-2, 1e-1]:
        if label.startswith("single"):
            warr = np.zeros(NS - 2); warr[b] = w
        else:
            warr = np.full(NS - 2, w)
        Hp = build_H(SIG, warr)
        dlnr = np.log(rho_edge(Hp)) - base
        _, psi, _ = E0_and_mode(Hp)
        PB = float(np.sum(np.abs(psi[1::2]) ** 2))
        pred = np.log(1 - PB)
        rel = abs(dlnr - pred) / max(abs(pred), 1e-300)
        print(f"     w={w:5.0e}   d ln rho={dlnr:+.6e}   ln(1-P_B)={pred:+.6e}   rel dev={rel:.1e}")

print("=" * 72)
print("3. B-B BONDS: zero-mode PT gives NO O(w^2) term; measured slope 2 is eta^2 broadening background  (odd bond b=9; fit log|R| vs log w)")
Rs, ws = [], [0.025, 0.05, 0.1, 0.2]
for w in ws:
    warr = np.zeros(NS - 2); warr[9] = w
    Rs.append(np.log(rho_edge(build_H(SIG, warr))) - base)
slope = np.polyfit(np.log(ws), np.log(np.abs(Rs)), 1)[0]
for w, R in zip(ws, Rs):
    print(f"   w={w:5.3f}   R={R:+.3e}")
print(f"   log-log slope = {slope:.3f}   (zero-mode: none at O(w^2); slope 2 = background, see warp-shift-computation.md corrected corollary)")

print("=" * 72)
print("4. A-SHAPE: 1 - cos_sim(A-part, unperturbed) ~ O(w^4)  [NOTE 17 Oct 2026: this test CANNOT detect")
print("   the O(w^2) envelope tilt from B-B bonds, because 1-cos_sim is quadratic in the shape change;")
print("   slope ~4 is CONSISTENT with that tilt. See scripts/cross_term_check.py for the direct measurement.]")
devs, ws4 = [], [0.01, 0.02, 0.04, 0.08]
for w in ws4:
    warr = np.full(NS - 2, w)
    _, psi, _ = E0_and_mode(build_H(SIG, warr))
    A = psi[0::2]
    A = A * np.exp(-1j * np.angle(A[0]))
    A0 = psi0[0::2]
    cs = abs(np.vdot(A0, A)) / (np.linalg.norm(A0) * np.linalg.norm(A))
    devs.append(1 - cs)
    print(f"   w={w:4.2f}   1-cos_sim = {1 - cs:.3e}")
slope4 = np.polyfit(np.log(ws4), np.log(devs), 1)[0]
print(f"   log-log slope = {slope4:.3f}   (quadratic in an O(w^2) tilt -> ~4; not a shape-invariance proof)")
