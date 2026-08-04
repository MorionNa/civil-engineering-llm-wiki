---
type: paper-analysis
title: Formalization of physics index notation in Lean 4
authors:
- Joseph Tooby-Smith
year: 2024
venue: arXiv preprint [cs.LO]
tags:
- domain/ai4s
- evidence/paper
methods:
- formalization
- theorem-proving
- proof-assistant
- lean-4
- mathlib
- physics-formalization
- index-notation
- category-theory
results:
- formalization
- theorem-proving
- proof-assistant
- physics-formalization
- index-notation
failure_modes:
- formalization
- proof-assistant
- lean-4
- physics-formalization
- index-notation
datasets: []
reproducibility: medium
code_url: []
dataset_url: []
id: paper--tooby-smith2024-physics-index-notation-results
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
- index-notation
- category-theory
- formal-science
- arXiv preprint [cs.LO]
sources:
- sources/papers/tooby-smith2024-physics-index-notation.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# 结果证据：Formalization of physics index notation in Lean 4

^[sources/papers/tooby-smith2024-physics-index-notation.md]

本页只记录预提取文本中有明确支撑的实现结果、定理声明和图表信息；方法机制见 [[tooby-smith2024-physics-index-notation-method]]，整体判断见 [[tooby-smith2024-physics-index-notation-analysis]]。

## 1. 论文报告的实现范围

论文摘要将工作描述为 Lean 4 中第一个经形式验证的 physics index notation implementation，并说明其目的在于让物理学家在 Lean 中书写和证明张量结果（原文第 1 页）。这是论文自身的贡献表述，不是本文独立验证的优先性结论。

正文说明实现可以处理不同 tensor species，包括 real Lorentz tensors、complex Lorentz tensors 和 ordinary tensors（如 vectors and matrices）；同时明确限制为：在写作时，最复杂的 complex Lorentz tensors 才已经实现（原文第 2 页）。

## 2. Figure 1：表示管线

Figure 1 的标签为 `Syntax`、`Tensor Tree`、`TensorElab` 和 `Cat theory`。图注说明实线表示形式验证的实现部分（原文第 2 页）。正文对这张图的文字解释是：

| 组件 | 文本证据 |
|---|---|
| Syntax | 用户在 Lean 文件中交互的、接近指标记号的表达式表示。 |
| Tensor tree | 结构化且便于操作的张量表达式，节点对应张量运算。 |
| TensorElab | 将 syntax 变成 tensor tree 的 elaborator；论文明确说 elaboration 本身没有形式验证。 |
| Cat theory | 通过表示的对称幺半范畴，把 tensor tree 解释成 bona-fide tensor。 |

这张图支持“存在分层实现管线”的结论，但不提供运行时间、内存、成功率或规模 benchmark。

## 3. TensorSpecies 与 complex Lorentz 实现

论文给出了 `TensorSpecies` 的完整 Lean 结构定义。结构包含：交换环 `k`、群 `G`、颜色 `C`、表示函子 `FD`、维数 `repDim`、非零维证明、基、颜色对偶 involution、收缩 `contr`、单位 `unit` 和度量 `metric`，以及收缩/单位/度量的相容性条件（原文第 3–8 页）。

complex Lorentz tensors 的颜色定义包括 `upL`、`downL`、`upR`、`downR`、`up` 和 `down`；`FD` 把这些颜色连接到 Weyl fermion、alternative Weyl fermion、contravariant complex Lorentz 和 covariant complex Lorentz 表示（原文第 5–7 页）。

论文还展示了 `Fermion.leftHanded` 的表示构造片段：矩阵作用于 `C^2` 模块，Lean 代码分别证明加法、标量乘、单位元和乘法相容性。此代码片段是实现证据，不等价于提供整套可下载代码。

## 4. TensorTree 的形式化结果

论文定义了带颜色签名的归纳类型 `TensorTree`，其构造子包括 `tensorNode`、`smul`、`neg`、`add`、`action`、`perm`、`prod`、`contr` 和 `eval`（原文第 10 页）。

`TensorTree.tensor` 对每个节点给出语义：

- 基节点直接返回输入 tensor。
- `smul`、`neg`、`add` 和 `action` 映射到表示中的对应运算。
- `perm` 通过 `S.F.map` 作用于 tensor。
- `prod` 通过 tensorator 和 `OverColor` 等价把两个 tensor 合并。
- `contr` 使用 `S.contrMap`，其前提包含颜色对偶证明。
- `eval` 使用基和 `S.evalMap` 显式取出一个指标。

