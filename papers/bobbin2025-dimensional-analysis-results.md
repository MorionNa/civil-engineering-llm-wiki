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
id: paper--bobbin2025-dimensional-analysis-results
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
# Results：形式化证据、定理与示例

^[sources/papers/bobbin2025-dimensional-analysis.md]

本页只记录预提取文本中能够定位到正文或补充信息的定义、定理、表格和作者明确报告的结果。不把“框架可用于未来科学计算”写成已完成的数值实验，也不补充论文未报告的性能指标。方法机制见 [[bobbin2025-dimensional-analysis-method]]，综合判断见 [[bobbin2025-dimensional-analysis-critical]]。

原始来源：<https://arxiv.org/abs/2509.13142>。

## 1. 论文报告的结果类型

论文没有实验数据集、误差曲线、运行时间表、准确率或与其他软件的定量 benchmark。它的结果载体是：

- Lean 中的对象定义和类型类实例；
- 对维度运算和维度齐次性的定理声明/证明片段；
- SI 单位和基本常数的形式化定义；
- Buckingham Π 定理的矩阵、秩和核表示；
- Lennard–Jones 势的维度一致性和两个物理性质定理。

因此，下面的“结果”指形式化工件和定理证据，而不是数值模型性能。

## 2. 维度代数证据（正文第 4.1–4.3 节，PDF 第 4–9 页）

论文给出 `dimension (B : Type u) (E : Type v) [CommRing E] := B → E`，并通过逐点指数操作定义：

| 维度操作 | 文本中给出的指数作用 |
|---|---|
| 乘法 | 指数相加：`(a * b) i = a i + b i` |
| 除法 | 指数相减：`(a / b) i = a i - b i` |
| 幂 | 指数与幂指数做标量乘法 |
| 加法/减法 | 只在相同维度时有意义；结果保持原维度，使用 `Classical.epsilon` 表达条件定义 |

在此基础上，正文列出并展示以下交换群性质的 Lean 证明：

- `mul_comm`：维度乘法交换；
- `one_mul` 与 `mul_one`：无量纲维度是乘法单位元；
- `mul_assoc`：维度乘法结合；
- `mul_left_inv`：维度与逆维度相乘得到单位元；
- `div_eq_mul_inv`：维度除法等于乘以逆维度。

作者随后给出 `CommGroup (dimension B E)` 实例，填充自然幂、整数幂、逆元、除法和上述证明字段。这里的证据支持“维度对象接入 Lean/Malhlib 交换群接口”，但文本没有给出编译日志或完整仓库快照。

## 3. 派生维度和齐次性定理（正文第 4.4 节，PDF 第 9–10 页）

论文定义 `length` 和 `time` 为在对应基础维度位置取 1 的 `Pi.single` 函数，再用运算符构造：

\[
\mathrm{velocity}=\mathrm{length}/\mathrm{time},
\qquad
\mathrm{acceleration}=\mathrm{length}/\mathrm{time}^2.
\]

正文给出的定理包括：

```lean
theorem accel_eq_vel_div_time ... :
  acceleration B E = velocity B E / time B E := by
  rw [acceleration, velocity, pow_two, div_div]
```

另一个定理 `reynolds_eq_dimless` 把由质量密度、速度、长度和动力黏度构成的 Reynolds 数归约为 `dimensionless B E`。论文正文给出了重写序列，包括 `mul_assoc`、`mul_div`、`pow_three`、`div_one` 等步骤。

这些是形式等式结果，不是对 Reynolds 数或加速度的数值计算；文本也没有提供具体参数、运行时间或输出样例。

## 4. 物理变量与自动齐次性（正文第 4.5 节，PDF 第 10–12 页）

论文定义带维度索引的结构：

```lean
structure PhysicalVariable {B} {V} [Field V]
    (dim : dimension B V) where
  value : V
```

正文明确给出以下类型级结果：

| 构造 | 输入/输出维度关系 |
|---|---|
| 乘法 | `PhysicalVariable d1` 与 `PhysicalVariable d2` → `PhysicalVariable (d1*d2)` |
| 加法 | `PhysicalVariable d` 与 `PhysicalVariable d` → `PhysicalVariable d` |
| 除法 | 输出维度为两个输入维度的商 |
| 幂 | 输出维度为 `d^n`；由于 `n` 决定输出类型，使用 `PhysicalVariable.Pow` |
| cast | 将命题上等于 `d1` 的变量转到 `d2`，证明前提默认为 `by evalAutoDim` |

