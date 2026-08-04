---
type: paper-analysis
title: A coupled implicit MPM-FEM approach for brittle fracture and fragmentation
authors:
- Ahmad Chihadeh
- William Coombs
- Michael Kaliske
year: 2023
venue: Computers and Structures
tags:
- domain/computational-mechanics
- evidence/paper
methods:
- material-point-method
- finite-element-method
- coupled-methods
- numerical-methods
- contact-mechanics
- brittle-fracture
- large-deformation
results:
- fracture
- dynamic-fracture
- impact
- coupled-methods
failure_modes:
- large-deformation
- fracture
- contact-mechanics
- numerical-methods
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--chihadeh2023-implicit-mpm-fem-fracture-method
status: active
project: civil-engineering-llm-wiki
keywords:
- computational-mechanics
- material-point-method
- finite-element-method
- coupled-methods
- large-deformation
- fracture
- brittle-fracture
- dynamic-fracture
- contact-mechanics
- impact
- numerical-methods
- reproducibility
- Computers and Structures
sources:
- sources/papers/chihadeh2023-implicit-mpm-fem-fracture.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Method — coupled implicit MPM-FEM for brittle fracture and fragmentation

^[sources/papers/chihadeh2023-implicit-mpm-fem-fracture.md]

论文：*A coupled implicit MPM-FEM approach for brittle fracture and fragmentation*；Ahmad Chihadeh、William Coombs、Michael Kaliske；2023；*Computers and Structures* 288, 107143。DOI：<https://doi.org/10.1016/j.compstruc.2023.107143>。

页面关系：[[chihadeh2023-implicit-mpm-fem-fracture-analysis]] · [[chihadeh2023-implicit-mpm-fem-fracture-results]] · [[chihadeh2023-implicit-mpm-fem-fracture-critical]] · [[entities/chihadeh-implicit-mpm-fem]]

以下按正文第 2–4 节展开；公式中的记号尽量保持预提取文本的含义。论文没有给出可直接运行的代码或完整输入文件，缺失项不作补全。

## 1. 总体计算结构

方法把三类贡献装配到同一个隐式系统：

1. MPM 背景网格中的 activated elements 及其材料点积分贡献。
2. 普通连续体有限元（FEM）贡献。
3. 把 FE 自由度与激活 MPM 单元自由度连接起来的 bond elements。

论文称这种耦合为 monolithic：MPM 和 FEM 的未知量一起进入一个系统并同时求解，不是先求一侧再把结果显式传给另一侧。

设计意图是让 FEM 覆盖远场，让 MPM 覆盖预期发生极端变形、裂纹和碎片运动的区域；在仿真中再把发生 eigenfracture 侵蚀的 FE 转成材料点。

## 2. 隐式 MPM 的三个时间步阶段

### 2.1 材料点到背景节点的映射

每个时间步的第一阶段，把体力、外力、质量、动量和惯性等材料点数据映射到背景网格节点。正文 Eq. (1) 的抽象形式为：

$$
\square_v=\sum_{p=1}^{n_p} \mathbf{N}(\boldsymbol{\xi}_p)^T\square_p,
$$

其中 `v` 表示节点，`p` 表示材料点，`N` 为形函数矩阵，`ξ_p` 为材料点局部坐标，`n_p` 为单元内材料点数，`□` 表示被映射的数据。

### 2.2 节点未知量的隐式求解

节点位移通过迭代过程求解（正文 Eq. (2)）：

$$
\mathbf{K}^{i}\Delta\mathbf{u}_v=\mathbf{f}^{i},\qquad
\mathbf{u}^{i+1}_v=\mathbf{u}^{i}_v+\Delta\mathbf{u}_v .
$$

`K` 是刚度矩阵，`u_v` 和 `Δu_v` 是节点位移及其增量，`f` 是残差向量，`i` 是迭代编号。

### 2.3 节点到材料点及网格重置

第三阶段把节点位移和加速度映射回材料点（正文 Eq. (3)）：

$$
\square_p=\mathbf{N}(\boldsymbol{\xi}_p)\square_v,
$$

