---
id: paper--hu2022-xpinn-generalization-results
title: Hu et al. (2022) — XPINN 泛化分析：解析例子与五类 PDE 结果
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/hu2022-xpinn-generalization
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_methods:
- physics-informed
- pinn
- collocation-strategy
- soft-constraint
- spatial-partitioning
legacy_results:
- benchmark
- comparison
- data-scarcity
- physics-constraint-weight-tuning
legacy_failure_modes:
- data-scarcity
- physics-constraint-weight-tuning
- limitation
legacy_datasets:
- dataset
- benchmark
- synthetic-data
legacy_reproducibility: medium
legacy_code_url:
- https://github.com/AmeyaJagtap/XPINNs
legacy_contested: true
legacy_tags:
- physics-informed
- pinn
- pde
- scientific-machine-learning
- spatial-partitioning
- comparison
- benchmark
- data-scarcity
- spectral-bias
- physics-constraint-weight-tuning
legacy_sources:
- raw/papers/hu2022-xpinn-generalization.pdf
evidence_scope: local workspace source record pending canonical verification
---

# 解析例子与五类 PDE 结果

> 本页回到总览：[[hu2022-xpinn-generalization-analysis]]。数字均按原始 PDF 表 1–6 和对应实验小节记录；XPINN 的总体判定应联系 [[pinn]] 的全域基线、子域样本数和接口权重一起看。

## 1. 结果总览

| 案例 | 表格中的 PINN 结果 | 表格中的 XPINN 结果 | bound（相对 PINN） | 按表格/分节证据的判定 |
|---|---|---|---|---|
| KdV | 相对 L2 \(6.899\mathrm e{-1}\pm8.015\mathrm e{-3}\)；复杂度 100% | XPINN-R：\(6.955\mathrm e{-1}\pm9.905\mathrm e{-3}\)，复杂度 101.31% | 121.08% | PINN 略优，整体相近 |
| Heat | 相对 L2 \(1.778\mathrm e{-3}\pm2.195\mathrm e{-4}\)；复杂度 100% | XPINN-T：\(4.490\mathrm e{-3}\pm1.517\mathrm e{-3}\)，复杂度 156.24% | 243.22% | PINN 优于 XPINN |
| Advection | 相对 L2 \(2.052\mathrm e{-1}\pm1.001\mathrm e{-1}\)；复杂度 100% | XPINN-L：\(1.617\mathrm e{-1}\pm3.582\mathrm e{-2}\)，复杂度 40.53% | 66.59% | XPINN 优于 PINN |
| Poisson | 相对 L2 \(5.553\mathrm e{-2}\pm2.936\mathrm e{-2}\)；复杂度 100% | XPINN3：\(1.108\mathrm e{-1}\pm1.561\mathrm e{-2}\)，复杂度 195.57% | 106.28% | PINN 优于所有报告的 XPINN 版本 |
| Compressible Euler | 密度相对 L2 \(3.4604\mathrm e{-2}\pm7.385\mathrm e{-3}\)；范数 100% | XPINN-A：\(1.048\mathrm e{-2}\pm5.3793\mathrm e{-3}\)，范数 37.28% | 81.09% | shock-aware XPINN-AM 优于 PINN；top/bottom 方案不稳定 |

表中的“Complexity/Norms”是权重矩阵范数乘积的相对量，不是误差百分比；表中的“Bound”是理论 bound 的相对量，也不是置信区间或实际误差。

## 2. 解析例子：先验 bound 的三种关系

### 2.1 XPINN 优于 PINN

在折线域 \(\Omega_1=[0,1]\times\{0\}\)、\(\Omega_2=\{0\}\times[0,1]\) 上，目标为 \(u^*(x,y)=2\sin x+\sin y\)。全域 \(W_2\) 范数为 3，两个子域的范数分别为 2 和 1；若两子域各取 \(n_r/2\) 个残差点，论文用 \(27=3^3\) 与 \(9/\sqrt2\) 的比较说明复杂度降低超过样本减少的代价，XPINN 的 prior bound 更有利。

