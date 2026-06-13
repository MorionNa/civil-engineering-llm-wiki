---
title: "AVBD"
created: 2026-06-13
updated: 2026-06-13
type: entity
tags: [physics-simulation, rigid-body-dynamics, augmented-lagrangian, contact-mechanics]
sources: [raw/papers/giles2025-avbd.md]
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
