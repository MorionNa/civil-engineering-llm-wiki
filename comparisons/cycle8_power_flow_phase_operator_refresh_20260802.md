---
id: comparison--cycle8_power_flow_phase_operator_refresh_20260802
title: 'Cycle 8 evidence refresh: power-flow phase carriers and function-space interfaces
  (2026-08-02)'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 8 evidence refresh: power-flow phase carriers and function-space interfaces (2026-08-02)

## Retrieval and status

The Nature retrieval workflow shortlisted two new DOI records and downloaded both published OA PDFs. Supporting Information was requested by default but remained unavailable because the local CDP proxy was unreachable.

| Paper | Venue | DOI | Status | SHA256 prefix |
|---|---|---|---|---|
| Research on structural damage identification based on temporal power flow graph network | Scientific Reports (2026) | 10.1038/s41598-026-37356-7 | open_access_downloaded | 96e7d1ef2f7c |
| Principled approaches for extending neural architectures to function spaces for operator learning | Nature Machine Intelligence (2026) | 10.1038/s42256-026-01267-z | open_access_downloaded | 61779ed2c61a |

Manifest: `papers/literature_20260802_cycle8/manifest.json`.

GNSS, `Graph Network-based Structural Simulator` (arXiv:2510.25683), and the LSTM-GNN nonlinear mechanical field reconstruction paper (arXiv:2606.10909) were reviewed as supplemental recall sources. They are not treated as Nature-whitelist primary shortlist records. The existing pinned GitHub repositories from cycle 7 were checked for refresh; a live fetch of `hanjq17/GMN` timed out, so the prior verified commits remain pinned. No new repository is used as implementation authority.

## Transferable evidence

1. TPF-GNet explicitly defines an edge force from known stiffness/damping and relative kinematics and uses instantaneous power flow as a temporal graph message. For this project, only a bounded **nominal linear-operator power proxy** is transferable. It must never replace the nonlinear constitutive force, enter `kx+cv+ma=F`, or be interpreted as actual Bouc-Wen dissipation.
2. GNSS reports local kinematics and a sign-aware acceleration loss for reducing phase errors in structural wave rollouts. Its autoregressive rollout/updater and connectivity redesign are excluded from the present direct whole-trajectory deployment. A sign loss alone is rejected as another loss reweighting family after TDDM/DSTR failures.
3. The Nature Machine Intelligence function-space paper makes quadrature/coordinate dependence explicit. The relevant project consequence is that every new edge carrier must use fixed model scales and per-edge matrix norms, never batch or subgraph statistics; otherwise full-graph and halo-subgraph predictions cease to represent the same operator.

## Candidate boundary authorized for design review

Sol recommended a single candidate for local implementation review: **PPEC-M0 (Power-Flow/Phase Edge Carrier)**. It computes normalized relative displacement and velocity, endpoint nominal K/C force rows, signed nominal power, bounded phase features, and a damping-availability mask before the existing constitutive state bound. A zero-initialized pointwise carrier may alter only constitutive-state logits; the existing plugin remains the sole source of edge force and signed node force.

The candidate is distinct from frozen BEMCI-M0 (memory-only interface), the failed edge-kinematic high-frequency adapter (high-pass/low-pass residual branch), and all residual/sample-weighting schemes. It has no new temporal memory, graph hop, force correction, constitutive call, FFT, or online solver.

## Hard rejection rules

- If a graph lacks edge damping weights, the damping contribution is zero with an explicit availability mask; damping may not be arbitrarily distributed across edges.
- The nominal power proxy is not used as a constitutive residual or EOM term for nonlinear laws.
- Any warm-start drift, extra constitutive call, halo mismatch, or speed overhead above 5% freezes the candidate.
- Even if local structural gates pass, remote training remains separately gated by a meaningful improvement in worst displacement or high-modal edge performance; pooled R2 alone is insufficient.

Sources: [TPF-GNet](https://www.nature.com/articles/s41598-026-37356-7), [function-space operator principles](https://www.nature.com/articles/s42256-026-01267-z), [GNSS supplemental preprint](https://arxiv.org/abs/2510.25683), [nonlinear mechanical field reconstruction supplemental preprint](https://arxiv.org/abs/2606.10909).

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
