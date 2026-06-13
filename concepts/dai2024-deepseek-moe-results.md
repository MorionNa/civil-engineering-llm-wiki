---
title: "Dai et al. (2024) — DeepSeekMoE 实验结果"
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [mixture-of-experts, sparse-moe, large-language-model, decoder-only-transformer, efficient-inference]
sources: [raw/papers/dai2024_deepseek_moe.pdf]
confidence: high
---

# DeepSeekMoE 实验结果

← 返回总览：[[dai2024-deepseek-moe-analysis]]

## 实验 1：2B 验证实验 — vs 五种架构（Table 1）

| 指标 | Dense 0.2B | Hash Layer 2B | Switch Trans. 2B | GShard 2B | **DeepSeekMoE 2B** |
|------|-----------|---------------|-------------------|-----------|---------------------|
| 总参数 | 0.2B | 2.0B | 2.0B | 2.0B | 2.0B |
| 激活参数 | 0.2B | 0.2B | 0.2B | 0.3B | 0.3B |
| Pile Loss ↓ | 2.060 | 1.932 | 1.881 | 1.867 | **1.808** |
| HellaSwag ↑ | 38.8 | 46.2 | 49.1 | 50.5 | **54.8** |
| PIQA ↑ | 66.8 | 68.4 | 70.5 | 70.6 | **72.3** |
| ARC-easy ↑ | 41.0 | 45.3 | 45.9 | 43.9 | **49.4** |
| ARC-challenge ↑ | 26.0 | 28.2 | 30.2 | 31.6 | **34.3** |
| HumanEval ↑ | 0.0 | 1.2 | 2.4 | 3.7 | **4.9** |
| TriviaQA ↑ | 4.9 | 6.5 | 8.9 | 10.2 | **16.6** |
| NQ ↑ | 1.4 | 1.4 | 2.5 | 3.2 | **5.7** |

**结论**：DeepSeekMoE 在 12 个 benchmark 的绝大多数上全面碾压 GShard（同总参数量/同激活参数量），知识密集型任务（TriviaQA）优势尤为显著。

## 实验 2：逼近 MoE 理论上限

| 对比 | Pile Loss |
|------|-----------|
| DeepSeekMoE 2B | 1.808 |
| GShard×1.5 (2.9B total, 1.5× expert params+compute) | 1.808 |
| Dense×16 (同总参数量密集模型，MoE 理论上限) | 1.806 |

**结论**：DeepSeekMoE 2B 性能与 1.5× 计算量的 GShard 持平，且仅比同参数量密集模型差 0.002 loss——**逼近 MoE 的性能上限**。

## 实验 3：Ablation — 两大策略有效性（Figure 2）

| 配置 | 归一化性能 |
|------|-----------|
| GShard (0 shared, 2/16 routed) | 基线 |
| + Shared Expert Isolation (1 shared, 1/15 routed) | ↑ 提升 |
| + Fine-Grained ×2 (1 shared, 3/31 routed) | ↑↑ 再提升 |
| + Fine-Grained ×4 (1 shared, 7/63 routed, =DeepSeekMoE) | ↑↑↑ 最佳 |

**单调递增**——两大策略各自有效、叠加更强。

## 实验 4：专家特化分析

### 路由专家冗余度低（Figure 3）
逐步 disable 最高概率的路由专家后，DeepSeekMoE 的 Pile loss 上升比 GShard×1.5 更快 → 每个路由专家更不可替代 → **冗余度更低**。

### 共享专家不可替代
Disable 共享专家、多激活 1 个路由专家（计算量不变）：Pile loss 从 1.808 暴增到 2.414 → 共享专家捕获了路由专家无法替代的**基础性通用知识**。

### 更精确的知识获取（Figure 4-5）
- 仅激活 4 个路由专家（vs 通常 7 个），DeepSeekMoE 仍与 GShard 可比
- 从头训练一个仅激活 3 个路由专家的 DeepSeekMoE（总参数不变、激活减半），仍**超越** GShard

→ 验证了"更高组合灵活性 → 更精确知识获取"的核心假说。

## 实验 5：DeepSeekMoE 16B — vs Llama2 7B / DeepSeek 7B（Table 2）

| 指标 | Llama2 7B (Dense, 6.7B) | DeepSeek 7B (Dense, 6.9B) | **DeepSeekMoE 16B** (激活 2.8B) |
|------|--------------------------|----------------------------|-----------------------------------|
| FLOPs per 4K | 187.9T | 183.5T | **74.4T** (40% 计算量) |
| Pile BPB ↓ | 0.76 | 0.75 | **0.74** |
| HellaSwag ↑ | 75.6 | 75.4 | **77.1** |
| GSM8K ↑ | 15.5 | 17.4 | **18.8** |
| MATH ↑ | 2.6 | 3.3 | **4.3** |
| HumanEval ↑ | 14.6 | 26.2 | **26.8** |
| MBPP ↑ | 21.8 | 39.0 | **39.2** |
| TriviaQA ↑ | 63.8 | 59.7 | **64.8** |
| CEval (中文) ↑ | 33.9 | 45.0 | 40.6 |
| CMMLU (中文) ↑ | 32.6 | 47.2 | 42.5 |
| MMLU ↑ | 45.8 | 48.2 | 45.0 |

**结论**：
- 仅 40% 计算量，总体上与 Llama2 7B / DeepSeek 7B **性能可比**
- Coding、Math、知识密集型任务上显著超越
- 中文任务（CEval/CMMLU）弱于 DeepSeek 7B——**注意力参数量受限**可能是瓶颈
- MMLU（多选题）略逊——同样可能与有限的 attention 参数有关

## 关键实验结论

1. **架构优势**：DeepSeekMoE 在所有规模（2B/16B）上均优于 GShard 等传统 MoE
2. **计算效率**：16B 模型仅需 40% 计算量即达 7B 密集模型水平
3. **专家特化验证**：降低冗余 + 共享不可替代 + 更少激活即达同等效果
4. **逼近理论上限**：2B 规模下仅比同参数量密集模型差 0.002 loss

← 方法机制：[[dai2024-deepseek-moe-method]]
→ 贡献与反思：[[dai2024-deepseek-moe-critical]]
