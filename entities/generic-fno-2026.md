---
id: entity--generic-fno-2026
title: Sulskis & Ravi (2026) GENERIC-FNO
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_evidence_scope: first-3-pages-only
legacy_tags:
- neural-operator
- energy-consistency
- entropy-production
- dissipative-dynamics
- fourier-neural-operator
legacy_sources:
- ../../../../papers/literature_20260802/GENERIC_FNO_2606_08343/PDFs/GENERIC-FNO_Embedding_Energy_Conservation_and_Entropy_Production_into_Fourier_Neural_Operators.pdf
- ../../../../papers/literature_20260802/GENERIC_FNO_2606_08343/manifest.json
evidence_scope: first-3-pages-only
---

# GENERIC-FNO

Sulskis & Ravi propose embedding the GENERIC/metriplectic structure into a Fourier neural operator. The abstract and introduction describe separate reversible energy-conserving and irreversible entropy-producing operators, coupled by degeneracy constraints; the PDF was downloaded from arXiv `2606.08343v3` and has 26 pages. Supporting information was not found in the downloader manifest.

## Relevance to this project

The transferable idea is to parameterize an energy/dissipation contribution with structural constraints instead of adding another unconstrained response head. For this project, such a term belongs inside a replaceable edge constitutive plugin; it must not replace matrix-edge `MechConv` assembly or the explicit `B^T f_e` balance.

## Limits and negative knowledge

The first three pages do not establish exact structural-dynamics EOM closure, matrix-edge subgraph equivalence, Bouc–Wen history identifiability, or a speed advantage over Newmark/FEM. Therefore GENERIC-FNO is a loss/parameterization inspiration only. [[mtp-mechconv-v2]] [[structured-state-space-s4]] [[hano-2025-history-aware-neural-operator]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
