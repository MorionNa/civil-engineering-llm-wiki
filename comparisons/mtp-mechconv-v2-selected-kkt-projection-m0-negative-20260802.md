---
id: comparison--mtp-mechconv-v2-selected-kkt-projection-m0-negative-20260802
title: Selected MechConv output KKT projection M0 — negative result
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_date: 2026-08-02
---

# Selected MechConv output KKT projection M0 — negative result

## Question

Can a frozen selected temporal-parallel MechConv prediction be minimally
corrected by a one-shot linear KKT projection so that independent acceleration
and force residuals close without damaging response quality or speed?

## Evidence

The remote RTX 4090 screen achieved pooled R² of
`0.92015/0.96002/0.92116/0.96418` for `u/v/a/edge`, with worst-case values
`0.74228/0.92804/0.87655/0.92573`. Constructed and independent force-balance
R² were `1.0`, normalized EOM residual was `1.15e-7`, independent acceleration
relative RMS was `1.34e-6`, and independent force relative RMS was `1.94e-6`.

Thus the linear projection solved the algebraic and discrete kinematic defect
that the small velocity adapter could not solve. Corrections stayed within
the pre-registered pooled/P95/max limits.

The decisive failure was runtime: full official90 projection timing was
`33.0155 s` median and `33.0746 s` P95, versus the allowed `0.634345 s`.
The implementation performs many small direct block solves from Python and
does not exploit a sufficiently batched GPU factorization.

## Transferable lesson

Exact linear closure is not enough for the end-to-end target. A future solver
would need a genuinely batched block-banded or cyclic-reduction implementation
with a measured speed proof before another GPU screen is authorized. Do not
hide this cost behind a post-processing layer or call it faster than Newmark.

## Sources and artifacts

- Plan and gate record: `docs/plans/selected_kkt_projection_m0_result_20260802.md`
- Metrics: `outputs/remote_selected_kkt_projection_m0_20260802/metrics_m0.json`
- Projected predictions: `outputs/remote_selected_kkt_projection_m0_20260802/predictions_projected.pt`
- Literature context: `knowledge/civil-engineering-llm-wiki/comparisons/structure-preserving-candidates-20260802.md`

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
