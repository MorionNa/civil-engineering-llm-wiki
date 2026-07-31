---
id: papers--akhauri2022-eznas-critical
title: EZNAS 批判性分析 — 贡献、局限、可迁移与未来方向
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- evidence/paper
- method/neural-architecture-search
- method/transformer
keywords:
- evolutionary-search
- genetic-programming
- limitation
- training-free-nas
- zero-cost-proxy
sources:
- sources/papers/akhauri2022-eznas.md
created: '2026-06-15'
updated: '2026-07-31'
confidence: high
parent: akhauri2022-eznas-analysis
---

# EZNAS 批判性分析

## 7. 贡献 (Contribution)

### 贡献 1：零成本代理设计的范式转变

EZNAS 将零成本 NAS 评分指标从**"专家手工设计"**转变为**"遗传编程自动发现"**。这不是渐进式改进，而是方法论的范式升级。观察到一个关键洞见：现有 ZC-NASM（synflow、SNIP、FISHER）都可以用简单表达式树表示 → 这些指标本身就在遗传编程的"可达程序空间"内 → 自动发现是自然且高效的。

### 贡献 2：表达式树程序表示

AutoML-Zero 使用顺序指令表示导致程序膨胀。EZNAS 改用表达式树后实现了：(a) 每个操作都对输出有贡献（无冗余）；(b) 进化时间可控（24h CPU）；(c) 发现的程序可解释（可直接读树结构）。这一设计选择是工程上的关键创新。

### 贡献 3：跨搜索空间泛化的 ZC-NASM

EZNAS-A 仅在 NDS-DARTS CIFAR-10 上进化，却在 NAS-Bench-201（3 数据集）、NDS（5 设计空间 × 2 数据集）、NATS-Bench（2 搜索空间）上全部取得 SoTA 相关性。对比 synflow 在 NDS Amoeba 上 τ=-0.06 的惨败，这是质的飞跃。

### 贡献 4：极小碳足迹

进化搜索 358.6g CO₂e，一次 NAS 搜索 4.49kg CO₂e → 12.5× 更低碳。且 EZNAS-A 一经发现即可反复使用 → 端到端 NAS 效率提升两个数量级。

### 贡献 5：揭示"加权参数计数"的本质

通过分析 EZNAS-A 和 EZNAS-B 的程序行为，论文揭示了最佳零成本代理的本质：不是某些神秘的数学量，而是**对参数/激活尺寸的非线性加权函数**。这一洞察为未来代理设计指明了方向。

## 8. 核心知识点 (Core Knowledge)

1. **遗传编程天然适合 ZC-NASM 发现**：现有指标都是简单程序 → GP 的搜索空间天然包含它们及更多组合
2. **表达式树 > 顺序指令**：树结构消弭冗余，是程序合成的关键架构选择
3. **"min fitness over multiple spaces" = 泛化**：每代随机选 4 空间取最低 τ 作为适应度 → 对抗过拟合的有效 meta-learning 策略
4. **加权参数计数 > 纯参数计数**：EZNAS-A 的优越性来自非线性的 kernel size 效应和通道加权方式
5. **零成本代理的天花板在 top 10%**：能区分好坏，不能区分最好 → 这是领域共性局限而非 EZNAS 独有
6. **batch size = 1 是精度-效率 trade-off**：增大 batch 提升相关性但线性增加内存
7. **连接拓扑信息的缺失是根本瓶颈**：当前设计完全忽略层间连接 → 只能评分"层的质量"而非"网络的质量"

## 9. Negative Knowledge（负知识）

### 局限 1：Top 10% 排名失败——零成本代理的天花板？

EZNAS-A 能有效排序整个搜索空间，但**无法区分 top 10% 中的最佳架构**。论文发现存在其他能弱排序 top 10% 的程序，但它们不泛化。这暗示：**准确区分顶级架构可能需要比"初始化统计量"更丰富的信息**——可能需要在搜索空间中引入 FLOPs/Params 相关性更低的设计变体。

### 局限 2：连接模式盲区

所有 RCB 实例的评分取 mean → 完全丢失层间连接拓扑。如果两个网络有相同的层配置但不同的 skip-connect 模式，EZNAS-A 给出相同评分。

### 局限 3：RCB/CBR 结构刚性

只能识别固定的 ReLU-Conv2D-BatchNorm2D 三连结构。NDS 中的 ReLU-Conv2D-Conv2D-BatchNorm2D 必须截断第二个卷积。当搜索空间出现 Transformer attention、depthwise conv 等新算子时，统计量采集需要重新设计。

