---
id: papers--lee2024-aznas-analysis
title: 'Lee & Ham (2024) — AZ-NAS: Assembling Zero-Cost Proxies for NAS 论文分析'
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- evidence/paper
- method/neural-architecture-search
keywords:
- nas-bench-201
- neural-architecture-search
- training-free-nas
- weight-sharing-nas
- zero-shot
sources:
- sources/papers/lee2024-aznas.md
created: '2026-06-15'
updated: '2026-07-31'
confidence: high
methods:
- pca-isotropy
- jacobian-spectral-norm
- non-linear-ranking-aggregation
- evolutionary-search
- zero-cost-proxy-ensemble
results:
- nas-bench-201
- mobilenetv2-imagenet
- autoformer-vit
- kendall-tau-0.741
- imagenet-top1-81.1
failure_modes:
- progressivity-fails-for-vit
- single-proxy-insufficient
- jacobian-approximation-linear
- gaussian-input-only
datasets:
- nas-bench-201
- cifar-10
- cifar-100
- imagenet-16-120
- imagenet
- autoformer
reproducibility: high
code_url:
- https://github.com/cvlab-yonsei/AZ-NAS
---

# AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search

> Junghyup Lee, Bumsub Ham — Yonsei University & KIST — arXiv:2403.19232, 2024
> **集成式零成本代理**：4 种互补代理 + 非线性排序聚合 → NAS-Bench-201 Kendall τ = 0.741，ImageNet 81.1% Top-1

## 1. 工程背景 (Engineering Background)

神经架构搜索（NAS）的核心问题是**评估一个架构好坏的成本极高**。传统方法（RL、EA、DARTS）需要迭代训练数万个子网络或训练超网（supernet），搜索成本动辄数百甚至数千 GPU 天，将 NAS 锁定在大厂手中。

训练-free NAS 的出现提供了突破口：用零成本代理（zero-cost proxy）在**初始化时**、**不需要任何训练和标签**的情况下，通过分析激活值或梯度来给架构打分排序。例如 NASWOT 用线性区域数衡量表达能力，Synflow 用参数重要性评估，ZiCo 用梯度统计量。但这些方法有一个共同的致命缺陷：**排序一致性弱**——在 NAS-Bench-201 上，连最基础的 #Params 和 FLOPs 的 Kendall τ 都经常超过精心设计的代理，说明现有代理没能真正捕捉到与最终性能相关的信号。

更关键的是，现有方法都**只用一个代理从单一视角评估架构**——或侧重表达能力，或侧重梯度信号。但一个架构的最终性能受多重因素影响（表达力、训练稳定性、计算复杂度等），单视角评估天然不充分。

## 2. Research Gap

训练-free NAS 面临三大瓶颈：

1. **单代理视角狭窄**：每个已有方法只捕捉一种网络特性（如 NASWOT 的线性区域数、Synflow 的突触流），而最终性能是多种因素的综合结果。例如参数量大的网络也会遭遇梯度消失/爆炸——单看参数量判断不了。

2. **已有代理高度相关**：Shu et al. (2022) 证明了基于梯度的代理（SNIP、Grasp、Synflow 等）**理论等价**，组装它们不能提供增量信息，反而增加计算开销。

3. **组合代理效率低下**：TE-NAS 组合了线性区域数 + NTK 条件数，但线性区域计数不支持大网络，NTK 计算极慢（1311.8 ms/arch），单独使用两个代理已不堪重负，遑论组合更多代理。

**核心空白**：能否设计一组**互补的、高效的、无需特殊架构修改**的零成本代理，并有效地聚合它们的排序信号，在不牺牲效率的前提下显著提升排序一致性？

## 3. 科学问题 (Scientific Question)

**如何设计一组捕捉网络不同维度的互补零成本代理，并通过有效的排序聚合机制，在无需训练、单次前向/反向传播的条件下，实现对候选架构的准确排序？**

## 4. 研究目标 (Research Objective)

提出 AZ-NAS：① 设计 4 个新颖的零成本代理——表达力（Expressivity）、渐进性（Progressivity）、可训练性（Trainability）、复杂度（Complexity），从不同视角评估架构；② 提出非线性排序聚合方法，使低排名代理不可被其他高排名代理"抵消"；③ 在 NAS-Bench-201、MobileNetV2 ImageNet、AutoFormer 上以极低搜索成本达到 SOTA。

## 5. 方法机制 (Method & Mechanism)

→ [[lee2024-aznas-method]]

核心：**4 代理互补体系 + 非线性 log-Rank 聚合 + 进化搜索**。

