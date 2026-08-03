---
id: comparison--chart-fold-m0-hold-20260802
title: 'CHaRT-Fold-M0: design hold, not a training result — 2026-08-02'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CHaRT-Fold-M0: design hold, not a training result — 2026-08-02

CHaRT-Fold-M0 was proposed after CMEJ²-M0 failed the speed and absolute residual gates. Its intended deployment is unchanged from the parent: the training-only causal halo tangent teacher is distilled into existing velocity-head weights and folded away. Therefore it has a plausible zero-online-cost story, unlike CMEJ².

The proposal is not yet evidence-backed. A full tangent can be locally useful but fail after nonlinear Bouc–Wen recomputation; an offline teacher can also leak future information or require graph context unavailable under halo=6. The existing hidden features may not identify the sample-dependent correction. These risks are decisive because the remaining parent defects are small in relative terms but hard in absolute terms: the parent is at independent acceleration `0.034003` and force `0.049418`, while the acceptance limits are `0.030` and `0.045`.

The correct next action is an oracle-only gate, not GPU training. Require nonlinear recomputation, ≥20% improvement in both residuals, ≥10% low/high-frequency improvement, causal prefix and halo stitching, bounded displacement drift, and a frozen-head expressivity probe. Only after those pass may a single serialized remote screen be considered. Full decision record: `docs/plans/chart-fold-m0-hold-20260802.md`.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
