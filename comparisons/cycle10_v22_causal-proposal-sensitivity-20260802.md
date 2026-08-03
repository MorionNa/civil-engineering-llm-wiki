---
id: comparison--cycle10_v22_causal-proposal-sensitivity-20260802
title: Cycle 10 — V22 causal proposal sensitivity audit (2026-08-02)
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 10 — V22 causal proposal sensitivity audit (2026-08-02)

## Result

V22 is rejected before training. The narrow proposal was:

`bounded Δv` → hard trapezoid displacement → explicit replaceable edge-state
plugin → `Bᵀ f_e` node-force assembly.

This preserved the direct-inference and hard-equilibrium contract and avoided
direct learned state correction. Luna implemented the read-only preflight in
`scripts/probe_v22_causal_proposal_sensitivity_v1.py` with four focused tests.

## Reproducible evidence

- Dataset: real `input_tf` training pool, case 0; 50 DOF; 17/65/1501 steps;
  `dt=0.02`.
- Dataset SHA256:
  `285540667a7ea50ccd94747199acb2fe7e1477e497f23024797872d49d0e3a6`.
- Tests: `4 passed`.
- Causal prefix invariance: max error `0`.
- 2/4 owner-force partition summation: max error `0`.
- One-percent kill gate: triggered by DC (65-step edge-force relative RMS
  `19.9%`) and random (`12.4%`); high-frequency was `2.28%`.

The full JSON is at
`outputs/local_v22_causal_proposal_sensitivity_v1/metrics.json`.

## Meaning

The physical prefix and partition mechanisms are internally sound, but a
small bounded velocity error can create unacceptable long-horizon force error
on the same explicit constitutive path. This is sufficient to reject the
learned proposal as a training candidate. It is not evidence that the V21
physical oracle is wrong; it is evidence that the proposed learned interface
is not robust enough for the requested precision target.

The probe deliberately does not use an EOM algebraic residual as a correctness
gate and does not claim full ghost/halo equivalence, learned accuracy,
Newmark/FEM speed superiority, or multi-constitutive generalization.

## Literature and repository context

Nature evidence continues to favor architecture-embedded conservation and
local mechanics, while also documenting unresolved resolution and high-
frequency difficulties. The DYNAMI-CAL GRAPHNET article is a useful reference
for conservation-aware local message passing; the materials operator work is a
warning against treating resolution generalization as solved. The public
`neuraloperator` repository remains a reusable operator reference, but no
current repository update establishes the requested direct, hard-EOM,
cross-constitutive, 50DOF speed-and-accuracy contract.

## Degraded recommendation

1. Retain the validated 5DOF TemporalParallelMatrixMechConv parent for direct
   inference.
2. Retain V21 as an explicit causal physical oracle and scalability reference.
3. For larger systems, use vectorized RK4/Newmark/FEM until a new proposal
   includes coarse/global communication and independently passes the same
   sensitivity, physics, halo, and speed gates.

No remote GPU run is justified by this cycle's evidence.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
