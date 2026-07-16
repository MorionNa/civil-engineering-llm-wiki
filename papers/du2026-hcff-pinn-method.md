---
title: "Du et al. (2026) — HCFF-PINN 方法机制展开"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [physics-informed, pinn, neural-network, deep-learning, hard-constraint-strategies, auxiliary-function, hard-constraints, structural-dynamics, seismic-response, equation-of-motion, vibration-analysis, sdof, adam-lbfgs, two-phase-optimization, collocation-strategy]
sources: [raw/papers/10_1016_j_engappai_2025_113640.xml, raw/papers/extracted/10_1016_j_engappai_2025_113640_extracted.txt]
methods: [physics-guided-fourier-features, hard-initial-conditions, tanh-squared-modulation, automatic-differentiation, static-condensation, adam-lbfgs-optimization]
results: [spectral-bias-mitigation, single-residual-training, smooth-loss-convergence]
failure_modes: [frequency-prior-mismatch, hard-constraint-function-mismatch, nonzero-initial-condition-unsupported]
datasets: [synthetic-harmonic-loads, northridge-symlar, san-simeon-diablo-canyon]
reproducibility: medium
code_url: []
dataset_url: []
confidence: high
---

# Du et al. (2026) — HCFF-PINN 方法机制展开

> 返回概述 → [[du2026-hcff-pinn-analysis]]；方法实体 → [[hcff-pinn]]

## 1. 基础结构动力方程

SDOF 模型为

$$m\ddot u(t)+c\dot u(t)+ku(t)=p(t),$$

MDOF 模型为 $M\ddot{\mathbf u}+C\dot{\mathbf u}+K\mathbf u=\mathbf P(t)$。网络以时间 $t$ 为输入、位移为输出，速度和加速度由自动微分得到。标准 [[pinn]] 同时最小化 ODE、初位移和初速度损失，本文将其诊断为谱偏差与多损失梯度失衡的叠加。

## 2. 物理引导 Fourier 特征

随机 Fourier 映射为

$$\gamma(t)=[\cos(Bt),\sin(Bt)],\qquad B\sim\mathcal N(0,\sigma^2).$$

多组 $\sigma_i$ 的分支特征经过各自全连接层后拼接并线性组合。与任意选择尺度不同，HCFF-PINN 用结构自振频率设定 $\sigma$：SDOF 使用阻尼自振频率

$$\omega_d=\sqrt{k/m}\sqrt{1-\xi^2},$$

MDOF 使用前几阶模态频率。3-DOF 剪切框架取 $[8.90,24.94,36.04]$ rad/s，四层钢框架取 $[9.17,23.47,35.72]$ rad/s。

从 [[neural-tangent-kernel]] 角度，标准 FNN 的大特征值方向偏低频；Fourier 映射把与 $B$ 对应的正弦/余弦方向显式送入网络，使高频分量不必靠深层 MLP 从低频表示中缓慢形成。

## 3. 初值硬约束与 label-free

作者设结构初始静止，即 $u(0)=0,\dot u(0)=0$，并令

$$u(t)=g(t)N(t;\theta).$$

只要 $g(0)=g'(0)=0$，两个初始条件便与网络参数无关地成立。最终选择

$$g(t)=\tanh^2(t),$$

于是训练目标简化为单项 ODE 残差

$$L_r=\frac1{N_u}\sum_i\left|m\ddot u(t_i)+c\dot u(t_i)+ku(t_i)-p(t_i)\right|^2.$$

这里的 label-free 仅指删除初值采样点和 IC loss；地震输入 $p(t)$、结构参数及配点仍是求解所必需的信息。

## 4. 五种调制函数消融

| $g(t)$ | 时间 | 相对 $L_2$ | 结论 |
|---|---:|---:|---|
| $t^2$ | 281 s | 49.87% | 失败 |
| $t\log(1+t)$ | 294 s | 31.53% | 失败 |
| $t-\log(1+t)$ | 277 s | 40.01% | 失败 |
| $\tanh(t)-\log(1+t)$ | 281 s | 16.52% | 仍不准确 |
| $\tanh^2(t)$ | 223 s | 0.28% | 最优且稳定 |

作者把差异归因于初始渐近行为、函数/导数是否无界及梯度符号变化；$\tanh^2(t)$ 有界且梯度平稳。但文中又称前四种在 $t\to0$ 均等价于 $t^2$，而 $\tanh^2(t)$ 本身也满足 $\tanh^2(t)\sim t^2$，故“初始阶数”不足以单独解释巨大差异，晚期有界性与优化景观需要独立消融。

## 5. 训练流程

| 场景 | 网络与优化 |
|---|---|
| SDOF 基线/FF-PINN | 4 层×50，tanh，lr=0.001，2000 interior、1000 initial，Adam，50000 iterations |
| MDOF 各 PINN 变体 | 4 层×50，tanh，lr=0.001，2000 interior；Adam 5000 + L-BFGS 5000 |
| 四层钢框架 | 与 MDOF 相同，Adam 5000 + L-BFGS 5000 |

HCFF-PINN 不需要 initial points；表格中的 1000 initial points 对应含 IC loss 的基线模型。两阶段优化先用 Adam 快速进入可行区域，再用 L-BFGS 精修。

## 6. 四层钢框架降阶

有限元模型含 25 节点、每节点 3 DOF；去除 5 个边界节点后为 60 DOF。作者用静力凝聚消去从属 DOF，得到 20 个主 DOF 的线性动力方程，再由 HCFF-PINN 求解。该验证证明了对降阶线性系统的扩展性，不等价于直接求解完整 60-DOF 或非线性有限元系统。

## 7. 与 AT-PINN-HC 的区别

| 维度 | HCFF-PINN | [[at-pinn-hc]] |
|---|---|---|
| 主要瓶颈 | 多频谱偏差 + IC/ODE loss 冲突 | 长时振动中的边界/初值硬约束与误差推进 |
| 频谱增强 | 自振频率引导 Fourier features | 非核心组件 |
| 初值形式 | $\tanh^2(t)$，零位移/零速度 | 多策略、多辅助函数 |
| 时间策略 | 整段时域训练 | 时间推进分段 |
| 已验证物理 | 线性 SDOF/MDOF/钢框架 | 线弹性梁/板振动 |

## 关联页面
- [[du2026-hcff-pinn-analysis]] — 12 维概述
- [[du2026-hcff-pinn-results]] — 数值证据
- [[hcff-pinn]] — 方法实体
- [[neural-tangent-kernel]] — 理论动机
