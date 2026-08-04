---
type: paper-analysis
title: Formalizing Dimensional Analysis Using the Lean Theorem Prover
authors:
- Maxwell P. Bobbin
- Colin Jones
- John Velkey
- Tyler R. Josephson
year: 2025
venue: arXiv preprint [physics.chem-ph]
tags:
- domain/ai4s
- evidence/paper
methods:
- formalization
- theorem-proving
- proof-assistant
- lean-4
- mathlib
- dimensional-analysis
- physics-formalization
results:
- formalization
- theorem-proving
- dimensional-analysis
- physics-formalization
- formal-science
failure_modes:
- formalization
- proof-assistant
- dimensional-analysis
- reproducibility
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--bobbin2025-dimensional-analysis-analysis
status: active
project: civil-engineering-llm-wiki
keywords:
- formalization
- theorem-proving
- proof-assistant
- lean
- lean-4
- mathlib
- physics-formalization
- dimensional-analysis
- formal-science
- reproducibility
- arXiv preprint [physics.chem-ph]
sources:
- sources/papers/bobbin2025-dimensional-analysis.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Formalizing Dimensional Analysis Using the Lean Theorem Prover

^[sources/papers/bobbin2025-dimensional-analysis.md]

论文作者为 Maxwell P. Bobbin、Colin Jones、John Velkey 和 Tyler R. Josephson。预提取文本标注为 arXiv:2509.13142v1、[physics.chem-ph]、2025 年 9 月 16 日；论文使用 Lean 4 和 Mathlib 4.23.0-rc1，将维度、物理变量、SI 单位、Buckingham Π 定理以及 Lennard–Jones 势写入 Lean 的类型与定理系统。方法展开见 [[bobbin2025-dimensional-analysis-method]]，证据清单见 [[bobbin2025-dimensional-analysis-results]]，算法实体见 [[entities/lean-dimensional-analysis]]。

原始来源：<https://arxiv.org/abs/2509.13142>。

## 1. 工程背景

> **⚙️ 非线性类型：** **本文不涉及物理非线性。** 论文研究的是 Lean 中的维度代数、类型约束和形式证明；Lennard–Jones 表达式虽对距离 (r) 含 ((\sigma/r)^{12}) 与 ((\sigma/r)^6) 的代数非线性，但没有求解非线性 PDE、材料/本构演化或动力响应，因此不归入三类物理非线性。它与材料/断裂建模的 [[chihadeh2023-implicit-mpm-fem-fracture-analysis]] 和显式断裂数值方法的 [[lv2025-phase-field-gimp-fracture-analysis]] 属于不同的分类对象；当前工作区没有可核实的 PDE 算子非线性对照页。

维度分析用于检查物理方程的维度齐次性，是公式构造和验证物理规律的基础。论文指出，物理变量同时携带数值和维度，而维度不随单位选择改变；如果关系式两侧的维度不一致，则不能代表物理上有效的关系。工程上，这意味着把“单位错误”从运行后的数值异常前移到定义和证明阶段。

论文把这一问题放到 Lean 4 的内核检查环境中：除了承载可执行或可计算的数值，系统还要证明维度操作的代数性质，以及具体物理式子的维度一致性。它不是有限元、材料点法或实验数据研究，而是面向形式化科学软件的基础库工作。

## 2. Research Gap

- 既有语言和程序库已经用类型系统或符号工具处理单位、维度和 Buckingham Π 定理，但论文认为这些实现没有在一个形式证明环境中同时表达维度分析的数学性质。
- 特别是，维度在乘法下构成 Abelian group（交换群）的事实，以及物理变量、单位和维度齐次性的组合，并未被论文作者找到一个由 Lean 内核检查的统一实现。
- 论文还把前一项 Lean 科学计算工作中的 Lennard–Jones 能量计算扩展到带维度和单位的物理变量，以补上“能算”与“能证明维度正确”之间的缺口。

## 3. 科学问题

核心问题是：如何在不把基础维度系统写死的前提下，把维度运算、物理量的数值部分、SI 单位和物理方程的齐次性编码为 Lean 可检查的对象？

论文将物理变量抽象为数值与维度的组合 (P=\langle V,D\rangle)，并让运算分别作用于数值和维度。维度本身表示为从基础维度到指数的映射 (D=B\to E)，从而把“维度齐次”转化为可由类型和定理证明处理的等式问题。

## 4. 研究目标

