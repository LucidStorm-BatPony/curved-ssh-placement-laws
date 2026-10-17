# Cold review: curved-ssh-placement-laws

Oct 17, 2026 · @Ben Watson

## Verdict

The mathematics holds; the device does not, as written. Every script runs, and every quoted number reproduces except one (the 10¹³ contrast). The curvature placement law (paper 1, §4) and the single-bond shift law (paper 2, §3) are both correct, and I re-derived them by hand.

Three things are wrong. (1) Paper 1's readout: the far-end lead cannot broaden the probed mode — the probed-site LDOS is set entirely by the numerical broadening η, so the absolute power (3.3 aW) rests on a linewidth the paper never specifies; with the coherence the paper assumes, the qubit and the edge mode are strongly coupled and the power is \~100× smaller. (2) Paper 2's "kernel exactly diagonal at leading order" is false once the shift sits on both sublattices, which the physical encoding requires: the B–B bonds reshape the A-sublattice mode at O(w²), a 4–5% leading-order correction on the warped chain that the addendum misattributed to the quartic term. (3) The superconducting implementation is never tested against on-site (frequency) disorder, the disorder class such chains actually have; hopping disorder, the only one tested, is the one SSH is famously immune to.

Below those sit overclaims a referee would strike (preamplification is an N=100 number that scales as N^2σ; "equivalence principle"; Landauer; the "methodological novelty"), one missing body of literature (tilted-cone lattices as shift metrics, which pays part of paper 2's "standing debt"), and housekeeping. None of it is fatal to the placement laws themselves. The honest pitch is narrower than the abstracts: a compact design formula and its N-scaling, verified; a device sketch that needs its loss channel designed before any number in §5 means anything.

## Reproduction ledger

All 14 scripts ran on a fresh clone (numpy 2.5.3, under a second each). Every quoted number is reproduced except the 10¹³ contrast, which has no script and does not come out at the stated broadening.

| Claim (where) | Quoted | Reproduced | Note |
| --- | --- | --- | --- |
| Decimation vs direct inversion (p1 §3.1) | \~10⁻¹⁵ | 4.3×10⁻¹⁶ | ok |
| Curvature law vs finite difference, power-law family (p1 §4.2) | 0.1% | 0.004–0.06% at σ≤0.5; 3–5% at σ=1 | as stated in App. A |
| Generic random smooth perturbations | 0.1% | 0.03–0.09% | ok |
| Left/right responsivity, N=250 (p1 §4.3) | +0.203 / −0.00134 | +0.20311 / −0.001343 | ok; left-edge ratio to law is 1.0011, i.e. three digits, not "four" |
| Asymmetry 60×/151×/304× at N=100/250/500 | yes | 59.8 / 151.3 / 304.0 | ok |
| Quiet edge η-independent | yes | −0.001343 at η=10⁻³ and 10⁻⁴ | ok |
| Near-critical +2.26 at r=0.97, 3.6× signal loss (p1 §4.4) | yes | +2.2599; LDOS ratio 0.281 | ok |
| Topological/trivial contrast (p1 §3.3) | \~10¹³ | 2.8×10⁶ / 9.6×10⁻⁶ = 3×10¹¹ at η=10⁻⁷, N=250 | **not reproduced**; ratio scales as η⁻², needs η≈10⁻⁸; no script |
| Real NNN unpinning E₀=−0.73t′ (p2 §2) | −0.73 | −0.7297 (both conventions) | ok; convention-independent, drop the parenthetical |
| Imaginary NNN pinning, w=0.1, 1% hopping disorder | ≤10⁻¹⁶ | median 5×10⁻¹⁷ | ok |
| ±E pairing with disorder | <10⁻¹⁴ | 9.3×10⁻¹⁵ | ok |
| Single-spike leak, amplitude (p2 §3) | 5 digits | ratio 1.00000, neighbours 10⁻¹⁶ | ok (single bond only — see Issue 2) |
| Single-bond law K\_bb=−p/t₂² across conventions | 0.9996–1.0000 | 0.9978–1.0000 warped, 1.0000 flat | ok |
| Preamplification 85× / 72× (p2 §4) | yes | 84.7× (t₁t₂=1), 71.9× (t₂=1) | ok at N=100 only — see §6 |
| Blindness curve, machine zero by cell 30 | yes | 8.9×10⁻¹⁶ at 30, 0 at 50 | ok |
| Bubble SNR ≈16–20 at 100 s | yes | 15.9 / 19.9 | arithmetic ok; inherits Issue 1 |
| Channel angles 38° / 21° (p2 §6) | yes | 37.7° / 21.15° | ok, but not the same computation — see §7 |
| B–B bonds: log-log slope 2, η² background | yes | slope 2.000 | ok; the zero mode is in fact unchanged to all orders, not just O(w²) |
| A-shape invariance "O(w⁴)" (derive\_verify test 4) | slope \~4 | slope 4.8 | **test cannot see the failure** — see Issue 2 |

## Issue 1 — paper 1: the lead is at the wrong end, so the absolute power is undefined

The lead does not broaden the probed mode. Paper 1 §3.1–3.2 says the far-end lead "endows the otherwise singular zero-mode response with a finite width"; the derivations write ρ\_edge = |a₁|²/Σ|aₙ|² × (lead broadening factor). On the even N=250 chain with the lead at the far end, the probed-site LDOS is ρ·πη = 0.8660 = |a₁|² at every η from 10⁻⁵ to 10⁻¹¹: it is 1/(πη) exactly, and the left mode's weight at the lead end is e^(−348) ≈ 10⁻¹⁵¹. The width the papers call "engineered" is the numerical η, chosen anywhere between 10⁻³ and 10⁻⁷.

What follows for §5. The responsivities d ln ρ/dσ are η-independent, so paper 1's laws survive. The absolute Γ = 2π t\_C² ρ(0) does not: with ρ(0) = |a₁|²/(πγ), Γ = 2 t\_C² |a₁|²/γ, and γ, the edge mode's physical half-width, is nowhere specified. Two branches:

1. Chain elements with the \~100 µs coherence the paper assumes for the probe: γ ≈ 10⁴ s⁻¹. Γ = 10⁶ s⁻¹ then needs t\_C ≈ 2π × 12 kHz ≫ γ — the strong-coupling (hybridised) regime, where the golden rule does not apply and the excitation Rabi-oscillates between qubit and edge mode instead of decaying. Dissipated power is capped near ℏω·γ ≈ 30 zW, not 3.3 aW; a 1% signal is \~0.3 zW, SNR ≈ 0.1 at 100 s.
2. A deliberately lossy chain, γ ≳ 10⁶–10⁷ s⁻¹ (element T₁ of 0.1–1 µs), with t\_C ≈ 0.1–0.3 MHz. Then 3.3 aW is reachable — but the power leaves through the chain's own loss channel, at the probed end, not through the far-end cold load. That channel is the calorimeter's input and has to be designed.

The cited detector fixes which branch is meant. Kokkoniemi et al. 2020 measures microwave power delivered through a 50 Ω transmission line into a graphene absorber (30 zW/√Hz at 55 mK, 503 MHz probe; thermal-fluctuation limit 12 zW/√Hz); it does not measure heat deposited in a substrate "at the cold stage". So the architecture that works is branch 2 with the loss channel being a line coupled to the probed end at rate γ\_line, feeding the bolometer; t\_C ≪ γ\_line is then the stated weak-coupling condition, and the far-end lead can be dropped from the story.

Two smaller points in the same section. P = Γℏω assumes the qubit sits at unit excitation; a continuously pumped two-level system reaches that only with a pump rate ≫ Γ, which broadens the qubit by the same amount. And at N=250 the near-horizon bonds are 2–6% of nominal — with t₂ = 100 MHz, t₁(1) ≈ 2 MHz — below the "demonstrated 10–250 MHz" range the table cites and comparable to a low-MHz t\_C, so weak coupling fails locally even in branch 2 unless t\_C is set against the local bond, not the nominal one.

## Issue 2 — paper 2: the kernel is not diagonal once the shift sits on both sublattices

The single-bond derivation is right; its fourth step is not general. Step 4 ("the second-order change to the A-sublattice shape is a pure renormalization") uses V ψ⁽¹⁾ = 0, which holds because V is A-only and ψ⁽¹⁾ is B-only. The physical encoding is 2w sin k × identity — the shift on both sublattices — and then V = V\_AA + V\_BB, and V\_BB acts on the leak. The second-order A correction solves

```latex
h^{\dagger}\alpha^{(2)} = -V_{BB}\,\psi^{(1)}_B ,\qquad \psi^{(1)}_B(n) = -\,i\,w\,\frac{a_{n+1}}{t_1(n)}
```

and the right-hand side is w²(1−r²) aₙ/t₁ in the bulk (with a sign-flipped boundary term at n = 1). The solution is a linear-in-n tilt of the A envelope: αₙ/aₙ = 1 + φ₁ − (n−1)·w²(1−r²)/t₁². The A-sublattice shape changes at O(w²).

Measured, flat chain, uniform w = 0.01 on all bonds: αₙ/aₙ = 0.999975, 1.000025, 0.999875, 0.999725, 0.999575, … (slope −1.42×10⁻⁴ per cell; predicted −1.5×10⁻⁴). With w on A–A bonds only the ratio is a constant 0.999975, as Step 4 says.

Why every flat-chain check still passed: at the edge site the bulk tilt and the boundary term cancel exactly in the normalisation (2φ₁ = −‖ψ⁽¹⁾‖², a one-line identity using ⟨n⟩ = 1/(1−r²)), so the uniform-w response on the flat chain equals the diagonal law to 10⁻⁵ — a cancellation, not diagonality. On the warped chain it does not cancel. Uniform shift on both sublattices divided by the A–A-only (= diagonal-law) response, in the w → 0 limit:

| σ | 0 | 0.25 | 0.5 | 0.75 | 1.0 |
| --- | --- | --- | --- | --- | --- |
| ratio | 1.0000 | 0.9578 | 0.9466 | 0.9510 | 0.9652 |

At σ = 0.5 the ratio is 0.9466 at w = 10⁻³, 0.9473 at 3×10⁻³, 0.9559 at 10⁻²: it is O(w²), the same order as the law. The addendum's "−1.85 predicted vs −1.80 measured, the \~3% gap is the quartic correction" is this term, misattributed. The repo already shows it: kernel\_law.py prints "diagonal-only share of R\_quad = 84.4%" for the flat-chain bubble and 96.8% for the warped one, with the whole off-diagonal weight at dm = 1 — the A–A bond and its adjacent B–B bond. Paper 2 §4's "exactly diagonal at leading order … immediate-neighbor cross term entering beyond leading order" states the opposite of its own numerics.

The test that was supposed to catch this cannot. derive\_verify.py test 4 reports 1 − cos\_sim(A part) ∝ w^4.8 and reads it as "A-shape invariant to O(w⁴)". But 1 − cos\_sim is quadratic in the shape change, so an O(w²) reshaping produces exactly O(w⁴). The slope 4.8 is consistent with the reshaping, not against it.

Fix. State the law as exact for A-sublattice bonds (it is) and add the cross term for two-sublattice profiles — it is one more line of the same perturbation theory, and it keeps the footprint structure (the tilt is weighted by the same aₙ). The derivation's "the entire disturbance exits through exactly one site" and "pure renormalisation" stay true for the leak; the sentence to delete is the one that promotes a cancellation on the flat chain into a theorem. One tightening for free: V\_BB alone leaves the zero mode unchanged to all orders (hβ = 0 forces β = 0, then h†α = 0 gives α = a), not merely at O(w²), so the η² background story is the whole story for B-only bonds.

## Issue 3 — paper 1 device: on-site disorder is the one that matters, and it is untested

Both papers test only hopping disorder, which SSH is immune to by construction (a chiral perturbation cannot move the mode). Superconducting elements scatter in frequency — that is an on-site term, it breaks both S and S∘K, and the vulnerability ledger names it as the enemy without ever pricing it. Warped odd chain, N=100, 200 realisations, Gaussian on-site disorder (units: t₂ = 1.414):

| On-site σ | as % of t₂ | median \|E₀\| | max \|E₀\| | edge weight |
| --- | --- | --- | --- | --- |
| 10⁻⁴ | 0.007% | 6.2×10⁻⁵ | 2.5×10⁻⁴ | 0.866 |
| 10⁻³ | 0.07% | 6.7×10⁻⁴ | 2.4×10⁻³ | 0.866 |
| 10⁻² | 0.7% | 6.3×10⁻³ | 2.7×10⁻² | 0.865 |

The mode's shape barely moves (edge weight stays 0.866, so the laws are safe); its energy moves by ≈ 0.6× the scatter. With t₂ = 100 MHz: 1% transmon frequency scatter is 50 MHz, half of t₂, and shifts the mode by \~30 MHz — off resonance from a 5 GHz qubit by far more than any MHz linewidth, and larger than the near-horizon bonds (t₁(1) ≈ 2 MHz at N=250). Keeping the mode inside a \~1 MHz linewidth needs element frequencies aligned to \~1 MHz, i.e. 2×10⁻⁴ of 5 GHz, across 500 elements — a trimming specification, and drift in it is the real calibration problem, not the hopping scatter §6 discusses. The paper needs this table, or one like it, before "every parameter … cited to demonstrated hardware" can stand.

## Overclaims and framing

**Preamplification is an N=100 number.** Same bubble geometry as bubble.py, w₀ = 0.02:

| N | 50 | 100 | 200 | 400 |
| --- | --- | --- | --- | --- |
| warped/flat | 41.8× | 84.7× | 174× | 369× |
| w₀/t₁(1) | 0.28 | 0.40 | 0.57 | 0.80 |

It scales as N^2σ because the horizon-end bonds vanish as N^−σ: the "preamplifier" is the statement that the local velocity goes to zero at the horizon, so any absolute shift becomes a large local tilt there. The same table shows the expansion parameter w₀/t₁(1) reaching 0.8 — the "two-percent shift" demonstration sits at the edge of perturbative validity at N=100 and outside it at the companion paper's N=250. State the scaling, and define the operating point by w̃ at the edge, not by absolute w.

**The quiet end is quiet by construction.** On the plateau, Φ\_R after j cells ≈ j/(2N), and ⟨j⟩ = r²/(1−r²) = 1/3 for r = 0.5, so the quiet-edge responsivity is −2⟨Φ⟩ ≈ −1/(3N): −0.00133 at N=250 against the computed −0.00134. The asymmetry and its linear growth follow from the parametrisation x ∈ (0,1\] stretched over N cells; a referee will say so. The sensitive end is the horizon end (v → 0 there in Rajbongshi–Modak's metric) — the papers never say this, and it is the physical content of the asymmetry.

**The curvature law is two lines from a textbook result.** The product form is the standard SSH zero-mode solution (Rajbongshi–Modak Eqs. 18–21; Asbóth–Oroszlány–Pályi); the law is its log-derivative. That is fine — it is a useful design formula — but "a result that reshaped the design" and "an equivalence principle realized at the lattice level" oversell it.

**"Equivalence principle" and "Landauer" should go.** H → λH leaves every eigenvector unchanged, not only the zero mode's; E = 0 is special only as the fixed point of E → λE. That is scale invariance. The Landauer bound is about erasure and is irrelevant here; the number that matters is ℏω/kT ≈ 16 (thermal occupation e⁻¹⁶). And "one-percent metric change" means δσ = 0.01 in the exponent — a position-dependent change of up to \~6% near the horizon end.

**Name the symmetry class.** S∘K is an antiunitary operator with (S∘K)² = +1 that anticommutes with H: that is particle-hole symmetry, class D (time reversal is broken by the imaginary hopping; chiral symmetry is gone). The shifted chain is a 1D class-D system with a ℤ₂ invariant, and the odd-chain unpaired mode is the ℤ₂ statement — the same protection as a Kitaev-chain Majorana. Saying so replaces the invented phrase "antiunitary chiral symmetry" with a known one and connects the pinning to a literature.

**Missing literature, paper 2.** Tilted Dirac/Weyl cones as metrics with a shift are established: position-dependent tilt on 1D tight-binding chains realising Dirac fermions near horizons is worked out in [Horizon physics of quasi-one-dimensional tilted Weyl cones on a lattice](https://link.aps.org/doi/10.1103/PhysRevResearch.4.033237), Phys. Rev. Research 4, 033237 (2022), and the tilt ↔ Painlevé–Gullstrand identification runs through Volovik's type-II Weyl work. Part of the "standing debt" dictionary is paid there; the novelty narrows to the edge-mode response under tilt. Cite it.

**Drop the "methodological novelty".** Independent reimplementation in a second convention is standard practice, and two sessions of one model under one director are not independent in the sense a referee means. Keep Appendix B as a description of the process; it is a good one.

## Traceability and housekeeping

- README: "All numbers quoted in the papers trace to a script here" is false. Untraceable: the 10¹³ contrast (and it needs η ≈ 10⁻⁸, not the appendix's 10⁻⁶–10⁻⁷), the 10²⁷ clock no-go (beat.py never persisted), the "two orders of magnitude" fabrication-scatter comparison in §6. Either persist scripts or soften the sentence to "every number in §4 and App. A".
- Paper 2 abstract quotes "condition number ≈ 5" while §6 says condition numbers are deliberately not quoted because they are normalisation-dependent. Pick one.
- "Verified … to four digits" (p1 §4.3): the left edge is 1.0011 at N=250 and drifts to 1.0025 at N=500 (the near-horizon gap approaches η at fixed η = 10⁻³). Three digits, or rerun at smaller η.
- The 38° vs 21° comparison (p2 §6) is not a convention check. hole\_check.py evaluates both elements at a w = 0.02 bias, where the warped element's curvature responsivity has already collapsed from +0.203 to +0.032; law\_check.py evaluates elements A and B at zero bias. Same qualitative verdict, different computation — say that instead of "reflecting the different effective shift bias … in the two hopping conventions".
- Paper 2 §2's "E₀ = −0.73 t′ (in the t₁t₂ = 1 convention)": the coefficient depends only on bond ratios and is identical in both conventions (−0.7297). Drop the parenthetical.
- derivations §3.3: N\_A − N\_B is the odd-chain index and equals 1 whether t₁ < t₂ or t₁ > t₂ (the single mode just sits at the other end); it is not the winding number, which is a bulk invariant of the even/periodic chain. The Witten-index statement is right; the winding identification is not.
- Code: verify\_return.py has no `if __name__ == "__main__":` guard, so law\_check.py, derive\_verify.py and exploratory/kernel\_law.py each re-run all of it on import, and the README's loop runs it four times. One guard fixes all three.
- Paper 2 references \[3\] and \[4\] are still marked "verify before submission"; the Clough–Dietrich–Khan one exists, I did not check \[3\].

## Fix list, in order

1. Paper 1 §3 and §5: design the loss channel. Put the dissipative coupling at the probed end (a line to the bolometer at rate γ\_line), state t\_C ≪ γ\_line, pick γ\_line and t\_C so Γ = 10⁶ s⁻¹ is a golden-rule rate, and drop the far-end lead from the readout story (keep it only as the numerical device it is). Recompute §5; the responsivities stand, the absolute power is new.
2. Paper 1 §5: add the on-site-disorder budget and the trimming specification it implies. Say which elements are tunable.
3. Paper 2 §3–4 and the derivations: restrict "pure renormalisation" and "exactly diagonal" to A-sublattice bonds; derive and state the A–A/B–B cross term; replace derive\_verify.py test 4 with a direct measurement of αₙ/aₙ; fix the addendum's "quartic" attribution.
4. Paper 2 §4–5: state preamplification ∝ N^2σ and define the operating point by w̃ at the edge; note the demonstration sits at w₀/t₁(1) ≈ 0.4.
5. Paper 2 §2: call S∘K particle-hole symmetry, class D, ℤ₂; cite the tilted-cone lattice literature in §1 and §8.
6. Paper 1 §1, §4.3, §3.2: cut "equivalence principle", "Landauer", "one-percent metric change"; say the sensitive end is the horizon end and the quiet end is ≈ −1/(3N).
7. README and both appendices: fix the traceability sentence, the 10¹³, the abstract's condition number, "four digits", the 38°/21° explanation, the winding/index conflation, the import guard. Drop the methodological-novelty sentence.

## Checks I ran

The five checks behind Issues 1–3 and the preamplification table are in one script, `cold_review_checks.py` (sent in chat). It runs from the repo's `scripts/` directory against `ssh_common.py` in about a second. Everything else is the repo's own verification set, run unmodified on a fresh clone at commit 49f75af.

Sources opened: [Rajbongshi & Modak, arXiv:2504.16200v3](https://arxiv.org/abs/2504.16200v3) (Hamiltonian Eq. 4, profile, Eqs. 18–21; DOI matches the README); [Kokkoniemi et al. 2020, arXiv:2008.04628](https://ar5iv.labs.arxiv.org/html/2008.04628) (30 zW/√Hz, 55 mK, transmission-line input, 500 ns time constant); [Phys. Rev. Research 4, 033237 (2022)](https://link.aps.org/doi/10.1103/PhysRevResearch.4.033237) (tilted cones on a lattice); [Zaimi et al., arXiv:1910.09926](https://arxiv.org/pdf/1910.09926) and [Delnour et al., arXiv:2302.13771](https://arxiv.org/pdf/2302.13771) exist as cited.
