# Computed: the chiral cost of encoding a shift (II.4 resolved)
### Feed-back to Cold-Boot Run 01's most falsifiable claim, computed in the imager home conversation, 2026-08-06
**Status of everything below: COMPUTED (exact diagonalization, odd warped chain, 201 sites, power-law profile, r=0.5, σ=0.5). Scripts: tilt_cost.py, tilt_cost2.py (persisted alongside this file as of Aug 2026).**

---

## The claim under test (bridge II.4, asserted not computed)
"The known lattice route to a shift is cone tilt via same-sublattice hopping, which breaks chiral symmetry — the protection the entire readout is built on. If it holds, encodability and protection draw from the same account."

## Verdict: FALSIFIED in its strong form; CONFIRMED for the naive encoding; and the correct encoding opens a new readout channel.

**1. The naive form behaves exactly as II.4 feared.** Real same-sublattice (NNN) hopping t′ — the k-even identity term — unpins the zero mode at first order: E₀ = −0.73 t′, linear, verified over four decades. Any real NNN amplitude is a protection catastrophe. II.4's pessimism is correct *for this term*.

**2. But the physically correct shift encoding is a different term, and it costs nothing in pinning.** The lattice form of a shift g_tx is the *current-like* imaginary same-sublattice hopping, iw(c†ₙ₊₂cₙ − h.c.), whose bulk dispersion contribution is 2w·sin k — the odd-in-k identity term that tilts the cone, i.e. the 1+1 shift. Computed: E₀ remains at machine zero (≤10⁻¹⁷) up to w = 0.1, *including under 1% nearest-neighbor hopping disorder over 200 realizations* (median |E₀| ~ 5×10⁻¹⁷ at w = 0.1, versus 1.5×10⁻² for the real form at t′ = 0.02).

**3. Mechanism identified and verified: the protection changes hands, it does not disappear.** The unitary chiral symmetry S does break, exactly as II.4 says. But an *antiunitary* chiral symmetry survives: S∘K (sublattice parity composed with complex conjugation) anticommutes with the full Hamiltonian — S flips the sign of the real NN terms, K flips the sign of the imaginary NNN term. Verified: the entire spectrum remains ±E paired at the 10⁻¹⁵–10⁻¹⁴ level at w = 0.1 with disorder (realization-dependent; machine floor). Protection and shift-encodability do **not** draw from the same account; they draw from adjacent accounts, and the second account honors the same disorder class (real hopping disorder) as the first. The vulnerability ledger is unchanged: on-site terms and *real* NNN remain the enemies; the shift term adds no new vulnerability class.

**4. The pinned mode reshapes — and the reshaping is a readout channel.** Though E₀ stays exactly at zero, the mode's structure responds strongly to w: sublattice polarization falls 1.00 → 0.49, footprint spreads 1.3 → 3.6 cells, edge weight falls 0.87 → 0.25 as w goes 0 → 0.1. Consequently the calorimetric observable acquires a large *shift responsivity*: d ln ρ_edge/dw = −0.9 at w = 0.01, −1.9 at 0.02, −6.6 at 0.05, −22 at 0.08. **The instrument reads g_tx.** The likely mechanism for the growth is the warped chain's soft region: the local gap shrinks toward the coordinate origin as the power-law profile does, so a uniform tilt approaches the local type-II threshold there first — the same footprint-gradient logic as the placement law, now on the shift channel.

**5. Cross-talk, stated honestly.** The curvature responsivity d ln ρ/dσ is not independent of w: it runs +0.20 (w=0) → +0.03 (w=0.02) → −7.3 (w=0.08). Curvature and shift channels are entangled in a single edge observable. A two-parameter metric (σ, w) needs two independent measurements — the two ends, or responsivity plus absolute level — and the optimal disentangling scheme is unsolved.