### 局限 4：操作空间的不完备性

- 34 个操作无标量超参数（Power 固定平方，噪声固定 N(0,1)）
- 无多输入比较操作 → 不可能发现 NASWOT 式的跨输入对比指标
- 无控制流 → 不可能发现条件判断逻辑

### 局限 5：batch size 与内存的 trade-off

batch=1 时一个样本不足以描述架构（论文证实增大 batch 提升相关性）。但增大 batch 线性增加中间张量存储 → 进化搜索的内存需求线性增长。

### 局限 6：进化搜索本身的效率

24 小时 CPU + 630GB RAM 虽然比训练 NAS 便宜，但对普通研究者仍有门槛。论文建议了低精度/小数据集代理任务，但未实际验证。

## 10. 可迁移知识 (Transferable Knowledge)

| 知识 | 描述 | 迁移场景 |
|------|------|----------|
| **遗传编程用于评估指标设计** | 当"什么是好的评估函数"难以先验定义时，用 GP 从数据中自动发现 | 模型质量评估、数据质量打分、超参重要性排序 |
| **表达式树作为可解释程序表示** | 树结构保证无冗余、天然可解释、适合进化操作 | 符号回归、AutoML pipeline 合成、特征工程自动化 |
| **Multi-space min fitness 泛化** | 不取均值而取最差值，惩罚空间间的不一致性 | 任何跨任务/跨域的元学习或代理构建场景 |
| **"加权参数计数"视角** | ZC-NASM 的核心信息源是参数/激活的尺寸分布而非神秘理论量 | 指导未来零成本代理的设计原则 |
| **batch size 对统计量的影响量化** | batch=1 方差大，多 seed 或大 batch 是零成本方法的必要成本 | 所有基于初始化统计量的 NAS/剪枝/分析工作 |
| **进化搜索的批量统计量预计算** | 为可进化性，必须预先计算并缓存网络统计量 | 任何 GP/AutoML 与大数据交互的架构设计 |

## 11. 研究机会 (Research Opportunity)

### 短期（1-2 年）

1. **引入连接编码**：将路径编码（path encoding）、邻接矩阵等作为程序的新终端节点类型 → 让 GP 能发现考虑拓扑的 ZC-NASM。这直接解决"连接模式盲区"问题。

2. **学习聚合权重**：替代 mean，学习 `score = Σ wᵢ × f(layer_i)` 中的 wᵢ → 区分关键层和非关键层。可用 attention 或简单的 MLP 学习。

3. **动态超参数优化**：让 GP 同时进化操作的标量参数（Power 指数、噪声方差等）→ 扩大程序空间。

4. **多输入比较操作**：引入支持两个 mini-batch 对比的操作 → 程序空间覆盖 NASWOT 类指标。

### 中期（2-3 年）

5. **神经符号程序合成加速**：用深度学习训练 proposal 网络，预测哪些子树变异可能有效 → 减少无效程序的评估次数，加速进化。

6. **扩展到非 CNN 架构**：将 EZNAS 应用到 Transformer（[[training-free-nas-transformers]]）、RNN 等架构的零成本代理发现。需要重新设计统计量采集和操作集。

7. **Top 10% 排名专项研究**：在更"反 FLOPs"的搜索空间中重新训练 benchmark → 检验 ZC-NASM 的区分能力是否有根本天花板。

### 长期（3-5 年）

8. **联合搜索 ZC-NASM + 架构**：不是先发现代理再搜索架构，而是让 GP 和架构搜索协同进化——代理的适应度取决于它引导架构搜索的效率。

9. **可微分遗传编程**：用可微分方法近似 GP 的离散搜索 → 梯度优化加速发现。

## 关联页面

- [[akhauri2022-eznas-analysis]] — 论文分析总览
- [[akhauri2022-eznas-method]] — 遗传编程方法详解
- [[akhauri2022-eznas-results]] — 完整实验结果
- [[eznas]] — EZNAS 实体
- [[te-nas]] — TE-NAS（手工设计的零成本代理先驱）
- [[training-free-nas-transformers]] — 训练-free NAS 在 Transformer 上的拓展工作

## Evidence By Source

### `sources/papers/akhauri2022-eznas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/eznas_akhauri2022.pdf`

^[sources/papers/akhauri2022-eznas.md]
