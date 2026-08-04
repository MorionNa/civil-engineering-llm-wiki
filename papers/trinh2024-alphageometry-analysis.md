---
type: paper-analysis
title: Solving olympiad geometry without human demonstrations
authors:
- Trieu H. Trinh
- Yuhuai Wu
- Quoc V. Le
- He He
- Thang Luong
year: 2024
venue: Nature
tags:
- domain/ai4s
- evidence/paper
methods:
- large-language-models
- machine-learning
- formalization
- theorem-proving
- geometry
results:
- benchmark
- evaluation
- geometry
- olympiad
failure_modes:
- geometry
- formalization
- benchmark
datasets:
- geometry
- olympiad
- benchmark
reproducibility: medium
code_url:
- https://github.com/google-deepmind/alphageometry
dataset_url: []
id: paper--trinh2024-alphageometry-analysis
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- scientific-reasoning
- benchmark
- evaluation
- geometry
- olympiad
- machine-learning
- formalization
- theorem-proving
- reproducibility
- Nature
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Solving olympiad geometry without human demonstrations

^[sources/papers/trinh2024-alphageometry.md]

原始论文：Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He & Thang Luong，2024，Nature 625，476–482。DOI：<https://doi.org/10.1038/s41586-023-06747-5>。

本文研究 AlphaGeometry：一个面向欧氏平面几何定理证明的神经符号系统。论文不把人类证明翻译成机器可验证训练样本，而是从随机生成的定理前提出发，使用符号引擎生成定理—证明数据，再训练 Transformer 语言模型学习辅助点构造，并让符号引擎负责可验证的演绎步骤。论文将此框架用于 IMO-AG-30 测试集，并报告 30 题中解决 25 题。

## 1. 工程背景

> **⚙️ 非线性类型：** 该论文不涉及物理非线性。论文处理的是几何定理证明中的组合搜索、辅助构造和神经网络引导，不是 PDE 算子非线性、材料/本构非线性，也不是动力响应非线性（线性弹性）。

数学定理证明需要在潜在无限的动作空间中搜索一条到目标结论的路径。奥林匹克几何尤其难以转译为 Lean 等通用形式语言，导致机器可验证的人类证明样本稀缺（正文 p. 1，Methods pp. 8–9）。

工程上的关键瓶颈不是单纯的算力，而是两类任务的耦合：符号引擎可以快速穷举已知规则的推论，却不会自然地产生新的辅助点；语言模型可以生成候选序列，却可能产生语法或语义错误。因此，一个可审计的系统需要把神经生成限制在候选构造上，并把结论验证交给符号引擎。

## 2. Research Gap

已有几何定理证明器主要依赖计算机代数，或依赖带有人类设计启发式的搜索/公理化方法。前者可能给出判定但不提供人类可读证明，且在 IMO 规模问题上时间和内存开销较大；后者的辅助构造覆盖范围受手工模板和经验限制（正文 pp. 3–4）。

通用形式化语言中的几何数据不足，几何专用语言又无法覆盖许多人类证明会使用的复数、重心坐标和高阶定理。论文要填补的缺口是：能否完全从合成数据中学习辅助构造，而不依赖人类示范、人工挑选问题或人工策划证明数据。

## 3. 科学问题

核心问题是：给定一个几何定理的前提和目标，如何让模型在符号推理的无限分支点处提出有效的新对象，同时保持每一步能够被专用引擎验证？

论文进一步考察三个可检验问题：

1. 随机前提、符号闭包和 traceback 能否产生足以训练模型的多样定理—证明对？
2. 纯合成预训练是否能帮助语言模型理解其所连接的符号引擎，从而提高辅助构造成功率？
3. 由语言模型提出构造、由 DD+AR 完成演绎的交替搜索，能否在 IMO-AG-30 上超过现有搜索和计算机代数基线？

## 4. 研究目标

论文目标是建立 AlphaGeometry 框架，生成数以百万计、复杂度分层的几何定理与证明，训练一个从零开始的语言模型，并用它引导符号引擎完成欧氏平面几何证明。

评测目标包括：在可表示的经典几何 IMO 题上建立 IMO-AG-30；与 Wu 方法、Gröbner basis、DD、DD+AR、人类启发式以及 GPT-4 等基线比较；分析数据规模、预训练、微调、beam size 和搜索深度对结果的影响。

