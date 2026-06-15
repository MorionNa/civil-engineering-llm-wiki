---
title: "Ru et al. (2020) — Neural Architecture Generator Optimization 论文分析"
created: 2026-06-15
updated: 2026-06-15
type: paper-analysis
tags: [neural-architecture-search]
methods: [bayesian-optimization, multi-fidelity-bo, multi-objective-bo, heteroscedastic-bnn, watts-strogatz-graph, erdos-renyi-graph]
results: [cifar10, cifar100, sport8, mit67, flowers102, imagenet, pareto-front-memory-accuracy]
failure_modes: [expanded-space-degradation, bo-dimensionality-limit, no-droppath-auxiliary, compute-cost-high]
datasets: [cifar-10, cifar-100, imagenet, sport8, mit67, flowers102]
sources: [raw/papers/nago_ru2020.pdf]
reproducibility: high
code_url:
  - https://github.com/ruoa/nago
dataset_url: []
confidence: high
---

# NAGO (Neural Architecture Generator Optimization)

> Binxin Ru, Pedro M. Esperança, Fabio M. Carlucci — Oxford / Huawei Noah's Ark Lab — NeurIPS 2020
> **将 NAS 重新定义为"搜索最优网络生成器"**：层次化图搜索空间 + 贝叶斯优化 → 6 个 benchmark SOTA

## 1. 工程背景 (Engineering Background)

NAS 领域长期存在一个深层矛盾：搜索空间越窄，精度越高，但架构突破的可能性越小。2019–2020 年的主流方法（DARTS、ENAS、ProxylessNAS）都依赖**人工设计的 cell-based 搜索空间**——宏观骨架（全局接线）固定，仅搜索微观操作选择。这导致了 Yang et al. (2020) [[nas-evaluation-hard]] 所指出的问题：现有 NAS 方法的高精度很大程度上来自过度工程化的搜索空间和高级训练技巧（DropPath、Auxiliary Towers），而非真正的架构创新。

与此同时，Xie et al. (2019) 的 [[randomly-wired-networks]] 工作表明，随机图模型生成的网络也能达到竞争性性能——这暗示**网络接线比操作选择更重要**，但他们的工作并未提供优化生成器的方法。

## 2. Research Gap

已有 NAS 方法存在两个核心空白：

1. **搜索空间过于狭窄**：cell-based 搜索空间即便搜到最优解，也只是在人类预设的宏观骨架下的局部最优，无法产生 ResNet、DenseNet 级别的范式创新
2. **缺乏对网络生成器的优化方法**：[[randomly-wired-networks]] 证明了随机接线网络的有效性，但只手工设定了生成器超参数，没有系统性地优化它们

**核心空白**：能否设计一个足够宽泛的搜索空间 + 高效的搜索策略，同时实现高精度和新颖架构的发现？

## 3. 科学问题 (Scientific Question)

**如何将 NAS 从"搜索单个最优架构"转变为"搜索最优网络生成器"，从而在极大扩展搜索空间的同时，利用低维连续参数化使贝叶斯优化等高效全局优化方法成为可能？**

## 4. 研究目标 (Research Objective)

提出 NAGO 框架：(1) 构建层次化图搜索空间 HNAG，用仅 8 个连续超参数表达 > 4.58×10⁵⁶ 种架构；(2) 使用多保真度 BO（BOHB）和多目标 BO（MOBO）优化生成器超参数；(3) 在 6 个视觉 benchmark 上验证性能和效率。

## 5. 方法机制 (Method & Mechanism)

→ [[ru2020-nago-method]]

核心创新分为两层：**搜索空间设计**（HNAG）和**搜索策略**（BO-based）。

**HNAG**：三级层次图——顶层 stage graph（WS 模型）、中层 cell graph（ER 模型）、底层 operation graph（WS 模型）。通过三个图的节点数、连接度、重连概率这 8 个连续超参数，可生成从 DARTS-like 到 RNAG-like 的极端多样化架构。

**搜索策略**：BOHB 提供多保真度加速（低 epoch 淘汰差配置），MOBO 在精度-内存双目标上学习 Pareto 前沿。关键创新是**异方差 BNN 代理模型**——网络性能的噪声随超参数变化（图 2），传统同方差 GP/BNN 无法捕获这一点。

