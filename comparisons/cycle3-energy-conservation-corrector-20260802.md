---
id: comparison--cycle3-energy-conservation-corrector-20260802
title: 'Cycle 3 evidence note: energy consistency, exact invariants, and residual
  correctors'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 3 evidence note: energy consistency, exact invariants, and residual correctors

Date: 2026-08-02
Scope: structural-dynamics MechConv / temporal-parallel PINN candidate selection

## Evidence package

The cycle-3 retrieval package is archived at:

`literature/github_20260802_cycle3/manifest_combined_20260802.json`

Full-text records downloaded through lawful open-access or publisher routes:

1. Tanaka et al., *Energy-consistent Neural Operators for Hamiltonian and Dissipative Partial Differential Equations*, AISTATS 2025 / PMLR 258. The paper constructs an energy-based neural-operator penalty using a functional derivative and combines it with data loss.
2. *Exactly conservative physics-informed neural networks and deep operator networks for dynamical systems*, Neural Networks 181 (2025), DOI `10.1016/j.neunet.2024.106826`. The method projects predictions onto an invariant manifold so conservation is imposed as a hard constraint.
3. *Residual-Based Error Corrector Operator to Enhance Accuracy and Reliability of Neural Operator Surrogates of Nonlinear Variational Boundary-Value Problems*, CMAME 419 (2024), DOI `10.1016/j.cma.2023.116595`. The correction is derived from a residual-dependent linear variational problem rather than an unconstrained high-capacity output head.

GitHub refreshes were also archived for Laplace Neural Operator, SCALE-PINN, Learning Vibrating Plates, and PINO closure models. Their pinned commits were unchanged from the previous cycle.

## Transferable lessons

### Energy and dissipation are diagnostics, not a substitute for EOM audit

Energy-consistent neural operators motivate tracking stored-energy drift, dissipated work, and passivity. For the present structural model these are useful additional diagnostics and regularizers, but they cannot replace the independent BDF2 acceleration and force residuals. The selected parent already satisfies constructed force balance by construction while retaining nonzero independent residuals; a constructed energy law could exhibit the same failure mode.

### Hard invariants must commute with the model's discrete operators

The exactly conservative PINN/DeepONet work supports an in-forward projection viewpoint. The local KKT experiment showed that a mathematically exact projection can be too expensive when implemented as a global solve. The practical implication is to prefer fixed, local, sparse operator actions whose discrete ordering is explicit and auditable. Any projection candidate must be checked against the same BDF2/trapezoidal operators used by the independent audit.

### Residual correctors need a protected base model

The residual-corrector paper supports mapping a physical residual to a bounded correction. It does not justify adding a free correction head to a small labeled set. In this project, the CGERC-v3 and TR-PCGrad branches both demonstrate that loss improvement or guard improvement can coexist with worse official independent physics. Future correctors therefore need parent identity at zero correction, a low-dimensional bounded correction space, a parent-proximity term, and fail-closed official gates.

## Decision for the current screen

These findings support testing CMEJ²-M0 as a fixed sparse matrix-edge residual-correction operator inside the existing projection slot. CMEJ² uses no new high-capacity response head and no global solve. It is still only a candidate: the formal decision remains determined by local identity/oracle/causality gates and the serialized remote official90 screen.

## Negative transfer warnings

- Do not claim energy consistency from force-balance residuals alone.
- Do not use official90 data for correction-gain selection.
- Do not promote a candidate based only on training or guard loss.
- Do not claim constitutive replaceability until linear, bilinear, and CM-Bouc-Wen plugins pass the same two-call and physics gates.
- Do not claim arbitrary graph scaling until full/halo/subgraph stitching and unseen larger graphs are measured.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
