---
title: "Liu et al. (2025) — 地震场地反应 PINN：方法机制"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [neural-network, physics-informed, deep-learning, soft-constraint, collocation-strategy, structural-dynamics, seismic-response, equation-of-motion, ground-motion, physics-constraint-weight-tuning, neural-tangent-kernel, pinn, ai4s, physics-simulation]
sources: [raw/papers/10_1016_j_compgeo_2025_107137.xml, raw/papers/extracted/10_1016_j_compgeo_2025_107137_extracted.txt]
methods: [lumped-mass-formulation, fourier-feature-embedding, nondimensionalization, tree-structured-parzen-estimator, batch-normalization, tanh, adam, learning-rate-scheduling, automatic-differentiation]
results: [spectral-bias-mitigation, stable-linear-site-response-solution]
failure_modes: [finite-collocation-nonuniqueness, sigma-sensitivity, gradient-imbalance, relu-second-derivative-zero, per-scenario-retraining]
datasets: [NGA-West2-ground-motion-records, synthetic-layered-soil-profiles]
reproducibility: low
code_url: []
dataset_url: []
confidence: high
---

# Liu et al. (2025) — 方法机制

> 返回总览：[[liu2025-site-response-pinn-analysis]]；方法实体：[[seismic-site-response-pinn]]

## 5.1 空间集中质量离散

一维土柱假定水平剪切波竖向传播，土体采用线性 Kelvin–Voigt 固体。作者先把土层离散成 $n$ 个集中质量自由度，再求时间响应：

$$\mathbf M\ddot{\mathbf u}(t)+\mathbf C\dot{\mathbf u}(t)+\mathbf K\mathbf u(t)=-\mathbf M\mathbf I\ddot u_g(t),$$

$$\mathbf u(0)=\mathbf 0,\qquad \dot{\mathbf u}(0)=\mathbf 0.$$

网络只替代时间积分器；空间层数/自由度仍由传统物理离散给出。因此“无网格”最多指时间方向不需要显式步进，不应理解为三维场地完全无离散。

## 5.2 时间连续 PINN

令 $\mathbf N(t;\Theta)=\mathbf u(t)$。网络输入一个时间标量，输出长度为 $n$ 的节点位移向量，AD 计算 $\dot{\mathbf N}$ 与 $\ddot{\mathbf N}$：

$$\mathcal L(\Theta)=\lambda\mathcal L_{ic}+\mathcal L_r,$$

$$\mathcal L_{ic}=\|\mathbf N(0;\Theta)\|^2+\|\dot{\mathbf N}(0;\Theta)\|^2,$$

$$\mathcal L_r=\frac1{N_t}\sum_i\|\mathbf M\ddot{\mathbf N}(t_i)+\mathbf C\dot{\mathbf N}(t_i)+\mathbf K\mathbf N(t_i)+\mathbf M\mathbf I\ddot u_g(t_i)\|_2^2.$$

多自由度残差使用欧氏范数。有限时间点上的软约束是 [[pinn]] 训练信号，但不等同于在整个连续域严格满足方程。

## 5.3 无量纲化与损失平衡

单层系统写作

$$\ddot u+2\zeta\omega\dot u+\omega^2u=-\ddot u_g.$$

令 $t=ay$、$u=bz$，其中 $a=1/\omega$、$b=-a^2$，得到

$$z''+2\zeta z'+z=\ddot u_g(ay).$$

该步骤统一惯性、阻尼、刚度与初值项的尺度，使本文可取 $\lambda=1$。作者把基于 [[neural-tangent-kernel]] 特征值动态调整 $\lambda$ 作为尺度仍失衡时的备选方法，而不是本文主实验实际采用的配置。

## 5.4 Fourier 特征缓解谱偏置

$$\gamma(t)=\begin{bmatrix}\sin(2\pi\mathbf Bt)\\\cos(2\pi\mathbf Bt)\end{bmatrix},\qquad \mathbf B\sim\mathcal N(0,\sigma^2\mathbf I).$$

$m$ 控制随机 Fourier 频率数量/嵌入容量，$\sigma$ 控制覆盖的频率尺度。示例采用 $m=100,\sigma=0.6$；普通 4 层 MLP 训练 5,000 次后 RMSE 仍为 0.48，而加 Fourier 特征后约 50 次迭代就能在工程关注的 0.1–30 Hz 区间贴近 NB 结果。

| 超参数 | 作用 | 论文建议/观察 |
|--------|------|---------------|
| $m$ | 可表达频率数量、容量与成本 | 一般搜索 50–200；100 与 200 在示例中接近 |
| $\sigma$ | 频率尺度 | 搜索 0.1–2；比 $m$ 更敏感 |
| 过小 $\sigma$ | 频带过窄 | 输出过度平滑，漏掉高频 |
| 过大 $\sigma$ | 频率过高 | 学得表示可能强振荡；示例 $\sigma=1.5$ 已退化 |

## 5.5 最终网络与优化

```text
t ─► Fourier embedding(m, σ) ─► 3×全连接层 ─► BatchNorm + tanh ─► u(t)∈Rⁿ
                                                                  │
                                                         AD ─► u̇(t), ü(t)
                                                                  │
                                              IC + equation residual loss
```

| 组件 | 设置 |
|------|------|
| 数据划分 | 时间戳与地震加速度 70% 训练 / 30% 验证用于调参 |
| 搜索器 | Tree-Structured Parzen Estimator（TPE） |
| 主架构 | Fourier 嵌入 + 3 个全连接层 + BatchNorm + tanh |
| 宽/深经验范围 | 宽度 50–500；深度 3–6 |
| 优化器 | Adam；初始学习率 0.01 |
| 调度 | 连续 50 次迭代无改进时学习率乘 0.5 |
| 最终训练 | 用选定超参数在全部时间点上重新训练 |

作者测试 Sigmoid、tanh、ReLU、Leaky ReLU、GELU，推荐 tanh 或 GELU；明确不推荐 ReLU，因为其二阶导数为零，会破坏加速度/二阶 ODE 残差计算。Adam 在其测试中优于 SGD、L-BFGS、RMSprop、Adagrad。

## 5.6 每场景重新训练

土层属性或输入地震动变化会改变方程系数/外力，因此流程必须重新运行。70/30 划分与 TPE 是单一场景内的超参数选择，不是跨场景监督学习；训练完成后也只负责该场景。这一区分决定了本文不能直接声称部署级实时推理。

## 关联页面

- [[liu2025-site-response-pinn-results]] — 单层、多层与极端地震动结果
- [[liu2025-site-response-pinn-critical]] — 有限配点与逐场景重训风险
- [[neural-tangent-kernel]] — 谱偏置解释
- [[pinn]] — 经典 PINN 方法
