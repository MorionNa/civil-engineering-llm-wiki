---
id: comparison--rpsl_literature_design_20260803
title: RPSL literature and design evidence — 2026-08-03
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# RPSL literature and design evidence — 2026-08-03

## New sources

OA retrieval completed through the Nature downloader:

- [Learning nonlinear operators in latent spaces](https://doi.org/10.1038/s41467-024-49411-w), PDF SHA256 \`04ca6503d91b90396553782d0f013025686d58dc9548d0cb60c79d812dc33ee1\`.
- [Temporal neural operator](https://doi.org/10.1038/s41598-025-16922-5), PDF SHA256 \`a5f77eb9435b56c80ac54a5ad513ab1db183100b9552c03c4805769f4b1f572c\`.

Manifest: \`literature/cycle31_broadband_state_operator_20260803/manifest.json\`.

Both main PDFs are verified OA downloads. Supporting-information requests were recorded as failed because the local CDP proxy was not running; no SI availability is claimed.

## Transferable evidence

The latent-operator paper motivates compressing high-dimensional dynamics into a lower-dimensional representation before operator decoding, with reported gains in accuracy and computational cost on large dynamical systems. The temporal-operator paper motivates causal history inputs and temporally bundled prediction, while also warning that long autoregressive rollouts can accumulate error.

These are representation principles only. They do not prove hard \(kx+cv+ma=F\), matrix-edge force ownership, subgraph equivalence, or Bouc–Wen path-state identifiability in this project.

The refreshed GitHub snapshots are:

- \`neuraloperator/neuraloperator\`: \`86a8bc7812a31b42c4f7895693cf4ac11521c066\`;
- \`neuraloperator/graph-pde\`: \`c28220a6558554a193303975adb60d8857d48c0c\`.

The graph-pde repository is deprecated upstream; its value here is historical evidence for graph-kernel/multilevel operator design, not a current implementation dependency.

## Candidate implication

RPSL uses causal path summaries as a low-rank shared hidden lift between existing MechConv blocks. It keeps the final matrix-edge force assembly and replaceable constitutive replay untouched. The decisive test is independent high-modal edge force plus independent BDF2 dynamics, not constructed equilibrium residual.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
