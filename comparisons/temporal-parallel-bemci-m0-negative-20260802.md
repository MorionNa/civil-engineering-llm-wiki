---
id: comparison--temporal-parallel-bemci-m0-negative-20260802
title: Temporal-parallel BEMCI-M0 negative result (2026-08-02)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Temporal-parallel BEMCI-M0 negative result (2026-08-02)

BEMCI-M0 was the only candidate authorized by the Sol design review after the DSTR-CVaR and TDDM-M0 freezes. It adds four fixed-decay causal edge-memory filters before the existing constitutive state bound, with a zero-initialized bounded projection. The replaceable constitutive plugin remains the sole force generator and signed edge-to-node scatterer.

The implementation passed focused interface tests and compileall, and a 3-epoch CPU smoke from the immutable parent completed with `required_halo_hops=6`, exactly the adapter trainable, and no loss changes. Official90 pooled R2 values remained essentially at the parent (`u=.9196411`, `v=.9595504`, `a=.9207791`, edge force `.9640711`), while independent acceleration/force errors remained `.0340026/.0494184`. Worst displacement R2 was `.73858` and the high-modal minimum was `.76661`, both below the local authorization gates.

Status: **rejected/frozen**. No remote GPU run occurred. Keep the module and configuration only for reproducibility; do not revive this exact combination with more epochs, wider unfreezing, decay tuning, or another BEMCI sweep. The production parent remains the reference.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
