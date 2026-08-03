---
id: notes--cycle41-hn-cs-lbpc-nogo-m1-2026-08-04
title: 'Cycle 41 HN-CS-LBPC: normalized Bouc-Wen equivalence failed M1'
type: decision
status: draft
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- method/evaluation
- decision/implementation
sources: []
created: '2026-08-04'
updated: '2026-08-04'
confidence: low
---

# Cycle 41 HN-CS-LBPC: normalized Bouc-Wen equivalence failed M1

Cycle 41 repaired the inactive-hysteresis scale found in [[notes/cycle40-cs-lbpc-nogo-hysteresis-2026-08-04]] by introducing a selection-only transition deformation `q_y=0.004442514552136224`. The normalized Bouc--Wen state `r=z/q_y` avoided direct state clipping, but exact equivalence to the physical parameterization required `beta=gamma=0.5/q_y^3=5,702,738.102198042`.

The formal M1 audit used four complete excitation histories with exactly 1,500 host intervals, refined to 12,000 internal steps, on the 500DOF structure. It compared normalized and physical implementations step by step before any nonlinear accuracy, speed, or learning experiment. Validation excitation generation remained locked.

The local material checks passed: finite-difference tangent errors were below `5.54e-9` across three orders of `q_y`; reversal and time-step convergence passed; `max |r|=0.9994887847`; and no clipping occurred. The complete rollout nevertheless failed its frozen equivalence thresholds. Velocity, physical state and tangent reached relative differences of `1.27e-8`, `1.83e-8` and `1.23e-8` against `1e-8` limits. The relative accepted-residual difference was `54.87` against `1e-5`; residuals were individually near zero, so this ratio is numerically ill-conditioned, but it was frozen before the run and cannot be replaced after inspection. The other three threshold exceedances independently preserve the NO-GO.

Cycle 41 therefore stopped before H1/H2, before validation generation, and before training. The reusable negative lesson is that a mathematically exact state normalization can still create a fragile numerical equivalence contract when it maps a small transition deformation into extremely large physical rate parameters. A successor should prefer a constitutive law with a closed-form, well-conditioned state update and algorithmic tangent, such as rate-independent bilinear kinematic hardening with exact return mapping.

Primary local evidence: `docs/plans/cycle41_hn_cs_lbpc_nogo_m1_20260804.md` and `outputs/remote_cycle41_m1_selection4_500dof_20260804a`.

## Verification Needed

This page records locally reproducible experiment evidence rather than an external publication. Re-run the frozen M1 script and inspect the artifact hashes before promotion from draft.

## Related Pages

- [[notes/cycle40-cs-lbpc-nogo-hysteresis-2026-08-04]]
- [[notes/cycle39-canonical-admissibility-refrozen-2026-08-03]]
- [[comparisons/structure-preserving-candidates-20260802]]
- [[notes/index]]
