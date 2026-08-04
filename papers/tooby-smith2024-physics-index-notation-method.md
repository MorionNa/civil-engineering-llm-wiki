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
id: paper--tooby-smith2024-physics-index-notation-method
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
# 方法：HepLean 的 Lean 4 physics index notation

^[sources/papers/tooby-smith2024-physics-index-notation.md]

本文只展开方法机制。论文元数据和 12 维总览见 [[tooby-smith2024-physics-index-notation-analysis]]；实现作为可复用算法实体记录于 [[entities/heplean-index-notation]]。

## 1. 设计契约：可读记号与可检查语义

论文把目标拆成三个表示及其映射（原文第 2–3 页）：

1. **Syntax**：用户在 Lean 文件中书写、接近纸笔指标记号的表达式。
2. **Tensor tree**：保留表达式结构、节点类型和指标位置，便于形式化操作。
3. **Bona-fide tensor**：表示实际关心的数学对象，但不再保留完整表达式树结构。

总体管线是 `syntax → elaborator → tensor tree → TensorTree.tensor → tensor`。Figure 1 用实线表示形式验证的部分；正文明确说明 elaboration 本身没有形式验证，但它输出的 tensor tree 被验证（原文第 2、14 页）。因此，系统的信任边界不只在 Lean 内核，也在非形式化的语法解析/展开规则。

## 2. TensorSpecies：跨张量类型的统一接口

`TensorSpecies` 是论文的核心抽象，用来描述一类张量所需的数据：

| 字段/组件 | 作用 |
|---|---|
| `k` 与 `k_commRing` | 张量所在的交换环，例如实数或复数。 |
| `G` 与 `G_group` | 作用在表示上的群，例如 Lorentz group 或 `SL(2, C)`。 |
| `C` | 指标颜色类型，例如 up/down 或 Weyl-fermion 的不同颜色。 |
| `FD` | 从离散颜色到 `Rep k G` 的表示函子，为每个颜色指定基础表示。 |
| `repDim` 与 `repDim_neZero` | 指定每种颜色的表示维度，并排除零维情况。 |
| `basis` | 用于显式指标求值的每色基。 |
| `τ` 与 `τ_involution` | 把颜色映到可收缩的对偶颜色。 |
| `contr` | 描述对偶颜色之间收缩的自然变换。 |
| `unit` | 描述单位对象及其对称性。 |
| `metric` | 描述把指标改成对偶指标的度量及其与收缩、单位的关系。 |

这些组件并非任意字段拼接：`contr_tmul_symm`、`unit_symm`、`contr_unit` 和 `contr_metric` 把交换、单位、收缩和度量的相容性写进结构（原文第 3–8 页）。例如，`τ` 是 involution，收缩需要证明被配对颜色满足对偶关系，度量收缩后要回到单位。

## 3. 复杂 Lorentz tensor 的实例化

对于 `complexLorentzTensor`，论文给出六种颜色：`upL`、`downL`、`upR`、`downR`、`up`、`down`。`FD` 将它们映射到左/右手 Weyl fermion 表示、alternative 表示、逆变复 Lorentz 表示和协变复 Lorentz 表示（原文第 5–7 页）。

以 `Fermion.leftHanded` 为例，论文展示了 `Rep C SL(2,C)` 的构造：底层函数用矩阵作用于 `C^2` 模块，并通过 `map_add`、`map_smul`、`map_one` 和 `map_mul` 证明线性与群作用公理。这说明具体物理表示的实现需要同时提供对象和 Lean 证明。

## 4. OverColor 与范畴提升

`OverColor C` 的对象是某个函数 `f : X → C`，即一组指标位置 `X` 以及每个位置的颜色；态射是保持颜色函数相容的双射。它带有由不交并给出的对称幺半结构 `⊗`（原文第 9 页）。

给定 `S.FD`，论文构造 `OverColor S.C` 到 `Rep S.k S.G` 的 braided functor `S.F`。对于 `f : X → S.C`，`S.F f` 表示所有 `FD (f x)` 的 `k`-张量积；因此一个带颜色指标的 tensor 可表示为这个表示中的向量。

这样做的原因是：物理表达式需要重排指标、组合不同张量并做收缩，而范畴结构为这些操作提供了自然的 tensorator、braiding、associator 和 unitors。论文没有把这些变换作为非类型化字符串替换，而是把它们嵌入表示范畴中的映射。

## 5. TensorTree 的数据结构与语义

论文用归纳类型 `TensorTree (S : TensorSpecies)` 表达具有 `Fin n → S.C` 颜色签名的树。构造子包括：

