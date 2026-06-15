---
title: "AZ-NAS"
created: 2026-06-15
updated: 2026-06-15
type: entity
tags: [training-free-nas, neural-architecture-search, zero-cost-proxy, ensemble-method, nas-method]
sources: [raw/papers/aznas_lee2024.pdf]
confidence: high
---

# AZ-NAS (Assembling Zero-Cost Proxies for NAS)

> Lee & Ham (2024) — Yonsei University & KIST — arXiv:2403.19232
> **集成式训练-free NAS**：4 种互补零成本代理 + 非线性排序聚合 → NAS-Bench-201 Kendall τ = 0.741

## 关键信息

| 项目 | 内容 |
|------|------|
| **全称** | AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search |
| **类型** | NAS method / Zero-Cost Proxy Ensemble |
| **作者** | Junghyup Lee, Bumsub Ham (Yonsei University, KIST) |
| **发表** | 2024 (arXiv:2403.19232) |
| **代码** | https://github.com/cvlab-yonsei/AZ-NAS |
| **核心贡献** | 首次系统性地提出"组装互补零成本代理"的训练-free NAS 范式；4 个新颖代理（表达力/渐进性/可训练性/复杂度）+ 非线性排序聚合 |

## 核心机制

### 四大零成本代理

| 代理 | 符号 | 评估维度 | 计算方式 | 输入 |
|------|------|---------|---------|------|
| **Expressivity** | sE | 特征空间各向同性（维度利用率） | PCA 特征值的熵 | 前向激活 |
| **Progressivity** | sP | 深度方向特征空间扩展的单调性 | min(相邻 block sE 差) | 前向激活（复用 sE） |
| **Trainability** | sT | 梯度传播稳定性 | Hutchinson 近似的 Jacobian 谱范数 | 反向梯度 |
| **Complexity** | sC | 计算资源利用率 | FLOPs | 架构定义 |

**关键特性**：所有代理分数在**单次前向+反向传播**内同时计算，42.7 ms/arch，无需特殊架构修改（不删 BN、不要求 ReLU、不限制非参数操作）。

### 非线性排序聚合

```
sAZ(i) = Σ_{M∈{E,P,T,C}} log(Rank(sM(i)) / m)
```

对数函数使低排名代理受到不成比例的惩罚——避免高排名代理"平均掉"低排名代理的警告。遵循"木桶效应"直觉。

### 搜索流程

1. 进化搜索（Algorithm 1）初始化 → 每轮评估 4 代理 → 非线性聚合 → 从 top-k 变异 → 迭代 → 选历史最高分
2. 代理排名基于**所有历史累积架构**的全局排序（随搜索推进越来越稳定）

## 关键性能

| 搜索空间 | 数据集 | 指标 | AZ-NAS | 最佳对比方法 |
|---------|--------|------|--------|------------|
| NAS-Bench-201 | CIFAR-10 | Kendall τ | **0.741** | GradSign 0.618 |
| NAS-Bench-201 | CIFAR-100 | Kendall τ | **0.723** | GradSign 0.594 |
| NAS-Bench-201 | IN16-120 | Kendall τ | **0.710** | ZiCo 0.584 |
| MobileNetV2 | ImageNet (450M) | Top-1 Acc | **78.6%** | ZiCo 78.1% |
| MobileNetV2 | ImageNet (600M) | Top-1 Acc | **79.9%** | ZiCo 79.4% |
| MobileNetV2 | ImageNet (1000M) | Top-1 Acc | **81.1%** | ZenNAS 80.8% |
| AutoFormer Tiny | ImageNet | Top-1 Acc | **76.4%** | TF-TAS 75.3% |
| AutoFormer Small | ImageNet | Top-1 Acc | **82.2%** | AutoFormer 81.7% |

搜索成本：NAS-Bench-201 ~42.7 ms/arch；MobileNetV2 ~0.4-0.7 GPU天；AutoFormer ~0.03-0.17 GPU天。

## 与其他 NAS 方法的关系

### vs [[te-nas]]（TE-NAS）
- TE-NAS 是 AZ-NAS 之前**唯一**使用双代理的训练-free NAS（线性区域数 + NTK 条件数）
- 区别：TE-NAS 的双代理计算成本极高（1311.8 ms/arch，NTK 是瓶颈），且线性区域计数只支持 ReLU。AZ-NAS 的 4 代理只有 42.7 ms/arch，不要求 ReLU
- TE-NAS 的排序聚合是**线性求和**，AZ-NAS 证明非线性 log-Rank 聚合显著更优

### vs [[eznas]]（EZNAS）
- EZNAS 用**遗传编程自动发现**零成本代理；AZ-NAS 用**手工设计**互补代理
- 互补性：EZNAS 发现的代理可能具有互补性（因为进化过程自然选择多样化的程序），但 EZNAS 的适应度是"最低 Kendall τ 最大化"——与 AZ-NAS 的"低排名惩罚"共享了"木桶效应"直觉
- EZNAS 可以使用 AZ-NAS 的非线性聚合来组合它的进化池中的多个高分程序

### vs [[training-free-nas-transformers]]
- 该工作将训练-free NAS 扩展到 RNN 和 BERT Transformer
- AZ-NAS 同样扩展到了 ViT（AutoFormer），但发现 sP 代理对 attention 架构失效
- 该工作的 hidden covariance 指标（基于隐藏状态协方差）与 AZ-NAS 的 sE（基于 PCA 特征熵）在"分析特征空间结构"上有共享的思路，但具体实现不同

### vs [[nago]]（NAGO）
- NAGO 是基于贝叶斯优化的训练式 NAS 框架（不同范式）
- NAGO 优化的是"网络生成器"而非单架构——AZ-NAS 优化的是单架构，但进化搜索的"历史集合排名"与 NAGO 的 surrogate model 有功能类比

### 与训练-based NAS 的关系
- AZ-NAS 在 MobileNetV2 上以 ~0.5 GPU天超越了需要 50 GPU天的 OFA（one-shot training）——证明训练-free NAS 在特定场景下已经实用
- AZ-NAS 代理可以作为**其他 NAS 方法的插件**——论文 Table 5 证明融入 ZiCo/Synflow 后 τ 提升 0.16-0.20

## 已知局限

1. **sP 对 ViT 失效**：attention 用高斯噪声输入时 token 间注意力值相似 → 块间特征空间不可靠区分 → 需要为 ViT 设计专用渐进性代理
2. **仅评估初始化行为**：所有代理用高斯随机输入 → 完全无法捕捉网络对真实数据分布的适配倾向
3. **Jacobian 线性近似误差**：sT 将 primary block 近似为线性系统 → 对非线性强的 block 可能不准确（论文未量化误差）
4. **sC 代理效果**：FLOPs 单独 τ=0.517-0.578 在 NAS-Bench-201 上已相当高——部分 AZ-NAS 效果可能来自 FLOPs 而非所有 4 代理的创新

## 关联页面

- [[lee2024-aznas-analysis]] — 完整 12 维度论文分析
- [[lee2024-aznas-method]] — 方法机制详解
- [[lee2024-aznas-results]] — 实验证据详解
- [[lee2024-aznas-critical]] — 贡献 / 失败知识 / 研究机会
- [[te-nas]] — TE-NAS：双代理训练-free NAS
- [[eznas]] — EZNAS：遗传编程自动发现零成本代理
- [[training-free-nas-transformers]] — 训练-free NAS 在 RNN/Transformer 上的探索
- [[nasbench201]] — NAS-Bench-201 基准数据集
- [[nago]] — NAGO：贝叶斯优化 NAS 框架
