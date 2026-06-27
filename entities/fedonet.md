---
title: "FEDONet — Fourier-Embedded DeepONet (傅里叶嵌入深度算子网络)"
created: 2026-06-27
updated: 2026-06-27
type: entity
tags: [fedonet, deeponet, fourier-features, neural-operator, operator-learning, spectral-accuracy, ai4s, pde-surrogate]
sources: [raw/papers/10_1016_j_jcp_2026_114931_extracted.txt]
confidence: high
---

# FEDONet — Fourier-Embedded DeepONet

## 定义

**FEDONet（Fourier-Embedded Deep Operator Network）** 是由 Sojitra et al. (2026, JCP) 提出的神经算子架构，在标准 DeepONet 的 trunk 网络（可选 branch 网络）中嵌入**随机 Fourier 特征（Random Fourier Features, RFF）**，使网络在不增加可训练参数的条件下获得**谱精度（spectral accuracy）**的空间表达能力。

```
FEDONet = DeepONet(branch-trunk) + Fourier Embedding Layer
```

## 核心创新

| 组件 | 标准 DeepONet | FEDONet |
|------|-------------|---------|
| Trunk 输入处理 | 坐标 y → 全连接 | 坐标 y → **γ(y) = [cos(By), sin(By)]** → 全连接 |
| 空间表达精度 | 代数精度（受谱偏置限制） | **谱精度**（Fourier 基展开） |
| 可训练参数 | 基准 | **相同**（频率矩阵 B 固定不可训练） |
| 高频捕捉能力 | 弱（低频主导） | **强**（Fourier 基天然覆盖全频谱） |

## 数学原理

Fourier 嵌入的核心是随机 Fourier 特征映射：

$$\gamma(y) = [\cos(2\pi B_1 \cdot y), \sin(2\pi B_1 \cdot y), \ldots, \cos(2\pi B_m \cdot y), \sin(2\pi B_m \cdot y)]$$

其中 $B_i \sim \mathcal{N}(0, \sigma^2 I)$。后续全连接层 $W \cdot \gamma(y)$ 等价于自适应 Fourier 级数：

$$f(y) \approx \sum_{k=1}^{m} \left[a_k \cos(2\pi B_k \cdot y) + b_k \sin(2\pi B_k \cdot y)\right]$$

这使网络天然具备谱方法的高精度特性。

## 关键超参数

| 参数 | 含义 | 指导 |
|------|------|------|
| **σ**（频率尺度） | 高斯分布标准差，控制嵌入的最高频率 | PDE 特征频率的 3-5 倍；混沌/刚性系统取大，光滑系统取小 |
| **m**（频率数量） | 嵌入维度的一半（2m 为输出维度） | 通常取输入维度 d 的 5-20 倍 |
| **p**（基函数数量） | DeepONet branch/trunk 的输出维度 | 与原 DeepONet 相同，无需因 Fourier 嵌入而调整 |

## 适用场景

### ✅ 特别适合

- 高频/多尺度 PDE（激波、相界面、混沌）
- 刚性问题（Allen-Cahn ε ≪ 1）
- 小数据场景（Fourier 嵌入提供强空间先验）
- 含噪声数据（中等噪声下天然鲁棒）
- 任何已有 DeepONet pipeline 的即插即用升级

### ⚠️ 增益有限

- 光滑解线性椭圆 PDE（如 2D Poisson）—— 解以低频为主，Fourier 嵌入边际收益低
- 极低频率 σ 选择不当——可能退化为标准 DeepONet

## 历史脉络

| 时间 | 事件 |
|------|------|
| 2007 | Rahimi & Recht 提出 Random Fourier Features (RFF) 用于大规模核方法 |
| 2020 | Tancik et al. 证明 Fourier Features 让 MLP 学习高频函数（NeRF 位置编码） |
| 2021 | Lu et al. 提出 DeepONet（Nature Machine Intelligence） |
| 2022 | Goswami et al. 提出 V-DeepONet（变分能量物理约束） |
| **2026** | **Sojitra et al. 提出 FEDONet** — 将 RFF 引入 DeepONet，实现谱精度算子学习 |

## 与其他算子的关系

```
神经算子家族:
├── DeepONet (Lu et al., 2021)
│   ├── V-DeepONet (Goswami et al., 2022) — 变分能量物理约束
│   ├── PI-DeepONet — PDE 残差物理约束
│   ├── MIONet — 多输入函数算子
│   └── FEDONet (Sojitra et al., 2026) ★ — Fourier 嵌入空间增强
├── FNO (Li et al., 2021) — Fourier 空间全局积分
├── NOMAD — 非线性流形解码
└── ...
```

> FEDONet 与 V-DeepONet 是**正交互补**的增强方向：一个提升空间表达能力，一个提升物理一致性。二者理论上可结合为"Fourier-V-DeepONet"。

## 关联论文（本 Wiki）

- [[sojitra2026-fedonet-analysis]] — FEDONet 论文分析（完整概述）
- [[sojitra2026-fedonet-method]] — FEDONet 方法展开
- [[sojitra2026-fedonet-results]] — FEDONet 结果展开
- [[sojitra2026-fedonet-critical]] — 贡献/知识/Negative/可迁移/机会
- [[deeponet]] — DeepONet 神经算子基础
- [[goswami2022-variational-deeponet-analysis]] — V-DeepONet（互补方向）

## 关联资源

- 原始论文：Sojitra, Dhingra, San (2026) "FEDONet: Fourier-embedded DeepONet for spectrally accurate operator learning", JCP
- Random Fourier Features 原始论文：Rahimi & Recht (2007) NIPS
- Fourier Features 在深度学习中的推广：Tancik et al. (2020) NeurIPS
- DeepONet 基础：Lu et al. (2021) Nature Machine Intelligence
