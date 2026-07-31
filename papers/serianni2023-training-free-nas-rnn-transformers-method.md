---
id: papers--serianni2023-training-free-nas-rnn-transformers-method
title: 'Serianni & Kalita (2023) — Method: Training-free NAS Proxies for RNNs and Transformers'
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- evidence/paper
- method/neural-architecture-search
- method/transformer
keywords:
- attention-confidence
- expressivity
- hidden-covariance
- rnn
- training-free-nas
- transformer
sources:
- sources/papers/serianni2023-training-free-nas-rnn-transformers.md
created: '2026-06-14'
updated: '2026-07-31'
confidence: high
parent:
- - serianni2023-training-free-nas-rnn-transformers-analysis
---

# Method: Training-free NAS Proxies for RNNs and Transformers

## 1. 方法总览

本文提出并评估了一系列训练-free NAS 代理指标，覆盖两类架构：

| 架构 | 新指标 | 借鉴的现有指标 | 评估 Benchmark |
|------|--------|---------------|---------------|
| RNN | Hidden Covariance | Jacobian Covariance, Synaptic Saliency, Activation Distance 等 | NAS-Bench-NLP |
| BERT Transformer | Attention Confidence, Softmax Confidence, Attention Importance | 同上 + Synaptic Diversity | 自建 FlexiBERT Benchmark |

核心方法论：**在初始化时，给网络一个 minibatch 输入，计算一个标量分数 S，该分数应与训练后的 validation loss / accuracy 呈正（或负）相关。**

---

## 2. Hidden Covariance（RNN 专用）

### 2.1 设计动机

RNN 的隐藏状态 H(X) 是层间信息传递的唯一载体。本文假设：**如果给定不同输入时，某一层的隐藏状态高度相似（低多样性），则网络难以从输入中提取区分性特征，训练难度大。** 这一假设与 Mellor et al. (2021a) 的 Activation Distance 指标思想一致，但直接作用于隐藏状态而非 ReLU 激活。

### 2.2 计算流程

给定 minibatch X = {x₁, ..., x_N}，对 RNN 的某一层：

1. **计算隐藏状态矩阵 H(X)**：形状为 (N, d)，其中 d 为隐藏维度
2. **中心化**：`M_H` 为按行均值矩阵，`(M_H)ᵢⱼ = (1/N) Σₙ Hᵢₙ`
3. **协方差矩阵**：`C = (H - M_H)(H - M_H)ᵀ`
4. **Pearson 相关系数矩阵**：`Rᵢⱼ = Cᵢⱼ / √(Cᵢᵢ · Cⱼⱼ)`
5. **KL 散度评分**：
   ```
   S(H) = -Σₙ [log(λₙ + k) + 1/(λₙ + k)]
   ```
   其中 λₙ 是 R 的特征值，k = 10⁻⁵（数值稳定项）

### 2.3 关键细节

- **可以按层分别计算**：本文发现对 RNN 第 1 层和第 2 层分别计算的 Hidden Covariance 性能最佳（τ = 0.37），高于对所有层求和
- **KL 散度的作用**：衡量相关系数矩阵特征值分布的"均匀程度"。特征值越均匀 → KL 散度越大 → 隐藏状态越多样化 → 网络越好
- **与 Jacobian Covariance 的区别**：前者操作在 loss 对输入的 Jacobian 上，后者操作在隐藏状态上——RNN 的隐藏状态比 Jacobian 包含更多架构特异信息

---

## 3. 现有通用训练-free 指标（迁移自 CNN）

本文评估了以下从 CNN 训练-free NAS 文献中迁移的指标：

### 3.1 Jacobian Covariance (Mellor et al. 2021b)

计算 loss 对输入 minibatch 的 Jacobian 矩阵 J = [∂L/∂x₁ ··· ∂L/∂x_N]，继而计算其协方差矩阵相关系数的 KL 散度。核心假设：Jacobian 越多样化 → 网络越容易学习。

- **变体**：Jacobian Cosine（用余弦相似度替代协方差）、Large Noise / More Noised（加噪输入测试鲁棒性）

### 3.2 Synaptic Saliency (Tanaka et al. 2020 → Abdelfattah et al. 2020)

源于网络剪枝的突触显著性分数，扩展为 NAS 指标：
```
S(θ) = Σᵢ (∂L/∂θᵢ ⊙ θᵢ)  # 对所有 N 个参数求和
```
衡量参数对 loss 的"重要程度"——去除重要参数会导致 layer collapse。

### 3.3 Activation Distance (Mellor et al. 2021a)

直接计算 mini-batch 输入间的 ReLU 激活 Hamming 距离。激活越相似 → 区分输入越困难 → 训练效果越差。

