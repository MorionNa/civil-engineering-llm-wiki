---
id: papers--li2025-node-onet-analysis
title: Deep Neural ODE Operator Networks for PDEs (NODE-ONet)：物理编码神经常微分方程算子网络
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- evidence/paper
- method/neural-operator
- method/pinn
keywords:
- digital-twin
- neural-ode
- neural-operator
- operator-learning
- physics-encoded-network
- pinn
- scientific-machine-learning
sources:
- sources/papers/li2025-node-onet.md
created: '2026-07-23'
updated: '2026-07-31'
confidence: high
---

# NODE-ONet：物理编码神经 ODE 算子网络

> 原文标题：Deep Neural ODE Operator Networks for PDEs

## 1. 核心问题

传统 PDE 数值方法精度高但在高维、多参数重复求解场景计算成本高。算子学习通过离线训练、在线推理学习参数到解的映射，但现有 DeepONet、MIONet 等方法通常采用通用神经网络，忽略 PDE 内在结构，导致时间动力学捕获不足以及训练时间范围外预测能力有限。论文提出 NODE-ONet，通过物理编码 Neural ODE 学习 PDE 解算子。

## 2. 科学问题

如何让神经算子不仅拟合输入输出关系，还能够利用 PDE 中已有的动力学结构，从而提高：

- 时间演化预测能力；
- 超出训练时间范围的外推能力；
- 多输入函数情况下的泛化能力。

## 3. 方法机制

NODE-ONet 采用 encoder-decoder 架构：

```
PDE参数
 ↓
Encoder（空间离散）
 ↓
Latent state
 ↓
Physics-encoded Neural ODE
 ↓
Decoder（空间重构）
 ↓
PDE解
```

三个核心部分：

### (1) Encoder

将无限维函数映射到有限维 latent space，例如：

- 网格采样；
- 有限元基函数；
- Fourier basis。

### (2) Physics-encoded NODE

核心创新不是简单使用 Neural ODE，而是在 NODE 结构中嵌入 PDE 特征。

例如扩散-反应方程中保持：

- 扩散系数与状态的双线性关系；
- 反应项非线性关系；
- 外部源项加性关系。

### (3) Decoder

根据空间基函数恢复连续场。

## 4. 物理编码思想

传统 Neural Operator：

$$v\rightarrow u$$

直接学习算子。

NODE-ONet：

$$v\rightarrow z(t)\rightarrow u$$

其中 latent dynamics 满足：

$$\dot z=N_\theta(z,t,v)$$

并通过网络结构保持 PDE 形式特征。

## 5. 损失函数

主要采用数据监督：

$$L(\theta)=\frac1{N}\sum ||\Psi_{NODE-ONet}(v)-\Psi^\dagger(v)||^2+\lambda R(\theta)$$

同时论文指出，也可以替换为 PINN 风格 PDE residual loss。

因此其物理约束主要位于：

- 网络结构（physics-encoded NODE）；
- 可选 PDE residual。

而不是单纯依赖 loss。

## 6. 结果证据

论文验证：

- 非线性 diffusion-reaction 方程；
- Navier-Stokes 方程。

主要发现：

- 相比 DeepONet/MIONet，NODE-ONet 使用更少参数获得相当或更高精度；
- 对多输入函数具有更高效率；
- 能够预测超过训练时间范围的动力演化。

## 7. 核心贡献

1. 提出 NODE-ONet 算子学习框架；
2. 将 PDE 结构编码到 Neural ODE，而非仅作为训练约束；
3. 实现时间变量与空间变量解耦，提高长期预测能力；
4. 提供 encoder-decoder 算子近似误差分析。

## 8. Negative Knowledge

- 当前主要验证 PDE，不直接针对结构动力学；
- 物理编码依赖已知 PDE 形式；
- 对未知本构非线性没有显式建模；
- 主要研究抛物型 PDE，双曲波动问题仍需扩展。

## 9. 对结构动力响应研究的启示

NODE-ONet 与 SeisGPT、PGT、CM-PINNs形成互补：

|方法|物理进入位置|
|-|-|
|CM-PINNs|本构/损失约束|
|PGT|Attention传播|
|SeisGPT|结构算子传播|
|NODE-ONet|连续时间动力算子|

对于非线性结构动力响应，可以考虑：

$$\dot z=F_\theta(z,M,K,C,f_{NL})$$

将：

- 质量矩阵；
- 刚度矩阵；
- 阻尼；
- 本构状态变量

编码进入 latent dynamics。

## 10. 可迁移知识

- 将动力系统学习从离散时间预测转向连续时间算子；
- 通过结构编码降低神经网络学习负担；
- encoder-decoder 可用于不同尺度物理模型之间映射；
- 适合数字孪生中的快速代理求解。

## 关联

- [[node-onet]]
- [[pgt]]
- [[seisgpt]]
- [[cm-pinns]]

## 11. 研究机会 (Research Opportunity)

- 在更复杂边界、非线性、多尺度和高维任务上检验方法边界。
- 对照统一 wall-clock、精度、稳定性和数据效率指标开展复现。

## 12. 可复现性 (Reproducibility)

- 复现应以本页列出的原始来源、代码、数据与超参数为准。
- 未公开实现细节应记录为复现缺口，不以模型推测补齐。

## Paper Family Pages

- [[li2025-node-onet-method]]
- [[li2025-node-onet-results]]
- [[li2025-node-onet-critical]]

## Evidence By Source

### `sources/papers/li2025-node-onet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2510.15651v1.pdf`

^[sources/papers/li2025-node-onet.md]
