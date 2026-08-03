---
id: paper--zhou2025-learnable-physics-engine-method
title: Zhou & Feng (2025) — Learnable physics engine：方法机制
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/zhou2025-learnable-physics-engine
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_methods:
- message-passing
- time-marching
- learning-rate-schedule
- physics-simulation
legacy_results:
- long-horizon-rollout
- extrapolation-ability
legacy_failure_modes:
- limitation
- extrapolation-ability
legacy_datasets:
- synthetic-data
legacy_reproducibility: low
legacy_tags:
- neural-network
- deep-learning
- message-passing
- physics-simulation
- scientific-machine-learning
- time-marching
- learning-rate-schedule
- metamodeling
legacy_sources:
- raw/papers/zhou2025-learnable-physics-engine.xml
evidence_scope: local workspace source record pending canonical verification
---

# Learnable physics engine：方法机制

> 本页只展开方法。论文的物理非线性是 **材料本构非线性**：网络学习 OSB-PD Drucker–Prager 的弹性储能与屈服面演化；它不是把 $u u_x$、$(u\cdot\nabla)u$ 这类 PDE 算子非线性塞进残差。图消息负责离散相互作用和状态推进。

## 1. 目标模型：OSB-PD Drucker–Prager

论文先把 ordinary state-based peridynamics（OSB-PD）Drucker–Prager 弹塑性模型作为 teacher/learning target。材料点 $x$ 与 horizon $\delta$ 内的邻域点 $x'$ 相互作用，初始键向量为 $\xi=x'-x$，相对位移为 $\eta=u'-u$。OSB-PD 的运动方程写成非局部积分形式：

$$
\rho(x)\,\ddot u(x,t)=\int_H\left[T(x,t)\langle x'-x\rangle-T(x',t)\langle x-x'\rangle\right]dH+b(x,t).
$$

这里 $T$ 是力状态，$b$ 是外力密度；图模型把材料点变成节点，把 horizon 内的键/邻域关系变成边。这样“非局部物理”首先被编码进图拓扑，而不是由一个全连接黑箱去猜。

### 1.1 可解释的弹性储能

键伸长 $s=s(\xi,\eta)$，体积膨胀为 $\Theta=a\,\omega\cdot s$。将键伸长分解为体积部分 $s^k$ 和偏差部分 $s^d=s-s^k$ 后，论文使用：

$$
\psi=\psi_k+\psi_d,\qquad
\psi_k=\frac12 k\Theta^2,\qquad
\psi_d=\mu'\,\omega\cdot(s^d)^2.
$$

力状态由储能对相对位移的梯度得到：

$$
T=\nabla_\eta\psi.
$$

这一步是解释性的核心：网络不是直接输出任意 $T$，而是先给出可解释的 $\hat\psi_k,\hat\psi_d$，再由导数构造力。体积储能与偏差储能还分别对应应力不变量中的压力和偏差应力信息。

### 1.2 Drucker–Prager 屈服与塑性状态

论文将屈服函数写成：

$$
F_y(\sigma,\zeta)=J_2+\alpha_{DP}I_1-k_{DP}(\zeta),
$$

其中 $I_1$ 是应力第一不变量，$J_2$ 是偏应力第二不变量，$\zeta$ 是控制屈服面尺寸的标量塑性状态。等价地，$p=I_1/3$，$q=\sqrt{3J_2}$；$k_{DP}(\zeta)$ 表示理想塑性或硬化规律。$\alpha_{DP}$ 与摩擦角有关，$k_{DP}$ 与黏聚力有关。

塑性流动采用非关联流动势 $g=J_2+\alpha'_{DP}I_1$。塑性应变增量方向由：

