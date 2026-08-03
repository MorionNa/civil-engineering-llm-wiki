---
id: comparison--temporal-parallel-ppec-m0-negative-20260802
title: Temporal-parallel PPEC-M0 negative result (2026-08-02)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Temporal-parallel PPEC-M0 negative result (2026-08-02)

PPEC-M0 was the single candidate selected by the Sol design/grill review after the prior TDDM-M0, DSTR-CVaR, and BEMCI-M0 freezes. It adds a zero-initialized pointwise power-flow/phase feature carrier before the existing constitutive-state bound. The carrier uses explicit element endpoint matrix rows, relative kinematics, and an optional damping-availability channel; it does not generate force, change the residual, add graph hops, or add constitutive calls.

The implementation passed 15 focused/regression tests and compile checks. A 3-epoch CPU smoke from the immutable parent trained only 57 carrier parameters and retained exactly two constitutive calls and halo=6. Official90 pooled R2 remained parent-like (`u=.9196397`, `v=.9595507`, `a=.9207796`, edge force `.9640716`); independent acceleration/force errors remained `.034002684/.049418453`. Worst displacement R2 improved only from `.7385343` to `.7385517`, and the high-modal edge-force score improved only from `.766607536` to `.766607543`—far below the required `+.010` improvement in either measure.

Status: **rejected/frozen**. No remote GPU run occurred. Preserve the implementation and test/config artifacts for reproducibility, but do not revive this exact no-memory pre-constitutive power/phase carrier by widening, shift tuning, backbone unfreezing, loss changes, or force correction. The production parent remains the reference.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