### 2.2 PINN 优于 XPINN

保持第一子域不变、把第二项改为 \(\tfrac12\sin y\)，全域范数为 2.5，两个限制后的范数为 2 与 2.5。此时论文比较 \(15.625=2.5^3\) 与 \(23.625/\sqrt2\approx16.70\)，说明第二子域并没有真正简单化，样本减半的统计代价更大，PINN 更有利。

### 2.3 阈值例子

目标改为 \(u^*(x,y)=2\sin x+q\sin y\)，第二子域范数仍为 \(2+q\)。论文给出

\[
(2+q)^3<\frac8{\sqrt2-1}\approx19.31\quad\Longleftrightarrow\quad q<0.683
\]

时 PINN 更有利，\(q>0.683\) 时 XPINN 更有利。这个阈值来自特定的正弦、折线、等长度子域和等量采样假设，不能当作通用 XPINN 超参数阈值。

## 3. KdV：复杂度简化与样本减少大致抵消

### 设置

方程为 \(u_t+uu_x=0.0025u_{xxx}\)，\(x\in[-1,1],t\in[0,1]\)，初值为 \(u(x,0)=\cos(\pi x)\)，并使用周期条件。PINN 使用 18,000 residual 点、914 boundary 点和 102,400 个测试点；XPINN 在 \(x>-0.74\) 的波动右域使用 14,000 residual/646 boundary，在 \(x\le-0.74\) 的平滑左域使用 4,000 residual/268 boundary，并配置 10,000 个接口点。两种模型均为 10 层、宽度 20、sine 激活；Adam 学习率 1e-3，5,000 epochs，5 个固定种子。

### 数值

| 方法 | Train Loss | Relative L2 | Complexity | Bound |
|---|---:|---:|---:|---:|
| PINN | \(3.597\mathrm e{-3}\pm7.194\mathrm e{-4}\) | \(6.899\mathrm e{-1}\pm8.015\mathrm e{-3}\) | 100.00% | 100.00% |
| XPINN-R | \(5.619\mathrm e{-3}\pm5.056\mathrm e{-3}\) | \(6.955\mathrm e{-1}\pm9.905\mathrm e{-3}\) | 101.31% | 121.08% |
| XPINN-L | 未在表中给出 | 未在表中给出 | 28.50% | 未在表中给出 |

XPINN-L 的局部解更简单，但复杂的 XPINN-R 因样本减少而达到与 PINN 相近的范数。按表格与分节文字，PINN 略优；该案例支持“收益和代价平衡”而非 XPINN 必胜。

## 4. Heat：异质热源分区仍被样本不足拖累

### 设置与数值

热方程为 \(u_t=u_{xx}\)，解包含三角函数、双曲函数和指数项。PINN 使用 2,000 residual 点、200 boundary 点、160,801 个测试点，9 层宽度 20 的 tanh 网络，L-BFGS 学习率 1e-1；XPINN 按 \(t\le0.5\)（XPINN-B）和 \(t>0.5\)（XPINN-T）分区。训练 20,000 epochs，residual 与 residual-interface 权重为 1，boundary 与 boundary-interface 权重为 20，5 个固定种子。

| 方法 | Train Loss | Relative L2 | Complexity | Bound |
|---|---:|---:|---:|---:|
| PINN | \(8.589\mathrm e{-5}\pm2.218\mathrm e{-5}\) | \(1.778\mathrm e{-3}\pm2.195\mathrm e{-4}\) | 100.00% | 100.00% |
| XPINN-T | \(2.585\mathrm e{-4}\pm1.726\mathrm e{-4}\) | \(4.490\mathrm e{-3}\pm1.517\mathrm e{-3}\) | 156.24% | 243.22% |
| XPINN-B | 未在表中给出 | 未在表中给出 | 75.75% | 未在表中给出 |

顶部热源更复杂、同时只拥有一半数据，XPINN-T 范数高于 PINN；底部 XPINN-B 虽范数低，但底部角落误差较大。论文分节结论和表格均支持 PINN 优于 XPINN。