1. 在 Lean 4 中定义可扩展的维度和基础维度系统，而不是只支持固定的七个 SI 维度。
2. 证明维度在乘法、除法、幂和逆运算下满足 Mathlib 的交换群接口。
3. 用同一基础构造派生维度、维度齐次性定理、带维度的物理变量和 SI 基准单位。
4. 实现 Buckingham Π 定理所需的维度矩阵、秩和核的表示。
5. 用 Lennard–Jones 势证明零能量分离和导数/力定律，同时检查表达式的维度一致性。

## 5. 方法机制

方法主线是“抽象基础维度 → 指数映射 → 类型类运算 → 交换群证明 → 分级物理变量 → 自动维度证明”。详细定义、Lean 代码片段和依赖关系见 [[bobbin2025-dimensional-analysis-method]]。

- 维度定义为 `dimension B E := B → E`，其中指数类型 `E` 具有 `CommRing` 结构；`B` 保持抽象，以容纳运动学系统、时空系统或 ISQ 系统。
- 乘法把指数逐点相加，除法逐点相减，幂把指数乘以幂指数。加法与减法只允许相同维度，并用 `Classical.epsilon` 表达这种条件定义。
- `HasBaseLength`、`HasBaseTime` 等类型类把不同的基础维度类型映射到同一概念基础维度；论文还定义了七个 ISQ 基础维度和 Currency 示例。
- 通过 `CommGroup (dimension B E)` 实例，Lean 可以复用交换群定理和运算符，而不是为每个具体物理系统重复证明。
- `PhysicalVariable d` 是带维度索引的结构，字段为数值；乘法、除法、加法和幂的结果类型携带对应的维度表达式。
- 当两个维度在命题上相等、但不是定义上同一表达式时，`cast` 与 `evalAutoDim` 尝试自动完成维度等式证明，例如 (F=ma) 的维度转换。
- SI 基础单位和基本常数被表示为带维度的 `PhysicalVariable`；补充信息以矩阵秩和线性映射核实现 Buckingham Π 定理，并以除法规则实现单变量导数的维度。

## 6. 结果证据

论文给出的主要证据是 Lean 定义、交换群实例、维度齐次性定理和 Lennard–Jones 定理，而不是数值基准或误差曲线。结果页 [[bobbin2025-dimensional-analysis-results]] 按正文页码和补充信息页码列出这些证据。

- 维度的乘法交换律、单位元、结合律、逆元以及除法与逆元的关系被分别写成 Lean 定理，并组装为 `CommGroup` 实例（正文第 7–9 页）。
- `accel_eq_vel_div_time` 证明加速度等于速度除以时间；`reynolds_eq_dimless` 证明 Reynolds 数的维度为无量纲（正文第 9–10 页）。
- 物理变量的分级结构让同维度加法成为类型可表达的约束；作者报告 `evalAutoDim` 在“所有测试的情况”中足以闭合目标，但未给出测试数量、运行时间或失败率。
- Table 3 给出 2019 SI 七个基本单位的定义，代码进一步定义秒、米、千克、安培、开尔文、摩尔、坎德拉及若干基本常数（正文第 12–13 页）。
- Lennard–Jones 示例给出 (r=\sigma) 时零势能的定理，以及对距离求导得到力表达式的定理；预提取文本明确省略了两段证明主体并指向 GitHub（正文第 14 页）。

## 7. 贡献

- 提出以 `B → E` 为核心、由类型参数控制基础维度和指数类型的 Lean 维度表示。
- 将维度的代数性质接入 Lean 的 `CommGroup`，使维度运算可以使用统一的类型类接口和证明策略。
- 把物理变量的数值与维度放进分级结构，使部分维度齐次性约束在类型层面出现，而不是只依赖事后检查。
- 将 SI 单位、物理常数、Buckingham Π 定理和 Lennard–Jones 应用放到同一个形式化框架中。
- 形成一个可供后续形式化科学库和带维度正确性保证的科学计算环境复用的基础。

## 8. 核心知识点

1. 维度可以视为基础维度到指数的函数；派生维度不是另起一套对象，而是通过函数上的指数运算得到。
2. 维度乘法对应指数相加，维度除法对应指数相减，维度幂对应指数的标量乘法；这使许多物理维度恒等式归约为环上的逐点恒等式。
3. 把基础维度保留为类型参数，并通过 `HasBase...` 类型类提供概念接口，可以在不同基础系统间复用定理。
4. 物理变量的加法结果要求相同维度；乘法结果的维度是两个输入维度的乘积；幂运算的输出维度依赖幂指数，因此不能直接套用普通 `Pow` 类型类接口。
5. Buckingham Π 定理的可形式化核心是维度矩阵的秩和线性映射的核：可形成的无量纲参数数量为参数数减去矩阵秩。
6. 对带维度变量求导时，导数维度按“函数输出维度除以输入维度”处理；补充信息把这个规则和数值导数分开编码。

