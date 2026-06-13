---
title: "Lepikhin et al. (2020) — GShard: 论文分析"
created: 2026-06-13
updated: 2026-06-13
type: paper-analysis
tags: [neural-network, deep-learning, transformer, mixture-of-experts, sparse-moe, gating-network, top-k-routing, load-balancing, conditional-computation, automatic-sharding, spmd, model-parallelism, distributed-training, sublinear-scaling, compiler-optimization, xla-compiler, multilingual-data]
sources: [raw/papers/lepikhin2021_gshard.md]
methods: [mixture-of-experts, top-2-gating, expert-capacity, auxiliary-loss, random-routing, automatic-sharding, spmd-partitioning, alltoall-resharding, einsum-partitioning, tensor-sharding-annotations]
results: [sublinear-scaling, superlinear-quality, sample-efficiency, constant-memory, o1-compilation, 600b-parameters, multilingual-bleu]
failure_modes: [capacity-bottleneck, diminishing-returns, numerical-stability-bfloat16, gating-sequential-bottleneck, expert-load-imbalance]
datasets: [in-house-web-scale-mt-corpus]
reproducibility: low
code_url:
  - https://github.com/tensorflow/tensorflow (XLA compiler)
dataset_url:
  - (in-house Google dataset, not publicly available)
confidence: high
---

# Lepikhin et al. (2020) — GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding

> **DOI:** 10.48550/arxiv.2006.16668 | **ICLR 2021** | **Google**
> **Authors:** Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu, Dehao Chen, Orhan Firat, Yanping Huang, Maxim Krikun, Noam Shazeer, Zhifeng Chen
> **Code:** XLA compiler in TensorFlow (open-source); MoE model code and dataset NOT public

---

## 1. 工程背景

训练超大规模神经网络（>100B 参数）面临三大工程瓶颈：(1) 单个加速器显存放不下模型；(2) 模型并行缺乏框架支持，手工实现工程量大且耦合模型代码；(3) 编译器图规模随设备数 O(D²) 膨胀导致编译不可行。不解决这些问题，模型容量增长将止步于单卡显存上限，阻碍多语言翻译等大容量需求场景。

## 2. Research Gap

已有模型并行方案（GPipe 流水线并行、Mesh-TensorFlow 算子级并行）要么需要专用框架迁移模型代码，要么图规模线性增长限制了扩展性。条件计算（MoE）虽已证明可让 RNN-LM 达 69B 参数 [Shazeer et al. 2017]，但缺乏通用分布式训练系统支持——MoE 的稀疏 dispatch/combine 模式与现有并行策略不兼容。**核心矛盾：MoE 架构提供了亚线性计算缩放的潜力，但缺乏能自动处理专家分片与通信的编译基础设施。**

## 3. 科学问题

**如何在保持 O(1) 编译时间和亚线性计算开销的同时，将条件计算（Mixture-of-Experts）自动扩展到数千个加速器，使单模型达到 600B+ 参数且训练时间可行？**

→ 这不是"MoE 是否有效"的问题，而是"MoE 如何被系统自动高效地并行化"的问题。

## 4. 研究目标

开发 GShard 模块：(1) 提供轻量级张量分片标注 API，最小化模型代码改动；(2) 在 XLA 编译器中实现 SPMD 自动分区器，编译时间 O(1) 与设备数无关；(3) 将 Transformer + MoE 扩展到 600B 参数，在 2048 TPU v3 上 4 天完成训练；(4) 验证亚线性计算/内存缩放和超线性质量提升。

## 5. 方法机制

GShard 系统分三层：**模型层** — Transformer 每隔一个 FFN 替换为 Position-wise MoE 层（top-2 gating + expert capacity + auxiliary loss + random routing），每个 token 只激活 2 个专家，计算量独立于总专家数；**标注层** — 通过 `split()`/`replicate()`/`shard()` API 声明张量分片策略，分离模型描述与并行实现；**编译层** — XLA SPMD Partitioner 自动将标注后的全尺寸计算图转换为单程序多数据（SPMD）程序，插入 AllToAll/AllReduce/CollectivePermute 通信原语，处理非均匀分片和 halo exchange。

→ [[lepikhin2021-gshard-method]] 完整架构图 + 算法 + 通信模式详解

## 6. 结果证据

在多语言翻译任务（100 language → English，25B 训练样本）上验证：
- **质量：** MoE(2048E, 36L) 600B 模型 avg BLEU 44.3，∆BLEU +13.5，碾压所有 baselines（单语基线 avg 30.8，密集 T(96L) 2.3B 仅 +6.1）
- **效率：** 600B 模型训练仅需 22.4 TPU v3 core-years、4 天；密集 T(96L) 需 235 core-years、6 周
- **缩放：** 模型大小 16x（37B→600B），计算成本仅 3.6x（6→22 core-years）；单设备显存 O(1)
- **更深 > 更宽：** 深度 12L→36L 带来 2-3 BLEU 稳定提升；专家数 128→512 跳跃性提升（+3.3 BLEU），512→2048 边际递减（+1.3）

→ [[lepikhin2021-gshard-results]] 完整实验表格 + 数值分析

## 7. 贡献