论文给出 `contr_tensor_eq` 引理：若两棵树的底层 tensor 相等，则在同一收缩位置和颜色相容证明下，收缩后的底层 tensor 也相等（原文第 13–14 页）。这为后续在树中定位和替换子树提供了形式化支撑。

## 5. Example 1：对称/反对称张量

论文给出 Lean 引理 `antiSymm_contr_symm`。假设：

- `A` 是 `complexLorentzTensor` 中两个 `Color.up` 指标的 tensor；
- `S` 是两个 `Color.down` 指标的 tensor；
- `hA` 断言 `A` 交换两个指标时取负，即反对称；
- `hs` 断言 `S` 交换两个指标不变，即对称。

目标是证明二者按相应指标收缩后，结果等于带负号的同一收缩。证明在 `conv` 中对左侧 tensor tree 使用一系列 `rw`：先应用 `hA` 和 `hs`，再移动/合并置换，重排两个收缩，传播负号，最后用 `perm_congr` 和 `decide` 处理剩余置换一致性（原文第 16–21 页）。

这提供了一个“在表达式树上证明，而不是直接展开分量”的可检查示例。原文没有报告该证明的耗时、自动化成功率或与手写分量证明的对比。

## 6. Example 2：Pauli matrices 与 bispinors

论文在 HepLean 中定义了四个 Pauli-matrix tensor 版本：`pauliContr`、`pauliCo`、`pauliCoDown` 和 `pauliContrDown`。这些定义使用 `PauliMatrix.asConsTensor`、metric 和 contraction，把 Pauli matrices 表成 complex Lorentz tensors（原文第 21–22 页）。

论文进一步给出四个 bispinor 构造：`contrBispinorUp`、`contrBispinorDown`、`coBispinorUp` 和 `coBispinorDown`，分别从逆变或协变 Lorentz vector 及 Pauli tensors 构造（原文第 21–22 页）。

示例中的定理/引理声明包括：

1. `coBispinorDown_eq_pauliContrDown_contr`，把 `coBispinorDown p` 写成 `pauliContrDown` 与 `p` 的收缩。
2. `pauliCo_contr_pauliContr`，形式化 Pauli 矩阵收缩得到度量张量乘积的恒等式。

论文没有逐字给出这两个证明；它只说明前一个是 tensor-product associativity 与 contraction shuffling 的较简单应用，并指出这些证明可以沿用前一示例的树操作。

## 7. Figure 2 与非形式化结果

Future Work 部分说明 HepLean 还添加了与指标记号相关的 `informal_lemma`。示例 `coBispinorUp_eq_metric_contr_coBispinorDown` 保存数学字符串、证明提示和依赖定义；这些内容没有经过类型检查，旨在引导人或 AI 进行后续形式化。

Figure 2 展示 HepLean informal dependency graph 的一部分，图注说明灰色节点是 informal results，蓝色节点是已经 formalised 的结果（原文第 22–23 页）。因此，图中出现的节点不能整体视为已证明知识。

## 8. 论文没有报告的结果

预提取文本中没有可核实的：

- 数值误差、运行时间、内存、定理证明成功率或规模曲线；
- 与 Haskell 或其他指标记号实现的定量对比；
- 用户可用性实验或物理学家评测；
- 外部数据集、训练集、预训练权重或数据下载地址；
- 明确的代码仓库、commit、许可证和完整编译配置。

因此，本页不把“更容易使用”“支持 AI”或“促进采用”写成已完成的实验结论；它们在论文中是目标、动机或展望。

## 9. 证据边界与复现信息

可复核证据是论文展示的 Lean 结构、函数名、引理/定理声明、部分证明脚本和示意图。实现入口仅以 `https://heplean.github.io/HepLean/` 形式出现；提供文本没有足够信息把它登记为代码仓库，所以 `code_url: []`。没有外部数据集，`dataset_url: []`。

按本知识库的分级，论文属于 **🟡 medium**：方法细节足以让熟悉 Lean/Mathlib 的读者理解并尝试重建，但没有完整版本锁定和可直接下载的实现证据。方法细节见 [[tooby-smith2024-physics-index-notation-method]]，失败边界见 [[tooby-smith2024-physics-index-notation-critical]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[tooby-smith2024-physics-index-notation-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
