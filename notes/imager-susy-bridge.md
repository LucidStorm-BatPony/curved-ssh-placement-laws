> **Working note, not for citation.** Design notes for a companion memory-mode thread; the papers and `derivations/` are authoritative.

# Bridge Document: Imager Constraint Algebra → SUSY Memory Architecture

**Purpose:** This document carries the symmetry and constraint structure of the topological tidal-curvature imager (worked out in the imager/white-paper thread, July 2026) into the supersymmetric quantum memory thread ("Light-based computing research"). It replaces the constraint algebra lost with the Fable sessions. Written to be self-contained: usable by Lucid, Cam, or any AI session with no other context.

**Status tags:** [VALIDATED] = checked against published work or exact numerics · [COMPUTED] = our numerics, internally consistent, not externally verified · [OPEN] = unresolved.

---

## 1. The Imager in One Paragraph

A finite Su-Schrieffer-Heeger (SSH) chain — alternating strong/weak hopping — hosts a topologically protected zero-energy edge mode. Spacetime curvature is encoded as position-dependent hopping (the curved-spacetime SSH model, Rajbongshi & Modak, arXiv:2504.16200 [VALIDATED]). A qubit probe couples weakly to one edge; its decoherence rate is Γ = t_C² × LDOS(E=0) at the coupling site (Fermi's golden rule), and each decoherence event dissipates ℏω into a heatsink, so power P = Γℏω is the observable, read by a cryogenic bolometer. Curvature deforms the edge mode's probability distribution → LDOS shifts → power shifts. Sensor mode = watching the energy cost of the system maintaining its single protected ground state.

## 2. The Symmetry Structure (the constraint algebra the memory thread needs)

### 2.1 Chiral / sublattice symmetry [VALIDATED]
The SSH Hamiltonian connects only A-sublattice sites to B-sublattice sites (never A–A or B–B). Define the chiral operator S = P_A − P_B (projectors onto sublattices). Then:

  S H S = −H,  S² = 1

Consequences:
- Spectrum is symmetric about E=0: every state at +E has a partner at −E.
- A state at exactly E=0 can be its own partner → can be pinned there, immune to any perturbation that preserves the A↔B structure.
- The zero mode lives entirely on ONE sublattice (all-B amplitudes vanish for the left-edge mode with our conventions).

### 2.2 Symmetry class and invariant [VALIDATED]
- Class: BDI (chiral symmetry + time-reversal + particle-hole, all squaring to +1).
- Invariant: 1D winding number ν ∈ {0, 1}. ν=1 (inter-cell bonds strong) → one zero mode per edge. ν=0 → none.
- Protection: ν cannot change without closing the bulk gap. Small deformations of hoppings — including curvature — cannot remove the zero mode.

### 2.3 What curvature does and does not do [VALIDATED]
- Curvature = position-dependent hopping: t₁(n) = t₁·((2n−1)/(2N−1))^σ, t₂(n) = t₂·((2n)/(2N−1))^σ. Derived from Dirac-in-curved-spacetime: local velocity v(x)=2t(x), Rindler-type metric.
- Curvature PRESERVES chiral symmetry (any position-dependent hopping does — it never introduces A–A or B–B terms). BDI class and winding number are unchanged.
- Curvature therefore deforms the zero mode's SHAPE (its probability footprint becomes asymmetric between edges) without lifting it from E=0. The deformation is the sensor signal.

### 2.4 The zero-mode product structure [VALIDATED — matches paper's analytics]
Solving Hψ=0 on the A sublattice gives the recursion a_{n+1}/a_n = −t₁(n)/t₂(n), hence:

  a_n = a₁ · ∏_k [−t₁(k)/t₂(k)]

Log turns the product into a sum → sensitivity law: d(ln LDOS)/d(curvature) = −(metric gradient integrated over the state's probability footprint) [DERIVED + VERIFIED Aug 2026: closed form vs numerics to 0.1%, generic profiles, both edges]. Uniform metric changes cancel exactly (equivalence principle at lattice level); only gradients couple. Placement rule: probe where footprint overlaps steepest gradient (left/right asymmetry 151× at N=250, growing linearly with N: 60×/151×/304× at N=100/250/500).

## 3. The SSH ↔ SUSY-QM Dictionary

This is the bridge proper. Write H in the sublattice basis:

  H = ( 0    h  )
      ( h†   0 )

where h is the N_A×N_B matrix of hoppings taking B-amplitudes to A-sites.

| SUSY-QM (Witten) | SSH imager |
|---|---|
| Supercharge Q | ( 0 h; 0 0 ) — hops B→A |
| Supercharge Q† | ( 0 0; h† 0 ) — hops A→B |
| SUSY Hamiltonian H = {Q,Q†} | H² block-diagonal: (hh† 0; 0 h†h) |
| Partner Hamiltonians H₊, H₋ | hh† (A-sector) and h†h (B-sector) |
| Isospectrality of partners | hh† and h†h share all nonzero eigenvalues (singular values of h, squared) |
| Superpotential W(x) | the hopping profile t₁(n), t₂(n) — curvature σ deforms W |
| Unbroken SUSY: E₀ = 0 exists | Topological phase ν=1: zero mode exists |
| Broken SUSY: E₀ > 0 | Trivial phase ν=0: no zero mode |
| Witten index Δ = n₊ − n₋ | # zero modes on A minus # on B = winding number (index theorem) |
| Ground state annihilated by Q | Edge mode lives on one sublattice only |

Key identification: **the imager's chiral symmetry IS the SUSY grading; the winding number IS the Witten index.** The toy model's superpotential choice (W=x unbroken vs W=x²−2 broken) maps onto the SSH phase choice (ν=1 vs ν=0).

## 4. What This Gives the Memory Architecture

The memory thread's blocker was: which symmetries to break/impose for the device-specific superpotential. The imager algebra answers the structural part:

1. **Sensor mode = unbroken phase.** ν=1, single zero mode, chiral symmetry intact. The system has ONE protected ground state; perturbations cost measurable reversion energy. (This is the imager as built.)
2. **Memory mode requires engineered degeneracy.** Routes consistent with the algebra:
   - **Two-edge doublet:** a finite ν=1 chain already has TWO near-zero modes (one per edge) split by exp(−N/ξ) tunneling — a natural near-degenerate doublet, directly analogous to the toy model's double-well splitting (24× protection ratio [COMPUTED in memory thread]). Chain length N and localization ξ are the protection knobs.
   - **Domain wall states:** a wall between ν=1 and ν=0 regions binds a zero mode (Jackiw–Rebbi). Multiple walls → multiple modes → multistate memory. Wall positions are the stored information; moving walls = writing.
   - **Curvature as the write field:** σ deforms mode shapes and inter-edge tunneling WITHOUT breaking chiral symmetry — a symmetry-respecting adiabatic write handle, matching the Landau-Zener write dynamics already validated in the toy model.
3. **What must NOT be broken:** any term coupling A–A or B–B (on-site potentials differing between sublattices, next-nearest-neighbor hopping) breaks chiral symmetry, unpins the modes from E=0, and destroys the protection. The memory design space is: deform t₁(n), t₂(n) freely; never introduce sublattice-diagonal terms. [This is the central design constraint.]

## 5. Numbers Worth Carrying Over [COMPUTED unless noted]

- Edge LDOS on/off contrast: ~10¹³ (recursive GF, paper's power-law hopping).
- Left/right placement asymmetry: 151× at σ=0.5, N=250; scales linearly with N (corrected Aug 2026).
- Superconducting platform: f=5 GHz, couplings 10–250 MHz (cited), T₁=100 µs, probe channel 10⁶/s (100× above intrinsic background), 15 mK, Landauer headroom 23×.
- Detector: 30 zW/√Hz demonstrated bolometer; system is detector-limited (shot noise 10× below NEP).
- SNR for 1% σ change: ≈2 @ 100 s, ≈22 @ 3 h.
- Memory-thread toy model: doublet protection ratio 24×; Landau-Zener write validated to ~1%; Witten index counting should use the asymptotic sign rule for W, not tolerance-based counting.

## 6. Open Items [OPEN]

- Device-specific superpotential: which t(n) profile realizes the desired memory well structure on hardware (flux-qubit foothold noted in memory thread).
- Physical mechanism writing σ onto a superconducting chip (tunable couplers are the candidate).
- Drift stability between calibrations (imager); retention time vs doublet splitting (memory).
- Noise correlation structure across multi-element arrays (decides averaging vs common-mode-rejection strategy).
- 2D extension: higher-order topology, corner modes — later papers.

## 7. Provenance

- CST-SSH model: arXiv:2504.16200 (Rajbongshi & Modak).
- Qubit decoherence probe of SSH edges: arXiv:1910.09926; scanning probe prior art: arXiv:2302.13771.
- SUSY-QM framework: Witten index formulation; toy model validated in "Light-based computing research" thread (July 2026).
- Imager physics, placement law, worked example: imager/white-paper thread (July 2026). White-paper skeleton exists as tidal-imager-skeleton.md (~75% complete).
