---
type: paper-analysis
title: Beam elements with frictional contact in the material point method
authors:
- Jingu Kang
- Michael A. Homel
- Eric B. Herbold
year: 2022
venue: International Journal for Numerical Methods in Engineering
doi: 10.1002/nme.6886
tags:
- domain/computational-mechanics
- evidence/paper
methods:
- CPDI2
- beam-particle
- multi-velocity-field-contact
- Coulomb-friction
- Euler-Bernoulli
- Timoshenko
- explicit-time-integration
results:
- analytical-validation
- finite-element-comparison
- dynamic-contact
- fiber-mixing
failure_modes:
- contact-gap
- grid-resolution-dependence
- no-angular-momentum-contact
- small-strain-beam-constitutive-assumption
datasets:
- paper-defined-numerical-benchmarks
reproducibility: medium
code_url: []
dataset_url: []
id: paper--kang2022-beam-contact-mpm-method
status: active
project: civil-engineering-llm-wiki
keywords:
- computational-mechanics
- material-point-method
- contact-mechanics
- friction
- beam-elements
- large-deformation
- numerical-methods
- coupled-methods
- reproducibility
- CPDI2
- beam-particle
- multi-velocity-field-contact
- Coulomb-friction
- Euler-Bernoulli
- Timoshenko
- explicit-time-integration
- analytical-validation
- finite-element-comparison
- dynamic-contact
- fiber-mixing
- contact-gap
- grid-resolution-dependence
- no-angular-momentum-contact
- small-strain-beam-constitutive-assumption
- paper-defined-numerical-benchmarks
- International Journal for Numerical Methods in Engineering
sources:
- sources/papers/kang2022-beam-contact-mpm.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Method：MPM beam particle 与 frictional contact

^[sources/papers/kang2022-beam-contact-mpm.md]