随后把计算网格重置到未变形构形。材料点携带历史相关的计算信息，背景网格在下一个时间步重新参与映射和求解。

## 3. 几何非线性、材料模型和切线刚度

正文给出离散弱式平衡方程（Eq. (4)）：

$$
\int_V \mathbf{N}^T\rho\ddot{\mathbf{u}}_v\,dV
+\int_V \mathbf{B}^T\boldsymbol{\sigma}\,dV
=\int_V\mathbf{N}^T\mathbf{b}\,dV
+\int_A\mathbf{N}^T\mathbf{t}\,dA .
$$

其中 `ρ` 为密度，`ü_v` 为节点加速度，`B` 为形函数导数矩阵，`σ` 为 Cauchy 应力，`b` 为体力，`t` 为表面力。

论文明确加入 geometrical non-linearity，并采用 St. Venant–Kirchhoff 材料模型，因此 Eq. (4) 关于节点位移是非线性的。

隐式 Newmark 时间离散与 Newton–Raphson 线性化后，材料点内力和有效刚度写成（Eqs. (5)–(7)）：

$$
\mathbf{f}_p=\mathbf{B}_L^T\boldsymbol{\sigma}V_p,
$$

$$
\mathbf{K}_p^*=\frac{1}{\beta\Delta t^2}\mathbf{M}_p+\mathbf{K}_p,
$$

$$
\mathbf{K}_p=
\left[\mathbf{B}_L^T\mathbf{C}_T\mathbf{B}_L
+\mathbf{B}_{NL}^T\boldsymbol{\sigma}\mathbf{B}_{NL}\right]V_p .
$$

`β` 为 Newmark 参数，`Δt` 为时间步，`M_p` 为材料点质量矩阵，`C_T` 为切线材料张量，`B_L` 和 `B_NL` 分别表示线性与非线性形函数导数相关矩阵。

## 4. CPDI2 插值

### 4.1 选择 CPDI2 的原因

标准 MPM 在材料点跨越背景单元边界时会出现 cell-crossing noise，表现为数值振荡和错误应力。正文列举 GIMP、CPDI、CPDI2、DDMP 和 B-spline 等改进版本，本工作采用 second-order Convected Particle Domain Interpolation（CPDI2）。

CPDI2 在二维把粒子域跟踪为四边形，在三维跟踪为六面体；论文选择它的直接原因是需要精确更新粒子域角点位移，使 FE 边界和材料点域边界保持连接。

### 4.2 形函数和积分

GIMP 形式用粒子影响域 `Ω_p` 上的平均形函数及其梯度：

$$
S_{vp}=\frac{1}{V_p}\int_{\Omega_p}N_v(\mathbf{x})d\Omega,
\qquad
\nabla S_{vp}=\frac{1}{V_p}\int_{\Omega_p}\nabla N_v(\mathbf{x})d\Omega .
$$

CPDI2 用替代形函数（正文 Eq. (10)）：

$$
N^{alt}_v(\mathbf{x})=\sum_{c=1}^{n_c}M_c(\mathbf{x})N_v(\mathbf{x}_c),
$$

其中 `M_c` 是粒子域四边形/六面体的形函数，`x_c` 是域角点，`n_c` 在二维和三维分别为 4 和 8。于是平均形函数和梯度都由粒子域积分得到（Eq. (11)）。

二维双线性四边形的方括号积分使用 Nguyen 等人的推导；三维六面体积分在文中说明为数值求积。论文没有在提供文本中给出实现代码或全部积分容差。

## 5. Nodal bond element：节点界面连接

设 FE 界面节点位移为 `u_n`，同一位置处激活 MPM 单元的插值位移为 `u_nc`，则滑移向量为（Eqs. (12)–(14)）：

$$
\mathbf{s}=\mathbf{u}_n-\mathbf{u}_{nc},
\qquad
\mathbf{u}_{nc}=\mathbf{N}_c(\boldsymbol{\xi}_{nc})\mathbf{u}_v,
$$

