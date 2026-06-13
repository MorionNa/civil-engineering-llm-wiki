---
title: "Chen et al. (2021) — TE-NAS: Training-Free NAS via NTK: 论文分析"
created: 2026-06-12
updated: 2026-06-12
type: paper-analysis
tags: [neural-architecture-search, training-free-nas, ntk, neural-tangent-kernel, linear-regions, expressivity, trainability, weight-sharing-nas, pruning-based-nas]
sources: [raw/papers/TE-NAS_chen2021_ICLR.pdf]
methods: [ntk-condition-number, linear-region-counting, pruning-by-importance, training-free-evaluation]
results: [nas-bench-201, cifar10-darts, imagenet-mobile, gpu-hours-four]
failure_modes: [ntk-correlation-limited, operator-preference-bias, combined-score-naive, no-architecture-novelty, theory-approximation-gap]
datasets: [nas-bench-201, cifar-10, cifar-100, imagenet-16-120, imagenet]
reproducibility: high
code_url:
  - https://github.com/VITA-Group/TENAS
dataset_url:
  - https://github.com/D-X-Y/NAS-Bench-201
confidence: high
---

# TE-NAS (Training-Free Neural Architecture Search)

> Wuyang Chen, Xinyu Gong, Zhangyang Wang — UT Austin — ICLR 2021
> **零训练成本 NAS**：NTK 条件数 + 线性区域数 → 不训练、不用标签，ImageNet 搜 4 GPU 小时

## 1. 工程背景 (Engineering Background)

NAS 的核心瓶颈不是"搜不到好架构"，而是**搜的过程太贵**。DARTS 训练 supernet 动辄数 GPU-day，ENAS 的 RL controller 也要反复训练子网评估。每次评估一个架构就要完整训练 → 搜索成本 = 架构数 × 单次训练成本。这导致 NAS 长期被大厂垄断，学术界的单卡用户望而却步。

另一方面，深度学习理论（NTK、线性区域计数）已经发展出**不需要训练就能刻画网络性质**的工具——但一直停留在理论分析层面，没人把它们用到实际的 NAS 搜索中。

## 2. Research Gap

已有 NAS 方法分两派：
- **训练派**（DARTS/ENAS/SPOS）：训练 supernet 或反复评估子网，成本高且引入搜索偏差
- **权重共享派**（One-shot）：训练一个 supernet，子网直接继承权重评估——但 supernet 训练本身也很贵，且子网排序不准

**核心空白**：能不能完全不训练、不用标签，就在初始化时判断一个架构的好坏？

## 3. 科学问题 (Scientific Question)

**如何利用深度网络理论中的训练无关指标（NTK 谱、线性区域数），在不涉及任何训练和标签的情况下，快速、可靠地排序神经架构的质量？**

## 4. 研究目标 (Research Objective)

提出 TE-NAS 框架：(1) 用 NTK 条件数 κN 衡量可训练性 + 线性区域数 ˆRN 衡量表达能力；(2) 基于 pruning-by-importance 机制高效搜索；(3) 在 NAS-Bench-201、DARTS CIFAR-10/ImageNet 上以极小搜索成本达到 SOTA 精度。

## 5. 方法机制 (Method & Mechanism)

→ [[chen2021-tenas-method]]

核心：**两个零训练指标 + pruning 搜索**。

1. **NTK 条件数 κN**：越小 → 梯度下降越容易优化（可训练性好）
2. **线性区域数 ˆRN**：越多 → 网络能表达更复杂的函数（表达能力强）
3. **Pruning-by-importance**：不采样评估每个架构，而是从全连接 supernet 出发，按边的重要性逐边剪枝，复杂度从 |O|^E 降到 |O|×E

两者 combine：用相对排名求和（不直接加数值），避免量级差异导致一方主导。

## 6. 结果证据 (Result & Evidence)

→ [[chen2021-tenas-results]]

