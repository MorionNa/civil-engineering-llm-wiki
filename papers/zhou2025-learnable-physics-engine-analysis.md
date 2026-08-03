---
id: paper--zhou2025-learnable-physics-engine-analysis
title: 'Zhou & Feng (2025) — The novel learnable physics engines for interpretable
  elastoplastic models of geomaterials: 论文分析'
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
- parallel-computing
legacy_failure_modes:
- limitation
- extrapolation-ability
legacy_datasets:
- synthetic-data
legacy_reproducibility: low
legacy_tags:
- neural-network
- deep-learning
- metamodeling
- message-passing
- physics-simulation
- scientific-machine-learning
- time-marching
- long-horizon-rollout
- parallel-computing
- learning-rate-schedule
- extrapolation-ability
legacy_sources:
- raw/papers/zhou2025-learnable-physics-engine.xml
evidence_scope: local workspace source record pending canonical verification
---

# The novel learnable physics engines for interpretable elastoplastic models of geomaterials based on the message passing neural network

> **论文信息（由 XML 核对）：** Xiao-Ping Zhou、Kai Feng（2025），*International Journal of Rock Mechanics and Mining Sciences*，194，106244，DOI: [10.1016/j.ijrmms.2025.106244](https://doi.org/10.1016/j.ijrmms.2025.106244)。原文的学习目标是 ordinary state-based peridynamics（OSB-PD）Drucker–Prager 弹塑性模型。

## 1. 工程背景 (Engineering Background)
> ⚠️ **非线性类型：材料本构非线性（主导），不是 PDE 算子非线性。** 本文要学习的是 geomaterial 的路径依赖塑性：应力–应变关系由弹性储能、Drucker–Prager 屈服面、塑性流动和历史内变量共同决定，塑性变形具有不可逆性。OSB-PD 的非局部运动方程和图上的消息传递只是承载材料状态更新的数值/图结构；它们不应被混同为 Burgers、Navier–Stokes 或 Allen–Cahn 中的 PDE 算子非线性。对于 PDE 算子非线性，PINN 通常把非线性项放进残差并用自动微分求导；对于本构非线性，网络必须显式表示 $\psi(\varepsilon)$、屈服函数和历史状态。本文属于后者。

岩土体、岩石和土体的塑性变形随加载路径演化，微观结构变化使得直接写出合适的本构表达式、标定材料参数以及在复杂边界值问题中稳定积分都很困难。传统数值模型可以保留力学结构，但在大量材料点、长时程或多组边界条件下计算成本高；纯数据驱动的应力–应变序列模型又容易成为黑箱，难以解释屈服面、硬化和力状态从何而来。

本文的工程问题是：能否把一个可解释的弹塑性本构模型重写为随时间演化的图，并让 GPU 上的图网络直接推进材料点、键伸长和力状态？这会把“材料积分器”和“全域数值演化”放进一个可并行的 learnable physics engine，而不是只训练一个事后回归器。

## 2. Research Gap

已有深度网络可以从应变/应力历史预测路径依赖塑性，但黑箱网络的可解释性和跨边界条件泛化较弱，而且常常还要嵌回 FEM 或其他传统求解器才能处理完整边值问题。另一类混合模型把弹性模块、屈服模块或本构约束显式放进网络，但通常只解决材料点级代理，未把它们和空间相互作用、状态更新及全域 forward prediction 统一起来。

本文针对的缺口有三层：

1. **结构缺口：** 需要把 OSB-PD 材料点及其邻域相互作用表示成可训练、可推进的图；
2. **本构缺口：** 不能让网络直接回归力而丢掉弹性储能和屈服面，应分别学习可解释的 elastic energy 与 yield function；
3. **时间缺口：** 屈服面的硬化和塑性状态是历史依赖的，需要在连续前向预测中更新，而不是只拟合独立快照。

这一路线与 [[cm-pinns]] 都强调显式本构结构，但本文的核心载体是 OSB-PD 图上的 MPNN 和材料状态推进；与 [[mp-pde]] 的图时间推进思想相近，却不等于学习一般 PDE 算子。

## 3. 科学问题 (Scientific Question)

核心科学问题不是“能否使用 MPNN”，而是：**在不牺牲弹塑性解释性的前提下，如何学习一个既能给出力和切线所需导数、又能随塑性内变量演化屈服面的材料—空间耦合推进器？**

具体而言，网络需要同时满足三种一致性：

- 能量函数的值、一阶导数和二阶导数分别对应储能、应力/力状态及切线信息；
- 屈服函数的零水平集要随累计塑性应变正确移动，不能只识别初始屈服面；
- 图消息更新产生的力和位置演化要与 OSB-PD 的材料点相互作用及塑性状态更新保持一致。

## 4. 研究目标 (Research Objective)

本文提出基于 message passing neural network 的可学习物理引擎，目标是从预处理的 OSB-PD Drucker–Prager 数据中构造一个可解释的弹塑性 surrogate。其研究目标包括：

- 用图节点表示材料点、边表示邻域键和相互作用；
- 用 H² Sobolev training 学习体积/偏差两部分 elastic energy，使其导数平滑；
- 把历史屈服面转换为应力空间的 signed-distance level set，并学习其随塑性状态的演化；
- 用 Newton 迭代求塑性乘子、更新塑性键伸长和力状态，再由图消息推进材料点位置；
- 在单点卸载、压头压入、圆形洞室开挖和边坡稳定四类数值例子中检验长期 forward prediction 与计算效率。

## 5. 方法机制 (Method & Mechanism)

方法是“物理结构 + 可学习函数 + 图状态推进”的组合，而不是一个端到端的无约束回归器。OSB-PD 提供材料点、邻域键、键伸长、体积膨胀和力状态；网络学习其中最难写死或最需要平滑导数的能量与屈服函数；算法仍显式执行塑性判断、Newton 更新和图状态演化。

计算链可压缩为：

OSB-PD graph（V, E）→ MPNN1 → bond stretch s 与体积/偏差状态 → MPNN2 + ψk/ψd + f̂(p,q,ζ) → elastic energy、force state、yield test、dλ、ζ、plastic stretch → MPNN3 → material-point force and updated graph state（V′, E′）。

其中 $\psi_k=\frac12 k\Theta^2$ 是体积储能，$\psi_d=\mu' \,\omega\cdot(s^d)^2$ 是偏差/畸变储能，力状态由 $T=\nabla_\eta\psi$ 得到；屈服函数写成 $F_y=J_2+\alpha_{DP}I_1-k_{DP}(\zeta)$。能量模块用 H² Sobolev loss 约束 $\psi$、$\partial\psi/\partial s$ 和 $\partial^2\psi/\partial s^2$；屈服模块用 level-set 的 signed distance 和 pseudo-time 演化表示硬化。→ [[zhou2025-learnable-physics-engine-method]]

## 6. 结果证据 (Result & Evidence)

XML 中报告的证据可分为四类：

1. **函数级测试：** 能量函数在独立测试数据上保持较高预测精度；对 ideal elastic–plastic 和 linear-hardening 两类数据训练的 $\hat f(p,q,\zeta)$，在单轴拉伸卸载测试中均能准确预测屈服函数。
2. **材料点级 benchmark：** 板的单轴拉伸—卸载连续预测中，等效应力误差很小；累计等效塑性应变有轻微误差积累，说明长期推进的误差主要先暴露在历史内变量上。
3. **全域边值问题：** 压头压入、圆形洞室开挖和边坡自重三例中，位移、等效/有效应力、静水压力和塑性应变场均与 OSB-PD 参考解相符。压头例 forward 2000 步后最大绝对误差比参考量小 1–2 个数量级；洞室例位移最大绝对误差约比实际值小 1 个数量级；边坡例最大位移误差约小 1 个数量级。
4. **速度与规模：** 在 AMD 5950X CPU、NVIDIA RTX 3080 GPU 上，以 100 个例子、每例 2000 步比较，作者称方法相对 OSB-PD 约快两个数量级。材料点数从 3600 增至 90,000 时，PD 时间从 200 s 增至 3000 s，而 surrogate 从 10 s 增至 45 s。→ [[zhou2025-learnable-physics-engine-results]]

这些数字证明的是“在同一 OSB-PD/Drucker–Prager 家族内的高效代理和长前向预测”，不是任意材料或任意 PDE 的误差保证。

## 7. 贡献 (Contribution)

本文的新增点不是简单地把 MPNN 用到岩土数据，而是把三个可解释结构接在一个图时间推进器中：

1. **可解释 elastic energy：** 由体积和偏差储能构造力状态，Sobolev training 同时约束值、梯度和 Hessian 相关信息；
2. **可演化 yield function：** 用 level-set signed distance 把屈服面硬化写成几何演化，再用自动微分参与 Newton 塑性更新；
3. **可学习 physics engine：** MPNN1/2/3 分别负责键伸长、材料本构与材料点位置/图状态更新，使材料点级本构和全域相互作用在同一计算图中运行；
4. **工程验证：** 在四类数值任务和 GPU 速度测试中展示长期 forward prediction 与规模扩展潜力。

与 [[cm-pinns]] 的显式本构 loss 相比，本文更强调“本构函数本身可解释 + 图状态可推进”；与 [[mp-pde]] 相比，本文的目标是材料本构非线性而不是通用 PDE 算子。

## 8. 核心知识点 (Core Knowledge)

- **先学能量，再取导数。** 学习 $\psi$ 而不是直接学习 $T$，把力状态和切线的来源固定在变分结构中；H² Sobolev loss 对需要平滑导数的本构代理尤其关键。
- **屈服面不是静态分类边界。** 通过 signed-distance level set 和 pseudo-time，硬化变成屈服面的演化问题；这比只拟合初始屈服面更接近路径依赖塑性。
- **图是离散相互作用的语言。** 节点/边把材料点及其邻域写入状态，MPNN 的聚合允许同一网络处理图上的局部相互作用；但物理传播范围仍受图连接和消息步数约束。
- **长期前向预测的关键在状态更新。** 论文保留塑性乘子、塑性键伸长和累计塑性状态的显式更新，因此可解释性来自“网络预测 + 算法状态机”的组合，而不是来自网络深度本身。
- **速度收益来自硬件与结构共同作用。** GPU 上的张量化图运算和固定局部相互作用带来规模优势，但速度结论必须连同硬件、PD 实现和数据规模一起读取。

## 9. Negative Knowledge

论文的成功边界需要和“高精度、长期、通用”这类宣传性表述区分开：

- **闭源/数据边界：** XML 的 data availability 仅写明“Data will be made available on request”，没有公开代码仓库、训练数据下载地址或预训练权重；因此目前不能声称结果可独立复现。
- **本构假设边界：** 验证对象是 OSB-PD 弹性模型 + Drucker–Prager 屈服准则，塑性状态主要由标量累计塑性应变/硬化描述；各向异性、复杂循环滞回、软化、损伤、率效应、孔压耦合和温度效应没有被证明。
- **外推边界：** 四个数值任务都来自同一类物理模型和合成数值数据；没有实验室三轴/真三轴数据、现场监测数据、不同材料参数族的系统 OOD 测试，也没有无限长 rollout 的稳定性证明。
- **数值边界：** 压头例已观察到累计塑性应变的轻微误差积累；“2000 步”是本文验证窗口，不等于任意时长都保持相同误差。
- **图传播边界：** OSB-PD 的邻域是非局部的，但 MPNN 的有效传播仍由边拓扑、邻域 horizon 和消息传递深度决定；当所需物理影响范围超过图的 receptive field 时，应参考 [[message-passing-reach-contract]] 做 reach/halo 审计。
- **速度对照边界：** surrogate 使用 RTX 3080，PD 参考实现的并行化、内存布局和 GPU 优化程度没有在 XML 中给出；因此不能把 10–45 s 对 200–3000 s 直接解释为对所有优化 PD/FEM 求解器的普适加速。

更直接地说，本文主要证明了“可解释的 OSB-PD 模型仿真器可以被压缩成高效图代理”，没有证明“网络发现了超出 Drucker–Prager 假设的新岩土本构规律”。→ [[zhou2025-learnable-physics-engine-critical]]

## 10. 可迁移知识 (Transferable Knowledge)

| 论文机制 | 可迁移对象 | 迁移时必须保留的契约 |
|---|---|---|
| $\psi$ 的值/梯度/Hessian 联合训练 | 超弹性、损伤、结构恢复力和 PINN 本构模块 | 能量导数必须对应力/切线，且要检查客观性、凸性或耗散条件 |
| level-set yield evolution | 多面屈服、损伤面、断裂准则、相变边界 | 需要定义 signed distance 的符号、伪时间/内变量和演化速度 |
| MPNN 的节点—边分工 | 不规则网格、颗粒/键模型、结构构件图 | 边特征要包含相对几何和必要物理状态，聚合要满足所需对称性 |
| Newton + 自动微分塑性更新 | 可微材料积分器、参数反演、物理约束训练 | 不能让黑箱输出绕过屈服判断；需审计根求解、分支和梯度稳定性 |
| GPU 上的长 rollout | 大规模材料点代理、数字孪生快速评估 | 必须同时报告硬件、图规模、步数、基线实现和内存成本 |

对当前知识库的直接启发是：用 [[cm-pinns]] 的本构一致性约束补足图代理的可验证性，用 [[mp-pde]] 的 rollout/分布偏移经验审查长期预测，再用 [[message-passing-reach-contract]] 检查局部图消息是否覆盖真实物理影响范围。[[bouc-wen-model]] 可作为另一类历史依赖本构的回归测试思想，但不能被当作 Drucker–Prager 岩土屈服面的等价替代。

## 11. 研究机会 (Research Opportunity)

1. **可复现基线：** 公开能量样本、level-set 样本、图构造、训练脚本、权重和误差曲线，并把 4 个例子的关键误差从“数量级”细化为逐步 RMSE、峰值误差和 drift 曲线。
2. **从单一 Drucker–Prager 扩展到多内变量：** 引入各向异性、软化/损伤、循环加载、率相关性、孔弹塑性和热–水–力耦合，同时保持能量、屈服面、流动法则和耗散可审计。
3. **数据与物理联合校准：** 用少量三轴或真三轴试验反演 $E,\nu,c,\phi$ 及硬化参数，把 level-set 网络从“拟合 OSB-PD 参考解”推进到“校准真实材料”。
4. **长时稳定性与误差控制：** 研究能量漂移、塑性耗散非负性、屈服面穿透、Newton 失败和图消息 under-reaching；对比不同消息深度、horizon、图粗化和 rollout 训练策略。
5. **跨模型对照：** 将 graph physics engine 与 [[cm-pinns]] 的 constitutive loss、[[mp-pde]] 的 pushforward/temporal bundling 组合或对照，明确哪些收益来自本构结构、哪些来自图并行化。
6. **实验与工程外推：** 在真实边坡、洞室监测和室内试验上检验不确定性；对材料参数、分辨率、边界和载荷路径做系统 OOD，而不是只改变边界几何。

## 12. 可复现性 (Reproducibility)

| 项目 | 说明 |
|---|---|
| **等级** | 🔴 低 |
| **官方代码** | []；XML 未给公开代码仓库或提交地址 |
| **数据集** | []；原文仅称数据可按请求提供，实验为 OSB-PD 合成数值例 |
| **已给出的实现信息** | PyTorch Geometric；MPNN2 的 $\phi^2_e$ 为 5 个 30 单元隐藏层、Tanh，$\phi^2_v$ 结构相近；Adam 初始学习率 0.0005，每 100 epoch 乘 0.1；Sobolev 权重 $\gamma_1=\gamma_2=\gamma_3=1$ |
| **关键缺口** | 数据规模、归一化、训练/验证划分、epoch/停止准则、随机种子、完整网络参数、图边方向与内存策略、逐步误差和代码版本未在 XML 中完整给出 |

因此，本文可按公式和文字重建方法原型，但不能仅凭公开 XML 独立生成与论文图 8–19 一致的全部曲线。

## 关联页面

- [[zhou2025-learnable-physics-engine-method]] — MPNN、能量 Sobolev training、level-set 屈服函数与算法流程
- [[zhou2025-learnable-physics-engine-results]] — 四类实验、误差数量级和 GPU 速度对照
- [[zhou2025-learnable-physics-engine-critical]] — 贡献、负知识、迁移和后续研究机会
- [[learnable-physics-engine]] — 本文提出的可学习物理引擎实体页
- [[cm-pinns]] — 显式本构约束的 PINN 对照
- [[message-passing-reach-contract]] — 图消息传播范围审计
- [[mp-pde]] — 图时间推进但目标不同的 PDE 代理
- [[bouc-wen-model]] — 历史依赖本构的对照实体

^[sources/papers/zhou2025-learnable-physics-engine]
