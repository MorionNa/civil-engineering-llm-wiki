---
title: "Xiong et al. (2025) — ConfSeq 构象描述语言：3D 分子结构与 AI 的桥梁"
created: 2026-06-24
updated: 2026-06-24
type: paper-analysis
tags: [chemical-language-model, molecular-conformation, 3d-molecular-generation, sequence-modeling, transformer, drug-discovery, internal-coordinates]
sources: [raw/papers/10_1101_2025.05.07.652440.pdf]
methods: [sequence-modeling, internal-coordinates, dihedral-angle, pseudo-chirality, se3-invariance]
results: [conformation-prediction, molecular-generation, representation-learning, virtual-screening, state-of-the-art]
failure_modes: [rotatable-bond-dependency, force-field-reference, data-scarcity]
datasets: [geom-drugs, moses, chembl, bindingdb, dude, pcba]
reproducibility: medium
code_url:
  - https://doi.org/10.5281/zenodo.19706011
dataset_url:
  - https://github.com/learningmatter-mit/geom
confidence: high
---

# Bridging 3D Molecular Structures and Artificial Intelligence by a Conformation Description Language

> 预印本 2025.05 | 正式发表: *Nature Machine Intelligence* 2026, DOI: `10.1038/s42256-026-01250-8`

## 1. 工程背景 (Engineering Background)
> 为什么这个问题在工程上重要？不解决会怎样？

化学语言模型（CLM）通过 SMILES 等 1D 序列表示，已在 2D 分子建模（分子翻译、生成、表征）取得巨大成功。但分子性质不仅取决于 2D 拓扑，还取决于 3D 构象——这对理解物理化学性质、化学反应性和药物-靶标结合至关重要。若不解决 3D 分子建模问题，AI 驱动的药物发现将被限制在二维层面，无法充分利用结构生物学和计算化学的潜力。

## 2. Research Gap
> 已有研究缺了什么？核心矛盾是什么？为什么现有方法不行？

现有 3D 分子建模主要依赖图基扩散模型（GeoDiff、EDM、Torsional Diffusion 等），但这些方法面临三大瓶颈：(1) 架构复杂、推理慢（扩散需多步去噪）；(2) 生成可控性弱、缺乏排序能力；(3) 与 CLM 生态不兼容，无法复用 LLM 基础设施。关键的缺失在于**缺乏有效的 3D 分子构象 1D 序列表示**——没有它，语言模型无法直接处理 3D 分子结构。

## 3. 科学问题 (Scientific Question)
> 核心难题是什么？

**如何将连续的、无序的 3D 分子几何信息离散化为一维 token 序列，同时保持 SE(3) 不变性、人类可读性和简洁性？** 这不是简单的数值编码问题——需要一种语言设计，使标准 Transformer 能像处理自然语言一样处理 3D 分子构象。

## 4. 研究目标 (Research Objective)
> 本文想实现什么？

提出 **ConfSeq**——一种分子构象描述语言，将 SMILES 与内坐标（二面角、键角、伪手性）整合，天然保证 SE(3) 不变性。以此将构象预测、3D 分子生成、3D 表征学习统一转化为序列建模问题，用标准 Transformer 实现 SOTA。→ `[[xiong2025-confseq-method]]`

## 5. 方法机制 (Method & Mechanism)
> 本文方法如何工作？输入→输出是什么？为什么这样设计？

ConfSeq 在 SMILES 序列中嵌入三种内坐标 token：(1) **二面角** `<113>` 替换键 token——最关键，标准化算法为每个可旋转键分配唯一二面角路径；(2) **键角** `<30>|` 插在中心原子 token 后——仅针对非环、连接两个重原子的灵活角度；(3) **伪手性** `{`/`}`——区分非手性中心的可交换构象。所有角度离散化为整数值 token，序列顺序遵循 SMILES 原子序列。详细 → `[[xiong2025-confseq-method]]`

## 6. 结果证据 (Result & Evidence)
> 什么结果支撑结论？

- **构象预测**（GEOM-Drugs）：COV-P 47.9→58.4%，MAT-P 0.86→0.77Å，全面超越 Tor. Diff. 等所有基线
- **无条件生成**：PB-validity 0.83（+0.06），二面角 MMD 0.0062→0.0004，采样速度约 500× 于扩散模型
- **形状条件生成**：近 100% 化学有效性，3D 构象分布与训练集高度一致
- **3D 表征学习**：DUDE AUC 0.76 / PCBA AUC 0.60，优于 E3FP、LSalign、SHAFTS，可 1 分钟查询 9800 万 PubChem 化合物
- **药物发现**：发现多个 STING 抑制剂和 ALDH1B1 抑制剂（IC₅₀ = 0.338–3.51 μM）
详细 → `[[xiong2025-confseq-results]]`

