---
title: "Liu et al. (2025) — PINN 用于一维地震场地反应分析：论文分析"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [neural-network, physics-informed, deep-learning, soft-constraint, collocation-strategy, structural-dynamics, seismic-response, equation-of-motion, ground-motion, synthetic-data, benchmark, physics-constraint-weight-tuning, neural-tangent-kernel, pinn, ai4s, physics-simulation]
sources: [raw/papers/10_1016_j_compgeo_2025_107137.xml, raw/papers/extracted/10_1016_j_compgeo_2025_107137_extracted.txt]
methods: [fourier-feature-embedding, nondimensionalization, tree-structured-parzen-estimator, batch-normalization, adam, automatic-differentiation, lumped-mass-formulation]
results: [rk45-agreement, newmark-beta-agreement, single-layer, three-layer, ten-layer, wide-intensity-range]
failure_modes: [finite-collocation-nonuniqueness, per-scenario-retraining, spectral-bias, sigma-sensitivity, no-speed-benchmark, linear-soil-only, missing-code]
datasets: [NGA-West2-ground-motion-records, synthetic-layered-soil-profiles]
reproducibility: low
code_url: []
dataset_url: []
confidence: high
---

# Leveraging PINNs in geotechnical earthquake engineering

> **作者：** Chenying Liu, Jorge Macedo, Alexander Rodríguez
> **期刊：** *Computers and Geotechnics*（2025）
> **DOI：** 10.1016/j.compgeo.2025.107137

## 1. 工程背景

> **⚠️ 非线性类型：** **本文验证范围是线性 Kelvin–Voigt/线性弹性土层，不存在已验证的材料本构非线性。** 集中质量模型采用常数质量、黏性阻尼和刚度矩阵，响应方程为线性 ODE；非线性只存在于神经网络函数逼近与优化过程。论文仅把**等效线性**描述为可由一系列线性分析串联实现的延伸建议，把**全非线性土体**明确留作未来工作，不能将本文归类为已验证的非线性本构 PINN。

一维地震场地反应分析把基岩输入地震动传播到地表，用于评估土层对不同频率成分的放大或滤波，是岩土地震工程与抗震设计的基础输入。传统 Newmark-beta（NB）和 Runge–Kutta 方法成熟可靠；本文关注 PINN 能否提供连续、可微且易于嵌入数据的替代求解表示。

## 2. Research Gap

据作者调研，PINN 在岩土地震工程、尤其一维场地反应中的系统评估仍缺失。该问题的瞬态地震输入包含宽频谱，普通 MLP 存在 [[neural-tangent-kernel|NTK]] 谱偏置；同时初始条件与运动方程残差量级不同，容易造成梯度失衡。

## 3. 科学问题

在土层先离散为集中质量系统后，如何使时间连续 PINN 同时捕捉低频与高频响应、稳定满足初始条件和运动方程，并在不同层数、土体刚度及地震动强度/持时下达到与成熟积分算法一致的精度？

## 4. 研究目标

建立面向线性一维场地反应的 [[seismic-site-response-pinn]]：诊断谱偏置与损失尺度问题，组合 Fourier 特征、无量纲化、学习率调度、批归一化和 TPE 超参数搜索，并以 RK45/NB 对 1、3、10 层系统及多类地震动进行验证。

## 5. 方法机制

土柱先转化为 $n$ 自由度集中质量模型：

$$\mathbf M\ddot{\mathbf u}+\mathbf C\dot{\mathbf u}+\mathbf K\mathbf u=-\mathbf M\mathbf I\ddot u_g,$$

其中本文验证时 $\mathbf C,\mathbf K$ 为常数。网络输入时间 $t$，输出各土层节点位移向量 $\mathbf u(t)$；速度和加速度由自动微分得到。损失由零初始位移/速度与运动方程残差组成。Fourier 特征缓解高频谱偏置，无量纲化使权重 $\lambda=1$ 可稳定训练。详见 [[liu2025-site-response-pinn-method]]。

## 6. 结果证据

