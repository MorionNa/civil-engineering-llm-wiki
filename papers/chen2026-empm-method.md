---
id: paper--chen2026-empm-method
title: Chen et al. (2026) — EMPM 方法机制
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
keywords:
- apic
- differentiable-mpm
- online-system-identification
- particle-grid
- real-to-sim-to-real
sources:
- sources/papers/chen2026-empm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
evidence_scope: full-text
---

# EMPM 方法机制

## Architecture And Data Flow

```text
multi-view RGB-D video
  → Grounded SAM2 segmentation
  → fused 3D point cloud + 3D tracked points
  → controller motion as boundary velocity
  → differentiable MPM rollout
  → Chamfer / tracking / mask losses
  → gradient-based or CMA-ES parameter update
  → MPM particle prediction + Gaussian rendering
```

Figure 2 separates data preprocessing, model optimization and downstream robotic use. ^[sources/papers/chen2026-empm.md]

## State And Parameters

The particle state at time $t$ contains positions $x_p$, velocities $v_p$ and deformation gradients $F_p$. The action-conditioned transition is

$$\hat X_{t+1}=f_\theta(X_t,u_t),$$

where $u_t$ is hand or gripper motion and $\theta$ includes Young's modulus $E$, Poisson's ratio $\nu$, density $\rho$ and plastic yield stress $y$.

## MPM Update

The simulator uses APIC-style particle-to-grid transfer, grid update under stress, gravity, contact and imposed controller velocity, followed by grid-to-particle transfer and deformation-gradient update. The paper applies Fixed Corotated elasticity and von Mises return mapping for plasticity. Robot or hand motion enters as Dirichlet boundary velocity; table and gripper contact use Coulomb friction. ^[sources/papers/chen2026-empm.md]

## Offline Identification

The offline loss combines 3D Chamfer distance and tracked-particle squared error:

$$L_{offline}=\lambda_{dist}\sum_t Chamfer(\hat X_t,\tilde X_t)+\lambda_{trk}\sum_t\sum_{j\in T_t}\lVert\hat X_{t,j}-\tilde X^{trk}_{t,j}\rVert_2^2.$$

Warp differentiates through the rollout. The authors also retain CMA-ES as a zero-order option when memory or aggressive parameter search is preferred.

## Online Adaptive Identification

Streaming RGB-D observations are segmented and back-projected to 3D. Because long-horizon tracking becomes unreliable, online correction omits tracked-point loss. At quasi-static states, the method performs a fixed $H$-step rollout and minimizes

$$L_{online}=\lambda_{dist}L_{dist}+\lambda_{mask}L_{mask}.$$

The updated material parameters replace the current simulator parameters after each correction step.

## Appearance Coupling

The initial point cloud supports a 3D Gaussian Splatting model. Gaussian centers follow neighboring MPM particles through Linear Blend Skinning, enabling photorealistic rendering of simulated deformation.

## Assumptions And Failure Boundaries

- Material parameters are constant over the material field.
- Online updates are restricted to near-equilibrium states.
- Reliable segmentation and depth calibration are assumed.
- Tracking quality is critical offline and degrades under occlusion.
- The paper demonstrates parameter identification and rollout, not closed-loop autonomous control.

## Related Pages

- [[chen2026-empm-analysis]]
- [[chen2026-empm-results]]
- [[chen2026-empm-critical]]
- [[entities/empm]]
