---
id: papers--li2026-exsgd-method
title: ExSGD 方法机制
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
sources:
- sources/papers/li2026-exsgd.md
created: '2026-07-30'
updated: '2026-07-31'
confidence: medium
---

# Method & Mechanism

ExSGD 框架由两个部分组成：

## 1. Historical Gradient Strengthening

在分布式训练中，每个计算节点产生局部梯度。ExSGD 保存过去多个 epoch 的梯度，形成梯度序列：

- 当前梯度
- 历史梯度
- 时间衰减权重

通过融合历史信息增强当前更新方向。

## 2. Adaptive Layer-wise Learning Rate

ExSGD 根据每层参数分布估计更新尺度，计算 trust ratio，并为不同网络层分配不同学习率。

## 3. Optimization Workflow

```
Distributed batches
        ↓
Local gradients
        ↓
Historical gradient sequence
        ↓
Gradient strengthening
        ↓
Layer-wise adaptive update
        ↓
Network parameter update
```

该设计针对大 batch SGD 中梯度平均造成的信息损失问题。

## Evidence By Source

### `sources/papers/li2026-exsgd.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/li2026-exsgd-source.md`

^[sources/papers/li2026-exsgd.md]

## Related Indexes

- [[papers/index]]
- [[index]]
