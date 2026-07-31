---
id: papers--zhao2021-memory-efficient-dnas-method
title: DARTSformer 方法机制：Multi-Split Reversible Network + BP-with-Reconstruction + DARTS
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/neural-architecture-search
- method/transformer
keywords:
- differentiable-nas
- gradient-checkpointing
- machine-translation
- reversible-layer
- transformer
sources:
- sources/papers/zhao2021-memory-efficient-dnas.md
created: '2026-06-14'
updated: '2026-07-31'
confidence: high
---

# DARTSformer 方法机制

> 父页面：[[zhao2021-memory-efficient-dnas-analysis]]

## 整体流程

```
阶段 1: 定义搜索空间
    候选操作集 O (13/14种) + multi-split encoder (n-split) + decoder ((n+1)-split)

阶段 2: 构建 Super Network (DARTSformer)
    Multi-split reversible network backbone，每 split 嵌入 mixed operation search node

阶段 3: Memory-Efficient DARTS 搜索 (Algorithm 2)
    用 BP-with-reconstruction (Algorithm 1) 更新 θ (训练集) 和 α (验证集)

阶段 4: 架构抽取 + 重训练
    argmax α 确定每个 search node 的操作 → 用普通 Transformer BP 重训练
```

## 核心组件 1: Multi-Split Reversible Network

### 动机

标准 Transformer 中 DARTS 的内存消耗来源于：每个 mixed operation search node 需要同时存储 |O| 个候选操作的中间输出（用于反向传播的梯度计算）。当 hidden size d 和候选操作数 |O| 增大时，内存迅速 OOM。

**解决方案**：使用可逆网络——每层的输入可以从输出重构，因此仅需存储最后一层输出，中间激活在 BP 时按需重建。

### 数学定义 (Eq. 3)

将输入 X 沿 embedding/channel 维度等分为 n 份 {X₁, X₂, ..., Xₙ}，每份 Xₖ ∈ ℝ^{l×d/n}（l 为序列长度，d 为 hidden size）。对每份应用可逆变换：

```
Y₁ = X₁ + G₁(X_{i>1}, θ₁)
Y₂ = X₂ + G₂(X_{i>2}, Y_{i<2}, θ₂)
...
Yₖ = Xₖ + Gₖ(X_{i>k}, Y_{i<k}, θₖ)
...
Yₙ = Xₙ + Gₙ(Y_{i<n}, θₙ)
```

**可逆性验证 (Eq. 4)**：从输出 Y 可逐分量重构输入 X：

```
Xₙ = Yₙ − Gₙ(Y_{i<n}, θₙ)
...
Xₖ = Yₖ − Gₖ(X_{i>k}, Y_{i<k}, θₖ)
...
X₁ = Y₁ − G₁(X_{i>1}, θ₁)
```

重构按 n → 1 的顺序进行。Gₖ 在搜索阶段是 mixed operation search node，搜索后是确定性操作。

### 设计细节

- **Split 沿着 embedding 维度**（而非序列长度维度），保持序列维度不变
- **Gₖ 的输入包含 (n−1) 个 tensors**：所有 X_{i>k}（来自第 k 个 split 之后的 X）和所有 Y_{i<k}（来自第 k 个 split 之前的 Y）
- **Gₖ 的输出必须与 Xₖ 同 shape**（R^{l×d/n}），以支持 element-wise addition
- **论文默认 n=2 (encoder), n=3 (decoder)**：搜索 s=2 个连续层，即在一个 2-layer encoder block 和 2-layer decoder block 中搜索

## 核心组件 2: Gₖ 的设计 — Pooling + Mixed Operation Search

### 结构 (Eq. 5, Fig. 3)

每个 Gₖ 分解为两个部分：

1. **Pooling 操作**：将 (n−1) 个 R^{l×d/n} 输入融合为单个 R^{l×d/n}
   ```
   Hₖ = Pooling(X_{i>k}, Y_{i<k})
   ```
   实验比较了 max pooling 和 average pooling（max 略优，Table 1）

2. **Mixed operation search node**：softmax 加权候选操作
   ```
   Gₖ = Σ_{o∈O} softmax(αₖ)ₒ · o(Hₖ)
   ```
   其中 αₖ 是第 k 个 split 的搜索参数（随机初始化）

### 候选操作集 O

| 操作类型 | 具体配置 | 数量 |
|---------|---------|------|
| Standard Conv (w×1) | w ∈ {3, 5, 7, 11} | 4 |
| Dynamic Conv (w×1) | w ∈ {3, 7, 11, 15} | 4 |
| Self Attention | 8 heads | 1 |
| Cross Attention | 8 heads, decoder only | 1 |
| GLU (Gated Linear Unit) | — | 1 |
| FFN | — | 1 |
| Zero | 输出零张量 | 1 |
| Identity | 输出输入 | 1 |

Encoder: 13 种候选 (无 Cross Attention)，Decoder: 14 种候选。

**操作内部嵌入残差连接 + LayerNorm**：每个候选操作 ˜o(X) = LayerNorm(X + o(X))（Zero 和 Identity 除外），使整个网络保持可逆性的同时保证训练稳定性。

### 搜索空间大小

设 encoder 为 m-split，decoder 为 n-split，搜索 s 个连续层：搜索空间大小 = |O|^{s(m+n)}。

默认配置：m=2, n=3, s=2, |O|≈13.5 → 搜索空间约 10⁹ (= 13.5^{10})。