$$
d\varepsilon^p_{ij}=d\lambda\frac{\partial g}{\partial \tau_{ij}}
=d\lambda\left(\alpha'_{DP}\delta_{ij}+\frac{S_{ij}}{2J_2}\right)
$$

决定。PD 键伸长分成弹性和塑性部分，体积塑性伸长与偏差塑性伸长分别更新；若 $F_y>0$，就需要求塑性乘子 $d\lambda$，然后回写 $\zeta$、塑性键状态和新的力状态。

## 2. 图表示与 MPNN

### 2.1 节点、边与聚合

图 $G(V,E)$ 中，节点 $v_i$ 表示一个材料点，边 $e_k$ 表示邻域中的一条相互作用键。边保存连接节点索引及边特征，节点保存位置、位移或材料状态等可更新/不可更新属性。论文使用标准 MPNN 的三步：

1. **边更新：** 每条边接收自身特征、接收消息的节点 $v_{r_k}$ 和发送消息的节点 $v_{s_k}$，通过 $\phi^e$ 得到 $e'_k$；
2. **边到节点聚合：** 对所有指向节点 $i$ 的边做逐元素求和，得到 $\bar e'_i=\sum_{k:r_k=i}e'_k$；
3. **节点更新：** 用 $\phi^v(\bar e'_i,v_i)$ 得到 $v'_i$。

抽象写为：

$$
e'_k=\phi^e(e_k,v_{r_k},v_{s_k}),\qquad
\bar e'_i=\rho_{e\to v}(E'_i),\qquad
v'_i=\phi^v(\bar e'_i,v_i).
$$

论文把 $\phi^e$、$\phi^v$ 用神经网络实现，把 $\rho$ 设为求和；平均、最大或最小也被作为可选聚合形式提及。求和聚合与材料点邻域贡献的叠加形式一致，但它本身不自动保证守恒、客观性或传播范围充分。

### 2.2 三个 MPNN 模块的职责

| 模块 | 输入 | 关键输出 | 物理职责 |
|---|---|---|---|
| MPNN1 | 图节点 $V$、边矩阵 $E$ | 键伸长 $s$ | 从相对位置/位移构造材料点之间的变形状态 |
| MPNN2 | $s$ 与 $E$ | $\psi_k,\psi_d$、$p,q$、$\hat f$、塑性更新 | 由能量得到力状态，判断屈服并更新 $d\lambda,\zeta$ 和塑性键状态 |
| MPNN3 | 力状态 $T$ 与 $E$ | $E',V'$ | 聚合材料点受力，推进位置和图状态 |

因此，MPNN2 不是普通的“edge-to-node 回归头”：它把网络函数放在一个仍然显式执行本构算法的环节里。图状态在每个时间步重新更新，形成 time-evolving graph。

## 3. Elastic energy 的 Sobolev training

### 3.1 H² 目标

论文扩展 Sobolev training，使学习的能量同时匹配函数值、一阶导数和二阶导数。对训练样本 $i=1,\ldots,N$，目标可写成：

$$
\min_{W,b}\frac1N\sum_i\left[
\gamma_1\Vert\psi_i-\hat\psi_i\Vert_2^2
+\gamma_2\left\Vert\frac{\partial\psi_i}{\partial s_i}-\frac{\partial\hat\psi_i}{\partial s_i}\right\Vert_2^2
+\gamma_3\left\Vert\frac{\partial^2\psi_i}{\partial s_i^2}-\frac{\partial^2\hat\psi_i}{\partial s_i^2}\right\Vert_2^2
\right].
$$

在数值实验中，$\gamma_1=\gamma_2=\gamma_3=1$。一阶导数直接关联力/应力，二阶导数关联切线/刚度，因此只拟合 $\psi$ 的数值而不约束导数，会留下不平滑或切线不可信的解。

### 3.2 网络拆分

输入是键伸长 $s$。作者比较了一个输出 $(\psi_k,\psi_d)$ 的 MLP 和两个各自输出一个标量的 MLP，最终采用分开的网络，因为优化更容易。这个拆分保留了体积与偏差能量的语义边界，也使后续的 $p,q$ 计算不必由一个无语义的混合标量反推。

Sobolev training 的优势在于把“可解释”落实成可检查的导数关系：

energy value → stored energy；first derivative → force state；second derivative → tangent/smoothness information。

