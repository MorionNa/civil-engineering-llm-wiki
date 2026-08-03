---
id: comparison--mtp-mechconv-v2-selected-nonintegrated-adapter-screen-v4-negative-20260802
title: MTP-MechConv v2 selected checkpoint non-integrated adapter screen (negative)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_evidence_scope: remote RTX4090 official90 screen
legacy_tags:
- temporal-parallel
- mechconv
- velocity-adapter
- dynamics
- negative-result
legacy_sources:
- ../../../docs/plans/temporal_parallel_selected_velocityadapter_screen_v4_20260802.md
evidence_scope: remote RTX4090 official90 screen
---

# Result

Starting from the selected temporal-parallel checkpoint and training only the zero-initialized, non-integrated causal velocity-consistency adapter preserved the pooled response but did not materially improve independent dynamics. Pooled R² was `(u,v,a,F)=(0.919822,0.959551,0.920780,0.964072)`, while independent acceleration relative RMS was `0.034001` and independent force relative RMS was `0.049416`.

The worst displacement case was `R²=0.740553`; therefore the branch did not pass the worst-case all-channel criterion. Constructed EOM and kinematic identities remained numerically closed (`5.83e-8` and `1.01e-6`), which confirms implementation integrity but not independent physical correctness.

The result supports a strict separation between constructed EOM closure and independent BDF2 acceleration/force validation. It does not authorize further adapter tuning in the current plan.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
