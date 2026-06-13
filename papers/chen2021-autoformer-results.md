---
title: "AutoFormer 实验结果：ImageNet / 迁移学习 / 蒸馏"
created: 2026-06-13
updated: 2026-06-13
type: paper-analysis
tags: [neural-architecture-search, one-shot-nas, weight-entanglement, autoformer, imagenet, cifar-10, cifar-100, transfer-learning, knowledge-distillation]
sources: [raw/papers/chen2021_autoformer.md]
confidence: high
---

# AutoFormer 实验结果

> 父页面：[[chen2021-autoformer-analysis]]

## Ablation: Weight Entanglement vs 经典权重共享 vs Random Search

| 搜索方法 | 继承权重 | Retrain (300ep) | Params |
|----------|:--------:|:---------------:|:------:|
| Random Search | — | 79.4% | 23.0M |
| Classical Weight Sharing + Random Search | 69.7% | 80.1% | 22.9M |
| **Weight Entanglement + Random Search** | **81.3%** | **81.4%** | 22.8M |
| Classical Weight Sharing + Evolution (SPOS) | 71.5% | 80.4% | 22.9M |
| **Weight Entanglement + Evolution (AutoFormer)** | **81.7%** | **81.7%** | 22.9M |

**关键发现**：
- 经典权重共享继承精度仅 69.7%，远低于 retrain 后的 80.1%——**supernet 排序能力失效**
- Weight Entanglement 继承精度 81.3%，与 retrain 仅差 0.1%——**无需 retrain**
- Random search + entanglement 已接近 evolution search（81.3% vs 81.7%），说明 entanglement 本身贡献了大部分增益
- SPOS (classical sharing + evolution) retrain 后仅 80.4%，比 entanglement random 还差 0.9%

## 继承 vs Finetune vs Retrain

| 模型 | Params | 继承 | Finetune (40ep) | Retrain (300ep) |
|------|:------:|:----:|:---------------:|:---------------:|
| AutoFormer-T | 5.7M | 74.7% | 74.9% | 74.9% |
| AutoFormer-S | 22.9M | 81.7% | 81.8% | 81.7% |
| AutoFormer-B | 53.7M | 82.4% | 82.6% | 82.6% |

**关键发现**：finetune 40 epoch 和 retrain 300 epoch 的增益几乎可忽略（≤0.2%）。Weight Entanglement 真正实现了 **once-for-all training**——supernet 训练完即可直接部署。

## 子网质量：1000 随机采样 from Supernet-Small

从 supernet-small 随机采样 1000 个子网（仅继承权重，无 finetune），top-1 精度分布如图：

- 全部 1000 子网精度 **80.1%–82.0%**
- **全部超越 DeiT-S (79.9%)** 和 RegNetY-8GF (80.0%)
- 仅低于最终搜索出的 AutoFormer-S (81.7%) 不到 1.6%

**这意味着训练好一个 supernet，就能免费获得数千个超越手工设计的模型。**

## ImageNet 主结果

### Tiny 级别 (~5-6M)

| 模型 | Top-1 | Params | FLOPs | 类型 | 设计 |
|------|:-----:|:------:|:-----:|:----:|:----:|
| MobileNetV3-Large | 75.2% | 5.4M | 0.22G | CNN | Auto |
| EfficientNet-B0 | 77.1% | 5.4M | 0.39G | CNN | Auto |
| DeiT-Tiny | 72.2% | 5.7M | 1.2G | Trans | Manual |
| **AutoFormer-Tiny** | **74.7%** | 5.7M | 1.3G | Trans | Auto |

→ **比 DeiT-Tiny 高 2.5%，但不及 EfficientNet-B0（CNN inverted residual 在极小模型上有优势）**

### Small 级别 (~22-23M)