## 6. 结果证据 (Result & Evidence)

→ [[ru2020-nago-results]]

- **CIFAR-10**：HNAG-BOHB 96.6% (vs RNAG-BOHB 94.3%)；HNAG-MOBO 96.6% 且仅 12.8MB 内存
- **CIFAR-100**：HNAG-BOHB 79.3% (vs RNAG-BOHB 73.0%)
- **ImageNet**：Top-1 76.8% (5.7M params)，超越 RandWire-WS (74.7%)、DARTS (73.1%)
- **Pareto 前沿**：HNAG-MOBO 找到的模型内存仅为 RNAG-D 的 1/3
- **搜索效率**：12.8 GPU-days (CIFAR-10 BOHB)，虽高于 one-shot 方法但远低于进化方法

关键证据：在 Figure 4 的"搜索方法 vs 随机采样"对比中，NAGO 在全部 5 个数据集上取得了相对于随机采样的**最大提升**——说明 NAGO 的有效性真正来自搜索算法，而非搜索空间本身的优势。

## 7. 贡献 (Contribution)

→ [[ru2020-nago-critical]]

1. **范式转换**：首次将 NAS 定义为网络生成器优化问题，用低维超参数替代高维离散架构选择
2. **HNAG 搜索空间**：三级层次图设计，搜索空间规模 (4.58×10⁵⁶) 远超 DARTS (4.40×10¹²)，且能表达 RNAG 和 DARTS-like 空间为其子集
3. **异方差 BNN 代理**：首次在 BO-NAS 中建模 heteroscedastic noise，NLL 远低于同方差 BNN
4. **仅用 Cutout 超越使用 DropPath+Auxiliary Towers 的 SOTA one-shot 方法**

## 8. 核心知识点 (Core Knowledge)

→ [[ru2020-nago-critical]]

1. **Generator vs. Architecture**：从同一生成器采样的多个架构性能相近 → 评估生成器只需 1 个样本
2. **WS vs. ER 图**：WS 图具有小世界特性（高聚类 + 短路径），适合顶层和底层；ER 图允许单节点，适合中层提供灵活性
3. **Multi-fidelity BO**：低预算（少 epoch）评估可筛选差配置，仅对好配置投入完整训练预算
4. **Local Penalisation**：实现并行 BO 批次推荐，显著加速收敛

## 9. 局限与反思 (Limitations)

→ [[ru2020-nago-critical]]

- 搜索计算成本 (<20 GPU-days) 仍高于 one-shot NAS (<2 GPU-days)
- 扩展搜索空间（加入操作选择和合并方式）反而**降低**性能——BO 在高维空间的采样效率急剧下降
- 未使用 DropPath 和 Auxiliary Towers——这些技巧能提升 one-shot 方法 0.5%+，但难以适配非 cell-based 架构
- ImageNet 仅 10 次 BOHB 迭代，远非充分搜索

## 10. 延伸方向 (Future Directions)

→ [[ru2020-nago-critical]]

- **迁移 BO**：不同数据集的最优超参数相似（表 3）→ transfer BO 可大幅降低搜索成本
- **终身 NAS**：在新任务上复用旧任务的搜索经验
- **与训练技巧结合**：将 DropPath/Auxiliary Towers 适配到 HNAG 空间
- **搜索更多维度**：stage ratio 和 channel ratio 的微调能在合理成本内提升性能（图 7）

## 11. 工程落地要点 (Engineering Takeaways)

→ [[ru2020-nago-critical]]

- HNAG 生成器的 8 个超参数是可以直接调优的连续值，适合接入任何 BO 框架
- 多目标优化对实际部署至关重要——HNAG-MOBO 找到的轻量模型内存仅为 RNAG 的 1/3
- 代码开源，基于 PyTorch，可直接复现
- 参数限制机制：自动根据给定参数预算计算各 stage 的通道数

## 12. 相关页面 (Cross-References)

- [[nago]] — NAGO 实体页面
- [[ru2020-nago-method]] — HNAG + BO 方法细节
- [[ru2020-nago-results]] — 完整实验结果
- [[ru2020-nago-critical]] — 贡献 / 局限 / 延伸分析
- [[randomly-wired-networks]] — RNAG 基础工作 (Xie et al. 2019)
