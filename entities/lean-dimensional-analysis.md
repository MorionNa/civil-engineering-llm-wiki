---
type: entity
title: Lean framework for formally verified dimensional analysis
authors:
- Maxwell P. Bobbin
- Colin Jones
- John Velkey
- Tyler R. Josephson
year: 2025
venue: arXiv preprint [physics.chem-ph]
tags:
- domain/ai4s
- entity/model
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
id: entity--lean-dimensional-analysis
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
# Algorithm entity: Lean framework for formally verified dimensional analysis

^[sources/papers/bobbin2025-dimensional-analysis.md]

这是 Maxwell P. Bobbin、Colin Jones、John Velkey 和 Tyler R. Josephson 在 2025 年 arXiv 论文中提出/实现的 Lean 4 维度分析框架。它把物理维度、SI 单位、物理变量、Buckingham Π 定理和 Lennard–Jones 示例放进 Lean 的类型与定理证明环境。论文总览见 [[bobbin2025-dimensional-analysis-analysis]]，方法细节见 [[bobbin2025-dimensional-analysis-method]]。

原始来源：<https://arxiv.org/abs/2509.13142>。

## 定义

框架的核心对象是参数化维度：

\[
\mathrm{dimension}\ B\ E := B\to E,
\]

其中 `B` 表示基础维度类型，`E` 是满足 `CommRing` 的指数类型。维度乘法、除法和幂分别对指数执行逐点加法、减法和标量乘法。`HasBaseLength`、`HasBaseTime` 等类型类让不同基础维度系统共享概念上的基础维度接口。

## 主要组件

- **维度代数：** 对 `dimension B E` 证明乘法交换律、结合律、单位元、逆元和除法关系，并注册为 Mathlib 的 `CommGroup`。
- **派生维度：** 用 `Pi.single` 定义长度、时间等基础维度，再构造速度、加速度、质量密度、Reynolds 数等维度。
- **维度齐次性：** 通过 `PhysicalVariable d` 的分级类型让同维度加法成为类型约束；乘法和幂的结果类型携带对应维度。
- **维度转换：** `PhysicalVariable.cast` 配合 `evalAutoDim` 尝试证明命题上相等的维度，例如把 Newton 第二定律中的等价维度接起来。
- **SI 单位和常数：** 形式化秒、米、千克、安培、开尔文、摩尔、坎德拉，以及 Planck 常数、元电荷、Boltzmann 常数、Avogadro 数等。
- **Buckingham Π：** 用维度矩阵、矩阵秩和 `LinearMap.ker` 表示无量纲参数的数量和构造空间。
- **Lennard–Jones：** 以长度维度的 `σ/r`、能量维度的 `ε` 定义势能，并给出 `LJ_zero_energy` 和 `LJ_deriv` 定理声明。

## 证据与适用范围

论文正文第 4 节和补充信息给出了上述定义、部分 Lean 代码和定理片段；结果清单见 [[bobbin2025-dimensional-analysis-results]]。该实体是形式化框架/算法接口，不是数据集、PDE 求解器、材料本构模型或数值 benchmark。

它适合：

- 在 Lean 中表达维度和物理变量的代数关系；
- 在公式构造时尽早捕获部分维度不一致；
- 为形式化科学库提供 SI 量纲和无量纲化的基础层。

## 边界与失败模式

- 预提取文本说证明托管在 GitHub，但没有给出可核实的代码 URL、commit 或完整构建说明，因此当前实体的 `code_url` 为 `[]`。
- 作者称 `evalAutoDim` 对所有测试情况足够，但没有披露测试规模、失败率或完备性证明；不能视为任意维度表达式的决策程序。
- `Classical.epsilon` 使维度加法定义为 `noncomputable`；物理变量实现还让数值类型和指数类型共享同一 `V`，这可能限制更丰富的类型设计。
- 论文没有提供外部数据集、实验校准或传统数值性能评测；Lennard–Jones 两个定理的证明主体在提供文本中被省略。

## 可复现性

按知识库标准记为 **medium**：论文披露 Lean 4、Mathlib 4.23.0-rc1、对象定义和部分证明，但无法从提供文本锁定完整源码与构建环境。没有外部数据集，`dataset_url` 为 `[]`。完整复现需要取得论文所称的 GitHub 项目，并重新检查 `evalAutoDim`、Buckingham Π 补充代码和 Lennard–Jones 证明。

## 关联页面

- 结果证据：[[bobbin2025-dimensional-analysis-results]]
- 批判性边界：[[bobbin2025-dimensional-analysis-critical]]
- 相关 Lean 物理形式化实体：[[entities/heplean-index-notation]]
