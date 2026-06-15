---
title: "NAGO (Neural Architecture Generator Optimization)"
created: 2026-06-15
updated: 2026-06-15
type: entity
tags: [method, neural-architecture-search, bayesian-optimization, nas-framework]
sources: [raw/papers/nago_ru2020.pdf]
confidence: high
---

# NAGO (Neural Architecture Generator Optimization)

Ru et al. (NeurIPS 2020) 提出的神经架构搜索框架，将 NAS 从"搜索单个最优架构"重新定义为"搜索最优网络生成器"。通过层次化图搜索空间 HNAG + 贝叶斯优化，在 6 个视觉 benchmark 上达到 SOTA。

## 关键信息

- **类型**: NAS 方法 / 框架
- **作者**: Binxin Ru (Oxford), Pedro M. Esperança, Fabio M. Carlucci (Huawei Noah's Ark Lab)
- **发表**: NeurIPS 2020 (arXiv: 2004.01395)
- **代码**: https://github.com/ruoa/nago（实际 repo: `rubinxin/vega_NAGO`）
- **核心贡献**: 范式转换——优化网络生成器而非单架构；HNAG 层次化图搜索空间；异方差 BNN + BOHB/MOBO 搜索策略

## 核心组成

### HNAG（层次化图搜索空间）
三级层次随机图模型：
- **顶层**：Watts–Strogatz 图 → stage 间连接（允许跨 stage 信息流）
- **中层**：Erdős–Rényi 图 → cell 内节点连接
- **底层**：Watts–Strogatz 图 → 原子操作连接

仅 8 个连续超参数表达 > 4.58×10⁵⁶ 种架构。

### 搜索策略
- **BOHB**：多保真度贝叶斯优化（低 epoch 淘汰差配置）
- **MOBO**：多目标贝叶斯优化（精度 + 内存 Pareto 前沿）+ 异方差 BNN 代理模型 + 并行批次评估

## 关键性能

| 数据集 | HNAG-BOHB 精度 | HNAG-MOBO 精度 | HNAG-MOBO 内存 |
|--------|---------------|---------------|---------------|
| CIFAR-10 | 96.6% | 96.6% | 12.8MB |
| CIFAR-100 | 79.3% | 77.6% | 12.8MB |
| ImageNet | 76.8% (Top-1) | — | — |
| FLOWERS102 | 97.9% | 98.1% | 48.4MB |

仅使用 Cutout（不用 DropPath/Auxiliary Towers），超越多数 SOTA NAS 方法。

## 与其他实体的关系

- 继承 [[randomly-wired-networks]] (Xie et al., 2019) 的网络生成器概念，但首次提供系统优化方法
- 比 DARTS 等 [[cell-based-nas]] 方法搜索空间更广（4.58×10⁵⁶ vs 4.40×10¹²），不以 weight-sharing 为代价
- 与 [[bossnas]] (Li et al., 2021) 形成互补——BossNAS 用 block-wise search + self-supervised proxy，NAGO 用 BO + generator optimization
- 与 [[te-nas]] (Chen et al., 2021) 形成"低价 vs 高质"的两极——TE-NAS 追求极低搜索成本（4 GPU 小时），NAGO 追求更全面的搜索（~15 GPU-days）
- 可看作 [[training-free-nas-transformers]] 的对立面：NAGO 坚持 sample-based evaluation，反对 weight-sharing 的偏差

## 关联页面

- [[ru2020-nago-analysis]] — 完整论文分析
- [[ru2020-nago-method]] — HNAG + BO 方法细节
- [[ru2020-nago-results]] — 完整实验结果
- [[ru2020-nago-critical]] — 贡献 · 局限 · 延伸分析
