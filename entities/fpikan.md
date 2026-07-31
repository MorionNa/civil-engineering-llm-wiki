---
id: entities--fpikan
title: FPIKAN — Fourier-enhanced Physics-Informed Kolmogorov–Arnold Network
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- entity/model
- method/pinn
keywords:
- deep-learning
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- entity/model
- equation-of-motion
- ground-motion
- limitation
- method/pinn
- neural-network
- physics-constrained-loss
- physics-informed
- pinn
- seismic-response
- soft-constraint
- structural-dynamics
- vibration-analysis
sources:
- raw/papers/extracted/10_1007_s10518-026-02408-w_abstract_extracted.txt
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

# FPIKAN

> **证据范围：ABSTRACT ONLY（仅出版社摘要）**
> 本实体只记录摘要可确认的模型轮廓。任何架构、公式、算例、数字或代码信息若未列在“已确认”中，均待全文核验。

## 定义

FPIKAN 是 Tao 等（2026）提出的 Fourier 增强物理信息 Kolmogorov–Arnold 网络，用于地震激励下结构响应计算。摘要确认它结合三项机制：

```text
structural-response inputs
  → Fourier input encoding
  → KAN with Fourier-series-parameterized activations
  → response approximation
  ↘ physics-constrained loss during training
```

原始论文摘要级概览：[[tao2026-fpikan]]。

## 已确认的模型组件

| 组件 | 可确认作用 | 尚未核实 |
|------|------------|----------|
| Fourier input encoding | 增强混合高低频输入的表示 | 频率来源、数量、尺度、是否可训练 |
| Fourier-series KAN activations | 用 Fourier 级数参数化 KAN 激活 | 网络层数、级数阶数、连接方式、参数量 |
| physics-constrained loss | 以结构响应物理约束训练 | 具体方程、初边值项、权重和数据项 |

## 物理与非线性边界

摘要没有说明实验结构是否含塑性、损伤、滞回或非线性恢复力，因此不能把 FPIKAN 归为材料本构非线性模型。当前只确认：它对结构地震响应方程进行神经网络逼近，并用物理损失约束训练。

Fourier-series KAN 激活的非线性属于网络表示，不等于结构物理非线性。全文未取得前，不应声称 FPIKAN 已验证非线性结构、[[bouc-wen-model]] 或其他本构。

## 与相关方法的区别

| 方法 | 摘要/知识库可确认差异 |
|------|----------------------|
| [[pinn]] | FPIKAN 继承 physics loss，但改造输入与网络激活的频谱表示 |
| [[kin]] | KIN/KINN 主要使用 B-spline KAN；FPIKAN 摘要确认使用 Fourier-series activations，并增加 Fourier input encoding |
| [[du2026-hcff-pinn-analysis]] | HCFF-PINN 全文确认结构频率先验与初值硬约束；FPIKAN 摘要未确认这两项 |
| [[neural-tangent-kernel]] | NTK 可解释谱偏差，但摘要未确认 FPIKAN 推导或测量 NTK |

## 摘要确认的验证主题

作者称模型面向：

- 混合高频与低频地震响应；
- 传统 PINN 的谱偏差；
- 噪声数据；
- 缺失观测；
- 低采样频率。

摘要只给出准确性、稳定性和鲁棒性的定性判断，没有任何可记录的误差、速度或统计数字。

## 待全文核验清单

1. 控制方程、结构自由度、线性/材料非线性类型；
2. Fourier 输入编码公式、频率选择及维度；
3. KAN 层数、宽度、Fourier 阶数和参数约束；
4. physics loss 组成、权重、是否含监督数据和初边值条件；
5. 地震记录、噪声水平、缺失比例、采样率、数据划分；
6. 对照模型、误差数字、消融、训练时间和硬件；
7. 官方代码、模型权重、数据地址与许可证。

## 可复现性

- **等级：** low；
- **代码：** 摘要未提供；
- **数据：** 可向通讯作者合理请求；
- **当前可复现范围：** 只能实现“Fourier 编码 + Fourier-series KAN + physics loss”的概念原型，不能声称复现论文。

## 关联页面

- [[tao2026-fpikan]] — 摘要级论文概览
- [[pinn]] — 基础范式
- [[kin]] — KAN-PINN 相关实体
- [[du2026-hcff-pinn-analysis]] — Fourier 增强结构动力 PINN 全文对照

## Evidence By Source

### `raw/papers/extracted/10_1007_s10518-026-02408-w_abstract_extracted.txt`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/extracted/10_1007_s10518-026-02408-w_abstract_extracted.txt]
