---
id: source--li2020-incremental-potential-contact
title: "Li et al. (2020) — Incremental Potential Contact 来源记录"
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- incremental-potential-contact
- contact-mechanics
- barrier-method
- friction
- continuous-collision-detection
sources:
- raw/papers/li2020-incremental-potential-contact-source.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
evidence_scope: full-text
code_url: []
---

# Li et al. (2020) — Incremental Potential Contact

## Bibliographic Record

- **Title:** Incremental Potential Contact: Intersection- and Inversion-free, Large-Deformation Dynamics
- **Authors:** Minchen Li, Zachary Ferguson, Teseo Schneider, Timothy Langlois, Denis Zorin, Daniele Panozzo, Chenfanfu Jiang, Danny M. Kaufman
- **Venue:** ACM Transactions on Graphics 39(4), Article 49
- **Publication date:** July 2020
- **DOI:** 10.1145/3386569.3392425
- **Original material:** `raw/papers/li2020-incremental-potential-contact-source.md`

## Evidence Scope

This source note is based on the complete 20-page user-provided paper. Claims below are restricted to the supplied main text. Supplemental derivations, videos, benchmark files, and the released implementation were not independently inspected or executed.

## Evidence Map

- **Pages 1–2:** problem statement, guarantees, scale claims, contributions;
- **Pages 3–4:** admissible trajectories, incremental potential, accuracy measures;
- **Pages 6–8:** local smooth barrier, projected Newton solver, CCD-aware line search, contact guarantees;
- **Pages 9–11:** smoothed and lagged variational friction, friction-accuracy limits;
- **Pages 11–12:** primitive distances and near-parallel edge mollification;
- **Pages 13–17:** unit tests, extreme deformation, friction benchmarks, scale and accuracy;
- **Pages 17–19:** comparison boundaries and unresolved friction-lag convergence;
- **Page 20:** benchmark statistics.

## Core Claims Supported by the Paper

1. IPC rewrites implicit contact time stepping as minimization of an incremental potential augmented by a local barrier over unsigned primitive distances.
2. A CCD-filtered line search maintains non-intersection during every nonlinear iterate; paired with a non-inverting constitutive energy, element inversion is also avoided.
3. Contact geometry accuracy, dynamic solve accuracy, and static-friction accuracy are exposed as separate tolerances.
4. Friction is approximated by a smoothed, lagged dissipative potential; lagged friction iterations do not have a general convergence guarantee.
5. The paper demonstrates problems up to 688K nodes and 2.3M tetrahedra, and reports as many as 498K contact constraints per time step.

## Evidence Boundaries

- “Intersection-free” relies on the implemented floating-point CCD and conservative advancement; exact rational CCD was used only as a slower post-check on selected stress tests.
- “Inversion-free” additionally requires a non-inverting elasticity energy such as neo-Hookean; fixed-corotational energy does not provide the same guarantee.
- The lagged friction formulation lacks a general convergence guarantee in high-speed or large-deformation cases.
- The paper predates later IPC variants and does not itself establish current best performance.
- Open-source release is stated, but the main-text PDF does not provide a direct project URL and no code reproduction was performed here.

## Derived Knowledge Pages

- [[li2020-incremental-potential-contact-analysis]]
- [[li2020-incremental-potential-contact-method]]
- [[li2020-incremental-potential-contact-results]]
- [[li2020-incremental-potential-contact-critical]]
- [[entities/incremental-potential-contact]]
- [[concepts/local-smooth-contact-barrier]]
- [[concepts/ccd-filtered-feasible-line-search]]
