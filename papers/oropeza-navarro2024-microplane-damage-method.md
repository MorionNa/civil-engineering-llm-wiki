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
id: paper--oropeza-navarro2024-microplane-damage-method
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
# Method — implicit gradient-enhanced microplane damage in coupled implicit MPM-FEM

^[sources/papers/oropeza-navarro2024-microplane-damage.md]

本页展开分析页第 5 维；论文总览见 [[oropeza-navarro2024-microplane-damage-analysis]]，模型实体见 [[entities/oropeza-microplane-damage]]。

## 1. 方法总览

方法由四层组成：

1. 有限变形连续体与隐式 MPM/FEM 离散；
2. 使用 CPDI2 的材料点域插值；
3. 21 个微平面上的纤维增强损伤本构；
4. 以机械 bond 和 nonlocal bond 共同实现 MPM–FEM 的 monolithic 耦合。

论文的关键新结构是把非局部等效应变 \(\bar{\eta}\) 作为额外场自由度，与位移自由度 \(\mathbf d\) 一起解，而不是只在界面传递机械位移。

## 2. 有限变形与隐式 MPM

参考构形到当前构形由 \(\mathbf x=\varphi(\mathbf X,t)\) 连接，变形梯度为

\[
\mathbf F=\nabla\mathbf u+\mathbf 1,
\qquad \mathbf C=\mathbf F^T\mathbf F,
\qquad \mathbf E=\tfrac12(\mathbf C-\mathbf 1).
\]

本构在第二 Piola–Kirchhoff 应力 \(\mathbf S\) 与 Green–Lagrange 应变 \(\mathbf E\) 的功共轭对上建立；通过

\[
\boldsymbol\sigma=J^{-1}\mathbf F\mathbf S\mathbf F^T
\]

得到当前构形的 Cauchy 应力和相应切线（PDF pp. 2–3，Eq. 3–11）。

MPM 每一步包括：

- 用形函数把材料点上的质量、外力、速度/加速度等量映射到固定背景网格；
- 在背景网格上求解未知节点位移；
- 把位移和加速度映射回材料点，更新材料点位置并重置网格。

隐式非线性平衡方程采用 Newton–Raphson 迭代和隐式 Newmark 时间积分。线性化后的材料点有效刚度包含惯性项 \(\mathbf M/(\beta\Delta t^2)\) 与切线刚度 \(\mathbf K_p\)（PDF p. 3，Eq. 14–17）。

## 3. CPDI2 插值

普通 MPM 在材料点穿越固定背景单元边界时会产生 cell-crossing noise。论文采用二阶 Convected Particle Domain Interpolation（CPDI2），将材料点看作随变形演化的四边形（2D）或六面体（3D）域。

标准形函数被材料点域上的加权函数替代：

\[
S^v_p=\frac{1}{v_p}\int_{\Omega_p}\chi_p(\boldsymbol\xi)N^v(\boldsymbol\xi)\,d\boldsymbol\xi,
\]

其梯度同样在材料点域上积分。CPDI2 的替代形函数由材料点域角点处的背景网格形函数和域内单元形函数组合而成（PDF pp. 3–4，Eq. 18–22）。

在耦合 MPM–FEM 中，CPDI2 的实际作用还包括：获得材料点域角点在 FE 网格变形位置处的位移，使界面 bond element 能使用正确的几何位置。

## 4. 微平面框架

微平面方法把宏观应变投影到单位球面上的随机取向微平面，在每个微平面上施加本构关系，再将微平面应力积分回宏观应力。论文利用球面数值积分的 21 个对称积分方向：

\[
\mathbf S=\frac{3}{4\pi}\int_\Theta\mathbf S_{mic}\,d\Theta
\approx\sum_{mic=1}^{21}\mathbf S_{mic}w_{mic}.
\]

无损伤时的微平面能量含三部分：基体体积/偏量弹性，以及沿两条纤维方向 \(\mathbf A\)、\(\mathbf B\) 的偏量纤维项：