| 模型 | Top-1 | Top-5 | Params | FLOPs | 设计 |
|------|:-----:|:-----:|:------:|:-----:|:----:|
| ResNet-50 | 79.1% | — | 25.5M | 4.1G | Manual |
| RegNetY-4GF | 80.0% | — | 21.4M | 4.0G | Auto |
| DeiT-S | 79.9% | 95.0% | 22.1M | 4.7G | Manual |
| ViT-S/16 | 78.8% | — | 22.1M | 4.7G | Manual |
| T2T-ViT-14 | 81.7% | — | 21.5M | 6.1G | Manual |
| BoTNet-S1-59 | 81.7% | 95.8% | 33.5M | 7.3G | Manual |
| **AutoFormer-S** | **81.7%** | **95.7%** | **22.9M** | **5.1G** | **Auto** |

→ **超越 DeiT-S +1.8%，超越 ViT-S/16 +2.9%，与 T2T-ViT-14 持平但参数量更优**

### Base 级别 (~54M)

| 模型 | Top-1 | Top-5 | Params | FLOPs | 设计 |
|------|:-----:|:-----:|:------:|:-----:|:----:|
| ResNet-152 | 80.8% | — | 60M | 11G | Manual |
| ViT-B/16 | 79.7% | — | 86M | 18G | Manual |
| DeiT-B | 81.8% | 95.6% | 86M | 18G | Manual |
| EfficientNet-B7 | 84.3% | 97.0% | 66M | 37G | Auto |
| **AutoFormer-B** | **82.4%** | **95.7%** | **54M** | **11G** | **Auto** |

→ **超越 DeiT-B +0.6%，参数仅 54M（vs 86M），但 EfficientNet-B7 仍领先 2.0%**

## 迁移学习：下游分类

ImageNet 预训练 → 下游数据集 finetune（DeiT training recipe）：

| 模型 | Params | ImageNet | CIFAR-10 | CIFAR-100 | Flowers | Cars | Pets |
|------|:------:|:--------:|:--------:|:---------:|:-------:|:----:|:----:|
| Graft ResNet-50 | 25M | 79.6 | — | — | 98.2 | 92.5 | — |
| Graft RegNetY-8GF | 39M | 79.6 | — | — | 99.0 | 94.0 | — |
| EfficientNet-B5 | 30M | 83.6 | 98.7 | 91.1 | 98.5 | — | — |
| ViT-B/16 | 86M | 77.9 | 98.1 | 87.1 | 89.5 | — | 93.8 |
| DeiT-B ↑384 | 86M | 83.1 | 99.1 | 90.8 | 98.5 | 93.3 | — |
| **AutoFormer-S ↑384** | **23M** | **83.4** | **99.1** | **91.1** | **98.8** | **93.4** | **94.9** |

**关键发现**：
- AutoFormer-S (23M) 在所有下游数据集上**接近或超越** EfficientNet-B5 (30M) 和 DeiT-B (86M)
- 参数仅为 DeiT-B 的 1/4，但迁移性能相当
- Fine-grained 任务（Cars 93.4%, Pets 94.9%）表现出色，说明 ViT 的 attention 对细粒度特征有效

## 知识蒸馏叠加

使用 RegNetY-32GF 作为 teacher 蒸馏 hard label：

| 模型 | 无蒸馏 | +蒸馏 | 提升 |
|------|:------:|:-----:|:----:|
| AutoFormer-T | 74.7% | **75.7%** | +1.0% |
| AutoFormer-S | 81.7% | **82.4%** | +0.7% |
| AutoFormer-B | 82.4% | **82.9%** | +0.5% |

→ 蒸馏对小模型增益更大（T: +1.0%），架构搜索和蒸馏是正交的优化方向。

## 进化搜索 vs 随机搜索

从 supernet 采样架构的搜索收敛曲线（Fig. 6）：
- 进化搜索随迭代持续提升（top-50 中位数从 ~80.0% → 81.5%）
- 随机搜索收敛更快但上限更低

**但值得注意的是**：random+entanglement 的精度（81.3%）与 evolution+entanglement（81.7%）仅差 0.4%，说明 entanglement 本身贡献了主要增益。

## 关联页面

- [[chen2021-autoformer-analysis]] — 全维度总览
- [[chen2021-autoformer-method]] — 方法展开
- [[chen2021-autoformer-critical]] — 贡献·局限·可迁移·机会