$$
\mathbf{s}=\mathbf{B}_b
\begin{Bmatrix}\mathbf{u}_n\\\mathbf{u}_v\end{Bmatrix} .
$$

`u_v` 是激活 MPM 单元的节点位移，`N_c` 是其形函数矩阵，`B_b` 将两侧位移组合成 slip。

滑移产生 bond stress（Eq. (17)）：

$$
\boldsymbol{\sigma}_b=\mathbf{C}_b\mathbf{s}.
$$

三维中 `C_b` 的 `C_x,C_y,C_z` 是用户定义的罚系数；这些较大的系数把 slip 压到接近零。bond force 和 bond stiffness 为：

$$
\mathbf{f}_b=\mathbf{B}_b^T\mathbf{C}_b\mathbf{s}
=\mathbf{B}_b^T\mathbf{C}_b\mathbf{B}_b
\begin{Bmatrix}\mathbf{u}_n\\\mathbf{u}_v\end{Bmatrix}
=\mathbf{K}_b
\begin{Bmatrix}\mathbf{u}_n\\\mathbf{u}_v\end{Bmatrix} .
$$

力和刚度按每个 bond element 装配到全局系统；一半力作用在 FE 节点，另一半作用在激活 MPM 单元。

## 6. Intermediate bond element：异尺寸网格连接

若 FEM 单元比 MPM 背景网格大，只在 FE 节点连接会导致界面中部失去连通性。论文因此在 FE 表面引入 intermediate bond elements。

中间 bond 的 FE 侧位移先用 FE 形函数插值得到：

$$
\mathbf{u}_{ne}=\mathbf{N}_e(\boldsymbol{\xi}_{ne})\mathbf{u}_i,
$$

再与同一位置的 `u_nc` 相减（Eqs. (22)–(24)）：

$$
\mathbf{s}=\mathbf{u}_{ne}-\mathbf{u}_{nc}
=\left[\mathbf{N}_e(\boldsymbol{\xi}_{ne})-\mathbf{N}_c(\boldsymbol{\xi}_{nc})\right]
\begin{Bmatrix}\mathbf{u}_i\\\mathbf{u}_v\end{Bmatrix} .
$$

其 bond force 和刚度与 nodal bond 相同。论文的应力波例子显示，粗 FE 界面必须加入这类连接；L 形板、裂纹分叉和冲击例子中也在连续体单元表面创建中间 bond。

## 7. Monolithic 全局方程

把 MPM、FEM 和 bond contributions 装配到一个块系统（正文 Eq. (21)）：

$$
\begin{bmatrix}
\mathbf{K}_{MPM+be} & \mathbf{K}_{be}\\
\mathbf{K}_{be} & \mathbf{K}_{FEM+be}
\end{bmatrix}
\begin{Bmatrix}\Delta\mathbf{u}_{MPM}\\\Delta\mathbf{u}_{FEM}\end{Bmatrix}
=
\begin{Bmatrix}\mathbf{f}_{MPM+be}\\\mathbf{f}_{FEM+be}\end{Bmatrix} .
$$

论文强调这按标准 FEM 的方式组装，但两个子域的未知量在同一方程组中同时求解。

## 8. MPM–FEM 接触

接触使用同一 bond-element 形式，但增加激活条件：

1. 至少一个 FE 节点进入 MPM 背景网格的 activated element。
2. 距离满足 `d ≤ 0`（proximity condition，正文 Eq. (25)）。
3. 两个物体正在接近而不是分离，即 `(u_n − u_nc) · n > 0`（正文 Eq. (26)）。

两个条件同时满足时，接触 bond 激活。接触 bond 的本构矩阵为：

$$
\mathbf{C}_b=\begin{bmatrix}C_n&0&0\\0&C_t&0\\0&0&C_t\end{bmatrix},
$$

`C_n` 是法向系数，使用罚项避免穿透；`C_t` 描述摩擦，但该论文接触算例设置 `C_t=0`，因此没有摩擦。

## 9. Eigenfracture 驱动的 FE→MP 转换

### 9.1 侵蚀判据

eigenfracture 把裂纹描述为一组 eroded elements，并以裂纹驱动的弹性能量和断裂能之间的平衡为基础。单元弹性能量泛函为：

