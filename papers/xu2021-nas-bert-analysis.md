---
title: "Xu et al. (2021) — NAS-BERT: Task-Agnostic BERT Compression with NAS: 论文分析"
created: 2026-06-13
updated: 2026-06-13
type: paper-analysis
tags: [neural-architecture-search, bert-compression, transformer, task-agnostic-compression, weight-sharing-nas, pruning-based-nas, knowledge-distillation, block-wise-training, progressive-shrinking, separable-convolution, supernet]
sources: [raw/papers/xu2021_nas_bert.md]
methods: [block-wise-search, progressive-shrinking, knowledge-distillation, supernet-training, performance-approximation]
results: [glu-e, squad, adaptive-size, task-agnostic, model-compression]
failure_modes: [supernet-convergence-difficulty, search-cost-explosion, block-wise-isolation-bias]
datasets: [glu-e, squad, bookcorpus, wikipedia]
reproducibility: medium
code_url: []
dataset_url:
  - https://gluebenchmark.com/
  - https://rajpurkar.github.io/SQuAD-explorer/
confidence: high
---

# NAS-BERT: Task-Agnostic and Adaptive-Size BERT Compression with Neural Architecture Search

> Jin Xu, Xu Tan, Renqian Luo, Kaitao Song, Jian Li, Tao Qin, Tie-Yan Liu — Microsoft Research Asia — KDD 2021
> **Task-agnostic BERT 压缩**：NAS 搜索新颖架构，输出 5M-60M 多尺寸模型，GLUE/SQuAD 超越手设计 BERT 和蒸馏方法

## 1. 工程背景 (Engineering Background)

BERT 等预训练语言模型在 NLP 下游任务表现优异，但参数量大（BERT-base 110M）、推理慢，难以部署到在线服务器、手机、嵌入式设备等多种资源约束场景。不同设备对内存和延迟的要求不同——嵌入式设备需要极小模型，在线服务器可接受较大模型——单一固定尺寸的压缩模型无法覆盖全部部署需求。^[raw/papers/xu2021_nas_bert.md]

## 2. Research Gap

已有 BERT 压缩方法存在两个缺口：(1) **固定尺寸**：DistilBERT、TinyBERT、MobileBERT 等都输出单一尺寸的压缩模型，无法自适应不同设备的内存/延迟约束；(2) **任务依赖**：AdaBERT、DynaBERT 在 fine-tuning 阶段为每个下游任务单独压缩，一个任务的压缩模型难以泛化到其他任务，且逐任务压缩成本高。核心空白是：**如何在预训练阶段一次性搜索出多尺寸架构族，同时保持下游任务无关性？** ^[raw/papers/xu2021_nas_bert.md]

## 3. 科学问题 (Scientific Question)

**如何在预训练阶段，利用 NAS 在包含多种算子（MHA/FFN/SepConv/Identity）和多种 hidden size 的超大搜索空间中，训练一个 weight-sharing supernet，并从中高效提取满足不同尺寸和延迟约束的 Task-Agnostic 压缩架构？核心难题是 supernet 在 NLP 预训练任务上的训练成本极高。** ^[raw/papers/xu2021_nas_bert.md]

## 4. 研究目标 (Research Objective)

提出 NAS-BERT 框架：(1) 设计包含 MHA、FFN、SepConv、Identity 四种操作 + 5 种 hidden size 的搜索空间；(2) 用 block-wise training + knowledge distillation 降低 supernet 训练成本；(3) 用 progressive shrinking 动态剪枝搜索空间集中资源给有潜力架构；(4) 用 performance approximation 快速从 multi-block 组合中选择满足约束的最优架构。^[raw/papers/xu2021_nas_bert.md]

## 5. 方法机制 (Method & Mechanism)

→ [[xu2021-nas-bert-method]]

三阶段流程：**搜索空间设计 → supernet 训练（block-wise + progressive shrinking）→ 模型选择（lookup table + performance approximation）**。

- **搜索空间**：链式结构 24 层，每层可选 MHA / FFN / SepConv(k=3,5,7) / Identity，每个操作有 5 种 hidden size {128,192,256,384,512}，共 26 个候选操作。supernet 被分为 N=4 blocks，每 block 6 层、hidden size 内部一致。
- **Block-wise 训练**：每个 student block 独立训练，用教师模型对应 block 的输入/输出 hidden states 做 MSE 蒸馏。hidden size 不匹配时用可学习线性变换对齐。
- **Progressive shrinking**：每 epoch 后按 validation loss 在每个 bin（按模型大小分组）中剪掉最差的 50% 架构，到只剩 10 个为止。bin 的设计保证多尺寸多样性的保留。
- **Model selection**：构建 lookup table，latency 用逐层累加法近似（预测量 26 个单操作延迟），loss 用 block-wise dev loss 相加近似，最终评估 top-T 候选选出最优。

## 6. 结果证据 (Result & Evidence)

→ [[xu2021-nas-bert-results]]

- **vs 手设计 BERT**：在 60M/30M/10M/5M 四个尺寸上，NAS-BERT 全面超越同参数量的手设计 Transformer baseline，模型越小优势越大（NAS-BERT5 领先 +3.9% AVG）。
- **vs 已有压缩方法**：NAS-BERT60 (84.2 AVG) 超越 DistilBERT (79.6)、TinyBERT (80.6)、DynaBERT (82.7) 等，数据增强后达 84.8。SQuAD v1.1 F1=88.0, v2.0 F1=76.3。
- **Ablation**：progressive shrinking 带来 +1.1% AVG 且搜索时间从 50h 降到 5min；两阶段蒸馏均有增益；pruning architectures 优于 pruning operations。

