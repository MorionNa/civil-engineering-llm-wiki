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
id: paper--bobbin2025-dimensional-analysis-method
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
# Method：Lean 中的维度、物理变量与形式证明机制

^[sources/papers/bobbin2025-dimensional-analysis.md]

本页展开论文第 5 维“方法机制”。论文使用 Lean 4 和 Mathlib 4.23.0-rc1；预提取文本在正文第 2 页称证明托管于 GitHub，但没有给出可核实的仓库 URL。总览见 [[bobbin2025-dimensional-analysis-analysis]]，可复用算法实体见 [[entities/lean-dimensional-analysis]]。

原始来源：<https://arxiv.org/abs/2509.13142>。

## 1. 从物理变量到类型对象

论文先把物理变量视为一个同时含有数值和维度的对象：

\[
P=\langle V,D\rangle .
\]

当运算 \(\star\) 作用于两个物理变量时，数值部分和维度部分分别运算：

\[
P_i\star P_j=\langle V_i\star V_j, D_i\star D_j\rangle .
\]

因此，普通数学分析已经覆盖了数值部分，本文重点是给出维度部分的可复用定义和证明接口。这个分解也解释了为什么维度齐次性可以在数值计算前由类型或定理检查。

## 2. 维度的抽象表示

论文没有把维度固定成七个指数的元组，而是定义：

\[
D=B\to E,
\]

其中 `B` 是基础维度的类型，`E` 是指数类型，并要求 `E` 具有 `CommRing`。抽象化带来三点机制收益：

- 基础维度数量由 `B` 决定，系统可以只包含实际需要的基础维度。
- 指数类型不被限定为固定的有理数；论文指出最简单的满足条件的数值类型是整数。
- 维度运算可以归约为函数的逐点运算，再调用环上的加法、减法和标量乘法定理。

论文用 `KinematicSystem` 示例表示 `Length`、`Time` 和 `Mass`，又用 `SpatialTemporalSystem` 表示只含空间和时间的系统。两个系统虽然概念上都含长度和时间，但 Lean 会把不同的归纳类型视为不同类型。

## 3. 基础维度类型类

为了解决“概念上的同一基础维度在不同 `B` 中是不同构造子”的问题，论文定义类似 `HasBaseLength (B)` 的类型类。该类提供：

1. 对 `B` 的可判定相等实例；
2. 一个表示概念上 Length 的元素。

同样的模式被用于 `HasBaseTime`、`HasBaseMass`、`HasBaseAmount`、`HasBaseCurrent`、`HasBaseTemperature` 和 `HasBaseLuminosity`。论文还定义 `HasBaseCurrency` 来展示 ISQ 之外的基础维度扩展。

这种接口使 `length`、`time` 等定义只要求相关类型类，而不要求基础系统必须等于某个全局枚举。例如 `length B E` 可以在任何实现了 `HasBaseLength B` 的系统中复用。

## 4. 维度上的运算

### 4.1 乘法、除法与幂

论文把维度乘法定义为指数逐点相加：

\[
(a*b)(i)=a(i)+b(i).
\]

维度除法定义为指数逐点相减：

\[
(a/b)(i)=a(i)-b(i).
\]

维度幂把指数与幂指数做标量乘法：

\[
(a^n)(i)=n\cdot a(i).
\]

这些函数随后通过 Lean 的 `Mul`、`Div` 等类型类实例暴露为常规运算符。设计的关键是，用户书写的维度式仍然使用熟悉的运算符，而证明可以回到指数函数和 `CommRing` 运算。

### 4.2 加法与减法

维度的加法和减法与数值加法不同：只有相同维度才能相加，结果仍是该维度，而不是把两个指数相加。论文使用 `Classical.epsilon` 定义一个满足“若 `a=b`，则 `a+b=a`”的选择函数，并把它标记为 `noncomputable`。减法采用同样的条件式思路。

对于物理变量，论文不需要在维度对象上用 epsilon 表达同维约束，因为 `PhysicalVariable d` 的加法函数本身要求两个输入共享同一个维度索引 `d`。

## 5. 把维度接入 Mathlib 的交换群

论文逐项证明维度乘法满足：

- `mul_comm`：交换律；
- `one_mul` 和 `mul_one`：维度无量纲元是单位元；
- `mul_assoc`：结合律；
- `mul_left_inv`：维度与其逆的乘积为无量纲元；
- `div_eq_mul_inv`：除法等于乘以逆元。

随后通过 `instance : CommGroup (dimension B E)` 把这些定理装配到 Mathlib 的 `CommGroup` 接口中，同时定义自然幂、整数幂、逆元和除法。证明脚本主要使用 `simp`、`funext`、加法交换律/结合律和指数上的环恒等式。

这种“先给出对象运算，再对接类型类”的顺序，使任意满足 `CommRing E` 的指数类型都能继承相同的维度群结构。论文正文第 7–9 页给出了实例字段及部分证明片段。

## 6. 派生维度与维度齐次性

基础维度用 `Pi.single` 定义。例如 `length` 在 `HasBaseLength.Length` 位置取 1，在其他基础维度取 0；`time` 采用同一模式。派生维度直接复用运算：

\[
\mathrm{velocity}=\mathrm{length}/\mathrm{time},
\qquad
\mathrm{acceleration}=\mathrm{length}/\mathrm{time}^2.
\]

论文还定义 `mass_density`、`volume`、`dynamic_viscocity` 等维度，并将 Reynolds 数写成相应维度的乘除组合。由于这些定义使用 `abbrev`，Lean 的类型检查器可以展开它们，从而更容易证明齐次性。

两个示例定理展示了机制：

