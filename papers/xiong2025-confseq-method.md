---
title: "ConfSeq 方法机制：内坐标序列化与 Transformer 统一架构"
created: 2026-06-24
updated: 2026-06-24
type: paper-analysis
tags: [chemical-language-model, molecular-conformation, sequence-modeling, internal-coordinates]
sources: [raw/papers/10_1101_2025.05.07.652440.pdf]
confidence: high
---

# ConfSeq 方法机制

> 来源：`[[xiong2025-confseq-analysis]]` | 本节展开第 5 维度

## 整体框架

```
分子 3D 结构 (SDF/XYZ)
       ↓ RDKit + Indigo 提取内坐标
ConfSeq token 序列 = SMILES tokens + 内坐标 tokens
       ↓ 标准 Transformer (encoder/decoder-only)
3D 分子任务 ← 序列建模 (seq2seq / autoregressive / siamese)
```

ConfSeq 的核心理念：**用好的 token 化代替好的模型架构**。不需要复杂的 GNN 或扩散模型——只要将 3D 信息有效地序列化，标准 Transformer 就能达到 SOTA。

## 三种内坐标 Token

### 1. 二面角 (Dihedral Angle) — 最关键

```
tokens: "<-173>", "<0>", "<113>"
位置: 替换 explicit-bond SMILES 中对应键的 "-" 或 "=" token
```

**标准化算法**（解决多路径歧义）：
- 中心键方向：原子索引小的在前
- 邻位原子选择：优先 degree > 1，其次最小索引
- 非芳香环的二面角也被纳入（以往工作仅考虑可旋转键）

### 2. 键角 (Bond Angle)

```
tokens: "<30>|", "<109>|"
位置: 插入中心原子 token 之后
```

**选择标准**：中心原子满足三个条件——不在任何环中 / 连接两个重原子 / 非双键氧。这些角度灵活性大，对整体构象影响显著。

**区分机制**：管道符 `|` 将其与二面角 token 区分。

### 3. 伪手性 (Pseudo-Chirality)

```
tokens: "{", "}"
位置: 对应二面角 token 前后
```

**动机**：非手性中心（如胺基氮）的两个构象可快速互变但需在 3D 建模中区分。`{` = 逆时针，`}` = 顺时针。

## 四大任务的模型架构

| 任务 | 架构 | 维度 | 关键设计 |
|------|------|------|----------|
| 构象预测 | Encoder-Decoder Transformer | 6+6 层, d=256 | SMILES→ConfSeq; 100× 数据增强 |
| 无条件生成 | Decoder-only Transformer | 6 层, d=768 | 自回归生成; 5× 增强 |
| 形状条件生成 | RISurConv + Decoder | 6 层, d=768 | 表面描述符→交叉注意力→生成 |
| 表征学习 | Encoder-only (Siamese) | 6 层, d=256 | 欧氏距离→相似度; 95.7M 分子对训练 |

## 推理特性

### 自回归评分
每步生成的概率 log 值平均 = 构象置信度评分。实验表明与 DFT 计算能量强负相关（ρ = -0.58，部分分子 > -0.9）。

### 温度控制多样性
调整采样温度 T：
- T ↓ → Precision ↑ / Recall ↓（更保守、更准确）
- T ↑ → Recall ↑ / Precision ↓（更多样化）

这提供了可控的 Precision-Recall 权衡，扩散模型不具备此能力。

## 与现有方法的本质区别

| | ConfSeq | 扩散模型 | 直接坐标编码 |
|------|---------|---------|------------|
| SE(3) 不变性 | 天然保证 | 需等变网络 | ❌ 破坏 |
| 推理速度 | 快（单步自回归） | 慢（多步去噪） | 中等 |
| 评分能力 | 内置 | 需额外模块 | 无 |
| 架构兼容性 | 标准 Transformer | 专用 GNN/等变网络 | 标准模型但效果差 |
| 数据增强 | 类似 SMILES 枚举 | 无等效方法 | 有限 |
