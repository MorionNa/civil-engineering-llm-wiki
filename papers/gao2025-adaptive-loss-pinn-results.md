---
id: papers--gao2025-adaptive-loss-pinn-results
title: Gao et al. (2025) — APINNs 数值结果与证据核查
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
keywords:
- adaptive-weighting
- collocation-strategy
- neural-network
- nonlinear-systems
- physics-constrained-loss
- physics-constraint-weight-tuning
- physics-informed
- pinn
- synthetic-data
sources:
- sources/papers/gao2025-adaptive-loss-pinn.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- multitask-learning
- adaptive-loss-weighting
- automatic-differentiation
results:
- relative-l2-error-reduction
- loss-scale-balancing
- convergence-acceleration
failure_modes:
- reporting-inconsistency
- configuration-mismatch
- no-random-seed-statistics
datasets:
- benjamin-ono-analytic-solution
- sine-gordon-analytic-solution
- mukherjee-kundu-analytic-solution
reproducibility: low
---

# Gao et al. (2025) — APINNs 数值结果与证据核查

> 返回概述 → [[gao2025-adaptive-loss-pinn-analysis]]；方法细节 → [[gao2025-adaptive-loss-pinn-method]]

## 1. 评价指标

论文以相对 $L_2$ 误差评价预测解，并以逐点绝对误差 $|u_i-u_i^*|$ 绘制误差图。提取文本中的相对误差分母写为 $\sum_i u_i^2$，没有明确标成精确解 $u_i^*$，因此本页沿用论文表格报告值，不自行改写指标定义。

## 2. Benjamin–Ono 孤立波

| 模型 | 区域 $\Omega$ | $(N_0,N_b,N_f)$ | 迭代 | 相对 $L_2$ |
|---|---|---|---:|---:|
| PINN | $[-5,5]\times[0,5]$ | (2000, 2000, 20000) | 8000 | $6.442025\times10^{-1}$ |
| PINN | $[-6,6]\times[0,1]$ | (2000, 2000, 20000) | 8000 | $5.462345\times10^{-1}$ |
| PINN | $[-5,5]\times[0,5]$ | (1000, 200, 10000) | 8000 | $7.272635\times10^{-1}$ |
| APINNs | $[-5,5]\times[0,5]$ | (2000, 2000, 20000) | 4400 | $1.488114\times10^{-2}$ |
| APINNs | $[-6,6]\times[0,1]$ | (2000, 2000, 20000) | 4230 | $3.462345\times10^{-2}$ |
| APINNs | $[-5,5]\times[0,5]$ | (1000, 200, 10000) | 8000 | $1.194622\times10^{-1}$ |

首组完全对齐时误差下降约 97.7%（43.29 倍），迭代数减少 45%。在作者讨论的训练曲线中，PINN 到 8000 次时四项损失为 $6.996\times10^{-4}$、$1.248\times10^{-3}$、$1.313\times10^{-3}$、$6.957\times10^{-3}$，最大点误差可达 6；APINNs 到 4400 次时分别为 $6.245\times10^{-5}$、$9.478\times10^{-5}$、$1.495\times10^{-5}$、$4.931\times10^{-4}$，最大点误差小于 0.12。

## 3. Sine–Gordon 呼吸波

| 模型 | 区域 $\Omega$ | $(N_0,N_b,N_f)$ | 迭代 | 相对 $L_2$ |
|---|---|---|---:|---:|
| PINN | $[-5,5]\times[-10,10]$ | (50, 50, 15000) | 15000 | $2.125225\times10^{-1}$ |
| PINN | $[-6,6]\times[-10,10]$ | (100, 100, 15000) | 15000 | $2.725725\times10^{-1}$ |
| PINN | $[-5,5]\times[-10,10]$ | (100, 100, 15000) | 15000 | $1.184863\times10^{-1}$ |
| APINNs | $[-5,5]\times[-10,10]$ | (50, 50, 15000) | 15000 | $2.065112\times10^{-2}$ |
| APINNs | $[-6,6]\times[-10,10]$ | (100, 100, 15000) | 15000 | $5.289643\times10^{-2}$ |
| APINNs | $[-5,5]\times[-10,10]$ | (100, 100, 15000) | 15000 | $3.267198\times10^{-2}$ |

