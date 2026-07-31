---
id: papers--so2021-primer-method
title: 'So et al. (2021) — Primer: 搜索空间、SQ-TC 搜索算法与训练策略'
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/transformer
keywords:
- conceptual-initialization
- evolutionary-search
- halving-hurdles
- primitives-search-space
- sq-tc-search
sources:
- sources/papers/so2021-primer.md
created: '2026-06-14'
updated: '2026-07-31'
confidence: high
methods:
- regularized-evolution
- program-synthesis
- low-level-tf-primitives
- implicit-efficiency-objective
---

# Primer 搜索空间、SQ-TC 搜索算法与训练策略

> 父页面：[[so2021-primer-analysis]]
> 搜索空间设计灵感来源于 AutoML-Zero（Real et al. 2020），但目标不同：前者是"从零演化 ML 算法"，Primer 是"从 Transformer 出发寻找底层改进"

## 搜索空间设计

### 表示层：DNA → 子程序 → 指令

Primer 的搜索空间将每个 decoder block 表示为一个 **DNA**（进化搜索中的个体），包含：

- **子程序银行（Subprogram Bank）**：S0 为 MAIN() 入口，S1~Sn 为可调用子程序
- 子程序调用无环约束：Si 只能调用 Sj（j > i）
- 每条指令 = 一个操作 + argument set {Input1, Input2, Constant, Dim Size}

### TF 原语词汇表（Primitives Vocabulary）

| 类别 | 原语 | TF 函数 |
|------|------|---------|
| 算术 | ADD, DIFFERENCE, DIVIDE, MULTIPLY | tf.math.add/subtract/divide/multiply |
| 一元 | ABS_ROOT, SQUARE, EXP, LOG, ABS, RECIP, SIGN | tf.sqrt(abs), tf.square, tf.exp, tf.log(abs)... |
| 三角 | COS, SIN, TANH, SIGMOID | tf.cos, tf.sin, tf.tanh, tf.sigmoid |
| 比较/选择 | MAX, MIN | tf.math.maximum/minimum |
| 标量运算 | C_MUL, SCALE, SHIFT | multiply(x, C), x+Variable(), x*Variable() |
| 归约 | RED_MEAN, RED_SUM, RED_MIN, RED_MAX, RED_PROD | tf.reduce_mean/sum/min/max/prod |
| 矩阵 | MAT_MUL, T-MAT_MUL | tf.matmul, tf.matmul(transpose_b=True) |
| 卷积 | CONV 1X1, CONV 3X1/7X1/15X1/31X1, DCONV 3X1/7X1/15X1/31X1 | tf.layers.dense, tf.nn.conv1d, tf.nn.depthwise_conv2d |
| 辅助 | MASK (causal), CUM_PROD, CUM_SUM | band_part, cumprod, cumsum |

总共约 32 个原语，从构造 Transformer 所需最低层操作出发扩展。

### 关键设计决策

- **相对维度**：dimension size 使用相对值 {1,2,4,8,12,16,24,32,48,64}，便于模型 resize
- **值银行**：所有 constant 和 dimension 从共享 bank 引用——多指令共享值，修改一处同步改变
- **分支（Branching）**：每条指令可指定并行执行次数 {1,2,4,8,16} 并拼接，实现 multi-head
- **Causal Masking**：卷积等空间位移操作增加 causal shift + mask
- **维度不匹配自动解决**：伪随机强制对齐

## 搜索算法

### Regularized Evolution + Halving Hurdles

- 种群大小：100（未调参）
- Tournament size：10
- 每代选择一个 parent，mutation 一次生成 child
- **Halving Hurdles**：5 个训练分带，每带 50% 通过率：

| Hurdle | 训练量 | 通过率 | 累计通过率 |
|--------|--------|--------|-----------|
| 1 | ~812.9s | 50% | 50% |
| 2 | ~1625.8s | 50% | 25% |
| 3 | ~3251.6s | 50% | 12.5% |
| 4 | ~6503.3s | 50% | 6.25% |
| Full | 25200s (7h) | - | - |

平均评估时间：4064s（约 1.13h）——比全 7h 评估省 6.2×。

设计原则：每带期望计算量相等，只需设一个超参数（hurdle 数量），不需设阈值。

### 7h Proxy

Vanilla Transformer 7h 训练达到 24h 训练 ~90% 的 perplexity 改进。用 7h 作 proxy → 额外省 3.43×。总搜索加速：6.2 × 3.43 ≈ 21.4×。

### 隐式效率目标（Implicit Efficiency Objective）

- 搜索目标：固定 24h 训练预算，最小化 LM1B perplexity
- 对比：Evolved Transformer 固定步数 → 选出的模型 sample efficient 但 step time 慢
- Primer 的目标将 step time 和 sample efficiency 之间的 tradeoff 隐式纳入——例如 Squared ReLU 和 MDHA 都增加 step time 但大幅提升 sample efficiency

### Mutation 类型

| Mutation | 操作 |
|----------|------|
| Delete | 删除子程序中的一条指令 |
| Insert | 插入一条新指令 |
| Delete + Insert | 先删后插（Uniform Mutation by Addition and Deletion） |
| Mutate Field | 改变指令某个 field 的值 |
| Swap | 交换两条指令的位置（同时交换 input 引用以保持图结构） |
| Mutate Bank Value | 改变 shared bank 中的 constant（×10^X + Y, X,Y~N(0,1)）或 dimension |

Mutation 后检查等价性：若 child 计算图和 parent 完全等价，重复 mutation 直到产生实质变化。

### 概念初始化（Conceptual Initialization）

将原始 Transformer 按概念模块拆解为 9 个子程序：

| 子程序 | 内容 | 参数 |
|--------|------|------|
| S0 MAIN | 整体流程 | pre-norm → attention → post-norm → FFN |
| S1 Self-Attention | QK投影 + softmax + V加权 | d_model=512, heads=8 |
| S2 Feed Forward | 上下投影 + 激活 | d_ff=2048 |
| S3 Multi-head Proj | 单头 1×1 卷积投影 | dim=64 |
| S4 Softmax | exp + causal mask + normalize | - |
| S5 Layer Norm | 调用 S6+S7 | - |
| S6 Z-score Norm | (x-μ)/σ | - |
| S7 Scale-shift | γx+β | - |
| S8 Residual | x + f(x) | - |
| S9 ReLU | max(x, 0) | C=0 |

搜索从 10 个 Transformer 副本初始化种群。对比实验：随机初始化导致 78% 程序连 5 分钟都无法训练（数值不稳定）。

## 训练配置

### 搜索阶段
- 任务：LM1B 自回归语言建模
- Codebase：Tensor2Tensor (T2T)
- 参数：d_model=512, d_ff=2048, L=6, ~35M params
- 优化器：Adafactor, lr=0.01, 10K warmup + reciprocal sqrt decay
- 序列长度：64，batch：4096 tokens
- 硬件：TPUv2，训练 24h（proxy 7h）
- 总搜索量：~25K 个体，top 100 retrain 选最优

### 重训练/对比阶段
- 使用三个 codebase 的默认超参数，不做调参
- T2T：TRANSFORMER_TPU 参数
- T5：开源 T5 参数，相对注意力 + SentencePiece
- Lingvo：默认 Transformer 参数

## Evidence By Source

### `sources/papers/so2021-primer.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/primer2021_efficient_transformers.pdf`

^[sources/papers/so2021-primer.md]

## Related Indexes

- [[papers/index]]
