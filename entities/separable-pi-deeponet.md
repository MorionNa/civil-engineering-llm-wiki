---
id: entities--separable-pi-deeponet
title: Separable Physics-Informed DeepONet (Sep-PI-DeepONet)
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- method/neural-operator
- method/pinn
keywords:
- deeponet
- domain/ai4s
- entity/model
- method/neural-operator
- method/pinn
- neural-operator
- operator-learning
- physics-informed
- scientific-machine-learning
sources:
- raw/papers/mandl2025-separable-pi-deeponet-source.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: high
---

# Separable Physics-Informed DeepONet

Sep-PI-DeepONet 是 Mandl et al. (2025) 提出的物理信息神经算子架构，用于缓解高维 PDE 中 DeepONet 的维度灾难。

## 核心思想

将传统 DeepONet 的多维 trunk：

$$t(x_1,x_2,...,x_d)$$

改写为低秩可分离形式：

$$\sum_r \prod_q t_q(x_q)$$

通过一维 trunk 网络组合得到高维表示。

## 与 PINN / DeepONet 的关系

- [[deeponet]]：学习函数到函数映射。
- [[pinn]]：通过物理残差约束训练。
- Sep-PI-DeepONet：将两者结合，并利用可分离表示降低物理残差计算成本。

## 结构动力应用潜力

适用于：

- 地震动到结构响应算子学习；
- 多参数结构响应预测；
- 大自由度系统低秩时空表示。

## 关联

- [[mandl2025-separable-pi-deeponet-analysis]]
- [[kolmogorov-n-width-piml]]
- [[rathore2024-pinn-loss-landscape-analysis]]

## Evidence By Source

### `raw/papers/mandl2025-separable-pi-deeponet-source.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/mandl2025-separable-pi-deeponet-source.md]
