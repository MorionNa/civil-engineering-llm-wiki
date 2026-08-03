---
id: comparison--cycle9_causal_consistency_physics_operator_refresh_20260802
title: 'Cycle 9 evidence refresh: causal path consistency and physics-constrained
  operators (2026-08-02)'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 9 evidence refresh: causal path consistency and physics-constrained operators (2026-08-02)

## Retrieval and verification

The Nature retrieval workflow selected two recent, directly relevant records. Both published OA PDFs were downloaded and verified; SI was requested by default but could not be fetched because the local CDP proxy at `127.0.0.1:3456` was unavailable.

| Paper | Venue | DOI | Status | SHA256 |
|---|---|---|---|---|
| Self-consistent recurrent neural network for path dependent deformation | Scientific Reports (2026) | `10.1038/s41598-026-49661-2` | `open_access_downloaded` | `07668286a009d95c57105194eeadd20bde6c5d30df184f5b55841ce0d88c47b8` |
| A robust physics-constrained neural operator framework for efficient geothermal resource development | Nature Communications (2026) | `10.1038/s41467-026-73183-0` | `open_access_downloaded` | `4f9fb7e208198109802fd68c5da496724b217e300cca4fd00c9d84fcbd11a384` |

Manifest: `papers/literature_20260802_cycle9/manifest.json`.

## Transferable evidence

1. The path-dependent deformation paper makes two requirements explicit: truncation (future inputs cannot change past outputs) and approximate consistency under different time discretizations. Its customized transition uses a bounded local update multiplied by a learned step-count surrogate. This is evidence for an offline causal-prefix/semigroup audit, not a license to add a recurrent deployment branch to the current temporal-parallel model.
2. The physics-constrained operator paper couples scalar and field inputs, governing-equation constraints, and large-domain operator inference. Its transferable lesson is to keep physical constraints tied to the actual field/operator interface and to measure scale/generalization separately; its U-FNO and geothermal-specific coupling are not drop-in replacements for matrix-edge MechConv.
3. Existing DYNAMI-CAL/NOEM/local-operator evidence remains consistent with the same boundary: antisymmetric force assembly, reusable local operators, and discretization-aware interfaces should be audited around the existing MechConv force path rather than inserted as online solvers or post-inference correctors.

## GitHub refresh

The existing local snapshots under `literature/github_20260802_next/repos` were checked. `Laplace-Neural-Operator` remained at `78c64ef7edc47f343352251d15f7d1341e6732ba`; live fetches for `Learning_Vibrating_Plates`, `pino-closure-models`, and `SCALE-PINN` timed out against `github.com:443`. No unverified or newly fetched commit is treated as implementation authority.

## Candidate boundary for Sol review

The next candidate must be training-only or a zero-forward-change interface audit. It may use causal prefix and time-grid consistency, or a nonlinear constitutive tangent teacher, but it must preserve the parent checkpoint, hard trapezoid kinematics, matrix-edge MechConv, replaceable plugin contract, exactly two constitutive calls, halo=6, direct inference, and the current speed cap. A candidate that only reweights samples, adds memory, adds a pointwise feature adapter, or introduces an online inverse/corrector is already covered by a frozen failure family.

Sources: [path-dependent deformation RNN](https://www.nature.com/articles/s41598-026-49661-2), [physics-constrained neural operator](https://www.nature.com/articles/s41467-026-73183-0).

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
