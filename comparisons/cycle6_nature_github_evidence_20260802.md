---
id: comparison--cycle6_nature_github_evidence_20260802
title: Cycle 6 evidence refresh — 2026-08-02
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 6 evidence refresh — 2026-08-02

## Decision-relevant evidence

- The TDDM-M0 screen is archived as a negative result. It preserved the parent response scores and speed, but did not pass the project gates: worst displacement R2 was 0.74135, the high-modal minimum score was 0.76661, independent acceleration RMS was 0.03400 (> 0.030), and independent force RMS was 0.04942 (> 0.045).
- Recent Nature evidence supports local space-time neural operators for system-level analysis and efficient multiscale computation, but this project must retain its hard EOM, direct inference, MechConv edge weights, and halo stitching. Therefore only a training/representation adaptation is admissible; no online solver or correction stage is imported.
- Recent Communications Physics evidence on physics-driven convolutional operators and current work on spectral-bias mitigation support testing a bounded multiscale representation or residual curriculum. Such a candidate must be evaluated against worst-case large-deformation and high-modal strata, not only pooled R2.
- The function-space operator-learning evidence supports discretization-aware interfaces. In this project that means preserving owned-node/owned-edge aggregation and applying the same physical scales to full-graph and halo-subgraph audits.

## Candidate constraints

Every successor must keep: the selected parent checkpoint and hard trapezoid integration contract; `TemporalParallelMatrixMechConv` matrix edge weights; replaceable constitutive plugin; two constitutive calls; `required_halo_hops=6`; direct end-to-end prediction; no post-inference solver/corrector/FFT; and the existing speed gate.

## Sources

- Fabiani et al., “Enabling local neural operators to perform equation-free system-level analysis,” Nature Machine Intelligence (2026), DOI: 10.1038/s42256-026-01265-1.
- Xiong and Zhao, “Attaining physics-driven convolutional operators by architecture design,” Communications Physics (2026), DOI: 10.1038/s42005-026-02613-8.
- Berner et al., “Principled approaches for extending neural architectures to function spaces for operator learning,” Nature Machine Intelligence (2026), DOI: 10.1038/s42256-026-01267-z.
- `neuraloperator/NNs-to-NOs`, `neuraloperator/physics_informed`, and the local SGNO/ET-PINN refresh are retained as implementation evidence only; none authorizes changing the deployed forward contract.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
