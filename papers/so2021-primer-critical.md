---
title: "So et al. (2021) — Primer 贡献·局限·可迁移·研究机会"
created: 2026-06-14
updated: 2026-06-14
type: paper-analysis
tags: [neural-architecture-search, transformer, efficient-inference, evolutionary-search, negative-knowledge]
sources: [raw/papers/primer2021_efficient_transformers.pdf]
failure_modes: [redundant-search-cost, encoder-decoder-gap, extraneous-mutations, open-ended-space-degeneracy]
confidence: high
---

# Primer 贡献·局限·可迁移·研究机会

> 父页面：[[so2021-primer-analysis]]

## 贡献 (Contribution)

### 1. 底层原语级别的 Transformer 进化搜索

首次在 TF 计算图 primitives 层面搜索 Transformer 变体。区别于 Evolved Transformer 的高层模块搜索空间，Primer 的开放空间允许修改模块内部（如 ReLU → Squared ReLU）甚至模块间顺序（如 pre-norm vs post-norm 的选择）。这种"开放空间 + 概念初始化"的组合策略，是在极度开放空间中做大规模模型搜索的关键方法论创新。

### 2. Squared ReLU — 一种无参新激活函数用于 Transformer

发现 y = (max(0, x))² 作为 FFN 激活函数，在自回归 LM 中稳定优于 ReLU/GELU/Swish/ReGLU/SwiGLU，且**不增加额外参数**（对比 GLU 家族需要双份权重）。其有效性可能根源于：
- 更高阶多项式 → 更强的非线性表达能力
- 与 ReGLU (U=V 特例) 数学等价性——但更简单
- x→∞ 的二次渐近行为带来截然不同的 training dynamics

### 3. MDHA — Multi-DConv-Head Attention

在每个 attention head 的 Q/K/V 1×1 投影后加入 3×1 spatial depthwise convolution。这个创新点颠覆了常规 separable convolution（depthwise → pointwise）的顺序，证明了 **pointwise → depthwise** 在 Transformer attention 中的有效性。与 Convolutional Attention (CvT) 的区别在于：per-head 独立 D-Conv + 不用 separable conv。

### 4. 隐式效率目标框架

不显式优化 training speed，而是固定训练预算用最终质量代理。这个设计哲学更符合实际需求——用户关心的是"同等算力下能达到多好"，而非"每一步花多长时间"。

### 5. 工程验证的广度

三个 codebase (T2T, T5, Lingvo) × 四种硬件 (TPUv2/v3/v4, V100) × 三个数量级参数 (20M~1.9B) × 三种模型家族 (dense, MoE, Synthesizer) × 多种数据集——在当时的 efficiency Transformer 研究中最全面的验证。

---

## 核心知识点 (Core Knowledge)

1. **Squared ReLU 替代性**：Decoder LM FFN 中，Squared ReLU 在 quality 和 simplicity 上均优——可直接替换，无额外参数
2. **MDHA 模式**：Pointwise → Spatial D-Conv on attention heads——简单的局部信息增强，大概率不破坏 attention 的全局建模能力
3. **开放空间搜索策略**：Conceptual initialization + Regularized Evolution + Halving Hurdles 的组合
4. **幂律节省**：更优架构的质量-计算关系服从 l = a(1-1/b)^k·s^(-k)，节省比例 b 恒定
5. **Decoder vs Encoder gap**：Decoder LM 的好改进不一定适用于 encoder MLM——架构选择高度任务依赖
6. **搜索 ROI**：Primer 搜索的 FLOPs 投资在单次大规模训练中即回收 9.24×

---

## Negative Knowledge (负面知识)

### 适用范围 / 前提假设

| 条件 | 说明 |
|------|------|
| **任务类型** | 仅验证 decoder-only 自回归 LM。Encoder-decoder MLM 上不如 Transformer++ |
| **模型规模上限** | 最大验证 1.9B。10B+ 未验证 |
| **搜索条件** | 35M/LM1B/24h 下的改进，不一定在更大 setting 下保持最优 |
| **激活函数** | Squared ReLU 仅在 FFN 中有效。注意力 softmax 后的 tanh 改动不是核心 |
| **数据** | LM1B/C4/PG19 — 标准英文文本。代码/多语言/噪声数据未测试 |

### 失效场景

1. **Encoder-only 或 encoder-decoder 架构**：Squared ReLU + MDHA 在 T5 MLM 上不如 SwiGLU + RMSNorm
2. **序列长度 >> 训练窗口 (512/1024)**：MDHA 的 3×1 D-Conv 是固定局部窗口
3. **需要严格 deterministic 的推理**：MDHA 引入的空间混合可能对某些任务有害

