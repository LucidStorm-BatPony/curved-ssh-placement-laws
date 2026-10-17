# The Imager Derivations — Complete and Self-Contained
### Every load-bearing proof from the tidal-curvature imager project, written out in full

**Who this is for:** Lucid, working alone or with any collaborator/AI, with no access to the original conversations.
**How to read it:** Every symbol is defined when it first appears. Every algebra step is shown. If a step feels like a jump, it's flagged with *[why this works]*.
**Status tags:** [VALIDATED] = matches published work or exact numerics · [COMPUTED] = our numerics, internally consistent · [OPEN] = unresolved.

---

## 0. Notation

| Symbol | Meaning | Units |
|---|---|---|
| n | site or cell index along the chain | — |
| N | number of unit cells | — |
| t₁(n) | intra-cell hopping (bond inside pair n) | energy |
| t₂(n) | inter-cell hopping (bond between pair n and n+1) | energy |
| σ | curvature/warping parameter (σ=0 is flat) | — |
| aₙ | zero-mode amplitude on A-site of cell n | — |
| E | energy at which we probe | energy |
| G(E) | Green's function | 1/energy |
| ρ(E) | density of states at energy E | 1/energy |
| t_C | qubit–chain coupling | energy |
| Γ | qubit decoherence rate | 1/time |
| ω | qubit angular frequency (ℏω = photon energy) | 1/time |
| P | dissipated power (the observable) | watts |

Convention: ℏ = 1 inside derivations except where power is computed; t₂ = 1 sets the energy unit.

---

## 1. The Green's Function and Why the Recursion Is Exact

### 1.1 Definition
The Green's function of a system with Hamiltonian H is defined by:

  **(E − H) G(E) = 1**  →  **G(E) = (E − H)⁻¹**

*[why this works]* This is just matrix inversion. G answers: "if I drive the system at energy E, how does it respond?" For any finite H you could invert directly. The problem is the semi-infinite lead: H is infinite-dimensional, so direct inversion is impossible.

### 1.2 The density of states lives in the imaginary part
Add a tiny imaginary piece to the energy, E → E + iη (η → 0⁺). Write G in the eigenbasis of H (eigenvalues Eₖ, eigenvectors |k⟩):

  G(E + iη) = Σₖ |k⟩⟨k| / (E − Eₖ + iη)

Take the imaginary part of the diagonal element at site n:

  Im Gₙₙ = Σₖ |⟨n|k⟩|² · Im[1/(E − Eₖ + iη)] = −Σₖ |⟨n|k⟩|² · η/((E−Eₖ)² + η²)

As η → 0, the Lorentzian η/((E−Eₖ)²+η²) becomes π·δ(E−Eₖ) (a spike exactly at each eigenvalue). Therefore:

  **ρₙ(E) = −(1/π) Im Gₙₙ(E) = Σₖ |⟨n|k⟩|² δ(E − Eₖ)**

Read in words: the local density of states at site n is a count of the system's energy levels, each weighted by how much probability that level has at site n. This is the bridge between "abstract inverse matrix" and "how many states can my qubit couple into, right here."

### 1.3 The recursion (decimation) — derived, not asserted
Take a chain: site 1 coupled to site 2 by hopping t, site 2 coupled onward to the rest. Write the eigenvalue problem (E − H)ψ = source at the surface. Row for site 1:

  (E − ε₁)ψ₁ − t ψ₂ = source