### 3.4 Synaptic Diversity (Zhou et al. 2022)

专为 ViT 设计，基于注意力头权重矩阵的核范数近似其秩：
```
SD = Σₘ ||∂L/∂Wₘ||_nuc ⊙ ||Wₘ||_nuc
```
核范数高 → 权重矩阵秩高 → 多样性好 → 避免 rank collapse。

---

## 4. 注意力头剪枝 → Transformer NAS 指标

### 4.1 改造思路

将剪枝文献中评估**单个注意力头重要性的分数**，扩展为评估**整个 Transformer 架构质量的分数**。公式：

```
A(X) = (1/H) Σₕ Aₕ(X)
```

其中 H 为注意力头总数，Aₕ 为第 h 个头的分数。

### 4.2 Attention Confidence (Voita et al. 2019)

衡量注意力头的输出"集中程度"——一个高置信度的头将其注意力高度集中在单个 token 上：
```
Aₕ(X) = (1/N) Σₙ ||max(Attₕ(xₙ))||
```
其中 Attₕ(xₙ) 是第 h 个头对输入 xₙ 的注意力输出向量。max 取输出的最大值（表示该头最关注的 token 的权重）。

**直觉**：高置信度的头承担了关键的 token 级信息提取任务，对模型性能贡献大。

### 4.3 Softmax Confidence (Behnke & Heafield 2020)

类似 Attention Confidence，但直接看 softmax 层的概率分布最大值：
```
Aₕ(X) = (1/N) Σₙ ||max(σₕ(xₙ))||
```
softmax 最大值大 → 该头的注意力分布尖锐 → 头"确定"自己在关注什么。

### 4.4 Attention Importance (Michel et al. 2019)

通过注意力输出对其权重的梯度来评估头的重要性——类似"剪掉这个头后 loss 会变多少"的一阶近似：
```
Aₕ(X) = ||Attₕ(X) · ∂L(X)/∂Attₕ(X)||
```
重要性高 → 该头对 loss 贡献大 → 该头关键。

---

## 5. BERT NAS Benchmark 构建

### 5.1 搜索空间：FlexiBERT (Tuli et al. 2022)

| 超参数 | 取值 |
|--------|------|
| Hidden dimension | {128, 256} |
| Number of Encoder Layers | {2, 4} |
| Attention operator type | {self-attention (scaled dot-product / multiplicative), linear transform (DFT / DCT), span-based dynamic conv (kernel 5 / 9)} |
| Number of operation heads | {2, 4} |
| Feed-forward dimension | {512, 1024} |
| Number of feed-forward stacks | {1, 3} |

关键特性：**encoder 层异构**，每层可独立选择 attention type 和参数。总搜索空间：10,621,440 架构。大小范围覆盖 BERT-Tiny 到 BERT-Mini。

### 5.2 训练方案

- **预训练**：ELECTRA (Clark et al. 2020) — 替换 token 检测任务，比 MLM 高效
- **语料**：OpenWebText (38 GB, 8M 文档)
- **步数**：100,000（经 10 架构消融确定的最优 trade-off）
- **微调评估**：GLUE benchmark（不含 WNLI）
- **硬件**：TPUv2-8，总计 ~25 TPU-days
- **采样**：500 架构随机采样

### 5.3 归一化策略

所有 Transformer 指标均按特征数归一化以避免参数量混淆：
```
S_normalized = S_raw / (number_of_features_in_architecture)
```
未归一化结果也在附录中报告，以揭示参数量偏差。

---

## 6. 评估协议

### 6.1 相关性度量

- **Kendall τ**（排序相关性）：衡量指标排序与真实性能排序的一致性
- **Spearman ρ**（等级相关性）：补充评估

### 6.2 消融实验设计

- 初始化权重影响：10 个随机种子（每个 decile 1 个架构）
- 输入 minibatch 影响：10 个随机批次（128 samples）
- RNN 指标按层 vs 全网络

## 关联页面

- [[serianni2023-training-free-nas-rnn-transformers-analysis]] — 论文分析总览
- [[serianni2023-training-free-nas-rnn-transformers-results]] — 实验结果详情
- [[serianni2023-training-free-nas-rnn-transformers-critical]] — 批判性分析
- [[chen2021-tenas-method]] — TE-NAS 的 NTK + 线性区域方法
- [[entities/training-free-nas-transformers]] — 实体页

## Evidence By Source

### `sources/papers/serianni2023-training-free-nas-rnn-transformers.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/training_free_nas2023.pdf`

^[sources/papers/serianni2023-training-free-nas-rnn-transformers.md]
