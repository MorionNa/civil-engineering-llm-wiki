---
id: papers--lahoti2026-mamba3-critical
title: Mamba-3 批判与研究机会
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/graph-neural-network
- method/pinn
sources:
- sources/papers/lahoti2026-mamba3.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# Mamba-3 批判与研究机会

## 贡献

- 将 SSM 离散化从经验形式提升为系统推导；
- 通过复值状态增强状态跟踪；
- 通过 MIMO 提升硬件利用率。

## Negative Knowledge

- 论文仍主要针对语言模型；
- 不证明 SSM 可以直接替代物理动力学求解器；
- MIMO 增加训练成本；
- 固定状态容量限制复杂长期检索。

## 面向结构动力 PINN 的机会

值得探索：

1. MechConv + Mamba 时间算子；
2. 将 SSM 状态与模态响应关联；
3. 用 MIMO 同时预测位移、速度、加速度和恢复力；
4. 将物理残差约束加入状态更新。

## Evidence By Source

### `sources/papers/lahoti2026-mamba3.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/lahoti2026-mamba3-source.md`

^[sources/papers/lahoti2026-mamba3.md]

## Related Indexes

- [[papers/index]]
- [[index]]
