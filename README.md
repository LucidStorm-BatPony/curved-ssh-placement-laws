# Placement laws for curved-spacetime SSH chains

Two draft papers, their derivations, and the scripts that verify them.

## Standing on whose shoulders

This work builds directly on the **curved-spacetime Su-Schrieffer-Heeger model** of
**Priyanuj Rajbongshi and Ranjan Modak**,
*Topological properties of curved spacetime extended Su-Schrieffer-Heeger model*,
J. Phys.: Condens. Matter, [DOI 10.1088/1361-648X/ae8635](https://doi.org/10.1088/1361-648X/ae8635) (2026);
[arXiv:2504.16200](https://arxiv.org/abs/2504.16200).
Their Hamiltonian, their proof that the topological phase survives warping, and their
exact zero-mode wavefunctions are the foundation of everything here. The placement
laws below are properties of their model that they did not have reason to look for.

The qubit-as-decoherence-probe readout is established prior art:
**Zaimi, Boudreault, Baspin, Delnour, Eleuch, MacKenzie & Hilke**,
Phys. Lett. A 388, 127035 (2021), [arXiv:1910.09926](https://arxiv.org/abs/1910.09926), and
**Delnour, Bissonnette, Eleuch, MacKenzie & Hilke**,
Phys. Lett. A 466, 128716 (2023), [arXiv:2302.13771](https://arxiv.org/abs/2302.13771).
The calorimetric floor comes from the bolometry of **Kokkoniemi et al.**,
Nature 586, 47 (2020). Full reference lists are in the papers.

## What is claimed

1. **Curvature placement law** (paper 1). For a warped SSH chain read by a weakly
   coupled qubit, the logarithmic response of the edge density of states to curvature
   equals the differential metric tilt integrated over the edge mode's own probability
   footprint. Uniform metric changes cancel exactly; only gradients register. The
   two ends of one warped chain differ in responsivity by 151× at 250 cells, growing
   linearly with chain length — a falsifiable prediction testable in a photonic array.
2. **Shift placement law** (paper 2). A stationary-metric shift g_tx enters the lattice
   as a current-like same-sublattice hopping. It breaks unitary chiral symmetry but an
   antiunitary one survives, so the mode stays pinned for any shift profile. The edge
   response is minus the leaked probability: d ln ρ = −w̃² |ψ₀|². Static calorimetry
   reads |g_tx|² and is blind to its sign.

Both laws are **derived** and **verified** against independent numerics, and were
re-derived by hand in an outside cold review (17 Oct 2026, `review/`). That review
also found that paper 1's absolute-power figures (section 5) rest on a linewidth the
draft never designs — the far-end lead cannot broaden the probed mode — so the device
numbers are under revision; the laws and responsivities are unaffected. The
identification of the lattice shift term with g_tx is by dispersion form, with the
tilted-cone lattice literature now cited, not a completed static-to-stationary
derivation. The papers state all of this.

## Status

Drafts for comment. Not peer-reviewed, not submitted. Developed in extended
collaboration between B. Watson (direction, framing, verification standard) and
AI systems (Claude, Anthropic), which performed the bulk of the derivation, numerics,
and drafting. Paper 2's Appendix B describes the two-session cross-checking process
(reimplementation in a second hopping convention, errors kept on the record); the
first independent reading is the cold review in `review/`, whose fix list is being
worked through in the commit history.

## Layout

```
papers/        tidal-imager-draft.{md,pdf}     paper 1, curvature placement law
               shift-law-draft.{md,pdf}        paper 2, shift placement law
derivations/   imager-derivations.md           every proof in paper 1, step by step
               warp-shift-computation.md       the claim→computed→derived chain for paper 2
               computed-ground-addendum.md     the counterpart session's independent reproduction
scripts/       the verification set (see below)
notes/         working notes: SUSY/memory bridge, memory protocol, archival skeleton
review/        the 17 Oct 2026 cold review and its check script
```

## Scripts

Every number in paper 1 section 4 and appendix A, and in paper 2 sections 2–6, traces to
a script here. Not traced (no persisted script): paper 1's 10²⁷ clock comparison and
the fabrication-scatter estimate of section 6. `ssh_common.py` holds the
lattice builders (t₁t₂ = 1 convention); the `verify_return.py` / `law_check.py` /
`derive_verify.py` set is the counterpart session's independent
implementation (t₂ = 1 convention). Requires only numpy.

```
cd scripts && for s in *.py; do [ "$s" != ssh_common.py ] && python3 "$s"; done
```

| script | checks |
|---|---|
| recursion_check.py | decimation vs direct inversion, 4×10⁻¹⁶ |
| curvature_law_check.py | curvature law vs finite differences, generic profiles |
| asym_check.py | both edges vs the per-edge law; 60×/151×/304× at N=100/250/500 |
| hole_check.py | near-critical curve stable in η and N; channel disentangling angles |
| tilt_cost.py, tilt_cost2.py | real vs imaginary NNN; S∘K pairing; mode reshaping |
| bubble.py | warp-wall profile: pinning, blindness curve, evenness, preamplification, SNR |
| derive_check.py | single-spike leak structure of the shift-law derivation |
| cross_term_check.py | the A–A/B–B cross term: envelope tilt, boundary identity, warped-chain 5%, preamplification ∝ N^2σ |
| reciprocal.py | counterpart's law verified across conventions; gauge-factor closure |
| verify_return.py, law_check.py, derive_verify.py | counterpart session's set |
| exploratory/kernel_law.py | counterpart diagnostics, no pass/fail criteria; provenance only |

## Contact

Ben Watson — ben.watson.research@proton.me
