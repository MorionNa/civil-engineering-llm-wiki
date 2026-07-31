---
id: comparisons--optimizer-for-ai4s-and-physics-models
title: AdamW vs Adafactor vs Lion vs Shampoo vs SOAP vs Muon：AI4S 与物理模型优化器选型
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- method/evaluation
- method/graph-neural-network
- method/neural-operator
- method/pinn
- method/transformer
keywords:
- adafactor
- adamw
- ai4s
- comparison
- lion-optimizer
- matrix-orthogonalization
- memory-efficiency
- muon
- neural-operator
- newton-schulz
- optimizer
- pinn
- preconditioning
- scientific-machine-learning
- shampoo-optimizer
- soap-optimizer
- training-efficiency
- wallclock-efficiency
sources:
- raw/articles/jordan2024-muon-blog.pdf
- https://arxiv.org/abs/1711.05101
- https://proceedings.mlr.press/v80/shazeer18a.html
- https://proceedings.mlr.press/v80/gupta18a.html
- https://arxiv.org/abs/2302.06675
- https://proceedings.iclr.cc/paper_files/paper/2025/hash/e988664070e9591f93fdcf605f7dc623-Abstract-Conference.html
created: '2026-07-29'
updated: '2026-07-31'
confidence: high
---

# AdamW vs Adafactor vs Lion vs Shampoo vs SOAP vs Muon

> **用途：** 为 PINN、神经算子、物理 Transformer、结构动力响应代理和一般 AI4S 模型选择训练优化器。
> **结论先行：** AdamW 仍应作为默认与公平 baseline；显存优先考虑 Adafactor/Lion；矩阵隐藏层和大批量训练优先试 Muon；能够承担矩阵预条件及分布式复杂度时再试 SOAP，Shampoo 更适合作为完整预条件路线和机制参照。

## 1. 这六类优化器解决的不是同一个问题

它们不能只按“谁的 loss 最低”排成单一榜单：

| 优化器 | 首要目标 | 核心操作 |
|---|---|---|
| AdamW | 稳定、通用、成熟的自适应训练 | 逐参数一阶/二阶矩 + decoupled weight decay |
| Adafactor | 降低 Adam 类二阶矩状态显存 | 用行/列因子近似矩阵二阶矩 |
| Lion | 用极简 sign-momentum 降状态并提高大批量效率 | momentum 的符号方向更新 |
| Shampoo | 利用矩阵/张量结构做多轴预条件 | 各维统计矩阵 + inverse matrix root |
| SOAP | 保留 Shampoo 坐标系，同时使用 Adam 式二阶矩更新 | 在 Shampoo 特征基中运行 Adam/Adafactor |
| Muon | 让二维隐藏层更新在奇异方向上更均衡 | momentum 后做 Newton–Schulz 近似正交化 |

因此选型首先取决于瓶颈：是**训练稳定性、显存、样本效率、wall-clock、矩阵病态性，还是分布式实现成本**。

## 2. 统一对比表

| 维度 | AdamW | Adafactor | Lion | Shampoo | SOAP | Muon |
|---|---|---|---|---|---|---|
| 更新粒度 | elementwise | factored elementwise | elementwise sign | matrix/tensor axes | matrix eigenbasis + elementwise moments | 2D matrix singular directions |
| 主要状态 | 一阶矩 + 二阶矩 | 行/列二阶矩；可无 momentum | 单个 momentum | 每轴预条件统计矩阵 | Shampoo 统计 + rotated moments | momentum；NS 临时矩阵 |
| 优化器状态显存 | 高，约 2× 参数量级 | 低，矩阵为行列和 | 中低，约 1× 参数量级 | 依层形状而定，可能很高 | 较高 | 中低；但需与 AdamW 混合 |
| 每步计算 | 低 | 低 | 很低 | 中高，含矩阵根/分解 | 中高，取决于预条件频率 | 中，主要是若干 GEMM |
| 分布式复杂度 | 最低 | 低 | 低 | 高 | 高 | 中高，超大规模仍需专门分片 |
| 默认成熟度 | 最高 | 高 | 中高 | 中 | 中 | 中，快速发展中 |
| 矩阵结构利用 | 无 | 低秩式二阶矩近似 | 无 | 强 | 强 | 强，但只作用于更新奇异谱 |
| 大批量潜力 | 稳定 baseline | 主要优势不是大批量 | 原论文称收益随 batch 增大 | 适合预条件收益可摊销的场景 | 论文重点为大批量 LM | Muon 经验上在大 batch 较有吸引力 |
| 适用全部参数 | 是 | 是 | 是 | 原则上可处理张量 | 原则上可处理矩阵/张量层 | 否；hidden 2D/flattened conv，其他用 AdamW |
| 最主要风险 | 状态显存；baseline 易被低估/欠调 | 收敛和超参行为与 AdamW 不完全相同 | sign 更新过粗、LR/WD 标度不同 | 实现、通信和矩阵运算复杂 | 实现复杂、证据集中于 LM | 规模/任务外推、混合参数组和分布式实现 |

