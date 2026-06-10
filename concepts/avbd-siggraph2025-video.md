---
title: "AVBD 物理仿真算法 (SIGGRAPH 2025) — B站视频笔记"
created: 2026-06-10
updated: 2026-06-10
type: concept
tags: [physics-simulation, real-time, game-engine, rigid-body, soft-body, cloth, fracture, pbd, vertex-block-descent, siggraph]
sources: [raw/articles/avbd-siggraph2025-bilibili.md]
methods: [avbd, vertex-block-descent, augmented-block-descent, position-based-dynamics]
results: [few-iteration-convergence, large-mass-ratio-stability, parameter-robustness]
datasets: [lego-wall, prism-array, cloth-particle, pendulum-test, brick-wall-fracture]
confidence: medium
---

# AVBD — Augmented Vertex Block Descent (SIGGRAPH 2025)

> **来源：** [B站 BV1QpKNzeEqq](https://www.bilibili.com/video/BV1QpKNzeEqq) | 转录：Kimi ReadMediaFile
> **论文：** Chris Giles, Elie Diaz, Cem Yuksel — Roblox, University of Utah
> **会议：** SIGGRAPH 2025, Vancouver, Aug 10–14

---

## 视频主题

AVBD（增强顶点块下降法）— 一种新型物理模拟求解器，在**极少迭代次数**（5 次）下达到甚至超越传统方法（VBD/XPBD/Sequential Impulse）的模拟质量，每帧仅 3.5–16ms。

## 核心方法

在 VBD 基础上加入增强项（augmentation），通过参数 β/α/γ 控制，以块坐标下降优化方式统一求解碰撞、接触、摩擦、链接约束。默认参数：β=10, α=0.95, γ=0.99, 20 iterations。

## 关键结果

| 测试场景 | AVBD vs 其他方法 |
|----------|-----------------|
| **刚体链** | AVBD 5 iter > VBD 100 iter + 多 substep |
| **旗帜** | AVBD 5 iter ≈ VBD 20 iter |
| **积木塔** | VBD 严重穿透粘连，AVBD 自然倒塌破碎 |
| **钟摆精度** | AVBD 最接近参考解（Seq.Imp 50 iter） |
| **大质量比** | Seq.Imp/XPBD 完全失效；AVBD 稳定 |
| **砖墙破碎** | VBD 像橡胶弹开，Seq.Imp/XPBD 残留大块，**AVBD 最自然** |
| **参数鲁棒性** | 默认参数适用于刚体/布料/破碎/摩擦多场景 |

## 核心知识点

1. **少迭代即收敛**：5 次迭代 ≈ 传统 100 次，3.5-16 ms/frame，实时可用
2. **解决 VBD "过软"问题**：VBD 少迭代时刚体像橡胶弹性变形，AVBD 增强项有效抑制
3. **大质量比碰撞稳定**：传统方法重碰轻时失效，AVBD 正确处理极端质量差异
4. **参数简洁鲁棒**：仅 β/α/γ 三个参数，默认值适用多种场景
5. **工业 + 学术双重验证**：Roblox 游戏公司 + 犹他大学，可直接集成大型实时平台

## 关联

- [[zhang2020-phylstm-analysis]] — 同样使用 physics-informed 方法加速仿真（PhyLSTM 推理 >10³x FEM）
- [[muller2023-pinn-spurious-analysis]] — 同样是物理计算效率优化
- 与 PhyLSTM 的对比：AVBD 是**算法层面**的加速（少迭代），PhyLSTM 是**学习层面**的替代（神经网络替 FEM）
