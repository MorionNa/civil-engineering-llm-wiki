---
type: paper-analysis
title: An implicit gradient-enhanced microplane damage material model in the coupled
  implicit MPM-FEM
authors:
- Osvaldo Andres Oropeza-Navarro
- Ahmad Chihadeh
- Jakob Platen
- Michael Kaliske
year: 2024
venue: Computers and Structures
tags:
- domain/computational-mechanics
- evidence/paper
methods:
- material-point-method
- finite-element-method
- coupled-methods
- microplane
- gradient-enhanced
- damage-mechanics
- large-deformation
- numerical-methods
results:
- coupled-methods
- damage-mechanics
- numerical-methods
- large-deformation
- fracture
failure_modes:
- numerical-methods
- damage-mechanics
- large-deformation
- coupled-methods
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--oropeza-navarro2024-microplane-damage-results
status: active
project: civil-engineering-llm-wiki
keywords:
- computational-mechanics
- material-point-method
- finite-element-method
- coupled-methods
- large-deformation
- damage-mechanics
- microplane
- gradient-enhanced
- numerical-methods
- reproducibility
- fracture
- Computers and Structures
sources:
- sources/papers/oropeza-navarro2024-microplane-damage.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Results — numerical evidence from the coupled implicit MPM-FEM

^[sources/papers/oropeza-navarro2024-microplane-damage.md]

本页只记录论文文本明确报告的实验/数值设置、图表和观察，不把定性接近改写成未报告的误差数字。方法推导见 [[oropeza-navarro2024-microplane-damage-method]]，总览见 [[oropeza-navarro2024-microplane-damage-analysis]]。

## 1. 结果范围与参照

论文第 7 节给出三个数值例子：

| 例子 | 目的 | 参照 |
|---|---|---|
| 缺口拉伸试验 | 检验非局部 bond 对不同界面配置的作用 | 独立 FEM 与 MPM |
| 悬臂构件 | 检验有限变形、纤维初始各向异性和加载循环 | FEM |
| L 形混凝土试件 | 检验微平面损伤、软化和裂纹图样 | Winkler et al. 实验数据与 FEM |

论文没有报告统一的数值误差指标、置信区间或统计重复试验；以下数值均是原文的模型参数、离散参数或加载参数。

## 2. 缺口拉伸试验

### 2.1 设置

这是无纤维、缺口试件的准静态拉伸。两种耦合配置为：

- MPM-FEM_1：下部为材料点，上部为有限元；
- MPM-FEM_2：左侧为材料点，右侧为有限元。

试件顶部施加 50.0 mm 位移，共 50 个载荷步；线性四边形有限元和背景网格尺寸均为 \(5\times5\) mm²，每个背景网格单元内放置 \(2\times2\) 个材料点（PDF p. 9，Fig. 4）。

### 2.2 Table 1 参数

| 类别 | 参数 | 数值 |
|---|---|---:|
| 弹性 | \(K\) | 5,208.00 MPa |
| 弹性 | \(G\) | 4,237.00 MPa |
| 弹性 | \(\nu\) | 0.18 |
| 损伤 | \(\gamma_0\) | \(2.05\times10^{-2}\) |
| 损伤 | \(k_r\) | 2 |
| 损伤 | \(\alpha\) | 0.8 |
| 损伤 | \(\omega\) | 2.0 |
| 梯度 | \(c\) | 400 |

### 2.3 图表报告

- Fig. 5 的不同载荷步损伤演化显示，两种 MPM-FEM 配置与独立 FEM、MPM 参照的损伤演化“nearly the same”。
- Fig. 6 比较纯机械 bond 与本文 nonlocal bond。没有 nonlocal bond 时，MPM-FEM_1 的下部发生应变局部化并产生非物理结果。
- 对 MPM-FEM_2，论文报告两种 bond 的损伤演化差异不明显；作者将其归因于该特定配置的边界条件、对称性和失效模式。
- Fig. 7 中，使用 nonlocal bond 的两种 MPM-FEM 配置，其反力–位移关系接近独立 MPM 和 FEM 参照。
- Fig. 7 还显示，仅使用机械 bond 时，MPM-FEM_2 明显偏离参照；论文将其归因于非局部场未被连接后，损伤起始区域发生应变局部化。

## 3. 悬臂构件

### 3.1 设置

悬臂构件下部与固定支座连接，材料含沿构件纵轴方向的纤维，因此具有初始各向异性。顶部施加 Fig. 8b 所示的侧向位移函数。

模拟分为 120 个时间步，\(\Delta t=0.1\) s，Newmark 参数 \(\beta=0.5\)。线性六面体有限元和背景网格尺寸为 \(0.25\times0.25\times0.25\) mm³，每个网格单元内有 \(2\times2\times2\) 个材料点（PDF p. 9，Fig. 8）。

