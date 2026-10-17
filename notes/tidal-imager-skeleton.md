> **ARCHIVAL — working notes, not for citation.** These three files are internal design notes kept for continuity. Statuses and numbers in them may lag the papers; the papers and `derivations/` are authoritative.

> **ARCHIVAL (June 2026 planning skeleton).** Status tags and numbers here are SUPERSEDED. Current verification statuses live in imager-derivations.md; current claims in the two paper drafts. Known superseded items: the '~300x' asymmetry (corrected Aug 2026 to 151x at N=250, growing linearly with N); the placement law is now DERIVED + VERIFIED, not merely COMPUTED; near-critical operation IMPROVES responsivity under the power-law profile (July linearized finding overturned).

# A Topological Tidal-Curvature Imager
## Calorimetric Readout of Edge-State Response in Curved-Spacetime SSH Arrays

**Status key used throughout:** [VALIDATED] = checked against published work or exact numerics · [COMPUTED] = our own numerics, internally consistent, not externally verified · [OPEN] = identified but unresolved

---

## Abstract (~200 words)
- One-sentence problem: spatial imaging of engineered/analog spacetime metrics lacks a dense, robust sensor architecture.
- One-sentence device: an array of topological SSH elements with qubit probes, read calorimetrically through the power dissipated to maintain coherence, differenced across neighbors to extract the frame-independent tidal field.
- Three headline results: (1) the placement/overlap law — sensitivity is the metric gradient integrated over the edge-state footprint, with a computed ~300x penalty for wrong-edge placement; (2) end-to-end SNR > 20 in 3 h with demonstrated hardware, all numbers cited; (3) fabrication scatter resolves into a static-calibration problem, leaving drift stability as the true spec.
- One-sentence honest scope: not a gravimeter; engineered metrics only.

## 1. Introduction & Motivation
- Analog gravity context: laboratory systems that mimic curved spacetime (cold-atom quantum field simulators, sonic horizons). Why *imaging* the metric spatially matters vs point measurements.
- The niche claim, stated honestly up front: optical clocks own absolute dilation (10⁻¹⁸); this architecture targets dense *spatial* maps of tidal structure in engineered metrics, where clocks are single exquisite points.
- Novelty statement (narrowed for prior art): the specific combination of (a) curvature-encoded CST-SSH lattice, (b) calorimetric power-draw readout, (c) differential array imaging. Each ingredient exists separately; the combination and the placement law are the contribution.

## 2. Background
### 2.1 SSH model and edge states [VALIDATED]
- Standard material: alternating hoppings, chiral symmetry, winding number, zero-energy edge modes.
### 2.2 Curved-spacetime SSH [VALIDATED — Rajbongshi & Modak, arXiv:2504.16200]
- Position-dependent hopping from the Dirac-in-curved-spacetime mapping, v(x) = 2t(x), Rindler-type metric.
- Their key results we build on: topology survives warping (BDI class preserved); edge modes become spatially asymmetric; chiral symmetry holds for arbitrary position-dependent hopping (pins zero mode).
### 2.3 Qubit decoherence probes of edge states [VALIDATED — prior art]
- Qubit-as-decoherence-probe of SSH chains (arXiv:1910.09926): decoherence rate ∝ coupling² × local DOS; ~5-decade edge-state contrast; left/right edge discrimination.
- Scanning qubit probe (arXiv:2302.13771): decoherence-rate mapping along a chain. **Cite prominently — this is the closest prior art and defines what we do NOT claim as new.**

## 3. Readout Architecture
### 3.1 Recursive Green's function engine [VALIDATED — matches direct inversion to 1e-15]
- Layer-by-layer decimation: fold semi-infinite lead into surface self-energy, O(N) vs O(N³).
- Figure: recursive vs direct LDOS agreement. (Source: ssh_gf.py run.)
### 3.2 The calorimetric observable [COMPUTED]
- Power = correction rate × energy quantum. Landauer floor at 15 mK: 23x headroom — thermodynamics is not the limit.
- Detector-limited regime: photon shot noise of the dissipation sits 10x below demonstrated bolometer NEP. Hardware improvements convert directly to sensitivity.
- Figure: energy-scale ladder (Landauer floor, kT, E_quantum, signal power, noise floors).
### 3.3 Edge-state contrast with the real Hamiltonian [COMPUTED on validated model]
- ON/OFF LDOS contrast ~1e13 using the paper's power-law hopping; robust across σ.

