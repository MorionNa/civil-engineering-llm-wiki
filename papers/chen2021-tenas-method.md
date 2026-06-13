---
title: "TE-NAS 方法机制：NTK 条件数 + 线性区域 + Pruning 搜索"
created: 2026-06-12
updated: 2026-06-12
type: paper-analysis
tags: [training-free-nas, ntk, neural-tangent-kernel, linear-regions, pruning-based-nas]
sources: [raw/papers/TE-NAS_chen2021_ICLR.pdf]
confidence: high
---

# TE-NAS 方法机制

> 父页面：[[chen2021-tenas-analysis]]

## 核心架构

```
搜索空间（cell-based DAG）
    │
    ├─→ 指标 1: NTK 条件数 κN  ─→ 衡量可训练性
    │        在 Kaiming 初始化时算一次 NTK 的特征值谱
    │        取 λ_max / λ_min → 越小越好
    │
    ├─→ 指标 2: 线性区域数 ˆRN  ─→ 衡量表达能力
    │        随机采样网络参数，计算 ReLU 激活模式数
    │        多次采样取平均 → 越多越好
    │
    └─→ Pruning-by-Importance 搜索
             从全连接 supernet 出发
             每次剪掉"最不重要"的边（按 κN + ˆRN 排名）
             复杂度: |O|×E（而非 |O|^E）
```

## 指标 1: NTK 条件数 κN

### 原理

NTK（Neural Tangent Kernel）刻画了网络在梯度下降下的训练动态。对于输入 x, x'：

```
Θ(x, x') = ∇_θ f(x) · ∇_θ f(x')^T
```

- NTK 的条件数 κN = λ_max / λ_min 衡量参数空间中 loss landscape 的局部曲率
- **κN 越小 → loss landscape 越平坦 → 梯度下降收敛越快越稳定**
- 计算：对 mini-batch 数据，构建 NTK 矩阵（不需要标签！），SVD 分解取最大/最小奇异值之比

### 偏好

κN 偏好 skip-connection 多的架构——残差连接改善梯度流，天然降低条件数。

## 指标 2: 线性区域数 ˆRN

### 原理

ReLU 网络将输入空间划分成多个线性区域（每个区域内的映射是线性的）。

- Hanin & Rolnick (2019): 线性区域数可作为网络表达能力的度量
- 计算方式：对随机输入，统计每个神经元在多少次前传中处于激活/非激活状态
- **多次随机初始化取平均**（公式 5）：ˆRN ≃ E_θ[R_{N,θ}]

### 偏好

ˆRN 偏好 conv 多的架构——卷积增加非线性变换，产生更多线性区域。

## 两个指标的解耦

```
         κN (越小越好)          ˆRN (越大越好)
         ↓                      ↓
    skip-connect               conv1×1
    avg pool                   conv3×3
         ↓                      ↓
      可训练性                  表达能力
```

两者天然存在 tension：skip-connect 帮助训练但减少非线性；conv 增加表达但恶化梯度流。**TE-NAS 的贡献之一就是首次量化了这种 tension。**

## Pruning-by-Importance 搜索

### 动机

采样式搜索（RL/evolution）需要评估 γ · |O|^E 个架构。当搜索空间大时（DARTS: |O|=8, E=14 → 8^14 可能性），采样成本不可接受。

### 算法

1. **初始化**：supernet 中每条边包含所有 |O| 个候选算子
2. **评分**：对每条边的每个算子，计算删除它后 κN 和 ˆRN 的变化
3. **剪枝**：删除"最不重要"的算子（对 κN + ˆRN 排名贡献最小的）
4. **迭代**：重复直到每条边只剩一个算子

复杂度从 |O|^E 降到 |O| × E（每轮评估 |O| × E 次，共剪 |E|×(|O|-1) 次 → O(|O|×E)）。

### 优势

- 不需要训练任何子网
- 天然解耦：每条边的算子选择独立决定
- 相比随机采样，pruning 更有方向性

## 两个指标如何组合

**不用原始数值，用相对排名求和**：

```
Score(arch_i) = Rank_κN(arch_i) + Rank_ˆRN(arch_i)
选 Score 最小的架构
```

原因：κN 的量级（10^3-10^6）和 ˆRN（10^2-10^4）差异大，直接数值加权会淹没其中一个。排名归一化消除了量级差异问题。

等权求和是最简方案，ablation 证明等权优于加权。

## 关联页面

- [[chen2021-tenas-analysis]] — 全维度总览
- [[chen2021-tenas-results]] — 实验结果
- [[chen2021-tenas-critical]] — 贡献·局限·可迁移·机会