作者报告 `evalAutoDim` 对“所有测试的情况”都足以完成维度等式证明，并说明 tactic 可以在新情况出现时扩展。文本没有披露测试数目、覆盖率、失败案例、平均证明时间或与手写证明的对比，所以这里只记录作者报告，不能推导出完备性或性能结论。

## 5. SI 单位和常数（正文第 4.5 节，PDF 第 12–13 页）

正文 Table 3 给出 2019 SI 七个基本单位的定义。预提取文本中明确出现的数值和对应关系如下：

| 单位/常数 | 论文文本中的形式化依据 |
|---|---|
| Second | Caesium-133 未扰动基态超精细跃迁；秒由 `9,192,631,770` 次振荡构造 |
| Meter | 以米和秒把真空光速固定为 `299,792,458` m/s |
| Kilogram | 以 Planck 常数 `6.62607015 × 10^-34` 的定义构造 |
| Ampere | 以元电荷 `1.602176634 × 10^-19` 的定义构造 |
| Kelvin | 以 Boltzmann 常数 `1.380649 × 10^-23` 的定义构造 |
| Mole | 以 `6.02214076 × 10^23` 个基本实体构造 |
| Candela | 以 540 THz 单色光的发光效能 `683` 构造 |

对应的 Lean 定义包括 `second`、`meter`、`kilogram`、`ampere`、`kelvin`、`mole`、`candela`，以及 `PlancksConstant`、`ElementaryCharge`、`BoltzmannConstant`、`AvogadrosNumber` 和 `MonochromaticRadiation540THz`。这些名称和数值来自正文 Table 3 与随后的代码片段；论文没有报告由这些定义驱动的实测校准结果。

## 6. Buckingham Π 定理证据（补充信息第 1 节，PDF 第 17–18 页）

对于 `n` 个变量和 `k` 个基础维度，论文定义 `k × n` 维度矩阵；每个矩阵条目是某变量在某基础维度上的指数。Lean 函数 `dimensional_matrix` 接受维度列表 `Fin n → dimension B E` 和基础维度排列 `Fin (Fintype.card B) → B`。

论文给出的数量结果是：

\[
p=n-\operatorname{rank}(M),
\]

其中 `p` 是可形成的无量纲参数数目。无量纲参数的形式由维度矩阵对应的线性映射核 `LinearMap.ker` 表示。文本还给出长度和面积的矩阵示例，说明一个未被变量使用的基础维度会使矩阵秩小于基础维度系统的基数。

这部分是可计算对象和线性代数接口的形式化定义；提供文本没有给出一个具体工程变量表上运行后的 Π 组输出。

## 7. Lennard–Jones 定理证据（正文第 5 节，PDF 第 14 页）

论文定义：

\[
V=4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^6\right].
\]

Lean 版本要求：

- `σ` 是 `dimension.length B V` 的物理变量；
- `ε` 是 `dimension.energy B V` 的物理变量；
- `r` 是 `dimension.length B V` 的物理变量；
- 基础系统至少具有 Length、Time 和 Mass；
- 返回值是 `dimension.energy B V` 的物理变量。

论文随后给出两个 theorem statement：

1. `LJ_zero_energy`：在 `σ.value ≠ 0` 的条件下，把分离距离设为 `σ`，Lennard–Jones 势能为 0。
2. `LJ_deriv`：在 `NontriviallyNormedField V` 和 `r.value ≠ 0` 条件下，对距离求导，得到与 \(-12\sigma^{12}/r^{13}+6\sigma^6/r^7\) 一致的力表达式，并保留 `ε` 的能量维度。

预提取文本明确写出这两个证明的主体为“rest of proof on GitHub”，所以证据等级是“论文给出定理声明和应用叙述”，而不是“当前提供文本中可逐行复核完整证明”。

## 8. 论文没有报告的结果

- 没有外部数据集、实验测量或真实工程系统的数值验证。
- 没有与单位检查器、CAS、其他语言或 Lean 方案的速度、内存、覆盖率或错误捕获率对比。
- 没有给出 `evalAutoDim` 的测试规模、失败边界或完整性能表。
- 没有在提供文本中给出 GitHub 仓库 URL、commit、许可证和可直接运行的构建命令。
- 没有给出完整 Lennard–Jones 证明脚本，因此无法从预提取文本确认所有实现细节已在同一环境中编译。

## 页面导航

- 12 维总览：[[bobbin2025-dimensional-analysis-analysis]]
- 方法机制：[[bobbin2025-dimensional-analysis-method]]
- 批判性分析：[[bobbin2025-dimensional-analysis-critical]]
- 算法实体：[[entities/lean-dimensional-analysis]]

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[bobbin2025-dimensional-analysis-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
