---
id: entity--transolver
title: Transolver — 基于物理 Token 的 PDE Transformer
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- evidence/webpage
- method/neural-operator
- method/transformer
keywords:
- dynamic-slicing
- pde-surrogate
- physical-token
- physics-attention
- slice-token
- transolver
sources:
- sources/articles/shenlan2026-physical-token-transolver.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: medium
evidence_scope: webpage
---

# Transolver

## Definition

Transolver 是一种面向流体、结构和一般 PDE 系统的 Transformer 类模型。当前知识页依据二次技术文章建立：它的核心不是把每个网格节点直接视为 Token，而是先用 [[concepts/dynamic-slicing]] 将大量节点特征压缩成少量 [[concepts/physical-token]]，再在这些 Token 之间执行 [[concepts/physics-attention]]。 ^[sources/articles/shenlan2026-physical-token-transolver.md]

## Information Flow

```text
几何坐标 + 边界条件 + 节点物理量
                ↓
             Encoder
                ↓
         节点特征表示空间
                ↓
         Dynamic Slicing
                ↓
            Slice Token
                ↓
         Physics Attention
                ↓
        全局信息反馈到节点
                ↓
             输出场
```

该流程把“寻找物理 Token”和“Token 间全局交互”分开：前者完成输入相关的表示压缩，后者完成全局信息传播。 ^[sources/articles/shenlan2026-physical-token-transolver.md]

## Distinguishing Features

- **不是节点级全注意力：** 避免在全部 $N$ 个物理节点之间构建 $N^2$ 关系。
- **不是固定 Patch：** Slice 不需要对应规则空间块或固定几何分区。
- **不是固定降阶基：** 与 POD/DMD 的共同点是寻找紧凑表示，但 Slice 随输入特征动态形成。
- **不是硬聚类：** 一个节点可以同时对多个 Slice 贡献不同权重。
- **全局交互发生在压缩空间：** 少量 Slice Token 先交换信息，再把结果传播回节点。 ^[sources/articles/shenlan2026-physical-token-transolver.md]

## Why It Matters

高分辨率 PDE 网格的节点数在二维随分辨率平方增长，在三维随分辨率立方增长。直接全注意力很快变得不可行，而纯局部消息传递又可能需要很多层才能覆盖远程影响。Transolver 提供了一种中间路线：保留节点级输入输出，同时把全局交互放到更小的学习型 Token 空间中。

## Evidence Boundary

- 当前页面来自 [[notes/articles/shenlan2026-physical-token-transolver]] 的来源解读，不是 Transolver 原始论文的全文分析。
- 尚未在本知识库中核验原始论文的作者、正式公式、具体网络层数、训练数据、benchmark 数字和代码版本。
- `status: active` 表示概念关系已从所列网页证据整理，不表示模型已被独立复现。

## Negative Knowledge

- Token 数量更少不保证局部物理细节一定保留。
- 输入相关 Slice 可能出现表示塌缩、分配不稳定或对边界条件敏感的问题。
- 远程信息能否通过 Token 正确传播，取决于切片质量，而不仅是 Attention 本身。
- 对流体有效的特征聚合不必然适用于结构损伤、接触、断裂或强局部非线性。

## Project Role — Migration Inference

对大规模结构动力模型，Transolver 可作为“局部物理图传播之上的全局通信模块”候选，而不是替代质量、刚度、阻尼和本构关系。一个可检验的组合是：MechConv 处理矩阵边权重与局部子图，Dynamic Slicing 形成状态相关结构 Token，Physics Attention 处理跨子图长程耦合，最后以运动方程残差校核输出。该组合属于设计建议，需要与 [[entities/seisgpt]]、[[entities/pgt]] 和局部图模型进行消融比较。

## Related Pages

- [[concepts/physical-token]]
- [[concepts/dynamic-slicing]]
- [[concepts/physics-attention]]
- [[concepts/neural-operator]]
- [[entities/seisgpt]]
- [[entities/pgt]]
