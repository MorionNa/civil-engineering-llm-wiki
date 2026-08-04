---
type: paper-analysis
title: 'PHYBench: Holistic Evaluation of Physical Perception and Reasoning in Large
  Language Models'
authors:
- Shi Qiu
- Shaoyang Guo
- Zhuo-Yang Song
- Yunbo Sun
- Zeyu Cai
- Jiashen Wei
- Tianyu Luo
- Yixuan Yin
- Haoxu Zhang
- Yi Hu
- Chenyang Wang
- Chencheng Tang
- Haoling Chang
- Qi Liu
- Ziheng Zhou
- Tianyu Zhang
- Jingtian Zhang
- Zhangyi Liu
- Minghao Li
- Yuku Zhang
- Boxuan Jing
- Xianqi Yin
- Yutong Ren
- Zizhuo Fu
- Jiaming Ji
- Weike Wang
- Xudong Tian
- Anqi Lv
- Laifu Man
- Jianxiang Li
- Feiyu Tao
- Qihua Sun
- Zhou Liang
- Yushu Mu
- Zhongxuan Li
- Jing-Jun Zhang
- Shutao Zhang
- Xiaotian Li
- Xingqi Xia
- Jiawei Lin
- Zheyu Shen
- Jiahang Chen
- Qiuhao Xiong
- Binran Wang
- Fengyuan Wang
- Ziyang Ni
- Bohan Zhang
- Fan Cui
- Changkun Shao
- Qing-Hong Cao
- Ming-xing Luo
- Yaodong Yang
- Muhan Zhang
- Hua Xing Zhu
year: 2025
venue: arXiv preprint
tags:
- domain/ai4s
- evidence/paper
methods:
- human-curation
- symbolic-expression-evaluation
- expression-tree-edit-distance
- bootstrap-analysis
- test-time-scaling
- perturbation-testing
- error-localization
- majority-voting
results:
- accuracy
- EED-score
- human-baseline
- sample-efficiency
- model-ranking
- robustness-analysis
failure_modes:
- oversimplified-tasks
- data-contamination
- flawed-items
- physical-perception
- semantic-reasoning
- symbolic-reasoning
- superficial-reasoning
- self-evaluation
- format-parsing
datasets:
- PHYBench
- MATH-500
- GPQA
- OlympiadBench
- AIME 2024
reproducibility: medium
code_url: []
dataset_url:
- https://www.phybench.cn/
id: paper--qiu2025-phybench-critical
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- physics-reasoning
- scientific-reasoning
- benchmark
- evaluation
- data-contamination
- machine-learning
- long-horizon
- reproducibility
- human-curation
- symbolic-expression-evaluation
- expression-tree-edit-distance
- bootstrap-analysis
- test-time-scaling
- perturbation-testing
- error-localization
- majority-voting
- accuracy
- EED-score
- human-baseline
- sample-efficiency
- model-ranking
- robustness-analysis
- oversimplified-tasks
- flawed-items
- physical-perception
- semantic-reasoning
- symbolic-reasoning
- superficial-reasoning
- self-evaluation
- format-parsing
- PHYBench
- MATH-500
- GPQA
- OlympiadBench
- AIME 2024
- arXiv preprint
sources:
- sources/papers/qiu2025-phybench.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# PHYBench — 批判性分析

^[sources/papers/qiu2025-phybench.md]

本页合并论文的贡献、核心知识、失败边界、可迁移知识与研究机会。具体机制见 [[qiu2025-phybench-method]]，数值证据见 [[qiu2025-phybench-results]]；可复用实体见 [[entities/phybench]] 和 [[entities/eed-score]]。

## 1. 贡献判断

### 1.1 Benchmark 贡献

PHYBench 的主要价值不只是把题目做难，而是把原创题目、物理情境、唯一符号答案、专家审阅和人类可解性检查放进同一评测协议。

