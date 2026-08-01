---
id: sources--papers--chen2026-empm
title: Chen et al. (2026) — EMPM: Embodied MPM for Modeling and Simulation of Deformable Objects
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
keywords:
- differentiable-mpm
- deformable-object
- digital-twin
- gaussian-splatting
- material-identification
- online-adaptation
- robotics
sources:
- raw/papers/chen2026-empm-source.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
evidence_scope: full-text
code_url: []
dataset_url: []
---

# Source Note — EMPM

## Bibliographic Record

- **Title:** EMPM: Embodied MPM for Modeling and Simulation of Deformable Objects
- **Authors:** Yunuo Chen, Yafei Hu, Lingfeng Sun, Tushar Kusnur, Laura Herlant, Chenfanfu Jiang
- **Affiliations:** Robotics and AI Institute; UCLA
- **Version:** arXiv:2601.17251v1, 24 January 2026
- **Project website:** https://embodied-mpm.github.io
- **Evidence:** user-provided 9-page full-text PDF.

## Evidence Scope

The paper presents a real-to-sim-to-real pipeline that combines multi-view RGB-D reconstruction, 3D Gaussian Splatting appearance modeling, differentiable Material Point Method simulation, offline parameter identification and online correction. It evaluates elastic and elastoplastic objects, compares against PhysTwin and PGND, and demonstrates a proof-of-concept bimanual Franka manipulation workflow.

## Page Map

- **pp. 1–2:** motivation, contributions, related work.
- **pp. 3–5:** system overview, MPM equations, offline and online identification.
- **pp. 5–8:** experimental setup, qualitative and quantitative results, applications and limitations.
- **p. 9:** references.

## Generated Knowledge Pages

- [[papers/chen2026-empm-analysis]]
- [[papers/chen2026-empm-method]]
- [[papers/chen2026-empm-results]]
- [[papers/chen2026-empm-critical]]
- [[entities/empm]]
