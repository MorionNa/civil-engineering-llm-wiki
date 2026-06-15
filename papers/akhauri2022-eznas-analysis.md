---
title: "Akhauri et al. (2022) — EZNAS: Evolving Zero Cost Proxies For NAS Scoring 论文分析"
created: 2026-06-15
updated: 2026-06-15
type: paper-analysis
tags: [training-free-nas, neural-architecture-search, zero-shot, nas-bench-201, evolutionary-search]
methods: [genetic-programming, expression-tree, kendall-tau, zero-cost-proxy, evolutionary-algorithm]
results: [nas-bench-201, nds, nats-bench, kendall-tau-0.65, spearman-rho-0.89]
failure_modes: [top-10-percent-ranking-failure, batch-size-sensitivity, connectivity-blind, rcb-structure-rigid]
datasets: [nas-bench-201, cifar-10, cifar-100, imagenet-16-120, nds, nats-bench]
sources: [raw/papers/eznas_akhauri2022.pdf]
reproducibility: high
code_url:
  - https://github.com/EzNAS/EZNAS
dataset_url: []
confidence: high
---

# EZNAS: 演化零成本代理用于神经架构评分

> Yash Akhauri (Cornell), J. Pablo Muñoz, Nilesh Jain, Ravi Iyer (Intel Labs) — NeurIPS 2022
> **遗传编程自动发现零成本 NAS 评分指标**：24 小时 CPU 演化 → 跨搜索空间泛化的 SoTA 评分指标

## 1. 工程背景 (Engineering Background)

神经架构搜索（NAS）的核心瓶颈不在"搜不到好架构"，而在**评估候选架构的成本极高**。传统 NAS 流程中，每个候选架构需要部分或完整训练才能评估其质量——AmoebaNet 消耗了 3150 GPU 天。零成本代理（Zero-Cost Proxy）的出现改变了这一范式：通过分析网络**在初始化时的统计量**（权重、激活、梯度），无需训练即可生成与真实精度高度相关的评分。

然而，现有的零成本代理（如 synflow、SNIP、FISHER、NASWOT、TE-NAS、GradSign）完全由**人类专家手工设计**——需要多轮经验试错来选择合适的算法、数据集和设计空间。随着深度学习应用场景的多样化，这种手工设计范式不可持续。更关键的是，**现有零成本代理在跨搜索空间上泛化失败**——在 NAS-Bench-201 上有效的指标在 NDS 上完全失效。

## 2. Research Gap

已有零成本 NAS 评分指标（ZC-NASM）面临两大困境：

- **设计不可持续**：每个指标都是专家反复试验的产物，缺乏自动化设计方法论
- **泛化性差**：synflow 在 NAS-Bench-201 上表现不错（τ ≈ 0.37-0.57），但在 NDS 的大部分设计空间上 τ 骤降至 0.06 甚至负值。FLOPs 和 Params 反而是更稳定的跨空间代理——这本身就说明现有 ZC-NASM 设计有根本性问题

**核心空白**：能否用**自动化程序合成（遗传编程）**替代人类专家去发现零成本代理？能否找到一个**泛化于多个搜索空间和数据集**的通用 ZC-NASM？

## 3. 科学问题 (Scientific Question)

**能否通过遗传编程（Genetic Programming）框架，在给定网络统计量和简单数学运算的条件下，自动化地发现可解释、可泛化且达到 SoTA 评分-精度相关性的零成本神经架构评分指标（ZC-NASM）？**

## 4. 研究目标 (Research Objective)

提出 EZNAS 框架：(1) 用表达式树（expression tree）表示 ZC-NASM 程序；(2) 以 Kendall τ 为适应度目标进行进化搜索；(3) 在 NAS-Bench-201、NDS、NATS-Bench 上验证发现的 ZC-NASM 的评分-精度相关性和搜索效率。

## 5. 方法机制 (Method & Mechanism)

→ [[akhauri2022-eznas-method]]

核心：**表达式树程序表示 + 进化搜索 + 多空间适应度评估**。

1. **网络统计量采集**：对每个 ReLU-Conv2D-BatchNorm2D (RCB) 实例，采集 22 个张量（权重、激活、梯度 × 三种输入：数据 D、噪声 N、扰动 P）
2. **表达式树表示**：ZC-NASM 被编码为表达式树——终端节点是网络统计量，内部节点是数学运算（34 种操作），根节点输出分数
3. **进化算法**：DEAP 框架，VarOr 变异策略（交叉+突变+繁殖），每代 50 个个体，进化 15 代
4. **抗过拟合评估**：每代从 4 个不同搜索空间各随机采样 20 个架构，取最低适应度——强制程序泛化

## 6. 结果证据 (Result & Evidence)

→ [[akhauri2022-eznas-results]]

- **NAS-Bench-201**：EZNAS-A 的 Kendall τ 达 0.65（CIFAR-10/100）和 0.61（ImageNet-16-120），全面超越 NASWOT (0.57/0.61/0.55) 和 synflow
- **NDS CIFAR-10**：五个设计空间（DARTS/Amoeba/ENAS/PNAS/NASNet）上 EZNAS-A 的 Kendall τ 为 0.44-0.56，远超 synflow（最高 0.37，多数负值）
- **NATS-Bench SSS**：Spearman ρ 达 0.89/0.74/0.81（CIFAR-10/100/ImageNet-16-120），NASWOT 仅为 0.45/0.18/0.41
- **搜索加速**：EZNAS-A 结合 Aging Evolution 搜索，比同类零成本方法更快找到高精度架构

## 7. 贡献 (Contribution)

→ [[akhauri2022-eznas-critical]]