## What this does to the warp frame
- The encoding-dictionary hole (bridge II.3) now has a computed foothold: the static→stationary extension requires the current-like NNN term, and that term is *protection-compatible*. The formal dictionary derivation (metric → w(x) profile) remains the theory task — this is the existence proof, not the derivation.
- The bridge's DP-10 ladder rung (b) — "pricing the chiral cost of II.4" — is paid: the price of the correct encoding is zero in pinning, finite in cross-talk.
- New falsifiable content for any photonic test: the predicted shift-responsivity curve d ln ρ/dw and the ±E spectral pairing under tilt are both measurable in the same platform as the placement-law test.

## Open, in order of value
1. ~~Position-dependent w(x) — a bubble's two opposite-signed shift walls~~ — **DONE, see Bubble-Wall Run below.**
2. The w-analog of the placement law: derive d ln ρ/dw² as a footprint-weighted integral (the S∘K-protected perturbation theory), so shift sensitivity becomes a design calculation like curvature sensitivity.
3. The disentangling scheme for (σ, w) from two-point measurements.
4. Formal CST-SSH dictionary extension static → stationary (the II.3 task proper).
5. Sign readout (see Bubble-Wall Run, finding 2): a time-odd observable — directional transport, not calorimetry — is required to read the sign of the shift.
6. Dynamics: a moving wall (formation/collapse analog) is untouched; all results here are static.

---

# Bubble-Wall Run (same session, immediately following)
### Position-dependent shift: a 1+1 Alcubierre-style top-hat w(x) with smooth tanh walls, flat inside and outside, structure only in the two opposite-signed gradient walls. Flat chain (r=0.5) primary; warped chain (σ=0.5) cross-check. All COMPUTED.

**1. Protection is profile-independent.** With a full bubble on the chain: |E₀| = 6×10⁻¹⁷, spectral ±E pairing to 9×10⁻¹⁶. The S∘K argument never referenced the profile — K flips the sign of *every* imaginary NNN term wherever it sits — so pinning holds for arbitrary w(x). A warp bubble costs the mode nothing.

**2. The observable is exactly even in the shift — derived, not just observed.** Complex conjugation maps H(w) → H(−w) with an identical spectrum, so ρ_edge(w) = ρ_edge(−w) identically and all odd-order response vanishes. Confirmed numerically: response is quadratic in w₀ over four doublings. Consequence stated plainly: **static calorimetry reads |g_tx|², the magnitude of the shift, and is blind to its direction.** Reading the sign (which way the frame drags) requires a time-odd observable — a directional transport measurement, not a power measurement. This is a real boundary of the instrument class, discovered by the computation.

**3. The blindness curve — bridge II.5 upgraded from argued to computed.** Edge response to a fixed bubble versus its center position: 2×10⁻⁴ at cell 5, 9×10⁻⁵ at 10, 3×10⁻⁷ at 15, 4×10⁻¹⁰ at 20, and *exactly* machine zero from cell 30 onward. The single edge mode is blind to a mid-chain bubble with exponential severity set by its own footprint. The array-as-warp-instrument conversion is now a computed fact, not an argument: each element images its ~ξ neighborhood and nothing else. The pixel is the footprint.

**4. Curvature bias is a shift preamplifier.** The same near-edge bubble (w₀ = 0.02) produces d ln ρ = −1.70×10⁻⁴ on the flat chain and −1.44×10⁻² on the warped chain — an **85× amplification** (earlier text said 70×, from rounding the flat value to one significant figure before dividing — corrected Oct 2026 on regeneration of bubble.py; the counterpart convention gives 72×) from the curvature background's soft local gap. Design statement: operating the imager with an engineered curvature bias amplifies shift response, the same soft-region mechanism as near-critical operation on the curvature channel. Mid-chain blindness is unchanged (machine zero on both chains).

**5. Wall decomposition consistency.** Front-step response plus back-step response equals uniform response plus full-bubble response (−0.0004 = −0.0004), the identity the profiles satisfy — the second-order response respected it numerically at this amplitude.