## 核心组件 3: Backpropagation with Reconstruction (Algorithm 1)

### 关键思想

传统 BP：前向存储所有中间激活 → 反向逐层使用。

BP-with-reconstruction：前向仅存储最后一层输出 → 反向时从顶层开始逐层重构输入 → 计算梯度。

### Algorithm 1 详解

```
输入：f(X)=[Y₁,...,Yₙ], df(X)=[dY₁,...,dYₙ], G₁,...,Gₙ
输出：X=[X₁,...,Xₙ], dX=[dX₁,...,dXₙ], dθ₁,...,dθₙ

1. 初始化空集合 X={}, dX={}
2. for k = n down to 1:           // 按 n→1 顺序重构
3.     C = Yₖ                      // 取出当前 split 输出
4.     gradₖ = dYₖ + (C的累计梯度) // 累积总导数
5.     gₖ = Gₖ(X, Y, θₖ)          // 重算 Gₖ
6.     gₖ.backward(gradₖ)          // 计算 dθₖ 和输入梯度
7.     Xₖ = C − gₖ                 // 重构 Xₖ
8.     X = X ∪ {Xₖ}
9. for k = 2 to n:                 // 收集 dX
10.    dXₖ = Xₖ.grad + gradₖ
11.    dX = dX ∪ {dXₖ}
12. dX₁ = grad₁
```

### 内存与计算权衡

| 指标 | 标准 BP | BP-with-reconstruction |
|------|---------|----------------------|
| 中间激活存储 | O(N) 层所有操作输出 | O(1) 仅顶层输出 |
| 前向计算量 | N 次 add-multiply | N 次 |
| 反向计算量 | 2N 次 | 2N 次 |
| 重构计算量 | 0 | N 次 |
| 总计算量 | ~3N | ~4N (+33%) |
| **仅搜索阶段使用** | — | ✓ |

**重要**：重构计算仅存在于搜索阶段。搜索收敛后，用 argmax α 确定架构，重训练使用标准 Transformer BP，无额外开销。

## 核心组件 4: DARTS 双层优化 (Algorithm 2)

### 搜索流程

```
Algorithm 2: DARTSformer 框架
1. 构建 multi-split reversible super network N_{super}(O, α, θ)
2. while α 未收敛:
3.     用 Algorithm 1 更新 θ（在 L_train 上）
4.     用 Algorithm 1 更新 α（在 L_val 上）
5. N_final = argmax_α N_super
```

### 数据划分

- WMT'14 En-De 4.5M sentence pairs → 2.5M (train θ) / 2.0M (val α)
- 两个数据集都用 cross-entropy loss + label smoothing 0.1

### 优化器配置

| 参数 | θ (网络权重) | α (搜索参数) |
|------|-------------|-------------|
| Optimizer | Adam (β₁=0.9, β₂=0.98) | Adam (β₁=0.9, β₂=0.98) |
| LR schedule | Transformer warmup (warmup=10000) | Fixed |
| Max LR | 5×10⁻⁴ | 3×10⁻⁴ |
| Weight decay | — | 1×10⁻³ |
| Dropout | 0.1 | — |

### 训练策略

- **Factorized embedding**：原始 E ∈ R^{|V|×d} 分解为 R^{|V|×e} × R^{e×d}，e≪d，节省内存
- **搜索配置**：e=256, d=960, 每 GPU batch 5000 tokens, 8×V100
- **搜索步数**：60,000 updates (30,000 θ + 30,000 α)
- **Checkpoint**：每 10,000 updates 保存一次

## Encoder/Decoder 架构约束

### Encoder (n-split)

每个 split 的 Gₖ 均为 Eq. 5 的混合操作 search node。

### Decoder ((n+1)-split)

- G₁...Gₙ：同 Eq. 5 的混合操作 search node
- **Gₙ₊₁ 固定为 Cross Attention**（不参与搜索）

**约束理由**：实验发现该约束使搜索到的架构性能更好。Cross Attention 作为 encoder-decoder 信息桥梁不应被搜索「淘汰」。

## 搜索到的最佳架构 (Fig. 4)

配置：2-split encoder + 3-split decoder, s=2, max pooling

**Encoder (2-split, M×block)**：
- Split 1: {X₁, X₂} → FFN + Self Attn (pooling) → Y₁
- Split 2: {Y₁} → FFN + Self Attn (pooling) → Y₂

**Decoder (3-split, N×block)**：
- Split 1: {X₂, X₃} → FFN + Self Attn → Y₁
- Split 2: {X₃, Y₁} → Cross Attn → Y₂
- Split 3 (fixed): {Y₁, Y₂} → Cross Attn → Y₃

搜索发现：FFN 和 Self Attention 在 encoder 中配对出现，Cross Attention 主导 decoder 的后两个 split。

## 关联页面

- [[zhao2021-memory-efficient-dnas-analysis]] — 全维度总览
- [[zhao2021-memory-efficient-dnas-results]] — 实验数据
- [[zhao2021-memory-efficient-dnas-critical]] — 贡献·局限·可迁移·机会
- [[memory-efficient-dnas]] — 实体页
- [[wang2020-hat-method]] — HAT 进化搜索 + weight-sharing 的方法论对比

## Evidence By Source

### `sources/papers/zhao2021-memory-efficient-dnas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/memory_efficient_dnas2021.pdf`

^[sources/papers/zhao2021-memory-efficient-dnas.md]
