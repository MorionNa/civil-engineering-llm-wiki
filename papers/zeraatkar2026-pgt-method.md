---
id: papers--zeraatkar2026-pgt-method
title: Physics-Guided Transformer 方法机制
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/graph-neural-network
- method/transformer
keywords:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/graph-neural-network
- method/transformer
sources:
- sources/papers/zeraatkar2026-pgt.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# Physics-Guided Transformer 方法机制

## Problem And Inputs

PGT 从稀疏时空观测重构连续 PDE 场。每个 context token 包含坐标、时间和观测值；任意 query 坐标通过隐式解码器获得场值。

## Architecture

```text
稀疏观测 {(x_i,t_i,u_i)}
        ↓
Token embedding
        ↓
Physics-guided Transformer encoder
  Attention logits + Green-function bias Γ
        ↓
Context representation
        ↓
Query-coordinate cross-attention
        ↓
FiLM-modulated SIREN decoder
        ↓
连续场 uθ(x,t)
```

## Physics-Guided Attention

标准 attention logits 被物理偏置修正：

$$
A_{ij}=\operatorname{softmax}\left(\frac{q_i k_j^\top}{\sqrt d}+\Gamma_{ij}\right),
$$

其中 $\Gamma_{ij}=\log G(x_i-x_j,t_i-t_j;\theta_p)$ 来自控制方程的 Green 函数或传播核。

## Heat-Kernel Bias

对扩散方程：

$$
\Gamma_{ij}=-\frac{|x_i-x_j|^2}{4\alpha\Delta t_{ij}}-\frac d2\log(4\pi\alpha\Delta t_{ij}),\qquad \Delta t_{ij}>0.
$$

未来信息或不符合因果传播的 token 被设为 $-\infty$。偏置同时编码扩散长度、空间局部性和时间因果性。

## Other PDE Classes

- 双曲方程可用光锥支持限制有限传播速度；
- 椭圆方程使用纯空间 Green 核，不施加时间 mask；
- 当物理偏置趋于常数时，模型退化为普通 Transformer。

## Query Conditioning And Decoder

query 坐标先经 MLP 得到 query embedding，再对 context 做 cross-attention。SIREN 以坐标为输入，并由 context 通过 FiLM 生成逐层 scale/shift，以恢复连续高频场。

## Composite Loss

$$
\mathcal L=\sum_{k\in\{data,PDE,BC,IC\}}\frac{1}{2\sigma_k^2}\mathcal L_k+\log\sigma_k.
$$

$\sigma_k$ 是联合优化的可学习不确定度，自动调节数据、PDE、边界和初值项。架构物理偏置与 residual loss 是互补关系。

## Assumptions

- 需要已知或可近似的传播核；
- Green 函数与边界、非线性和变系数问题之间可能存在偏差；
- attention 计算与隐式解码器带来较高 FLOPs；
- 物理偏置不替代 PDE residual 和边界条件。

## Structural-Dynamics Migration Inference

可基于脉冲响应、模态 Green 函数或图传播核构造 $\Gamma$，但非线性滞回系统的核随状态变化，不能直接使用固定线性核。可考虑状态条件化偏置与 MechConv 拓扑 mask。

## Related Pages

- [[zeraatkar2026-pgt-analysis]]
- [[zeraatkar2026-pgt-results]]
- [[zeraatkar2026-pgt-critical]]
- [[pgt]]

## Evidence By Source

### `sources/papers/zeraatkar2026-pgt.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2603.27929v1.pdf`

^[sources/papers/zeraatkar2026-pgt.md]