- **Expressivity (sE)**：对每个 primary block 输出特征做 PCA → L1 归一化特征值 → 计算熵。高熵 = 各方向方差均衡 = 特征空间各向同性 → 网络表征容量大，避免维度坍缩。
- **Progressivity (sP)**：相邻 block 的 sE 差异的最小值。若后续 block 的 sE 持续增大 → 网络沿深度渐进扩展特征空间 → 有效捕获多层次语义。
- **Trainability (sT)**：用 Hutchinson 方法近似 Jacobian 谱范数，惩罚偏离 1 的范数（对称惩罚偏大和偏小）→ 梯度传播稳定，不消失不爆炸。
- **Complexity (sC)**：直接用 FLOPs 作为代理，偏好用满计算预算的架构。
- **非线性排序聚合**：`sAZ(i) = Σ log(Rank(sM(i)) / m)` → 低排名代理被对数函数严重惩罚，无法被高排名"平均掉"→ 选出的架构在所有代理上都高分。

所有代理在**单次前向+反向传播**内同时计算（~42.7 ms/arch），无需特殊架构修改（如去 BN、限制非参数操作等）。

## 6. 结果证据 (Result & Evidence)

→ [[lee2024-aznas-results]]

- **NAS-Bench-201**：Kendall τ = 0.741 (CIFAR-10), 0.723 (CIFAR-100), 0.710 (IN16-120)，全面超越所有对比方法。Spearman ρ = 0.913/0.900/0.886。选出的架构精度接近 ground-truth 上限。
- **MobileNetV2 ImageNet**：450M FLOPs → 78.6% Top-1；600M → 79.9%；1000M → 81.1%，超越 ZiCo、ZenNAS 及多数训练-based 方法（OFA、ProxylessNAS 等）。搜索成本仅 ~0.4-0.7 GPU 天。
- **AutoFormer (ViT)**：Tiny 76.1-76.4%、Small 82.0-82.2%、Base 82.1-82.3%，超越 AutoFormer one-shot 和 TF-TAS，搜索成本仅 0.03-0.17 GPU 天。
- **消融实验**：单个代理 τ 0.349-0.578，组合两个 0.547-0.674，全组合 + NL 聚合 0.710-0.741。非线性聚合比线性聚合在每个配置上都有显著增益（如全组合：NL 0.741 vs. L 0.697）。
- **可迁移性**：将 AZ-NAS 代理融入 ZiCo 或 Synflow → Kendall τ 进一步提升（ZiCo+all 达 0.773/0.757/0.747），证明"组装互补代理"的范式通用。

## 7. 贡献 (Contribution)

1. **范式贡献**：首次系统地提出"组装多视角零成本代理"的训练-free NAS 方法论，证明从表达力、渐进性、可训练性、复杂度四个角度综合评估远优于单代理。
2. **技术创新**：
   - 基于 PCA 特征熵的表达力评分（各向同性检测），可检测死神经元和通道冗余
   - 基于 Jacobian Hutchinson 近似的可训练性评分，适用于任意 primary block 结构（包括非参数操作）
   - 基于块间表达力差的渐进性评分，自动鼓励渐进式特征扩展
   - 非线性 log-Rank 排序聚合，核心技巧简单但效果显著
3. **工程贡献**：所有代理可在单次前向/反向传播中同步计算，42.7 ms/arch 的运行时低于多数单代理方法，且不要求特殊的架构修改。
4. **实证贡献**：在 CNN（NAS-Bench-201、MobileNetV2）和 ViT（AutoFormer）搜索空间上均达到 SOTA，证明方法不依赖特定架构类型。

## 8. 核心知识点 (Core Knowledge)

1. **特征空间各向同性 (Isotropy)**：PCA 特征值的均匀程度反映了特征空间的利用效率——若某几个 PC 主导，说明发生了维度坍缩（dimensional collapse），网络有效容量被浪费。
2. **Hutchinson 估计**：利用 Rademacher 随机向量 v 满足 E[vvᵀ]=I 的性质，通过一次反向传播计算 `u = φ(v)` 获得 Jacobian 的迹或无偏估计。AZ-NAS 将其推广用于估计任意 primary block 的 Jacobian。
3. **渐进式宽度扩展原则**：现代架构（ResNet、MobileNet）通常后面的 block 更宽 → 这与"高维特征用于捕获语义"的直觉一致。sP 对这个原则做了量化。
4. **对数惩罚聚合**：log(Rank/m) 的非线性使低排名代理的惩罚不成比例地大——这与"木桶效应"的直觉一致：最短的板决定了整体水平。
5. **训练-free NAS 代理设计原则**：代理必须满足 (a) 正向相关（越高越好或越低越好）、(b) 互补（彼此 Kendall τ 较低）、(c) 高效（可一次前向/反向计算）。

## 9. Negative Knowledge (失败知识)