首组对齐比较中误差下降约 90.3%（10.29 倍）。到 15000 次迭代，PINN 四项损失为 $1.255\times10^{-6}$、$5.036\times10^{-7}$、$4.322\times10^{-7}$、$1.618\times10^{-5}$，最大点误差约 1.0；APINNs 分别为 $1.777\times10^{-6}$、$2.228\times10^{-6}$、$1.845\times10^{-6}$、$8.373\times10^{-6}$，最大点误差小于 0.1。

## 4. Mukherjee–Kundu 呼吸波

| 模型 | 区域 $\Omega$ | $(N_0,N_b,N_f)$ | 迭代 | 相对 $L_2$ |
|---|---|---|---:|---:|
| PINN | $[-6,6]\times[-2.5,2.5]$ | (100, 100, 20000) | 8000 | $3.556391\times10^{-1}$ |
| PINN | $[-5,5]\times[-2.5,2.5]$ | (100, 100, 20000) | 8000 | $4.109634\times10^{-1}$ |
| PINN | $[-6,6]\times[-3,3]$ | (500, 100, 20000) | 8000 | $3.126423\times10^{-1}$ |
| APINNs | $[-6,6]\times[-2.5,2.5]$ | (100, 100, 20000) | 8000 | $1.124187\times10^{-1}$ |
| APINNs | $[-5,5]\times[-2.5,2.5]$ | (100, 100, 20000) | 8000 | $1.003564\times10^{-1}$ |
| APINNs | $[-6,6]\times[-3,3]$ | (500, 100, 20000) | 8000 | $1.356974\times10^{-1}$ |

首组对齐比较中误差下降约 68.4%（3.16 倍）；第二组下降约 75.6%（4.10 倍）。训练曲线讨论给出的 PINN 四项损失为 $3.767\times10^{-5}$、$2.029\times10^{-7}$、$1.658\times10^{-7}$、$2.864\times10^{-5}$，最大点误差约 0.3；APINNs 为 $5.689\times10^{-6}$、$1.226\times10^{-6}$、$1.256\times10^{-6}$、$4.289\times10^{-6}$，最大点误差小于 0.05。

## 5. 证据强度

三组表格一致支持 APINNs 优于同配置 PINN，且各分量损失通常更接近。但只有 Benjamin–Ono 首组同时显示迭代数明显减少；Sine–Gordon 和 Mukherjee–Kundu 的表格迭代数相同，不能据此主张普遍训练加速。[[wang2021-pinn-ntk-failure-analysis]] 从梯度/NTK 角度解释损失失衡，本文结果只提供经验支持，没有证明损失量级平衡就是梯度或收敛速率平衡。

## 6. 文内不一致与审读注意

1. Benjamin–Ono 图示正文称 $N_b=200$，表 1 对应首行写 $N_b=2000$；正文还把 PINN 首行误差 $0.6442025$ 与 APINNs 第二行误差 $0.03462345$ 并列，条件并未完全对齐。
2. Sine–Gordon 正文把区域 $[-6,6]$ 的 PINN 值 $0.2725725$ 与区域 $[-5,5]$ 的 APINNs 值 $0.03267198$ 并列；结论段改用首组对齐值 $0.2125225$ 与 $0.02065112$。
3. 结论称 Mukherjee–Kundu 误差“小于 10%”，但表中 APINNs 最低值是 $0.1003564$，严格说略高于 10%；摘要较谨慎地表述为“约 10%”。
4. 论文只给单次结果，没有随机种子、均值、标准差或显著性检验，无法判断改进的随机稳定性。

因此，横向比较应使用本页表格中区域、采样与迭代均一致的行，不应直接采用正文中混配的数字。

## 关联页面
- [[gao2025-adaptive-loss-pinn-analysis]] — 论文概述
- [[gao2025-adaptive-loss-pinn-critical]] — 贡献与局限
- [[adaptive-loss-weighting-pinn]] — APINNs 方法实体
- [[raissi2019-pinn-analysis]] — 标准 PINN 基线范式

## Evidence By Source

### `sources/papers/gao2025-adaptive-loss-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_camwa_2025_01_007.xml`, `raw/papers/extracted/10_1016_j_camwa_2025_01_007_extracted.txt`

^[sources/papers/gao2025-adaptive-loss-pinn.md]