## 5. Advection：常值子域带来明显复杂度下降

### 设置与数值

方程为 \(u_t+0.5u_x=0\)，初值是 \([-0.2,0.2]\) 内的指示函数。PINN 使用 2,000 residual 点、200 boundary 点、6 层宽度 20 的 tanh 网络，Adam 学习率 1e-3；XPINN-LMR 沿移动不连续区域分成三个常值子域。训练 5,000 epochs，5 个固定种子；残差连续权重为 0，边界和边界接口权重为 1。

| 方法 | Train Loss | Relative L2 | Complexity | Bound |
|---|---:|---:|---:|---:|
| PINN | \(1.387\mathrm e{-5}\pm1.298\mathrm e{-5}\) | \(2.052\mathrm e{-1}\pm1.001\mathrm e{-1}\) | 100% | 100% |
| XPINN-L | \(4.239\mathrm e{-3}\pm2.385\mathrm e{-5}\) | \(1.617\mathrm e{-1}\pm3.582\mathrm e{-2}\) | 40.53% | 66.59% |
| XPINN-M | 未在表中给出 | 未在表中给出 | 53.16% | 未在表中给出 |
| XPINN-R | 未在表中给出 | 未在表中给出 | 79.95% | 未在表中给出 |

表格数值显示 XPINN-L 的相对 L2 和 bound 都低于 PINN，且三个子网范数都低于 PINN；不连续附近误差也更小。因此此处 XPINN 优于 PINN。注意原文 5.3.2 的一句话把“XPINN (2.052e-1)”与“PINN (1.617e-1)”写反，不能照抄该句。

## 6. Poisson：接口/边界权重的 trade-off 未被完全解决

### 设置

Poisson 方程为 \(u_{xx}+u_{yy}=f\)，\(f\) 在中央 \([0.25,0.75]^2\) 为 1、其余为 0，边界为零；因此残差在中央区域边缘不连续。PINN 使用 400 residual 点、80 boundary 点、1,002,001 个测试点，9 层宽度 20 的 tanh 网络，L-BFGS 学习率 1e-1；XPINN 以中央区域和其余区域分区，训练 20,000 epochs，5 个固定种子。

### 权重消融

| 方法 | Residual | Interface R | Additional I | Boundary | Interface B |
|---|---:|---:|---:|---:|---:|
| PINN | 1 | NA | NA | 20 | NA |
| XPINN1 | 1 | 20 | 0 | 20 | 20 |
| XPINN2 | 1 | 20 | 30 | 20 | 20 |
| XPINN3 | 1 | 20 | 30 | 80 | 20 |

`Additional I` 是靠近接口的一阶导数正则权重；XPINN2 用它减小接口误差，XPINN3 再把 boundary 权重从 20 提到 80。

### 数值

| 方法 | Relative L2 | Complexity/Norms | Bound |
|---|---:|---:|---:|
| PINN | \(5.553\mathrm e{-2}\pm2.936\mathrm e{-2}\) | 100.00% | 100.00% |
| XPINN1-A / XPINN1-M | \(4.022\mathrm e{-1}\pm1.648\mathrm e{-1}\) | 142.71% / 297.91% | 122.56% |
| XPINN2-A / XPINN2-M | \(1.387\mathrm e{-1}\pm7.030\mathrm e{-3}\) | 183.44% / 292.93% | 108.57% |
| XPINN3-A / XPINN3-M | \(1.108\mathrm e{-1}\pm1.561\mathrm e{-2}\) | 195.57% / 300.47% | 106.28% |

对应的 Train Loss 为：PINN \(2.688\mathrm e{-4}\pm3.411\mathrm e{-4}\)，XPINN1-A \(1.181\mathrm e{-2}\pm4.319\mathrm e{-3}\)，XPINN2-A \(1.016\mathrm e{-2}\pm3.713\mathrm e{-3}\)，XPINN3-A \(1.621\mathrm e{-2}\pm5.222\mathrm e{-3}\)；M 子网的 Train Loss 未在表中单列。按误差和 bound，PINN < XPINN3 < XPINN2 < XPINN1。XPINN1 在接口附近误差大；XPINN2 的额外接口正则改善接口却放大边界误差；XPINN3 提高 boundary 权重后总体改善，但接口误差又上升。所有 XPINN 子网范数都高于 PINN，说明子域数据不足的负面影响超过了解复杂度分解收益。

