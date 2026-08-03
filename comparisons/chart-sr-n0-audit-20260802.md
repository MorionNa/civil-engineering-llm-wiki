---
id: comparison--chart-sr-n0-audit-20260802
title: CHaRT-SR-N0 stateful replay audit
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CHaRT-SR-N0 stateful replay audit

## Bottom line

The stateful causal oracle is implemented and locally verified, but it is not a deployable candidate and did not authorize training. It replays the physical Bouc–Wen step law with causal edge-state carry and can run a local current-step Newton diagnostic. The locked parent uses a learned CM constitutive correction, so direct physical-law replay is a compatibility diagnostic rather than a parent-quality score.

## Evidence

The audit was read-only over one locked `input_tf/train_pool` record. It verified the parent checkpoint SHA256, used strict teacher-valid times starting at `t=2`, and did not access official90 or pred15. Parent residual RMS was `0.1483790576`; the independent physical Bouc–Wen replay residual RMS was `0.8984621854`. The audited parent maximum displacement magnitude was `1.7109429836`, but no pre-registered small/large deformation thresholds existed, so no deformation-regime pass is claimed.

## Reusable rule

For nonlinear hysteresis, a fixed parent edge state is not a full constitutive tangent. A causal stateful replay is the minimum honest diagnostic, but it still cannot become a student target until the state law, learned correction, initial state, and deformation strata are explicitly compatible. CHaRT-SR-N0 is therefore frozen; the temporal-parallel matrix parent remains the default.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