Row for site 2 (coupled to site 1 and to the "rest," whose surface Green's function is g_rest):

  ψ₂ = g_rest · t ψ₁   *(the rest of the chain responds to being driven by site 1 through the bond t)*

Substitute the second line into the first:

  (E − ε₁ − t² g_rest) ψ₁ = source

Compare with the definition of a surface Green's function, (E − ε_eff) g = 1. The entire rest of the chain has been replaced by a single complex correction to site 1's energy:

  **Σ = t² g_rest   (the self-energy)**
  **g₁ = 1 / (E − ε₁ − t² g_rest)**

*[why this is exact]* Nothing was approximated. We solved site 2's row exactly and substituted. Repeating the move site by site — each new surface Green's function built from the previous one — is algebraically identical to inverting the full matrix, but costs N steps instead of N³. This is the "fuzzy logic bubble" architecture made formal: each layer's response, compressed into one number, becomes the boundary condition of the next layer. [VALIDATED — recursive vs direct inversion agree to ~10⁻¹⁵ in our runs]

For the semi-infinite uniform lead (all hoppings t_L, on-site 0), the recursion must reproduce itself: g = 1/(E − t_L² g). Solve the quadratic:

  t_L² g² − E g + 1 = 0  →  **g_lead(E) = (E − i√(4t_L² − E²)) / (2t_L²)**  for |E| < 2t_L

(The root with negative imaginary part is chosen so the lead absorbs — retarded response.) At E=0: g_lead = −i/t_L. The lead contributes a purely imaginary self-energy at zero energy — it is a pure absorber there. This is what makes the LDOS finite instead of a delta spike.

---

## 2. From Density of States to Power (the observable chain)

### 2.1 Fermi's golden rule
A qubit at energy E, coupled with matrix element t_C to a continuum with density of states ρ(E), decays at rate:

  **Γ = 2π t_C² ρ(E)**   (ℏ=1)

*[why squared]* The transition probability amplitude is proportional to the coupling t_C; probability is amplitude squared. *[why ρ]* The qubit can only decay into states that exist; ρ counts them per unit energy at the qubit's energy.

With the surface Green's function: ρ(E) = −(1/π)Im G^S(E), so

  **Γ = −2 t_C² Im G^S(E)**

Weak coupling matters twice: (i) t_C ≪ bulk gap keeps the qubit's back-action from deforming the topology it measures (back-action is O(t_C²)); (ii) the same t_C² suppresses the signal — the fundamental coupling/protection tension of the device.

### 2.2 Power
Each decoherence event releases one qubit quantum, energy ℏω. Events happen at rate Γ. Therefore:

  **P = Γ ℏω = 2π t_C² ρ(0) ℏω**

Numbers used throughout [COMPUTED, inputs cited]: ω/2π = 5 GHz → ℏω = 3.3×10⁻²⁴ J; Γ_on = 10⁶/s → P_on ≈ 3.3 aW. Landauer floor at 15 mK: kT ln2 = 1.4×10⁻²⁵ J → 23× headroom (thermodynamics is not the limit; the detector is).

### 2.3 The six-step causal chain, with the equation at each step
1. Curvature sets the bonds: t₁(n) = t₁·((2n−1)/(2N−1))^σ, t₂(n) = t₂·((2n)/(2N−1))^σ [VALIDATED — arXiv:2504.16200]
2. Bonds set the zero-mode shape: aₙ₊₁/aₙ = −t₁(n)/t₂(n) (derived in §3)
3. Shape sets the local density of states: ρ_edge(0) = |a_edge|² / Σₙ|aₙ|² × (lead broadening factor)
4. Density of states sets the rate: Γ = 2π t_C² ρ_edge(0)
5. Rate sets the power: P = Γ ℏω
6. Detector reads ΔP = P(σ) − P(σ_ref) against noise NEP/√τ.

Every arrow is one of the derivations in this document. Nothing else enters.

---

## 3. The Zero Mode Is a Product (the heart of everything)

### 3.1 Setup
Chiral symmetry: H only connects A-sites to B-sites. Define S = (+1 on A, −1 on B). Then SHS = −H. Consequence: eigenvalues come in ±E pairs; a state at exactly E=0 can live on one sublattice alone.

### 3.2 Derivation of the product form
Look for a zero-energy state with all B-amplitudes zero: ψ = (a₁, 0, a₂, 0, …). The eigenvalue equation Hψ = 0, evaluated on B-site of cell n (the only equations not automatically satisfied):

  t₁(n)·aₙ + t₂(n)·aₙ₊₁ = 0

*[why]* B-site n touches exactly two A-sites: its own cell's A (bond t₁(n)) and the next cell's A (bond t₂(n)). Zero energy demands these contributions cancel. Solve:

  **aₙ₊₁ = −[t₁(n)/t₂(n)] · aₙ**

Iterate from the edge:

  **aₙ = a₁ · ∏ₖ₌₁ⁿ⁻¹ ( −t₁(k)/t₂(k) )**

If |t₁/t₂| < 1 the amplitude shrinks geometrically with n: the state is exponentially localized at the left edge, with localization length ξ set by ln|t₂/t₁|. This product IS the probability wave; |aₙ|² is where the particle sits. [VALIDATED — matches arXiv:2504.16200 Eqs. 19–20]

### 3.3 Existence bookkeeping (index theorem, used by the memory thread)
Count equations vs unknowns: N_A unknowns (A-amplitudes), N_B constraint equations (one per B site). Guaranteed solutions on A: N_A − N_B. An odd chain (N_A = N_B + 1) therefore has EXACTLY one zero mode, pinned at E=0 regardless of any hopping values — this integer is the winding number and equals the Witten index of the SUSY formulation. [VALIDATED numerically: E₀ = 0 to machine precision, 100% sublattice weight]

---

## 4. The Placement Law (sensitivity = gradient × footprint)

### 4.1 What the probe reads
The probe couples at the edge site; the LDOS there is the normalized probability at the edge (times lead broadening, which is σ-independent to leading order):

  ρ_edge(0) ∝ |a₁|² / Σₙ |aₙ|²  = 1 / Σₙ |aₙ/a₁|²

*[why normalization matters]* This is the crucial structural fact: the edge reading depends on the amplitude at EVERY site, because the state must carry total probability 1. The footprint enters through the normalization sum.

### 4.2 Insert curvature and take the log
Let curvature multiply each bond by a metric factor: t(k) → t(k)·m(k), with m(k) = 1 + ε·f(k), ε small, f(k) the metric profile at bond k. Each ratio becomes

  t₁(k)/t₂(k) → [t₁(k)/t₂(k)] · [m₁(k)/m₂(k)]

Define w(n) ≡ |aₙ/a₁|². Take logs (products → sums):

  ln w(n) = 2 Σₖ₌₁ⁿ⁻¹ ln|t₁(k)/t₂(k)|  +  2 Σₖ₌₁ⁿ⁻¹ [ln m₁(k) − ln m₂(k)]

Expand ln m ≈ ε·f for small ε:

  ln w(n) = [flat-space part] + 2ε · Φ(n),  where **Φ(n) ≡ Σₖ₌₁ⁿ⁻¹ (f₁(k) − f₂(k))**

Φ(n) is the ACCUMULATED METRIC TILT from the edge out to cell n — the running total of how much the two bond species have been differentially stretched along the way.

### 4.3 Differentiate the observable
ρ_edge ∝ 1/Σₙ w(n). Then:

  d ln ρ_edge/dε = −(1/Σ w) · Σₙ (dw/dε) = −(1/Σ w) · Σₙ w(n) · d ln w(n)/dε = −Σₙ w(n)·2Φ(n) / Σₙ w(n)

  **d ln ρ_edge/dε = −2 ⟨Φ⟩_footprint**

where ⟨·⟩_footprint is the average weighted by the state's own probability distribution w(n)/Σw. **This is the placement law:** sensitivity equals the accumulated metric tilt, averaged over where the state actually lives. [DERIVED + VERIFIED, Aug 2026: closed form vs finite-difference numerics to 0.1% on the power-law family and on generic random smooth metric perturbations; verified independently at EACH edge of the even chain against the per-edge pairing form (left mode: Φ from t₁(k)/t₂(k); right mode: Φ from t₁(m)/t₂(m−1)); quiet-edge responsivity is broadening-independent (mode physics, not background). Scripts: curvature_law_check.py, asym_check.py.]

**N-scaling of the asymmetry (correction to earlier statements):** the quiet edge's responsivity falls as 1/N (per-bond plateau tilt ~1/2N times a fixed footprint), so the two-edge asymmetry GROWS LINEARLY with chain length: 60× (N=100), 151× (N=250), 304× (N=500). The old "~300× at N=250" figure was a rounding artifact (0.20/0.001 with the small number quoted to one digit; true values +0.203/−0.00134 → 151×). The asymmetry is a scaling law, not a single number.

### 4.4 Two corollaries that carry the paper
**(a) Uniform is invisible — exactly.** If the metric change is uniform, f₁(k) = f₂(k) for all k (both bond species stretched identically), then Φ(n) = 0 for every n, and the sensitivity vanishes identically — not to first order, exactly, for the zero mode. *[This is the lattice equivalence principle: a uniform potential is unobservable; only its variation couples.]* Caveat for honesty: this exactness is a property of the chirally protected zero mode; finite-energy observables ARE scale-sensitive. A uniform rescaling that includes the probe coupling is also invisible for a different reason (the comoving-frame argument); one that excludes the probe coupling is visible (the Pound–Rebka configuration). State which configuration you mean.

**(b) Placement decides everything.** ⟨Φ⟩ is large only where the state's footprint w(n) overlaps the region where f varies steeply. For the power-law warping ((n/N)^σ varies steeply at small n, plateaus at large n): a left-edge state sits on the steep region (large ⟨Φ⟩); a right-edge state sits on the plateau (⟨Φ⟩ ≈ 0). Same chain, same curvature: responsivities differ by 151× at N=250 [−0.00134 vs +0.203 in d ln ρ/dσ at σ=0.5], growing linearly with N (60×/151×/304× at N=100/250/500). **The falsifiable headline prediction of the paper — an asymmetry AND its scaling law.**

---

## 5. SNR Arithmetic (why "real but slow")

Signal: a fractional warping change δσ produces δP = P_on · |d ln ρ/dσ| · δσ. With P_on = 3.3 aW, responsivity 0.20, δσ = 0.01: **δP ≈ 6.6 zW.**
Noise: detector NEP = 30 zW/√Hz [demonstrated hardware]; integrating τ seconds gives noise = NEP/√τ.
Shot noise of the dissipation itself: ℏω·√(Γ/τ) ≈ 3 zW at τ=1 s — 10× below the detector. **The system is detector-limited**, so bolometer improvements convert one-for-one into sensitivity (the first lever to pull).

  SNR(τ) = δP·√τ / NEP → **≈ 2.2 at τ = 100 s; ≈ 22 at τ = 3 h.** [COMPUTED, all inputs cited]

---

## 6. Appendix: The Memory Corrections (derived in the final sessions)

**(a) Doublet splitting** of a finite topological chain: dE ∝ exp(−N/ξ) — two edge modes tunnel-coupled through the bulk. Retention (hold) time of a written bit at Δ=0 is t_hold ≈ ℏ/dE (the bit is a superposition of the doublet and oscillates between edges at the splitting frequency). Practical retention is additionally capped by T₁ (photon loss deletes the excitation): the device is a LATCH (~100 µs class), not an archive.

**(b) Write-time scaling — correcting the script's comment.** The adiabatic write sweeps a staggered (Rice–Mele, chiral-breaking) tilt Δ through the avoided crossing at Δ=0, whose gap IS the splitting dE. Landau–Zener adiabaticity requires sweep rate v ≪ dE², so **T_write ∝ 1/dE² ∝ t_hold².** Retention and write speed fight through the same exponential. NOT "write slows only linearly" — that claim in ssh_memory_unified.py is wrong.

**(c) The two-phase write protocol (the fix).** Barrier height is set by chiral-SAFE knobs (t₁/t₂ ratio, σ); the write tilt is the chiral-BREAKING knob (staggered Δ). Sequence: (store: barrier high, Δ=0) → (write: transiently push t₁/t₂ → 1 to open the gap, sweep Δ fast, restore barrier) → (store). Write through an open door, store behind a thick wall. Chirality analysis guarantees the barrier move never unpins the modes. [Same trick as flux-qubit gating; the design rule that must never be violated: no static A–A or B–B terms.]

---

## 7. What Is NOT in This Document [OPEN list]
- Physical mechanism writing σ onto a superconducting chip (tunable couplers are the candidate; not designed).
- Drift stability between calibrations; noise correlation across arrays (decides averaging vs common-mode strategy).
- The hold test and two-phase write demonstration (specified above; not yet coded).
- 2D skin / higher-order (corner-mode) extension — later papers.
- External validation of the readout layer (lead + calorimetric observable): our numerics only.
