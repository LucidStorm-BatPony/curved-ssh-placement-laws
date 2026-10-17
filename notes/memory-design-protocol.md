> **Working note, not for citation.** Operating spec for a companion memory-mode thread; untested, see "Required tests not yet run".

# Memory Design Protocol — SSH Doublet Register
### One-page operating specification for the cryogenic memory mode of the imager hardware
**Companion to:** imager-susy-bridge.md (the dictionary and constraint algebra) and imager-derivations.md §6 (the derived scalings). Self-contained for use by Lucid, Cam, or any AI session.

---

## The knobs and what they do

| Knob | Symbol | Chiral-safe? | Function |
|---|---|---|---|
| Dimerization ratio | r = t1/t2 | YES | Barrier height. Sets doublet splitting dE ∝ exp(−N/ξ), ξ from ln(t2/t1). Storage wants r deep (small dE); writing wants r near 1 (large dE). |
| Warping | σ | YES | Barrier trim / mode shaping. Squeezes splitting further (≈4.5× by σ=1 in tests); makes the two logical states spatially asymmetric — note readout implications. |
| Chain length | N | YES (fabrication-time) | Exponential protection knob. Longer chain = smaller splitting = longer coherent hold, at the cost of slower naive writes. |
| Staggered tilt (Rice–Mele) | Δ | NO — deliberately chiral-breaking | The write field. Biases one sublattice/edge over the other; sweeping +Δ→−Δ through zero transfers the bit. Applied ONLY during writes. |

## The one inviolable rule
**No static A–A or B–B terms, ever.** No sublattice-asymmetric on-site potentials at rest, no next-nearest-neighbor hopping. Verified consequence: hopping-only disorder leaves the doublet center at zero to machine precision; equal-strength on-site disorder unpins it by ~10¹⁴×. Chiral symmetry is the entire protection budget. The write tilt Δ breaks it on purpose, transiently, and must return to zero.

## The derived scalings (do not trust the old script comment)
- Hold time (coherent): t_hold ≈ ℏ/dE. Grows exponentially with N.
- Hold time (practical): capped by T₁ ≈ 100 µs class — photon loss deletes the excitation regardless of splitting. **This is a latch, not an archive.**
- Naive write time: Landau–Zener through the Δ=0 crossing whose gap IS dE ⇒ T_write ∝ 1/dE² ∝ t_hold². The comment in ssh_memory_unified.py claiming "write slows only linearly-ish" is WRONG.

## The two-phase write protocol (resolves the write/retention conflict)
1. **Store:** r deep, σ as trimmed, Δ = 0. Barrier high, splitting tiny, bit parked in one edge mode.
2. **Open:** ramp r → near 1 (chiral-safe). Crossing gap becomes large. Protection intentionally softened; bit is briefly vulnerable — keep this window short.
3. **Write:** sweep Δ through zero fast (large gap permits fast adiabatic passage). Bit transfers edges.
4. **Close:** Δ → 0 first, then r → deep. Barrier restored, bit parked.
Rationale: write through an open door, store behind a thick wall. Same trick as flux-qubit gating, which remains the identified hardware foothold.

## Required tests not yet run
1. **Hold test:** after a write, ramp Δ→0, evolve at fixed r, confirm the bit persists for t ≪ ℏ/dE and Rabi-oscillates away at t ≈ ℏ/dE. Five lines added to ssh_memory_unified.py; demonstrates the retention law Part 2 only infers.
2. **Two-phase write demo:** full store→open→write→close cycle in one simulation; verify fidelity vs the naive slow sweep and quantify the vulnerability window in step 2.
3. **Asymmetric-doublet readout check:** with σ>0 the two logical states are not mirror images; verify both states read out with acceptable margin.

## Integration with the imager (the co-location claim)
Role: **on-chip frame buffer** — latch a curvature map between sense epochs to enable temporal differencing without data leaving the fridge. Not persistent storage; classical memory upstairs remains the archive.
Constraint discovered in review: memory writes dissipate far above the zeptowatt sensing scale. **Thermal partitioning + duty cycling are mandatory** — sense quietly, then write; never both on one thermal island. Design this in from the start.