> 表中的显存为优化器辅助状态的结构性比较，不等于训练总显存；激活、梯度、master weights、分片策略和混合精度可能更占主导。

## 3. 六种方法分别在做什么

### 3.1 AdamW：默认基线与控制组

AdamW 的关键不是发明新的自适应矩，而是把 weight decay 从梯度更新中解耦。与在 Adam 梯度中加入 $L_2$ 项相比，decoupled weight decay 让学习率与衰减系数的作用更清楚，也改善了原始 Adam 的泛化表现。

**优势：**

- 框架实现、分布式、混合精度和 checkpoint 生态最成熟；
- 小批量、噪声梯度、多类型参数和复杂 loss 下通常最稳妥；
- 是评估其他优化器是否真正有效的必要 baseline。

**局限：**

- 保存一阶、二阶矩，状态显存高；
- elementwise 缩放不利用权重矩阵的行列或奇异方向结构；
- 在大批量、矩阵主导的模型中可能不是最优 wall-clock-to-target。

**AI4S 定位：** 默认起点。任何 Muon、SOAP 或 Lion 结论，都应建立在充分调优的 AdamW 上。

### 3.2 Adafactor：显存优先的 Adam 类方案

Adafactor 对矩阵参数不保存完整逐元素二阶矩，而只维护行和列的统计量，并用它们重构近似二阶矩。原始论文还提出 update clipping、逐渐变化的 decay rate 与相对参数尺度更新，并可通过取消 momentum 进一步节省状态。

**优势：**

- 对大矩阵的辅助状态从元素数级降至行数加列数级；
- 保留自适应更新的基本思想；
- 适合显存受限、参数规模大而算力尚可的训练。

**局限：**

- 行列因子只能表达特定的可分离二阶矩结构；
- 不应把 AdamW 超参数直接原样复制；
- 节省优化器状态不一定改善 wall-clock 或样本效率。

**AI4S 定位：** 当模型、状态变量或高维输出导致显存先于计算成为瓶颈时，是优先候选；对于较小 PINN，通常没有必要仅为节省优化器状态而更换。

### 3.3 Lion：单 momentum 状态的 sign 更新

Lion 由程序搜索得到，只跟踪 momentum，并通过 sign operation 产生各参数幅值相同的更新。原论文报告其优化器状态比 Adam 少，并指出 Lion 需要比 Adam 更小的学习率；由于 sign 更新范数较大，weight decay 也需重新调优。论文观察到，其相对收益会随 batch size 增大。

**优势：**

- 更新规则简单，状态比 AdamW 少；
- kernel 易优化，通信形式简单；
- 在视觉、扩散和部分语言任务上显示出较好的计算效率。

**局限：**

- sign 丢弃梯度幅值信息；
- 在梯度噪声高、不同物理残差尺度差异大时，可能放大不稳定方向；
- 论文也报告某些任务收益很小或无统计显著性。

**AI4S 定位：** 适合作为显存与吞吐优先的轻量候选，但不应假定 sign update 能自动解决 PINN 多损失失衡；必须检查每个物理 loss 的梯度和收敛。

### 3.4 Shampoo：完整的矩阵/张量预条件路线

Shampoo 为张量的每一个维度维护预条件统计矩阵，避免存储完整 Kronecker 预条件器，并通过矩阵逆根调整梯度。它比 Adam 的 elementwise 二阶矩更充分地利用层结构。

