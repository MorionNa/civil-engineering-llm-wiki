---
id: source--du2024-embedded-ipc
title: Du et al. (2024) — Embedded IPC source note
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
keywords:
- embedded-ipc
- reduced-order-modeling
- barrier-contact
- robotics
- collision-surface
sources:
- raw/papers/du2024-embedded-ipc-source.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---

# Du et al. (2024) — Embedded IPC

## Bibliographic Record
- *Embedded IPC: Fast and Intersection-free Simulation in Reduced Subspace for Robot Manipulation*.
- arXiv:2409.16385v1 [cs.RO], 24 September 2024.
- Ten authors from UCLA, Toyota Research Institute, University of Utah and UCSD.

## Evidence Scope
Full-text review of an eight-page preprint. The paper derives reduced-coordinate backward-Euler incremental potential dynamics, composes full-resolution IPC barrier/friction energies with a linear embedding map, constructs the map from a coarse tetrahedral mesh to a high-resolution collision surface, and evaluates soft-gripper manipulation.

## Directly Supported Claims
1. Elasticity is solved on a low-resolution tetrahedral subspace while collision constraints remain on the original high-resolution surface.
2. The method uses Projected Newton, CCD-limited line search and ACCD, inheriting IPC's intersection-free feasible path under the stated assumptions.
3. Full-space IPC and affine body dynamics are special cases of the framework.
4. In the teddy-bear grasping test, the low-resolution embedding is reported about 2.0× faster than full-space IPC and reaches 1.8× real-time at $h=0.02$ s.
5. The plate-placement test shows deformation and penetration differences against Drake and Isaac Sim, but real–simulation state mismatches remain.

## Evidence Boundaries
- Preprint evidence only.
- Small subspaces can lock under large deformation.
- Only volumetric soft bodies are handled.
- Coarse embedding meshes are constructed heuristically.
- IPC has action at a distance inside its activation layer.
- Parallel implementation differences partly affect runtime comparisons.
- Robot examples do not validate structural-collapse fragments or arbitrary topology change.

## Related Pages
- [[du2024-embedded-ipc-analysis]]
- [[du2024-embedded-ipc-method]]
- [[du2024-embedded-ipc-results]]
- [[du2024-embedded-ipc-critical]]
- [[entities/embedded-ipc]]
- [[concepts/coarse-elasticity-fine-contact-embedding]]
- [[concepts/reduced-coordinate-ipc]]

## Persistent Provenance
^[raw/papers/du2024-embedded-ipc-source.md]
