---
id: comparison--cycle36_pdps_mco_literature_20260803
title: 'Cycle 36: PDPS-MCO literature and GitHub evidence'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_manifest: literature/cycle36_pdps_mco_20260803/manifest_cycle36_pdps_mco_20260803.json
legacy_evidence_scope: Five-paper shortlist, lawful OA/preprint retrieval, PDF text
  verification, and read-only GitHub HEAD checks; no training.
legacy_tags:
- pdps-mco
- viscoelasticity
- rom
- gnn
- pignn
- prnn
- structural-dynamics
evidence_scope: Five-paper shortlist, lawful OA/preprint retrieval, PDF text verification,
  and read-only GitHub HEAD checks; no training.
---

# Cycle 36: PDPS-MCO literature and GitHub evidence

## Retrieval record

The archive is under `literature/cycle36_pdps_mco_20260803/`. The consolidated manifest records source edition, typed OA status, SI status, page count, byte count, and SHA-256. The downloader requested supporting information by default. The Nature paper's main OA PDF was downloaded, but its SI attempt is `fetch_failed` because the local CDP proxy was unavailable. The other retrieved PDFs have SI `not_found`. The initial exact DOI OA route returned `oa_not_found` for the two Elsevier records; lawful OSTI and arXiv public versions were then used where available. Publisher-final-version equivalence is not claimed for those public manuscripts/preprints.

## What each paper supports—and does not support

### 1. Learning viscoelasticity models from indirect data using deep neural networks

The verified public manuscript supports a PDE-constrained inverse-learning pattern: infer parametric or neural viscoelastic constitutive behavior from indirect displacement observations, with automatic/implicit differentiation around numerical schemes. It is relevant to hidden constitutive identification and differentiable calibration.

It does not support a causal graph-level second-order hard-EOM surrogate, Bouc-Wen history ownership, matrix edge endpoint force assembly, halo equivalence, or a solver-free fast rollout. The paper explicitly concerns inverse computation and numerical PDE solution; it is not evidence for PDPS-MCO's runtime or structural contract.

### 2. A hybrid numerical methodology coupling ROM and GNN for structural dynamics

The verified arXiv version supports combining classical reduced-order modeling with GNNs for heterogeneous/non-parametric geometries and structural-dynamics design iteration. It is evidence for geometry-conditioned latent reduction and a ROM/GNN division of labor.

It does not establish exact constitutive state evolution, authoritative endpoint force ownership, hard mass EOM at every step, Bouc-Wen reversal behavior, or full-vs-halo force/gradient equality. The DOI target is represented here by the lawful arXiv preprint, not asserted as the publisher PDF.

### 3. Multi-level physics informed deep learning for PDEs in computational structural mechanics

The verified published OA PDF supports multi-level physics-informed learning for computational structural-mechanics PDEs, including the use of physics residuals across levels/scales. It is relevant to multilevel training and residual design.

It does not prove exact time integration, local constitutive state ownership, general matrix endpoint forces, subgraph halo synchronization, or long-horizon high-frequency stability. Its SI was requested but not retrieved because the CDP route was unavailable.

### 4. Time-Continuous Energy-Conservation Neural Network for Structural Dynamics Analysis

The verified arXiv paper supports a time-continuous energy-based neural parameterization for structural dynamics, including SDOF-to-MDOF examples, damping/external-force extensions, and a motivation for long-term energy behavior. It is relevant to energy-aware state-space parameterizations.

It does not provide a Bouc-Wen edge-state protocol, exact sparse endpoint force scatter, matrix-edge/owner-halo semantics, or an independent hard EOM certificate for this project. Energy conservation in the reported construction cannot be promoted to forced/damped hysteretic graph dynamics without new gates.

### 5. Stable Long-Horizon Spatiotemporal Prediction on Meshes Using Latent Multiscale Recurrent GNNs

The verified arXiv paper supports latent recurrent graph representations, multiscale temporal coupling, variational graph compression, and long-horizon mesh-field prediction in its powder-bed-fusion temperature setting. It is relevant to latent multiscale recurrence and rollout-stability diagnostics.

It does not establish structural second-order mechanics, exact mass EOM, constitutive path dependence, edge force authority, matrix edge laws, or structural halo/owner synchronization. Its long-horizon evidence is task-specific and cannot be treated as a stability certificate for nonlinear structural dynamics.

## PDPS-MCO versus existing project routes

| Route | Primary authority | State/physics boundary | Evidence that does not transfer automatically |
|---|---|---|---|
| PDPS-MCO | Intended project candidate: physical/discrete state with learned prediction or correction around mechanics | Must retain `u/v/a`, constitutive edge state, endpoint force authority, hard EOM, and owner/halo semantics | None of the five papers supplies this full contract; it remains a project-specific hypothesis |
| GraphPhyGRU | Direct graph-temporal recurrent predictor with project constitutive components | Historical strong direct baseline, but output width/scale and complete physics certification remain limited | Do not infer exact hard EOM or universal cross-graph sharing from its accuracy numbers |
| PRNN (`SLIMM-Lab/pyprnn`) | Intact material constitutive model embedded in an encoder-decoder recurrent architecture | Material/path-dependent surrogate demonstration, primarily micromodel constitutive behavior | It is not a graph-level structural dynamics solver and does not provide node mass/halo EOM authority |
| Temporal-parallel | Parallel temporal graph model with project-specific mechanics/constitutive paths | Efficient sequence processing and parent/checkpoint compatibility are the main project assets | Parallel recurrent prediction is not by itself a proof of endpoint force, history, or high-frequency stability |

## GitHub refresh

Read-only `git ls-remote` checks report:

- `SLIMM-Lab/pyprnn`, `refs/heads/main`: `5d2aca4211c4a783b9e6964fd34f2b611f2e2c15`.
- `dodaltuin/soft-tissue-pignn`, `refs/heads/main`: `7623b2eae4e203ae933c05f1f251ff9fb0d74574`.

The refresh changed no repositories or remote state.

## Transfer decision for the next candidate

Transfer only bounded hypotheses: constitutive state can be learned or embedded, latent multiscale recurrence may help long rollouts, and ROM/GNN features may reduce geometry cost. Treat as hard counterexamples the absence of a second-order endpoint EOM, matrix edge force authority, history/owner synchronization, damping/work accounting, and high-frequency stability evidence. No paper here authorizes training or remote execution by itself.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