## 7. Compressible Euler：分区必须围绕 shock 结构

### 设置与数值

二维稳态无粘可压缩 Euler 方程用于 Mach 2、-10° 入流的斜激波问题，激波角为 29.3°。论文用 10,000 residual 点、5 hidden layers、每层 20 个神经元、tanh 激活和 8e-4 学习率，报告密度 \(\rho\) 的相对 L2；没有在该段明确给出优化器。XPINN-AM 按“两个常值区域 + 中间 shock strip”分区，另用 \(y=0.5\) 构造 XPINN-TB。

| 方法 | Train Loss | Relative L2 in \(\rho\) | Norms | Bound |
|---|---:|---:|---:|---:|
| PINN | \(1.819\mathrm e{-3}\pm6.043\mathrm e{-4}\) | \(3.4604\mathrm e{-2}\pm7.385\mathrm e{-3}\) | 100.00% | 100.00% |
| XPINN-A | \(9.210\mathrm e{-4}\pm1.882\mathrm e{-4}\) | \(1.048\mathrm e{-2}\pm5.3793\mathrm e{-3}\) | 37.28% | 81.09% |
| XPINN-M | 未在表中给出 | 未在表中给出 | 64.37% | 未在表中给出 |
| XPINN-T | \(1.067\mathrm e{-3}\pm4.829\mathrm e{-4}\) | \(3.5722\mathrm e{-2}\pm4.290\mathrm e{-3}\) | 42.37% | 137.63% |
| XPINN-B | 未在表中给出 | 未在表中给出 | 131.26% | 未在表中给出 |

正文把 XPINN-A/M 合称 XPINN-AM，结论是其 shock-aware 分区优于 PINN；简单 top/bottom 分区的 bottom 子网范数升至 131.26%，因此 XPINN-TB 不稳定。该案例支持“按解的物理结构分区”，而不是“任意均匀切块”。

## 8. 结果中的原文不一致与证据边界

1. **Advection 叙述对调：** 表 3 的 PINN 是 0.2052、XPINN-L 是 0.1617，但 5.3.2 一句文字反写了方法标签；本文按表格和 bound 判定 XPINN 更好。
2. **Conclusion 清单矛盾：** 结论一处把 Heat 列入 XPINN 胜出案例，另一处又把 Heat 列入 PINN 胜出案例；正文 5.2 和表 2 明确是 PINN 更好。
3. **wave/Poisson 名称矛盾：** 结论提到 wave equation，但正文五个实验实际是 KdV、Heat、Advection、Poisson、Compressible Euler；这里不把未出现的 wave 结果当作证据。
4. **缺失单项不补全：** KdV 的 XPINN-L、Heat 的 XPINN-B、Euler 的 XPINN-M/B 只在表中给出复杂度/范数，不能由此推算它们的相对 L2 或训练损失。
5. **理论覆盖边界：** KdV 和 Euler 的实验 bound 与 Theorem 3.1/3.2 的线性二阶假设不完全匹配；这些 bound 应记录为作者采用的经验指标，而不是严格定理保证。

## 9. 可复现性

论文报告了主要训练配置和 5 个固定种子，官方实现入口为 `https://github.com/AmeyaJagtap/XPINNs`。但本文实验的完整脚本、精确数据打包与独立 dataset URL 未在原文中作为一个可核验 bundle 给出，故 `reproducibility: medium`、`dataset_url: []`。

## 关联

- [[hu2022-xpinn-generalization-analysis]]
- [[hu2022-xpinn-generalization-method]]
- [[hu2022-xpinn-generalization-critical]]
- [[xpinn-generalization]]
- [[pinn]]
- [[fbpinn]]
- [[causal-training]]

^[sources/papers/hu2022-xpinn-generalization]
