---
type: paper-analysis
title: Explicit phase field generalized interpolation material point method for dynamic
  fracture problems
authors:
- Chi Lv
- Xiao-Ping Zhou
year: 2025
venue: Computers and Structures
tags:
- domain/computational-mechanics
- evidence/paper
methods:
- phase-field
- material-point-method
- generalized-interpolation
- contact-mechanics
- friction
- numerical-methods
results:
- dynamic-fracture
- brittle-fracture
- fracture
- impact
- numerical-methods
failure_modes:
- large-deformation
- fracture
- contact-mechanics
- numerical-methods
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--lv2025-phase-field-gimp-fracture-method
status: active
project: civil-engineering-llm-wiki
keywords:
- computational-mechanics
- material-point-method
- generalized-interpolation
- phase-field
- fracture
- brittle-fracture
- dynamic-fracture
- contact-mechanics
- friction
- large-deformation
- impact
- numerical-methods
- reproducibility
- Computers and Structures
sources:
- sources/papers/lv2025-phase-field-gimp-fracture.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Method — explicit phase field GIMP-MPM for dynamic fracture

^[sources/papers/lv2025-phase-field-gimp-fracture.md]

论文：*Explicit phase field generalized interpolation material point method for dynamic fracture problems*；Chi Lv、Xiao-Ping Zhou；2025；*Computers and Structures* 310, 107685。DOI：<https://doi.org/10.1016/j.compstruc.2025.107685>。

页面关系：[[lv2025-phase-field-gimp-fracture-analysis]] · [[lv2025-phase-field-gimp-fracture-results]] · [[lv2025-phase-field-gimp-fracture-critical]] · [[entities/lv-phase-field-gimp]]

以下按正文 §2–§4、Algorithm 1 和 Eq. (60)–(62) 展开。预提取文本中的公式有少量排版字符丢失，下面只保留能由上下文确认的结构；未披露的实现细节不作补全。

## 1. 方法总览

EPF-GIMP 的三个关键词对应三个设计层：

1. **Explicit phase field**：用带人工黏性的速率相关相场方程显式推进裂纹变量，不在每个时间步求解隐式全局耦合非线性方程。
2. **GIMP**：将线性网格形函数在材料点特征域上积分，得到更平滑的权函数和梯度，减少粒子跨 cell 的数值噪声。
3. **MPM**：材料点携带质量、位置、速度、应力、应变、phase field 与历史变量；背景网格只在当前时间步承担方程更新，之后被重置。

作者在 Updated Lagrangian 框架中将位移场和 phase field 都离散在材料点/背景节点之间，并用 MUSL（Modified Update Stress Last）重新投影更新后的粒子动量，以改善能量守恒性质（§1、§4.1）。

## 2. Phase-field fracture 的能量与状态变量

### 2.1 弥散裂纹和断裂能

论文用一维指数函数说明弥散裂纹：

$$
c(x)=\exp\left(-\frac{|x|}{l_c}\right),
$$

其中 `c=0` 表示无断裂，`c=1` 表示完全断裂，`l_c` 控制非光滑裂纹拓扑被正则化后的宽度（Eq. (1)）。裂纹表面密度函数为：

$$
\gamma_l(c,\nabla c)=\frac{1}{2l_c}c^2+\frac{l_c}{2}|\nabla c|^2,
$$

相应的 Griffith 断裂能为：

$$
\Psi_f=G_c\int_\Omega \gamma_l(c,\nabla c)\,dV,
$$

`G_c` 是单位裂纹面积的临界能量释放率（Eqs. (4)、(7)）。

### 2.2 张压分解和退化

论文只退化拉伸断裂相关的弹性能，将弹性能分为 `φ_e^+` 与 `φ_e^-`。分解使用主应变、Lamé 常数和 Macaulay brackets；退化函数为：

$$
g_c(c)=(1-c)^2.
$$

Cauchy 应力由退化后的张拉部分和未退化的压缩部分构成：

$$
\boldsymbol\sigma=g_c(c)\boldsymbol\sigma^+ + \boldsymbol\sigma^-.
$$

历史场

$$
H(t)=\max_{\tau\leq t}\phi_e^+(\tau)
$$