它并不自动保证热力学稳定性；若要迁移到新的材料，仍需增加客观性、凸性、正切对称性或耗散约束。

## 4. Yield function 的 level-set training

### 4.1 从屈服面到 signed distance

只训练初始 $F_y=0$ 不能表示硬化。论文把应力降到三维不变量表示 $x=(p,\beta,\theta)$，其中 $p$ 是平均压力，$\beta$ 是 Lode 半径，$\theta$ 是 Lode 角；随后对每个累计塑性应变/伪时间快照构造屈服面的 signed-distance level set：

$$
\Phi(x,\zeta,t)=
\begin{cases}
d(x), & x\text{ 在屈服面外},\\
0, & x\text{ 在屈服面上},\\
-d(x), & x\text{ 在屈服面内},
\end{cases}
$$

其中 $d(x)$ 是到当前屈服面的最小欧氏距离。符号约定让“屈服面内/外”不再只是离散标签，而是有几何距离的连续监督。

### 4.2 用 Hamilton–Jacobi 演化硬化

把累计塑性状态当作 pseudo-time，level set 满足：

$$
\frac{\partial\Phi}{\partial t}+\vartheta\cdot\nabla\Phi=0,
\qquad
\vartheta=F\,n,
\qquad
n=\frac{\nabla\Phi}{|\nabla\Phi|}.
$$

由于 signed distance 保持 $|\nabla\Phi|\approx1$，可写成：

$$
\frac{\partial\Phi(\zeta)}{\partial t}+F(\zeta)|\nabla\Phi(\zeta)|=0.
$$

论文用相邻 level-set 快照的有限差分近似速度场：

$$
F_i\approx\frac{\Phi_{i+1}(\zeta_{i+1})-\Phi_i(\zeta_i)}{\Delta t}.
$$

这使硬化机制变成“屈服面沿法向如何移动”的学习问题，而不是给每个状态训练一个互不关联的分类器。

### 4.3 应力空间采样与神经屈服函数

算法 2 先把采样应力谱分解并映射到 $(p,\beta,\theta)$，再投影到 $(p,q)$。在每个原始样本周围沿 $q$ 方向做 $L$ 级插值，使用 $\varsigma>1$ 扩展到屈服面内外，得到 $(p_m,q_m,\varepsilon^p_m,f_m)$。最终训练：

$$
\hat f(p,q,\zeta\mid W,b)\approx f(p,q,\zeta).
$$

论文的两个代表性 level-set 数据集对应：

- ideal elastic–plastic：$k_{DP}(\varepsilon^p)=k_{DP}$；
- linear hardening：$k_{DP}(\varepsilon^p)=2k_{DP}(1+2\varepsilon^p)$。

### 4.4 Newton 更新与自动微分

若网络屈服函数 $\hat f>0$，算法用自动微分得到 $\partial\hat f/\partial d\lambda$，并用 Newton 迭代：

$$
d\lambda\leftarrow d\lambda-\frac{\hat f(d\lambda)}{\partial\hat f/\partial d\lambda}.
$$

每次迭代按照 OSB-PD 的塑性更新重新计算 trial 状态、$p'$、$q'$、$\zeta'$ 和 $\hat f$；收敛后更新弹性键伸长、塑性键伸长、力状态及累计塑性状态。自动微分在这里服务于本构根求解，不代表本文学习了 PDE 算子非线性。

## 5. 端到端计算流程

论文算法 3 可以按如下顺序实现：

1. **MPNN1：** 从 $E,V$ 更新边和节点，计算每个材料点的键伸长 $s$。
2. **MPNN2：** 由 $s,E$ 计算 $\hat\psi_k,\hat\psi_d$，求出能量导数、$T$、$p$ 和 $q$；将 $(p,q,\zeta)$ 输入 $\hat f$。
3. **塑性判断：** 若 $\hat f\le0$，保持弹性状态；若 $\hat f>0$，用 Newton 迭代得到塑性乘子，更新 $\zeta$、塑性伸长和 $T$。
4. **MPNN3：** 用 $T$ 更新边消息，分别聚合到端点节点，计算材料点合力，得到下一时刻的 $E',V'$。
5. **重复推进：** 将图状态送入下一时间步，形成长期 forward prediction。

