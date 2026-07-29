---
title: "Dolean et al. (2024) — Multilevel FBPINN 方法机制"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [physics-informed, pinn, domain-decomposition, fbpinn, multilevel-fbpinn, pde]
sources: [raw/papers/dolean2024-multilevel-fbpinn.xml]
methods: [domain-decomposition, overlapping-domain-decomposition, multilevel-fbpinn, hard-constraint-strategies]
confidence: high
---

# Multilevel FBPINN 方法机制

> 返回 [[dolean2024-multilevel-fbpinn-analysis]] · 基础 [[moseley2023-fbpinn-method]] · 实体 [[fbpinn]]

## 1. 单层函数空间

单层 FBPINN 定义 `V=Σ_j ω_j V_j`，窗函数满足 `Σ_jω_j=1`，全局预测为局部网络的紧支撑和。相较 [[xpinn]]，它用重叠窗构造连续性，不依赖显式界面 loss。

## 2. 多层扩展

对 `l=1…L` 定义不同尺度的子域集合，各层输出共同相加。实验采用

$$J^{(l)}=2^{d(l-1)},$$

使少量层覆盖指数增长的子域和频率尺度。粗层具有大支撑，细层具有小支撑。（PDF p. 10, Figure 4）

## 3. 频率分工

附录层贡献显示，最细层大致学习最高频，粗层学习低频成分。这种分工来自局部归一化和神经网络谱偏置的共同作用，而非显式频带约束。

## 4. 训练协议

| 项目 | 设置 |
|---|---|
| 网络 | 各子域相同 FCN，tanh |
| 约束 | 统一硬边界算子 |
| 优化器 | Adam |
| 学习率 | FBPINN/PINN `1e-3`；Fourier-PINN `1e-4` |
| 重复 | 10 个随机种子 |
| 硬件 | 单 NVIDIA RTX 3090 |
| 指标 | normalized L1 test loss |

## 5. 稀疏计算

朴素计算所有 `J` 个子网成本为 `O(NJ S_tilde)`。预先建立“每个配点属于哪些子域”的映射后，只计算平均覆盖数 `C` 个局部网络，成本变为 `O(N C S_tilde)`。JAX `vmap` 用于并行执行小子网。（PDF pp. 5, 17）

## 6. 强/弱缩放定义

- 强缩放：固定问题复杂度，增加层数/容量，观察精度和成本。
- 弱缩放：问题频率、配点、子域和层数同步增长，观察精度是否保持。

这些定义与经典 DDM 类比，但不直接测多 GPU speedup。

## 7. 方法边界

规则指数层级假设解的频率结构较均匀；复杂几何需异步训练、不规则窗和不同局部容量；最高波数 Helmholtz 暴露了边界条件主导的优化困难。

> 页面导航：[[dolean2024-multilevel-fbpinn-analysis]] · [[dolean2024-multilevel-fbpinn-results]] · [[dolean2024-multilevel-fbpinn-critical]] · [[pinn]]