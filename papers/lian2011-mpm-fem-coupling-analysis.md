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
results:
- symmetric plate impact
- asymmetric plate impact
- sphere rolling
- thick-plate perforation
- water-column fluid-structure interaction
failure_modes:
- mesh-ratio mismatch
- interface oscillation
- background-grid penetration
- missing public implementation
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--lian2011-mpm-fem-coupling-analysis
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
- impact
- fluid-structure-interaction
- numerical-methods
- local multi-mesh contact coupling
- central difference time integration
- 8-node hexahedral FEM
- MPM background-grid mapping
- Coulomb friction
- symmetric plate impact
- asymmetric plate impact
- sphere rolling
- thick-plate perforation
- water-column fluid-structure interaction
- mesh-ratio mismatch
- interface oscillation
- background-grid penetration
- missing public implementation
- Computer Methods in Applied Mechanics and Engineering
sources:
- sources/papers/lian2011-mpm-fem-coupling.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Coupling of finite element method with material point method by local multi-mesh contact method

^[sources/papers/lian2011-mpm-fem-coupling.md]

> 论文事实来自提供的 PDF 预提取文本（13 页）；DOI: [10.1016/j.cma.2011.07.014](https://doi.org/10.1016/j.cma.2011.07.014)。

## 1. 工程背景

> **⚙️ 非线性类型：** 材料/本构非线性。论文的核心还包含接触与大变形带来的几何/边界非线性，但不是 PDE 算子非线性。板撞击和滚动案例包含线弹性工况；穿孔案例使用弹塑性与 Johnson–Cook 本构，水柱案例使用状态方程。因此不能把“MPM/FEM 耦合”本身归类为 PDE 算子非线性。

传统 FEM 在极端变形时容易出现网格畸变和单元纠缠，导致数值困难；MPM 通过粒子携带历史变量、每步重建规则背景网格来处理大变形。

相反，MPM 的粒子积分精度和效率通常低于 FEM 的 Gauss 积分，并且同时保存粒子与背景网格，存储开销更大。论文据此把小变形体交给 FEM，把极端变形体交给 MPM（摘要；第 1 节）。

本文提出在 MPM 背景网格上处理 FEM 体与 MPM 体接触的局部多网格接触方法，并将 8 节点六面体单元并入三维显式 MPM3D 代码，形成 coupled finite element–material point（CFEMP）方法。

## 2. Research Gap

已有网格无关方法与 FEM 的耦合多采用主从接触、混合插值、拉格朗日乘子或过渡单元。此前 MPM 相关工作主要处理显式 material point finite element、混合杆单元等，并没有在本文目标场景中直接给出“一个小变形 FEM 体 + 一个极端变形 MPM 体”的接触耦合流程。

论文要解决的是：两种离散方式的质量、动量和接触力如何投影到同一背景网格；如何既保持 FEM 的小变形精度，又允许 MPM 体发生极端变形；以及如何在不穿透的条件下加入摩擦滑移（第 1、3 节）。

## 3. 科学问题

核心问题是一个显式、非共形界面上的动量协调问题：若两个物体对同一背景网格点有质量和动量贡献，如何判断真实接触、构造法向/切向接触力，并把力反向施加到 MPM 粒子和 FEM 接触节点。

该问题还受到三个离散尺度因素约束：FEM 单元尺寸与 MPM 网格单元尺寸的比值、临界时间步长的同步，以及粒子积分与单元积分之间的精度差异。

## 4. 研究目标

论文目标是建立一个可用于三维显式计算的 FEM–MPM 接触耦合方案，具体包括：

- 把接触界面的 FEM 节点标记为 hybrid nodes，并像粒子一样在 MPM 背景网格上建立动量方程。
- 用同一网格点上的分体速度、质量和动量检测接触，并施加满足不可穿透条件的法向力。
- 用 Coulomb 摩擦模型处理粘着与滑移。
- 在 MPM 的每步网格重建机制下修正动量，避免应力更新时重新产生界面扰动。
- 用板撞击、滚动、穿孔和流固耦合例子验证精度、效率和鲁棒性（摘要；第 3–5 节）。

本文的耦合对象是两个相互接触的物体，而不是同一物体内部的 FEM/MPM 区域拼接；文中把 FEM 体记为 `X_F`，MPM 体记为 `X_M`。

“local multi-mesh”指接触计算使用局部公共背景网格，不表示两侧采用完全相同的网格，也不等同于全局重网格或通用多物理场接口。

本文的核心判据是界面动量和不可穿透约束；材料本构、状态方程、人工体积黏性和 hourglass control 则作为两侧主体求解的一部分。

## 5. 方法机制

MPM 体的粒子质量和动量通过 8 点六面体形函数映射到背景网格；FEM 体只有接触表面的节点参与该接触映射，成为 hybrid nodes。两个子域先各自独立计算 trial nodal variables，再在公共网格点上解决接触。

接触检测使用两个物体在同一网格点的分体速度。FEM 表面法向来自包含 hybrid nodes 的单元面法向求和，MPM 表面法向由粒子质量梯度近似；随后还检查真实物理距离，以避免背景网格造成过早接触（第 3.2 节，式(30)–(33)）。

法向接触力由更新后的不可穿透约束求得；切向先按无滑移条件计算粘着力，再以 `μ f_n` 限幅得到 Coulomb 滑移力。为了适应每步丢弃并重建背景网格，算法先用法向力的动量修正项调整 MPM 网格动量和 FEM hybrid-node 速度，再更新应力（第 3.3–4 节）。

应力用中心差分时间积分、Jaumann 应力率和各物体对应的本构关系更新；FEM 单元中心计算应变率/自旋，MPM 粒子处计算应变率/自旋。FEM 采用一点评分积分并实现 standard 与 Flanagan–Belytschko hourglass control。

## 6. 结果证据

五类三维数值例子均报告了与解析解或文献结果的总体一致性：

1. 对称和非对称板撞击的应力波形、分离时间与一维解析解吻合；CFEMP 在给定设置下比全 MPM 使用更少粒子并降低 CPU 时间（图 5、8；表 1、2）。
2. 斜板上的弹性球质心轨迹与刚体动力学解析式吻合；CFEMP 的 CPU 时间低于全 MPM（图 11；表 3）。
3. 厚板穿孔中，网格细化使 CFEMP 残余速度从 286 m/s 收敛到 456 m/s，实验值为 455 m/s；全速度组的结果也接近实验（表 6、7）。
4. 穿孔图像中的弹丸形状、弹道和塑性应变分布与实验观察一致，最细网格案例的能量误差不超过 5.5%（图 14–17）。
5. 水柱撞击弹性障碍物的自由表面、障碍物变形和左上角位移历史与 PFEM 及已有数值结果相符，但论文明确指出没有可用实验结果（图 19–21）。

详尽的工况、网格、表格数字与图表证据见 [[lian2011-mpm-fem-coupling-results]]；方法实现见 [[lian2011-mpm-fem-coupling-method]]。

## 7. 贡献

论文的直接贡献是 local multi-mesh contact method 在 FEM–MPM 接口上的实现：把接触 FEM 节点变成 hybrid nodes，在 MPM 背景网格点上统一处理接触动量，并将法向与切向接触力分配回两种离散。

该方案把 FEM 的小变形精度和 MPM 的极端变形能力放在同一个显式计算框架中；论文还给出了可执行的 11 步数值实现流程，以及关于单元/网格尺寸比和时间步长同步的经验边界。

## 8. 核心知识点

- 选择离散方法应按局部变形 regime 分工，而不是强迫整个结构使用同一离散。
- 非共形界面可以通过“分体投影到公共背景网格 + hybrid nodes”交换动量，不需要共节点网格。
- 接触检测必须区分两个物体在同一网格点的速度，不能只用总速度场。
- MPM 每步重建网格会重新破坏不可穿透状态，因此应在应力更新前做法向动量修正。
- `R = FEM element size / MPM cell size` 是关键离散控制量：文本中图 6 报告 `R < 2` 时结果与解析解较好，`R > 2` 出现明显振荡；并报告 `R > 1` 时可观察到穿透。

关联方法实体：[[entities/lian-local-multimesh-contact]]。

## 9. Negative Knowledge

- 论文只验证了特定的八节点六面体、中心差分、显式背景网格组合，不能据此声称任意高阶单元、任意粒子形函数或隐式耦合都适用。
- 网格不匹配会在 MPM 接口附近产生应力波形突起和振荡；尺寸比过大时还会出现穿透（图 5、6）。
- 结论给出“单元尺寸/网格尺寸应小于 2”这一保守要求，但图 6 的文字还报告 `R > 1` 已可观察到穿透；因此工程使用应按更严格的观测边界校核，而不能把 `R < 2` 当成充分保证。
- MPM 的粒子积分精度、双重数据存储和接触网格尺度限制，意味着 CFEMP 不会在所有问题上都比纯 FEM 或纯 MPM 更快。
- 穿孔例子忽略弹丸与靶板摩擦；水柱例子没有实验验证；论文未披露公共代码仓库或可下载数据集。

## 10. 可迁移知识

这套设计可迁移到需要局部极端变形、局部小变形和接触传力的多离散问题：先按变形尺度分配方法，再用公共支撑域交换界面动量；接触约束应在主体求解和应力更新之间显式插入。

具体可迁移的工程检查包括：

- 在计算前检查两类离散的特征长度与材料波速，使用全局最小临界时间步长。
- 用分体质量/动量建立接触检测，不用把两种离散合成一个虚假的材料场。
- 把界面误差、能量误差、穿透量和尺寸比作为独立验收指标。
- 当摩擦状态可能改变时，先算 stick 力、再做 Coulomb 限幅，比直接指定滑移速度更可审计。

这些原则与 [[entities/lian-local-multimesh-contact]] 及本文 [[lian2011-mpm-fem-coupling-critical]] 的边界分析相互补充。

## 11. 研究机会

以下是基于论文边界提出的研究机会，而非论文已报告结果：

1. 建立对尺寸比、粒子数、界面方向和材料波阻抗的系统收敛/误差模型，解释图 6 的振荡与穿透阈值。
2. 设计自适应局部网格或粒子分辨率，使公共背景网格不再成为接触精度的主要瓶颈。
3. 引入能量-动量一致的接触修正和界面振荡抑制，特别是对强冲击、摩擦转换和塑性软化。
4. 公开 MPM3D 的可运行实现、输入文件和基准数据，补足论文当前的复现缺口。
5. 将该接口扩展到更多本构、断裂/损伤和多体接触，并用实验数据而不只是 PFEM/解析解进行验证。

## 12. 可复现性

**等级：🟡 medium。** 论文披露了控制方程、映射公式、接触力公式、11 步实现流程、时间步长条件、多个材料常数、网格/粒子尺寸和表格结果，足以支持有经验的计算力学研究者重写方法。

但提供文本中没有公共代码 URL、数据集 URL 或 MPM3D 的下载入口；`code_url: []`、`dataset_url: []`。水柱例子还依赖文献对比而无实验数据。因而无法从提供文本确认独立复现所需的完整代码、输入文件、接触阈值实现细节和所有初始几何文件。

复现优先级建议为：先重现对称板撞击的分离时间，再测试图 6 的尺寸比敏感性，最后复现穿孔表 6/7 和水柱图 19/20；每一步都记录界面穿透、能量误差和时间步长。
