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
id: paper--chihadeh2023-implicit-mpm-fem-fracture-analysis
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
# A coupled implicit MPM-FEM approach for brittle fracture and fragmentation

^[sources/papers/chihadeh2023-implicit-mpm-fem-fracture.md]

> 论文概览：Chihadeh、Coombs 与 Kaliske 在 *Computers and Structures* 288 (2023), 107143 中提出一种隐式、整体式的 MPM–FEM 耦合框架，用界面 bond elements、罚函数接触和 eigenfracture 驱动的有限元到物质点转换处理大变形、脆性断裂与碎片运动。

DOI：<https://doi.org/10.1016/j.compstruc.2023.107143>
原文证据：`raw/papers/1-s2.0-S0045794923001736-main.pdf`；本次读取的预提取文本为 `tmp/pdfs/1-s2.0-S0045794923001736-main.txt`。

相关页面：[[chihadeh2023-implicit-mpm-fem-fracture-method]] · [[chihadeh2023-implicit-mpm-fem-fracture-results]] · [[chihadeh2023-implicit-mpm-fem-fracture-critical]] · [[entities/chihadeh-implicit-mpm-fem]]

## 1. 工程背景

> **⚙️ 非线性类型：** 材料/本构非线性（文中同时明确包含几何非线性，并采用 St. Venant–Kirchhoff 材料模型；非线性不是 PDE 算子学习，也不是“线性弹性下仅动力响应非线性”类别）。断裂、侵蚀和接触还会带来离散状态转换。

工程结构在冲击、断裂和碎片化过程中会产生极端变形。FEM 在单元严重畸变时会失效，而 MPM 能通过材料点和重置背景网格处理大变形。

论文指出 MPM 通常比 FEM 更耗时、精度较低且数值稳定性较弱，因此希望让 MPM 只覆盖极端变形区域，让 FEM 留在远场或小变形区域。

隐式 MPM 允许使用较大的时间步长；但 MPM 与 FEM 的界面位移一致性、不同网格尺寸下的连通性以及两种离散体之间的接触仍需处理。

## 2. Research Gap

论文回顾的已有耦合工作很少：有的只处理小位移有限元，有的采用显式时间积分，有的只处理桁架有限元。

因此，文中要补的缺口是一个可用于大变形/断裂场景的隐式、整体式 MPM–FEM 耦合，而不是只在小位移或显式框架中连接两种方法。

论文还把“预先固定哪些区域用 MPM、哪些区域用 FEM”的人工划分视为限制，提出在计算过程中把被 eigenfracture 侵蚀的 FE 转换成材料点。

## 3. 科学问题

核心问题是：如何在同一个非线性求解系统中，把 MPM 激活背景单元、连续体 FE 和界面连接统一起来，同时避免界面滑移和 MPM–FEM 物体互相穿透？

另一个问题是：当 FEM 网格比 MPM 背景网格粗时，仅在 FE 节点放置连接是否足以维持边界连通性？

最后，断裂区域何时从 FE 表示切换为材料点表示，才能保留裂纹传播并把 MPM 限制在需要大变形的区域？

## 4. 研究目标

1. 用 bond elements 和罚函数实现隐式 MPM–FEM 的整体式耦合。
2. 为 MPM 与 FEM 之间的接触加入接近条件和相向运动条件，并用法向罚项阻止穿透。
3. 用 eigenfracture 的 intact/eroded 判定自动触发 FE 到材料点的转换。
4. 通过梁、应力波、L 形板、裂纹分叉和冲击板数值例子展示该框架的实现能力。

## 5. 方法机制

MPM 部分采用隐式求解和 CPDI2；每个时间步把材料点数据映射到背景网格，求解节点未知量，再把位移/加速度映射回材料点并重置网格。

非线性隐式 MPM 使用几何非线性、St. Venant–Kirchhoff 材料、隐式 Newmark 时间离散和 Newton–Raphson 线性化。

界面 bond element 以 FE 节点或 FE 表面中间点与激活 MPM 单元位移的差为 slip，以用户给定的大罚刚度抑制 slip。

当 FE 网格比 MPM 网格粗时，引入 intermediate bond elements；接触 bond elements 另用距离和相向运动两个条件激活。

eigenfracture 将满足裂纹驱动能量阈值的单元标为 eroded；这些单元被排除并转换为材料点，必要的状态数据通过形函数赋给材料点。

方法方程、变量和转换顺序见 [[chihadeh2023-implicit-mpm-fem-fracture-method]]。

## 6. 结果证据

在 1 × 5 cm 动力悬臂梁上，MPM、FEM 和 MP–FE 三种离散的梁端位移曲线相同，支持 nodal bond element 的实现（Fig. 2–3）。

应力波基准中，MPM 与 FEM 网格同尺寸时波平滑通过界面；FE 网格较粗且没有 intermediate bond elements 时波在界面处失真；加入中间 bond 后恢复正确传播（Fig. 13–16）。

同一基准的 MPM–FEM 结果与仅 FEM 结果在拉伸和压缩下“very good agreement”；网格细化时归一化应力趋于解析传播关系，材料点数 2×2 与 3×3 的影响相较单元尺寸很小（Fig. 16–18）。

接触基准中，移动块在 0.4 s、0.8 s、1.2 s 分别撞击框架左、下、右边界；接触 bond 在接近且相向运动时激活，位移/速度曲线呈现反弹（Fig. 8–9）。