论文报告 500 道最终题来自 757 道 Reviewer’s Library 题目，经过多轮 reviewer 返修和 81 名学生评估；这为“题目本身有问题导致的低分”提供了比未校准题库更明确的控制。

题目覆盖 mechanics、electromagnetism、thermodynamics、optics、modern physics 和 advanced physics，要求模型从文字关系构建长链推理。

### 1.2 EED 贡献

[[entities/eed-score]] 将最终 LaTeX 转成 SymPy 表达式树，并用扩展 tree edit distance 产生部分得分。

它把“系数小错但保留物理结构”和“结构完全不对”分开，且在论文的 bootstrap 分析中获得 204% 平均 sample-efficiency 提升。

### 1.3 诊断贡献

PP/RR 把第一次错误拆成物理情境感知错误与后续稳健推理错误；RR 内部再区分 semantic 与 symbolic reasoning。

chain-of-thought poisoning 则把“模型能否拒绝一个带错的中间步骤”变成可测条件，进一步区分 superficial、genuine 和 pseudo-genuine reasoning。

## 2. 核心知识

1. **复杂物理推理包含多个决策节点。** 模型可以读出变量并操作已有方程，却仍可能在“从物理语境生成新方程”时失败。
2. **最终答案评分与过程评分不是同一件事。** EED 解决的是表达式相似度，不等于对每一步物理因果链的验证。
3. **连续评分增加信息量。** 当题目很难、二值准确率集中在低分区间时，部分得分可以降低统计稀疏性；论文用 204% 的平均 sample-efficiency 量化这一点。
4. **pass@k 与 majority voting 测量不同能力。** pass@k 只说明候选答案空间中可能存在正确答案；投票提升小则说明模型的选择/自评机制仍弱。
5. **扰动响应比无扰动分数更能显示稳健性。** 同一模型在不同错误类型上的下降差异，揭示其使用的是语义修复、量纲/极限检查，还是上下文模式延续。

## 3. 失败边界

### 3.1 题库覆盖边界

论文明确指出，题目主要以 Olympiad-level 难度为主且不同物理主题分布不均；结果不能直接推广到研究级物理、真实实验设计或开放式科研问题。

题目是 text-only，因此论文没有测量图表、装置图、空间视觉输入或多模态物理感知。

尽管题目被称为 original，论文的构造说明仍包含由既有物理练习改编的过程；“不易通过互联网直接发现”降低了污染风险，但不等于经过独立的全量预训练语料排查。

### 3.2 评分边界

EED 只看 `\boxed{}` 中的最终表达式，不看中间推理是否包含错误前提、错误守恒律或不合法的物理假设。

表达式树节点近似等权，不能直接判断量纲、单位、符号约束、边界条件或物理可行性。

LaTeX/转换/计算失败直接记 0；这使格式遵循、解析器兼容性和推理正确性之间仍可能混淆。

子树折扣使整体分量的遗漏更平滑，但折扣函数和 `r` 的分段阈值仍是人为设定；提供的文本未给出对所有物理题型的语义校准证明。

### 3.3 实验与统计边界

API 模型采用各服务默认超参数，服务端版本、系统提示、推理预算和调用日期没有全部公开，因此跨时间复现会遇到外部状态变化。

TTS 只在选定子集和有限重复次数上执行，pass@k 的拟合上界不是无限采样下的观测事实。

人工基线来自北京大学物理学院学生，且 50 人为中国物理奥林匹克金牌级选手；它是有明确能力背景的专家组，不应无条件等同于所有物理学习者或科研物理学家。

论文报告若干模型的错误分布，但提供的文本没有逐题标注文件、完整模型输出或独立审阅者一致性统计，因此无法从文本单独审计全部错误标签。

## 4. 可迁移知识

### 4.1 对科学 benchmark 设计

