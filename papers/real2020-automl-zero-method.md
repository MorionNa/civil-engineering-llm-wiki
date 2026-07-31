---
id: papers--real2020-automl-zero-method
title: Real et al. (2020) — 方法详解：AutoML-Zero 的三组件搜索空间与进化引擎
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
keywords:
- evolutionary-search
- functional-equivalence-checking
- genetic-programming
- regularized-evolution
sources:
- sources/papers/real2020-automl-zero.md
created: '2026-06-15'
updated: '2026-07-31'
confidence: high
reproducibility: high
---

# AutoML-Zero 方法机制详解

> 本章从搜索空间、进化引擎、评估基础设施三个维度展开 AutoML-Zero 的方法设计。

## 5.1 搜索空间：三组件程序表示

### 5.1.1 总体架构

AutoML-Zero 将每个机器学习算法表示为一个**包含三个组件函数的计算机程序**：

| 组件函数 | 职责 | 调用时机 |
|----------|------|----------|
| `Setup()` | 初始化内存变量（权重、超参数等） | 训练开始前，执行一次 |
| `Predict()` | 根据输入特征 x 产生预测 | 每个样本的训练/验证/测试时 |
| `Learn()` | 根据 label y 更新可学习参数 | 每个训练样本的 Predict 之后 |

三个函数共享一个**全局虚拟内存**，包含三个独立地址空间：
- **标量** (s0, s1, s2, ...)：单个浮点数
- **向量** (v0, v1, v2, ...)：维度为 F（输入特征维度）的浮点向量
- **矩阵** (m0, m1, m2, ...)：F×F 的浮点矩阵

所有内存初始化为零，且在训练/验证全过程中保持持久。

### 5.1.2 程序执行协议

如图 1（伪代码）所示，算法的评估过程为：

```
训练阶段（对 Dtrain 中每个样本 (x, y)）：
  v0 = x          # 输入特征写入向量地址0
  Predict()       # 执行预测指令
  s1 = Normalize(s1)  # s1 被解释为预测输出，归一化到概率
  s0 = y          # 标签写入标量地址0
  Learn()         # 执行学习指令

验证阶段（对 Dvalid 中每个样本 (x, y)）：
  v0 = x
  Predict()       # 仅 Predict，不 Learn
  s1 = Normalize(s1)
  sum_loss += Loss(y, s1)
```

关键设计：`Predict()` 仅接收特征 x，标签 y 仅在 `Learn()` 中可见——这强制算法必须通过内存变量在 Predict 和 Learn 之间传递信息，模拟了真正的监督学习流程。`s1` 是"约定输出地址"——Predict 可以将任意值写入 s1，评估器将其归一化为分类概率。

### 5.1.3 指令集：65 种基础数学操作

为最小化人类偏见，操作选择的标准是**"高中水平数学"**，刻意排除：
- ❌ 机器学习概念（loss、gradient、batch-norm）
- ❌ 矩阵分解（SVD、Eigendecomposition）
- ❌ 导数计算

包含的操作类别（完整列表见 Suppl. Section S2）：
- **基本算术**：+、−、×、÷、幂、开方
- **三角函数**：sin、cos、tan、arctan
- **指数/对数**：exp、log
- **比较/逻辑**：>、<、=、max、min、sign、heaviside
- **向量/矩阵运算**：dot product、outer product、matrix-vector 乘法
- **统计/规约**：mean、sum、norm、abs
- **随机生成**：gaussian(μ, σ)、uniform(a, b)
- **内存操作**：copy、swap

每条指令格式：`output_address = op(arg1, arg2, ...)`，操作类型和参数地址都是搜索变量。

### 5.1.4 搜索空间的通用性与稀疏性

该空间极其通用——不假设神经网络结构、不假设梯度存在、不假设损失函数形式，理论上可以表示线性模型、神经网络、决策树、kNN 等任意算法。

代价是**极高的稀疏性**：在"发现可学习线性回归的算法"这一简单任务上，好的解仅占搜索空间的 10⁻⁷。对于更复杂的问题（如 Learn 组件中同时发现前向+反向传播），稀疏度可达 10⁻¹²。

## 5.2 进化搜索引擎

### 5.2.1 Regularized Evolution

搜索采用 **regularized evolution**（Real et al., 2019），这是一个简化的稳态遗传算法：

**种群**：P 个算法（初始全部为空程序——三个组件函数均无指令）

**每轮循环**（Figure 2）：
1. **移除最老算法**（保持种群新鲜度/正则化效果）
2. **Tournament selection**：随机选 T=10 个算法，选适应度最高者为 parent
3. **复制 parent** → child
4. **变异 child**
5. 将 child 加入种群