## 7. 贡献 (Contribution)
> 本文新增了什么？

1. **ConfSeq 语言**：首个完整的分子构象 token 序列描述语言，天然 SE(3) 不变
2. **伪手性概念**：解决非手性中心构象歧义问题
3. **统一框架**：将 4 类 3D 分子任务统一为序列建模，复用标准 Transformer
4. **自评分能力**：自回归生成天然产生置信度评分，与 DFT 能量强负相关（ρ = -0.58）
5. **超大虚拟筛选**：预计算 9800 万分子嵌入，单 CPU 1 分钟完成全库 3D 相似性搜索
详细 → `[[xiong2025-confseq-critical]]`

## 8. 核心知识点 (Core Knowledge)
> 读完这篇论文应该记住什么？

1. **内坐标是 3D→1D 的桥梁**：二面角 + 键角 + 伪手性提供完整的 SE(3) 不变构象描述
2. **序列化 = 统一范式**：将异构的 3D 分子任务转化为 Transformer 可处理的序列建模，避免了为每个任务设计专用架构
3. **语言模型天然优势**：温度控制多样性、自回归评分、比扩散模型快 500×
4. **DIKW 层级**：ConfSeq 是"信息"层创新——好的表示设计（information）胜过复杂的模型架构（knowledge）

## 9. Negative Knowledge
> 风险、失败边界、不该照搬的做法？

- **可旋转键依赖**：二面角只对可旋转键有意义，刚性环系统贡献有限
- **力场参考偏差**：min RMSD 以 MMFF94 力场为参考，力场本身有系统误差
- **数据规模敏感**：生成任务需 43 万分子训练，小数据场景可能退化
- **键角覆盖不全**：仅编码非环、两重原子键角，环内和涉及氢/末端原子的角度被忽略
- **不应照搬**：直接拼接 3D 坐标字符串到 SMILES——破坏 SE(3) 不变性，LM 处理数值能力有限
详细 → `[[xiong2025-confseq-critical]]`

## 10. 可迁移知识 (Transferable Knowledge)
> 哪些经验可用于其他研究？

| 知识 | 如何迁移 |
|------|----------|
| 内坐标编码范式 | 其他需要序列化连续几何信息的领域（蛋白质骨架、材料结构） |
| 伪手性区分 | 任何需要区分不可区分构象的场景 |
| 标准 Transformer = SOTA | 不需要为 3D 任务设计复杂 GNN/扩散架构，语言模型 + 好的 token 化即可 |
| 自回归评分 = 免费 oracle | 利用生成概率评估候选质量，无需训练独立评分器 |
| 500× 加速 | 推理密集型任务（虚拟筛选）考虑序列模型替代扩散模型 |
详细 → `[[xiong2025-confseq-critical]]`

## 11. 研究机会 (Research Opportunity)
> 下一步可以研究什么？

1. **条件生成扩展**：口袋条件、药效团条件、多目标条件（活性+合成性+类药性）
2. **更大模型 + 更大数据**：扩展到数十亿参数，覆盖全 ChEMBL/ZINC
3. **蛋白质-配体复合物建模**：将蛋白质上下文编码入 ConfSeq
4. **构象动力学**：预测构象集合的温度依赖性分布
5. **对接集成**：ConfSeq 作为分子对接的前处理/后处理模块
详细 → `[[xiong2025-confseq-critical]]`

## 12. 可复现性 (Reproducibility)
> 代码和数据是否公开？

| 项目 | 说明 |
|------|------|
| **等级** | 🟡 中 |
| **官方代码** | Zenodo: `10.5281/zenodo.19706011`（ConfSeq 包，当前无文件） |
| **数据集** | GEOM-Drugs、MOSES、ChEMBL、BindingDB、DUD-E、PCBA（全部公开） |
| **协议** | CC-BY-NC-ND 4.0（预印本）；正式版 Nature 订阅 |
| **复现要点** | 需 RDKit + Indigo 生成 ConfSeq；数据增强策略（100×）对性能关键；Transformer 配置详见原文 |

## 关联页面
- `[[confseq]]` — ConfSeq 构象描述语言实体页
- `[[xiong2025-confseq-method]]` — 方法机制展开
- `[[xiong2025-confseq-results]]` — 实验结果展开
- `[[xiong2025-confseq-critical]]` — 贡献+Negative+可迁移+机会
