---
id: concept--dynamic-slicing
title: Dynamic Slicing — 特征空间中的输入相关软聚合
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/webpage
- method/neural-operator
- method/transformer
keywords:
- dynamic-clustering
- dynamic-slicing
- feature-space-aggregation
- soft-assignment
- tokenization
sources:
- sources/articles/shenlan2026-physical-token-transolver.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: medium
evidence_scope: webpage
---

# Dynamic Slicing

## Definition

Dynamic Slicing 是 [[entities/transolver]] 中用于从大量节点特征形成少量 Slice Token 的输入相关软聚合机制。它依据 Encoder 输出的特征表示分配节点权重，而不是依据固定空间坐标把网格硬切成若干块。 ^[sources/articles/shenlan2026-physical-token-transolver.md]

## Mechanism

```text
原始节点输入
  → Encoder 将几何、边界和物理量编码为节点特征
  → 为每个节点计算其对多个 Slice 的贡献权重
  → 对节点特征进行加权聚合
  → 得到少量 Slice Token
```

文章明确指出，一个节点可以同时参与多个 Slice；同一 Slice 也由许多节点共同构成。因此它更接近连续的软聚合，而不是唯一类别的硬分组。 ^[sources/articles/shenlan2026-physical-token-transolver.md]

## Spatial Interpretation

- 空间上距离很远的节点，如果编码后特征相似，可能对同一 Slice 贡献较大；
- 空间上相邻的节点，如果状态、边界或物理参数不同，也可能被分配到不同 Slice；
- Slice 的可视化区域可能随输入和训练变化，但 Slice 本身代表的是特征组合，不是固定区域。

## Why “Dynamic” Matters

固定分区在几何、网格或边界条件变化后可能失去适应性。Dynamic Slicing 让 Token 化过程依赖当前输入，使同一个模型有机会对不同流场、结构状态或网格形成不同的紧凑表示。

## Failure Modes — Migration Inference

以下是根据软聚合机制推导的风险，不是来源文章报告的实验结果：

- **Slice collapse：** 多个 Slice 学到近似相同表示，实际有效 Token 数减少。
- **过度压缩：** Token 太少导致边界层、局部塑性、冲击或高频信息丢失。
- **分配不稳定：** 小输入扰动引起 Slice 权重大幅改变，影响预测连续性。
- **尺度偏置：** 大范围平滑区域主导聚合，稀少但关键的局部异常被淹没。
- **跨网格失配：** 编码特征若依赖训练网格统计，换网格后软分配可能失效。

## Evaluation Suggestions

- 可视化节点到 Slice 的权重而不只显示最终类别；
- 比较固定空间分区、硬聚类和 Dynamic Slicing；
- 对 Token 数、温度/归一化方式和局部异常进行消融；
- 检查从 Slice 广播回节点后的 PDE 残差和局部误差；
- 对高频响应、损伤集中与边界条件变化单独测试。

## Related Pages

- [[concepts/physical-token]]
- [[concepts/physics-attention]]
- [[entities/transolver]]
- [[concepts/neural-operator]]