- **NAS-Bench-201**：CIFAR-10 93.9%，搜索仅 1558 GPU 秒（vs DARTS 10890s）
- **DARTS CIFAR-10**：test error 2.63%，搜索 0.05 GPU-day
- **ImageNet (mobile)**：top-1 24.5%，搜索 4 GPU 小时（单 1080Ti）

关键：TE-NAS 比同期训练-free 方法（NASWOT）精度高 + 方差小。

## 7. 贡献 (Contribution)

→ [[chen2021-tenas-critical]]

1. 首次将 NTK 谱分析和线性区域计数引入实际 NAS，实现**完全不训练**
2. 发现 κN 和 ˆRN 分别偏好不同算子（skip-connect vs conv1×1），首次解耦可训练性和表达能力的独立贡献
3. Pruning-by-importance 搜索机制，复杂度线性于搜索空间大小
4. ImageNet 搜索仅 4 GPU 小时，单卡可跑

## 8. 核心知识点 (Core Knowledge)

1. **NTK 条件数 = 可训练性代理**：初始化时算一次 NTK 的特征值谱，条件数小 → loss landscape 平坦 → 梯度下降收敛快
2. **线性区域数 = 表达能力代理**：ReLU 网络将输入空间划分成若干线性区域，区域越多表达越强
3. **两者天然 tension**：κN 偏好 skip-connect（利于梯度流），ˆRN 偏好 conv（增加非线性）——需要显式 trade-off
4. **训练-free 不是魔法**：两个指标与测试精度的 Kendall-tau 相关性约 0.5-0.7，足够排序但非完美

## 9. Negative Knowledge

→ [[chen2021-tenas-critical]]

- κN 和 ˆRN 的 rank correlation ~0.5-0.7，不是精确预测——可能漏掉好架构或高估差架构
- 两个指标的等权求和是最 simple 的方案，没有理论保证最优
- NTK 分析依赖 Kaiming 初始化 → 换初始化策略需要重新验证
- ˆRN 只对 ReLU 网络有效，非 ReLU 激活函数不适用
- 搜索空间固定（cell-based），不能发现全新架构类型

## 10. 可迁移知识 (Transferable Knowledge)

→ [[chen2021-tenas-critical]]

| 知识 | → 迁移 |
|------|--------|
| 训练-free 指标替代 validation accuracy | 任何需要快速评估模型质量的场景 |
| pruning-by-importance 搜索 | 从 |O|^E 降为 |O|×E 的通用搜索加速模式 |
| NTK 条件数作为可训练性指标 | 可迁移到其他模型选择/初始化分析场景 |
| 相对排名组合异构指标 | 两个量纲不同的指标如何公平融合 |

## 11. 研究机会 (Research Opportunity)

→ [[chen2021-tenas-critical]]

- 发现更强的训练-free 指标（如 Zico、GradSign 的后续工作已验证）
- TE-NAS + Transformer 搜索（当时限于 CNN，现在可扩展到 ViT）
- 动态 pruning 阈值替代固定值
- 训练-free 指标指导 supernet 训练（而非替代）

## 12. 可复现性 (Reproducibility)

**🟢 高复现性** — 代码 + benchmark 完全公开

| 项目 | 说明 |
|------|------|
| **等级** | 🟢 高 |
| **官方代码** | `https://github.com/VITA-Group/TENAS`（PyTorch） |
| **Benchmark** | NAS-Bench-201 公开数据库，无需重新评估 |
| **数据集** | CIFAR-10/100 / ImageNet-16-120 / ImageNet（全公开） |
| **协议** | MIT |

**复现要点**：单卡 1080Ti 可完整复现。NAS-Bench-201 直接查表验证最快。NTK 计算需要 batch 数据通过未训练网络前传，代码包已包含。

## 关联页面

- [[chen2021-tenas-method]] — NTK 条件数 + 线性区域 + pruning 搜索展开
- [[chen2021-tenas-results]] — NAS-Bench-201 / DARTS / ImageNet 完整数据
- [[chen2021-tenas-critical]] — 贡献 / Negative / 可迁移 / 机会
- [[xie2021-segformer-analysis]] — SegFormer 也是"less is more"的架构设计哲学
