---
id: papers--du2026-hcff-pinn-results
title: Du et al. (2026) — HCFF-PINN 数值结果与证据核查
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
- adam-lbfgs
- benchmark
- deep-learning
- equation-of-motion
- finite-element
- ground-motion
- hard-constraints
- neural-network
- physics-informed
- pinn
- sdof
- seismic-response
- structural-dynamics
- synthetic-data
- vibration-analysis
sources:
- sources/papers/du2026-hcff-pinn.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- physics-guided-fourier-features
- hard-initial-conditions
- tanh-squared-modulation
- static-condensation
- adam-lbfgs-optimization
results:
- mixed-frequency-error-reduction
- multi-degree-of-freedom-validation
- cross-ground-motion-robustness
- frequency-prior-sensitivity
failure_modes:
- baseline-reporting-inconsistency
- extreme-frequency-prior-mismatch
- nonconvergence-of-gradient-and-self-adaptive-baselines
datasets:
- synthetic-harmonic-loads
- northridge-symlar
- gazli-karakyr
- kocaeli-duzce
- el-centro-array
- san-simeon-diablo-canyon
reproducibility: medium
---

# Du et al. (2026) — HCFF-PINN 数值结果与证据核查

> 返回概述 → [[du2026-hcff-pinn-analysis]]；方法配置 → [[du2026-hcff-pinn-method]]

## 1. SDOF：谱偏差诊断与 Fourier 增益

SDOF 参数为 $m=1$ kg、$k=20$ N/m、阻尼比 0.1。低频荷载为 $10\sin(2t)$，混频荷载为 $30\sin(60t)+2\cos(0.5t)$；所有模型训练 50000 次。

| 模型 | 低频相对 $L_2$ | 混频相对 $L_2$ | 混频高频段误差 |
|---|---:|---:|---:|
| 传统 PINN | 1.1% | 38% | 58% |
| FF-PINN | 0.03% | 0.36% | 原文称 FFT 幅值误差很小，未给单一汇总数 |

FF-PINN 将低频和混频总误差分别降低约 97% 和 99%。前六个 NTK 特征向量由传统 PINN 的平滑低频形态转为包含更丰富高频振荡，支持 Fourier 映射改变可学习频谱的解释。

## 2. 硬约束函数消融

$\tanh^2(t)$ 的误差 0.28%、训练 223 s；其余四种函数误差 16.52%–49.87%、训练 277–294 s。结果表明“满足 $g(0)=g'(0)=0$”只是必要条件，不足以保证可训练性；调制函数在全时域的有界性和导数行为同样关键。详见 [[du2026-hcff-pinn-method]]。

## 3. 3-DOF Northridge 对比

表 6 报告 DOF1 的位移、速度、加速度误差：

| 模型 | 高频段 Disp/Velo/Acc | 时域 Disp/Velo/Acc | 训练时间 |
|---|---|---|---:|
| PI-KAN | 0.67% / 0.65% / 0.66% | 1.03% / 1.01% / 1.01% | 1532 s |
| FF-PINN | 0.82% / 0.81% / 0.82% | 1.22% / 1.22% / 1.22% | 881 s |
| G-PINN | 99.92% / 99.92% / 99.91% | 99.97% / 99.97% / 99.97% | 1131 s |
| SA-PINN | 99.95% / 99.94% / 99.94% | 100% / 99.99% / 99.99% | 1375 s |
| **HCFF-PINN** | **0.25% / 0.26% / 0.24%** | **0.29% / 0.30% / 0.29%** | **713 s** |

HCFF-PINN 明显优于其余模型，并比 FF-PINN 快约 19%、比 PI-KAN 快约 53%。论文正文把 FF-PINN 概括为“约 1.0%”、PI-KAN 为“约 1.2%”，但表 6 实际显示 PI-KAN 时域约 1.01%–1.03%、FF-PINN 为 1.22%；本页以表格原值为准并保留该不一致。

G-PINN 与 SA-PINN 的失败说明：只加高阶残差或动态权重并没有消除 FNN 的频谱表示瓶颈。这个结论与 [[neural-tangent-kernel]] 的谱偏差解释一致，但仅基于本文给定超参数，不能视为这些方法普遍失效。

## 4. 四条地震动泛化

| 地震记录 | PGA | 时长 | 时域误差 | 0–50 Hz 频域误差 |
|---|---:|---:|---:|---:|
| Gazli 1976 | 0.608 g | 16.26 s | 0.37% | 0.33% |
| Northridge 1994 | 0.410 g | 29.98 s | 0.28% | 0.22% |
| Kocaeli 1999 | 0.312 g | 34.995 s | 0.31% | 0.33% |
| El Centro 1940 | 0.319 g | 39.03 s | 0.32% | 0.34% |

同一组超参数下八个指标均低于 0.5%，覆盖脉冲型、近场、长周期远场和长持续时间输入。结论段据此报告 MDOF 相对 FF-PINN 改善 30%–60%。

## 5. 四层钢框架与频率敏感性

四层四跨线性钢框架由 60 DOF 静力凝聚为 20 DOF，以 San Simeon 地震动输入。HCFF-PINN 在所有楼层的位移、速度、加速度时域与频域图中优于 FF-PINN，但提取全文没有给出统一的全局相对 $L_2$ 数字，因此不在此补写。

频率先验试验显示：使用部分真实频率或近似 $[3,12,20,40]$ rad/s 时性能退化较小；仅在极端偏离的 $[60,120]$ rad/s 下误差显著增大。证据支持“近似频带可用”，不支持“无需频率先验”。

## 6. 证据边界

- 参考解来自 Newmark-$\beta$，没有实验振动台或实测结构响应验证。
- 所有结构模型保持线性，四层框架还经过降阶；没有非线性恢复力或材料塑性。
- 没有多随机种子的均值/方差，无法判断随机 Fourier 特征初始化的统计稳定性。
- “实际工程就绪”主要由数值基准支持，仍缺完整尺寸、高维和现场噪声检验。

## 关联页面
- [[du2026-hcff-pinn-analysis]] — 论文概述
- [[du2026-hcff-pinn-critical]] — 局限与机会
- [[hcff-pinn]] — HCFF-PINN 实体
- [[at-pinn-hc]] — 硬约束结构振动对照方法

## Evidence By Source

### `sources/papers/du2026-hcff-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_engappai_2025_113640.xml`, `raw/papers/extracted/10_1016_j_engappai_2025_113640_extracted.txt`

^[sources/papers/du2026-hcff-pinn.md]