- 先定义可验证的答案接口，再设计题目内容；如果答案形式不可规范化，后续评分会被格式噪声主导。
- 题目、参考答案和评测器需要共同质控；只审题干、不审答案提取会制造伪错误。
- 在公开题库中同时报告题目来源、污染风险和人类可解性，比单独声称“难”更有解释力。
- 用至少两个指标报告结果：一个 exact/binary 指标保持直观性，一个结构/连续指标提供部分正确性。

### 4.2 对结构化答案评测

EED 的“canonicalization → tree representation → structural distance → partial credit”链条可以迁移到数学表达式、程序 AST、符号推导和形式化语言。

迁移时需要重新定义：等价归一化规则、节点语义、分块/子树单位、错误成本以及领域约束检查；不能把 EED 的默认数字直接搬到其他任务。

### 4.3 对推理稳健性研究

给出正确/错误的部分轨迹，再要求模型继续，是一个低成本的上下文依赖实验。

扰动应覆盖“量纲可发现”“概念明显但量纲不报警”“物理定律直接反转”和“复合错误”等不同可见性，以避免只测一种错误。

PP/RR 与 semantic/symbolic 的标注框架也适合分析数学、程序合成和科学问答中的“新决策”与“已有状态变换”。

## 5. 研究机会

1. **物理约束 EED。** 在树编辑距离之外加入单位、量纲、守恒律、边界条件和极限行为检查，比较结构相似但物理无效的答案。
2. **过程级监督。** 公开逐步解与错误位置，训练 verifier 或 self-correction 模型，直接针对 semantic reasoning 而不是只优化最终表达式。
3. **分层 benchmark。** 按物理主题、难度、链长、所需定律数量和视觉依赖分层报告，检验分数差距来自哪里。
4. **多模态扩展。** 将 text-only 题扩展为图示、实验装置、场分布和观测数据，并把感知错误与推理错误分开统计。
5. **污染审计。** 对题目版本、来源和预训练语料做可审计的时间切分、近邻搜索和记忆测试，验证“原创性”是否真的改变模型暴露风险。
6. **可控的自评训练。** 用 pass@k 与 vote@k 的差距定义候选生成/候选选择缺口，训练模型识别和拒绝 poisoned CoT。
7. **跨领域验证。** 在数学表达式、程序 AST 和形式化证明中测试 EED 类指标，比较结构距离与语义/可执行性验证的互补性。
8. **公开运行基线。** 发布固定题库版本、完整输出、解析器版本、调用配置和随机种子，复核 204% sample-efficiency 以及 Table 6 的参数稳健性。

## 6. 可复现性审计

**等级：medium（中等）。** 论文给出了相当完整的题目约束、审核流程、EED 算法、统一 prompt、模型列表、部分解码参数、硬件与 bootstrap/TTS 设置；PHYBench 数据集和结果网站为 [phybench.cn](https://www.phybench.cn/)。

代码仓库在提供文本中未披露，`code_url: []`；论文也没有给出完整逐题输出、审阅 annotations、所有 API 版本和端到端执行脚本。因此可重建方法，但不能仅凭论文保证全部表格逐数字重现。

复现者还必须处理两个文本层面的歧义：EED 分段在抽取文本中对 `r=0.6` 未单独说明，且题目/模型/评测网站的版本状态可能变化。

## 7. 结论边界

最稳健的结论是：在论文定义的 500 道、text-only、原创并经人工校准的物理符号题上，当前模型与该人类基线有明显差距；EED 在该数据和参数范围内比 binary accuracy 更具样本效率；模型对多步语义推理和错误中间轨迹仍不稳健。

不应把这些结论扩大为“模型没有物理知识”“EED 能验证完整思维过程”或“pass@k 上界等于可部署可靠性”。这些表述超出论文提供的证据边界。

相关页：[[qiu2025-phybench-analysis]]、[[qiu2025-phybench-method]]、[[qiu2025-phybench-results]]、[[entities/phybench]]、[[entities/eed-score]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[qiu2025-phybench-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | https://www.phybench.cn/ |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
