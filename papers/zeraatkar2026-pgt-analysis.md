---
title: "Zeraatkar et al. (2026) — Physics-Guided Transformer (PGT): Physics-Aware Attention Mechanism for PINNs"
created: 2026-07-22
updated: 2026-07-22
type: paper-analysis
tags: [physics-informed, pinn, transformer, attention, ai4s, diffusion-models, navier-stokes, heat-equation]
sources: [raw/papers/2603.27929v1.pdf]
confidence: high
---

# Physics-Guided Transformer (PGT)

## 1. Engineering Background

PINNs usually introduce governing equations as soft penalties in the loss function. However, under sparse observations, this often causes gradient imbalance, optimization instability, and poor physical consistency. PGT argues that physics should not only constrain optimization, but also determine information propagation inside the neural architecture.

## 2. Research Gap

Existing PINNs, PINNsFormer and neural operators generally keep attention or feature propagation data-driven, while PDE constraints remain external losses. PGT aims to embed physical causality and propagation rules directly into Transformer attention.

## 3. Core Idea

PGT modifies self-attention:

$$A=softmax(QK^T/\sqrt d+\Gamma)V$$

where Gamma is a physics-guided bias derived from the Green's function of the governing PDE.

For diffusion systems, Gamma is constructed from the heat kernel, enforcing spatial diffusion locality and forward temporal causality.

## 4. Architecture

Pipeline:

```
sparse observations
 -> physics-guided Transformer encoder
 -> cross-attention query conditioning
 -> FiLM-modulated SIREN decoder
 -> continuous physical field
```

The model combines:

- physics-aware attention;
- implicit neural representation;
- FiLM frequency modulation;
- PINN-style PDE supervision.

## 5. Main Contributions

1. Move physical priors from loss functions into attention computation.
2. Use Green-function-based attention bias to encode causal propagation.
3. Combine physics-guided encoding with adaptive implicit decoding.
4. Demonstrate sparse reconstruction on heat equation and Navier-Stokes systems.

## 6. Relevance to Structural Dynamics

PGT provides a possible direction for structural-response PINNs:

Instead of only adding equation residual loss:

$$M\ddot u+C\dot u+f(u)-F=0$$

physical information can enter attention:

$$\Gamma=f(M,K,C,\Phi,t)$$

allowing attention to follow modal propagation, structural connectivity and temporal causality.

## 7. Limitations

- Validation focuses on PDE fields rather than structural hysteretic dynamics.
- Physics bias requires known propagation kernels.
- Nonlinear constitutive behavior is not explicitly modeled.
- Extension to collapse, contact and strong material nonlinearity remains open.

## Related

- [[pinn]]
- [[cm-pinns]]
- [[seisgpt]]
- [[zeraatkar2026-pgt-method]]
