"""Cold-review checks for curved-ssh-placement-laws (17 Oct 2026).

Run from the repo root (imports ssh_common.py from scripts/, t1*t2 = 1 convention):
    python3 review/cold_review_checks.py

Five checks behind the review's findings:
  1. the far-end lead does not broaden the probed mode (LDOS at site 0 is 1/(pi*eta) exactly)
  2. topological/trivial contrast at the stated broadening (paper 1 says ~1e13; no script existed)
  3. on-site (frequency) disorder on the warped chain -- the untested disorder class
  4. shift preamplification vs chain length (scales as N^(2 sigma))
  5. uniform shift on both sublattices vs the diagonal (A-A-only) law, and the O(w^2)
     reshaping of the A-sublattice profile that derive_verify.py test 4 cannot see
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import numpy as np
from ssh_common import bonds, hamiltonian, zero_mode, ldos

print("1. LDOS at the probed site vs eta, even chain N=250, sigma=0.5, exact lead self-energy on the far end")
Nc, r, sig, tL = 250, 0.5, 0.5, 1.0
tb = bonds(Nc, sig, r, odd=False); ns = len(tb) + 1
H = np.zeros((ns, ns), complex)
for i in range(ns - 1):
    H[i, i + 1] = H[i + 1, i] = tb[i]
H[ns - 1, ns - 1] += tL * tL * (-1j / tL)          # g_lead(E=0) = -i/t_L
for eta in [1e-5, 1e-7, 1e-9, 1e-11]:
    A = (1j * eta) * np.eye(ns) - H; e = np.zeros(ns, complex); e[0] = 1
    rho = -np.linalg.solve(A, e)[0].imag / np.pi
    print(f"   eta={eta:.0e}: rho = {rho:.4e}   rho*pi*eta = {rho*np.pi*eta:.4f}  (|a_1|^2 = 0.8660 -> purely eta-limited)")
lw = sum(2 * (np.log(tb[2 * n - 2]) - np.log(tb[2 * n - 1])) for n in range(1, Nc))
print(f"   left-mode weight at the lead end / edge = exp({lw:.0f}) = 1e{lw/np.log(10):.0f}")

print("\n2. Topological vs trivial zero-energy LDOS at site 0, N=250, eta=1e-7, lead at the far end")
vals = {}
for label, rr in [("topological r=0.5", 0.5), ("trivial r=2.0", 2.0)]:
    tbb = bonds(250, 0.5, rr, odd=False); Hh = hamiltonian(tbb); Hh[-1, -1] += -1j * tL
    vals[label] = ldos(Hh, 0, 1e-7); print(f"   {label}: rho = {vals[label]:.3e}")
print(f"   contrast = {vals['topological r=0.5']/vals['trivial r=2.0']:.1e}  (scales as eta^-2; 1e13 needs eta ~ 1e-8)")

print("\n3. On-site Gaussian disorder, warped odd chain N=100, 200 realisations (units: t2 = sqrt 2)")
Nc = 100; tb = bonds(Nc, 0.5, 0.5); ns = len(tb) + 1
rng = np.random.default_rng(1)
print(f"   edge bonds: t1(1)={tb[0]:.4f}  t2(1)={tb[1]:.4f}  (nominal t2 = {np.sqrt(2):.3f})")
for d in [1e-4, 1e-3, 1e-2]:
    Es, edge = [], []
    for _ in range(200):
        Hd = hamiltonian(tb) + np.diag(d * rng.standard_normal(ns))
        E, v = zero_mode(Hd); Es.append(abs(E)); edge.append(abs(v[0]) ** 2)
    print(f"   sigma_onsite={d:.0e} ({d/np.sqrt(2)*100:.3f}% of t2): median|E0|={np.median(Es):.2e} max={np.max(Es):.2e}  edge weight {np.median(edge):.3f}")

print("\n4. Preamplification (warped/flat) vs N, bubble.py geometry, w0=0.02")
for Nc in [50, 100, 200, 400]:
    ns = 2 * Nc + 1
    x = np.arange(ns - 2) / 2.0
    prof = 0.01 * (np.tanh(0.5 * (x - (8 - 10))) - np.tanh(0.5 * (x - (8 + 10))))
    def resp(s):
        t = bonds(Nc, s, 0.5)
        return np.log(ldos(hamiltonian(t, warr=prof))) - np.log(ldos(hamiltonian(t)))
    f, wv = resp(0.0), resp(0.5); t1e = bonds(Nc, 0.5, 0.5)[0]
    print(f"   N={Nc:3d}: preamp {wv/f:6.1f}x   t1(1)={t1e:.4f}   w0/t1(1)={0.02/t1e:.2f}")

print("\n5. Uniform shift on A-A and B-B bonds vs A-A only (= diagonal law), w -> 0")
Nc = 100; ns = 2 * Nc + 1
for s in [0.0, 0.25, 0.5, 0.75, 1.0]:
    tb = bonds(Nc, s, 0.5); base = np.log(ldos(hamiltonian(tb)))
    out = []
    for w in [1e-3, 1e-2]:
        wall = np.full(ns - 2, w); wA = np.where(np.arange(ns - 2) % 2 == 0, w, 0.0)
        dl = np.log(ldos(hamiltonian(tb, warr=wall))) - base
        dlA = np.log(ldos(hamiltonian(tb, warr=wA))) - base
        out.append(dl / dlA)
    print(f"   sigma={s:4.2f}: ratio = {out[0]:.4f} (w=1e-3), {out[1]:.4f} (w=1e-2)")

print("\n   A-sublattice profile ratio alpha_n/a_n, flat chain, uniform w=0.01 on all bonds (cells 1..8):")
tb = bonds(Nc, 0.0, 0.5)
_, a = zero_mode(hamiltonian(tb)); a = (a * np.exp(-1j * np.angle(a[0]))).real
_, psi = zero_mode(hamiltonian(tb, warr=np.full(ns - 2, 0.01))); psi = psi * np.exp(-1j * np.angle(psi[0]))
print("   ", np.array2string(psi[0::2].real[:8] / a[0::2][:8], precision=6))
print("    (A-A bonds only gives a constant 0.999975: the reshaping is the B-B cross term, O(w^2))")
