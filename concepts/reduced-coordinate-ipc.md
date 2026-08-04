---
id: concept--reduced-coordinate-ipc
title: 约化坐标 IPC
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
keywords:
- reduced-coordinates
- barrier-contact
- projected-hessian
sources:
- sources/papers/du2024-embedded-ipc.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# 约化坐标 IPC

把全空间 IPC 能量复合到映射 $x=Jq$ 上，在约化坐标中以 $J^T\nabla_xE$ 和 $J^T\nabla_x^2EJ$ 求解，同时用全空间 CCD 限制步长。^[sources/papers/du2024-embedded-ipc.md]

全空间 IPC 与单仿射体可视为不同子空间选择的特例。

## 关联页面
- [[du2024-embedded-ipc-method]]
- [[concepts/coarse-elasticity-fine-contact-embedding]]
- [[entities/embedded-ipc]]
- [[entities/incremental-potential-contact]]
