---
id: papers--mandl2025-separable-pi-deeponet-analysis
title: Mandl et al. (2025) — Separable Physics-Informed DeepONet
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/graph-neural-network
- method/neural-operator
- method/pinn
keywords:
- curse-of-dimensionality
- deeponet
- neural-operator
- pde
- physics-informed
- scientific-machine-learning
sources:
- sources/papers/mandl2025-separable-pi-deeponet.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: high
methods:
- separable-operator-learning
- low-rank-representation
- pi-deeponet
results:
- high-dimensional-pde
- reduced-collocation-cost
failure_modes:
- rank-selection-dependence
- separability-assumption
reproducibility: high
---

# Separable Physics-Informed DeepONet

> Mandl et al. (2025), Computer Methods in Applied Mechanics and Engineering 434, 117586.

## 1. Engineering Background

Physics-informed machine learning suffers from dimensionality curse because collocation points and physical residual evaluation become expensive in high-dimensional PDEs.

## 2. Research Gap

Physics-informed DeepONet introduces physical constraints into operator learning, but high-dimensional residual computation remains expensive.

## 3. Scientific Question

Can separable representations transform high-dimensional physics constraints into scalable low-dimensional computations?

## 4. Research Objective

Develop a Separable Physics-Informed DeepONet (Sep-PI-DeepONet) that reduces the computational burden of high-dimensional PDE learning while preserving physical constraints.

## 5. Method Mechanism

→ [[mandl2025-separable-pi-deeponet-method]]

The method represents high-dimensional trunk functions through separable low-rank products, converting multidimensional operations into combinations of lower-dimensional components.

## 6. Result Evidence

→ [[mandl2025-separable-pi-deeponet-results]]

The paper demonstrates improved scalability for high-dimensional physics-informed operator learning problems.

## 7. Contribution

- Separable PI-DeepONet architecture.
- Reduced dimensionality burden for physics-informed operator learning.
- New route for scalable SciML models.

## 8. Core Knowledge

The key idea is that exploiting solution structure can be more effective than simply increasing network size.

## 9. Negative Knowledge

→ [[mandl2025-separable-pi-deeponet-critical]]

Performance depends on whether the target solution admits useful separable structure.

## 10. Transferable Knowledge

For structural dynamics, separable representations may be used for spatial modes, temporal evolution and parameterized response operators.

## 11. Research Opportunity

Combine separable operators with graph neural networks, Mamba/SSM temporal models and Kolmogorov n-width analysis for large-scale structural response prediction.

## 12. Reproducibility

Official code is available.

## Evidence By Source

### `sources/papers/mandl2025-separable-pi-deeponet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/mandl2025-separable-pi-deeponet-source.md`

^[sources/papers/mandl2025-separable-pi-deeponet.md]
