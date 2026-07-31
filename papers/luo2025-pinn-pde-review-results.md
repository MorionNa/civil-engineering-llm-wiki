---
id: papers--luo2025-pinn-pde-review-results
title: Luo et al. (2025) PINN-PDE 综述结果：分类、比较与证据层级
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- evidence/paper
- method/neural-architecture-search
- method/pinn
- method/transformer
keywords:
- collocation-strategy
- comparison
- deepxde
- physics-informed
- physics-simulation
- pinn
- review
sources:
- sources/papers/luo2025-pinn-pde-review.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- narrative-review
- taxonomy
- evidence-stratification
results:
- pinn-taxonomy
- hybrid-adaptive-sampling-example
- software-comparison
- application-map
failure_modes:
- heterogeneous-evidence
- no-unified-benchmark
- self-reported-comparisons
reproducibility: low
contested: false
---

# 结果展开：哪些是综述发现，哪些只是被引结果

> 返回概述 → [[luo2025-pinn-pde-review-analysis]]

## 6.1 结果证据分层

| 层级 | 本文中的证据 | 解读限制 |
|------|--------------|----------|
| A：综述结构证据 | 表 2 方法族、表 4 软件后端、应用与挑战章节 | 支持“覆盖了哪些路线”，不支持性能排名 |
| B：作者既有实验 | 表 3/图 10 的 HA 采样；图 12/13 的 DaPINN 案例 | 来自作者团队先前论文，不是本综述新建的统一实验 |
| C：被引研究报告 | Transolver、PAF、PINNsFormer、[[kin]] 等性能叙述 | 未由 Luo 等复跑，需回查原论文 |

## 6.2 分类结果：PINN 改进集中在四个部件

【综述归纳】表 2 的核心价值是把大量变体压缩为四个可组合部件：

1. **架构：** MLP、CNN、RNN、GAN、KAN、Transformer，以及 NAS-PINN、SPINN、PirateNets；
2. **空间/激活：** XPINN、cPINN、域分解、自适应激活、物理核/物理激活；
3. **训练：** RAR/RAD/R3/生成式采样、损失重加权、gPINN 等新损失；
4. **输入：** Fourier、先验字典、正弦和维度增强。

这个分类解释了为什么 [[wang2021-pinn-ntk-failure-analysis]]、[[wang2023-pinn-spurious-analysis]]、[[wang2024-causal-pinn-analysis]] 可以同时成立：它们分别处理收敛谱、目标函数伪解和时间因果，证据并不互相替代。

## 6.3 唯一成表的数值比较：HA 采样示例

【作者既有工作示例】1D Poisson 方程，指标为 L² 相对误差，十次重复给出均值 ± 标准差。$N_r$ 是残差点数。

| 方法 | 20k, Nr=14 | 20k, Nr=26 | 40k, Nr=14 | 40k, Nr=26 |
|------|-----------:|-----------:|-----------:|-----------:|
| PINN | 18.07% ± 3.70% | 6.82% ± 4.11% | 48.28% ± 36.22% | 15.30% ± 13.95% |
| Random-R | 3.76% ± 2.02% | 0.99% ± 1.37% | 2.52% ± 1.89% | 0.14% ± 0.06% |
| RAD, k=1,c=1 | 5.49% ± 4.53% | 2.23% ± 2.54% | 1.62% ± 1.28% | 1.02% ± 1.53% |
| RAD, k=1,c=2 | 3.31% ± 1.57% | 2.51% ± 2.81% | 2.21% ± 1.40% | 0.82% ± 0.82% |
| RAD, k=2,c=1 | 5.44% ± 4.95% | 3.78% ± 2.30% | 2.04% ± 2.06% | 1.11% ± 0.65% |
| RAD, k=2,c=2 | 6.00% ± 5.49% | 2.50% ± 2.44% | 1.87% ± 1.59% | 0.89% ± 1.01% |
| **HA (authors)** | **2.73% ± 2.38%** | **0.24% ± 0.21%** | **1.28% ± 0.76%** | **0.11% ± 0.08%** |