## 5. 方法机制

方法可以概括为“合成数据生成 → 纯符号预训练 → 辅助构造微调 → 神经—符号交替搜索”：

1. 以 constructive diagram builder 逐个采样一致的几何前提，避免自由采样造成自相矛盾。
2. 由 structured deductive database（DD）和代数推理引擎（AR）交替扩展推理闭包。
3. 用 traceback 从结论反向抽取最小前提集合和依赖子图，并用 dependency difference 识别证明中独立于目标对象的辅助构造。
4. 将前提、结论和证明序列化为文本，训练 Transformer 做 next-token prediction。
5. 推理时让语言模型每轮提出一条辅助构造；符号引擎加入新对象后重新计算闭包；对候选构造做 beam search，直到目标出现或达到最大迭代数。

方法细节见 [[trinh2024-alphageometry-method]]；实体关系见 [[entities/alphageometry]] 与 [[entities/alphageometry-synthetic]]。

## 6. 结果证据

在 IMO-AG-30 上，AlphaGeometry 解决 25/30 题；Wu 方法解决 10 题，DD+AR 加人类启发式解决 18 题，DD+AR 本身解决 14 题，GPT-4 直接生成自然语言证明解决 0 题（Table 1，正文 p. 5）。

只使用 20% 训练数据时解决 21 题；beam size 从 512 降至 8 时仍解决 21 题；搜索深度从 16 降到 2 时也解决 21 题（Extended Data Fig. 6）。

在 231 题的更大测试集上，AlphaGeometry 解决 98.7%，Wu 方法解决 75%，DD+AR 加人类启发式解决 92.2%（正文 p. 6；Extended Data Fig. 6b）。论文还报告模型解决了 2000 年和 2015 年 IMO 中的全部几何题，并由美国 IMO 队教练评估为可获满分的证明。

数据与消融结果的逐项记录见 [[trinh2024-alphageometry-results]]；限制与边界见 [[trinh2024-alphageometry-critical]]。

## 7. 贡献

- 提出不依赖人类示范的几何定理证明路线：用随机前提和符号引擎生成定理—证明数据。
- 将 DD 与 AR 统一为交替闭包引擎，使角度、比值、距离和几何常数的代数推理进入同一流程。
- 用 dependency difference 和 traceback 把辅助构造从合成证明中分离出来，让语言模型学习生成新对象。
- 建立 IMO-AG-30，并在该测试集上报告 25/30 的结果，超过论文比较的既有方法。
- 以 AlphaGeometry 展示一个可迁移的框架：目标领域需要对象与定义、随机前提采样器、符号引擎和 traceback 四个组件（Methods p. 10）。

## 8. 核心知识点

### 8.1 让模型学习“提出什么”，让引擎验证“是否成立”

DD+AR 对已知对象和规则进行确定性、可验证的演绎；语言模型只提出会引入新符号的辅助构造。这个职责分解同时利用了神经模型的生成能力和符号系统的精确性。

### 8.2 dependency difference 是训练信号

对结论节点 N，traceback 得到依赖子图 G(N) 及其最小前提 P。若某个对象参与证明但不属于结论对象的依赖，则它落在 dependency difference 中，可作为辅助构造学习信号，而不是被当作普通演绎步骤。

### 8.3 最小证明不是默认得到的

即使每个节点的直接祖先集合最小，完整依赖子图仍可能含有冗余辅助点。论文通过删除辅助点并重复运行 DD+AR 来检验目标可达性，保留试验中得到的最小证明。

### 8.4 数据的广度与人类审美不同

随机生成的定理通常不具有人类偏好的对称性，但能覆盖更宽的欧氏几何情形。论文报告生成数据中发现了部分已知定理，同时没有发现 IMO-AG-30 原题，说明训练集合与测试题之间没有简单的题目复制。

## 9. Negative Knowledge

