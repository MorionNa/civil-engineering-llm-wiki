---
id: comparison--cycle26_eces_p_evidence_nogo_20260803
title: 'Cycle 26 ECES-P audit: rejected for insufficient evidence'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 26 ECES-P audit: rejected for insufficient evidence

## Intended contribution

ECES-P tried to make the edge-level nonlinear strain map explicit before node aggregation, motivated
by edge-local physical interaction and convex-potential structure. The proposed invariants are
plausible, but they were never executed against the current graph, constitutive, and halo APIs.

## Why the branch is closed

The implementation worker stopped before creating or running the mandatory tests. Therefore there
is no evidence for exact parent parity, nonzero activity, cross-law gradients, PSD/nullspace,
partition work, active halo equivalence, speed, or the locked non-circular accuracy gate. Formula-
level plausibility cannot substitute for those checks.

## Reusable lesson

After several architecture branches failed their real tail-response gates, local implementation
must be time-boxed around an executable M0. If the M0 cannot be completed, the candidate is rejected
without remote training rather than kept alive as an untested promise.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
