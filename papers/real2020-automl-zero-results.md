---
id: papers--real2020-automl-zero-results
title: Real et al. (2020) — 实验结果详解：进化发现的算法与技术涌现
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
keywords:
- algorithm-discovery
- backpropagation
- cifar-10
- emergent-techniques
- evolutionary-search
sources:
- sources/papers/real2020-automl-zero.md
created: '2026-06-15'
updated: '2026-07-31'
confidence: high
reproducibility: high
---

# AutoML-Zero 实验结果详解

> 实验分三个阶段递进：(4.1) 在受控空间中验证进化搜索的必要性，重发现神经网络+反向传播；(4.2) 在最小人类偏见下搜索完整算法，与人工设计基线对比；(4.3) 验证算法的任务自适应能力。

## 6.1 Section 4.1：在困难空间中寻找简单神经网络

### 6.1.1 实验动机

验证 AutoML-Zero 搜索空间的固有难度，并证明 evolution 相比 random search 的优势随难度增长而加大。

### 6.1.2 实验设置

- **任务**：线性/仿射回归（8维随机生成数据）
- **搜索空间限制**：仅使用必要操作，固定组件函数长度（如线性 SGD 需 4 条 Learn 指令）
- **成功标准**：RMS 误差低于人工设计参考（线性回归器或神经网络）
- **难度量化**：RS 成功率的倒数（即找到 1 个可接受解所需的评估次数）

### 6.1.3 核心发现

| 任务类型 | RS 成功率（难度） | Evolution 相对 RS 的效率 |
|----------|-------------------|-------------------------|
| 线性回归 (learning only) | 10⁻⁷ | 2.9× |
| 线性回归 (full algorithm) | 10⁷ | 5.6× |
| 仿射回归 (learning only) | 10⁹ | 150× |
| 仿射回归 (full algorithm) | 10¹² | 23,000× |

**关键趋势**（Figure 4）：随着任务难度从 10⁷ 增长到 10¹²，evolution/RS 效率比从 2.9 飙升到 23,000。这解释了为什么在传统 AutoML 空间中 RS 常与进化竞争（密度高），但在 AutoML-Zero 的稀疏空间中 evolution 不可或缺。

### 6.1.4 反向传播重发现

当任务从线性升级到非线性（教师网络：ReLU(Mx)）且使用多个任务（D=100）时：

- **D=1**：进化直接 hard-code 教师网络的权重（过拟合单个任务）
- **D=100**：进化必须学会从数据中学习——结果**自动"发明"了完整的反向传播 + 梯度下降代码**（Figure 5）

重发现算法（简化注释后）：

```python
# Setup: 初始化权重和学习率
m1 = gaussian(-1e-10, 9e-09)   # 第一层权重
s3 = 4.1                         # 学习率
v4 = gaussian(-0.033, 0.01)     # 第二层权重

# Predict: 前向传播
v6 = dot(m1, v0)                 # 第一层线性变换
v7 = maximum(0, v6)              # ReLU 激活
s1 = dot(v7, v4)                 # 第二层线性输出

# Learn: 反向传播
v3 = heaviside(v6, 1.0)          # ReLU 导数
s1 = s0 - s1                     # 计算误差
s2 = s1 * s3                     # 学习率缩放
v2 = s2 * v3                     # 第二层权重增量
v3 = v2 * v4                     # 反向传播梯度
m0 = outer(v3, v0)               # 第一层权重梯度
m1 = m1 + m0                     # 更新第一层权重
v4 = v2 + v4                     # 更新第二层权重
```

**意义**：这是在仅给定输入-标签对、无任何梯度/损失函数概念的情况下，**从零进化出的完整反向传播实现**。

## 6.2 Section 4.2：最小人类偏见下的完整算法搜索

### 6.2.1 实验设置

- **任务**：CIFAR-10 二分类（45 个 class pairs → 36 个用于搜索，9 个用于选择，测试集用于最终评估）
- **搜索空间**：全部 65 种操作可用，组件函数长度可变
- **规模**：W=10k workers
- **对比基线**：线性模型（逻辑回归）和 2 层全连接网络（均使用同等总计算量调参）

### 6.2.2 进化过程发现

Figure 6 展示了进化过程中的关键 stepping-stone 发现：

```
空程序 → 线性模型(无SGD) → 线性模型(有缺陷SGD) → Loss Clipping
→ 线性模型(完整SGD) → 随机学习率 → 更好的超参数
→ 梯度/输入范数归一化 → Hard-coded LR → ReLU
→ 随机权重初始化 → 梯度归一化
→ 乘法交互(有缺陷SGD) → 乘法交互(完整SGD) → 最佳进化算法
```

### 6.2.3 最佳进化算法的技术特征

最终进化出的算法（Figure 6 流程图）包含四项关键技术：

1. **输入噪声注入**（正则化）：
   ```
   a = x + u;  b = x - u;  u ~ Uniform(α, β)
   ```
   向输入添加随机噪声，类似 Dropout/Noisy ReLU 的变体。

2. **双线性乘法交互** (multiplicative interactions)：
   ```
   o = aᵀWb
   ```
   比标准线性变换 o=wᵀx 更强的表达能力，Jayakumar et al. (2020) 近期才系统研究此技术。

3. **梯度归一化**（优化稳定性）：
   ```
   ĝ = g / ||g||;  g = δ·a·bᵀ;  δ = y* - y
   ```
   梯度被归一化为单位向量后用于更新，这是非凸优化中的常见启发式 (Hazan et al., 2015; Levy, 2016)。

