---
id: concept--physics-attention
title: Physics Attention — Slice Token 间的全局物理信息交换
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/webpage
- method/neural-operator
- method/transformer
keywords:
- global-interaction
- physics-attention
- slice-token
- token-broadcast
- transolver
sources:
- sources/articles/shenlan2026-physical-token-transolver.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: medium
evidence_scope: webpage
---

# Physics Attention

## Definition

Physics Attention 是 [[entities/transolver]] 中在少量 Slice Token 之间进行全局信息交换、再把结果反馈到节点的注意力机制。它与 [[concepts/dynamic-slicing]] 配合：Dynamic Slicing 决定哪些紧凑表示成为 [[concepts/physical-token]]，Physics Attention 决定这些 Token 如何相互作用。 ^[sources/articles/shenlan2026-physical-token-transolver.md]

## Information Path

```text
N 个节点特征
    → Dynamic Slicing
M 个 Slice Token，M 远小于 N
    → Token 间全局 Attention
更新后的 M 个 Token
    → 按节点-Slice 关系广播
N 个节点的全局增强特征
```

文章的核心解释是，把原来需要在大量节点之间建立的全局联系，转换为少量 Token 之间的信息交互，从而同时保留全局感受野并降低计算复杂度。 ^[sources/articles/shenlan2026-physical-token-transolver.md]

## Complexity Interpretation

在概念层面，若节点数为 $N$、Slice Token 数为 $M$ 且 $M\ll N$，节点级全注意力的核心关系规模约为 $N^2$，而 Token 化路径通常由节点-Slice 映射和 Token 间 Attention 组成，可理解为约 $NM+M^2$ 的关系规模。这个表达是对文章机制的复杂度推论，不是来源给出的完整实现 FLOP 或显存公式。

## Difference from Other Attention Uses

- **与标准节点 Attention 不同：** 不直接让每个节点查看所有其他节点。
- **与固定 Patch Attention 不同：** Token 由特征空间软聚合形成，而非固定分块。
- **与物理偏置 Attention 不同：** [[entities/pgt]] 侧重把 Green 函数等物理关系写入 Attention；Physics Attention 在当前来源中更强调先压缩为物理 Token，再进行全局交互。
- **与局部 GNN 不同：** GNN 通过多层边传播扩大感受野，Physics Attention 在 Token 空间中直接建立全局联系。

## Failure Modes — Migration Inference

- Dynamic Slicing 若遗漏关键节点，Attention 无法恢复已丢失的信息；
- Token 间全局混合可能削弱局部守恒、相位和高频细节；
- 广播回节点的权重若过平滑，可能产生空间模糊；
- 计算节省取决于 $M$ 足够小，但 $M$ 太小又会形成表示瓶颈；
- 全局交互并不自动满足控制方程，需要额外物理约束或结构化传播。

## Structural-Dynamics Migration Inference

在大规模结构图中，可让局部 MechConv 先处理质量、刚度、阻尼和构件连接，再用 Physics Attention 在状态相关结构 Token 之间交换跨楼层、跨子结构信息。评价时应分别检查低频整体模态、高频局部响应、非线性本构状态和运动方程残差，避免把全局信息交换误当作物理一致性的替代品。

## Related Pages

- [[concepts/dynamic-slicing]]
- [[concepts/physical-token]]
- [[entities/transolver]]
- [[entities/pgt]]
- [[entities/seisgpt]]
