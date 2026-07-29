---
title: "Kopaničáková et al. (2024) — SPQN 贡献、负知识与机会"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [physics-informed, pinn, schwarz-method, nonlinear-preconditioning, quasi-newton, model-parallelism, limitation, future-work, comparison]
sources: [raw/papers/kopanicakova2024-dd-preconditioning.pdf]
failure_modes: [architecture-mismatch-failure]
confidence: high
---

# SPQN 批判性分析

> 返回 [[kopanicakova2024-dd-preconditioning-analysis]] · 结果 [[kopanicakova2024-dd-preconditioning-results]] · 实体 [[schwarz-preconditioned-pinn]]

## 1. 主要贡献

- 将层级参数分解解释为非线性 Schwarz 预条件。
- 同时给出加法并行和乘法串行版本。
- 把 time-to-common-error、梯度评估与 update cost 纳入优化器比较。
- 指出参数域分解可与输入域分解组合。

## 2. Negative Knowledge

| 风险 | 说明 | 影响 |
|---|---|---|
| 硬件混杂 | ASPQN 用 6–8 GPU | 28× 非等资源 speedup |
| 全网复制 | 每 GPU 完整前向/参数 | 大模型显存瓶颈 |
| 固定层分组 | 未根据曲率自适应 | 分块可能不匹配耦合 |
| 无重叠/粗层 | 深层长程耦合弱 | 可扩展迭代数未知 |
| 确定性环境 | 无 mini-batch 噪声 | 深度学习任务外推有限 |
| 代码状态 | 预印本仅称将公开 | 当前复现需再核查 |

## 3. 资源公平性

建议未来同时报告 wall-clock、GPU-hours、峰值显存、能耗和通信量。ASPQN 适合“尽快得到解”，MSPQN 适合“同资源更高效”，两者不能只用一个 speedup 数字概括。

## 4. 可迁移方向

- 与 [[fbpinn]] 嵌套：空间局部化 + 参数条件性。
- DeepONet/Transformer：按模块而非逐层分组。
- 自适应分组：用近似 Fisher/Hessian 块耦合图聚类。
- 粗参数空间：训练低秩全局校正器连接远隔层组。

## 5. 研究机会

### O1 双域分解 PINN

子域 GPU 组训练局部网络，组内按层作 MSPQN，组间粗层同步；需验证嵌套循环是否超过收益。

### O2 曲率驱动分组

周期估计块间梯度协方差，动态合并强耦合层；风险是估计噪声和重分组开销。

### O3 无复制 ASPQN

把局部 loss 的全网前向拆成激活缓存/流水线，使 GPU 只保存负责参数和必要激活，再评估显存—通信折中。

> 页面导航：[[kopanicakova2024-dd-preconditioning-analysis]] · [[kopanicakova2024-dd-preconditioning-method]] · [[kopanicakova2024-dd-preconditioning-results]] · [[dolean2024-multilevel-fbpinn-critical]]