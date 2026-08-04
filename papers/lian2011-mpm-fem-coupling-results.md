---
type: paper-analysis
title: Coupling of finite element method with material point method by local multi-mesh
  contact method
authors:
- Y.P. Lian
- X. Zhang
- Y. Liu
year: 2011
venue: Computer Methods in Applied Mechanics and Engineering
tags:
- domain/computational-mechanics
- evidence/paper
methods:
- CFEMP
- MPM
- FEM
- analytical-solution comparison
- literature-result comparison
- experimental-result comparison
results:
- plate-impact stress
- separation time
- rolling trajectory
- residual velocity
- water-column collapse
failure_modes:
- interface oscillation
- background-grid penetration
- energy error
- no experimental result for FSI case
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--lian2011-mpm-fem-coupling-results
status: active
project: civil-engineering-llm-wiki
keywords:
- computational-mechanics
- material-point-method
- finite-element-method
- coupled-methods
- contact-mechanics
- impact
- fluid-structure-interaction
- numerical-methods
- CFEMP
- MPM
- FEM
- analytical-solution comparison
- literature-result comparison
- experimental-result comparison
- plate-impact stress
- separation time
- rolling trajectory
- residual velocity
- water-column collapse
- interface oscillation
- background-grid penetration
- energy error
- no experimental result for FSI case
- Computer Methods in Applied Mechanics and Engineering
sources:
- sources/papers/lian2011-mpm-fem-coupling.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Results: numerical evidence

^[sources/papers/lian2011-mpm-fem-coupling.md]

方法说明见 [[lian2011-mpm-fem-coupling-method]]；总览与边界见 [[lian2011-mpm-fem-coupling-analysis]]。以下只记录提供文本中由图、表或正文明确报告的实验/数值结果。

## 1. 对称板撞击

两块长度 21 mm、截面 3 × 3 mm 的板以大小相等、方向相反的 100 m/s 速度相撞。两板均采用线弹性材料，`E=6.5×10^3 MPa`、`ν=0`、`ρ=2.75×10^-3 g/mm^3`；FEM 单元尺寸和 MPM 背景网格尺寸均为 0.5 mm，粒子间距为 0.25 mm。一块板用 FEM，另一块用 MPM（第 5.1 节；图 4）。

在 `t=3.0 μs` 的应力剖面中，CFEMP 与一维解析解总体一致。接口附近 MPM 区域出现局部剖面突起，正文将其归因于 MPM 与 FEM 离散不对称，并指出影响局限于局部区域；MPM 区域还出现 FEM 区域没有的振荡（图 5）。

表 1 报告：

| 方法 | FEM 单元数 | MPM 粒子数 | 到 15 μs 的时间步数 | CPU cost/s | 分离时间/μs |
|---|---:|---:|---:|---:|---:|
| Analytical | — | — | — | — | 8.63 |
| CFEMP | 1,512 | 12,096 | 695 | 50 | 8.7 |
| MPM | — | 24,192 | 695 | 97 | 8.7 |

正文据此报告，CFEMP 的分离时间与解析解一致，并且该设置下计算成本低于全 MPM。

尺寸比敏感性分析固定 MPM 网格尺寸为 0.5 mm，将 FEM 单元尺寸从 0.25 mm 增加到 1.5 mm。图 6 报告：`R<2` 时数值结果与解析结果吻合较好；`R>2` 时 MPM 区域出现显著振荡；`R>1` 时观察到由于网格不匹配导致的穿透。

对相同板撞击再使用各向同性硬化弹塑性材料（`E=6.5×10^3 MPa`、切线模量 `E_T=3.0×10^3 MPa`、屈服应力 300 MPa、`R=1`），图 7 显示数值结果接近一维解析解，并能表现弹性波和塑性波同时传播的双波结构（第 5.1 节）。

## 2. 非对称弹性板撞击

较长板尺寸为 3 × 3 × 42 mm，由 FEM 模拟，`E=6.5×10^3 MPa`、`ρ=2.75×10^-3 g/mm^3`；较短板尺寸为 3 × 3 × 21 mm，由 MPM 模拟，`E=32.5×10^3 MPa`、`ρ=5.5×10^-3 g/mm^3`。两者声速相差约两倍但阻抗匹配，`R=1`。

图 8(a) 在 `t=3.6 μs` 对比 CFEMP、全 MPM 与解析解；正文报告 CFEMP 结果与解析解一致。表 2 报告：

| 方法 | FEM 单元数 | MPM 粒子数 | 到 20 μs 的时间步数 | CPU cost/s | 分离时间/μs |
|---|---:|---:|---:|---:|---:|
| Analytical | — | — | — | — | 17.28 |
| CFEMP | 3,024 | 12,096 | 2,756 | 212 | 17.3 |
| MPM | — | 36,288 | 2,777 | 582 | 17.3 |

该表给出的分离时间与解析值一致；在此离散设置下，CFEMP 的 CPU cost 低于全 MPM（图 8、表 2）。

## 3. 斜板上的球滚动