在表内四种设置中 HA 的均值最低，但只能支持“作者既有 HA 方法在该 1D Poisson 配置有效”。标准 PINN 在 40k 时误差和方差反而增大，也提示迭代数增加不保证收敛；不能据此推断 HA 在非线性、多维、噪声或复杂几何上普遍最优。

## 6.4 被引论文的选择性比较

以下数字均为【被引研究报告】，不是本综述的复跑结果：

| 路线 | 综述转述的结果 | 应如何使用 |
|------|----------------|------------|
| 梯度统计损失平衡 | Wang et al. 报告部分计算物理问题精度提高 50–100 倍 | 回查 PDE、预算与基线；与 [[wang2021-pinn-ntk-failure-analysis]] 的 NTK 机制区分 |
| Physical Activation Functions | 被引研究报告网络规模最多减少 75%，保持精度 | 不等于所有 PDE 都可缩小 75% |
| Transolver | 六个基准与工业仿真中报告 22% 相对增益 | 它更接近通用 PDE solver/算子模型，不能直接与单实例 PINN 混排 |
| KAN-PINN | 文中转述 KINN/PIKAN 在多尺度、奇异和异质问题上的优势 | 参见 [[kin]] 与 [[wang2024-kinn-results]]；复杂几何和训练成本仍是边界 |
| sf-PINN | 被引研究称精度可提高若干数量级 | 缺少统一设置，必须读原论文确认量级与稳定性 |

## 6.5 应用覆盖结果

| 应用域 | 综述覆盖 | 证据性质 |
|--------|----------|----------|
| 流体力学 | Navier–Stokes、尾流重建、高速可压缩流、血流 | 代表案例叙述，无统一比较 |
| 固体力学 | 线弹性、弹塑性、超弹性、断裂、正/逆问题 | 覆盖跨度大，但没有按非线性类型分层 |
| 电磁与光学 | Helmholtz、准线性算子、纳米光学逆散射 | 简要案例叙述 |

这些应用证明“PINN 已被尝试于多域”，不能证明其在每个域都优于 FEM/FVM/FDM。尤其结构地震响应需要另查本构、长时传播和多自由度证据，不能从本综述的“solid mechanics”一段直接推出。

## 6.6 软件对比

【综述归纳】表 4 只比较后端：

| 框架 | 后端（按论文） |
|------|----------------|
| DeepXDE | TensorFlow、PyTorch、JAX |
| IDRLnet | PyTorch |
| NeuroDiffEq | PyTorch |
| SciANN | TensorFlow |
| TensorDiffEq | TensorFlow |

该表没有比较维护状态、版本、边界条件 API、分布式能力、基准速度或许可证。选择工具时，[[notes/lectures/ai4s-pinn-deepxde]] 可作为 DeepXDE 实践入口，但仍需按当前版本验证。

## 6.7 综述自身可以成立的结论

1. PINN 的改进已从单一 MLP 扩展到表示、采样、损失、输入与域分解的多部件生态；
2. 高维、高频、多尺度、多物理和噪声/缺失数据仍是跨路线难点；
3. 现有成功结果高度依赖问题与训练配置，尚不存在由本文证据支持的“通用最佳 PINN”；
4. 算子学习是从单实例求解向函数到函数映射扩展的重要方向，但本文只作展望，未做实证比较。

## 页内导航

- [[luo2025-pinn-pde-review-analysis|← 概述]]
- [[luo2025-pinn-pde-review-method|← 分类方法]]
- [[luo2025-pinn-pde-review-critical|批判分析 →]]

## Evidence By Source

### `sources/papers/luo2025-pinn-pde-review.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1007_s10462-025-11322-7.pdf`

^[sources/papers/luo2025-pinn-pde-review.md]