**优势：**

- 对病态、各向异性的矩阵优化问题有更强结构建模能力；
- 理论框架完整，是理解 Muon 和 SOAP 的重要参照；
- 在预条件器成本可以被大批量训练摊销时具有吸引力。

**局限：**

- 矩阵根、统计更新、block size、更新频率和 damping 增加实现复杂度；
- 大层和分布式环境下需要分块、分片和通信设计；
- 每步 FLOP 不等于实际 wall-clock，kernel 和通信效率决定最终收益。

**AI4S 定位：** 对大规模神经算子、物理 Transformer 或矩阵病态明显的模型有研究价值；对小型逐实例 PINN 通常过重。

### 3.5 SOAP：Shampoo 坐标系中的 Adam

SOAP 的出发点是：Shampoo 的预条件特征基可以看作一个旋转坐标系，在该坐标系内运行 Adafactor/Adam 式二阶矩更新。它不必每步重新计算特征分解，而是在缓慢变化的基中持续更新二阶矩。

ICLR 2025 论文在 360M 和 660M 语言模型大批量预训练中报告：相对 AdamW，迭代数减少超过 40%，wall-clock 减少超过 35%；相对 Shampoo，两个指标均改善约 20%。这些数字属于该论文特定 LM 设置，不是 AI4S 的直接验证。

**优势：**

- 比原始 Shampoo 更接近 Adam 的使用方式；
- 尝试同时获得旋转坐标预条件和 Adam 稳定性；
- 仅比 Adam 多一个主要超参数：预条件更新频率。

**局限：**

- 仍需矩阵特征基、周期性分解与较复杂的分布式实现；
- 证据目前主要集中于较大语言模型与大批量设置；
- 小模型或短训练中，预条件成本可能无法摊销。

**AI4S 定位：** 大规模、长训练、矩阵层占主导且 AdamW 明显受病态限制时，SOAP 比 Shampoo 更适合作为第二阶段高级候选。

### 3.6 Muon：momentum 更新的近似正交化

Muon 先形成 SGD/Nesterov momentum 更新矩阵，再用 5 步 bfloat16 Newton–Schulz 迭代近似替换为最近的半正交矩阵。它保留奇异向量，压平奇异值差异，从而相对增强低幅值的“稀有方向”。

Muon 只处理 hidden 2D matrices；embedding、输出头、bias、gain 和其他标量/向量必须用 AdamW 等辅助优化器。Transformer 的 Q、K、V 应分别处理。

**优势：**

- 主要运算是 GPU 友好的矩阵乘法；
- 状态接近 momentum，低于 AdamW 的双矩状态；
- Muon 博客和 NanoGPT/CIFAR 竞争任务显示较强的样本与 wall-clock 效率；
- 比完整 Shampoo/SOAP 更简单，适合快速实验。

**局限：**

- 不是所有参数可用，必须设计 parameter groups；
- “稀有方向放大”仍是解释性假说；
- 原始博客证据集中于小型至 1.5B 预训练和 speedrun；
- 超大规模分布式 Newton–Schulz、finetuning 与 RL 的适用性仍需验证。

**AI4S 定位：** 对 MLP/Transformer/GNN/Neural Operator 的隐藏矩阵，是最值得优先与 AdamW 做 A/B 测试的新候选；但物理参数和输出层应保留 AdamW。

## 4. 按研究场景选型

### 场景 A：普通 PINN、小模型、逐问题训练

推荐顺序：

```text
AdamW
  → AdamW + 合理的 loss weighting / nondimensionalization / causal strategy
  → Muon(hidden matrices) + AdamW(other parameters)
  → Lion
```

原因：这类任务常见的主问题是梯度冲突、尺度不平衡、刚性和配点覆盖，而不是优化器状态显存。先修复物理训练问题，再比较优化器。

### 场景 B：高自由度结构动力响应、图网络或 Transformer 代理

推荐顺序：

```text
AdamW baseline
  → Muon + AdamW hybrid
  → SOAP
  → Shampoo
```

原因：模型逐渐由二维线性投影、注意力和图消息矩阵主导，矩阵方向病态更可能成为瓶颈；Muon 改造成本最低，SOAP/Shampoo 用于进一步验证预条件收益。

