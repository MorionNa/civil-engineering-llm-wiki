---
id: papers--akhauri2022-eznas-method
title: EZNAS 方法机制 — 遗传编程驱动零成本 NAS 代理自动发现
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/neural-architecture-search
keywords:
- evolutionary-algorithm
- expression-tree
- genetic-programming
- kendall-tau
- training-free-nas
- zero-cost-proxy
sources:
- sources/papers/akhauri2022-eznas.md
created: '2026-06-15'
updated: '2026-07-31'
confidence: high
parent: akhauri2022-eznas-analysis
---

# EZNAS 方法机制详解

> 核心问题：如何用遗传编程自动发现一个**可解释、可泛化**的零成本 NAS 评分程序？

## 5.1 程序表示：表达式树 (Expression Tree)

### 为什么需要表达式树？

EZNAS 的初始尝试使用类似 [[automl-zero]] 的**顺序指令 + 内存地址**表示——程序是一系列 4 元组指令（写地址、操作 ID、读地址 1、读地址 2），有 22 个静态内存地址（网络统计量）+ 80 个动态地址（中间张量）。

**问题**：这种表示导致程序长度膨胀和大量冗余计算——许多指令对最终输出毫无贡献，评估速度极慢。

**解决方案**：强制使用**表达式树结构**——根节点是最终输出，中间节点是数学运算，终端节点（叶子）是网络统计量。这保证每个操作都对输出有贡献 → 无冗余 → 进化可追踪。

```
         [to_scalar: Mean]
              |
        [aggregation: Mean across all RCB instances]
              |
         [运算: e.g., Sum, Product, CosSim, ...]
            /          \
     [运算: Abs]    [终端: T4GD]
        /
   [终端: T3GN]
```

### 程序应用流程

表达式树对网络的**每一个 RCB 实例**独立应用（22 个终端节点对应该实例的 22 个统计量），每个 RCB 输出一个标量 → 所有实例的结果通过 `aggregation_function`（Mean）聚合 → 得到最终评分。

关键简化：表达式树只有 22 个可能的终端输入（而非 22 × 100+ RCB 实例 = 2200+），大幅降低搜索空间。

## 5.2 网络统计量采集 (Neural Network Statistics)

对每个采样架构，识别所有 ReLU-Conv2D-BatchNorm2D (RCB) 实例，用**三种类型的输入**做一次前向/反向传播：

| 输入类型 | 符号 | 含义 |
| ---------|------|------|
| Data | D | 数据集中的一个 mini-batch |
| Noise | N | 纯随机噪声张量 `torch.randn(shape)` |
| Perturbed | P | 数据 + 噪声扰动 `data + √0.01 × randn(shape)` |

对每个 RCB 实例采集 22 个张量：

| 张量 | 说明 | 受输入类型影响？ |
|------|------|:---:|
| T1, T2 | ReLU 前后的激活 | ✅ (×3) |
| T3 | Conv2D 权重 | ❌ (×1) |
| T4 | Conv2D 输出激活 | ✅ (×3) |
| T1G, T2G | ReLU 前后激活梯度 | ✅ (×3) |
| T3G | Conv2D 权重梯度 | ✅ (×3) |
| T4G | Conv2D 输出激活梯度 | ✅ (×3) |

总计：10 个（激活类）+ 12 个（梯度类）= 22 个张量/RCB 实例。

论文在附录验证了 Conv2D-BatchNorm2D-ReLU (CBR) 替代结构也有效，证明框架不限于 RCB 顺序。

## 5.3 数学操作空间

34 种数学操作，涵盖四个层次：

| 类别 | 操作 | 数量 |
|------|------|:---:|
| **基础运算** | Sum, Difference, Product, MatMul, Abs, Power(²), Exp, Log, AbsLog, Normalize, Sign, Heaviside, ReLU, Softmax, Sigmoid, Element-wise Invert, Greater Than, Less Than, Equal To, Greater Than Zero, Less Than Zero | 21 |
| **范数/缩减** | Frobenius Norm, L1 Norm, Normalized Sum, Number of Elements | 4 |
| **线性代数** | Determinant, LogDeterminant, SymEigRatio, EigRatio | 4 |
| **相似度/距离** | Cosine Similarity, Hamming Distance, KL Divergence | 3 |
| **占位** | Ones Like, Zeros Like | 2 |

关键设计选择：**所有操作均无可调标量超参数**——Power 固定为平方，噪声固定为 N(0,1)。这是一种简化，但论文指出未来可动态优化这些参数。

## 5.4 进化搜索算法

