---
type: entity
title: HepLean Lean 4 physics index-notation implementation
authors:
- Joseph Tooby-Smith
year: 2024
venue: arXiv preprint [cs.LO]
tags:
- domain/ai4s
- entity/model
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
id: entity--heplean-index-notation
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
# Algorithm entity: HepLean Lean 4 physics index-notation implementation

^[sources/papers/tooby-smith2024-physics-index-notation.md]

来源论文：*Formalization of physics index notation in Lean 4*，Joseph Tooby-Smith，2024，arXiv:2411.07667v1 [cs.LO]。论文将该实现放在 HepLean 中，并给出入口 `https://heplean.github.io/HepLean/`。论文分析见 [[tooby-smith2024-physics-index-notation-analysis]]，方法展开见 [[tooby-smith2024-physics-index-notation-method]]。

## 1. 定义

这是 HepLean 中面向物理指标记号的 Lean 4 实现：用户以接近纸笔的 syntax 表达 tensor expression，elaborator 将其转换成 tensor tree，再由 `TensorTree.tensor` 解释为表示中的 bona-fide tensor。

它不是通用 Lean 4 占位实体，也不是单独的张量数据集。实体范围限定为论文所描述的 physics index-notation implementation 及其支撑结构。

## 2. 关键组成

- **`TensorSpecies`**：定义交换环 `k`、群 `G`、颜色 `C`、表示函子 `FD`、维数和基，以及颜色对偶、收缩、单位和度量。
- **`OverColor` / `S.F`**：将指标位置和颜色组合成对象，并把基础表示提升为表示范畴中的 braided/symmetric monoidal functor。
- **`TensorTree`**：以 `tensorNode`、`smul`、`neg`、`add`、`action`、`perm`、`prod`、`contr`、`eval` 节点保留表达式结构。
- **Elaboration**：根据指标数量、颜色和配对规则从 syntax 生成 tensor tree；论文明确说明这一过程本身尚未形式验证。
- **证明接口**：使用 `contr_tensor_eq` 等局部等价引理在树上导航、替换和重排，再由 Lean 检查最终 tensor 等式。

## 3. 论文证据

论文展示了 complex Lorentz tensor 的颜色和表示实例，并以 `antiSymm_contr_symm` 演示反对称/对称张量收缩的形式证明；还定义 Pauli matrices、bispinors 并给出相应定理声明。结果边界见 [[tooby-smith2024-physics-index-notation-results]]。

论文说明框架可面向 real Lorentz、complex Lorentz 和 ordinary tensors，但写作时只有 complex Lorentz tensors 的最复杂实例已经实现。Pauli/bispinor 部分的证明没有全部展开，HepLean 的 `informal_lemma` 也不是类型检查后的定理。

## 4. 适用范围与限制

适用对象是需要在 Lean 4 中表达、重排、收缩并证明物理张量恒等式的形式化工作。它不提供 PDE 求解、材料本构模型、数值实验或外部数据集。

主要限制是 elaborator 的未验证信任边界、species 覆盖不完整、缺少量化 benchmark，以及论文文本没有给出明确源码仓库、commit、版本和完整构建步骤。显式求值越界按论文描述默认到 `0`，需要使用者额外防护。

## 5. 可复现性

按知识库标准记为 `medium`：论文给出结构定义、函数名、示例和部分 Lean 片段，但 `code_url` 与 `dataset_url` 均为 `[]`，提供文本不足以锁定一个可直接下载和编译的完整版本。批判性分析见 [[tooby-smith2024-physics-index-notation-critical]]。