- `tensorNode`：从真实 tensor 生成叶节点，是递归基例。
- `smul`、`neg`、`add`：标量乘、取负和同签名加法。
- `action`：对 tensor 施加 `S.G` 中的群元素。
- `perm`：依据 `OverColor` 态射重排指标，并改变颜色签名。
- `prod`：组合两个 tensor tree，通过 tensorator 把两个表示的张量积放回合并后的签名。
- `contr`：选取两个位置，要求第二个颜色是第一个颜色的 `τ`，再经 `S.contrMap` 做收缩。
- `eval`：用给定基索引求值并移除一个指标。

`TensorTree.tensor` 对这些构造子递归解释：普通运算映射到表示上的加法、取负、标量作用和群作用；置换通过 `S.F.map`；乘积通过 tensorator 与 `OverColor` 等价；收缩通过 `S.contrMap`；求值通过 `S.evalMap`（原文第 10–14 页）。

## 6. 为什么保留树结构

直接在最终 tensor 上运算会丢失“这个对象是怎样由指标表达式构成的”信息。论文把 tensor tree 的一个节点及其子节点称为 subtree，并利用“等价 tensor 的子树可替换”这一性质建立引理。

代表性引理是：若 `T1.tensor = T2.tensor`，则在相同收缩位置和颜色证明下，`(contr i j h' T1).tensor = (contr i j h' T2).tensor`。这让证明可以定位到乘积、收缩或置换树中的局部位置，而不必重新展开整个表示对象（原文第 13–14 页）。

## 7. Syntax 与 elaboration 规则

用户通过类似 `{T | i j}T` 的记号创建 `tensorNode T`。elaborator 会检查 tensor 需要多少个指标；错误数量会触发错误。显式基索引可把某个位置变成 `eval` 节点。

负号、标量乘、群作用、乘积和加法分别映射到相应树节点。加法和等式允许两边指标顺序不同，elaborator 会插入 permutation 节点以对齐签名。

收缩通过在两个表达式中配对相同的指标名实现。生成的 `contr` 带有颜色对偶的证明；若颜色不是对偶，证明失败并由 elaborator 报错。论文还说明，多次收缩的处理取决于表达式嵌套位置：先在子表达式中完成的收缩可以避免同一时刻尝试收缩超过两个指标。

论文特意不把上标/下标作为独立 syntax 信息：对某些 complex Lorentz tensors，上指标也有三种类型，且上下关系由 tensor 类型携带。这个取舍减少了表面语法，但将类型建模责任转移给 `TensorSpecies` 和颜色系统。

## 8. 形式证明工作流

Section 3 的反对称/对称例子采用 `conv` 进入等式左侧，然后连续使用 `rw`：

1. 通过 `prod_tensor_eq_fst` 和 `prod_tensor_eq_snd` 使用反对称、对称假设。
2. 用 `prod_perm_left`、`prod_perm_right`、`perm_perm` 传播并合并置换。
3. 用 `perm_contr_congr`、`contr_contr` 调整收缩顺序和位置。
4. 用 `neg_fst_prod`、`neg_contr` 将负号穿过乘积与收缩。
5. 以 `apply perm_congr _ rfl; decide` 完成剩余的签名/置换一致性。

这不是数值算法，而是基于已证明结构引理的可检查重写流程。具体证明证据和声明/实现区分见 [[tooby-smith2024-physics-index-notation-results]]。

## 9. 方法的实现边界

- 论文声称框架可覆盖 ordinary tensors、real Lorentz tensors 和 complex Lorentz tensors，但写作时只有最复杂的 complex Lorentz tensors 已实现。
- `eval` 的实现用基展开；若自然数索引超出 `repDim`，论文描述为默认到 `0`，因此越界输入不是一个必然的硬错误。
- `contr` 依赖颜色对偶证明和不相同位置的索引构造；这把许多非法物理配对排除在类型检查阶段。
- elaborator 是规则驱动但未形式验证，属于从用户文字到受验证树之间的主要边界。
- 论文假定读者掌握 symmetric monoidal categories，未披露完整编译环境、依赖锁定和测试命令。

## 10. 可复现性说明

论文正文提供了核心结构和若干 Lean 代码片段，且把实现指向 `https://heplean.github.io/HepLean/`；但提供文本没有明确 Git 仓库、commit、许可证或版本矩阵。因此 frontmatter 的 `code_url` 和 `dataset_url` 保持空列表，等级记为 medium。

复现时至少需要：对应版本的 Lean/Mathlib/HepLean；`TensorSpecies` 的实例；`TensorTree.tensor` 的语义；颜色对偶和收缩证明；以及 Section 3 的代码环境。不能仅凭论文中的片段声称已经重建完整实现。总览页见 [[tooby-smith2024-physics-index-notation-analysis]]，批判性边界见 [[tooby-smith2024-physics-index-notation-critical]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[tooby-smith2024-physics-index-notation-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