### 3.2 Table 2 参数

| 类别 | 参数 | 数值 |
|---|---|---:|
| 砂浆基体 | \(K\) | 17,222.22 MPa |
| 砂浆基体 | \(G\) | 12,916.67 MPa |
| 砂浆基体 | \(\nu\) | 0.2 |
| 纤维 | \(e_{mic}\) | 1,000.00 MPa |
| 纤维 | \(f_{mic}\) | 0 MPa |
| 纤维方向 | \(\mathbf A\) | \{0.0, 0.0, 1.0\} mm |
| 纤维方向 | \(\mathbf A\perp\mathbf B\) | 满足 |
| 损伤 | \(\gamma_0\) | \(1.0\times10^{-3}\) |
| 损伤 | \(k_r\) | 1 |
| 损伤 | \(\alpha\) | 0.9 |
| 损伤 | \(\omega\) | 100 |
| 梯度 | \(c\) | 2 |

### 3.3 图表报告

- Fig. 9 将 \(x\) 方向反力–位移曲线与 FEM 参照比较。论文报告：nonlocal bond 的连续红线在有限变形加载循环下保持可靠；纯机械耦合在达到损伤阈值后开始偏离参照。
- 曲线阶段被描述为：A–B 初始弹性；B–C 损伤起始并软化；C–D–E 卸载–再加载的弹性响应；E–F 由于纤维更趋向外载方向而出现载荷增加。
- Fig. 10 跟踪初始坐标为 \{5.9375, 1.4375, 4.9375\} mm 的材料点在 \(x-z\) 平面上的位移。论文报告该材料点在卸载和再加载时不处于完全相同的位置，纯机械耦合时差异更明显。
- Fig. 11 报告上部悬臂中纤维方向随外载的演化。
- E–F 区域的振荡被论文归因于：基体达到最大损伤值导致刚度大幅下降，以及每个时间步纤维逐渐对齐外力而产生相对前一步的刚度跳变。
- Fig. 12 的两个时间步损伤演化显示，本文耦合结果与 FEM 参照具有良好相关；纯机械耦合则在损伤起始区域产生局部化并给出不正确结果。

## 4. L 形混凝土试件

### 4.1 设置

该例子是用于混凝土裂纹扩展研究的准静态 L 形试件，实验数据取自 Winkler et al. [28]。内区使用 8,800 个材料点和 \(2.5\times2.5\) mm² 背景网格，每个背景单元有 \(2\times2\) 个材料点；外区使用尺寸为 \(2.5\times2.5\) mm² 的线性四边形有限元。

试件底部固定，在指定位置施加 1.0 mm 位移，共 500 个载荷步（PDF p. 11，Fig. 13）。

### 4.2 Table 3 参数

| 类别 | 参数 | 数值 |
|---|---|---:|
| 弹性 | \(K\) | 9,375.00 MPa |
| 弹性 | \(G\) | 7,627.00 MPa |
| 弹性 | \(\nu\) | 0.18 |
| 损伤 | \(\gamma_0\) | \(1.95\times10^{-4}\) |
| 损伤 | \(k_r\) | 10 |
| 损伤 | \(\alpha\) | 0.965 |
| 损伤 | \(\omega\) | 300 |
| 梯度 | \(c\) | 5 |

论文称这些材料参数被选择为拟合实验结果；文本没有进一步披露参数搜索过程。

### 4.3 图表报告

- Fig. 14a 的力–位移特性与实验结果和 FEM 参照一致；论文据此认为耦合隐式 MPM-FEM 能描述应变软化。
- Fig. 14b 给出 Fig. 14a 中 A、B 两点的收敛率。B 是软化阶段最差的收敛载荷步；论文报告非线性解呈二次收敛，并据此认为推导、实现和线性化是正确的。
- Fig. 15a 是实验裂纹图样，Fig. 15b 是模拟预测的损伤区。论文报告两者在位置和演化方面具有良好相关。
- 论文没有在文本中给出裂纹路径误差、力–位移误差、收敛迭代次数或网格收敛表，因此这些量无法从提供文本确认。

## 5. 结果边界

论文的证据支持：nonlocal bond 能在所选三类示例中传递非局部场，并改善某些配置下的局部化、力–位移和损伤区表现。证据不支持：在所有材料、所有 penalty、所有网格或所有界面方向下都无条件稳定，也不支持纤维破坏已经被建模。

更详细的贡献、失败边界和后续问题见 [[oropeza-navarro2024-microplane-damage-critical]]；实体模型页见 [[entities/oropeza-microplane-damage]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[oropeza-navarro2024-microplane-damage-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
