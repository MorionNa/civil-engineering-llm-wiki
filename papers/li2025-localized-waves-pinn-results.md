---
title: "Li & Wang (2025) — 局域波实验：数值结果与证据"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [neural-network, physics-informed, deep-learning, nonlinear-systems, synthetic-data, pinn, ai4s, physics-simulation]
sources: [raw/papers/10_1007_s11071-024-10359-7.pdf]
methods: [backlund-transformation, multi-output-pinn, lbfgs, latin-hypercube-sampling]
results: [one-soliton, signed-sech-wave, flat-top-wave, stair-wave, gaussian-wave-evolution, residual-verification]
failure_modes: [no-v-reference-solution, multi-wave-cost-growth, waveform-terminology-ambiguity, incomplete-gaussian-metrics]
datasets: [modified-kdv-one-soliton, modified-kdv-two-soliton, gaussian-initial-wave]
reproducibility: low
code_url: []
dataset_url: []
confidence: high
---

# Li & Wang (2025) — 结果与证据

> 返回总览：[[li2025-localized-waves-pinn-analysis]]；方法解释：[[li2025-localized-waves-pinn-method]]

## 6.1 统一实验设置

论文对已知 mKdV 解 $u$ 计算相对误差

$$RE_u=\frac{\|\hat u-u\|_2}{\|u\|_2}.$$

单波数据网格为 $N_x\times N_t=513\times201$，区域 $x\in[-12,4]$、$t\in[0,3]$；训练用 $N_u=200$ 个初边界点和 $N_f=10{,}000$ 个内部配点。误差、耗时和迭代数均为五次实验平均值。

## 6.2 单波：$k=1$

| 指标 | 数值 |
|------|------|
| $RE_u$ | $5.190663\times10^{-4}$ |
| 平均迭代 | 630 |
| 平均训练时间 | 38.1618 s |
| 最终 $MSE_G$ | $1.798\times10^{-6}$ |
| 最终 $MSE_{BT}$ | $3.707\times10^{-7}$ |

$\hat u$ 与解析单孤子在 $t=0.6,1.5,2.4$ 的剖面基本重合，主要误差集中在脉冲附近。网络同时生成的 $v$ 为较宽、底部近似平坦的负值局域结构；作者将其描述为类似 antikink–kink 碰撞，但两部分保持固定间距传播。

**证据强度：** $u$ 有解析基准；$v$ 只有 $G$ 残差、BT 残差与图形证据，不能把它等同于独立验证。

## 6.3 符号翻转：$k=-1$

| 指标 | 数值 |
|------|------|
| $RE_u$ | $7.744260\times10^{-4}$ |
| 平均迭代 | 772 |
| 平均训练时间 | 29.2134 s |

由于两条 PDE 分别关于 $u,v$ 呈奇对称，论文把该组结果解释为前一组的镜像。生成的 $v$ 是正值、近似 flat-top 的结构，可描述为左 kink 与右 antikink 的组合。

**术语核对：** 论文把 $k=-1$ 的 $u$ 称为 cuspon，但给定公式 $2k\operatorname{sech}(kx+k^3t)$ 对 $k=-1$ 仍是光滑负脉冲。图中也没有明确展示导数奇异点，因此知识库保留作者用语，同时把它标记为待核实，而不把“尖峰”当作已证事实。

## 6.4 双波案例

| 指标 | 数值 |
|------|------|
| 评估网格 | $513\times401$ |
| $N_u$ | 200 |
| $RE_u$ | $3.123852\times10^{-3}$ |
| 平均迭代 | 约 16,166 |
| 平均训练时间 | 1,949.1901 s |

$\hat u$ 跟随双波传播，生成的 $v$ 呈阶梯状；作者将其解释为两个同向 antikink 的叠加。相较 $k=1$ 单波，误差约增至 6 倍，迭代数约增至 26 倍，训练时间约增至 51 倍，说明多波相互作用显著加重优化负担。

上述倍数由论文表内平均值计算，是复杂度趋势而非硬件无关的算法标度；硬件未披露，绝对时间不能横向比较。

## 6.5 高斯初波

$$u_0(x)=e^{-x^2/20},\qquad u_1(t)=u_2(t)=0,\qquad x\in[-20,20].$$

网络仍为 4×100，最终 $MSE_G=8.803\times10^{-6}$、$MSE_F=8.965\times10^{-6}$。图 11 中两输出呈作者所称的 soliton 与 antisoliton 传播形态。

**证据边界：** 本组没有报告相对 $L_2$ 误差、独立数值解对比、训练时间或 BT 最终残差，因此只能说明联合残差可降到 $10^{-5}$ 量级并产生平滑波形，不能据此量化解的准确性。

## 6.6 结果如何解读

1. 对 $u$：单波和双波均有解析基准，误差证据较强。
2. 对 $v$：没有真值，主要是内部一致性验证；须结合 [[wang2023-pinn-spurious-analysis]] 理解“小残差不保证真解”。
3. 对方法扩展性：双波成本增长是最清晰的负面证据。
4. 对架构选择：可将 [[wang2024-kinn-analysis]] 作为后续骨干替换基线，但本文没有做架构对比。

## 关联页面

- [[backlund-transformation-pinn]] — 变换约束的机制与适用条件
- [[pinn]] — PINN 基础实体
- [[raissi2019-pinn-analysis]] — 非线性 PDE 基线
- [[li2025-localized-waves-pinn-critical]] — 证据缺口与研究机会