```lean
theorem accel_eq_vel_div_time ... :
  acceleration B E = velocity B E / time B E := by
  rw [acceleration, velocity, pow_two, div_div]
```

以及 Reynolds 数归约到 `dimensionless B E`。这些定理说明，工程维度推导被转成了 Lean 可重写的函数等式。

## 7. 分级物理变量

论文的物理变量结构带有维度索引：

```lean
structure PhysicalVariable {B} {V} [Field V]
    (dim : dimension B V) where
  value : V
```

其中 `B` 是基础维度系统，`V` 同时作为数值类型和指数类型，`dim` 是该物理变量的维度索引。作者选择这个结构是为了让运算结果的维度直接进入结果类型。

### 7.1 乘法与加法

乘法把两个不同维度的物理变量映射为乘积维度：

```lean
PhysicalVariable d1 → PhysicalVariable d2 →
  PhysicalVariable (d1 * d2)
```

实现只对 `value` 字段做数值乘法；维度结果由返回类型记录。加法则是：

```lean
PhysicalVariable d → PhysicalVariable d → PhysicalVariable d
```

所以 Lean 在构造加法表达式时就要求两边共享同一维度。除法和减法使用同类方式，幂的返回维度是 `d ^ n`。

### 7.2 幂运算的类型限制

物理变量的幂不能写成完全普通的二元函数，因为只有看到幂指数 `n` 后，才能确定输出维度 `d^n`。论文因此提供 `PhysicalVariable.Pow`，并允许用 `a.Pow b` 的形式调用。它牺牲了一点常规运算符的表面统一性，但保留了维度信息。

## 8. 命题相等、cast 与自动维度 tactic

物理方程可能在数学上维度相等、但在 Lean 中不是定义上相同的类型。例如 `force` 的维度和 `mass * acceleration` 的维度可能只是 propositionally equal，直接写 (F=ma) 会遇到类型检查问题。

论文定义 `PhysicalVariable.cast`，输入一个带维度 `d1` 的物理变量和一个证明 `d1 = d2` 的前提，返回带维度 `d2` 的物理变量。然后为这个证明前提提供默认 tactic：

```lean
:= by evalAutoDim
```

`evalAutoDim` 的宏按顺序尝试 `rfl`、若干 `rw`、`simp`、`funext`、`module`、`ring_nf` 和 `field_simp` 等步骤，最后再次尝试简化和反射。论文说在所有测试的情况中该 tactic 足以闭合目标，并指出用户也可以在 tactic 失败时直接提供证明。

这里的 tactic 是工程便利层，不是一个论文中证明了完备性的维度决策算法；它依赖可展开的定义、可用的类型类实例和现有 Mathlib 重写规则。

## 9. SI 基础单位和常数

论文以 2019 SI 定义为依据，用 `PhysicalVariable` 表示基准单位：

- 单位秒从 Caesium-133 基态超精细跃迁的单次振荡持续时间构造，随后定义 `second`；
- 米作为一个长度单位，并以米和秒定义精确的真空光速 `SpeedOfLight`；
- 千克、安培、开尔文、摩尔和坎德拉分别作为相应维度的带值变量；
- Planck 常数、元电荷、Boltzmann 常数、Avogadro 数和 540 THz 单色光的发光效能被表示为带维度的物理常数。

这一层把单位的尺度信息和维度信息放在同一结构中，但论文提供的文本没有展示完整的单位换算 API，也没有实验校准数据接口。

## 10. Buckingham Π 定理

补充信息第 1 节把 `n` 个变量的维度组织成 `k × n` 维度矩阵：行对应基础维度，列对应变量，矩阵元素是相应指数。Lean 定义接收一个 `Fin n → dimension B E` 的变量列表，以及一个对基础维度进行编号的排列，从而显式固定矩阵的行顺序。

对矩阵的两个核心操作是：

\[
\text{number of dimensionless parameters}=n-\operatorname{rank}(M),
\]

以及用 `LinearMap.ker` 表示维度矩阵的核，以得到无量纲参数的指数组合。论文特别指出，当系统含有未被变量使用的基础维度时，矩阵秩可以小于基础维度类型的基数；长度和面积的示例展示了这一退化情形。

## 11. 物理变量导数

补充信息第 2 节先在维度层定义单变量导数和积分：

\[
[df(x)/dx]=[f(x)]/[x],
\qquad
[\int f(x)dx]=[f(x)]\,[x].
\]

物理变量导数 `PhysicalVariable.deriv` 把数值部分交给 Lean 的单变量导数实现，把输出维度设为 `d2/d1`。这保持了“数值微分”和“维度传播”两个层面的分离；该实现要求 `NontriviallyNormedField V`，比普通物理变量结构的 `Field V` 假设更强。

## 12. Lennard–Jones 方法映射

论文在正文第 14 页将 Lennard–Jones 势定义为：

\[
V(r)=4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^6\right].
\]

Lean 定义要求 `σ` 和 `r` 是长度维度、`ε` 是能量维度，并返回能量维度。表达式内部使用 cast 把两个幂和乘积转换到可相减、可与能量相乘的等价维度；`evalAutoDim` 尝试自动证明这些等式。随后两个定理分别把 `r=σ` 的零能量性质和对 `r` 的导数/力表达式纳入形式化接口。证明主体在提供的预提取文本中没有展开。

## 页面导航

- 总览与 12 维分析：[[bobbin2025-dimensional-analysis-analysis]]
- 结果证据：[[bobbin2025-dimensional-analysis-results]]
- 失败边界与研究机会：[[bobbin2025-dimensional-analysis-critical]]
- 算法实体：[[entities/lean-dimensional-analysis]]
