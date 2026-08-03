---
id: comparison--cycle28_independent_parent_baseline_nogo_20260803
title: Cycle 28 — independent parent baseline NO-GO
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 28 — independent parent baseline NO-GO

The new independent truth split invalidated the assumption that the frozen parent generalizes beyond the repeatedly inspected `official90` development distribution.

| split | pooled R² (u, v, a, edge) | worst u/v/a/edge | independent force R² | independent acceleration RMS |
|---|---|---|---:|---:|
| calibration | -0.218/-0.758/-0.284/0.238 | -28.894/-10.273/-5.351/-0.956 | -7.595 | 2.349 |
| dev | -0.195/-0.154/-0.009/0.358 | -13.080/-3.515/-4.324/-0.935 | -6.529 | 2.224 |

The approximately unit constructed force-balance R² is not evidence of correct prediction: it comes from the model's construction `reference + equilibrium_force_residual`. The independent force-balance and acceleration audits are the relevant physics checks and fail. High-modal edge-force spectral error is about `0.993` on both splits.

Decision: stop this candidate cycle. Keep the frozen parent only as a legacy-distribution fallback; do not claim the full objective and do not start a new architecture/training run until a calibration/dev-only design review identifies a falsifiable conditioning or distribution-coverage change.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
