---
id: papers--wu2025-cm-pinn-results
title: Wu et al. (2025) — CM-PINNs 实验结果展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
keywords:
- data-scarcity
- hysteresis
- lstm
- nonlinear-systems
- physics-informed
- pinn
- sdof
- seismic-response
- structural-dynamics
- synthetic-data
sources:
- sources/papers/wu2025-cm-pinn.md
created: '2026-07-01'
updated: '2026-07-31'
confidence: high
results:
- cross-domain-generalization
- extrapolation-ability
- synthetic-data
datasets:
- blwn
- synthetic-data
---

# Wu et al. (2025) — CM-PINNs 实验结果展开

> 返回概述 → [[wu2025-cm-pinn-analysis]]

## 1. 数据与评价指标

SDOF 数据：100 条 BLWN 地震动，每条 30 s、50 Hz、1501 时间步；10 条有标签训练，90 条测试；额外 50 条输入序列用于 physics-informed collocation。OpenSeesPy 用于验证 PyTorch 结构响应计算框架。评价指标包括 Pearson $R$、峰值误差 $E_{Peak}$ 和归一化误差分布 CI。

## 2. SDOF：本构约束有效性

| 指标 | PhyLSTM | CM-PhyLSTM | 改善 |
|---|---:|---:|---:|
| 2% 误差阈值内 CI | 84.97% | 92.28% | +7.31pp |
| 位移最大 $E_{Peak}$ | 12.11% | 8.11% | 约 33% 降低 |
| 位移平均峰值误差 | — | — | 约 10% 降低 |

结论：显式本构约束显著提高峰值预测，说明结构响应 PINN 中只写运动方程是不够的；恢复力还需要满足材料/构件本构。

## 3. SDOF：FC-SLSTM 架构有效性

| 架构 | 2% 误差阈值内 CI | 位移最大 $E_{Peak}$ |
|---|---:|---:|
| LSTM | 92.28% | 8.11% |
| SLSTM | 93.48% | 6.23% |
| FC-SLSTM | 97.23% | 5.92% |

结论：skip connection 有帮助，但仅 skip 不够；FC preprocessing 能过滤和变换浅层特征，使其更适合与深层 LSTM 特征融合。

## 4. SDOF：自适应权重初始化

| 指标 | Fixed Init | Adaptive Init |
|---|---:|---:|
| 2% 误差阈值内 CI | 97.23% | 99.01% |
| 位移最大 $E_{Peak}$ | 5.92% | 4.14% |
| 位移平均 $E_{Peak}$ | 1.18% | 0.75% |

结论：多损失 PINN 的物理项量级不平衡会直接影响收敛；按 $L^D_u$ 基准初始化权重能提高稳定性和精度。

## 5. MDOF Case 1：对称 5-DOF 剪切模型

| 指标 | 3rd DOF | 5th DOF |
|---|---:|---:|
| 5% 误差阈值内 CI | 96.11% | 96.27% |
| 平均 $E_{Peak}$ | 1.84% | 2.38% |
| $E_{Peak}$ 标准差 | 1.45% | 1.89% |
| 最大 $E_{Peak}$ | < 7.5% | < 7.5% |

5-DOF 平均 $R=0.9978$。结论：CM-PINNs 对中层和顶层响应均保持高精度，说明方法不只适用于 SDOF。

## 6. MDOF Case 2：非对称 7-DOF 剪切模型

| 指标 | 3rd DOF | 5th DOF |
|---|---:|---:|
| 5% 误差阈值内 CI | 98.32% | 98.30% |
| 平均 $E_{Peak}$ | 2.25% | 2.06% |
| $E_{Peak}$ 标准差 | 1.85% | 1.70% |
| 最大 $E_{Peak}$ | < 9.3% | < 9.3% |

7-DOF 平均 $R=0.9986$。即使结构非对称、自由度增加，CM-PINNs 仍能稳定捕捉非线性位移响应。

## 7. Appendix C：CM-PINNs vs PhyLSTM MDOF 对比

### 位移响应（5th DOF）
| 系统 | 模型 | CI95% | Mean EPeak | Max EPeak | R |
|---|---|---:|---:|---:|---:|
| 5-DOF | PhyLSTM | 88.54% | 3.01% | 15.38% | 99.6 |
| 5-DOF | CM-PINNs | 96.27% | 2.37% | 7.48% | 99.8 |
| 7-DOF | PhyLSTM | 88.20% | 2.86% | 9.90% | 99.6 |
| 7-DOF | CM-PINNs | 98.30% | 2.07% | 6.97% | 99.9 |

### 速度响应（5th DOF）
| 系统 | 模型 | CI95% | Mean EPeak | Max EPeak | R |
|---|---|---:|---:|---:|---:|
| 5-DOF | PhyLSTM | 89.24% | 2.68% | 12.99% | 99.5 |
| 5-DOF | CM-PINNs | 97.80% | 2.05% | 8.41% | 99.8 |
| 7-DOF | PhyLSTM | 95.32% | 2.42% | 7.71% | 99.7 |
| 7-DOF | CM-PINNs | 99.28% | 1.66% | 7.16% | 99.9 |

### 加速度响应（5th DOF）
| 系统 | 模型 | CI95% | Mean EPeak | Max EPeak | R |
|---|---|---:|---:|---:|---:|
| 5-DOF | PhyLSTM | 46.24% | 5.38% | 14.03% | 97.1 |
| 5-DOF | CM-PINNs | 69.83% | 4.02% | 9.57% | 98.9 |
| 7-DOF | PhyLSTM | 48.39% | 9.62% | 25.72% | 96.2 |
| 7-DOF | CM-PINNs | 53.57% | 8.84% | 23.08% | 96.9 |

加速度的改善幅度小于位移/速度，说明高阶导数或差分派生响应仍是 CM-PINNs 的薄弱环节。

## 8. 结果总判读

| 论文问题 | 实验证据 | 判读 |
|---|---|---|
| 本构约束是否有用？ | CI 84.97%→92.28%，峰值 12.11%→8.11% | 有用，尤其对峰值 |
| FC-SLSTM 是否有用？ | CI 92.28%→97.23%，峰值 8.11%→5.92% | 有用，保留浅层时序特征 |
| 自适应权重是否有用？ | CI 97.23%→99.01%，峰值 5.92%→4.14% | 有用，缓解多 loss 不平衡 |
| 能否扩展 MDOF？ | 5-DOF/7-DOF R≈0.998 | 初步可扩展 |
| 最大风险在哪里？ | 加速度 CI 仍低，真实数据未验证 | 高阶导数与真实泛化仍需验证 |

## 关联
- [[wu2025-cm-pinn-analysis]] — 论文概述
- [[wu2025-cm-pinn-method]] — 方法机制
- [[wu2025-cm-pinn-critical]] — 批判与机会
- [[zhang2020-phylstm-results]] — PhyLSTM 原始结果对照

## Evidence By Source

### `sources/papers/wu2025-cm-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/wu2025-cm-pinn-extracted.md`

^[sources/papers/wu2025-cm-pinn.md]