**6. Detectability with the paper's own hardware.** On the warped chain, the w₀ = 0.02 near-edge bubble is a 1.4% power change: with the worked example's 3.3 aW signal, that is ≈47 zW against the 30 zW/√Hz demonstrated bolometer floor — **SNR ≈ 16 at 100 seconds.** A static analog warp wall parked on one pixel of this instrument, at 2% shift amplitude, is comfortably measurable with cited hardware.

**Scripts:** bubble.py (this run), tilt_cost.py, tilt_cost2.py (prior run). Odd chains, 201 sites, exact diagonalization, η = 10⁻³ broadening as the engineered-Γ proxy.

---

# The Derivation (COMPUTED → DERIVED, 2026-08-06)
### The one-page S∘K perturbation theory for the shift placement law. Every step verified numerically (derive_check.py: single-spike structure to 5 digits, both chains).

**Setup.** Chiral chain H₀ in sublattice blocks: H₀ = [[0, h],[h†, 0]], zero mode |0⟩ = (a, 0) purely on A, real, normalized, with the product structure a_{m+1}/a_m = −t₁(m)/t₂(m). Perturbation: one shift bond of strength w on the A–A link between cells m and m+1: V = iw(|A_{m+1}⟩⟨A_m| − h.c.).

**Step 1 — the first-order correction leaks entirely into B.** V|0⟩ = iw(a_m|A_{m+1}⟩ − a_{m+1}|A_m⟩) ≡ (f, 0) is A-supported, and ⟨0|V|0⟩ = iw(a_m a_{m+1} − a_{m+1}a_m) = 0. Chiral pairing of the excited states (|k,±⟩ = (u_k, ±v_k)/√2 at energies ±E_k) makes the A-components of the first-order sum cancel between the ± partners while the B-components add: |ψ⁽¹⁾⟩ is purely B-sublattice, solving **h ψ⁽¹⁾_B = −f**. *[why this matters: the edge site is an A site, so the reading is untouched at O(w) — the evenness of the observable in w is derived, not just observed.]*

**Step 2 — the energy stays pinned.** E⁽¹⁾ = ⟨0|V|0⟩ = 0. E⁽²⁾ = ⟨0|V|ψ⁽¹⁾⟩ = 0 because V acts only within A and ψ⁽¹⁾ has no A-component. (All orders: the S∘K anticommutation forbids any shift of the unpaired mode from zero — the perturbative statement of the pinning computed earlier.)

**Step 3 — the leak is a single site.** Solve h ψ_B = −f site by site from the closed end. All B-amplitudes vanish until cell m; at cell m: ψ_B(m) = iw·a_{m+1}/t₁(m). At cell m+1 the two contributions are a_m + a_{m+1}t₂(m)/t₁(m), **which the zero-mode ratio makes exactly zero** — and every B-site beyond it stays zero. *[why this works: the same product structure that builds the mode confines its leak. The telescoping cancellation is the zero-mode condition read backwards.]* Verified: one spike, predicted site, predicted amplitude to 5 digits; neighbors at 10⁻¹⁶.

**Step 4 — the reading drops by the leaked probability.** At second order, Vψ⁽¹⁾ = 0 (V is A-only, ψ⁽¹⁾ is B-only), so the O(w²) correction solves Hψ⁽²⁾ = 0: it is proportional to the zero mode itself, fixed by normalization: ψ⁽²⁾ = −½‖ψ⁽¹⁾‖²·|0⟩. The A-sublattice shape is *unchanged*; the entire effect is a uniform renormalization. Hence

> **d ln ρ_edge = −‖ψ⁽¹⁾‖² = −w²·a_{m+1}²/t₁(m)² = −w²·a_m²/t₂(m)²**

the last equality by the mode ratio — recovering the other session's empirical form exactly, and revealing it as one face of a two-faced identity: *the sensitivity is the amplitude the bond ships across, divided by the local escape bond, squared.* In the canonical variable w̃ = w/t₂(m): **d ln ρ = −w̃² a_m²** — pure footprint.