用于保证相场只增长、不发生裂纹愈合（Eqs. (9)–(14)、(18)–(24)）。这使损伤退化成为本文的材料/本构非线性来源，而不是机器学习中的 PDE 算子非线性。

### 2.3 动能、黏性能和强形式

动能为 `W_k=1/2∫_Ωρ\dot u·\dot u dV`。相场引入黏性能项：

$$
W_v=\int_0^t\int_\Omega\frac12\eta\dot c^2\,dV\,dt,
$$

其中 `η` 是人工黏性参数，论文给出 `η=Δt^2/ε`；`ε` 是无直接物理意义的正则化参数，应依据系统矩阵条件数确定（Eq. (16)）。

由三场 Lagrangian `L=W_k+W_v-ψ_pot` 变分得到耦合强形式。动量方程为：

$$
\nabla\cdot\left[g_c(c)\boldsymbol\sigma^+ + \boldsymbol\sigma^-\right]+\mathbf b=\rho\ddot{\mathbf u}.
$$

相场方程的结构为：

$$
-\frac{\partial g_c}{\partial c}H
-\frac{G_c}{l_c}\left(c-l_c^2\Delta c\right)
=\eta\dot c.
$$

边界条件包括退化应力牵引、`∇c·n=0`，并给定位移、初始位移/速度和初始 `c=0`（Eqs. (18)–(24)）。

## 3. MPM 离散与 GIMP 插值

### 3.1 材料点积分

MPM 用材料点承载质量和状态变量，密度场以 Dirac delta 的粒子和表示：

$$
\rho(\mathbf x)=\sum_{p=1}^{n_p}m_p\delta(\mathbf x-\mathbf x_p).
$$

将动量方程弱式代入该表示后，连续积分转为材料点求和。节点动量满足 `\dot{\mathbf p}_I=\mathbf f_I^{int}+\mathbf f_I^{ext}`；内部力由退化应力、材料点质量/密度和形函数梯度构成，外力由体力和牵引构成（Eqs. (25)–(33)）。

### 3.2 GIMP 的形函数

标准 MPM 在材料点穿越背景 cell 时因梯度不连续而出现噪声。GIMP 用材料点特征函数 `χ_p` 表示粒子域，并在粒子域上积分线性形函数，使权函数达到 `C^1` 连续（§3.2、Fig. 2）。

论文给出一维线性网格上的分段形函数 `S_{Ip}` 和梯度 `∇S_{Ip}`，取决于网格尺寸 `h_x`、当前粒子尺寸 `l_p` 和粒子到节点的距离。三维实现沿各坐标方向使用相应的 GIMP 权重；论文提供了解析表达式，但没有给出代码或全部边界实现细节。

位移场使用

$$
\mathbf u_p=\sum_I S_{Ip}\mathbf u_I,
\qquad
\delta\mathbf u_p=\sum_I S_{Ip}\delta\mathbf u_I,
$$

phase field 使用同一形函数：

$$
c_p=\sum_I S_{Ip}c_I,
\qquad
\nabla q_p=\sum_I(\nabla S_{Ip})q_I.
$$

这使力学场与相场在相同材料点–节点支撑域中更新（Eqs. (28)–(29)、(55)–(57)）。

## 4. Phase field 的材料点离散

相场弱式将节点更新写成 crack driving force、geometric resistance 和 lumped viscous matrix 的组合：

$$
\dot c_I=-(y_I^{dri}+y_I^{res})/C_I.
$$

其中驱动力由 `-∂g_c/∂c·H-G_c/l_c·c` 及材料点体积、质量/密度和 `S_{Ip}` 汇总；几何阻力包含 `G_c l_c`、形函数梯度和相场值；黏性矩阵为：

$$
C_I=\sum_p\eta_pV_pS_{Ip}.
$$

论文在 Algorithm 1 中按增量形式求解 `Δc_I=(y_I^{dri}+y_I^{res})Δt/C_I`，再用 `S_{Ip}` 映射回粒子。更新后施加：

1. 单调增长约束，禁止 `c_p^{k+1}<c_p^k`；
2. 值域约束，把 `c_p` 限制在 `0≤c_p≤1`；
3. 用 `∇S_{Ip}` 重新计算材料点相场梯度。

## 5. 粒子接触与 Coulomb 摩擦

