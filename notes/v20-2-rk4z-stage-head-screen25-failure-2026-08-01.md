---
id: notes--v20-2-rk4z-stage-head-screen25-failure-2026-08-01
title: 'V20.2 RK4Z stage-head screen25: failure evidence'
type: decision
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# V20.2 RK4Z stage-head screen25: failure evidence

The one-carrier RK4Z algebra, exact RK4 oracle ceiling, causality, matrix-edge block-chain assembly, constitutive plugin protocol, and strict final equilibrium had already passed their corresponding M0 gates. V20.2 then tested whether a 25,192-parameter causal temporal head could infer all four RK4 stage edge residuals and internal states directly from ground excitation and static edge features.

On eight untouched development cases, the formal 25-epoch screen achieved R2 values of 0.5925/0.4646/0.3949 for displacement/velocity/acceleration, a mean of 0.4840, stage-residual R2 of 0.0930, and exact force-balance R2 of 1.0. High-frequency displacement and velocity R2 were negative. The run therefore failed its preregistered mean-response and stage-residual gates.

The failure is structurally informative. Residual R2 was approximately 0.093 for every RK4 stage, and the predicted residual magnitude was only about 31% of truth. The screen excluded the carrier from training and optimized only direct normalized labels plus temporal differences. Consequently, it did not impose the preregistered soft constitutive consistency relation on carrier-reconstructed stage states. Exact final equilibrium alone does not make the learned stage forcing accurate or spectrally stable.

The next preferred experiment, if authorized, is V20.3: differentiate through the single RK4Z carrier and jointly optimize stage supervision, plugin consistency, response accuracy, and frozen spectral bands. A two-carrier predictor-corrector is the principal speed-degraded fallback; bounded correction iterations are the end-to-end-degraded fallback. No longer V20.2 training is authorized by this failed screen.

Primary local evidence: `outputs/remote_rk4z_stage_head_v20_2_screen25_v1_20260801ai` and `docs/plans/rk4z_stage_head_v20_2_screen25_fail_2026-08-01.md`.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[notes/index]]
- [[index]]
