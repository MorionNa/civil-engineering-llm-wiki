---
id: papers--mandl2025-separable-pi-deeponet-method
title: Sep-PI-DeepONet Method
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/neural-operator
- method/pinn
sources:
- sources/papers/mandl2025-separable-pi-deeponet.md
created: '2026-07-31'
updated: '2026-07-31'
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

## Evidence By Source

### `sources/papers/mandl2025-separable-pi-deeponet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/mandl2025-separable-pi-deeponet-source.md`

^[sources/papers/mandl2025-separable-pi-deeponet.md]

## Related Indexes

- [[papers/index]]
- [[index]]
