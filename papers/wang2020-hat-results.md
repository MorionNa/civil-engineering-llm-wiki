---
title: "HAT 实验结果：四任务×三硬件 BLEU-Latency 全面对比"
created: 2026-06-13
updated: 2026-06-13
type: paper-analysis
tags: [hardware-aware-nas, machine-translation, wmt14, wmt19, iwslt14, edge-inference, evolutionary-search]
sources: [raw/papers/wang2020_hat.md]
confidence: high
---

# HAT 实验结果

> 父页面：[[wang2020-hat-analysis]]

## 实验设置总览

| 维度 | 详情 |
|------|------|
| **任务** | WMT'14 En-De (4.5M), WMT'14 En-Fr (36.3M), WMT'19 En-De (43M), IWSLT'14 De-En (160K) |
| **硬件** | Raspberry Pi 4 (ARM Cortex-A72), Intel Xeon E5-2640, Nvidia TITAN Xp |
| **延迟测试** | 翻译固定长度句子（WMT: 30 tokens, IWSLT: 23 tokens），300 次取中间 80% 平均 |
| **Baselines** | Transformer-Base/Big, Evolved Transformer, Levenshtein Transformer, Lite Transformer |

---

## 1. 核心性能对比 (WMT'14 En-De, Raspberry Pi ARM CPU)

| 模型 | 延迟 (s) | #Params | BLEU | 加速比 | 压缩比 |
|------|----------|---------|------|--------|--------|
| Transformer-Big | 20.5 | 176M | 28.4 | 1× | 1× |
| Transformer-Base | 3.3 | 32M | 25.8 | — | — |
| Evolved Transformer | 7.6 | 47M | 28.2 | 2.7× | 3.74× |
| **HAT** | **6.0** | **44M** | **28.2** | **3.4×** | **4.0×** |
| **HAT (更大)** | **6.9** | **48M** | **28.4** | **3.0×** | **3.7×** |

HAT 以 Transformer-Big 同 BLEU 实现 **3× 加速 + 3.7× 压缩**。比 Evolved Transformer 快 2.7×，参数少 3.6×，搜索成本仅 1/12,041。

---

## 2. 多硬件 Latency-BLEU 曲线 (WMT'14 En-De & En-Fr)

### 关键数值（图 7, Table 8 Appendix）

| 任务 | 硬件 | HAT vs Transformer-Big 加速 |
|------|------|---------------------------|
| WMT'14 En-De | Raspberry Pi ARM | **3.0×** |
| WMT'14 En-De | Intel CPU | **2.0×** |
| WMT'14 En-De | Nvidia GPU | **1.5×** |
| WMT'14 En-Fr | Raspberry Pi ARM | **3.0×** |
| WMT'14 En-Fr | Intel CPU | **2.2×** |
| WMT'14 En-Fr | Nvidia GPU | **1.8×** |

**GPU 特殊现象**：dimension scaling（蓝色虚线）在 GPU 上几乎垂直——增大/缩小 hidden dim 对 GPU 延迟影响极小。因为 GPU 的大规模并行可以轻松处理矩阵乘法，瓶颈在序列长度和层数。HAT 仍能找到低延迟模型。

### WMT'19 En-De / IWSLT'14 De-En (GPU)

| 任务 | 加速比 |
|------|--------|
| WMT'19 En-De (Nvidia GPU) | **1.8×** |
| IWSLT'14 De-En (Nvidia GPU) | **1.8×** |

---

## 3. 与其他高效模型对比 (WMT'14 En-De, Raspberry Pi ARM CPU)

| 模型 | 延迟 (s) | BLEU |
|------|----------|------|
| Transformer (Vaswani et al.) | 4.3 | 25.85 |
| Levenshtein Transformer | 6.5 | 25.20 |
| Evolved Transformer | 3.7 | 25.40 |
| Lite Transformer | 3.4 | 25.79 |
| **HAT** | **3.4** | **25.92** |

HAT 以最低延迟获得最高 BLEU：比 Levenshtein 快 **1.9×** 且 BLEU 高 0.7，比 Lite Transformer 同延迟下 BLEU 高 0.13。

