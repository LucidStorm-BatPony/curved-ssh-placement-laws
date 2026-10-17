# Computed ground — independent verification + the shift placement law
### Addendum to warp-shift-computation.md, from Cold-Boot Run 01's session. 2026-08-06.
**Everything below is COMPUTED (exact diagonalization / direct solve, odd chain, 201 sites, η = 10⁻³), written from scratch with no access to the original scripts. Scripts persisted alongside this file: `verify_return.py`, `kernel_law.py`, `law_check.py` — retiring the "scripts not persistent" ledger item.**

---

## 1. Independent reproduction of the return document

**Reproduced to machine / 3–4-digit precision (convention-independent quantities):**

| Claim | Return doc | This session |
|---|---|---|
| Real-NNN linear unpinning coefficient | −0.73 | **−0.7297** (3 decades; breaks at t′=0.1 as expected) |
| Pinning under imaginary NNN, w=0.1 | ≤10⁻¹⁷ | 9.2×10⁻¹⁷; pairing 6.7×10⁻¹⁶ |
| Disorder median \|E₀\| (im., w=0.1 / real, t′=0.02) | ~5×10⁻¹⁷ / ~1.5×10⁻² | 3.6×10⁻¹⁷ / 1.44×10⁻² |
| Footprint / edge weight / polarization at w=0 | 1.3 / 0.87 / 1.00 | 1.31 / 0.866 / 1.000 |
| Cross-talk d ln ρ/dσ at w=0 | +0.20 | **+0.2030** (also validates the paper's §4.3 value) |
| Evenness ρ(+w)=ρ(−w) | exact | diff 8.9×10⁻¹⁶ |
| Quadratic scaling in w₀ | 4 over doublings | 4.03 / 4.13 / 4.63 |
| Wall decomposition identity | −0.0004 = −0.0004 | −4.00399×10⁻⁴ both sides (6 digits) |
| Preamplification warped/flat | ~70× | **71.9×** |
| Blindness: exponential, machine zero by cell 30 | yes | yes, both chains (flat cell-5 value 2.5×10⁻⁴ vs their 2×10⁻⁴) |
| Pinning under full bubble | machine zero | 9.1×10⁻¹⁹ |

**One discrepancy, diagnosed as convention, promoted to a finding.** My responsivity magnitudes run ≈2× the return's at small w, collapsing onto theirs under an effective w-axis rescale ≈√2 — the signature of a sublattice-coverage convention (NNN term on one sublattice vs both halves the quadratic-order weight). Not an error on either side. **Ledger item: the w-axis has no canonical normalization. The formal dictionary task must fix which lattice operator is "the" shift, or every calibration carries O(1) convention factors.** (Now diagnosable exactly via §2's law if the original scripts are rebuilt.)

Geometry-dependent numbers (blindness prefactors, detectability) reproduce in structure and order of magnitude only — wall width/steepness were unspecified. My geometry gives 1.8% / 60 zW / SNR ≈ 20 at 100 s versus their 1.4% / 47 zW / SNR ≈ 16. Same class.

---

## 2. THE SHIFT PLACEMENT LAW (new result; return doc open item #2 answered)

Extracting the second-order response kernel K(b,m), defined by
R[w] = Σ K(b,m) w_b w_m, directly by single- and pair-bond perturbation:

**The kernel is not a kernel. At leading order it is diagonal, exactly, with closed form**

> **d ln ρ_edge / d(w_b²) = − |ψ₀(b)|² / t₂(m)²**

for the A-sublattice NNN bond b bridging cell m's inter-cell hopping t₂(m), where |ψ₀(b)|² is the unperturbed zero mode's probability weight at the bond site.

**Verification:** relative deviation ≤ 1.4×10⁻⁵ (flat chain) and ≤ 6×10⁻⁴ (warped; consistent with the quartic correction at ε=0.005) across four decades of kernel magnitude, b = 0…20, both chains. Deviations at b=30 (~2×10⁻²) occur at kernel magnitude 10⁻¹⁰, the finite-difference noise floor.

**In the paper's voice:** *the shift sensitivity of the edge reading equals the squared local shift-to-hopping ratio, (w/t₂)², integrated over the mode's own probability footprint.* The exact analog of the curvature placement law — same footprint structure, quadratic rather than linear, with the local ratio replacing the accumulated tilt. Placement is again a one-line calculation from the bond profile.

