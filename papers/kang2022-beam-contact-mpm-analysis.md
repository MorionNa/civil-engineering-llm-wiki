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
id: paper--kang2022-beam-contact-mpm-analysis
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
# Beam elements with frictional contact in the material point method

^[sources/papers/kang2022-beam-contact-mpm.md]

> 证据范围：以下内容依据论文预提取文本 `tmp/pdfs/Numerical Meth Engineering - 2021 - Kang - Beam elements with frictional contact in the material point method.txt`；原文 DOI 为 [10.1002/nme.6886](https://doi.org/10.1002/nme.6886)。页码均指该文本中的论文页码标记。

## 1. 工程背景

> **⚙️ 非线性类型：** 动力响应非线性（线性弹性）为本文对新 beam particle 的主分类。梁粒子在小应变下采用 Euler–Bernoulli 或 Timoshenko 梁的线性应力合力—共轭应变关系，但大位移、大转动、屈曲、碰撞和 Coulomb 摩擦使整体响应呈现几何与接触动力非线性；用于 CPDI2 固体对照的 neo-Hookean 应力更新另含本构非线性。本文不涉及 PDE 算子非线性，也不是 PINN 约束问题。

梁、纤维、杆件、晶格和织物中的细长构件，其整体响应不仅取决于单根构件，还取决于构件之间的接触。用连续体实体单元表示单根梁就可能需要大量单元，多个构件的计算成本更高（第 1–2 页，Introduction）。

MPM 将材料点作为 Lagrangian 离散，将运动方程放在固定 Eulerian 背景网格上，适合大变形、大转动和接触问题。本文把这一优势延伸到梁/框架结构，并与 [[entities/kang-beam-particle]] 和 [[kang2022-beam-contact-mpm-method]] 建立方法链路。

## 2. Research Gap

- 既有 MPM 对极大变形、转动和多体接触已有基础，但针对 rods、trusses、membranes、shells 等细长结构的开发相对少（第 2 页）。
- 用体积型 MPM 粒子表示梁会带来过多粒子；而普通 beam element 是非体积对象，碰撞检测和接触方向不易从 MPM 粒子域直接得到。
- 普通单速度场 MPM 天然施加无滑移接触；虽然多速度场算法可以结合 Coulomb 摩擦，但尚未解决梁的转动自由度、粒子域跟踪和空间接触范围的统一表示。

## 3. 科学问题

论文要回答的是：能否以少量、具有两个端节点的 reduced-order beam particle 表示梁的轴向、弯曲、扭转和大位移/大转动，同时在 MPM 背景网格上保持相邻梁粒子的连接性，并与实体 CPDI2 粒子自然耦合，处理滑动摩擦接触？

## 4. 研究目标

1. 在 MPM 中建立由两个端节点组成的三维 beam particle；每个端节点有 3 个平移和 3 个转动自由度。
2. 在背景网格上引入角速度和角加速度场，使弯曲转动自由度能够像线动量一样映射、更新和回写。
3. 通过梁粒子边缘的 spatial nodes 表示其空间范围，使非体积梁可以进行碰撞检测和摩擦接触。
4. 用一组解析解、有限元结果、已有实验/数值曲线和多体接触算例验证精度与适用性。

## 5. 方法机制

方法以三维 CPDI2 MPM 为背景。梁粒子中心存储质量、质心平移/角速度和历史状态；两端的位置描述轴向变形，端部转角描述曲率。端点的网格形函数采用两端点形函数的平均，使粒子跨越背景网格时仍可连续传递场量。

在网格上，梁粒子除了映射平动质量和动量，还映射质量惯性张量与角动量。网格角加速度由节点力矩平衡得到，再插值回梁粒子端部以更新转角。内部力和力矩通过局部梁切线刚度矩阵计算，并使用截面面积、惯性矩和极惯性矩等 section properties 表示不同截面。

接触部分采用 multi-velocity-field MPM。每个材料组在相同网格节点上保留独立速度场；由质量梯度估计接触法向，法向力阻止穿透，切向力按 Coulomb 摩擦截断。梁粒子在两端截面边缘布置 spatial nodes，再把质心试探速度或权函数近似的速度映射到这些节点，从而在背景网格节点计算梁—梁、梁—实体等接触。

详细的变量映射、角动量更新、梁切线刚度和接触步骤见 [[kang2022-beam-contact-mpm-method]]；该算法的可复用定义见 [[entities/kang-beam-particle]]。

## 6. 结果证据

- 纯弯曲悬臂梁：25 个梁粒子的端部位移—弯矩结果与精确解析解高度吻合；同一问题用 5 个梁粒子也得到文中所称的 practically identical result，但该结果未在图中展示（Fig. 4，第 13–14 页）。
- 空间六边形框架：提出方法的荷载—位移曲线与 Griggs 的实验研究以及已有数值分析结果比较良好，并覆盖屈曲前与屈曲后响应（Fig. 5，第 14 页）。
- 动力悬臂梁：20 个以上梁粒子即可得到与理论周期相符的振荡；50 个 MPM 梁粒子与 50 个 FEM 梁单元的响应吻合良好。理论最低频率为 0.16152 Hz，周期为 6.191 s（Fig. 6，第 14–15 页）。
- 45° 曲梁：10 个梁粒子的三向端部位移与 FEM 结果相同；5 个梁粒子也得到相同精度（Fig. 7，第 15–16 页）。
- 厚悬臂梁：Timoshenko 梁的含剪切变形响应接近 CPDI2 MPM；不含剪切的 Euler–Bernoulli 结果端部位移减小。梁粒子的应力轮廓接近 CPDI2 粒子（Figs. 8–10，第 15–16 页）。
- 纤维堆积、六边形框架落球和混合纤维算例展示了大转动下的滑动摩擦、接触点形成、折叠/变形以及摩擦对团聚和混合的影响（Figs. 11–15，第 17–20 页）。

## 7. 贡献

论文的主要新增是一个适用于 MPM 的两端节点 beam particle，而不是一个新的材料模型。具体贡献包括：

- 用端节点平移自由度表示轴向运动，用端节点转动自由度表示弯曲；
- 在背景网格上引入角速度场和角动量更新，使梁粒子之间可传递转动信息；
- 用梁刚度矩阵和质量惯性张量承接传统梁理论中的截面参数；
- 用 spatial nodes 近似梁的空间范围，并将多速度场摩擦算法用于梁接触；
- 将三维 CPDI2 实体粒子与梁粒子通过同一背景网格自然耦合（第 20–21 页，Summary and Conclusion）。

## 8. 核心知识点

1. MPM 的背景网格不仅可以承载线动量，也可以承载梁的角速度、角加速度和角动量场。
2. 对非体积梁，接触检测的关键不是把梁粗略当成实体，而是显式表示其截面边缘和空间范围。
3. 梁粒子采用 reduced-order 表示后，计算效率来自“少量粒子 + 梁截面性质”，但仍保留大位移/大转动运动学。
4. CPDI2 的域跟踪和多速度场接触，使梁—梁、梁—实体接触能够在相同的 MPM 框架中处理。
5. Euler–Bernoulli 与 Timoshenko 的选择会直接影响厚梁的端部位移；剪切变形不能对厚梁自动忽略。

## 9. Negative Knowledge

- 接触模型没有考虑接触过程中的 angular-momentum field，只使用梁与实体之间的平动速度计算接触力；滚动圆柱会滑动而不是沿平面滚下，这是论文明确给出的失败边界（第 12–13 页）。
- 多速度场 MPM 可能在接近物体之间留下数值 gap；减小网格可以缓解但提高成本。网格不能小于梁直径，否则大截面梁的接触可能发生在其体积内部而变成非物理接触。
- 梁粒子在本文实现中是大位移/大转动、小应变模型，初始长度、面积和惯性张量在仿真中保持常数；材料非线性仅被作者指出可通过扩展切线刚度实现，本文算例没有证明该扩展。
- 本文的精度证据主要是数值基准和图线比较，不等同于对所有截面、摩擦律、网格尺度和材料模型的普适验证。
- 提供文本没有披露公开代码 URL、版本、硬件环境或可下载数据集 URL，因此不能据此声称可一键复现实验。

## 10. 可迁移知识

- 在粒子—网格方法中，若对象具有额外的旋转自由度，可以把对应的惯性量和速度场作为与平动并行的网格状态。
- 对细长、薄或非体积对象，接触几何可用少量代表空间范围的节点耦合到统一接触算法。
- 减少离散点数量不应只依靠粗化实体网格；保留对象的结构刚度、截面性质和转动惯性，能够在低阶离散下维持结构响应。
- 通过同一背景网格让不同粒子类型共享接触机制，是把纤维/梁相与实体基体耦合到制造过程模拟中的直接路径。

## 11. 研究机会

以下是基于论文明确局限提出的后续问题，而非论文已完成的结果：

1. 为梁接触加入角动量/自旋的接触冲量，验证滚动、扭转接触和角动量守恒。
2. 研究 gap、梁直径与背景网格尺寸的定量误差，并发展自适应网格或更精细的接触几何。
3. 把材料非线性、损伤、塑性或截面随变形更新纳入梁粒子切线刚度，并设置独立基准。
4. 系统比较 Euler–Bernoulli、Timoshenko 以及更高阶梁理论在粗粒子和厚梁下的误差。
5. 对纤维—基体、织物、晶格和壳体场景建立公开的参数化基准与代码实现。

## 12. 可复现性

**等级：🟡 medium。** 论文给出了 CPDI2 背景、梁粒子状态变量、映射关系、接触力公式、算法步骤、主要材料参数和多组算例；数据可得性声明称大部分支撑结果的数据已在文章中呈现，其他数据可向通讯作者合理请求（第 21 页）。因此，按文中公式重建一个独立实现是可能的。

但提供文本未披露公开代码 URL 或数据仓库 URL，`code_url: []`、`dataset_url: []`；也未给出完整求解器版本、运行脚本、硬件/性能记录和所有网格/时间步敏感性文件。该等级表示“方法较详细但缺少公开代码/数据包”，不是已完成的独立复现声明。方法细节参见 [[kang2022-beam-contact-mpm-method]]，结果证据参见 [[kang2022-beam-contact-mpm-results]]。

## 关联页面

- [[kang2022-beam-contact-mpm-critical]]