## 9. Negative Knowledge

- 论文没有给出运行时间、内存、证明搜索成功率、测试用例数量或与 SymPy、BuckinghamPy、Haskell 等系统的定量比较；不能把“形式化完成”解释成数值性能优越。
- 预提取文本只说证明托管在 GitHub，没有给出可核实的仓库 URL、commit、许可证或完整构建命令，因此 `code_url` 保持 `[]`。
- Lennard–Jones 两个定理的证明主体在文本中以“rest of proof on GitHub”省略；仅凭提供文本无法独立审计每一步证明脚本。
- `evalAutoDim` 是一串尝试性 tactic 组合，作者报告所有测试情况均可闭合，但没有给出完备性定理或失败边界清单；不能将其视为对任意维度等式的通用决策程序。
- 论文没有实验数据集、观测误差、单位换算基准或真实工程案例；SI 单位和 Lennard–Jones 示例是形式化定义/定理示例，不是实验验证。
- `Classical.epsilon` 带来 `noncomputable` 定义；物理变量的值类型和指数类型在实现中被安排为相同类型，这些设计选择可能限制直接迁移到更丰富的量纲/数值类型组合。

## 10. 可迁移知识

- 在形式化科学中，可把“语法/数据结构—语义对象—证明接口”分层；本论文的维度函数和物理变量分级结构可作为其他物理量库的类型设计模板。
- 对具有代数闭包的科学对象，先证明基础运算满足 Mathlib 类型类，再定义派生量，能降低后续齐次性证明的重复劳动。
- 当定义相等与命题相等不一致时，可用显式 `cast` 加自动证明 tactic 连接表达式层和类型层；但应同时保留手写证明入口。
- Buckingham Π 的“矩阵—秩—核”路线把传统工程推导接到线性代数库，可迁移到无量纲化、参数降维和方程建模工具。
- 代码片段、定理名和来源页码应与 Lean/Mathlib 版本绑定，才能把“论文中的形式证明”转化为可重复构建的工程组件。

## 11. 研究机会

以下是基于论文边界提出的后续问题，不是论文已经报告的结果：

- 发布可锁定 Lean、Mathlib 和项目 commit 的最小构建仓库，并用自动化 CI 报告每个定理的编译状态。
- 建立维度 tactic 的公开基准，覆盖不同基础维度系统、嵌套幂、分数指数、类型类缺失和刻意不齐次的反例。
- 扩展单位层以表达单位换算、量纲数值的不同表示类型、测量不确定度和带单位的数组/张量运算。
- 将同一维度安全层接入微分方程、有限元或分子动力学代码，评估类型检查能否在真实模型构造阶段捕获单位错误。
- 形式化 Buckingham Π 的构造性输出，并把线性代数核中的基选择、非唯一性和秩退化情况暴露为用户可读诊断。
- 补全 Lennard–Jones 及更多势函数的证明库，明确零点、奇异点、极限和导数定义所需的代数/拓扑假设。

## 12. 可复现性

**🟡 中可复现性（medium）**——论文给出 Lean 版本族、Mathlib 版本、核心定义、定理名和大量代码片段；但提供文本没有给出明确代码仓库 URL、commit、许可证、完整构建命令或测试清单。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 medium |
| **官方代码** | 论文声称证明托管在 GitHub，但提供文本未披露可核实 URL；`code_url: []`。 |
| **数据集** | 无外部数据集；材料是 Lean 定义、定理、SI 表格和 Lennard–Jones 形式化示例；`dataset_url: []`。 |
| **版本信息** | Lean 4；Mathlib 4.23.0-rc1；更细的 Lean 编译器版本和依赖锁定信息未披露。 |
| **复现要点** | 需要获得与正文代码片段一致的项目源码，特别是 `evalAutoDim`、`PhysicalVariable.deriv`、Buckingham Π 补充信息和两段 Lennard–Jones 证明；还要验证 `Classical.epsilon` 导致的 `noncomputable` 定义与当前 Mathlib 版本兼容。 |

## 页面导航

- 方法机制：[[bobbin2025-dimensional-analysis-method]]
- 结果证据：[[bobbin2025-dimensional-analysis-results]]
- 批判性边界：[[bobbin2025-dimensional-analysis-critical]]
- 算法实体：[[entities/lean-dimensional-analysis]]
- 相关 Lean 形式化实体：[[entities/heplean-index-notation]]
