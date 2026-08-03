---
id: comparison--cycle23_literature_evidence_20260803
title: 'Cycle 23 evidence note: shared local physical representations'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 23 evidence note: shared local physical representations

## What transfers

- Edge-local, node-swap antisymmetric features are a credible way to preserve interaction direction
  without injecting a separate edge-head correction.
- Physics-constrained graph latent states can improve long-horizon representation, but their results
  are not a substitute for the current hard-EOM and replaceable-constitutive contract.

## What does not transfer automatically

- Conservation or port-Hamiltonian structure does not prove the strict worst-case accuracy target.
- Locality claims do not prove active halo equivalence under nonzero candidate parameters.
- A generic latent state does not prove speed advantage over Newton/Newmark on large deformation.

## Audit rule for the next candidate

The candidate must create one shared pre-constitutive state from which both node and edge features are
derived. Its gate must use fixed parent-generated targets or held-out real labels, never a teacher
with manually activated weights of the same candidate. Orientation, degree, finite-gradient,
constitutive-call count, zero-init parity, and active-halo tests are mandatory.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