**适应度**：算法在 D 个搜索任务上的分类精度中位数。使用中位数而非均值是为了对异常任务鲁棒。

### 5.2.2 三种变异操作

从 parent 生成 child 时，随机选择一种变异（Figure 3）：

| 变异类型 | 操作 | 影响 |
|----------|------|------|
| **插入/删除指令** | 在随机组件的随机位置插入一条随机指令，或删除一条随机指令 | 改变程序长度和功能 |
| **随机化组件函数** | 将一个组件函数的所有指令替换为随机指令 | 大幅度探索 |
| **修改参数** | 替换一条指令的某个参数（输出地址、输入地址、或常数值） | 微调现有功能 |

变异概率 U=0.9（即 10% 的 child 不与 parent 不同）。

### 5.2.3 大规模并行基础设施

为达到 2k–10k 算法/秒/CPU 核的吞吐量，采用：

| 技术 | 机制 | 加速 |
|------|------|------|
| **Migration** | W 个 worker 进程（100–1000），各有独立 P 大小种群；定期随机交换算法 | 线性并行 |
| **FEC** (Functional Equivalence Checking) | 记录算法在固定 10 样本×10 步训练后的预测→哈希为指纹；相同指纹=功能性等价→复用评估分数 | ~4× |
| **Hurdles** | 先用少量样本/少步数快速筛选，仅通过者进行完整评估 | ~5× |
| **Proxy tasks** | 用随机投影矩阵降维（F=8~256），替代全维 CIFAR-10 评估 | ~10-100× |

### 5.2.4 多样性增强

半数 worker 在投影 CIFAR-10 上搜索，半数在投影 MNIST 上搜索——不同数据源的算法通过 migration 混合，增加种群多样性。

### 5.2.5 超参设计哲学

大多数超参**未在最终全规模实验上调参**：P 从早期小实验决定，T 从先前工作取用，不确定的参数使用范围值（如 100 ≤ P ≤ 1000），不同 worker 在范围内取不同值。

## 5.3 评估与选择协议

### 5.3.1 搜索阶段

- **Tsearch**：用于进化搜索的任务集（如 36 个 CIFAR-10 二分类 pairs）
- 每个 worker 在每轮评估中随机抽取 1 ≤ D ≤ 10 个任务评估算法
- 适应度 = 这些任务上的精度中位数

### 5.3.2 模型选择阶段

- **Tselect**：搜索结束后，用 held-out 任务集（如 9 个未见的 CIFAR-10 pairs）评估搜索得到的候选算法
- 选择在 Tselect 上表现最好的算法

### 5.3.3 最终评估阶段

- 在原始维度 CIFAR-10 上（F=3072，非投影）用测试集评估
- 将所有常数视为超参数，通过随机搜索调参后比较
- 对线性基线和神经网络基线使用**同等总计算量**调参

## 5.4 方法流程总览

```
┌─────────────────────────────────────────────────────────┐
│                    AutoML-Zero 搜索流程                    │
├─────────────────────────────────────────────────────────┤
│  1. 构建搜索空间                                         │
│     ├─ 65种高中水平数学操作                               │
│     ├─ 三组件程序模板 (Setup/Predict/Learn)               │
│     └─ 标量/向量/矩阵内存                                 │
│                                                         │
│  2. 准备 Proxy Tasks                                     │
│     ├─ 从 CIFAR-10/MNIST 提取二分类 pairs                │
│     ├─ 随机投影降维 (F=8~256)                            │
│     └─ 划分 Tsearch / Tselect                           │
│                                                         │
│  3. Regularized Evolution 搜索                            │
│     ├─ 空程序初始化种群                                  │
│     ├─ Tournament Selection + 三种变异                    │
│     ├─ Worker 并行 + Migration + FEC + Hurdles           │
│     └─ 适应度 = Tsearch 上精度中位数                     │
│                                                         │
│  4. 模型选择 (Tselect)                                   │
│                                                         │
│  5. 最终评估                                              │
│     ├─ 原始维度 CIFAR-10 测试集                          │
│     ├─ 超参调优（随机搜索）                               │
│     └─ 与其他数据集交叉验证                               │
└─────────────────────────────────────────────────────────┘
```

## 关联页面

- [[real2020-automl-zero-analysis]] — 完整 12 维度论文分析
- [[real2020-automl-zero-results]] — 实验结果详解
- [[real2020-automl-zero-critical]] — 贡献 / 知识点 / Negative Knowledge
- [[automl-zero]] — 实体页

## Evidence By Source

### `sources/papers/real2020-automl-zero.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/automl_zero_real2020.pdf`

^[sources/papers/real2020-automl-zero.md]