> 本页展开论文第 2–3 节的方法机制。证据来自预提取文本的第 3–13 页；原文 DOI：[10.1002/nme.6886](https://doi.org/10.1002/nme.6886)。总览见 [[kang2022-beam-contact-mpm-analysis]]，算法实体见 [[entities/kang-beam-particle]]。

## 1. 计算框架：CPDI2 MPM

MPM 将固体离散为带历史变量的 Lagrangian material points，并在固定 Eulerian background grid 上求解运动方程。一个时间步的基本顺序是：

1. 把粒子中心的质量、速度和其他场量映射到网格；
2. 在网格上组装内力、外力并求解平动加速度；
3. 用接触算法修改网格速度/加速度；
4. 把更新后的网格量映射回粒子；
5. 更新粒子位置、粒子域和历史变量，然后重置网格。

本文采用二阶 convected particle domain interpolation，即 CPDI2。粒子域在二维中用四边形、三维中用六面体顶点显式跟踪，而不是把粒子仅当作无尺寸点。网格形函数和其梯度在粒子域上积分，再由粒子域顶点的形函数值近似，从而改善 cell-crossing instability 和网格力积分精度（第 3–5 页）。

对 CPDI2 固体，粒子质量和速度由域积分形函数映射到网格；网格加速度由 lumped mass 下的力平衡计算。更新后的网格速度插值回粒子和粒子顶点，顶点位置给出新的粒子域。变形梯度可由速度梯度更新，也可由粒子域顶点位移按一点评分的有限元方式得到。

文中 CPDI2 对照固体使用 updated-Lagrangian neo-Hookean 模型计算 Cauchy stress。作者同时指出，CPDI2 在高度变形、材料失强后可能产生奇异变形梯度，此时需要流体型本构或切换到其他权函数；这不是新 beam particle 的接触算法本身。

## 2. Beam particle 的状态与几何

### 2.1 两端节点

一条曲梁被分段为有限个直的 Lagrangian beam particles。每个 beam particle 的中性轴在变形过程中沿两个端节点的连线；因此它是局部线性、整体可大转动的 reduced-order 单元。

每个粒子包括：

- 质心位置 `x_b` 与质心刚体转动；
- lumped mass 和关于主轴的 mass moment of inertia；
- 质心平移速度 `v_b`、角速度 `ω_b`；
- 局部正交基/方向余弦；
- 两个端节点，每个端节点 3 个平移 DOF 和 3 个转动 DOF。

端点位置控制轴向变形；端点转角控制曲率和弯曲。该设计把结构运动学从“许多体积粒子”压缩为两端节点 + 截面参数。

### 2.2 端点到背景网格的映射

梁粒子质量和线动量映射为：

\[
m_g=\sum_b S_{gb}m_b,\qquad
m_g v_g=\sum_b S_{gb}m_b v_b .
\]

其中论文给出的 beam-particle alternative basis function 为两端点传统六面体网格形函数的平均：

\[
S_{gb}=\frac{1}{2}S_g(x_I)+\frac{1}{2}S_g(x_J),
\]

`x_I`、`x_J` 是两个端点。端点的网格插值沿用 CPDI2 的形函数，避免把粒子域强行切分在网格单元边界，并帮助维持相邻梁粒子的连接性（第 7 页，Eq. 17）。

## 3. 角速度场与转动更新

这是新梁粒子与普通 MPM 平动粒子的关键区别。论文在背景网格节点引入角速度 `ω_g` 和角加速度 `α_g`，并以惯性加权方式映射梁粒子的转动状态：

\[
I_g=\sum_b S_{gb}I_b,\qquad
I_g\omega_g=\sum_b S_{gb}I_b\omega_b .
\]

梁粒子在全局坐标下的惯性张量由局部惯性张量和正交变换矩阵 `T` 给出：

\[
I_b=T^{\mathsf T}\,\bar I_b\,T .
\]

在本文的直梁、恒定截面假设下，局部惯性张量只使用主轴对角项。圆截面例子给出了关于局部轴的主惯性表达式；一般截面可以通过对截面/多面体积分获得（第 7–8 页）。

网格上先由力矩平衡求 `α_g`，再更新 `ω_g`。梁粒子角速度由网格角加速度插值更新；两个端点的增量转角由端点处的网格角速度积分得到。质心刚体转动同样由网格角速度积分，并用其构造增量旋转矩阵，更新局部正交基。

## 4. 力、力矩和梁本构

梁端点的内力和内力矩直接映射到网格节点。对每个时间步，梁粒子的内力/力矩采用增量更新：

\[
\begin{bmatrix}
\Delta f^{\mathrm{int}}\\
\Delta M^{\mathrm{int}}
\end{bmatrix}
=T^{\mathsf T}k_pT
\begin{bmatrix}
\Delta x\\
\Delta\theta
\end{bmatrix},
\]

其中 `k_p` 是局部切线刚度矩阵，`Δx` 和 `Δθ` 是端点平移/转动增量。`k_p` 可采用常规 Euler–Bernoulli frame stiffness 或 Timoshenko beam stiffness；截面二次矩、极惯性矩、面积和剪切系数等传统结构参数直接进入刚度。

论文明确限定：该 beam particle 针对大位移、大转动，但粒子域为小应变；初始长度、面积和惯性张量在仿真中保持常数。作者认为适当扩展切线刚度后可描述非线性材料，但本文没有给出这一扩展的数值示范。

## 5. 一个不含接触的梁粒子时间步

论文在第 9 页给出八步算法，可压缩为：

```text
initialize grid: m_g, I_g, v_g, ω_g, a_g, α_g, f_g, M_g
map beam particles: m_b, I_b, v_b, ω_b -> grid
assemble beam internal/external forces and moments
solve translational and angular accelerations on grid
update grid v_g and ω_g
interpolate grid accelerations to v_b and ω_b
map grid velocities to both endpoints; update x_I, x_J and endpoint rotations
update beam internal forces and moments through k_p
```

更新后的两个端点还可重新计算梁粒子的质心。局部基向量随质心刚体旋转更新，因而梁粒子的截面方向和惯性张量随姿态变化。

## 6. CPDI2 固体的多速度场接触

为处理两个或更多材料组，MPM 为每个材料组维护独立速度场，但仍映射到同一网格节点。对于网格节点 `g` 上的速度场 `α`，由质量梯度构造外法向：

\[
n_g^\alpha=\frac{\sum_p \nabla S_{gp}m_p^\alpha}
{\left\mid\sum_p \nabla S_{gp}m_p^\alpha\right\mid}.
\]

两场接触对的质量加权法向和质心速度分别由文中 Eqs. 35–36 给出。接触力分解为法向和切向分量，切向力按 Coulomb 上限截断：

\[
f_g^{\mathrm{ct}}
=f_g^{\mathrm{nor}}n_g
+\min(\mu|f_g^{\mathrm{nor}}|,|f_g^{\mathrm{tan}}|)
\operatorname{sgn}(f_g^{\mathrm{tan}})s_g .
\]

接触力被除以对应材料场的网格质量，作为接触加速度，再修改网格速度。文中强调，通常不需要昂贵的显式邻域搜索；接触对由共享网格节点上的多个速度场确定。

## 7. Beam particle 的空间接触

### 7.1 Spatial nodes

普通梁是非体积对象，直接从中性轴检测碰撞会丢失截面范围。论文在梁粒子边缘布置 spatial nodes：矩形截面在两端各放置四个边缘节点，共八个节点构成该梁粒子的空间几何；端部中心节点位于截面中心。空间节点把梁的截面尺寸带入接触检测，并允许梁与梁、实体或流体粒子进行接触。

### 7.2 空间节点速度

空间节点的动力学仍由两个端节点决定，因而空间节点速度不是独立自由度。算法先用未计入接触的加速度计算质心试探速度：

\[
v_b^{\mathrm{trial}}=v_b^n+\sum_gS_{gb}a_g\Delta t .
\]

矩形截面直接使用 CPDI2 alternative shape function 将试探梁速度映射到空间节点。圆截面等其他形状则使用权函数 `W_\xi(x_\xi)`：

\[
m_g=\sum_b\sum_\xi S_g(x_\xi)W_\xi(x_\xi)m_b,
\]

\[
v_g=\frac{1}{m_g}\sum_b\sum_\xi S_g(x_\xi)W_\xi(x_\xi)m_bv_b^{\mathrm{trial}}.
\]

当截面恒定时，论文将权函数简单取为一个梁粒子 spatial nodes 总数的倒数。

### 7.3 接触插入位置

空间接触被插入梁粒子基本算法的网格加速度/速度更新阶段：

1. 计算接触前的 `v_b^{trial}`；
2. 把空间节点关联的质量和速度映射到背景网格；
3. 用多速度场算法计算 `f_g^{ct}`；
4. 把接触加速度加入网格加速度/速度；
5. 将接触后的网格加速度插值回梁粒子，并按端点映射更新端点位置。

这样，梁粒子与 CPDI2 实体粒子使用同一套网格接触力更新，但梁的转动字段只通过其结构更新链路演化。

## 8. 时间积分与梁理论

所有数值结果采用 explicit time integration。除厚梁算例外，论文采用 Euler–Bernoulli 梁理论；厚梁算例采用 Timoshenko 梁理论以计入剪切变形。时间步约按

\[
\Delta t\approx0.4l_g\sqrt{\frac{\rho_0}{E}}
\]

设置，其中 `l_g` 是背景网格单元尺寸，`E` 是弹性模量，`ρ_0` 是初始密度（第 13 页）。

## 9. 设计假设与实现边界

- beam particle 初始为直线段；曲梁由多个直梁粒子分段逼近。
- 梁粒子在大位移/大转动下仍采用小应变结构本构。
- 质量、初始长度、截面面积和惯性张量按论文描述在模拟期间保持常数。
- friction contact 只在平动速度层面计算，不把角动量场纳入接触冲量。
- 网格尺寸、梁直径和多速度场接触的 gap 之间存在直接耦合；空间节点减轻了“接触发生在梁内部”的问题，但没有消除 gap。

方法的逐步结果证据见 [[kang2022-beam-contact-mpm-results]]；局限与迁移边界见 [[kang2022-beam-contact-mpm-critical]]。

## 10. 可复现性相关实现信息

论文公开了核心公式、算法步骤、所用梁理论、主要材料参数、背景网格/粒子数和图示时间点；数据声明称大部分结果数据已在文章中给出，其他数据可向通讯作者合理请求。提供文本没有公开代码或数据仓库 URL，因此本页不填入任何猜测链接：`code_url: []`、`dataset_url: []`，复现等级为 `medium`。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[kang2022-beam-contact-mpm-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
