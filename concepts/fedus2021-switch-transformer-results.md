---
title: "Fedus et al. (2021) — 结果证据展开"
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: []
sources: [raw/papers/fedus2021_switch_transformer.md]
results: [pre-training-speedup-7x, downstream-fine-tuning-sota, multilingual-101-languages, distillation-99pct-compression, trillion-parameter-scaling, perplexity, t5-baseline]
datasets: [c4, mc4, glue, superglue, squad, cnndm, bbc-xsum, winogrande, trivia-qa, natural-questions, web-questions, arc, anli]
confidence: high
---

# Fedus et al. (2021) — 结果证据展开

> 返回概述 → [[fedus2021-switch-transformer-analysis]]

---

## Experiment 1: Switch vs MoE Head-to-Head

### 设置：所有模型在 C4 上预训练 100k steps，TPUv3 32 cores

| Model | Capacity Factor | Neg. Log Perp. (↑) | Time to -1.50 (↓ hrs) | Speed (ex/s) |
|-------|----------------|---------------------|------------------------|--------------|
| T5-Base | — | -1.731 | Not achieved | 1600 |
| T5-Large | — | -1.550 | 131.1 | 470 |
| MoE-Base | 2.0 | -1.547 | 68.7 | 840 |
| **Switch-Base** | 2.0 | **-1.554** | **72.8** | **860** |
| MoE-Base | 1.25 | -1.559 | 80.7 | 790 |
| **Switch-Base** | 1.25 | **-1.553** | **65.0** | **910** |
| MoE-Base | 1.0 | -1.572 | 80.1 | 860 |
| **Switch-Base** | 1.0 | **-1.561** | **62.8** | **1000** |
| Switch-Base+ | 1.0 | **-1.534** | 67.6 | 780 |

**关键结论：** (1) Switch 在所有 capacity factor 下速度均优于 MoE；(2) Switch 在较低 capacity factor (1.0, 1.25) 下表现更好——这对大模型的内存受限场景至关重要；(3) Switch-Base+（增加 hidden size 直到与 MoE 同速）进一步超越所有模型。

---

## Experiment 2: 预训练缩放 (Scaling Properties)

### 2a. Step-basis 缩放（固定步数）

随着 expert 数量从 2 增加到 256，在相同 FLOPs/token 下：

- **模型参数量从 223M → 14.7B**，test loss 持续单调下降
- Switch-Base 64e 在 **step 60k 达到 T5-Base step 450k 的质量** → **7.5× step speedup**
- 更大稀疏模型样本效率更高（一致性符合 Kaplan et al. 缩放律）

### 2b. Time-basis 缩放（固定训练时间/计算预算）

| 比较 | Speedup |
|------|---------|
| Switch-Base 64e vs T5-Base | **7×** |
| Switch-Base 64e vs T5-Large（3.5× FLOPs/token） | **2.5×** |

- 即使考虑通信开销，wall-clock speedup 依然显著
- **回答核心问题：固定预算下应训练稀疏模型而非密集模型**

### 2c. 万亿参数模型

| Model | Parameters | Neg. Log Perp. @250k | Neg. Log Perp. @500k |
|-------|-----------|----------------------|----------------------|
| T5-XXL | 11B | -1.147 | -1.095 |
| Switch-XXL | 395B | **-1.086** | **-1.008** |
| Switch-C | 1571B | **-1.096** | **-1.043** |

- 两者 @250k 均超越 T5-XXL 的质量达 **0.061**（T5-XXL 需额外 250k steps 才能提升 0.052）
- Switch-C 比 T5-XXL **快 4×**，且差距随训练持续扩大
- ⚠️ Switch-XXL 有时不稳定，未完成完整 1M steps 训练

---

## Experiment 3: 下游微调 (Fine-tuning)

### Fine-tuning Setup
- 预训练：C4，220 tokens/batch，550k steps（576B total tokens）
- Fine-tuning：1M batch size，16k steps，每 200 steps 评估峰值

### 结果

| Model | GLUE | SQuAD | SuperGLUE | Winogrande |
|-------|------|-------|-----------|------------|
| T5-Base | 84.3 | 85.5 | 75.1 | 66.6 |
| **Switch-Base** | **86.7** | **87.2** | **79.5** | **73.3** |
| Δ vs T5-Base | **+2.4** | **+1.7** | **+4.4** | **+6.7** |
| T5-Large | 87.8 | 88.1 | 82.7 | 79.1 |
| **Switch-Large** | **88.5** | **88.6** | **84.7** | **83.0** |
| Δ vs T5-Large | **+0.7** | **+0.5** | **+2.0** | **+3.9** |

