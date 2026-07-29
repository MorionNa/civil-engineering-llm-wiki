---
title: "Moseley et al. (2023) — FBPINN 方法机制"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [physics-informed, pinn, domain-decomposition, overlapping-domain-decomposition, fbpinn, pde]
sources: [raw/papers/moseley2023-fbpinn.pdf]
methods: [domain-decomposition, overlapping-domain-decomposition, hard-constraint-strategies, collocation-strategy]
confidence: high
---

# FBPINN 方法机制

> 返回 [[moseley2023-fbpinn-analysis]] · 实体 [[fbpinn]] · 对照 [[hu2022-xpinn-generalization-method]]

## 1. 全局表示

将 `Ω` 划分为 `n` 个重叠子域 `Ω_i`。每个子域放置网络 `NN_i`，并定义

$$
\hat u(x;\theta)=C\left[\sum_{i=1}^{n} w_i(x)\,\mathrm{unnorm}(NN_i(\mathrm{norm}_i(x)))\right].
$$

`norm_i` 将该子域坐标归一化到 `[-1,1]`，`w_i` 为可微窗函数，`C` 可将边界/初值作为硬约束写入 ansatz。（PDF pp. 8–9, Equations 12–15）

## 2. 窗函数与连续拼接

对规则超矩形域，窗函数由左右 sigmoid 乘积构造。它在子域外近零、中心接近有效支撑；重叠区由多个局部网络加和，因此不另加 XPINN 式界面连续损失。

## 3. 局部归一化为何重要

全域频率随域尺度增长；局部归一化将每个子问题重新映射到标准尺度，使相同局部网络看到更低的有效频率。论文把这视为缓解谱偏置的核心，而非仅靠子网络变小。

## 4. 训练状态机

| 状态 | 是否更新 | 是否向邻域贡献 |
|---|---:|---:|
| active | 是 | 是 |
| fixed | 否 | 是 |
| inactive | 否 | 否 |

all-active 同时训练全部子网；learning-outwards 从边界附近开始，逐步激活外侧网络并冻结已学区域。（PDF p. 8, Figure 3）

## 5. 并行训练步骤

1. 各活动/固定子域独立采样、归一化、前向与求导。
2. 仅在重叠区域交换邻域输出并求和。
3. 对活动子域施加硬约束、计算 PDE loss、反传和更新。

除第 2 步外各子域可独立执行；理论并行性来自局部邻域通信。（PDF p. 9, Figure 4）

## 6. 复杂度与实现含义

总参数可随子域数增长，但每个配点只与有限邻域子网交互。实际性能取决于是否真正并行；论文单线程实现逐网更新，因此未兑现理论并行优势。

## 7. 方法边界

划分必须覆盖域且有重叠；窗可微；局部网络容量、点密度和调度需与解结构匹配。二阶问题表明，即便 PDE residual 可优化，错误积分常数/特解仍可能远离边界积累。

> 页面导航：[[moseley2023-fbpinn-analysis]] · [[moseley2023-fbpinn-results]] · [[moseley2023-fbpinn-critical]] · [[pinn]]