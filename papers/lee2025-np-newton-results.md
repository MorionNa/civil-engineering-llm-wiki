---
id: papers--lee2025-np-newton-results
title: Lee et al. (2025) — NP-Newton 结果证据
type: paper-analysis
status: verified
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
- method/evaluation
- method/neural-operator
keywords:
- wall-clock
- iteration-count
- hyperelasticity
- nonlinear-Poisson
sources:
- sources/papers/lee2025-np-newton.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
reproducibility: medium
code_url: []
dataset_url: []
---

# NP-Newton 结果证据

## 非线性 Poisson

| 网格/工况 | 基线 | NP-Newton | 墙钟变化 |
|---|---:|---:|---:|
| 粗网格 Case I | 14 次 / 0.0710 s | 6 次 / 0.0671 s | 约 1.06× |
| 粗网格 Case II | 14 次 / 0.0795 s | 2 次 / 0.0336 s | 约 2.37× |
| 细网格 Case I | 14 次 / 0.5435 s | 4 次 / 0.2768 s | 约 1.96× |
| 细网格 Case II | 13 次 / 0.5030 s | 2 次 / 0.1575 s | 约 3.19× |
| Case III 强/高频 forcing | Newton-LS 发散 | 3–4 次收敛 | 只证明该基准鲁棒性 |

训练在 1,089 DOF 粗网格完成，细网格为 16,641 DOF。

## Neo-Hookean 超弹性

| 网格/工况 | 对照 | NP-Newton-TR | 解释 |
|---|---:|---:|---|
| 粗网格小变形 | Newton-LS 5 次 / 0.0596 s | NP-Newton-LS 3 次 / 0.0901 s | 负加速 |
| 细网格小变形 | Newton-LS 6 次 / 0.2114 s | NP-Newton-LS 3 次 / 0.2258 s | 负加速 |
| 粗网格大变形 | Newton-TR 107 次 / 1.2541 s | 6 次 / 0.1797 s | 约 6.98× 更快 |
| 细网格大变形 | Newton-TR 207 次 / 6.9841 s | 8 次 / 0.5676 s | 约 12.30× 更快 |

增量加载 IC-Newton-LS 在大变形粗/细网格分别为 42 次/0.5160 s 与 44 次/1.6192 s，仍慢于 NP-Newton-TR。训练网格为 1,029 DOF，细网格为 3,932 DOF。

## 训练成本

| 问题 | 初值数 | 训练/验证样本 | Epoch | 训练时间 | 验证相对 L2 |
|---|---:|---:|---:|---:|---:|
| 非线性 Poisson | 3,150 | 10,658 / 1,185 | 1,921 | 0.62 h | 0.6% |
| 超弹性 | 2,000 | 46,257 / 5,140 | 3,293 | 4.12 h | 0.1% |

硬件为 AMD EPYC 9554、256 GB、NVIDIA L40S 48 GB。论文说明 Python 路径未编译且未调参。

## 不能外推的结论

- 这些时间不是 OpenSeesPy，也不是动态时程。
- 论文报告的“speed-up %”使用 ((t_mathrm{base}/t_mathrm{new}-1)	imes100%)；本页同时给出更直观的时间比。
- 训练时间不包含为生成 Newton 轨迹与收敛解所付出的离线求解器成本。
- 未报告结构响应 (u/v/a/F) 的 R²，因此不能直接进入 [[current-structural-pinn-ranking-2026-08-03]]。

- 数值证据须与 [[lee2025-np-newton-method]] 的原方程验收机制一并理解。

## Evidence By Source

^[sources/papers/lee2025-np-newton.md]