## 4. Sensitivity Theory: the Placement Law
### 4.1 Zero-mode product structure [VALIDATED — matches paper's Eq. 19–20 analytics]
- Zero-energy recursion telescopes: edge LDOS = product of bond ratios → log turns it into a sum → sensitivity = integrated metric tilt over the state's support.
### 4.2 The overlap/placement law [COMPUTED, paper-consistent]
- d(ln LDOS)/d(curv) = −(metric span weighted by edge-state density). Uniform shifts invisible to the protected zero mode; only gradients couple.
- **Key design rule:** probe must sit where edge-state footprint overlaps the strongest metric gradient.
- Killer figure: right-edge readout responsivity −0.001 vs left-edge +0.2 — a ~300x penalty for wrong placement, *predicted by our law and independently confirmed by the published model's asymmetry result*. (Source: honest_rerun.py, leftedge.py.)
### 4.3 Honest framing of the equivalence-principle connection
- Comoving probe (coupling co-scaled) blind to uniform redshift = freely-falling observer; externally referenced probe recovers it = Pound–Rebka. The lead is the reference frame.
- Caveat to state plainly: uniform-invisibility is a property of the chiral-protected zero mode, not of the device; finite-energy observables are scale-sensitive.

## 5. Differential Array Imaging
### 5.1 Neighbor differencing = geodesic deviation [COMPUTED]
- Each element reads local gradient; differencing adjacent elements yields the second derivative — the tidal, frame-independent part. The array is a lattice of test masses.
- Figure: reconstructed vs true tidal field. Honest note: 37% RMS error at current resolution, resolution-limited not matching-limited. (Source: imager.py.)
### 5.2 Resolution [COMPUTED]
- Pixel size = edge-state penetration length; features below the footprint attenuate (0.26 recovery at half-footprint width). Table from imager.py.
### 5.3 Noise structure — the architecture fork [OPEN, partially]
- Averaging requires independent noise; common-mode rejection requires correlated noise. Which regime holds across a shared substrate is an empirical question.
- State plainly: no rejection factor is assumed anywhere in the headline SNR (single-ended numbers only). Differential gains are conditional and listed as upside, not baseline.
### 5.4 Matching and calibration [COMPUTED]
- Fab scatter (~2%) is ~100x the neighbor tidal signal — but static. One-time flat-metric calibration map + SQUID-tunable coupler trimming. True spec: drift stability between calibrations [OPEN — quantify in future work].

## 6. Worked Example: Superconducting Implementation
- Platform justification: only ecosystem where Γ (MHz decoherence), the heatsink (dilution fridge), and the demonstrated detector (30 zW/√Hz cryogenic bolometer, Nature 2020) coexist natively.
- Cited parameter table: f = 5 GHz; couplings 10–250 MHz (arXiv:2310.12179, 2111.05561); T1 = 100 µs (range 10 µs–1 ms, arXiv:2412.19421); probe channel engineered at 1e6/s, 100x above intrinsic background (1% power contamination); T = 15 mK.
- SNR table (source: worked_example.py): δσ = 1% → 6.6 zW signal; SNR 2.2 @ 100 s; 22 @ 3 h. Detector-limited.
- Per-element readout/multiplexing question flagged [OPEN].

## 7. Validation Path
- Step 1 (cheap, room-temp): photonic waveguide SSH mock-up to confirm the placement law and edge asymmetry. Thousands of dollars, not millions.
- Step 2: cold-atom CST-SSH (the route the model's authors propose) for Hamiltonian-level physics: asymmetric edge modes, horizon slowdown.
- Step 3: superconducting prototype — small array, single bolometer, static engineered metric, measure left-vs-right edge responsivity ratio (the 300x prediction is the clean falsifiable target).

## 8. Limitations and Honest Scope
- Not a gravimeter: real-gravity tidal/gradient ratios put matching out of reach; absolute dilation belongs to optical clocks (quantitative comparison from beat.py: skin needs ~1e27 qubits to match 1e-18).
- Femtosecond framing retired: figure of merit is fractional stability and spatial resolution, not time resolution.
- Drift stability between calibrations unquantified [OPEN].
- Readout-layer physics (lead + dissipation channel) is our own numerics, not yet externally validated [COMPUTED].
- One metric family tested (power-law warping); generality of responsivity numbers unestablished.

## 9. Conclusion
- Restate the placement law as the central transferable result.
- Restate the honest niche: dense spatial tidal imaging of engineered metrics.
- The falsifiable near-term prediction: ~300x left/right responsivity asymmetry in a warped SSH chain probed by qubit decoherence.

## References (anchor set)
- Rajbongshi & Modak, arXiv:2504.16200 (CST-SSH)
- Qubit decoherence probe of SSH edges, arXiv:1910.09926
- Scanning qubit probe, arXiv:2302.13771 (prior art)
- 30 zW/√Hz bolometer: Nature 586, 47 (2020) class; 20 zW/√Hz: Comm. Phys. (2019)
- Superconducting SSH implementations: arXiv:1711.06829, 2108.01276, 2310.12179, 2111.05561, 2412.19421
- Tolman–Ehrenfest; Unruh; Landauer (standard citations to fill)

## Appendix A: Numerical methods
- Recursive GF algorithm, convergence checks, the eta-broadening floor.
## Appendix B: The clock-comparison no-go arithmetic
- Full beat.py derivation showing why absolute dilation is conceded to optical clocks.