\[
\psi_{mic}=\tfrac12K_{mic}E_V^2+G_{mic}\mathbf E_D\!\cdot\!\mathbf E_D
+e_{mic}\mathbf E_{DA}\!\cdot\!\mathbf E_{DA}
+f_{mic}\mathbf E_{DB}\!\cdot\!\mathbf E_{DB}.
\]

其中体积应变由 \(J\) 表达，微平面法向应变来自 \(\mathbf n_{mic}\otimes\mathbf n_{mic}:\mathbf E\)，偏量应变和纤维方向投影由 Eq. 26–32 定义。对能量关于 \(\mathbf E\) 求导得到微平面第二 Piola–Kirchhoff 应力及其弹性切线（PDF pp. 4–5，Eq. 23–39）。

## 5. 隐式梯度增强

局部软化会导致应变集中、病态网格依赖和收敛丢失。论文引入改进 Helmholtz 方程：

\[
\bar\eta-\eta-c\nabla^2\bar\eta=0,
\qquad \nabla\bar\eta\cdot\mathbf n_b=0.
\]

\(\eta\) 是局部变量，\(\bar\eta\) 是其非局部对应物和额外自由度，\(c\) 控制梯度相互作用。边界采用齐次 Neumann 条件（PDF p. 5，Eq. 40–41）。

### 5.1 局部/非局部等效应变

每个微平面上的局部等效应变为

\[
\eta_{mic}=3k_1E_V+\sqrt{(3k_1E_V)^2+\tfrac32k_2\mathbf E_D\!\cdot\!\mathbf E_D}.
\]

\(k_1\)、\(k_2\) 由压拉强度比 \(k_r\) 和 Poisson 比 \(\nu\) 确定。论文明确指出 Eq. 42 不含纤维贡献，因为引用的材料试验在结束前没有观察到纤维失效。

体材料的局部变量取 21 个微平面的最大值：

\[
\eta=\max_{mic=1,\ldots,21}(\eta_{mic}).
\]

将 Helmholtz 方程求得的 \(\bar\eta\) 按最大局部值与各微平面局部值的比例映射回微平面：

\[
\bar\eta_{mic}=\frac{\bar\eta}{\eta}\eta_{mic}.
\]

### 5.2 损伤与切线

微平面历史变量和损伤变量分别为

\[
\gamma_{mic}(t)=\max(\gamma_0,\bar\eta_{mic}),
\]

\[
d_{mic}=1-\frac{\gamma_0}{\gamma_{mic}}
\left[1-\alpha+\alpha\exp\!\left(\omega(\gamma_0-\gamma_{mic})\right)\right].
\]

损伤只削弱基体的体积/偏量能量，纤维项保持独立：

\[
\psi_{mic}=(1-d_{mic})\psi_{mic}^{M}+\psi_{mic}^{F},
\qquad
\mathbf S_{mic}=(1-d_{mic})\mathbf S_{mic}^{M}+\mathbf S_{mic}^{F}.
\]

切线除基体与纤维弹性切线外，还包含

\[
-\mathbf S_{mic}^{M}\otimes\frac{\partial d_{mic}}{\partial\mathbf E},
\]

以捕捉损伤随应变变化的影响。论文还推导 \(\partial\mathbf S/\partial\bar\eta\)，再 push-forward 得到 \(\partial\boldsymbol\sigma/\partial\bar\eta\)（PDF pp. 6–7，Eq. 47–57）。

## 6. 双场非局部 MPM 离散

问题由动量平衡和 Helmholtz 方程组成：

\[
\nabla\!\cdot\!\boldsymbol\sigma+\mathbf b=\rho\ddot{\mathbf u},
\qquad
\bar\eta-\eta-c\nabla^2\bar\eta=0.
\]

对位移变分 \(\delta\mathbf u\) 和非局部变分 \(\delta\bar\eta\) 写弱式并积分分部，得到机械场和非局部场的残量（PDF pp. 6–7，Eq. 58–63）。

论文用同一套 CPDI2 权重函数离散位移场和非局部场：

