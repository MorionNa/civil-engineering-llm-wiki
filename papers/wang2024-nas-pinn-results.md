---
id: papers--wang2024-nas-pinn-results
title: Wang & Zhong (2024) — NAS-PINN results
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/neural-architecture-search
- method/pinn
keywords:
- advection-equation
- burgers-equation
- neural-architecture-search
- pinn
- poisson-equation
sources:
- sources/papers/wang2024-nas-pinn.md
created: '2026-07-30'
updated: '2026-07-31'
confidence: high
---

# Results

## Benchmarks

论文测试：Poisson、Burgers、Advection 方程以及非规则计算域。

## Main findings

- NAS-PINN 找到搜索空间内误差最低结构；
- 网络深度增加不一定提高 PINN 性能；
- 不同 PDE 偏好的架构不同。

Poisson实验中，NAS-PINN 架构 L2 error 为 4.46×10⁻⁴，优于比较架构。

复杂非规则区域中，作者发现残差连接更有利，且深层网络并非总是最佳。

## Conclusions

论文总结指出：不同 PDE 需要不同网络结构，人工设计难以覆盖这种多样性。

## Evidence By Source

### `sources/papers/wang2024-nas-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/wang2024-nas-pinn-source.md`

^[sources/papers/wang2024-nas-pinn.md]

## Related Indexes

- [[papers/index]]
- [[index]]