---

## 4. 搜索成本对比

| 方法 | GPU Hours | CO2 排放 (lbs) | 云成本 (USD) |
|------|-----------|----------------|--------------|
| Evolved Transformer | 2,192,000 | 626,000 | $1.6M–5.5M |
| Transformer-Big | 184 | 52 | $136–456 |
| **HAT** | **184–224** | **52–64** | **$136–555** |
| **HAT vs Evolved** | **12,041× 低** | **12,041× 低** | **12,041× 低** |

HAT 的总 GPU 小时甚至低于训练一个 Transformer-Big（因为 HAT 模型本身更紧凑）。

---

## 5. SuperTransformer 代理有效性

### 继承权重 vs 从头训练 (Table 5)

| 模型 | WMT'14 En-De 继承 BLEU | 从头训练 BLEU | 排名一致 |
|------|------------------------|--------------|---------|
| 1 (最差) | 24.9 | 25.8 | ✓ |
| 2 | 25.8 | 27.6 | ✓ |
| 3 | 26.3 | 28.1 | ✓ |
| 4 | 26.7 | 28.2 | ✓ |
| 5 (最好) | 26.9 | 28.4 | ✓ |

### 继承后微调 vs 从头训练 (Table 6)

| 任务 | 从头训练 40K | 继承微调 10K | 节省 |
|------|-------------|-------------|------|
| WMT'14 En-Fr | 41.5 | **41.7** | 4× |
| WMT'14 En-De | 28.0 | 28.0 | 4× |

继承微调仅需 1/4 训练步数，BLEU 持平或更好。

---

## 6. 设计洞察

### 6.1 硬件差异化架构

| 硬件 | 偏好 | 原因 |
|------|------|------|
| **Nvidia GPU** | **浅而宽** (few layers, large dims) | 并行能力强，embed/hidden dim 几乎不影响延迟 |
| **Raspberry Pi ARM** | **深而瘦** (many layers, small dims) | CPU 顺序执行，embed dim 增大 = 内存带宽瓶颈 |
| **Intel Xeon CPU** | 中等 | 介于 GPU 和 ARM 之间 |

**指导手动设计**：GPU 上 → 减层数加维度降延迟保性能；ARM 上 → 深层窄维策略。

### 6.2 Arbitrary Encoder-Decoder Attention

搜索出的 HAT 模型中：**~10% 的 decoder 层关注 3 个 encoder 层，~40% 关注 2 个**。仅 50% 使用传统单层连接。证明了多 encoder 层连接的普遍价值。

### 6.3 更大 ≠ 更好 (Table 4)

| 模型 | 延迟 | #Params | BLEU |
|------|------|---------|------|
| 最大 SubTransformer (En-De) | 10.1s | 71M | 28.1 |
| **搜索出的 HAT (En-De)** | **6.9s** | **48M** | **28.4** |

搜索出的 HAT 比设计空间中最大的模型更小、更快、BLEU 更高——说明盲目增大模型不如智能搜索。

---

## 7. 量化与蒸馏正交兼容性

| 方法 | BLEU | 模型大小 | 压缩比 |
|------|------|---------|--------|
| Transformer Float32 | 41.2 | 705MB | — |
| HAT Float32 | 41.8 | 227MB | 3× |
| HAT 8-bit (K-means) | **41.9** | 57MB | 12× |
| HAT 4-bit (K-means) | 41.1 | **28MB** | **25×** |

- 8-bit 量化 BLEU 甚至比全精度高 0.1（鲁棒性信号）
- 4-bit 量化：25× 压缩，仅 0.1 BLEU 损失
- 知识蒸馏：teacher BLEU 28.5 + 49M params → student 30M params → BLEU 25.8→26.1 (+0.3)

---

## 关联页面

- [[wang2020-hat-analysis]] — 全维度总览
- [[wang2020-hat-method]] — 方法展开
- [[wang2020-hat-critical]] — 贡献·局限·可迁移·机会
- [[jiang2024-mixtral-of-experts-results]] — Mixtral 的效率对比视角
