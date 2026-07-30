---
title: "ExSGD 方法机制"
created: 2026-07-30
updated: 2026-07-30
type: paper-analysis
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