| Model | XSum | ANLI (R3) | ARC Easy | ARC Chal. |
|-------|------|-----------|----------|-----------|
| T5-Base | 18.7 | 51.8 | 56.7 | 35.5 |
| **Switch-Base** | **20.3** | **54.0** | **61.3** | 32.8 |
| T5-Large | 20.9 | 56.6 | 68.8 | 35.5 |
| **Switch-Large** | **22.3** | **58.6** | 66.0 | 35.5 |

| Model | CB WebQA | CB NaturalQA | CB TriviaQA |
|-------|----------|--------------|--------------|
| T5-Base | 26.6 | 25.8 | 24.5 |
| **Switch-Base** | **27.4** | **26.8** | **30.7** |
| T5-Large | 27.7 | 27.6 | 29.5 |
| **Switch-Large** | **31.3** | **29.5** | **36.9** |

**关键结论：**
- Switch 在绝大多数任务上 **全面超越** FLOP-matched T5 基线
- **仅两个例外**：ARC Challenge (Switch-Base 略差) 和 ARC Easy (Switch-Large 略差)
- 知识密集型任务（闭卷 QA）受益最大（TriviaQA **+6.2pp**，WebQA **+3.6pp**）
- 推理任务 SuperGLUE：Switch-Base **+4.4pp**，Switch-Large **+2.0pp**

---

## Experiment 4: 蒸馏 (Distillation)

### 蒸馏策略消融

| Technique | Parameters | Neg. Log Perp. |
|-----------|-----------|----------------|
| T5-Base (student) | 223M | -1.636 |
| Switch-Base (teacher) | 3,800M | -1.444 |
| Distillation (standard) | 223M | -1.631 (3%) |
| + Init non-expert weights from teacher | 223M | -1.598 (20%) |
| + 0.75 mix hard + soft loss | 223M | **-1.580 (29%)** |
| Init only (no distillation) | 223M | -1.639 |

- 最佳方案：从 teacher 继承非 expert 权重 + 0.75 硬标签 + 0.25 软标签混合损失
- 保留 29-30% 的质量增益，仅需 1/20 参数量

### 压缩率

| Teacher Params | Compression | Quality Gain Preserved |
|---------------|-------------|----------------------|
| 1.1B (2e) | 82% | 37% |
| 2.0B (4e) | 90% | 32% |
| 3.8B (8e) | 95% | 30% |
| 7.4B (16e) | 97% | 27% |
| 14.7B (32e) | **99%** | **28%** |

### Fine-tuned 模型蒸馏 (SuperGLUE)

| Model | Params | SuperGLUE |
|-------|--------|-----------|
| T5-Base | 223M | 74.6 |
| Switch-Base | 7,410M | 81.3 |
| Distilled T5-Base | 223M | **76.6 (30%)** |

- 即使 fine-tuned specialist model，蒸馏仍保留 30% 收益

---

## Experiment 5: 多语言 (Multilingual)

### 设置
- 预训练：mC4（101 种语言，107 个任务，含文字变体），1M steps
- Baseline：mT5-Base

### 结果

- **101/101 语言全部提升**（无一例外）
- 平均步数加速：**5×**
- **91% 语言获得 ≥4× speedup**

---

## Experiment 6: 小规模适用性

即使在最小规模（2/4/8 experts），Switch Transformer 仍优于 T5-Base——无需超级计算机即可受益。

---

## 汇总：Switch vs Dense 核心指标

| 指标 | Switch-Base vs T5-Base | Switch-Large vs T5-Large |
|------|----------------------|-------------------------|
| 预训练 speedup | **7×** | **2.5×** |
| SuperGLUE 提升 | **+4.4** | **+2.0** |
| TriviaQA 提升 | **+6.2** | **+7.4** |
| 参数量 (vs FLOP-matched dense) | 7B vs 0.2B (35×) | 26B vs 0.7B (37×) |

---

## 关联

- [[fedus2021-switch-transformer-analysis]] — 论文概述
- [[fedus2021-switch-transformer-method]] — 方法机制展开
- [[fedus2021-switch-transformer-critical]] — 贡献/知识点/Negative/可迁移/研究机会