1. **首个自动发现零成本 NAS 评分指标的框架**——从手工设计到自动化发现的范式转变
2. **表达式树程序表示**——比 AutoML-Zero 式的顺序指令更高效，避免程序长度膨胀和冗余计算
3. **跨搜索空间泛化**：EZNAS-A 仅在 NDS-DARTS 上进化，却泛化到 NAS-Bench-201、NDS 全部 5 个子空间和 NATS-Bench
4. **可解释性**：发现的 EZNAS-A 本质上是一种"加权参数计数"——从 T3GN（随机噪声下的权重梯度）中提取信号，得分随通道数和深度单调递增
5. **极低碳足迹**：进化搜索仅 358.6g CO₂e（24 CPU 小时），vs 一次 NAS 搜索 4.49kg+

## 8. 核心知识点 (Core Knowledge)

1. **遗传编程用于 NAS 代理发现**：ZC-NASM 本质上都是简单程序（见图 2：synflow、SNIP、FISHER 均可表示为表达式树）→ 遗传编程是自然的发现工具
2. **表达式树 vs 顺序指令**：树结构保证每个操作都对最终输出有贡献 → 无冗余计算 → 进化时间可控
3. **加权参数计数的优越性**：EZNAS-A 本质是对激活/权重尺寸的非线性加权——比 FLOPs/Params 更精细，又比 synflow/SNIP 更稳健
4. **跨空间泛化需要对抗过拟合的评估策略**：单一空间评估 → 程序迅速过拟合；多空间 "min fitness" 策略 → 强制泛化
5. **零成本代理的实际作用是"粗筛"**：EZNAS-A 能有效区分好坏架构，但无法区分 top 10% 中的最佳架构——这是整个 ZC-NASM 领域的共性局限

## 9. Negative Knowledge

→ [[akhauri2022-eznas-critical]]

- **Top 10% 排名失败**：EZNAS-A 无法有效区分搜索空间中 top 10% 的最佳架构——这可能是 ZC-NASM 的固有局限，或需要搜索空间本身具有更低 FLOPs/Params 相关性
- **连接模式盲区**：当前方案对所有 RCB 实例取 mean 聚合 → 完全忽略网络的全局连接拓扑
- **RCB 结构刚性**：只能处理 ReLU-Conv2D-BatchNorm2D 结构，需截断 ReLU-Conv2D-Conv2D-BatchNorm2D
- **无法发现 NASWOT 类指标**：当前统计量采集设计不支持多输入比较 → 无法发现需要对比两个输入的指标
- **批大小敏感性**：batch size=1 时方差高，增大 batch size 线性增加内存需求
- **操作空间局限**：34 个操作均无标量超参数（如 Power 固定为平方，噪声固定为 N(0,1)）→ 可能错过更优配置

## 10. 可迁移知识 (Transferable Knowledge)

→ [[akhauri2022-eznas-critical]]

| 知识 | → 迁移 |
|------|--------|
| 遗传编程自动发现评估指标 | 任何需要从数据中学习评分函数的场景（模型选择、数据质量评估） |
| 表达式树作为程序表示 | 需要高效搜索可执行程序的任何 AutoML 任务 |
| "min fitness over multiple spaces" 泛化策略 | 任何需要从多个子任务学习通用代理的元学习问题 |
| ZC-NASM = 加权参数计数 | 提示未来零成本代理设计应更关注"如何加权"而非"测量什么新量" |
| batch size=1 的方差问题 | 任何零成本评估都需考虑随机初始化/输入的方差，需多 seed 取均值 |

## 11. 研究机会 (Research Opportunity)

→ [[akhauri2022-eznas-critical]]

- **引入连接编码**：将 NAS 架构的连接编码（如 path encoding）作为程序输入 → 发现能捕获拓扑信息的 ZC-NASM
- **学习加权聚合**：替代 mean 聚合，学习各层的权重 → 区分关键层和非关键层
- **动态超参数优化**：让遗传编程同时优化操作的标量超参数（如 Power 的指数、噪声的方差）
- **多输入比较操作**：引入多 mini-batch 比较 → 使程序空间覆盖 NASWOT 类指标
- **神经符号程序合成**：用深度学习加速程序搜索（如学习 proposal 网络引导变异）
- **探索低精度/小数据集代理**：降低进化搜索本身的成本以扩展到更大程序空间
- **Top 10% 排名专项研究**：设计新的搜索空间和评估策略专门针对顶级架构的区分

## 12. 可复现性 (Reproducibility)

**🟢 高复现性** — 代码 + benchmark 完全公开

| 项目 | 说明 |
|------|------|
| **等级** | 🟢 高 |
| **官方代码** | `https://github.com/EzNAS/EZNAS`（开源） |
| **Benchmark** | NAS-Bench-201、NDS、NATS-Bench（全公开） |
| **数据集** | CIFAR-10/100、ImageNet-16-120、ImageNet（全公开） |
| **硬件** | 进化搜索：Intel Xeon Gold 6242 CPU + 630GB RAM（~24h）；测试：NVIDIA V100 GPU |
| **超参数** | 论文附录完整列出（表：15 代、50 个体、tournament size=4 等） |

**复现要点**：网络统计量采集需要约 60GB RAM。EZNAS-A 可通过加载预计算统计量直接验证。进化搜索本身 24h 可完成。

## 关联页面

- [[akhauri2022-eznas-method]] — 遗传编程框架、表达式树、进化算法详解
- [[akhauri2022-eznas-results]] — NAS-Bench-201 / NDS / NATS-Bench 完整相关性数据
- [[akhauri2022-eznas-critical]] — 贡献 / Negative / 可迁移 / 机会
- [[eznas]] — EZNAS 实体页面
- [[te-nas]] — TE-NAS（训练无关 NAS 先驱，NTK + 线性区域数）
- [[nasbench201]] — NAS-Bench-201 基准数据集