### 场景 C：大规模 Neural Operator / PDE foundation model

推荐顺序：

```text
显存足够：AdamW → Muon → SOAP
显存不足：Adafactor → Lion → sharded AdamW
大批量且长训练：SOAP / Muon 优先进入正式 sweep
```

应分别记录 token/sample efficiency 与 wall-clock efficiency，避免只比较 iteration 数。

### 场景 D：极端显存受限

推荐：

1. Adafactor：最明确地针对二阶矩状态显存；
2. Lion：单 momentum 状态且实现简单；
3. Muon + auxiliary AdamW：只有 hidden matrices 节省状态，辅助 AdamW 参数仍有双矩状态；
4. 结合 optimizer-state sharding、activation checkpointing 和低精度状态。

### 场景 E：强病态、矩阵结构明确、大 batch

推荐：SOAP 或 Shampoo；Muon 作为成本更低的对照。

需要注意：Muon 是压平更新奇异值，Shampoo/SOAP 是学习更完整的预条件坐标。二者都利用矩阵结构，但机制不等价。

## 5. AI4S 中不能由优化器替代的问题

以下问题通常不会因为换优化器而自动消失：

- 控制方程、边界、初值和数据 loss 的量纲不一致；
- 多个 loss 梯度方向冲突；
- PINN 的谱偏差和高频学习困难；
- 刚性系统或长期因果传播；
- 配点不足导致的伪解；
- 本构路径依赖状态未输入网络；
- 输出归一化和物理变量尺度差异；
- 时间积分或自回归 rollout 的误差积累。

因此优化器比较必须固定这些训练策略，或者将其作为显式实验因子。

## 6. 推荐的公平实验协议

### 6.1 第一阶段：建立强 AdamW baseline

固定：

- 网络、初始化和数据；
- 无量纲化/归一化；
- loss weighting 或 causal strategy；
- batch、配点和时间窗；
- 总训练算力与 early-stopping 规则。

AdamW 至少搜索：

- learning rate；
- weight decay；
- $\beta_1,\beta_2$；
- warmup 与 decay schedule。

### 6.2 第二阶段：等预算 optimizer sweep

| 优化器 | 必须单独搜索的关键量 |
|---|---|
| Adafactor | relative step、clipping threshold、decay、是否 momentum |
| Lion | 更小 LR、weight decay、$\beta_1/\beta_2$ |
| Shampoo | block size、damping、preconditioner frequency、root precision |
| SOAP | LR/WD、Adam betas、preconditioner frequency |
| Muon | Muon LR、momentum/Nesterov、weight decay、NS steps、aux AdamW LR |

禁止把 AdamW 的最优 LR/WD 原样复制给其他方法，然后宣布其失败。

### 6.3 第三阶段：报告四类指标

1. **优化质量：** 最终 loss、相对 $L_2$、峰值误差、物理残差；
2. **样本效率：** samples/steps-to-target；
3. **计算效率：** wall-clock-to-target、GPU-hours、每步时间；
4. **资源与稳定性：** 峰值显存、通信量、失败率、不同 seed 方差。

建议使用至少 3 个随机种子，并同时报告：

```text
best final accuracy
median wallclock-to-target
failure / divergence rate
```

### 6.4 结构动力模型的附加指标

- 位移、速度、加速度和恢复力分别评价；
- 峰值响应误差与全时程误差分开；
- 能量平衡残差；
- 长时相位漂移；
- 跨地震动、跨结构和跨自由度泛化；
- 本构内变量/损伤变量的物理可行性。

## 7. 决策树

```text
是否首先需要可信、成熟、易复现的 baseline？
├─ 是 → AdamW
└─ 否 / baseline 已充分调优
   │
   ├─ 优化器状态显存是否是主要瓶颈？
   │  ├─ 是 → Adafactor（最省）或 Lion（简单）
   │  └─ 否
   │
   ├─ 模型是否以 2D hidden matrices 为主？
   │  ├─ 是 → Muon + AdamW hybrid
   │  └─ 否 → AdamW / Adafactor / Lion
   │
   ├─ 是否大 batch、长训练，且怀疑矩阵病态？
   │  ├─ 是 → SOAP；资源充足时加入 Shampoo
   │  └─ 否 → Muon 或 AdamW
   │
   └─ 是否只有小模型、短训练或高度噪声的物理 loss？
      └─ 是 → 优先 AdamW，其他优化器仅作严格对照
```