- 适用范围被限定为可翻译到专用经典几何语言的欧氏平面几何；几何不等式和组合几何不在该测试环境内（正文 p. 4）。
- 该表示约能覆盖非组合几何 IMO 题的 75%，不是完整的 IMO 数学形式化方案；论文明确未直接解决 Lean 等通用语言的几何表示问题。
- 语言模型不保证发现证明。全设置仍有 5/30 题未解决；论文给出的 IMO 2019 P2 使用 barycentric coordinates，IMO 2008 P6 需要 Pitot theorem、homothety 等当前引擎没有的高阶工具（Extended Data Figs. 4–5）。
- 给出正确辅助构造也不保证成功：IMO 2008 P6 在提供人类证明中的辅助构造后仍未得到解，说明符号规则覆盖不足可能是独立瓶颈。
- 证明可验证不等于证明具有人类级可读性。对 IMO 2000 P6 和 IMO 2004 P1 的比较显示，AlphaGeometry 可能产生超过 100 步的低层演绎，代数中间步骤还可能被 Gaussian elimination 隐式吸收（Extended Data Figs. 2–3）。
- hypergraph traceback 中的最小生成树优化是 NP-hard；论文使用 greedy 算法，因此“最小”在这类情形是 best-effort，而不是全局最优保证（Methods p. 9）。
- AlphaGeometry 的人类比较只覆盖经典几何，且机器的二元解题计数与人类 IMO 分数的缩放比较是近似的，不能解释为完整 IMO 能力等价（Fig. 2）。
- 论文正文披露了代码和模型 checkpoint，但未给出独立的完整 100 million 合成语料下载 URL；仅凭论文不能确认从原始随机种子重建完全相同的训练语料和大规模运行轨迹。

## 10. 可迁移知识

该框架适合数据稀缺、但存在可执行符号引擎的形式推理领域。迁移时应先明确领域对象和定义，再设计不会生成矛盾状态的随机前提采样器；随后实现可扩展的符号引擎和能抽取最小依赖的 traceback。

“辅助构造”可以泛化为 exogenous term generation：模型负责在证明状态中提出尚未出现的对象、假设或中间表达式，验证器负责闭包、检查和证明输出。迁移不应只复制 Transformer 规模，还要复用数据生成、依赖差分和验证闭环。

论文的跨领域示例覆盖其他数学领域，但文本没有提供这些领域的完整实证结果。因此，迁移到不等式、组合数学、物理形式化或工程方程时，以下结论应视为研究假设而不是已验证效果。

## 11. 研究机会

- 引入 Reim theorem、Pitot theorem、homothety、复数和 barycentric coordinates 等高层工具，检验更强的符号规则是否同时提高覆盖率、搜索效率和证明可读性。
- 将高层证明大纲与低层可验证步骤结合，减少冗余辅助点和长链条，并评估人类专家对证明可读性的独立评分。
- 扩展 diagram builder 和专用语言，使其覆盖目前约 25% 的不可表示非组合几何题，以及不等式和组合几何。
- 公开或可再生成完整合成语料的版本化数据资产，报告随机种子、去重哈希、生成分布和训练/搜索成本，以提高独立复现能力。
- 将合成数据、目标题目上的 proof attempts 和 hindsight experience replay 结合，检验论文所述与 AlphaGeometry 正交的数据生成路线。
- 在其他领域按四个必要组件逐一做消融，而不是直接把几何上的神经—符号接口迁移过去。

## 12. 可复现性

等级：**medium**。

- 代码与模型 checkpoint：论文的 Code availability 指向 <https://github.com/google-deepmind/alphageometry>。
- 结果数据：论文说明支撑发现的数据位于 Extended Data 和 Supplementary Information，并提供 source data；但在预提取文本中没有独立数据集 URL，因此 dataset_url 保持为空。
- 方法披露：论文给出了 151 million 参数 Transformer（不含输入/输出 embedding）、12 层、1,024 embedding dimension、8 个 attention heads、4,096 dense layer、757 词表、1,024 token context、5% dropout，以及预训练 10,000,000 steps、微调 1,000,000 steps 等关键设置（Methods pp. 9–10）。
- 运行资源：数据生成使用 100,000 个 CPU workers、72 h，最终约 500 million 例去重为 100 million；测试搜索使用 4 个 GPU workers 和 10,000 个 CPU workers。大规模硬件并行度是复现成本的重要组成部分。
- 未确认项：提供文本没有证明完整合成训练语料、全部随机种子、所有 TPU 训练日志和与论文完全一致的端到端复现实验均可下载。因此不能把它标为 high，也不应声称已独立复现。

证据边界：以上数值均来自预提取 PDF 的摘要、正文、Table 1、Fig. 4–6、Methods 和 Extended Data Fig. 6；若代码仓库或补充材料后来发生变化，应重新核对，而不能由本页推断其当前状态。
