---
id: papers--li2026-exsgd-critical
title: ExSGD 贡献与批判
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
sources:
- sources/papers/li2026-exsgd.md
created: '2026-07-30'
updated: '2026-07-31'
confidence: medium
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

## Evidence By Source

### `sources/papers/li2026-exsgd.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/li2026-exsgd-source.md`

^[sources/papers/li2026-exsgd.md]

## Related Indexes

- [[papers/index]]
- [[index]]
