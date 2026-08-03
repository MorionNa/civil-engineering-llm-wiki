---
id: source--li2022-bfemp
title: "Li et al. (2022) — BFEMP 来源记录"
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- bfemp
- mpm-fem-coupling
- barrier-contact
- implicit-integration
- frictional-contact
sources:
- raw/papers/li2022-bfemp-source.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
evidence_scope: full-text
---

# BFEMP：Interpenetration-free MPM–FEM Coupling with Barrier Contact

## Bibliographic Record

- Xuan Li, Yu Fang, Minchen Li, Chenfanfu Jiang.
- *Computer Methods in Applied Mechanics and Engineering*, 390 (2022), 114350.
- DOI: 10.1016/j.cma.2021.114350.
- Full-text evidence from the user-provided 25-page publisher PDF. ^[raw/papers/li2022-bfemp-source.md]

## Evidence Map

- **pp. 1–3:** motivation, prior MPM–FEM coupling limitations, BFEMP contribution and IPC ancestry.
- **pp. 3–7:** governing equations, incremental variational integration, separate FEM/MPM discretizations and APIC/PIC/FLIP transfers.
- **pp. 8–10:** particle–FEM boundary barrier potential, boundary quadrature approximation and chain-rule transfer to MPM grid DOFs.
- **pp. 11–13:** friction mollification, lagged dissipative pseudo-potential, projected Newton solver and CCD/determinant filtered line search.
- **pp. 14–22:** momentum/energy, irregular boundaries, Hertzian disk, friction threshold, refinement, buckling and 3D twist experiments.
- **pp. 22–23:** conclusions and limitations concerning particle-domain overlap and cutting.

## Central Claims Supported by the Paper

1. BFEMP monolithically couples implicit MPM and FEM through barrier-energy particle–mesh contact.
2. Contact is defined between MPM particles and FEM boundary simplices, while MPM unknowns remain grid-node displacements.
3. A filtered line search prevents particle penetration and deformation-gradient degeneracy throughout nonlinear iterations.
4. Prescribing all FEM displacements converts the method into a separable irregular-boundary treatment for MPM.
5. Numerical studies support momentum preservation, bounded contact/friction errors and refinement convergence under the tested settings.

## Evidence Boundaries

- The paper does not model dynamic conversion between FEM and MPM; the two domains remain separately discretized and interact through contact.
- Strict non-penetration concerns material-point centers versus FEM boundary primitives; finite particle support can still create small physical-domain overlap.
- Fully implicit friction uses lagged normal forces and tangent frames; convergence is not guaranteed for arbitrarily large time steps.
- The paper provides seven numerical examples, only one in 3D, and no reinforced-concrete collapse validation.
- No public BFEMP code URL is stated in the supplied main-text PDF.

## Derived Knowledge Pages

- [[li2022-bfemp-analysis]]
- [[li2022-bfemp-method]]
- [[li2022-bfemp-results]]
- [[li2022-bfemp-critical]]
- [[entities/bfemp]]
- [[concepts/particle-simplex-barrier-coupling]]
- [[concepts/separable-mpm-boundary-via-fem]]
