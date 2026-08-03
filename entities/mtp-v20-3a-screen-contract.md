---
id: entity--mtp-v20-3a-screen-contract
title: MTP-MechConv V20.3a screen contract
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- structural-dynamics
- physics-informed
- mechconv
- rk4
- constitutive-history
- fixed-point
- screen-contract
legacy_sources:
- docs/plans/coupled_rk4z_mechconv_v20_3_preregister_2026-08-01.md
- docs/plans/rk4z_stage_head_v20_2_screen25_fail_2026-08-01.md
- docs/plans/tridiagonal_zcq_mechconv_v19_m0b_veto_2026-08-01.md
- knowledge/civil-engineering-llm-wiki/comparisons/fbpinn-xpinn-structgraph-pignn-transfer-boundaries.md
- literature/github/StructGraph-Dyna/README.md
- literature/github/soft-tissue-pignn/README.md
---

# V20.3a screen contract

V20.3a is a falsifiable five-DOF screen, not evidence of arbitrary-scale or
cross-constitutive success. Its single-carrier result is explicitly a
proposal-driven learned fixed-point surrogate. The plugin branch audits the
proposal; it does not silently correct the final state.

## Required history semantics

The replaceable constitutive slot is a discrete-history protocol with
initialization, stage evolution, force, commit, admissibility, and defects.
Default Bouc--Wen requires z1 = zn, RK4 stage recursion, and a grid commit
defect. A free latent state or a stage-q versus stage-z loss is invalid because
z is internal state, not displacement.

## Causality and metrics

Stage 1 and 2 must be invariant under suffix perturbation containing F(n+1).
Proposal and plugin residual and acceleration branches require separate
frozen-scale NRMSE and per-channel/per-stage R2. High-frequency response is a
hard gate. One previously unseen internal set is evaluated once after the
model, normalization, checkpoint rule, and code hash are frozen, then retired.

## Route distinction

A genuinely plugin-driven final response requires two carriers: proposal C1,
legal history replay, plugin residual, corrected carrier C2, followed by a
second replay and fixed-point defect audit. A bounded two/three-iteration
variant must predeclare cost. Matrix edges, MechConv assembly,
owner/separator/Schur interfaces, and scale qualification remain post-screen
gates.

## Related evidence

- [[mtp-v20-v19-negative-knowledge-architecture]]
- [[fbpinn-xpinn-structgraph-pignn-transfer-boundaries]]
- [[fbpinn]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
