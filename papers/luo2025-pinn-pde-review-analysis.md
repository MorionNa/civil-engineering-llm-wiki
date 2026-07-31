---
id: papers--luo2025-pinn-pde-review-analysis
title: Luo et al. (2025) PINN 求解 PDE 综合综述：分类框架与证据边界
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
- method/transformer
keywords:
- adaptive-weighting
- ai4s
- collocation-strategy
- comparison
- inverse-problem
- neural-tangent-kernel
- physics-informed
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
- architecture-comparison
- adaptive-sampling
- loss-design
- feature-embedding
results:
- pinn-taxonomy
- application-map
- software-comparison
- hybrid-adaptive-sampling-example
failure_modes:
- no-systematic-search-protocol
- heterogeneous-evidence
- unclear-coverage-cutoff
- no-reproducible-review-corpus
reproducibility: low
contested: false
---

# Physics-informed neural networks for PDE problems: a comprehensive review

> **作者：** Kuang Luo, Jingshang Zhao, Yingping Wang, Jiayao Li, Junjie Wen, Jiong Liang, Henry Soekmadji, Shaolin Liao
> **期刊：** Artificial Intelligence Review, 58:323 (2025)
> **DOI：** 10.1007/s10462-025-11322-7
> **证据口径：** 本页严格区分【综述归纳】、【被引研究报告】和【作者既有工作示例】；除 HA 采样表格外，论文没有开展统一重跑实验。

## 1. 工程背景 (Engineering Background)

> **⚡ 非线性类型：** 这是一篇跨问题综述，**不能归为单一非线性类型**。它同时覆盖 PDE 算子非线性（如 Burgers、Navier–Stokes，参见 [[raissi2019-pinn-analysis]]）、材料本构非线性（弹塑性、超弹性、断裂，参见 [[wu2025-cm-pinn-analysis]]）以及线弹性动力响应（参见 [[chen2025-at-pinn-hc-analysis]]）。网络激活函数的“非线性”只是表示机制，也不能与上述物理非线性混为一类；跨论文比较时必须分别标注。

PDE 是流体、固体、传热、电磁和生物系统的基础模型。传统 FEM/FVM/FDM 在许多成熟问题上可靠，但面对高维参数空间、稀疏观测下的逆问题或数据—物理融合时，建模与反复求解成本可能很高。[[pinn]] 通过神经网络近似解、自动微分计算 PDE 残差，并把初边值条件和观测数据写入同一目标函数，提供了一个统一但并不自动可靠的替代路径。

## 2. Research Gap

【综述归纳】PINN 文献已从经典 MLP 扩展到 CNN、RNN、GAN、KAN、Transformer、域分解、自适应采样、损失重加权和特征嵌入，但这些改进分散在不同 PDE 与应用领域。读者缺少一张把“网络表示—训练点—损失—输入特征—应用—软件”串起来的路线图。

【批判边界】论文没有报告系统综述所需的数据库、检索式、检索日期、纳排标准和质量评价，因此这里的 gap 是“需要叙事性全景整理”，不是经过 PRISMA 式流程证明的完整证据缺口。

## 3. 科学问题 (Scientific Question)

PINN 求解 PDE 的性能瓶颈究竟分布在哪些设计层：网络架构、配点采样、多损失优化、特征表示还是问题物理？这些改进路线之间如何形成可用于选型的分类框架，又有哪些共同失败边界尚未解决？

## 4. 研究目标 (Research Objective)

论文旨在：介绍 PINN 基础公式与评价指标；按架构、采样、损失、激活及特征增强梳理代表工作；概览流体、固体、电磁/光学应用与开源框架；最后总结高频、多尺度、多物理、噪声数据和可扩展性挑战，并把算子学习列为后续方向。

## 5. 方法机制 (Method & Mechanism)

详见 [[luo2025-pinn-pde-review-method]]。这篇综述**没有提出一个新的中心算法**，其方法是建立多轴叙事分类：

1. **基础层：** 用统一的 PDE 残差、初值、边界与数据损失描述经典 PINN；
2. **表示层：** MLP、CNN、RNN、GAN、KAN、Transformer 与 NAS/可分离/残差网络；
3. **求解层：** 域分解、激活函数、残差自适应采样、损失重加权和新损失；
4. **输入层：** Fourier、先验字典、正弦和维度增强；
5. **落地层：** 应用领域、软件框架、挑战与算子学习展望。

## 6. 结果证据 (Result & Evidence)

详见 [[luo2025-pinn-pde-review-results]]。

