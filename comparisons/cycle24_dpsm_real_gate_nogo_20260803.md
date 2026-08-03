---
id: comparison--cycle24_dpsm_real_gate_nogo_20260803
title: 'Cycle 24 DPSM audit: rejected'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 24 DPSM audit: rejected

## Mechanism tested

DPSM inserted a stable causal port state inside each existing matrix MechConv spatial message:
the matrix edge flux was filtered by a vectorized exponential state, and a bounded transient
term was scattered back to the shared node hidden state. This was a distinct pre-constitutive
representation candidate rather than a force correction or edge-head shortcut.

## Why it failed

Although the implementation had a genuine calibration common-descent direction, the independent
held-out worst-displacement gain was only `8.96e-5`, while the required gain was `3e-3`. The result
shows that the new edge memory is either redundant with the parent causal poles or unable to move
the displacement tail without sacrificing the other targets. A successful local gradient is not
enough evidence for a new architecture.

## Reusable lesson

In-block physical memory can be structurally valid, causal, and cross-law differentiable while
still failing the tail-response target. Future candidates must demonstrate a substantial held-out
worst-u gain before any remote screen; speed, halo, and formal cross-law experiments cannot rescue
this failed accuracy gate.

## Fallback

Keep the frozen parent and V21 physics-first fallback. Preserve DPSM only for audit and do not
reopen it without a genuinely new mechanism and a new Sol authorization.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
