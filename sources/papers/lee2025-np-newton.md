---
id: source--paper--lee2025-np-newton
title: Lee et al. (2025) — Neural-Operator Preconditioned Newton — source note
type: source
status: verified
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
- method/neural-operator
keywords:
- nonlinear-preconditioning
- Newton
- FPNO
- MIONet
sources:
- ../../../literature/cycle37_pnp_dpc_20260803/open_access_preprints/npnewton/PDFs/A_Neural-Operator_Preconditioned_Newton_Method_for_Accelerated_Nonlinear_Solvers.pdf
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
evidence_scope: full-text
---

# Lee et al. (2025) — Neural-Operator Preconditioned Newton — Source Note

## Evidence Scope

- Scope: full-text arXiv manuscript, 16 pages.
- arXiv: 2511.08811.
- The downloaded PDF is 1,646,033 bytes with SHA-256 `0fe6d8cf81be3846351d5eb63c6aec4f23371487c0e2b4b144888323f760453a`.
- Verification: `%PDF` content, 16 nonzero pages, and title/abstract text extracted with pdfplumber.
- Supporting Information was requested by default; arXiv direct-PDF routing reported `not_found`.

## Original Materials

- `../../../literature/cycle37_pnp_dpc_20260803/open_access_preprints/npnewton/PDFs/A_Neural-Operator_Preconditioned_Newton_Method_for_Accelerated_Nonlinear_Solvers.pdf`
- `../../../literature/cycle37_pnp_dpc_20260803/open_access_preprints/npnewton/manifest.json`
- `../../../literature/cycle37_pnp_dpc_20260803/open_access_preprints/npnewton/npnewton_fulltext.txt`

## Derived Knowledge Pages

- [[lee2025-np-newton-analysis]]
- [[lee2025-np-newton-method]]
- [[lee2025-np-newton-results]]
- [[lee2025-np-newton-critical]]
- [[np-newton]]
- [[fixed-point-neural-operator]]

## Verification Notes

- Numerical values were checked against Tables 1–7 in the full manuscript.
- The paper studies nonlinear Poisson and quasi-static Neo-Hookean hyperelastic benchmarks, not second-order structural dynamics.
- No public implementation or dataset URL was found in the manuscript; reproducibility is therefore graded medium.

