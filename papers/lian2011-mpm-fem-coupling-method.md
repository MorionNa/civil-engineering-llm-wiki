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
- local multi-mesh contact coupling
- central difference time integration
- 8-node hexahedral FEM
- MPM background-grid mapping
- Coulomb friction
- hourglass control
results:
- interface momentum transfer
- impenetrability enforcement
- frictional contact
failure_modes:
- mesh-ratio mismatch
- early contact from background grid
- time-step restriction
- interface disturbance
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--lian2011-mpm-fem-coupling-method
status: active
project: civil-engineering-llm-wiki
keywords:
- computational-mechanics
- material-point-method
- finite-element-method
- coupled-methods
- contact-mechanics
- large-deformation
- friction
- numerical-methods
- local multi-mesh contact coupling
- central difference time integration
- 8-node hexahedral FEM
- MPM background-grid mapping
- Coulomb friction
- hourglass control
- interface momentum transfer
- impenetrability enforcement
- frictional contact
- mesh-ratio mismatch
- early contact from background grid
- time-step restriction
- interface disturbance
- Computer Methods in Applied Mechanics and Engineering
sources:
- sources/papers/lian2011-mpm-fem-coupling.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Method: local multi-mesh contact coupling

^[sources/papers/lian2011-mpm-fem-coupling.md]

关联概览：[[lian2011-mpm-fem-coupling-analysis]]；算法实体：[[entities/lian-local-multimesh-contact]]。

## 1. 离散分工与状态变量

论文将轻微变形的物体记为 `X_F`，使用 FEM；将极端变形的物体记为 `X_M`，使用 MPM。两者都在显式中心差分框架中推进，但状态变量的位置不同：

- MPM 以拉格朗日 material points 携带质量、位置、速度、应力、历史变量等；Eulerian 背景网格只在当前时间步积分动量方程。
- FEM 使用 8 节点六面体单元；材料场由单元积分点/中心计算，并保留 FE 节点的动量和速度。
- FEM 接触界面上对公共背景网格有贡献的节点称为 hybrid nodes。它们在接触计算阶段按粒子式方式映射到背景网格，但随后仍作为 FEM 节点更新。

两种离散使用相同形式的 8 点六面体形函数。MPM 粒子质量通过

\[
m_I=\sum_p m_p N_{Ip}
\]

映射到网格点，粒子动量通过

\[
p_{iI}=\sum_p N_{Ip}m_p v_{ip}
\]

映射。FEM 方面，单元弱式产生节点内力、外力以及用于抑制一点评分积分 hourglass mode 的阻力；论文实现 standard 和 Flanagan–Belytschko 两种 hourglass control。

## 2. 一个时间步的总体结构

每个时间步先把 MPM 体与 FEM 体当作不接触，分别得到 trial nodal variables；当两者在同一背景网格点有质量/动量贡献时，再执行接触检测和接触动量修正。

论文给出的实现顺序为：

1. 初始化规则背景网格。
2. 遍历 MPM 粒子，计算其对网格质量 `m_I` 和半步动量 `p_I^{k+1/2}` 的贡献。
3. 遍历 FEM 表面节点，计算其对 `m_I^r` 和 `p_I^{r,k+1/2}` 的贡献。
4. 施加边界条件。
5. 遍历网格点检测接触，并把贡献到接触点的 FE 节点标为 hybrid nodes。
6. 用法向接触力的第一项调整 MPM 网格动量和 FEM hybrid-node 速度。
7. 用调整后的速度计算两种离散的增量应变和自旋，并更新应力、密度、压力和本构状态。
8. 计算 MPM 粒子内力/外力以及 FEM 单元内力/外力/hourglass 力，并把 hybrid-node 力映射回网格。
9. 计算法向接触力的第二项和切向 Coulomb 接触力。
10. 更新背景网格动量，再由网格更新 MPM 粒子速度/位置；同时更新普通 FE 节点和 hybrid nodes 的速度/位置。
11. 丢弃变形背景网格，重建下一时间步的规则网格。

## 3. 时间积分与临界步长

MPM 和 FEM 均使用中心差分。对 MPM 域，网格半步动量按

\[
p_{iI}^{k+1/2}=p_{iI}^{k-1/2}+f_{iI}^{k}\Delta t^k
\]

更新，随后粒子速度和位置从网格力、动量和形函数得到。FEM 普通节点按节点力/节点质量更新；hybrid nodes 则使用背景网格贡献加上 FEM hourglass resisting force 更新。

临界步长按论文给出的尺度估计

\[
\Delta t=\min\left(\frac{L_e}{c}\right),
\]

其中 `L_e` 是 MPM 网格单元或 FEM 单元的特征长度，`c` 是材料局部声速。为了让两个子域同步，使用 FEM 与 MPM 临界步长的最小值；论文建议 FEM 的特征长度不小于 MPM 网格特征长度，使步长主要受 MPM 域控制。强冲击时还加入人工体积黏性：压缩时由线性和二次速度散度项给出，膨胀时取零。