- 【综述归纳】表 2 给出 PINN 求解器的主要方法族，但它是代表性清单，不是计量统计或质量排序。
- 【综述归纳】表 4 对 DeepXDE、IDRLnet、NeuroDiffEq、SciANN、TensorDiffEq 的后端作了简表；未做版本、功能或性能基准。
- 【作者既有工作示例】表 3 报告 1D Poisson 上 HA 采样与 PINN、Random-R、RAD 的十次重复 L² 相对误差；这是 Luo et al. (2025) 既有工作的复述，不是对全文方法族的统一新实验。
- 【被引研究报告】文中引用了 KAN/[[kin]]、Transformer、NTK、域分解等工作的性能结论，但综述作者没有在同一代码、预算或数据上复核。

## 7. 贡献 (Contribution)

1. 将 PINN 改进组织为“架构—采样—损失—特征”的可操作分类框架；
2. 把理论动机、应用地图、软件入口与挑战展望放在同一篇入门综述中；
3. 通过基础公式和三类指标（L² 相对误差、RMSE、PDE 残差）建立共同语言；
4. 把 KAN/[[kin]]、Transformer 与算子学习纳入 PINN 演进路线，便于连接经典 [[raissi2019-pinn-analysis]] 与后续架构改造。

## 8. 核心知识点 (Core Knowledge)

- PINN 不是单一网络，而是一套耦合设计：**表示能力 × 配点覆盖 × 多损失平衡 × 优化动力学 × 物理先验**。
- 低 PDE 残差不能单独证明解正确；应结合参考解误差、守恒/边界检查和失败诊断。该边界可与 [[wang2023-pinn-spurious-analysis]] 对照。
- 架构替换（如 [[kin]]）、自适应采样和损失加权解决的是不同瓶颈，不能把一个算例上的优势外推为普遍优越。
- 算子学习追求跨参数/函数族复用，而经典 PINN 通常针对单个 PDE 实例优化；二者是互补演进，不是简单替代。

## 9. Negative Knowledge

详见 [[luo2025-pinn-pde-review-critical]]。

- “comprehensive” 没有可审计的检索协议支撑，不能据此推断领域无遗漏。
- 被引论文使用不同 PDE、精度指标、训练预算和基线，横向性能数字不可直接拼表排名。
- 文中把许多成功案例概括为 PINN 的通用优势，但 [[wang2021-pinn-ntk-failure-analysis]]、[[wang2023-pinn-spurious-analysis]] 与 [[wang2024-causal-pinn-analysis]] 表明，梯度谱、伪解和时序因果是彼此不同的失败机制。
- 对作者团队 HA/DaPINN 工作的展示比其他路线更具数值细节，使用时应寻求独立基准验证。

## 10. 可迁移知识 (Transferable Knowledge)

可把综述的四轴分类变成项目选型表：先诊断问题是高频/多尺度、局部残差集中、多损失失衡还是边界/因果传播失败，再分别选择架构、采样、加权或约束策略。不要“堆叠所有技巧”；每次只改变一个机制，并用统一预算和多随机种子验证。

## 11. 研究机会 (Research Opportunity)

1. 建立可更新、带检索式和纳排记录的 PINN living review；
2. 在统一 PDE 套件、算力预算和随机种子下做架构 × 采样 × 损失的因子实验；
3. 把三类物理非线性分层标注，避免把算子非线性、本构非线性和训练非线性混写；
4. 将 [[wang2021-pinn-ntk-failure-analysis]]、[[wang2023-pinn-spurious-analysis]]、[[wang2024-causal-pinn-analysis]] 的诊断整合为面向工程的失败检测流程；
5. 比较经典 PINN、[[kin]] 与神经算子在单实例精度、跨参数复用和总计算成本上的边界。

## 12. 可复现性 (Reproducibility)

**🔴 低复现性。** 全文可访问、公式和代表方法清楚，但综述语料与筛选过程不可重建；作者既有 HA 数值表也没有在本文附带代码、原始数据或完整训练配置。

| 项目 | 说明 |
|------|------|
| **等级** | 🔴 low |
| **官方代码** | 无综述配套代码 |
| **数据集** | 声明可向通讯作者索取，但未给出公开数据地址；综述文献语料未公开 |
| **协议** | 文章为 CC BY-NC-ND 4.0；代码/数据协议未说明 |
| **复现要点** | 需补齐检索数据库、检索式、截止日期、去重/筛选记录、证据提取表，以及 HA 示例的实现与随机种子 |

## 关联页面

- [[pinn]] — 综述所覆盖的中心范式
- [[raissi2019-pinn-analysis]] — 经典 PINN 基线
- [[wang2021-pinn-ntk-failure-analysis]] — 多损失谱失衡
- [[wang2023-pinn-spurious-analysis]] — 低残差伪解边界
- [[wang2024-causal-pinn-analysis]] — 时域因果训练
- [[kin]] — 综述收录的 KAN-PINN 架构分支

## Evidence By Source

### `sources/papers/luo2025-pinn-pde-review.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1007_s10462-025-11322-7.pdf`

^[sources/papers/luo2025-pinn-pde-review.md]