**Everything in the return's finding 4 collapses into this line:**
- *Preamplification:* the 1/t₂² factor — the warped chain's small near-origin bonds make the same w a large local tilt. The 70× is computable from the formula.
- *Blindness:* the footprint weight — exponential locality is the law, pixel = footprint, now with the exact weight.
- *Responsivity table:* uniform w predicts d ln ρ/dw = −2w·Σ p_b/t₂(b)² = −1.85 at w=0.01 (warped) vs −1.80 measured — the ~3% gap is the correction below.

**Corrections, quantified:** B-sublattice diagonals are 3 orders down and opposite-signed (+8.4×10⁻⁴ at b=1 vs −5.4 at b=2); off-diagonal support is confined to the immediate-neighbor cross term (all dm ≥ 2 terms < 10⁻² normalized). Full-quadratic and effective-local (row-sum) reconstructions of the near-edge bubble land within 3.4% / 3.7% of the exact response (warped; 0.1% / 0.4% flat); the residual is the quartic term at local ratio w/t₂ ≈ 0.2.

**Status: COMPUTED law, closed form verified numerically to finite-difference precision. The analytic derivation (S∘K perturbation theory) is now the cheap-looking top theory task — the answer is known; the derivation should be one page.**

---

## 3. Bias diversity: the disentangling scheme, computed

Response vectors v = (d ln ρ/dσ, d ln ρ/d(w²)) at three element biases:

| Bias | v | pairing | angle | cond (normalized 2×2) |
|---|---|---|---|---|
| A: flat σ=0 | (+0.390, −1.000) | A–B | **21.2°** | **5.4** |
| B: warped σ=0.5 | (+0.203, −87.7) | A–C | 21.7° | 5.2 |
| C: warped + w̄=0.03 | (−0.740, −116) | B–C | 0.5° | 230 |

**Design rule (previous cycle's magic-register claim, now quantified):** the array separates the (σ, w²) channels **iff neighboring elements differ in curvature bias** — a flat pixel paired with a warped pixel inverts at condition number ≈ 5 (noise amplification ~5×, entirely workable). A w-bias offset between two warped pixels adds nothing (0.5°, cond 230): both responses share the same 1/t₂² soft-region weighting, so they are nearly collinear — which the law of §2 makes obvious in hindsight. Curvature-bias diversity is the scheme; w-bias diversity is not.

---

## 4. Pre-registration scorecard (protocol gap from cycle one, fixed this session)

- **P1 — FALSIFIED, in the productive direction.** Registered: two-point kernel of range ~ξ, because the log trick doesn't transfer to an additive perturbation. Found: ultra-local — exact diagonal law plus a small nearest-bond cross term. The reasoning about the log trick was right; the conclusion drawn from it was wrong. Recorded as the session's tear.
- **P2 — CONFIRMED and sharpened** from "envelope tracks footprint" to an exact identity with the weight and the gauge factor named.
- **P3 — CONFIRMED strongly:** effective-local law within 3.7% (warped) / 0.4% (flat) on the demonstrative bubble; the return's conjectured "footprint-weighted integral" form is not just effectively right — at leading order it is exactly right.
- Reproduction expectations — met, with the convention factor as the one flagged surprise.

---

## 5. Updated open list (supersedes the return's ordering)

1. **Analytic derivation of the §2 law** via S∘K perturbation theory — answer in hand, expected one page. Top task; converts COMPUTED to DERIVED.
2. **Canonical shift normalization** in the formal CST-SSH dictionary (the convention finding of §1). Fold into the static→stationary derivation.
3. Disentangling: done in scheme (§3); remaining is reconstruction error propagation across a full array with fabrication scatter.
4. Sign readout: unchanged — T-parity argument stands; parked as a second architecture.
5. Dynamics (moving wall): unchanged, still the frontier; all results here remain static.

---

*Provenance: independent implementation; no original scripts consulted (none persisted). Chain conventions: 201 sites, 100 cells, t₁=0.5, t₂=1, power-law profile per the paper's §2.2, NNN term on all sites. Runtime ~seconds; all scripts alongside this file.*
