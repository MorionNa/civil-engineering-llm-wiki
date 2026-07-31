---
id: papers--li2021-bossnas-analysis
title: 'Li et al. (2021) — BossNAS: Block-wisely Self-supervised NAS for Hybrid CNN-Transformers 论文分析'
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/neural-architecture-search
- method/transformer
keywords:
- block-wise-training
- hybrid-cnn-transformer
- neural-architecture-search
- self-supervised
- transformer
sources:
- sources/papers/li2021-bossnas.md
created: '2026-06-14'
updated: '2026-07-31'
confidence: medium
methods:
- ensemble-bootstrapping
- block-wise-search
- self-supervised-nas
- hybrid-search-space
results:
- imagenet
- cifar
- transfer-learning
failure_modes:
- teacher-bias
- block-wise-separation-granularity
- contrastive-loss-doesnt-rank-architectures
- search-space-coupling
datasets:
- imagenet
- cifar-10
- cifar-100
reproducibility: high
code_url:
- https://github.com/changlinli/BossNAS
---

# Li et al. (2021) — BossNAS: 块级自监督混合 CNN-Transformer 架构搜索

> **Authors:** Changlin Li, Tao Tang, Guangrun Wang, Jiefeng Peng, Bing Wang, Xiaodan Liang, Xiaojun Chang
> **Venue:** ICLR 2021 | arXiv:2103.12424 | **Code:** [changlinli/BossNAS](https://github.com/changlinli/BossNAS)

---

## 1. 工程背景

手工设计的混合 CNN-Transformer 架构（如 BoTNet, ViT 混合变体）已在图像分类、检测、分割上取得突破性结果。然而混合架构的搜索空间巨大：CNN 和 Transformer 在感受野、空间分辨率、参数效率上差异极大，手工设计需大量经验试错。NAS 有望自动化这一过程，但现有方法面临双重困境。

## 2. Research Gap

现有 NAS 有两大问题：(1) **权重共享空间过大**导致架构评分不准确——深度每增加一层，权重共享架构数指数爆炸，共享权重高度纠缠无法公平评估；(2) **块级 NAS 的教师偏见**——将搜索空间分块后使用预训练教师网络逐块蒸馏虽可缩小权重共享空间（如 DNA），但评分与教师架构高度相关（卷积老师偏好卷积候选，transformer 老师偏好 self-attention 候选），无法公平评估差异性候选。**无监督 NAS 能否同时解决这两个问题？**

→ 对比 [[chen2021-autoformer-analysis]]（AutoFormer 搜索纯 ViT 架构但依赖有监督权重共享），BossNAS 探索无监督块级搜索混合架构。

## 3. 科学问题

**如何设计一个无监督 NAS 方法，既不依赖标签也不依赖教师模型，同时能在大权重共享空间中给出准确的架构评分？混合 CNN-Transformer 搜索空间的设计如何保证搜索的公平性和有效性？**

## 4. 研究目标

(1) 提出完全无监督的块级 NAS 方案 BossNAS；(2) 设计 Ensemble Bootstrapping 自监督训练方案替代教师蒸馏；(3) 提出无监督架构评价指标（向种群中心搜索）；(4) 构建 HyTra 混合搜索空间；(5) 在 ImageNet 上搜出超越 EfficientNet 的混合架构。

## 5. 方法机制

BossNAS 在"分块搜索空间 + 无监督自训练"框架下运作（Fig. 1c）。核心是两个对称设计的阶段：

**训练阶段 — Ensemble Bootstrapping：** 双 Siamese 超级网络（在线网络 + EMA 动量网络），受 BYOL 启发。关键创新是不让每条路径学自己的动量版本（这会导致权重共享冲突），而是让在线网络的每条路径去预测 EMA 网络中**所有采样路径的预测概率集成（ensemble）**。这为所有权重共享子网络提供了一个共同学习目标，稳定了超级网络训练。

**搜索阶段 — 向种群中心搜索：** 不使用标签或线性分类头作为评估指标（因为对比学习 loss 不代表架构好坏），而是用**整个搜索空间的预测集成作为评价目标**，计算每个候选架构与该集成中心的距离。当块大小为 4 层 × 4 候选时 (|A_k|=256)，可遍历搜索。

→ 完整架构细节：[[li2021-bossnas-method]]

## 6. 结果证据

在 3 个搜索空间 + 3 个数据集上验证：

- **HyTra + ImageNet:** BossNet-T1 达到 82.5% top-1（超越 EfficientNet-B2 2.4%，同推理时间）；BossNet-T0 80.8%（超越 BoTNet50 2.2%、EfficientNet-B1 1.7%、DNA-T 0.5%）
- **MBConv + ImageNet:** BossNet-M2 77.4%（超越 EfficientNet-B0 1.1%）；**架构评分 Spearman ρ=0.78**，超越 MnasNet (0.77) 和 DNA (0.77)，而搜索成本仅 10 GPU-days（比 MnasNet 加速 28.8×）
- **NATS-Bench SS + CIFAR-100:** Spearman ρ=0.76，超越 CE predictor (0.60) 达 0.16 τ

→ 详细数据：[[li2021-bossnas-results]]

## 7. 贡献

1. **Ensemble Bootstrapping 训练方案**：首次将自监督对比学习引入块级 NAS，用概率集成解决超级网络的优化不稳定性
2. **无监督架构评价指标**：用种群集成中心替代标签/教师，消除评分偏差
3. **HyTra 搜索空间**：首个 fabric-like 混合 CNN-Transformer 搜索空间，支持可搜索下采样位置
4. **ResAtt 构建块**：用隐式深度可分离卷积替代显式位置编码，计算量从 O(CW³) 降至 O(CW²)

## 8. 不足与失败模式

1. **块间独立性假设**：将深度维度切成独立块训练，忽略了块间的特征交互和梯度耦合，可能导致搜出的跨块组合非全局最优
2. **对比学习 loss 不等于架构好坏**：虽然作者提出种群中心评估缓解了此问题，但该评估方法依赖"好架构靠近中心"的假设，未见严格理论证明
3. **HyTra 搜索空间耦合**：搜索空间的块划分（4 层/块）影响搜索效果，但如何选择块大小未见系统研究
4. **中-低计算量范围验证**：BossNet-T 的计算量（3-10B MAdds）属于中低端，未验证到更大模型（如 ViT-L/16 级）
5. **仅限分类任务**：未在检测、分割等下游任务上验证 HyTra + BossNAS 的迁移能力

## 9. 泛化能力

BossNAS 在 3 个不同粒度的搜索空间（HyTra 混合空间、MBConv 纯 CNN 空间、NATS-Bench SS 通道搜索空间）和 3 个数据集（ImageNet 大规模 + CIFAR 中等规模）上都取得了 top 级评分精度，说明其无监督架构评价能力具有较强泛化性。关键前提是搜索空间可被合理地在深度维度分块。

## 10. 可复现性

**高。** 代码开源（[changlinli/BossNAS](https://github.com/changlinli/BossNAS)）。搜索空间定义清晰，训练超参数在附录中详细说明。MBConv 和 NATS-Bench 搜索空间为公开 benchmark。HyTra 搜索空间设计细节完整。主要挑战在于 ImageNet 级别的超级网络训练需较多 GPU 资源（10 GPU-days 搜索 + 完整 retraining）。

## 11. 关键洞见

1. **集成 → 稳定 supernet**：多路径共享权重的超网中，单路径 bootstrapping 会因缺少共同目标而不稳定；概率集成提供了一致的优化方向——这是块级 NAS 训练的核心 insight
2. **无监督可超越有监督**：在 MBConv 空间中 BossNAS 评分精度（τ=0.65）超越 DNA 有监督蒸馏（τ=0.62），证明好的无监督设计（ensemble bootstrapping + 种群中心评估）可以反超监督方案
3. **种群中心假设的威力**：以整个搜索空间的平均预测为目标来评分架构，不需要任何标签，且在 CIFAR-100 上超越了用真值训练的性能预测器——这是自监督 NAS 领域的重要发现
4. **混合搜索空间的设计原则**：CNN 和 transformer 块必须计算量匹配（ResAtt 通过隐式位置编码降计算量）、功能对称（ResConv ↔ ResAtt），才能在搜索中公平竞争

## 12. 逻辑链总结

问题：权重共享 NAS 评分不准 → 块级分解可缩小共享空间 → 但块级蒸馏引入教师偏见 → 用自监督对比学习替代蒸馏 → 但 naive bootstrapping 不稳定 → Ensemble Bootstrapping（概率集成提供共同目标） → 种群中心无监督评估 → BossNAS 在 3 个搜索空间均超越 SOTA

→ 批判性分析：[[li2021-bossnas-critical]]

---

*见 [[bossnas]] 实体页 | 方法细节 [[li2021-bossnas-method]] | 实验 [[li2021-bossnas-results]] | 批评 [[li2021-bossnas-critical]]*

## Evidence By Source

### `sources/papers/li2021-bossnas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/bossnas2021_iclr.pdf`

^[sources/papers/li2021-bossnas.md]
