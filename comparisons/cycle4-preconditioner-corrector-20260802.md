---
id: comparison--cycle4-preconditioner-corrector-20260802
title: 'Cycle 4 evidence: preconditioners, residual correctors, and state-space operators
  — 2026-08-02'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 4 evidence: preconditioners, residual correctors, and state-space operators — 2026-08-02

## Evidence set

The auditable evidence bundle is `literature/github_20260802_cycle4/manifest_combined_20260802.json`. It records five lawful paper bundles (including the already downloaded PDFs, with page counts and SHA-256 hashes) and five GitHub snapshots. The main external anchors are [PhysicsCorrect AAAI 2026](https://doi.org/10.1609/aaai.v40i26.39360), [Neural Preconditioning Operator](https://arxiv.org/abs/2502.01337), [the state-space neural operator study](https://pubmed.ncbi.nlm.nih.gov/41447828/), [Mamba](https://github.com/state-spaces/mamba), and [neuraloperator/physics_informed](https://github.com/neuraloperator/physics_informed).

## Engineering transfer

1. PhysicsCorrect and residual-error-corrector methods support residual-driven correction, but their online linearized correction/inverse solve is incompatible with the current inference budget. Their safe transfer is offline: use residuals as a training diagnostic, teacher target, or acceptance gate, not as another deployed solve.
2. Neural preconditioning suggests learning a cheap residual-conditioned transformation. For this project, “cheap” must mean a reused tensor path or existing head; adding a second or third matrix inverse is not acceptable. The CMEJ²-M0 screen confirms this experimentally: independent acceleration/force improved only to `0.032463/0.047181`, while official90 forward total grew from `0.454877 s` to `1.024504 s`.
3. State-space and selective-memory operators are relevant to low/high-frequency history, but a new recurrent/scan branch must preserve causality, halo locality, and subgraph equivariance. A memory module that is merely accurate on the training window is not evidence of scalable structural dynamics.
4. The parent’s hard construction already protects EOM and kinematic identities. The next candidate should therefore modify the learned representation or training objective so that the existing single forward produces a velocity trajectory whose discrete derivative agrees with its constructed acceleration. Post-hoc online correction is disfavored unless it reuses an existing operation at effectively zero additional cost.

## Decision rule for the next candidate

Accept only a candidate that has a credible algebraic route to reducing both independent acceleration and force residuals, keeps the parent response contract, adds no online inverse/large edge action, and passes the local identity/shape/halo/smoke gates before one serialized remote screen. The hard remote limits remain: independent acceleration `≤0.030`, independent force `≤0.045`, official90 total forward `≤0.634345 s`, average response R² `≥0.9`, worst response R² `>0.8`, plus hard EOM, kinematics, frequency, and subgraph audits. If the design cannot meet all of these without speculative extra machinery, do not train it.

## Frozen negative branch

CMEJ²-M0 is retained as an offline diagnostic and is not the production default. Full result: `docs/plans/temporal_parallel_cmej2_m0_remote_result_20260802.md`; raw metrics: `outputs/remote_temporal_parallel_cmej2_m0_20260802b/metrics_official90_spectral.json`.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