## 7. 贡献 (Contribution)

→ [[xu2021-nas-bert-critical]]

1. **首次将 NAS 引入 BERT 预训练级压缩**，不同于以往 CV 领域的 NAS-for-efficient-models 或 fine-tune 级 NAS 压缩
2. **块间弹性 hidden size 设计**：不同 block 可以不同 hidden size，真正实现弹性宽度搜索
3. **Bin-based progressive shrinking**：按模型大小分 bin 再剪枝，确保搜索结束时仍有覆盖全尺寸范围的候选架构
4. **Block-wise + performance approximation** 降低搜索成本三招组合：分块 → 块内 progressive shrinking → 近似评估，将完整搜索从不可行变为 3 天 32×P40 GPU

## 8. 核心知识点 (Core Knowledge)

1. **NAS 可以做 BERT 级预训练压缩**：前提是 block-wise 分治 + progressive shrinking 控制成本，否则直接训练完整 supernet 根本无法收敛
2. **SepConv 在 NLP 中有竞争力**：当参数量受限于 5-60M 时，SepConv 可能在部分层优于 MHA/FFN，NAS 自动决定了哪些层用什么操作
3. **Bin-based shrinking = 多样性保证**：如果不分 bin 直接剪枝，大会被早期优化困难淘汰、小会被后期容量不足淘汰——bin 保留全尺寸候选
4. **Block-wise 蒸馏 + 线性变换对齐 hidden size**：当 student/teacher hidden size 不一致时，可学习投影层是简单有效的对齐方案

## 9. Negative Knowledge

→ [[xu2021-nas-bert-critical]]

- Supernet training 收敛极难：作者 preliminary experiment 中直接训练完整 supernet（不用 block-wise）甚至不收敛
- Block-wise 训练破坏了 block 间的交互：每个 block 独立蒸馏，最优 block 的组合不一定全局最优
- Progressive shrinking 的超参敏感：bin 数 B=10、每 epoch 剪 50%、保留 m=10，换配置可能得到不同架构
- 不适用于需要 cross-block attention 或长距离依赖的架构压缩
- 知识蒸馏只用了 prediction layer distillation，更先进的中间层/attention 蒸馏未探索

## 10. 可迁移知识 (Transferable Knowledge)

→ [[xu2021-nas-bert-critical]]

| 知识 | → 迁移 |
|------|--------|
| Block-wise supernet 训练 + 教师蒸馏 | 任何超大模型（>100M）NAS 搜索的通用降成本策略 |
| Bin-based progressive shrinking | 需要保持输出多样性的任何 pruning-based 搜索 |
| Performance approximation via lookup table | 延迟/精度快速评估，避免逐架构实测 |
| 预训练级 NAS = task-agnostic | 可推广到其他预训练模型（ViT, GPT 系列）的压缩 |
| SepConv 在 NLP 小模型中的竞争力 | 为 NLP 轻量架构设计提供备选操作 |

## 11. 研究机会 (Research Opportunity)

→ [[xu2021-nas-bert-critical]]

- 将 NAS-BERT 框架迁移到 GPT/decoder-only 模型压缩（生成任务 vs 理解任务的不同搜索空间需求）
- Cross-block search：打破 block 独立约束，搜索 block 间 hidden size 的全局最优组合
- 更丰富搜索空间：加入动态卷积、稀疏 attention、混合专家（MoE）等操作
- 结合更先进的蒸馏技术（attention distillation, embedding distillation）进一步提升
- Training-free NAS 指标（如 NTK）替代 validation loss 评估，进一步降低搜索成本

## 12. 可复现性 (Reproducibility)

**🟡 中复现性** — 论文配置详细但无开源代码

| 项目 | 说明 |
|------|------|
| **等级** | 🟡 中 |
| **官方代码** | 未公开 |
| **数据集** | GLUE / SQuAD v1.1 & v2.0 / English Wikipedia + BookCorpus（全公开） |
| **计算资源** | 32 NVIDIA P40 GPUs × 3 天 supernet 训练 + 教师 BERT-base 5 天 16 V100 GPUs |
| **复现要点** | 附录 A.1-A.5 提供了完整训练超参和搜索空间细节。核心难点在 supernet 训练收敛控制。无代码需从零实现 chain-structured supernet + block-wise 蒸馏框架。 |

## 关联页面

- [[xu2021-nas-bert-method]] — 搜索空间 / Block-wise 训练 / Progressive shrinking / Model selection 展开
- [[xu2021-nas-bert-results]] — GLUE / SQuAD / Ablation 完整数据
- [[xu2021-nas-bert-critical]] — 贡献 / 知识点 / Negative / 可迁移 / 研究机会
- [[chen2021-tenas-analysis]] — 同样是 NAS 搜索，TE-NAS 走 training-free 路线形成对比
- [[jiang2024-mixtral-of-experts-analysis]] — Mixtral 的稀疏 MoE 可作为 NAS-BERT 未来搜索空间的候选操作
