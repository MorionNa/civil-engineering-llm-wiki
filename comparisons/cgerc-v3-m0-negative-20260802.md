---
id: comparison--cgerc-v3-m0-negative-20260802
title: CGERC-v3 M0 negative result（2026-08-02）
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CGERC-v3 M0 negative result（2026-08-02）

## Entity

`CGERC-v3`: causal graph equation-recast residual corrector for temporal-parallel MatrixMechConv.

## Evidence

The candidate used an explicit `p1 = p0 - A0^-1 DeltaA p0` matrix-edge action, twenty causal scalar lift channels, two temporal MatrixMechConv blocks, a bounded correction, exactly two constitutive calls, and a supervised correction loss on ten labeled trajectories. Local shape/causality/gradient/call-count/20-step target gates passed.

The completed CUDA screen at `outputs/remote_cgerc_v3_m0_20260802c` failed the response and independent-physics gates: `R2_u=0.833851`, independent acceleration RMS `0.394709`, independent force RMS `0.573658`, while the selected parent was approximately `0.919638`, `0.034003`, and `0.049418`. Median forward time improved to `0.3178 s/90`, but training loss increased from `7.1102` to `11.9246`.

## Decision

Negative branch. Do not merge or select CGERC-v3 M0. Keep the selected temporal-parallel parent checkpoint unchanged. The result supports a failure mode in which a high-capacity correction head trained from too few labeled trajectories overwhelms a parent whose projection already satisfies the response contract.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