### 算法流程

```
Algorithm: EZNAS Search
1. evol_space = {从 NDS/NAS-Bench-201 中选取的搜索空间}
2. population = 随机生成 n 个有效程序（n=50）
3. 评估 population 适应度（Kendall τ）
4. for generation = 1 to 15:
5.     offspring = []
6.     while |offspring| < n/2:      // 25 个
7.         children = VarOr(population)  // 交叉/突变/繁殖
8.         offspring.append(valid(children))
9.     offspring.append(random_valid(n/2))  // 25 个随机新个体
10.    population = evaluate(offspring)
```

### 关键超参数

| 参数 | 值 |
|------|:--:|
| 代数 (T) | 15 |
| 种群大小 (n) | 50 |
| 锦标赛大小 | 4 |
| MU (父代选择数) | 25 |
| Lambda (子代产生数) | 50 |
| 交叉概率 | 0.4 |
| 突变概率 | 0.4 |
| 树深度范围 | 2-10 |

### 变异操作 (VarOr)

DEAP 框架提供三种变异，每次生成 ⌊n/2⌋ 个有效后代：

1. **交叉 (Crossover)**：随机选两个个体 → 各选一个交叉点 → 交换子树 → 保留第一个孩子
2. **突变 (Mutation)**：随机选一个点 → 用随机生成的子树替换
3. **繁殖 (Reproduction)**：直接从种群中复制（保持精英）

变异循环直到 ⌊n/2⌋ 个**有效**个体生成（有效 = 执行时不产生 inf/nan/error）。

另外 ⌊n/2⌋ 个个体完全随机生成 → 维持多样性。

## 5.5 抗过拟合的适应度评估

### 核心问题

如果固定用一个小子集评估适应度 → 程序迅速过拟合到该子集。

如果评估完整数据集（~1TB 网络统计量） → 计算不可行。

### 解决方案：演化任务数据集 (Evolution Task Dataset)

每个 generation 重新：
1. 随机选择 s=4 个搜索空间（从 NDS + NAS-Bench-201 中）
2. 每个空间随机采样 20 个架构
3. 计算程序在 4 个空间上的 Kendall τ
4. **取最差值作为适应度**：`fitness = min(τ₁, τ₂, τ₃, τ₄)`

→ min 策略强制程序在所有空间上都表现好 → **跨空间泛化**。

### 测试阶段

从最终种群选 fittest + 整个演化史中最 fit 的两个个体 → 在 NAS-Bench-201 全量 15,625 架构和 NDS ~5,000 架构上评估。

## 5.6 EZNAS-A 的发现与分析

EZNAS-A 仅在 **NDS-DARTS CIFAR-10** 上进化发现，其结构：

- **输入**：T3GN（随机噪声下的 Conv2D 权重梯度）
- **本质**：加权参数计数——得分随输入/输出通道数**非线性单调递增**，对不同 kernel size 有非对称偏好（1×1 和 7×7 得分高，3×3 得分最低）

```
预期得分 = f(channels_in) · g(channels_out) · h(kernel_size)
其中 f, g 为单调递增，h 为以 kernel=3 为谷底的抛物线
```

这解释了为什么 EZNAS-A 在跨空间上泛化好——它捕捉的是"参数容量"这个普遍的架构质量信号，但比纯 FLOPs/Params 更精细（考虑了非线性的 kernel size 效应和通道的加权方式）。

## 5.7 与已有 ZC-NASM 的程序表示对比

论文 Figure 2 展示了现有 ZC-NASM 均可表示为表达式树：

- **synflow**：`sum(|T3GD × T3D|)` — 权重梯度 × 权重 的绝对值求和
- **SNIP**：`sum(|T3GD × T3D|)` on data input — 与 synflow 类似但仅用数据输入
- **FISHER**：`sum(T3GD²)` — 权重梯度的平方和

→ 这些手工设计的指标都是 EZNAS 程序空间的**特例**。EZNAS 能自动发现它们，还能发现更复杂的组合。

## 关联页面

- [[akhauri2022-eznas-analysis]] — 论文分析总览
- [[akhauri2022-eznas-results]] — 完整实验结果
- [[akhauri2022-eznas-critical]] — 批判性分析
- [[eznas]] — EZNAS 实体
- [[te-nas]] — TE-NAS（NTK 条件数 + 线性区域数的手工零成本指标）

## Evidence By Source

### `sources/papers/akhauri2022-eznas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/eznas_akhauri2022.pdf`

^[sources/papers/akhauri2022-eznas.md]