**Physical statement, one sentence:** the shift term pushes protected amplitude off the A sublattice; chirality routes the entire disturbance through exactly one B site; and the edge reading falls by precisely the probability that escaped — sensitivity is leaked probability.

**Corollaries falling out of the derivation for free:** the leading-order kernel is exactly diagonal (each bond's spike occupies a different B site, so cross terms vanish at O(w²) — the other session's falsified pre-registration P1, now derived); and the preamplification is the 1/t₁(m)² (equivalently a_m²/t₂(m)²) factor growing in the warped chain's soft region.

**One corollary corrected by the other session's verification (tear kept visible).** This section originally claimed B–B shift bonds respond at quartic order. Their derive_verify.py measured the B–B response as *quadratic* (log-log slope 2.000). Both are partly right and the resolution is derived: the zero mode genuinely cannot respond at O(w²) (V_BB|0⟩ = 0 stands), and the measured quadratic residual is the **non-topological bulk background transmitted through the Lorentzian broadening** — confirmed by its scaling R_BB ∝ η², constant to four digits across a 30× range of η, with the A–A response η-independent as a zero-mode property must be. In device terms: an artifact channel nine orders below the signal at operating parameters, suppressible as η² by narrowing the engineered linewidth. The original "quartic" attribution was wrong; the mechanism is now identified and stronger than the wrong claim was.

**Status: DERIVED.** Open list updates: item 1 closed; the dictionary task (item 2) inherits the canonical variable w̃ with the derivation behind it.

---

# Reciprocal Verification and Convention Closure (2026-08-06, on receipt of computed-ground-addendum.md)
### The other session reproduced this file's results from scratch; this session verified their new law and closed their flagged discrepancy. All COMPUTED (reciprocal.py).

**1. Their shift placement law is verified in the independent convention.** Single-bond kernel K_bb measured in this session's implementation (t₁t₂ = 1 normalization, distinct from their t₂ = 1) against their closed form −|ψ₀(b)|²/t₂,bridged²: ratio 1.0000 on the flat chain and 0.9996–0.9998 on the warped chain, across **eight decades of kernel magnitude** (b = 0…20). The law holds with each convention's own t₂ inserted — it is convention-covariant, which is the strongest available check short of the analytic derivation.

**2. Their §1 discrepancy is closed, with a different mechanism than they guessed.** The 2× responsivity gap is not sublattice coverage: both implementations apply the NNN term on all sites. It is **absolute hopping normalization** — their bonds (t₂ = 1) vs ours (t₂ = √2), and the law's own 1/t₂² gauge factor predicts exactly the observed factor in the small-w window w ≲ 0.02 (above which the raw-w numbers of the two conventions diverge nonperturbatively — see paper 2, Appendix A) ((√2)² = 2; our symmetric-derivative −0.89 × 2 = −1.78 vs their measured −1.80, residual 1.5% = quadratic-order corrections). Their √2 axis-rescale observation was exactly right; their attribution was wrong; their own law diagnoses it — which is precisely what they predicted the law could do once both codebases were in one place.

**3. The canonical-normalization question is answered, not just flagged.** The invariant variable is the **local dimensionless ratio w̃_b ≡ w_b / t₂(b)**. In that variable the law collapses to pure footprint, K = −|ψ₀(b)|², and the shift placement law becomes structurally identical to the curvature placement law — footprint weight, no gauge factor, convention-free. **Recommendation for the dictionary task: define the lattice shift in local-hopping units.** This retires open item 2 in principle; the formal static→stationary derivation should adopt w̃ from the start.

**Round-trip status, for the ledger:** results reproduced independently in both directions; one pre-registration falsified productively over there; a closed-form law found there and verified here across conventions; a convention item opened there and closed here with mechanism. The scripts of both sessions and the addendum are persisted alongside this file — the "not persistent" caveats on both sides are retired. Remaining open, in order: array error propagation with fabrication scatter, sign readout (second architecture), dynamics (the frontier). (The S∘K analytic derivation, formerly first on this list, is complete — see The Derivation section above.)
