---
id: papers--tao2026-fpikan
title: Tao et al. (2026) FPIKAN：Fourier 特征增强的物理信息 KAN（摘要级概览）
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
keywords:
- deep-learning
- equation-of-motion
- ground-motion
- limitation
- neural-network
- physics-constrained-loss
- physics-informed
- pinn
- seismic-response
- soft-constraint
- structural-dynamics
- vibration-analysis
sources:
- sources/papers/tao2026-fpikan.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: medium
evidence_scope: abstract-only
methods:
- fourier-input-encoding
- fourier-series-kan-activations
- physics-constrained-loss
results:
- multi-frequency-response
- high-frequency-response
- noise-robustness
- missing-sample-robustness
- low-frequency-sampling
failure_modes:
- abstract-only-evidence
- unverified-architecture
- unverified-benchmarks
- unverified-physical-nonlinearity
- missing-code
reproducibility: low
contested: false
---

# Physics-informed Kolmogorov–Arnold network with Fourier features for structural response computation under earthquake excitation

> **证据范围：ABSTRACT ONLY（仅出版社摘要）**
> 本页不是全文精读。只能确认摘要明确写出的模型组件、目标问题和定性结论；网络层数、Fourier 频率设置、KAN 拓扑、物理损失公式、实验结构、误差数字、训练时间、优化器、代码与数据细节均未核实。

> **作者：** Dongwang Tao, Jiaxin Li, Ke Du, Zheng Lu
> **期刊：** *Bulletin of Earthquake Engineering*, 24, 3795–3817 (2026)
> **DOI：** 10.1007/s10518-026-02408-w
> **标题说明：** 本地摘要记录使用替代题名 “A Fourier-enhanced physics-informed Kolmogorov–Arnold network for multi-frequency seismic response analysis of structures”；本页采用任务提供的正式出版题名。

## 1. 工程背景与非线性边界

> **⚠️ 非线性类型：摘要不足以判定。** 摘要只确认研究对象为地震激励下的结构响应、多频/高频成分和 physics loss，没有说明结构模型是否包含塑性、损伤、滞回或非线性恢复力。因此只能确认其处理**结构响应方程与神经网络逼近**，不能宣称已经验证材料本构非线性或非线性结构。Fourier 级数参数化的 KAN 激活属于网络表示非线性，也不等于物理系统非线性。

标准 [[pinn]] 往往存在谱偏差：先拟合低频、较难重建高频或混合频率响应。地震结构响应还可能面临噪声、观测缺失和低采样频率，使高频局部特征更容易丢失。FPIKAN 试图同时改造输入频谱表示、KAN 激活表示和物理约束训练。

## 2. 摘要确认的方法

| 组件 | 摘要可确认内容 | 摘要无法确认内容 |
|------|----------------|------------------|
| Fourier input encoding | 对网络输入进行 Fourier 编码，以增强多频表示 | 映射公式、频率数量/尺度、是否使用结构固有频率 |
| Fourier-series KAN activations | KAN 激活函数由 Fourier 级数参数化 | 层数、宽度、阶数、系数约束、激活位于边还是节点的具体实现 |
| physics-constrained loss | 训练目标包含物理约束 | 控制方程、初边值项、各 loss 权重、是否有监督数据项 |

三项组件共同构成 [[fpikan]]。与以 B-spline KAN 为核心的 [[kin]] 相比，摘要明确的差异是 Fourier 级数激活与额外 Fourier 输入编码；但无法据此判断参数量、计算复杂度或哪一项贡献最大。

## 3. 摘要确认的研究目标与结果

摘要称 FPIKAN 面向混合高、低频地震激励下的结构响应，目标是缓解传统 PINN 的谱偏差，并提高以下场景的预测表现：

- 多频与高频响应；
- 含噪观测；
- 缺失观测样本；
- 低频率采样。

作者定性报告准确性、稳定性与鲁棒性提升，但摘要没有给出结构类型、自由度、地震记录、噪声强度、缺失比例、采样率、对照模型、误差数字或重复试验。因此不能量化提升，也不能推断对真实工程结构普遍有效。

## 4. 与知识库方法的关系

- [[pinn]] — FPIKAN 使用 physics-constrained loss 的基础范式；
- [[kin]] — KAN 与 physics-informed 学习结合的既有路线；
- [[neural-tangent-kernel]] — 可解释谱偏差的理论工具，但摘要**没有确认 FPIKAN 做了 NTK 分析**；
- [[du2026-hcff-pinn-analysis]] — 同一研究团队的 Fourier 增强结构动力 PINN；HCFF-PINN 的全文确认了结构频率先验和初值硬约束，而本摘要不能证明 FPIKAN 也使用这两项；
- [[fpikan]] — 本文新模型实体。

## 5. 核心贡献（摘要级判断）

1. 在输入端加入 Fourier 编码以增强多频表达；
2. 用 Fourier 级数参数化 KAN 激活，而非只使用传统固定激活或常见 B-spline KAN；
3. 将上述表示与 physics loss 结合，面向地震结构响应的谱偏差；
4. 把噪声、缺失样本与低采样频率纳入鲁棒性讨论。

## 6. Negative Knowledge 与待全文核验

- 摘要未说明物理方程是线性还是非线性，不能给出材料本构非线性标签；
- 未确认是否无标签训练、是否硬编码初值/边界、是否使用自动微分；
- 未确认 Fourier 输入频率是否随机、可学习或由结构固有频率指导；
- 未确认 Fourier-series KAN 的级数阶数、正则化、参数量和复杂度；
- 未确认实验结构、地震记录、数据划分、噪声/缺失方案和基线；
- 未提供任何误差、训练时间、加速比或统计显著性数字；
- 未在摘要中提供代码仓库或公开数据链接；
- “鲁棒”是作者摘要级定性结论，不能替代真实记录、振动台或实测结构验证。

## 7. 可复现性

**🔴 低复现性 / 摘要证据。** 当前只能重建模型概念，不能重建架构、损失或实验。

| 项目 | 说明 |
|------|------|
| **证据范围** | abstract-only |
| **官方代码** | 摘要未提供；不得推测代码地址 |
| **数据集** | supporting data available from the corresponding author on reasonable request |
| **可确认组件** | Fourier 输入编码；Fourier-series KAN 激活；physics-constrained loss |
| **可确认结果** | 作者定性声称多频/高频及噪声、缺失、低采样场景下更准确、稳定、鲁棒 |
| **待全文补充** | 控制方程、非线性类型、架构、损失、训练配置、算例、数字、消融、代码与数据 |

## 关联页面

- [[fpikan]] — FPIKAN 模型实体
- [[pinn]] — 标准物理信息神经网络
- [[kin]] — KAN-PINN 路线
- [[du2026-hcff-pinn-analysis]] — 可作 Fourier 结构动力方法对照的全文论文

## Evidence By Source

### `sources/papers/tao2026-fpikan.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/extracted/10_1007_s10518-026-02408-w_abstract_extracted.txt`

^[sources/papers/tao2026-fpikan.md]