Table 2 中，PINN 相对 RK45/NB 的位移 RMSE 分别为 $5.35\times10^{-8}/3.43\times10^{-8}$ cm，速度为 $5.79\times10^{-7}/5.26\times10^{-7}$ cm/s，加速度为 $3.57\times10^{-6}/3.12\times10^{-6}$ cm/s²。验证覆盖 1/3/10 层、PGA 0.003–1.8 g、$D_{5-95}$ 2–148 s；这是**逐场景重新训练后的稳健性**，不是对未见场景的一次训练泛化。详见 [[liu2025-site-response-pinn-results]]。

## 7. 贡献

1. 据作者所知，首次系统评估 PINN 作为岩土地震工程场地反应求解器的潜力。
2. 把谱偏置诊断与工程频带联系起来，并用 Fourier 特征显著改善收敛。
3. 给出可操作训练流程：无量纲化、TPE、Adam 调度、BatchNorm 与激活函数筛选。
4. 在宽土层/地震动范围内与两类传统积分算法交叉核验，而不只展示单一算例。

## 8. 核心知识点

- 本文是“空间集中质量离散 + 时间连续神经求解”，不是完全无空间离散的场地模型。
- Fourier 特征的 $m$ 推荐 50–200、$\sigma$ 推荐 0.1–2，性能对 $\sigma$ 更敏感；过小会过度平滑，过大会引入高振荡。
- 连续网络表示可直接用 AD 得到速度/加速度，避免由离散位移做有限差分。
- 该 [[pinn]] 是每个方程实例的求解器，不是训练一次即可跨土层、跨地震动推理的代理模型。

## 9. Negative Knowledge

- **有限配点零损失不保证唯一正确解。** 论文明确指出，ODE/IC 只在有限样本上软满足时，可能存在多个低损失函数；必须用独立时间点和传统算法验证。
- **每个新土层或地震动都需要重训。** 系统参数与输入变化会改变方程实例，本文不提供零样本跨场景泛化。
- **本文不以提速为目标。** 没有给出 PINN 与 RK45/NB 的运行时间、训练成本或盈亏平衡点，不能声称计算加速。
- **只验证线性土层。** 等效线性只是串行线性分析的延伸建议；全非线性本构需要新增土体非线性信息，尚未实现。
- 数据可用性声明为 “No data was used”，正文虽引用 NGA-West2 输入地震动但未见代码和可直接复现实验的记录清单；精确复现受限。
- 结果依赖 $\sigma$、TPE 搜索与“properly trained”前提，不能把不同刚度/地震动下的成功写成无条件不敏感。详见 [[liu2025-site-response-pinn-critical]]。

## 10. 可迁移知识

“先无量纲化、再 Fourier 嵌入、最后用验证集搜索频率尺度”的流程可迁移到桥梁振动、波动方程和其他宽频瞬态系统。[[neural-tangent-kernel]] 提供谱偏置与损失梯度不平衡的解释框架。

## 11. 研究机会

下一步应分别验证等效线性迭代与真正非线性本构，加入真实场地观测和不确定性；用迁移学习、元学习或神经算子减少逐场景重训，并公开与传统算法同精度下的端到端时间/能耗基准。

## 12. 可复现性

**🔴 低复现性**——控制方程、训练流程和推荐范围较清楚，但未见代码；最终每个案例的 TPE 参数、随机种子、硬件、停止条件与 NGA-West2 记录标识在正文提取文本中不完整。

| 项目 | 说明 |
|------|------|
| **等级** | 🔴 低 |
| **官方代码** | 未见公开链接 |
| **数据集** | 文中使用 NGA-West2 地震动作为输入；Data availability 声明 “No data was used” |
| **协议** | 未见代码/数据协议 |
| **复现要点** | 先复现无量纲单层系统；独立验证点核对 RK45/NB；再加入 Fourier/TPE；每场景重新搜索并训练 |

## 关联页面

- [[liu2025-site-response-pinn-method]] — 方程、网络与调参流程
- [[liu2025-site-response-pinn-results]] — 精度、频域和覆盖范围
- [[liu2025-site-response-pinn-critical]] — 验证边界与研究机会
- [[seismic-site-response-pinn]] — 方法实体
- [[pinn]] — PINN 基础实体
- [[neural-tangent-kernel]] — 谱偏置与梯度失衡
