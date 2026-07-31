---
id: papers--chen2021-tenas-critical
title: TE-NAS 贡献·局限·可迁移·研究机会
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/neural-architecture-search
- method/pinn
- method/transformer
keywords:
- linear-regions
- nas-bench-201
- neural-tangent-kernel
- ntk
- pruning-based-nas
- training-free-nas
sources:
- sources/papers/chen2021-tenas.md
created: '2026-06-12'
updated: '2026-07-31'
confidence: high
failure_modes:
- ntk-correlation-limited
- operator-preference-bias
- combined-score-naive
- no-architecture-novelty
- theory-approximation-gap
---

# TE-NAS 贡献·局限·可迁移·研究机会

> 父页面：[[chen2021-tenas-analysis]]

## 贡献 (Contribution)

### 1. 首次实现真正训练-free 的 NAS

不训练任何网络（不用 supernet、不训子网、不用标签），仅在 Kaiming 初始化时计算两个理论指标就完成搜索。在 ImageNet 上搜索成本仅 4 GPU 小时，比 RL 方法省 **12,000 倍**。

### 2. 解耦可训练性与表达能力

首次量化了 κN（NTK 条件数 → 可训练性）和 ˆRN（线性区域数 → 表达能力）对算子选择的不同偏好。κN 选 skip-connect，ˆRN 选 conv——两者的 tension 是之前 NAS 方法未曾明确揭示的。

### 3. Pruning-by-Importance 搜索机制

相比采样式搜索的指数复杂度，pruning 将复杂度降为线性：|O|^E → |O| × E。这使 TE-NAS 可以处理更大的搜索空间。

### 4. 桥接理论与应用

首次将 NTK、线性区域等深度学习理论工具引入实际 NAS pipeline，证明"理论可以指导工程"——这一工作鼓舞了后续大量训练-free NAS 研究（ZiCo、GradSign、NASWOT 等）。

## Negative Knowledge

### 适用范围 / 前提假设

- **搜索空间必须是 cell-based**（DAG 结构），非 DAG 架构（如 MLP、chain-structure）未验证
- **仅验证 ReLU 激活函数**——线性区域计数依赖 ReLU 的分段线性性质
- **依赖 Kaiming 初始化**——NTK 分析假定权重来自特定分布
- **分类任务**——未扩展到检测、分割等其他 vision task

### 失效场景

- **指标相关性仅 ~0.5-0.7**（Kendall-tau）：不是精确预测，可能漏掉好架构。TE-NAS 的结果有方差（±0.47%）
- **固定的算子候选集**：如果某条边的最优算子是 dilated conv 5×5 而 TE-NAS 偏好 conv3×3，则可能选不到最优
- **不适用于已经训练过的网络**：NTK 分析假定网络处于初始化状态
- **大 batch 场景**：NTK 矩阵大小 = batch_size × batch_size，大 batch 下内存爆炸

### 未解决的问题

- 等权求和是否最优？——论文尝试了加权但等权最好，没有理论解释
- κN 和 ˆRN 是否独立？——论文假设独立但未证明
- 线性区域数对深层网络（>100 层）是否仍然有效？——论文最多验证到 20 cells
- 训练-free 指标能否替代 validation accuracy 做 early stopping？——未探索

### 不该照搬的做法

- **不要在非 cell-based 搜索空间直接用**（如不经过改造用在 NLP 上）
- **不要单用 κN 或单用 ˆRN**——单用会偏向 skip-connect（κN）或 conv（ˆRN）
- **不要跳过 NAS-Bench-201 验证**——先在这个小型 benchmark 上跑通再扩展到 DARTS
- **不要假定训练-free = 零成本**——NTK 计算在 ImageNet 上仍需几小时（只是不训练）

## 可迁移知识

| 知识点 | 迁移到 | 具体做法 |
|--------|--------|---------|
| 训练-free 指标替代 validation | 任何需要快速评估模型质量的场景 | 在初始化时算 κN + ˆRN 作为排序依据 |
| NTK 条件数作为可训练性诊断 | 架构设计 / 初始化策略选择 | 算 κN 判断新设计的架构是否容易训练 |
| Pruning-by-importance 搜索 | 任何大搜索空间的剪枝 | 从 full connectivity 出发逐边剪枝，O(N) 复杂度 |
| 相对排名融合异构指标 | 多指标模型选择 | 不用原始数值，用排名归一化后求和 |
| NAS-Bench-201 作为快速验证 | 新 NAS 方法开发 | 先跑 NAS-Bench-201（查表即可，零评估成本） |

### 特别适用于本知识库领域

- **结构图纸分割模型选择**：如果要在扫描图纸上试多个 backbone（U-Net/PSPNet/HRNet/SegFormer），TE-NAS 思路可快速筛选最有潜力的架构 → [[ronneberger2015-unet-analysis]] [[xie2021-segformer-analysis]]
- **PINN 架构搜索**：PINN 的网络结构选择目前靠经验，NTK 分析可能帮助判断哪种架构对特定 PDE 更"可训练" → [[wang2023-pinn-spurious-analysis]]

## 研究机会

1. **更强的训练-free 指标**：ZiCo（2023）、GradSign（2022）等后续工作已验证有比 κN+ˆRN 更好的指标
2. **TE-NAS for Vision Transformer**：论文限于 CNN，将 NTK 线性区域分析扩展到 Transformer 的 attention 机制
3. **多目标 TE-NAS**：加入延迟/FLOPs/显存约束，同时优化精度和效率
4. **动态 pruning 率**：当前固定剪枝率，可设计自适应剪枝策略
5. **TE-NAS 指导 supernet 训练**：不替代而是辅助——用 κN/ˆRN 决定哪些子网值得训
6. **训练-free 的增量 NAS**：新增算子时不重新搜，仅增量评估

## 关联页面

- [[chen2021-tenas-analysis]] — 全维度总览
- [[chen2021-tenas-method]] — 方法展开
- [[chen2021-tenas-results]] — 实验数据
- [[xie2021-segformer-analysis]] — SegFormer 的架构设计哲学对比
- [[wang2023-pinn-spurious-analysis]] — PINN 训练稳定性与 NTK 分析的潜在关联

## Evidence By Source

### `sources/papers/chen2021-tenas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/TE-NAS_chen2021_ICLR.pdf`

^[sources/papers/chen2021-tenas.md]