\[
\mathbf u=S^v_p\mathbf d,
\qquad
\bar\eta=S^v_p\mathbf E,
\]

其中 \(\mathbf d\) 是网格节点位移，\(\mathbf E\) 是背景网格上的非局部等效应变节点量。

Newton–Raphson 的整体增量系统写为

\[
\begin{bmatrix}
\mathbf S_{uu}&\mathbf K_{u\bar\eta}\\
\mathbf K_{\bar\eta u}&\mathbf K_{\bar\eta\bar\eta}
\end{bmatrix}
\begin{bmatrix}\Delta\mathbf d\\\Delta\mathbf E\end{bmatrix}
=-
\begin{bmatrix}\mathbf R_u\\\mathbf R_{\bar\eta}\end{bmatrix}.
\]

其中 \(\mathbf S_{uu}=\mathbf M/(\beta\Delta t^2)+\mathbf K_{uu}\)；\(\mathbf K_{\bar\eta\bar\eta}\) 来自质量型项和梯度项；\(\mathbf K_{u\bar\eta}\) 来自应力对非局部等效应变的导数；\(\mathbf K_{\bar\eta u}\) 来自局部等效应变随位移变化的导数以及梯度项（PDF p. 7，Eq. 68–77）。

## 7. MPM–FEM bond element

### 7.1 机械 bond

界面 bond element 同时连接 FEM 节点和 MPM 激活背景单元节点。两侧界面位移差定义为

\[
\mathbf s=\mathbf u_{n,FE}-\mathbf u_{n,MP}=\mathbf N_b
\begin{Bmatrix}\mathbf u_{bn}\\\mathbf u_{bc}\end{Bmatrix}.
\]

bond stress 取 \(\boldsymbol\sigma_b=\mathbf C_b\mathbf s\)，通过用户定义 penalty 将 \(\mathbf s\) 压到零；其内部力和刚度为 \(\mathbf N_b^T\mathbf C_b\mathbf N_b\)（PDF pp. 7–8，Eq. 78–85）。

### 7.2 nonlocal bond

非局部界面要求

\[
\Delta\bar\eta=\bar\eta_{n,FE}-\bar\eta_{n,MP}=0.
\]

它使用两侧非局部场的形函数构造 \(\mathbf N_b\)，并令该形函数与机械 bond 的形函数相同。应力型变量 \(\bar\zeta_b=\mathbf C_b\Delta\bar\eta\)，内部力和非局部刚度为 \(\mathbf N_b^T\mathbf C_b\mathbf N_b\)（PDF pp. 8–9，Eq. 86–92）。

两类 bond 组合为

\[
\mathbf f_b^{int}=\begin{Bmatrix}\mathbf f_{b,u}^{int}\\\mathbf f_{b,\bar\eta}^{int}\end{Bmatrix},
\qquad
\mathbf K_b=
\begin{bmatrix}\mathbf K_{b,uu}&\mathbf0\\\mathbf0&\mathbf K_{b,\bar\eta\bar\eta}\end{bmatrix}.
\]

因此，界面处既约束机械位移，又约束非局部等效应变；这正是本文相对纯机械 MPM–FEM bond 的机制差异。

## 8. 实现依赖与可复现信息

实现至少需要：21 点微平面积分权重、CPDI2 域几何与梯度、有限变形应力 push-forward、微平面损伤历史更新、\(\partial d/\partial\mathbf E\) 和 \(\partial\boldsymbol\sigma/\partial\bar\eta\) 的切线、双场 Newton–Raphson 装配、Newmark 参数以及两类 penalty bond。

论文给出了三个例子的主要材料参数和离散设置，但没有公开代码、输入文件、完整收敛容限或 penalty 选取流程。因此本方法属于 medium 可复现性，而不是 high 可复现性。

结果对应的输入设置和观测见 [[oropeza-navarro2024-microplane-damage-results]]；失败边界和可迁移设计见 [[oropeza-navarro2024-microplane-damage-critical]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[oropeza-navarro2024-microplane-damage-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
