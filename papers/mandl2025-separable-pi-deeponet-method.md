---
title: "Sep-PI-DeepONet Method"
created: 2026-07-31
updated: 2026-07-31
type: paper-analysis
sources: [raw/papers/mandl2025-separable-pi-deeponet-source.md]
confidence: high
---

# Method

## Core idea

Sep-PI-DeepONet extends Physics-Informed DeepONet using separable representations.

Traditional operator representation:

$$G(u)(y)=\sum_i b_i(u)t_i(y)$$

The separable trunk represents high-dimensional functions through products of lower-dimensional components.

```text
High-dimensional PDE
        ↓
separable representation
        ↓
low-dimensional trunk components
        ↓
physics residual evaluation
```

## Mechanism

The method reduces the cost of evaluating derivatives and physics constraints by exploiting tensor-product-like separability.

## Relation to other methods

- DeepONet: learns function-to-function operators.
- PINN: enforces PDE residuals.
- Sep-PI-DeepONet: combines operator learning with separable physics constraints.

## Structural dynamics relevance

Potential migration:

- spatial structural modes as separable basis;
- temporal earthquake response as separate operator component;
- parameterized structures as branch inputs.
