---
title: "FBPINN — Finite Basis Physics-Informed Neural Network"
created: 2026-07-28
updated: 2026-07-28
type: entity
tags: [physics-informed, pinn, domain-decomposition, overlapping-domain-decomposition, fbpinn, multilevel-fbpinn, pde]
sources: [raw/papers/moseley2023-fbpinn.pdf, raw/papers/dolean2024-multilevel-fbpinn.xml]
confidence: high
---

# FBPINN

## 定义

FBPINN（Finite Basis Physics-Informed Neural Network）把 PDE 域分成重叠子域，在每个子域放置独立神经网络，用光滑窗函数加权求和形成连续全局解，并以局部坐标归一化缓解大域/高频问题中的谱偏置。

## 核心表示

$$\hat u=C\left[\sum_i w_i\,\mathrm{unnorm}(NN_i(\mathrm{norm}_i(x)))\right].$$

`w_i` 限制局部支撑，`norm_i` 把坐标映射到标准域，`C` 可硬编码边界/初值。与 [[xpinn]] 不同，FBPINN 使用重叠窗求和，不必额外加入界面连续 loss。

## 关键机制

- 重叠域分解：把一个全域非凸问题变成耦合局部问题。
- 子域归一化：降低每个网络看到的有效频率。
- 训练调度：active/fixed/inactive，可从边界或初值向外传播。
- 邻域通信：仅在重叠区交换输出。
- 多层扩展：粗层负责长程低频，细层负责局部高频。

## 单层与多层

| 维度 | FBPINN | Multilevel FBPINN |
|---|---|---|
| 层级 | 单尺度子域 | 多个指数尺度 |
| 全局通信 | 邻域重叠 | 粗层 + 邻域 |
| 代表论文 | [[moseley2023-fbpinn-analysis]] | [[dolean2024-multilevel-fbpinn-analysis]] |
| 主要风险 | 调度/划分依赖 | 层数—局部点密度耦合 |

## 适用场景

高频、多尺度、大域 PDE；需要连续拼接且局部网络可并行的神经场；可与 [[schwarz-preconditioned-pinn]] 组合为物理域 + 参数域双重分解。

## 局限

高维采样量未降低；复杂几何和不规则窗未充分验证；单线程实现可能更慢；真正多 GPU efficiency 尚未证明。

## 关联页面

- [[moseley2023-fbpinn-method]] / [[moseley2023-fbpinn-results]] / [[moseley2023-fbpinn-critical]]
- [[dolean2024-multilevel-fbpinn-method]] / [[dolean2024-multilevel-fbpinn-results]] / [[dolean2024-multilevel-fbpinn-critical]]
- [[pinn]] · [[xpinn]] · [[schwarz-preconditioned-pinn]]