## 4. 接触检测

在背景网格点 `I`，分别计算两个物体的速度

\[
v_{iI}^{b,k+1/2}=\frac{p_{iI}^{b,k+1/2}}{m_I^b},\qquad b\in\{r,s\},
\]

其中 `r` 表示 FEM 体，`s` 表示 MPM 体。论文的基本接触判据是相对速度沿 FEM 体外法向为正：

\[
\left(v_{iI}^{r,k+1/2}-v_{iI}^{s,k+1/2}\right)n_{iI}^{r,k}>0.
\]

FEM 法向 `n^r` 由接触网格点所关联的单元面法向求和；MPM 体因为质量集中在粒子上，使用网格点的粒子质量梯度近似外法向：

\[
n_{iI}^{s,k}\approx\sum_p N_{Ip,i}^{k}m_p.
\]

仅使用同一网格点和相对速度会使接触在真实接触前发生：论文指出当两物体间距离小于约两个网格单元尺寸时可能过早接触。因此实现中采用 Ma 等人改进的检测方法，并额外检查两物体的真实物理距离是否小于预设阈值。

## 5. 法向接触力

设接触点的 trial 半步动量为

\[
\bar p_{iI}^{b,k+1/2}=p_{iI}^{b,k+1/2}+\Delta t^k f_{iI}^{b,k}.
\]

加上接触力后，动量为

\[
p_{iI}^{b,k+1/2}=\bar p_{iI}^{b,k+1/2}+\Delta t^k f_{iI}^{b,c,k}.
\]

不可穿透约束要求相对动量在法向上的分量为零：

\[
\left(m_I^s p_{iI}^{r,k+1/2}-m_I^r p_{iI}^{s,k+1/2}\right)n_{iI}^{r,k}=0.
\]

由此求得法向力 `f_I^{nor,k}`，论文将它分为两项：

- `f_I^{nor,k;1}` 由当前半步动量违反不可穿透条件的程度决定，用于先行调整 MPM 动量和 FEM hybrid-node 速度。
- `f_I^{nor,k;2}` 由两个物体的 trial 节点力决定，在网格动量更新时加入。

两物体的接触力方向相反。对 MPM 体，第一项动量修正写为

\[
\tilde p_{iI}^{s,k+1/2}=p_{iI}^{s,k+1/2}+\Delta t^k f_I^{nor,k;1}n_{iI}^{s,k},
\]

FEM hybrid nodes 则按其对网格点的形函数贡献获得相应速度修正。这样，应力更新使用的速度满足同一网格点上的不可穿透约束，避免网格重建造成的人工扰动。

## 6. 切向接触与摩擦

若采用 stick 接触，论文用相对速度的切向投影构造单位切向向量 `t_I`，并令接触后相对切向动量为零，由此得到粘着力 `f_I^{stick}`。

实际滑移接触采用 Coulomb 模型：

\[
f_I^{tan}=\min\left(\mu f_I^{nor}, f_I^{stick}\right),
\]

其中 `μ` 是摩擦系数。最终施加到物体 `b` 的网格点接触力为

\[
f_{iI}^{b,c}=f_I^{nor}n_{iI}^{b}+f_I^{tan}t_{iI}^{b}.
\]

因此算法在一个统一接口中同时处理不可穿透、粘着和滑移；穿孔算例则明确将弹丸与靶板间摩擦设为忽略。

## 7. 应力更新

半步速度修正后，MPM 粒子和 FEM 单元分别计算增量应变与自旋。应力采用

\[
\sigma_{ij}^{k+1}=\sigma_{ij}^{k}+\dot{\sigma}_{ij}^{k+1/2}\Delta t^{k+1/2},
\]

其中应力率由 Jaumann（共转）应力率和自旋张量组合：

\[
\dot\sigma_{ij}=\overset{\circ}{\sigma}_{ij}-\sigma_{ik}\Omega_{jk}-\sigma_{jk}\Omega_{ik}.
\]

FEM 单元中心使用形函数导数和 FE 节点速度计算应变率/自旋；MPM 粒子使用背景网格形函数导数和调整后的网格速度计算。偏应力由本构律更新，压力由状态方程（EOS）更新；密度依据体积应变增量更新。

## 8. 方法边界

论文方法依赖规则 MPM 背景网格、8 节点六面体形函数、显式中心差分和接触网格点上的局部投影。图 6 的敏感性分析显示，FEM 单元尺寸与 MPM 网格单元尺寸的比值 `R` 过大时，接口不匹配会放大振荡；文本报告 `R>1` 时可见穿透，`R>2` 时出现显著振荡。

论文未披露 MPM3D 的公共代码 URL，也未提供独立数据集；因此这里的机制描述可支持重实现，但不能声称已有开箱即用的复现实例。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[lian2011-mpm-fem-coupling-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