$$
E(\mathbf{u},c)=\int_{v_e}\psi(\mathbf{F}(\mathbf{u}),c)dV,
$$

$$
\psi(\mathbf{F}(\mathbf{u}),c)=c\psi^+(\mathbf{F}(\mathbf{u}))
+\psi^-(\mathbf{F}(\mathbf{u})),
$$

$$
\psi^-=\psi-\psi^+,
\qquad
c=\begin{cases}0,&\text{eroded},\\1,&\text{intact}.
\end{cases}
$$

当（正文 Eq. (32)）

$$
\int_{v_e}\psi^+(\mathbf{F}(\mathbf{u}))dV\geq G_c|C|
$$

时，FE 被侵蚀；`G_c` 是临界能量释放率，`|C|` 是裂纹面积。

### 9.2 单元转换

仿真可以从全 FEM 开始。单元变为 eroded 后：

1. 该 FE 从连续体求解中排除。
2. 生成用户选择数量的材料点。
3. 用给定材料点局部坐标和形函数，把替代 FE 所需的数据赋给材料点。
4. 在可能出现材料点的区域建立 MPM 计算网格，并通过 bond elements 与仍 intact 的 FE 连接。

论文指出，为避免数值不稳定，`c=0` 的零刚度在实践中通常改为很小的刚度；动态惯性项也有助于维持稳定。不同 split 模型可能导致 eroded 材料在压缩下保留不同的刚度。

正文列举 volumetric–deviatoric、spectral/TC 和 Representative Crack Element（RCE）split，并引用相关工作认为 RCE 表现较优；提供文本没有明确说明本文每个算例最终采用哪一种 split，因此这里不作进一步指定。

## 10. 论文实际给出的参数化控制

- bond penalty 系数：用户定义；具体值未在提供文本中列出。
- 接触切向系数：接触示例中 `C_t=0`。
- 转换触发器：本文使用 eigenfracture eroded 状态；正文说明其他问题也可用畸变或损伤比例作为标准，但没有在本文中验证那些标准。
- 每个侵蚀 FE 的材料点数：可自由选择；示例使用 4 或 8 个/单元，基准还比较 2×2 与 3×3。
- MPM 插值：CPDI2；二维粒子域积分使用推导结果，三维积分数值求取。
- 时间积分：隐式 Newmark；Newton–Raphson 求解非线性方程。各数值例子的 `Δt, β, γ` 见 [[chihadeh2023-implicit-mpm-fem-fracture-results]]。

## 11. 证据链式算法流程

```text
初始化 FE、MPM 背景网格、材料点和边界条件
        ↓
材料点 → MPM 节点映射；FE 贡献独立形成
        ↓
按界面位置建立 nodal / intermediate bond；按条件建立接触 bond
        ↓
装配 MPM + FEM + bond 的整体切线系统
        ↓
Newmark 时间离散 + Newton–Raphson 迭代求解
        ↓
节点 → 材料点映射，并重置 MPM 背景网格
        ↓
检查 eigenfracture 能量阈值
        ├─ intact：继续 FE 表示
        └─ eroded：FE → 材料点，生成/更新局部 MPM 区域和界面 bond
```

这是按正文各节拼接的机制流程，不是论文提供的伪代码；实现级的数据结构、收敛容差和并行策略未披露。

## 12. 方法边界与实现缺口

论文建议实际使用中 MPM 网格应更细或至少不粗于 FE 网格；FE 更细的耦合没有被明确研究。

接触机制只在无摩擦设置下数值验证。材料模型、penalty 取值、split 选择和求解器细节的完整组合没有作为开放输入集给出。

论文说明全部算法实现在 in-house Fortran MP-FE code 中，但没有提供 `code_url`；研究没有使用数据集，`dataset_url` 为 `[]`。

方法与结果的对应关系可从 [[chihadeh2023-implicit-mpm-fem-fracture-results]] 核对，失败边界和迁移判断见 [[chihadeh2023-implicit-mpm-fem-fracture-critical]]。