### 5.1 预测–修正

接触算法只考虑多个物体同时对同一背景节点有贡献的情形；推导先写两个物体，作者说明未来可扩展到更多物体。对物体 `b`，先基于各物体独立解得到 trial velocity `\tilde v_I^{(b)}`，再计算参与接触的质心速度：

$$
v_{I}^{cm}=\frac{(m_I\tilde v_I)^{(1)}+(m_I\tilde v_I)^{(2)}}{m_I^{(1)}+m_I^{(2)}}.
$$

用该物体的质量加权形函数梯度估计法向 `n_I^{(b)}`。若相对 trial velocity 在法向上的投影满足文中接触判据，则进入 contact，否则 release。接触状态下先去除相对法向速度，随后修正切向速度。

### 5.2 法向、切向和摩擦力

使物体完全粘着所需的法向力与切向 stick force 分别按时间步 `Δt` 和节点质量计算。Coulomb friction 将实际摩擦力限制为：

$$
\mathbf f_I^{fric,(b)}
=\frac{\mathbf f_I^{stick,(b)}}{\mid\mathbf f_I^{stick,(b)}\mid}
\min\left(\mu\mid\mathbf f_I^{normal,(b)}\mid,\mid\mathbf f_I^{stick,(b)}\mid\right).
$$

修正后的节点速度用于更新加速度、粒子速度和位置。接触面施加相反法向和摩擦力，满足作用–反作用；论文同时强调共线性、动量守恒和防止界面渗透（Eqs. (36)–(52)）。

## 6. Algorithm 1：一个显式时间步

论文的 EPF-GIMP 流程可按以下顺序复述：

1. 初始化背景网格、材料点、`l_c`、`G_c`、`η`、初始 `c`、质量、体积和映射关系。
2. 将粒子质量、半步动量和黏性耗散量映射到节点；固定边界处令节点半步动量为零。
3. 计算内部/外部节点力，更新节点总力与半步动量；执行接触修正。
4. 用修正后的节点速度更新粒子位置和速度。
5. 由粒子状态汇总相场驱动力、几何阻力，求解 `Δc_I`；映射回粒子并施加单调/值域约束。
6. 用 MUSL 重新构造网格动量和节点速度。
7. 由节点速度梯度更新粒子应变、应力和密度。
8. 更新正应变能与历史场 `H`，进入下一时间步。

这套顺序把相场更新放在位移/接触更新之后，把历史场更新放在应力更新之后；具体实现中的数组组织、并行策略和边界代码未披露。流程图见 Fig. 4–5。

## 7. 显式稳定时间步

位移场和相场都采用显式时间积分，时间步满足 CFL 条件：

$$
\Delta t\leq\zeta\min\{\Delta t_u,\Delta t_d\},
$$

其中 `ζ∈(0,1]`，`Δt_u` 与 `Δt_d` 分别是位移场和相场的临界时间尺度。论文给出近似关系：

$$
\Delta t_u\approx\frac{L_{min}}{c_d},
\qquad
\Delta t_d\approx\frac{L_{min}^2}{2\alpha},
\qquad
\alpha=\frac{g_cl_c}{\eta}.
$$

因此细网格、较小长度尺度、较大的相场扩散率或不合适的 `η` 都可能压低稳定时间步。论文只给出稳定性表达式和算例时间步，未给出自适应时间步实现。

## 8. 方法中可确认与未披露的参数

- 可确认：GIMP、显式 forward-difference、MUSL、粒子接触、Coulomb friction、CFL 稳定控制、phase-field 历史场与 `0≤c≤1` 约束。
- 论文给出 `η=Δt^2/ε` 的关系，并说明 `ε` 无直接物理意义；各算例表格给出具体 `η`。
- 环碰撞算例明确使用摩擦系数 `μ=0.65`；接触算法的一般参数敏感性没有系统展开。
- 无法从提供文本确认：完整代码、输入文件、接触边界实现、所有图例对应的黏性组合、求解流程自动化脚本和性能数据。

方法与量化基准的对应见 [[lv2025-phase-field-gimp-fracture-results]]；对 `η`、`l_c`、网格和接触验证边界的判断见 [[lv2025-phase-field-gimp-fracture-critical]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[lv2025-phase-field-gimp-fracture-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
