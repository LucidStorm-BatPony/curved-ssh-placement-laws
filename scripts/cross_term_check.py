"""The A-A / B-B cross term in the shift law (paper 2, section 3, two-sublattice profiles).

The single-bond law d ln rho = -w^2 a_{m+1}^2/t1(m)^2 is exact for shift on A-A bonds.
The physical encoding (2w sin k x identity) puts the shift on both sublattices, and the
B-B part acts on the leaked B amplitude, tilting the A envelope at O(w^2):

    alpha_n / a_n = 1 + phi_1 - (n-1) * w^2 (1 - r^2) / t1^2      (flat chain, uniform w)

with the boundary identity 2*phi_1 = -||psi_B||^2, which makes the uniform-w response
on the FLAT chain equal the A-A-only (diagonal) law exactly -- a cancellation, not
diagonality.  On the warped chain the cancellation fails and the cross term is a
~5% leading-order correction.  (Found by the 17 Oct 2026 cold review; see review/.)

Expected: tilt slope ratio 1.000; identity to 1e-5; warped uniform/AA ratio ~0.947,
w-independent as w -> 0 (i.e. the cross term is O(w^2), same order as the law).
"""
import numpy as np
from ssh_common import bonds, hamiltonian, zero_mode, ldos

Nc = 100
ns = 2 * Nc + 1

print("1. A-envelope tilt under uniform w on all bonds, flat chain  (test 4 of derive_verify.py cannot see this)")
for r in [0.5, 0.7]:
    tb = bonds(Nc, 0.0, r)
    t1 = tb[0]
    w = 0.01
    _, a = zero_mode(hamiltonian(tb))
    a = (a * np.exp(-1j * np.angle(a[0]))).real
    _, psi = zero_mode(hamiltonian(tb, warr=np.full(ns - 2, w)))
    psi = psi * np.exp(-1j * np.angle(psi[0]))
    ratio = psi[0::2].real[:12] / a[0::2][:12]
    slope_meas = np.polyfit(np.arange(2, 10), ratio[1:9], 1)[0]
    slope_pred = -w ** 2 * (1 - r ** 2) / t1 ** 2
    leakB = np.sum(np.abs(psi[1::2]) ** 2)
    ok = abs(slope_meas / slope_pred - 1) < 1e-3 and abs(2 * (ratio[0] - 1) + leakB) < 1e-6
    print(f"   r={r}: slope {slope_meas:+.3e}/cell vs predicted {slope_pred:+.3e}  (ratio {slope_meas/slope_pred:.4f});"
          f"  2*phi_1 = {2*(ratio[0]-1):+.3e} vs -||psi_B||^2 = {-leakB:+.3e}   {'PASS' if ok else 'FAIL'}")
    print(f"   alpha_n/a_n, cells 1..6: {np.array2string(ratio[:6], precision=6)}")

print("\n2. Uniform shift (both sublattices) / A-A-only (diagonal law), w -> 0")
print(f"{'sigma':>6} {'w=1e-3':>9} {'w=3e-3':>9} {'w=1e-2':>9}")
for s in [0.0, 0.25, 0.5, 0.75, 1.0]:
    tb = bonds(Nc, s, 0.5)
    base = np.log(ldos(hamiltonian(tb)))
    row = []
    for w in [1e-3, 3e-3, 1e-2]:
        wall = np.full(ns - 2, w)
        wA = np.where(np.arange(ns - 2) % 2 == 0, w, 0.0)
        dl = np.log(ldos(hamiltonian(tb, warr=wall))) - base
        dlA = np.log(ldos(hamiltonian(tb, warr=wA))) - base
        row.append(dl / dlA)
    print(f"{s:6.2f} {row[0]:9.4f} {row[1]:9.4f} {row[2]:9.4f}")
print("   (flat: 1.0000 by the boundary identity; warped sigma=0.5: 0.947, a -5% O(w^2) cross term)")

print("\n3. Preamplification (warped/flat, bubble.py geometry, w0=0.02) vs N -- scales as N^(2 sigma)")
print(f"{'N':>5} {'preamp':>8} {'t1(1)':>8} {'w0/t1(1)':>9} {'N^(2sig)/100^(2sig)':>21}")
for N in [50, 100, 200, 400]:
    n_s = 2 * N + 1
    x = np.arange(n_s - 2) / 2.0
    prof = 0.01 * (np.tanh(0.5 * (x + 2)) - np.tanh(0.5 * (x - 18)))
    def resp(s):
        t = bonds(N, s, 0.5)
        return np.log(ldos(hamiltonian(t, warr=prof))) - np.log(ldos(hamiltonian(t)))
    f, wv = resp(0.0), resp(0.5)
    t1e = bonds(N, 0.5, 0.5)[0]
    print(f"{N:5d} {wv/f:8.1f} {t1e:8.4f} {0.02/t1e:9.2f} {(N/100)**1.0:21.2f}")
print("   (the expansion parameter w0/t1(1) reaches 0.8 at N=400: define the operating point by w-tilde at the edge)")
