---
id: comparison--temporal-parallel-dstr-cvar-negative-20260802
title: DSTR-CVaR local screen result — 2026-08-02
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# DSTR-CVaR local screen result — 2026-08-02

## Status

Rejected and frozen. No remote GPU screen was authorized. The production parent remains `outputs/remote_temporal_parallel_dynamicprojection75_selected_full_v2_20260731cm/selected_model.pt` with SHA-256 `4ef1c46b5535a75b45a6cc5897bb4bde194ba6a92f015756963cd6aabca35293`.

## Candidate

DSTR-CVaR added an opt-in truth-only deformation/frequency case weighting and weighted CVaR response risk. Forward model kwargs, hard trapezoid kinematics, matrix edge MechConv, replaceable constitutive plugin, two constitutive calls, and `required_halo_hops=6` were unchanged. Only `node_head.*`, `edge_head.*`, `node_high_frequency_head.*`, and `edge_high_frequency_head.*` were trainable in the screen configuration.

## Local evidence

Three CPU epochs were run from the locked parent checkpoint on the training pool only, followed by a read-only official90 evaluation to detect regression. Parent → candidate:

- pooled R2 u/v/a/edge: `(0.9198513, 0.9595504, 0.9207796, 0.9640716)` → `(0.9196519, 0.9594972, 0.9207798, 0.9640645)`;
- worst displacement R2: `0.7413499` → `0.7474676`;
- high-modal minimum remained about `0.76661`;
- independent acceleration RMS: `0.0340008` → `0.0340548`;
- independent force RMS: `0.0494158` → `0.0494941`.

The implementation gates passed: 31 targeted regressions, compileall, truth-only strata metadata, finite gradients, parent kwargs equality, halo=6, and constitutive paths. These are implementation gates only, not evidence of acceptance.

## Decision

Sol denied the single remote screen. The candidate shows a small worst-u improvement but fails the preregistered local requirement for substantive high-frequency improvement and non-degradation of independent physics. Do not revive this exact loss/strata/head-only combination by merely extending epochs, changing weights, or widening the same screen. Parent remains the reference for the next design cycle.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
