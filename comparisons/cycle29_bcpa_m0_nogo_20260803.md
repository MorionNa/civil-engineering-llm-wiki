---
id: comparison--cycle29_bcpa_m0_nogo_20260803
title: BCPA M0 decision record — 2026-08-03
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# BCPA M0 decision record — 2026-08-03

## Verdict

**NO-GO.** Broadband Coverage Pareto Adaptation failed the required calibration-only common-descent preflight and was stopped before formal training.

## Why this candidate was considered

The independent split exposed a distribution shift dominated by broadband content: the legacy input has roughly 4.0% spectral energy above 3 Hz and 0.032% above 6 Hz, while independent calibration/dev have roughly 39–40% and 25–26%, respectively. Sol's proposal was to adapt only the parent representation on calibration-64 while preserving the parent constitutive and temporal-pole structure.

This was deliberately a narrow candidate: no new forward operator, no extra normalization, no teacher labels, no hidden-data tuning, and no change to the constitutive-law interface.

## What was actually tested

Remote run:

`/home/senna/nonlinear-pinn-next/outputs/remote_bcpa_common_descent_m0_v6_20260803`

Local evidence:

`artifacts/bcpa_common_descent_m0_v6/remote_20260803/m0_metrics.json`

Locked inputs:

- calibration-64 only;
- parent checkpoint SHA256 `4ef1c46b5535a75b45a6cc5897bb4bde194ba6a92f015756963cd6aabca35293`;
- dataset root SHA256 `692ea2933f56e798ca01832d402b0a67e1ee55509c0de74f1f79fc0987796e6f`;
- official90 accessed: false;
- sealed access: false.

## Gate outcome

The corrected trust step lowered all four aggregate losses, but the MGDA direction was not uniformly descending for high-modal edge error:

- `rms0_fold2`: −0.01793;
- `rms0_fold3`: +0.07029;
- `rms1_fold2`: −0.00735.

The required threshold was cosine ≤ −0.05 for every objective in every strata-fold. Since this universal condition failed, the candidate was not trained.

## Interpretation

This is a genuine representation/objective conflict under the locked broadband calibration distribution, not a GPU, device-binding, or data-integrity failure. The fact that the aggregate trust step decreases all objectives is insufficient: it does not establish robust descent for every RMS stratum and fold, especially for the high-modal edge target.

The earlier v5 attempt is retained as an implementation retry record only; its trust-step sign was wrong and it is not used as scientific evidence.

## Fallback

Keep the frozen parent restricted to its legacy distribution. Retain V21 physics-first as the next fallback candidate. Do not access the sealed split or claim independent generalization for BCPA.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