1. **单个代理远远不够**：sT 单独 Kendall τ 仅 0.349-0.407，低于 FLOPs 的 0.517-0.578。sP 单独也仅 0.489-0.521。如果只用单个代理，AZ-NAS 并不优于已有方法。
2. **渐进性代理对 ViT 失效**：在 AutoFormer 搜索空间上必须禁用 sP，因为 Attention 模块用高斯随机输入在初始化时会产生相似的注意力值，导致块间特征空间无法可靠区分。这揭示了**代理与架构类型的耦合性**——没有通用的零成本代理。
3. **线性聚合不够**：全 4 代理用线性聚合 τ = 0.663-0.697，远低于非线性的 0.710-0.741。简单的平均/求和忽视了低排名代理的警告信号。
4. **Jacobian 近似是线性假设**：把复杂的 primary block（含多种操作、多路径）近似为线性系统 Al ——对包含非线性较强的路径（如 ReLU 密集的 cell）可能不准确。论文未讨论这个近似误差的上界。
5. **只用高斯随机输入**：所有代理的输入是 N(0,1) 噪声——这意味着代理只评估了**初始化时的行为**，完全无法捕捉网络对真实数据的适配倾向。

## 10. 可迁移知识 (Transferable Knowledge)

1. **"组装互补代理"比"设计更强代理"更有前景**：将 AZ-NAS 代理融入 ZiCo/Synflow，τ 提高了 0.1-0.2。这暗示未来的训练-free NAS 可以走"轻量代理组合"而非"深度代理优化"的路线 → 类似 ensemble learning 的逻辑。
2. **非线性排序聚合是通用工具**：`log(Rank/m)` 聚合可应用于任何多代理或多指标场景，不限于 NAS。例如多目标 NAS 中处理精度-延迟 trade-off，或多任务学习的综合评分。
3. **PCA 熵可用于网络诊断**：sE 可作为网络初始化质量检测工具——检测是否发生维度坍缩、是否有死神经元风险、通道是否冗余。这可以独立于 NAS 使用。
4. **Hutchinson 方法推广**：将 Jacobian 谱范数估计从纯线性层推广到任意复合块（残差块、attention 块、cell 结构），为分析复杂模块的梯度动力学提供了实用工具。
5. **FLOPs 作为代理并非"退步"**：AZ-NAS 明确将 FLOPs 作为一个正相关代理使用，背后逻辑是"在给定预算内最大化计算利用率"——这不同于一般的"FLOPs 越小越好"的约束式使用。

## 11. 研究机会 (Research Opportunities)

1. **数据感知的代理设计**：AZ-NAS 用高斯随机输入——能否在保持高效的约束下，引入少量真实数据（甚至 1-2 张），让代理同时捕捉网络对真实数据分布的适配性？
2. **ViT 专用渐进性代理**：sP 对 ViT 失效说明需要为 Transformer 族设计专属的"特征扩展深度监测"指标。注意力熵、token 多样性的深度演化可能是候选方向。
3. **代理自动选择与加权**：AZ-NAS 的 4 代理是手工挑选的——能否用类似 [[eznas]] 的进化方法自动发现适用于特定搜索空间的代理组合？或自动学习代理权重？
4. **理论收敛性保证**：Hutchinson 近似的误差界、PCA 熵的统计性质、非线性聚合的最优性——目前都偏经验。需要理论工作建立这些代理与泛化误差的定量联系。
5. **更大搜索空间的 scaling**：AZ-NAS 的 42.7 ms/arch 在 NAS-Bench-201 上很快，但在 10¹² 级别的搜索空间上仍需要数 GPU 天。能否结合 surrogate model 做两阶段搜索？

## 12. 可复现性 (Reproducibility)

**复现性评级：高。** 官方代码开源（cvlab-yonsei/AZ-NAS），实验设置详尽：NAS-Bench-201 的结果可一键复现；MobileNetV2 和 AutoFormer 的搜索配置完整给出。表 1 中的所有对比方法结果均用原作者官方代码复现，且随机搜索的 3000 个架构集合在方法间共享（公平对比）。

潜在复现障碍：① MobileNetV2 训练配置引用 [39, 40]——但某些细节需跨论文查找；② AutoFormer Base 的训练 epoch 数被减半以"避免过拟合"，但减少的理由依赖经验判断；③ 文中提到使用单个 batch（batch size=64）的高斯随机输入——如果 GPU 显存不足需调整 batch size 或使用 FP16，可能影响代理分数。

---

## 关联页面

- [[az-nas]] — AZ-NAS 方法实体页面
- [[lee2024-aznas-method]] — 方法机制详解
- [[lee2024-aznas-results]] — 实验证据详解
- [[lee2024-aznas-critical]] — 贡献 / 失败知识 / 研究机会
- [[te-nas]] — TE-NAS：另一个双代理训练-free NAS 方法
- [[eznas]] — EZNAS：遗传编程自动发现零成本代理
- [[training-free-nas-transformers]] — 训练-free NAS 在 Transformer 上的探索
- [[nasbench201]] — NAS-Bench-201 基准数据集

## Evidence By Source

### `sources/papers/lee2024-aznas.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/aznas_lee2024.pdf`

^[sources/papers/lee2024-aznas.md]
