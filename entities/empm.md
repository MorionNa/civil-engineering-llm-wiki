---
id: entity--empm
title: EMPM — Embodied Material Point Method
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- entity/model
- evidence/paper
keywords:
- deformable-object
- differentiable-mpm
- digital-twin
- online-identification
- real-to-sim-to-real
sources:
- sources/papers/chen2026-empm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
---

# EMPM

## Definition

EMPM is an embodied, differentiable Material Point Method framework for reconstructing, identifying, simulating and visually rendering deformable objects from multi-view RGB-D observations. It combines MPM continuum mechanics, parameter optimization, 3D point-cloud supervision and Gaussian Splatting. ^[sources/papers/chen2026-empm.md]

## Core Components

- Multi-view RGB-D fusion and segmentation.
- Offline 3D point tracking.
- APIC-style differentiable MPM implemented with Warp.
- Fixed Corotated elasticity and von Mises plastic return mapping.
- Chamfer, tracking and mask losses.
- Offline and online material-parameter correction.
- 3DGS appearance model driven by MPM particles.

## Project Role

EMPM is relevant to differentiable system identification and local particle-based fracture simulation. For the user's structural-collapse research, it is most useful as evidence that MPM parameters can be updated from observation and embedded in an action-conditioned digital twin. It is not itself a building-collapse solver.

## Evidence Boundary

The current entity page is grounded in the full text of arXiv:2601.17251v1. No independent code execution or reproduction was performed.

## Related Pages

- [[chen2026-empm-analysis]]
- [[chen2026-empm-method]]
- [[chen2026-empm-results]]
- [[chen2026-empm-critical]]
- [[entities/3d-gaussian-splatting]]
