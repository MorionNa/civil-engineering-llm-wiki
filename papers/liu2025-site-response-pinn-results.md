---
title: "Liu et al. (2025) — 场地反应 PINN：结果与定量证据"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [physics-informed, pinn, structural-dynamics, seismic-response, equation-of-motion, ground-motion, synthetic-data, benchmark, neural-tangent-kernel, ai4s, physics-simulation]
sources: [raw/papers/10_1016_j_compgeo_2025_107137.xml, raw/papers/extracted/10_1016_j_compgeo_2025_107137_extracted.txt]
methods: [fourier-feature-embedding, nondimensionalization, adam, rk45, newmark-beta]
results: [displacement-rmse, velocity-rmse, acceleration-rmse, frequency-spectrum-agreement, single-layer, three-layer, ten-layer, wide-intensity-range]
failure_modes: [spectral-bias, sigma-sensitivity, derivative-error-propagation, per-scenario-retraining, no-speed-benchmark]
datasets: [NGA-West2-ground-motion-records, synthetic-layered-soil-profiles]
reproducibility: low
code_url: []
dataset_url: []
confidence: high
---

# Liu et al. (2025) — 结果与定量证据

> 返回总览：[[liu2025-site-response-pinn-analysis]]；训练配置：[[liu2025-site-response-pinn-method]]

## 6.1 谱偏置消融

单层示例中，普通 4 层 MLP 在 5,000 次迭代后仍未恢复高频成分，RMSE 为 0.48。加入 $m=100,\sigma=0.6$ 的 Fourier 特征后，约 50 次迭代已能在 0.1–30 Hz 工程频带内逼近 NB 解，直接支持“频率嵌入是必要组件”。

$m=200$ 只比 $m=100$ 略好但更耗时；$\sigma$ 过小会过度平滑，过大则引入振荡。论文据此给出 $m=50$–200、$\sigma=0.1$–2 的搜索范围，并指出对 $\sigma$ 更敏感。

## 6.2 Table 2：单层基准精度

以下误差是 PINN 分别相对 RK45 和 Newmark-beta（NB）的差异：

| 响应量 | RMSE vs RK45 | RMSE vs NB | MAE vs RK45 | MAE vs NB |
|--------|--------------|------------|-------------|-----------|
| 位移 $u$ (cm) | $5.35\times10^{-8}$ | $3.43\times10^{-8}$ | $9.11\times10^{-8}$ | $7.89\times10^{-8}$ |
| 速度 $\dot u$ (cm/s) | $5.79\times10^{-7}$ | $5.26\times10^{-7}$ | $3.32\times10^{-6}$ | $2.34\times10^{-6}$ |
| 加速度 $\ddot u$ (cm/s²) | $3.57\times10^{-6}$ | $3.12\times10^{-6}$ | $2.12\times10^{-5}$ | $9.67\times10^{-6}$ |

误差从位移到速度、加速度递增，符合导数误差传播；绝对量仍被作者判断为工程上可忽略。三个方法的加速度 Fourier 幅值谱在约 0.4–90 Hz 内一致，极低/极高频差异较明显；作者指出多数工程应用关注 0.1–30 Hz。

## 6.3 土体刚度与地震动周期覆盖

九个单层附加工况组合了：

- 剪切模量 $G=5{,}000/50{,}000/200{,}000$ kPa（软到硬）；
- 地震动平均周期 $T_m=0.2/0.5/1.0$ s；
- 输入记录来自 NGA-West2。

这些案例的 RMSE/MAE 分布与主案例一致，说明训练策略可适应不同固有频率与输入频率组合。注意：每个案例都重新训练，所以这是流程稳健性，不是 [[seismic-site-response-pinn]] 对未见参数的直接泛化。

## 6.4 三层与十层系统

| 系统 | 配置摘要 | 结果 |
|------|----------|------|
| 3 层 | 厚度 10/5/5 m；$G=10{,}000/5{,}000/15{,}000$ kPa；阻尼比 0.1/0.1/0.2 | 位移与 PSA 和 RK45/NB 实用上一致 |
| 10 层 | 厚度 2–10 m、$G=5{,}000$–15,000 kPa、不同容重，阻尼比 0.1 | 位移与 PSA 对比一致 |

输出维度随土层数从 1 扩展到 3 和 10，表明欧氏范数多自由度残差可工作；但论文没有进一步测试几十/几百层的宽输出和优化规模。

## 6.5 强度与持时极端范围

三层系统还采用四条对比强烈的输入地震动：

- PGA 从 0.003 g 到 1.8 g；
- 显著持时 $D_{5-95}$ 从 2 s 到 148 s。

地表 PSA 与 RK45/NB 保持一致。由于土层仍为线性，1.8 g 只代表大输入幅值，**不等于验证了大应变土体材料非线性**。

## 6.6 结果证据边界

1. RK45 与 NB 提供两类独立数值基线，但都求解相同的线性集中质量方程；这验证求解器一致性，不验证模型形式本身。
2. “相同结果”建立在调参成功且逐场景重训后，不能外推到无调参的新场地。
3. 未报告训练/推理耗时，无法比较计算效率；研究明确不以提速为目标。
4. [[neural-tangent-kernel]] 解释了谱偏置，但本文没有实际使用 NTK 自适应权重作为主结果。

## 关联页面

- [[liu2025-site-response-pinn-critical]] — 不应外推的结论
- [[seismic-site-response-pinn]] — 方法适用范围
- [[pinn]] — PINN 基础实体
- [[liu2025-site-response-pinn-method]] — Fourier/TPE 训练流程