4. **权重累积平均**（训练/推理不一致）：
   ```
   W' = Σₜ Wₜ  （推理时使用）
   ```
   训练时使用当前权重 Wₜ，推理时使用所有训练步权重的累加 W'。类似 averaged perceptron (Collins, 2002) 和 Polyak averaging (Polyak & Juditsky, 1992)。通过在 Predict 末尾将 W 设为 W'、Learn 开头恢复 Wₜ 实现——训练时 Predict↔Learn 交替执行无影响，验证时只有 Predict 使得 W 保持为 W'。

### 6.2.4 多数据集性能

| 数据集 | 最佳进化算法 | 线性基线 | 非线性基线 (2层NN) |
|--------|-------------|---------|-------------------|
| **CIFAR-10 (test)** | **84.06 ± 0.10%** | 77.65 ± 0.22% | 82.22 ± 0.17% |
| **SVHN** | **88.12%** | 59.58% | 85.14% |
| **ImageNet (downsampled)** | **80.78%** | 76.44% | 78.44% |
| **Fashion MNIST** | **98.60%** | 97.90% | 98.21% |

**关键结论**：进化算法在全部四个数据集上超越两种人工设计基线，且优势在不同数据集间一致。

### 6.2.5 搜索实验重复性

在 20 次独立搜索实验中，进化候选算法在 held-out Tselect 上的表现**13 次优于 2 层神经网络基线**，展示了方法的统计可靠性。

## 6.3 Section 4.3：算法任务自适应机制

### 6.3.1 实验设计

以 Figure 5 的神经网络算法为初始化种群，在三种不同条件的任务上继续进化：

- **小样本**：80 个训练样本/100 epochs
- **快速训练**：800 个样本/10 epochs
- **多分类**：CIFAR-10 全部 10 类

每种条件运行 30 次独立实验 + 30 次对照实验。

### 6.3.2 自适应发现1：Noisy ReLU（数据增强/正则化）

**条件**：小样本（80 样本）

**涌现行为**（Figure 7a）：
```
v6 = dot(m1, v0)          # 线性变换
v8 = gaussian(-0.5, 0.41) # 随机噪声
v6 = v6 + v8              # 注入噪声
v7 = maximum(v9, v6)      # ReLU (v9≈0)
```

**统计显著性**：实验组 8/30 次出现，对照组（800 样本）0/30 次出现，p < 0.0005。

**解释**：进化自动发现类似于 Noisy ReLU (Nair & Hinton, 2010) 和 Dropout (Srivastava et al., 2014) 的随机正则化技术——仅在数据稀缺时出现。

### 6.3.3 自适应发现2：学习率衰减

**条件**：快速训练（10 epochs）

**涌现行为**（Figure 7b）：
```python
# Setup
s2 = 0.37               # 初始学习率

# Learn
s2 = arctan(s2)         # 每次更新后衰减学习率
```

迭代应用 arctan 产生近似指数衰减的学习率调度。衰减曲线显示：从 log(0.37)≈-1 到约 log(10⁻⁴)≈-9 的平滑下降。

**统计显著性**：实验组 30/30 次出现，对照组（100 epochs）3/30 次出现，p < 10⁻¹⁴——几近确定性的自适应行为。

### 6.3.4 自适应发现3：基于权重的自适应学习率

**条件**：多分类（10 类）

**涌现行为**（Figure 7c）：
```python
s3 = mean(m1)          # 权重矩阵均值
s3 = abs(s3)           # 取绝对值
s3 = sin(s3)           # sin 变换
# s3 被用作学习率
```

**统计显著性**：实验组 24/30 次出现，对照组（二分类）0/30 次出现，p < 10⁻¹¹。

**解释**：论文作者坦言"不知原因"，但这种模式在统计上极其显著，可能与多分类任务的权重规模调整有关。

### 6.3.5 自适应机制总览

| 任务挑战 | 涌现技术 | 本质 | 出现率 (实验 vs 对照) | p-value |
|----------|---------|------|---------------------|---------|
| 数据稀缺 | Noisy ReLU | 随机正则化/数据增强 | 8/30 vs 0/30 | < 0.0005 |
| 快速收敛 | 学习率衰减 | 优化调度 | 30/30 vs 3/30 | < 10⁻¹⁴ |
| 多分类 | 权重均值→学习率 | 自适应步长 | 24/30 vs 0/30 | < 10⁻¹¹ |

## 6.4 消融实验 (Section 5)

Figure 8 展示了搜索方法各组件的消融效果：

| 配置 | 最佳精度 (CIFAR-10) |
|------|---------------------|
| Base (单 worker, 无优化) | 0.69 |
| + Migration | 0.76 |
| + FEC | 更高 |
| + MNIST 多样性 | 更高 |
| + Hurdles (完整配置) | 最高 |

四项升级均对搜索质量有正向贡献——所有技术缺一不可。

## 关联页面

- [[real2020-automl-zero-analysis]] — 完整 12 维度论文分析
- [[real2020-automl-zero-method]] — 方法机制详解
- [[real2020-automl-zero-critical]] — 贡献 / 知识点 / Negative Knowledge
- [[automl-zero]] — 实体页

## Evidence By Source

### `sources/papers/real2020-automl-zero.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/automl_zero_real2020.pdf`

^[sources/papers/real2020-automl-zero.md]
