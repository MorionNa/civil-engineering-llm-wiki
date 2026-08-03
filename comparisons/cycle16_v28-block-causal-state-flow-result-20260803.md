---
id: comparison--cycle16_v28-block-causal-state-flow-result-20260803
title: Cycle 16 — V28 Block-Causal State-Flow result (2026-08-03)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 16 — V28 Block-Causal State-Flow result (2026-08-03)

## Evidence record

V28 tested a deployment-oriented causal state-flow: edge-local constitutive
state, nodal force assembly, hard mass-normalized EOM, and fixed symplectic
Euler time stepping. The local linear and Bouc–Wen shape/finite-value tests
passed. The hard-EOM and kinematic residuals were below `1e-12`.

The design is nevertheless rejected for formal training. It lacks actual
halo/subgraph inference, and explicit integration is unstable on a high-
frequency SDOF probe (`k=100000`, `dt=0.01`, 200 steps, `max|u|≈1.94e179`).
Consequently it cannot meet the combined requirements of scalable local
deployment and robust high-frequency convergence. No remote training was run.

## Relation to prior evidence

This result is consistent with the prior GraphCausal/GRU screen: causal
sequencing alone is not evidence of accuracy. It also confirms the V21 oracle's
trade-off: exact physical recurrence can be accurate, but it must be evaluated
as a solver-like sequential path and cannot be advertised as faster than
Newmark/FEM without a matched benchmark.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
