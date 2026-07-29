---
title: "Kopaničáková et al. (2024) — SPQN 优化实验结果"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [physics-informed, pinn, schwarz-method, nonlinear-preconditioning, quasi-newton, model-parallelism, gpu-computing]
sources: [raw/papers/kopanicakova2024-dd-preconditioning.pdf]
results: [distributed-training, gpu-computing]
datasets: [synthetic-data]
confidence: high
---

# SPQN 优化实验结果

> 返回 [[kopanicakova2024-dd-preconditioning-analysis]] · 方法 [[kopanicakova2024-dd-preconditioning-method]] · 实体 [[schwarz-preconditioned-pinn]]

## 1. 基准与协议

Burgers、Klein–Gordon、advection–diffusion、Allen–Cahn；每题 10,000 配点，网络深宽由 L-BFGS 搜索；10 次独立运行。基线 Adam/L-BFGS，方法 ASPQN/MSPQN。

## 2. 局部步数与子域数

Figures 3–6 扫描 `k_s∈{10,50,100}` 和多种 `N_sd`。较大的 `k_s` 通常降低最终误差，但增加局部工作；子域数更多并不单调更好，梯度评估与 update cost 的排序可能不同。

## 3. Time-to-solution

共同阈值定义为 L-BFGS 可达到的最低平均 `E_rel`。

| 问题 | 阈值 `E_rel` | L-BFGS (min) | ASPQN (min/GPU) | MSPQN (min) |
|---|---:|---:|---:|---:|
| Burgers | 4.6e-4 | 558.5 | 14.4 / 8 | 40.7 |
| Klein–Gordon | 6.1e-4 | 236.5 | 6.8 / 6 | 26.9 |
| Allen–Cahn | 6.0e-4 | 1001.6 | 79.2 / 6 | 117.5 |

Adam 未达到这些阈值，因此无 time-to-solution；advection–diffusion 中 L-BFGS 停滞，未进入该表。（PDF p. 19, Table 3）

## 4. 平均加速的正确读法

作者汇总 MSPQN 约 10×、ASPQN 约 28×。MSPQN 是单 GPU 对单 GPU；ASPQN 用 6–8 GPU，因此 28× 不是等资源算法 speedup。若按 GPU-minutes 粗算，ASPQN 的资源优势会显著缩小，但仍可能通过并行缩短等待时间。

## 5. 最终误差

Figure 7 显示 SPQN 通常比 Adam/L-BFGS 更早进入低误差区，并能达到更低 `E_rel`。这支持“预条件改善优化可转化为 PDE 解精度”，但不证明改变了网络逼近上限。

## 6. 复现与公平性边界

- ASPQN 每 GPU 复制完整网络。
- 架构超参用 L-BFGS 搜索。
- 论文预印本称代码接收后公开；本次未独立运行。
- 全批量合成配点环境不代表 noisy mini-batch。

## 7. 有界结论

四类 PDE 支持非线性 Schwarz 预条件显著降低训练时间；纯算法效率优先看 MSPQN，端到端并行等待时间可看 ASPQN，但须附 GPU 数与 GPU-hours。

> 页面导航：[[kopanicakova2024-dd-preconditioning-analysis]] · [[kopanicakova2024-dd-preconditioning-method]] · [[kopanicakova2024-dd-preconditioning-critical]] · [[pinn]]