L 形板的裂纹形态与文献中的实验结果及数值结果相符；动力预裂板出现从初始缺口尖端直线传播后再分成两支的裂纹路径（Fig. 20–25）。

300 × 300 × 25 mm 板的冲击例子显示冲击器穿透板材；冲击后速度降低，断裂阶段后重新趋于近似恒速且加速度趋近零（Fig. 26–29）。

全部数值例子及图表证据集中整理在 [[chihadeh2023-implicit-mpm-fem-fracture-results]]。

## 7. 贡献

论文的主要方法贡献是把激活 MPM 单元、连续体 FE 和 bond element 组装进一个同时求解的单一系统，而不是分步传递两种方法的结果。

第二个贡献是用 nodal 与 intermediate 两类 bond elements 处理同尺寸和异尺寸网格的界面连通性。

第三个贡献是把接触激活逻辑与同一 bond-element 形式结合，并通过法向罚项避免 MPM–FEM 穿透；该例子明确设置切向系数为零，即无摩擦。

第四个贡献是让 eigenfracture 的 eroded FE 成为运行时转换触发器，使初始模型可以从全 FEM 开始。

## 8. 核心知识点

- MPM 的优势在大变形区域，FEM 的优势在远场；区域耦合的关键不是简单拼接网格，而是约束界面自由度。
- CPDI2 的粒子域角点能随网格变形更新，这一点被论文视为保持 FE 边界和材料点域边界连接所必需。
- bond element 的基本机制是 `slip → penalty stress → coupled force/stiffness`，并在全局系统中同时装配。
- 粗 FE 与细 MPM 的界面需要 intermediate bonds；只放 FE 节点连接会造成应力波失真。
- eigenfracture 把裂纹表示为 eroded elements，从而可直接作为 FE→MPM 转换判据。

## 9. Negative Knowledge

- 论文明确观察到：粗 FE 网格没有 intermediate bonds 时应力波不能正确传播；该结构不是可省略的装饰项。
- 论文实践建议 MPM 网格应比 FE 网格更细或至少不更粗；FE 比 MPM 更细的耦合情形没有被明确研究。
- 接触例子令 `C_t = 0`，没有展示摩擦接触；不能把该结果外推为已验证的摩擦 MPM–FEM 接触。
- bond penalty 系数是用户定义的，但提供文本没有给出各数值例子的具体 penalty 参数；罚刚度敏感性也没有系统报告。
- 论文使用 eroded/intact 二元状态，并指出为避免零刚度通常使用很小的刚度；不同能量 split 对侵蚀材料压缩响应的影响需要谨慎解释。
- 论文给出的是数值图形、曲线和模型规模，没有报告统一的误差表、运行时间/加速比或内存节省量；“优化”目标未被这些量化指标完整验证。
- 所有算法由作者的 in-house Fortran MP-FE code 实现，但提供文本没有公开代码 URL；论文声明研究没有使用数据集。

## 10. 可迁移知识

1. 在混合离散方法中，把界面连续性写成可装配的局部连接单元，可复用现有 FE 全局装配和 Newton 求解器。
2. 连接单元的密度应随两侧离散尺度匹配：节点约束不足时，用表面中间连接补足空间连通性。
3. 将“失效状态”作为表示切换事件，可以把高成本/高鲁棒性离散限制在局部，而不必一开始把全域都建成 MPM。
4. 接触激活逻辑应至少区分“几何接近”和“相向运动”，否则仅按距离激活会把正在分离的邻近体误判为接触。
5. 这一设计可迁移到以畸变或损伤为转换判据的其他问题，但论文只在 eigenfracture 判据下展示了实现。

## 11. 研究机会

- 公开 Fortran 实现、输入文件和自动化后处理，形成可重复的 MPM–FEM 断裂基准。
- 对 penalty、MPM/FEM 网格比、材料点数和 eigenfracture split 做系统敏感性与误差分析。
- 将 `C_t = 0` 的无摩擦接触扩展到有摩擦、粘着/分离和多体碎片接触，并给出独立接触基准。
- 比较不同转换触发器（畸变、损伤、能量）对计算成本、裂纹路径和碎片运动的影响。
- 对应力波、L 形板、裂纹分叉和三维冲击建立统一的公开实验/解析对照指标，而非只比较图形。

这些是基于论文未覆盖部分提出的研究方向，不是论文已经报告的结果；贡献、边界和机会的批判性展开见 [[chihadeh2023-implicit-mpm-fem-fracture-critical]]。

## 12. 可复现性

按本知识库分级，本论文为 **medium**：正文给出了核心方程、耦合逻辑、若干材料/网格/时间步参数和图表对应关系，足以重建方法原型；但实现是 in-house Fortran code，`code_url` 为 `[]`，且论文声明 `No data was used for the research described in the article`，`dataset_url` 为 `[]`。

仍无法从提供文本确认的复现要素包括：各算例的 penalty 数值、完整求解器容差/收敛准则、全部 eigenfracture 能量 split 的选择细节，以及可直接运行的输入文件。因此这里的 medium 是“方法披露较充分但没有公开代码/数据”的等级，不等同于独立复现已完成。

复现实验的最小证据路径是先重建 [[chihadeh2023-implicit-mpm-fem-fracture-method]] 中的整体装配和转换流程，再按 [[chihadeh2023-implicit-mpm-fem-fracture-results]] 的 Fig. 3、Fig. 16、Fig. 18、Fig. 20–29 设置基准。
