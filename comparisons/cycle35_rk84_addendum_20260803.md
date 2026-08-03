---
id: comparison--cycle35_rk84_addendum_20260803
title: 'Cycle 35 addendum: eight-stage pseudo-symplectic RK(4,8)'
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_tags:
- runge-kutta
- pseudo-symplectic
- phase-accuracy
- lco-rk8
---

# Eight-stage pseudo-symplectic RK(4,8)

*Eight-stage pseudo-symplectic Runge-Kutta methods of order (4, 8)*, arXiv `2301.09335v4` (revised 2025-02-16), is the direct numerical-analysis source for a one-parameter family of eight-stage methods with nonlinear order four and pseudo-symplectic order eight.

Verified local artifact:

- PDF: `literature/cycle35_state_space_spacetime_operator_20260803/PDFs/Eight-stage_pseudo-symplectic_Runge-Kutta_methods_of_order_(4,_8).pdf`
- SHA256: `5edaf85cd869065f486e7af1aa6ede2cee9f38e50fcfe955ea1e20e2b93abb98`
- 23 pages; SI requested and not found.

This replaces the earlier unsupported wording “lock the stability polynomial to P8” with an auditable concrete tableau family. It does not prove forced/damped/history-dependent graph dynamics, so LCO still requires the local matrix-edge, Bouc-Wen, work, halo, and speed gates.

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
