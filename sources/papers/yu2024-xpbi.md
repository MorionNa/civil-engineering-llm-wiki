---
id: source--yu2024-xpbi
title: Yu et al. (2024) — XPBI source note
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- xpbd
- xpbi
- continuum-inelasticity
- updated-lagrangian
- smoothing-kernel
sources:
- raw/papers/yu2024-xpbi-source.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
---

# Yu et al. (2024) — XPBI

## Bibliographic Record

- **Title:** XPBI: Position-Based Dynamics with Smoothing Kernels Handles Continuum Inelasticity
- **Authors:** Chang Yu, Xuan Li, Lei Lan, Yin Yang, Chenfanfu Jiang
- **Version:** arXiv:2405.11694v2 [cs.GR], 14 September 2024
- **Pages:** 12
- **Source file:** `2405.11694v2.pdf`

## Evidence Map

- **pp. 1–2:** motivation, relation between XPBD and MPM, updated-Lagrangian interpretation, contributions.
- **pp. 3–4:** StVK-Hencky constraint formulation, velocity-gradient-based deformation-gradient update, smoothing-kernel gradient correction.
- **pp. 5–7:** implicit plasticity fixed point, velocity-primary XPBD, colored Gauss–Seidel, XSPH and position correction.
- **pp. 7–10:** comparisons, convergence, scalability, timing, timestep study and demonstrations.
- **p. 10:** limitations and future work.

## Core Claims

XPBI augments XPBD with meshless updated-Lagrangian deformation-gradient tracking and classical continuum return mappings. It uses velocity as the primary unknown, estimates velocity gradients with corrected Wendland kernels, alternates XPBD updates with plastic projection, and supports Von Mises, Drucker–Prager, NACC and Herschel–Bulkley materials. The paper reports examples with up to 4 million particles and a 20k-particle interactive case at 30 fps.

## Evidence Boundary

The paper is a computer-graphics preprint. Its validation emphasizes visual plausibility, qualitative comparisons, solver residuals and runtime. It does not establish engineering-grade constitutive calibration, conservation-error bounds, fracture-energy convergence, or structural-collapse accuracy. It also explicitly states that quantitative convergence of the plastic fixed-point iteration is not monitored.

## Persistent Provenance

^[raw/papers/yu2024-xpbi-source.md]