### 不该照搬的做法

1. ❌ **不要在 encoder-decoder 模型上直接替换激活函数为 Squared ReLU**——实验结果表明不如 Transformer++ 的 SwiGLU
2. ❌ **不要忽略 search artifact**：Primer 包含 ×(-1.12) 等无意义的 modification——它们是进化搜索的"垃圾基因"，不是推广时应包含的
3. ❌ **不要假设加速比恒定**——4.2× 是在特定 T5 配置下的结果，实际加速比因硬件/数据/规模而异
4. ❌ **不要用 random init 在这个搜索空间做搜索**——78% 退化率

### 未解决的问题

1. Squared ReLU 比 SwiGLU 好的深层理论原因
2. Post-softmax spatial gating (per-channel scalars) 无法处理变长序列——有没有替代方案？
3. MDHA 的"pointwise→depthwise"顺序为何优于常规 reversed separable conv？
4. 搜索的 artifact mutations (×(-1.12) 等) 是纯噪声还是隐藏了未知机制？

---

## 可迁移知识 (Transferable Knowledge)

| 知识 | 迁移场景 | 迁移难度 |
|------|----------|---------|
| Squared ReLU | 任何 decoder-only LM FFN | ★☆☆ 一行代码 |
| MDHA | 任何 attention 架构 | ★★☆ 需实现 per-head D-Conv |
| 概念初始化 | 任何开放空间架构搜索 | ★★★ 需设计概念模块拆分方案 |
| 隐式效率目标 | 任何计算受限的 NAS | ★★☆ 需确定预算和 proxy |
| Halving Hurdles | 任何计算密集型进化搜索 | ★☆☆ 即插即用 |
| 幂律节省分析 | 任何架构对比实验 | ★☆☆ 双对数线性拟合 |

---

## 研究机会 (Research Opportunities)

### 直接延伸

1. **Primer for encoder-decoder MLM**：以 MLM 为搜索目标重跑，可能找到 encoder 专属的改进
2. **10B+ 规模验证**：Squared ReLU + MDHA 在 GPT-4 级别的 scaling 下是否仍然有效？
3. **长序列 MDHA**：用 dilated D-Conv 或 multi-scale D-Conv 增强长程能力
4. **跨模态**：ViT + Squared ReLU? Speech Transformer + MDHA?

### 方法论延伸

5. **训练-free Primer 搜索**：用 NTK/线性区域等指标减少搜索 cost（如 [[chen2021-tenas-analysis]] 的范式）
6. **AutoML 级别的原语发现**：不是手工设计 primitives vocabulary，而是自动发现有效原语
7. **多任务联合搜索**：同时优化 decoder LM + encoder MLM 目标，寻找通用改进

### 理论延伸

8. **Squared ReLU 的 training dynamics 分析**：为什么高阶多项式在 Transformer FFN 中有效？
9. **Local-Global 信息混合理论**：MDHA 为什么在 attention 内部做局部混合比在外部（如 Conformer）更好？

---

## 可复现性评分表

| 维度 | 评分 | 说明 |
|------|------|------|
| 代码开源 | ⭐⭐⭐⭐⭐ | T2T + T5 对比代码完全开源 |
| 架构完整描述 | ⭐⭐⭐⭐⭐ | 附录给出完整 DNA 指令列表（Figure 25） |
| 超参数 | ⭐⭐⭐⭐⭐ | 附录 A.8 全训练细节 |
| 数据集可获取 | ⭐⭐⭐⭐☆ | C4/LM1B 公开；GPT-3 式 pretraining 闭源 |
| 硬件可负担 | ⭐⭐☆☆☆ | 需 TPU——但 Primer-EZ 可在 GPU 验证 |
| 搜索可复现 | ⭐⭐☆☆☆ | 1145.8 TPUv2-day 搜索成本极高 |
| 论文自洽性 | ⭐⭐⭐⭐⭐ | 结果可信，消融充分，附录详实 |
| **总体** | ⭐⭐⭐⭐☆ | **高** — Primer-EZ 改动简单可在 GPU 复现，但完整搜索复现成本极高 |

### 复现 Tips
- 推荐从 **Primer-EZ** 开始——只需改两处代码
- T5 代码库已有 Primer 对比实验脚本
- GPU 复现建议用 110M/525K steps 设置（图 9），成本可控
