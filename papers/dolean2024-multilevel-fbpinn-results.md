---
title: "Dolean et al. (2024) — Multilevel FBPINN 缩放实验"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [physics-informed, pinn, domain-decomposition, fbpinn, multilevel-fbpinn, pde, gpu-computing]
sources: [raw/papers/dolean2024-multilevel-fbpinn.xml]
results: [sublinear-scaling, cross-domain-generalization]
datasets: [synthetic-data]
confidence: high
---

# Multilevel FBPINN 缩放实验

> 返回 [[dolean2024-multilevel-fbpinn-analysis]] · 方法 [[dolean2024-multilevel-fbpinn-method]] · 实体 [[fbpinn]]

## 1. 实验协议

规则 2D Laplacian 与 Helmholtz；PINN、Fourier-feature PINN、SA-PINN、单层和多层 FBPINN；统一点集，10 个种子，单 RTX 3090。

## 2. Multiscale Laplacian 强缩放

固定 6 个指数增长频率分量，层数从 2 增至 7，使用 320×320 配点与 350×350 测试点。

| 层数 | 观察 |
|---|---|
| 2–4 | 不能完整恢复全部频率 |
| 5–7 | 能恢复全部频率 |
| 7 vs 6 | 7 层略差；最细域仅约 10×10 配点 |

结论不是“层越多越好”，而是容量和局部采样密度必须同步增长。（PDF p. 12, Figure 6）

## 3. Laplacian 弱缩放

令频率分量数 `n=L-1`，配点与子域随 `L` 指数增长。所有模型能捕捉频率，但 normalized L1 随复杂度略降，因此是 near—but not perfect—weak scaling。（PDF p. 13, Figure 7）

## 4. 基线比较

标准 PINN 只抓住部分周期，训练时间比 7 层 FBPINN 高一个数量级且曲线不稳；Fourier-PINN 精度改善但仍较慢；SA-PINN 未优于标准 PINN；单层 FBPINN 能建模但精度低于多层。

## 5. Helmholtz 弱缩放

`L=2…6`，波数与点数同步增长。多层 FBPINN 除最高波数外均较准确；最高波数只恢复主频和同心结构，未抓住复杂 motifs。PINN/SA-PINN 均失败且训练更慢；Fourier-PINN 精度相近但约慢一个数量级。（PDF pp. 15–16, Figures 9–10）

## 6. 证据边界

- 结果报告种子 min/max，稳健性优于单轨迹实验。
- Fourier feature 的 `σ` 手工逐题选择，基线调参预算不完全对称。
- 没有多 GPU speedup/efficiency 曲线。
- 只有规则二维合成问题。

## 7. 有界结论

多层粗空间在大量细子域时确实改善准确性；但“可扩展”目前是算法/精度层面的经验结论，尚非分布式系统层面的证明。

> 页面导航：[[dolean2024-multilevel-fbpinn-analysis]] · [[dolean2024-multilevel-fbpinn-method]] · [[dolean2024-multilevel-fbpinn-critical]] · [[pinn]]