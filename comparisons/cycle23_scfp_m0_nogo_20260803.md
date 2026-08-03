---
id: comparison--cycle23_scfp_m0_nogo_20260803
title: 'Cycle 23 SCFP M0 audit: rejected'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 23 SCFP M0 audit: rejected

## Why it failed

SCFP was intended to add one shared causal matrix-flux patch before the first parent block. The
local audit showed that nonzero gains did not change displacement output under the tested parent
configuration, and the Bouc–Wen path produced an exactly zero gain gradient. This is stronger than
an accuracy miss: the proposed path is not demonstrated to be active or learnable across the
replaceable constitutive interface.

## Evidence boundary

Five structural tests passed, but two mandatory tests failed. The real parent/ground-truth
common-descent test was not completed. Therefore no claim is made about worst displacement,
acceleration, high-modal edge force, speed, or halo stitching.

## Current fallback

Keep the frozen parent as the deployable candidate and V21 as the physics-first fallback. Preserve
SCFP only as a negative audit branch; do not spend remote GPU time on it without a new design and a
new authorization decision.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
