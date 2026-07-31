---
id: papers--zeraatkar2026-pgt-critical
title: Physics-Guided Transformer 批判分析
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/graph-neural-network
- method/pinn
- method/transformer
keywords:
- domain/ai4s
- evidence/paper
- method/graph-neural-network
- method/pinn
- method/transformer
sources:
- sources/papers/zeraatkar2026-pgt.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# Physics-Guided Transformer 批判分析

## Contribution

PGT 将 PDE Green 函数作为 additive attention bias，使物理传播规律进入 token 交互；并结合 query cross-attention、FiLM-SIREN 与 uncertainty-weighted residual objective 实现稀疏连续场重构。

## Core Knowledge

- 物理先验可以进入信息传播，而不仅是 loss；
- additive log-kernel bias 与 softmax 自然结合；
- 架构物理与 residual 物理具有互补性；
- query-conditioned implicit decoder 适合连续坐标重构。

## Negative Knowledge

- Green 函数通常只对线性、理想边界或简化算子有闭式表达；
- 固定核可能与非线性、变系数和状态依赖传播不匹配；
- PGT 成本显著高于简单 PINN/SIREN；
- 现有实验规模和方程类型有限；
- 不确定度权重并不保证每项物理约束被充分满足。

## Do-Not-Copy Cautions

1. 不要把任意距离 bias 命名为 Green-function physics；
2. 不要在非因果/椭圆问题中机械使用时间 mask；
3. 不要忽略边界条件对真实 Green 核的改变；
4. 不要仅比较误差而隐去 60–100 倍 FLOPs 差异；
5. 不要用线性热核处理滞回结构并声称物理一致。

## Transferable Knowledge

| PGT 组件 | 结构动力迁移 |
|---|---|
| propagation bias | 模态/脉冲响应/拓扑可达性偏置 |
| causal mask | 时程响应有限传播与历史依赖 |
| query cross-attention | 任意节点、构件、时刻查询 |
| FiLM SIREN | 条件化连续响应场解码 |
| uncertainty weighting | 数据、平衡、本构、能量多损失自适应 |

## Research Opportunities

- 状态条件化 Green bias 处理刚度退化和频率漂移；
- 图 Green 函数与 MechConv 矩阵边权结合；
- 低秩/局部 attention 降低大结构复杂度；
- 线性物理核 + 非线性 correction 的可解释分解；
- 统一比较 PGT、普通 Transformer、图算子和 PINN。

## Paper Claims Vs Migration Inference

论文支持热扩散和二维 Navier–Stokes 稀疏重构。结构滞回、模态核、图拓扑和大自由度推理属于迁移推论。

## Related Pages

- [[zeraatkar2026-pgt-analysis]]
- [[zeraatkar2026-pgt-method]]
- [[zeraatkar2026-pgt-results]]
- [[pgt]]

## Evidence By Source

### `sources/papers/zeraatkar2026-pgt.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2603.27929v1.pdf`

^[sources/papers/zeraatkar2026-pgt.md]