弹性球半径为 1.6 m，弹性板尺寸为 20 × 4 × 0.8 m，重力为 10 g/s²。板底固定，板用 FEM，球用 MPM；单元尺寸和网格尺寸为 0.2 m，粒子间距为 0.1 m。球 `E=4.2×10^6 Pa`、`ν=0.4`、`ρ=1000 kg/m^3`；板 `E=4.2×10^7 Pa`、`ν=0.4`、`ρ=10000 kg/m^3`（第 5.3 节；图 9、10）。

四个工况为：`(θ=π/4, μ=0.1)`、`(π/4,0.4)`、`(π/3,0.2)`、`(π/3,0.6)`。正文按刚体动力学解析式将第 1、3 个工况判为滚动-滑移，其余两个判为滚动-粘着。

图 11 比较质心位置与解析解，四个工况的 CFEMP 数值结果均报告为与解析结果吻合。表 3 给出第 1 个工况到 2.0 ms 的成本：

| 方法 | FEM 单元数 | MPM 粒子数 | 时间步数 | CPU cost/s |
|---|---:|---:|---:|---:|
| CFEMP | 8,000 | 17,259 | 3,391 | 144 |
| MPM | — | 81,259 | 3,622 | 456 |

图 12 给出了第 1、2 个工况的能量演化曲线；正文报告该例中 CFEMP 的 CPU 时间低于全 MPM。

## 4. 厚板穿孔

弹丸以 30° 斜向撞击厚铝板。弹丸长 88.9 mm、直径 12.9 mm、弹头为 3.0 caliber-radius-head；靶板厚 26.3 mm、面积 110 × 110 mm。弹丸使用非结构 FEM 网格和各向同性硬化弹塑性，靶板使用结构化 MPM 网格、Johnson–Cook 强度模型和 Mie–Grüneisen EOS；有效塑性应变达到 `ε_fail=1.6` 时将偏应力分量置零。该例忽略摩擦（第 5.4 节；图 13）。

在打击速度 `v0=575 m/s` 下，表 6 的网格细化结果为：

| Case | 网格尺寸/mm | 靶板粒子数 | 弹丸单元数 | 残余速度/m/s |
|---|---:|---:|---:|---:|
| 1 | 3.0 | 90,593 | 5,440 | 286 |
| 2 | 2.0 | 314,600 | 18,144 | 418 |
| 3 | 1.5 | 756,315 | 42,752 | 433 |
| 4 | 1.0 | 2,516,800 | 145,152 | 456 |
| Experiments | — | — | — | 455 |

正文据此报告残余速度随网格细化向实验值收敛；Case 4 的 456 m/s 接近实验 455 m/s。图 14 对比实验 X-ray 序列与数值过程，正文报告穿孔过程中的弹丸形状一致；图 15 给出最终时刻 0.28 ms 的靶板有效塑性应变，图 16 报告 Case 4 的能量误差不超过 5.5%。

表 7 给出不同打击速度下的弹丸残余速度：

| `v0`/m/s | Experiment | CFEMP | MPM |
|---:|---:|---:|---:|
| 400 | 217 | 229 | 241 |
| 446 | 288 | 293 | 306 |
| 575 | 455 | 456 | 471 |
| 730 | 655 | 631 | 652 |

正文报告 CFEMP 与实验结果接近；CFEMP 残余速度低于全 MPM，但差异不显著。由于该例最小 `R` 小于 1，CFEMP 总成本高于 MPM；不过按时间步计的效率更高。图 17 对 `v0=400 m/s` 的过程给出弹丸形状和弹道与实验数据一致的定性比较。

## 5. 水柱坍塌与弹性障碍物流固耦合

水柱宽 `L=146 mm`、高 `2L`，与宽 12 mm、高 80 mm 的柔性障碍物相距 `L`；水在重力 `g=9.8×10^-3 mm/ms²` 下流动，忽略空气。障碍物用 FEM，`ρ=2.5×10^-3 g/mm^3`、`E=1 MPa`、`ν=0`；水用 MPM、null material model 和 Mie–Grüneisen EOS，并允许 0.006 MPa 的抗拉强度以平滑自由表面。

该问题采用平面应变；粒子间距 2 mm，网格和单元尺寸 4 mm，`R=1`。水有 10,608 个粒子，障碍物有 60 个单元。水的表 8 参数包括 `ρ=1000 kg/m^3`、`c0=1647 m/s` 和 `s=1.921`。

论文明确指出没有可用实验结果，因此改与 PFEM 结果及已有 staggered level-set 结果比较。图 19 中 CFEMP 的障碍物变形和水自由表面与 PFEM 结果吻合；图 20 比较障碍物左上角位移时间历史；图 21 给出该问题的能量曲线（第 5.5 节）。

## 6. 结果范围

上述结果覆盖解析解、已有数值结果和实验数据三类证据，但并不等价于所有工况下的收敛证明。论文未提供公共代码或独立数据集 URL，具体复现状态见 [[lian2011-mpm-fem-coupling-analysis]] 的第 12 维，并参见算法实体 [[entities/lian-local-multimesh-contact]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[lian2011-mpm-fem-coupling-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
