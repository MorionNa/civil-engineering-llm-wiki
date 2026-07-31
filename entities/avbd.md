---
id: entities--avbd
title: AVBD
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- entity/model
keywords:
- augmented-lagrangian
- contact-mechanics
- domain/computational-mechanics
- entity/model
- physics-simulation
- rigid-body-dynamics
sources:
- raw/papers/giles2025-avbd.md
created: '2026-06-13'
updated: '2026-07-31'
confidence: medium
---

# AVBD (Augmented Vertex Block Descent)

AVBD 将 **Augmented Lagrangian** 方法引入 Vertex Block Descent (VBD) 框架，实现对硬约束和高刚度比的稳定支持，同时保持极少的迭代次数即可收敛，推动基于位置的动力学模拟在刚体接触场景中的应用边界。

## 关键信息
- **类型**: algorithm
- **提出**: Giles et al., 2025
- **发表**: SIGGRAPH 2025
- **核心贡献**: Augmented Lagrangian 扩展 VBD，支持硬约束 + 高刚度比，少迭代收敛

## 关联页面
- [[giles2025-avbd-analysis]] — 论文完整分析

## Evidence By Source

### `raw/papers/giles2025-avbd.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/giles2025-avbd.md]

## Related Indexes

- [[entities/index]]
