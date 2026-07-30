---
title: "ExSGD 贡献与批判"
created: 2026-07-30
updated: 2026-07-30
type: paper-analysis
---

# Critical Analysis

## Contribution

- 历史梯度增强优化；
- 面向大 batch 分布式训练的层级学习率策略；
- 建筑遥感提取任务验证。

## Negative Knowledge

- 主要验证对象是遥感建筑提取，不代表所有深度学习任务；
- 分布式硬件环境要求较高；
- 参数分布假设需要进一步验证。

## Transfer to PINN

潜在迁移：

- 保存 PINN 历史梯度轨迹；
- 利用优化历史判断训练阶段；
- 自动调节不同物理约束项更新强度。

## Research Opportunity

可与 PINN 自动优化框架结合：

```
Adaptive sampling
        +
Adaptive loss weighting
        +
Gradient-history optimizer
        +
Second-order refinement
```

形成自动化物理神经求解器。