## 8. 面向当前结构动力研究的建议

对于“PINN/图模型求解上百至上千自由度非线性结构响应”，建议采用三级路线：

### V1：AdamW 可信基线

- 先解决无量纲化、物理 loss 平衡、时间因果和内变量表示；
- 记录完整 loss trajectory 和 wall-clock-to-target；
- 与 [[functional-scaling-law]] 的轨迹分析结合。

### V2：Muon 混合优化

- 图编码器、Transformer、MLP hidden matrices 用 Muon；
- 输入/输出层、本构参数、归一化参数和标量参数用 AdamW；
- Q/K/V 分开；
- 对比更新矩阵奇异值谱，验证“少数方向主导”是否真实存在。

### V3：SOAP 预条件验证

当模型足够大、batch 足够大且 Muon 已显示收益时，再引入 SOAP：

- 判断收益来自一般矩阵预条件还是 Muon 特定的正交化；
- 做等 wall-clock、等显存和等样本三套对比；
- 测试跨自由度泛化是否因更好的优化而改善，而非只降低训练误差。

## 9. 最终选型结论

| 需求 | 第一选择 | 第二选择 |
|---|---|---|
| 最稳妥、论文 baseline | AdamW | — |
| 显存最低 | Adafactor | Lion |
| 简单低状态、高吞吐 | Lion | Adafactor |
| hidden matrix 训练效率 | Muon + AdamW | SOAP |
| 强矩阵预条件 | SOAP | Shampoo |
| 小型 PINN | AdamW | Muon hybrid |
| 大型物理 Transformer/Neural Operator | Muon hybrid | SOAP |
| 方法机制研究 | Shampoo / SOAP / Muon 三者并列 | AdamW 控制组 |

**最重要的原则：** 不应问“哪个优化器最好”，而应问“在相同训练目标、相同硬件预算和充分调优的 baseline 下，哪个优化器最先达到物理可接受误差”。

## 10. 证据边界

- AdamW、Adafactor、Shampoo、Lion 与 SOAP 的主要机制和实验结论来自各自原始论文；
- Muon 的主要材料来自 Keller Jordan 技术博客和公开 speedrun 日志，而非同行评审论文；
- SOAP 的 >40% iteration、>35% wall-clock 改善来自 360M/660M 大批量语言模型实验；
- Muon 的 1.35× NanoGPT 改善和 1.5B 结果来自博客报告；
- 这些结论均未直接证明在 PINN、神经算子或结构动力响应任务上有效；本页的 AI4S 选型是基于机制的可检验推断。

## 11. 主要来源

1. Loshchilov & Hutter (2019), *Decoupled Weight Decay Regularization*: https://arxiv.org/abs/1711.05101
2. Shazeer & Stern (2018), *Adafactor: Adaptive Learning Rates with Sublinear Memory Cost*: https://proceedings.mlr.press/v80/shazeer18a.html
3. Gupta, Koren & Singer (2018), *Shampoo: Preconditioned Stochastic Tensor Optimization*: https://proceedings.mlr.press/v80/gupta18a.html
4. Chen et al. (2023), *Symbolic Discovery of Optimization Algorithms* (Lion): https://arxiv.org/abs/2302.06675
5. Vyas et al. (ICLR 2025), *SOAP: Improving and Stabilizing Shampoo using Adam for Language Modeling*: https://proceedings.iclr.cc/paper_files/paper/2025/hash/e988664070e9591f93fdcf605f7dc623-Abstract-Conference.html
6. Jordan et al. (2024), *Muon: An optimizer for hidden layers in neural networks*: https://kellerjordan.github.io/posts/muon/

## 关联页面

- [[jordan2024-muon-optimizer]]
- [[functional-scaling-law]]
- [[wang2021-pinn-ntk-failure-analysis]]
- [[gao2025-adaptive-loss-pinn-analysis]]
- [[pgt]]
- [[legonet]]
- [[sgno]]

## Evidence By Source

### `raw/articles/jordan2024-muon-blog.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/articles/jordan2024-muon-blog.pdf]
