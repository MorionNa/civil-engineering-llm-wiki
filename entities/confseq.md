---
title: "ConfSeq — 分子构象描述语言"
created: 2026-06-24
updated: 2026-06-24
type: entity
tags: [chemical-language-model, molecular-conformation, sequence-modeling, internal-coordinates]
sources: [raw/papers/10_1101_2025.05.07.652440.pdf]
confidence: high
---

# ConfSeq

**ConfSeq** (Conformation Sequence) 是一种分子构象描述语言，由上海药物所郑明月课题组于 2025 年提出（Jiacheng Xiong 等，正式发表于 *Nature Machine Intelligence* 2026）。

## 核心思想

将 3D 分子构象编码为离散 token 序列，使标准 Transformer 能像处理自然语言一样处理 3D 分子结构。核心理念：**好的 token 化胜于好的模型架构**。

## 三种编码要素

| 要素 | Token 格式 | 含义 |
|------|-----------|------|
| 二面角 | `<113>` | 四原子二面角，替换 SMILES 中键 token |
| 键角 | `<30>\|` | 三原子键角，插入中心原子后 |
| 伪手性 | `{` / `}` | 逆/顺时针，区分非手性中心构象 |

## 关键特性

- **SE(3) 不变性**：内坐标天然保证平移/旋转不变性
- **人类可读**：类似 SMILES 的符号化表示
- **数据增强友好**：类似 SMILES 枚举的序列级增强
- **自评分**：自回归生成的 per-token 概率天然构成置信度评分

## 支持任务

1. 3D 构象预测（SMILES → ConfSeq）
2. 无条件 3D 分子生成
3. 形状条件 3D 分子生成
4. 3D 分子表征学习 + 虚拟筛选

## 关键结果

- 构象预测 COV-P: 47.9→58.4%（+10.5 pp over Tor. Diff.）
- 生成采样速度：500—2200× 于扩散模型
- 虚拟筛选：单 CPU 1 分钟搜索 9800 万 PubChem

## 代码

Zenodo: `10.5281/zenodo.19706011` | 需要 RDKit + Indigo

## 相关页面

- `[[xiong2025-confseq-analysis]]` — 论文完整分析
- `[[xiong2025-confseq-method]]` — 方法机制展开
- `[[xiong2025-confseq-results]]` — 实验结果
- `[[xiong2025-confseq-critical]]` — 贡献+Negative+机会
