---
id: entities--automl-zero
title: AutoML-Zero
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- entity/dataset
- method/neural-architecture-search
- method/transformer
keywords:
- algorithm-discovery
- automl
- entity/dataset
- evolutionary-search
- genetic-programming
- method/neural-architecture-search
- method/transformer
sources:
- raw/papers/automl_zero_real2020.pdf
created: '2026-06-15'
updated: '2026-07-31'
confidence: high
---

# AutoML-Zero

AutoML-Zero 是 Google Brain 在 ICML 2020 提出的框架，旨在**仅使用基本数学运算作为构建块，通过进化搜索从零自动发现完整的机器学习算法**（包括模型结构、优化方法和初始化策略）。其名称承袭自 AlphaGo Zero——寓意"零人类知识输入"。

## 关键信息

- **类型**: framework / methodology
- **提出**: Esteban Real, Chen Liang, David R. So, Quoc V. Le (Google Brain), 2020
- **发表**: ICML 2020 (PMLR 119)
- **核心贡献**: 证明仅用 65 种高中水平数学操作，进化搜索可以从空程序出发，自动发现神经网络+反向传播、双线性交互、梯度归一化、权重平均等现代 ML 技术，且性能超越人工设计的 2 层神经网络

## 框架架构

### 三组件程序表示

每个 ML 算法被表示为三个组件函数的指令序列：

| 组件 | 职责 | 示例 |
|------|------|------|
| `Setup()` | 初始化权重和学习率等变量 | `m1 = gaussian(0, 0.01)` |
| `Predict()` | 前向推理：输入特征 → 输出预测 | `s1 = dot(v0, v1)` |
| `Learn()` | 根据标签更新可学习参数 | `v1 = v1 + s2*v0` |

三个函数共享全局虚拟内存（标量/向量/矩阵地址空间），按在线 SGD 范式交替执行。

### 搜索空间

- **65 种基础数学操作**：算术、三角函数、指数/对数、向量/矩阵运算、随机生成
- **刻意排除**：ML 概念（loss, batch-norm）、矩阵分解（SVD）、导数
- **极度稀疏**：好的解密度低至 10⁻⁷（线性回归）到 10⁻¹²（完整算法）

### 搜索方法

- **Regularized Evolution**：Tournament selection (T=10) + 三种变异（插入/删除指令、随机化组件、修改参数）
- **分布式并行**：100-1000 workers + 随机迁移 + 功能等价检查 (FEC, 4×加速) + Hurdles (5×加速)
- **Proxy tasks**：低维投影 (F=8~256) 的 CIFAR-10/MNIST 二分类任务上评估

## 关键结果

- **反向传播重发现**：从空程序和教师网络标签数据中，进化独立"发明"了完整的反向传播+梯度下降
- **CIFAR-10 精度**：进化算法 84.06% vs 2层神经网络 82.22%
- **跨数据集泛化**：在 SVHN, ImageNet (downsampled), Fashion MNIST 上一致超越基线
- **技术自发涌现**：双线性乘法交互、梯度归一化、权重累积平均、Noisy ReLU、学习率衰减
- **任务自适应**：数据稀缺→Noisy ReLU (dropout-like)，快速训练→学习率衰减，多分类→自适应学习率

## 关联页面

- [[real2020-automl-zero-analysis]] — 完整 12 维度论文分析
- [[real2020-automl-zero-method]] — 三组件程序表示 + 进化引擎详解
- [[real2020-automl-zero-results]] — 实验数据与涌现技术分析
- [[real2020-automl-zero-critical]] — 贡献 / Negative Knowledge / 研究机会
- [[te-nas]] — training-free NAS：用零成本指标替代训练评估，可能加速 AutoML-Zero
- [[primer]] — PRIMER：同样用进化搜索发现 Transformer 架构
- [[nasbench201]] — NAS 基准数据集，可用于对比 AutoML-Zero 与传统 NAS 的搜索难度

## Evidence By Source

### `raw/papers/automl_zero_real2020.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/automl_zero_real2020.pdf]