这一流程与 [[message-passing-reach-contract]] 的关系是：材料点每步所需的真实邻域信息必须已经出现在图边或消息 receptive field 中；仅增加 MLP 宽度并不能补回缺失的远程路径。与 [[mp-pde]] 相比，这里每一步的核心不是通用 PDE residual，而是显式材料状态、屈服判断和非局部键力。

## 6. 网络与优化设置

XML 中给出的共同预测架构包括：

| 项目 | 论文设置 |
|---|---|
| 主要函数 | MPNN2 的 $\phi^2_e$、$\phi^2_v$ |
| 隐藏层 | $\phi^2_e$ 为 5 层，每层 30 个单元；$\phi^2_v$ 结构基本相同 |
| 激活 | 每个隐藏层后接 Tanh |
| 输出 | $\phi^2_e$ 输出规模 $N_e\times2$；$\phi^2_v$ 输出规模 $N_e\times1$ |
| 优化器 | Adam |
| 初始学习率 | 0.0005 |
| 学习率调度 | 每 100 个 epoch 乘以 0.1 |
| 图实现 | PyTorch Geometric（PyG） |
| 能量 loss 权重 | $\gamma_1=\gamma_2=\gamma_3=1$ |

论文强调 MPNN1 和 MPNN3 中部分函数采用显式、简单的图运算，以降低训练复杂度和时间；并非所有函数都必须由独立深网络替代。这一点是工程实现时的关键：将所有步骤都黑箱化会增加训练难度，也会削弱能量/力/位置之间的可解释接口。

## 7. 方法优势与方法级风险

**优势：**

- $\hat\psi$ 的一阶/二阶导数可直接用于力和切线，避免单独回归互不一致的应力与刚度；
- level-set 表达将屈服面内外距离和硬化速度结合起来，能表示随塑性状态移动的屈服边界；
- MPNN 将材料点级本构与空间/邻域相互作用放在一个状态机内，适合 GPU 上批量推进；
- Newton 和塑性状态更新保留了传统本构算法的可解释步骤。

**方法级风险：**

- level-set 速度由有限差分快照得到，数据采样、距离符号和伪时间步长会影响训练目标；
- Newton 需要 $\partial\hat f/\partial d\lambda$ 稳定且根存在，论文没有给出全面的失败/回退策略；
- 求和聚合并不自动保证平衡、客观性或耗散；
- 图的 horizon 与消息深度决定有效传播范围，跨分辨率/跨域使用前必须做 reach 审计；
- 训练网络来自 OSB-PD teacher，因而代理的“准确”首先是对该本构假设的准确，而不是对真实 geomaterial 的无偏发现。

## 8. 可复现性

| 项目 | 说明 |
|---|---|
| 等级 | 🔴 低 |
| 代码 | []；XML 无公开仓库 URL |
| 数据 | []；原文仅称可按请求提供 |
| 可复现基础 | 公式、MPNN 角色、部分层数/学习率/调度策略明确 |
| 仍缺信息 | 数据样本量、归一化、划分、epoch/停止标准、随机种子、完整图构造和版本信息 |

## 关联页面

- [[zhou2025-learnable-physics-engine-analysis]] — 12 维总览
- [[zhou2025-learnable-physics-engine-results]] — 方法在 4 个数值任务中的证据
- [[zhou2025-learnable-physics-engine-critical]] — 迁移边界与批判性分析
- [[learnable-physics-engine]] — 方法实体
- [[cm-pinns]] — 本构约束 PINN 的对照方法
- [[mp-pde]] — message-passing PDE solver 对照
- [[message-passing-reach-contract]] — 图消息传播范围契约

^[sources/papers/zhou2025-learnable-physics-engine]