1. **GShard 系统：** 首个通过轻量标注 API + XLA 编译器 SPMD 分区实现自动模型并行的通用方案，编译时间 O(1)
2. **MoE Transformer：** 将条件计算扩展到 Transformer encoder-decoder，top-2 gating + expert capacity + auxiliary loss + random routing 的四合一门控设计
3. **亚线性缩放的实证验证：** 模型大小 16x → 计算量 3.6x，单设备显存 O(1)，通信 O(√D)
4. **600B 多语言 NMT SOTA：** 单模型超越 100 个单语基线，训练效率远超密集模型
5. **容量瓶颈 vs 正向迁移的相互作用分析：** 揭示了深度（促进迁移）与宽度/专家数（缓解容量瓶颈）对高低资源语言的不同影响

→ [[lepikhin2021-gshard-critical#7-贡献-contribution]]

## 8. 核心知识点

1. **条件计算 = 亚线性缩放的关键：** 每个 token 仅激活 O(1) 专家，计算量独立于总专家数，让模型容量与计算成本解耦
2. **SPMD > MPMD 用于编译扩展性：** 生成单程序在所有设备上运行，编译时间 O(1) vs MPMD 的 O(D)
3. **标注 API 实现关注点分离：** 模型开发者只需标注关键张量的分片策略，编译器自动推导其余张量 + 反向传播的分片
4. **容量瓶颈在 128-512 专家区间：** 低于此数，高资源语言质量因任务干扰受损；越过瓶颈后，继续扩专家边际递减
5. **深度促进正向迁移，宽度缓解容量瓶颈：** 密集深模型（T(96L)）在低资源语言上优于浅 MoE，因为 100% 参数共享最大化迁移

→ [[lepikhin2021-gshard-critical#8-核心知识点-core-knowledge]]

## 9. Negative Knowledge

- **容量瓶颈区间需针对任务重新确定**（128-512 专家仅为本文实验设置）
- **1T 模型 bfloat16 数值不稳定**，论文未包含其结果——超大模型的训练稳定性仍是开放问题
- **门控中 Cumsum 操作是串行瓶颈**（O(D) 复杂度），虽常数因子小，但扩展至万级专家可能成为主导
- **AllToAll 通信成本 O(√D)**，非零成本，极端规模下仍可成为瓶颈
- **代码和数据集均不公开**——GShard XLA 部分在 TensorFlow 开源，但 MoE 模型实现和 25B 训练数据未公开
- **仅验证了 NMT 场景**——GShard 通用性在图像空间分区上有简述（Appendix A.4），但无实验
- **专家容量固定为 O(N/E)**，可能在高方差 token 分布下导致过度溢出

→ [[lepikhin2021-gshard-critical#9-negative-knowledge]]

## 10. 可迁移知识

| 知识 | 迁移方向 |
|------|----------|
| SPMD 自动分区范式 | 任何大规模分布式训练：编译器根据标注生成单程序，O(1) 编译 |
| 标注 API 解耦模型与并行 | 研究者写模型如单设备，标注关键张量即可——适用于所有框架 |
| top-2 gating + expert capacity + auxiliary loss | 任何 MoE 实现的标准配方 |
| 亚线性缩放的要素：条件计算 | 不仅要大模型，还要每个样本只激活子网络 |
| 通信原语与 Einsum 分区模式 | AllToAll resharding 适合 MoE dispatch/combine 模式 |

→ [[lepikhin2021-gshard-critical#10-可迁移知识-transferable-knowledge]]

## 11. 研究机会

自动分片策略优化（超越迭代数据流分析，如 ILP/ML）、动态专家容量、MoE 在更多架构（ViT、扩散模型）上的应用、GShard 扩展到多框架（PyTorch/XLA、JAX）、专家专业化分析（哪些专家学了什么语言/任务）、推理优化（MoE 推理时仅有部分专家激活但显存占用仍大）。

→ [[lepikhin2021-gshard-critical#11-研究机会-research-opportunity]]

---

## 12. 可复现性 (Reproducibility)

**🔴 低复现性** — 数据和 MoE 模型代码未公开，但 XLA 编译器开源且论文方法描述详尽

| 项目 | 说明 |
|------|------|
| **等级** | 🔴 低 |
| **官方代码** | XLA SPMD Partitioner 在 TensorFlow 仓库（`tensorflow/compiler/xla`）开源；GShard API 为内部 Lingvo 框架扩展 |
| **数据集** | Google 内部 Web 挖掘数据（25B 平行句对，100 语言↔英语），不公开 |
| **协议** | XLA: Apache 2.0；MoE 模型: 未公开 |
| **复现要点** | 需要 >128 TPU v3 集群和 25B 级 Web 平行语料。XLA SPMD Partitioner 可独立使用，论文提供了完整的 Einsum 分区模式和通信原语说明，有开源复现可能（如 Fairseq MoE、DeepSpeed MoE 借鉴了此设计） |

## 关联页面

- [[lepikhin2021-gshard-method]] — 方法机制展开：MoE 架构 + GShard API + SPMD 分区器
- [[lepikhin2021-gshard-results]] — 结果证据展开：翻译质量 + 训练效率 + 显存与运行时
- [[lepikhin2021-gshard-critical]] — 贡献 + 知识点 + Negative + 可迁移 + 研究机会
