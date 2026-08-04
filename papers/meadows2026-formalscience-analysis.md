---
type: paper-analysis
title: 'FormalScience: Scalable Human-in-the-Loop Autoformalisation of Science with
  Agentic Code Generation in Lean'
authors:
- Jordan Meadows
- Lan Zhang
- André Freitas
year: 2026
venue: arXiv preprint
tags:
- domain/ai4s
- evidence/paper
methods:
- human-in-the-loop
- autoformalization
- theorem-proving
- lean-4
- mathlib
- language-agents
results:
- benchmark
- evaluation
- formalization
- physics-formalization
failure_modes:
- large-language-models
- physics-formalization
- theorem-proving
- evaluation
datasets:
- physics
- benchmark
- formalization
- lean-4
reproducibility: medium
code_url:
- https://github.com/jmeadows17/formal-science
dataset_url: []
id: paper--meadows2026-formalscience-analysis
status: active
project: civil-engineering-llm-wiki
keywords:
- formal-science
- autoformalization
- formalization
- theorem-proving
- proof-assistant
- lean
- lean-4
- mathlib
- physics-formalization
- physics-reasoning
- scientific-reasoning
- large-language-models
- language-agents
- human-in-the-loop
- benchmark
- evaluation
- physics
- arXiv preprint
sources:
- sources/papers/meadows2026-formalscience.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# FormalScience：科学自动形式化的可扩展人机协同管线

^[sources/papers/meadows2026-formalscience.md]

> 证据范围：论文 arXiv:2604.23002v1，2026-04-24，正文 §1–§7、Appendix A–D。正文的经验评估只覆盖 physics；“domain-agnostic”是管线设计目标，不是跨学科实证结论。

相关页面：方法机制见 [[meadows2026-formalscience-method]]；结果明细见 [[meadows2026-formalscience-results]]；批判性边界见 [[meadows2026-formalscience-critical]]；算法实体见 [[entities/formalscience]]；数据集实体见 [[entities/formalphysics]]。

## 1. 工程背景

> **⚙️ 非线性类型：** 本论文不涉及物理非线性。它研究科学推理从自然语言/LaTeX 到 Lean4 形式代码的自动形式化、编译验证和语义对齐；文本没有 PDE 算子、材料/本构关系或动力响应模型。因此，文中的 “alignment-validity trade-off”、LLM 推理难度和 semantic drift 不是 PDE 算子非线性、材料/本构非线性，也不是动力响应非线性。

科学研究中的推导通常以自然语言、LaTeX 和领域记号表达，而形式系统要求严格的类型、语法、库依赖和可编译证明。论文将这一落差视为科学验证、探索和事实核查的工程瓶颈，尤其指出 physics 中的 Dirac notation、vector calculus 和非交换算子会放大自然语言到形式语言的语义偏移。

大型语言模型提供了跨越 informal reasoning 与 formal language 的候选接口，但论文指出，任务复杂度上升或发生分布外迁移时，幻觉和语义/语法落差会加剧。FormalScience 的工程目标是让一个领域专家在不具备深厚形式语言经验的情况下，以较低成本生产可编译且尽量语义对齐的科学形式证明。

## 2. Research Gap

这里的“工程背景”属于科学软件与知识表示基础设施，而不是数值求解器或力学本构模型。论文的输出对象是可编译的 theorem/proof corpus；它是否保留物理量、算子、积分和坐标几何的含义，需要另行检查。

该区分对于计算力学知识库尤其重要：不能因为输入例子来自 physics，就把 FormalScience 归类为 computational mechanics 方法；论文没有给出网格、边界条件、材料参数、时间积分或 PDE 离散化实验。

论文也指出，数学库派生 benchmark 的库覆盖更完整，直接与 FormalPhysics 比较并不完全公平。FormalPhysics 的价值恰在于把形式系统的覆盖缺口显式暴露出来，而不是把所有领域对象强行映射成数学库中最容易证明的类型。

本文的工程问题可以概括为“如何在保留科学语义的同时获得可执行证明”，而不是“如何提高某个物理方程求解器的收敛率”。因此，后续复现应同时记录形式库覆盖、人工判断和 LLM 生成行为。

这也解释了为什么论文把 alignment 作为独立指标：同一段代码可以在 prover 中成立，却只保留原问题的代数外壳。该判断贯穿 [[meadows2026-formalscience-results]] 和 [[meadows2026-formalscience-critical]]。

现有 autoformalisation 工作主要围绕数学形式库和数学 benchmark；规模较大的库派生数据有污染风险，自动生成数据又可能浅层或低质量。论文认为，面向 science 的数据需要同时保留自然语言问题、非形式推导、形式陈述和完整 formal proof，而现有集合很少同时覆盖这四种对象。

physics 还存在形式系统能力边界：Lean4/Mathlib 不直接支持 vector calculus 或 Dirac notation，并且对基础导数、积分的支持不足。于是，“形式代码编译成功”并不自动意味着原始物理语义得到保存。论文将这一 validity 与 alignment 的分离作为核心研究空缺。

## 3. 科学问题

论文集中回答四个问题：

1. 能否用轻量的人机协同循环，从 equation-only derivations 生成带物理上下文的问答、Lean4 代码和无 sorry/axiom 的可编译证明？
2. 在没有人工对齐门控时，zero-shot、带编译错误反馈的 self-refinement、以及 agentic code generation 能否同时提高 formal validity 与语义 alignment？
3. 当物理记号不能原样进入 Lean4 时，编译器究竟验证了什么 surrogate statement？
4. 能否把 semantic drift 分类，并将每一类 drift 对应到可陈述的部分验证保证？

## 4. 研究目标

- 提出 domain-agnostic 的 FormalScience 人机协同 agentic semi-autoformalisation pipeline。
- 用该管线构造 FormalPhysics：200 个 university-level physics statement、非形式 LaTeX solution 和完整 Lean4 formal proof。
- 在同一数据集上比较 open-source 与 proprietary LLM，以及三种逐步增加推理时计算和符号反馈的推理管线。
- 用编译器的 formal validity、LLM-as-a-judge 的 formal quality/logical preservation/mathematical consistency，以及 drift taxonomy 同时审计语法和语义。

## 5. 方法机制

FormalScience 有四个阶段。第一阶段用 5 个 gold-standard statement-proof pairs 构造 few-shot template，把 200 个相关 derivations 分成每批 5 个的 40 批，并由 GPT-5.1 扩展问题、答案和物理上下文；专家循环检查 statement-proof alignment。第二阶段用 Lean4 + Mathlib 生成代码，编译器返回成功或 fatal error，LLM 据错误迭代纠正。

第三阶段由专家把 alignment 作为二分类门控：不接受时，用固定 prompt 生成改进，再重新编译；每个样本的最大 patience 为 3。第四阶段拆分 C1–C5、重新编译每个 proof，并修正后处理引入的错误。ChatGPT 界面约承担三分之一的样本，Claude Code + 自定义 Python Lean 编译脚本承担其余样本。

对照 agentic pipeline 则取消人工 alignment，使用 surface guard、结构/语义错误分类、完整重生成和最小 unified diff patch agent，在最多 25 次初始尝试和 25 次纠错中寻找可编译代码。详细机制见 [[meadows2026-formalscience-method]]。

## 6. 结果证据

FormalPhysics 包含 200 个例子，主要来自 quantum mechanics 与 electromagnetism，也含其他 physics 子域。Table 2 报告其平均自然语言 statement 含 6.41 ± 2.34 个对象和 6.22 ± 2.13 个公式；形式代码 formal validity 为 100.0%，formal quality 为 73.5%，logical preservation 为 72.0%，mathematical consistency 为 72.5%。

在 Table 3 的 GPT-4.1-mini judge 下，论文自己的 FormalScience（GPT-5.1 / Claude-4.5）达到 100.0% FV、73.5% FQ、72.0% LP、72.5% MC。最佳 open-source agent（GPT-OSS-20B）为 31.0% FV、73.0% FQ、72.5% LP、73.0% MC；GPT-5.1 的 zero-shot 和 self-refinement FV 分别为 14.5% 和 17.0%。

定性/定量 drift 分析显示，Notational Collapse 出现在超过 75% 的 QM proofs；正文还报告 Abstraction Elevation、Proof Strategy Substitution 和 Implicit Premise Selection 只占少数例子。预提取文本中的比较符号有编码损坏，因此这里不把其余类别的严格不等式或约数当作可靠数字。

## 7. 贡献

1. 一个把 informal statement/proof 扩展、Lean 编译纠错、人工 alignment 和后处理复核串起来的低成本管线。
2. 一个同时含 sNL、pNL、sFL、pFL 的 FormalPhysics corpus；论文将其定位为 evaluation benchmark，而非 fine-tuning corpus。
3. 对 zero-shot、self-refinement、agentic pipeline 和 FormalScience 的统一比较，明确展示 formal validity 与 semantic alignment 不能由同一个分数替代。
4. Notational Collapse、Abstraction Elevation、Proof Strategy Substitution、Implicit Premise Selection 四类 drift，以及“在 drift 存在时 Lean 实际验证什么”的解释框架。

## 8. 核心知识点

- 编译成功只保证形式对象和证明在给定 Lean4/Mathlib 环境中成立，不保证它仍然表达原始物理对象。
- 人工 alignment gate 是当前管线质量的关键部件；仅增加错误反馈或推理轮数并不能稳定解决物理语义丢失。
- physics 形式化的主要障碍不是把公式写成某种 Lean 语法，而是把 Hilbert-space/Dirac/vector-calculus 结构映射到已有类型和库。
- Drift 可以是破坏性的 surrogate verification，也可以是有益的 implicit premise selection；必须按类别解释保证，不能只看 FV。
- 小模型可能利用 compilation shortcut 获得较高 FV，却有很低的 LP/MC；符号工具需要足够强的 base LLM 才能被有效使用。

## 9. Negative Knowledge

- 不应把 100% formal validity 当作 100% physics correctness；FormalPhysics 的低 LP/MC 与 QM/EM 记号的替换正是反例。
- 不应直接把 zero-shot 或 naive error-based self-refinement 当作可靠的科学 autoformaliser。论文报告二者的 alignment 分数在主 judge 下几乎不变，self-refinement 还增加 token 使用。
- 不应只复制 Kimina-7B 的高 FV；它在 zero-shot 中 FV 为 51.5%，但 FQ/LP/MC 仅 6.5%/10.5%/9.5%，与语义保持相冲突。
- 不应把 30B 参数或更多 test-time scaling 视为充分条件；agentic 表现对 base model、上下文和符号工具协同高度敏感。
- 不应把本论文的跨域可扩展性当作已验证事实：实证只在 200 个 university-level physics examples 上完成，chemistry/biology 只是未来工作。
- 不应把 LLM-as-a-judge 的单一校准当作完备语义指标；第二个 7B judge 支持主趋势，但部分次级结论依赖 judge。

## 10. 可迁移知识

将“形式可执行性”和“语义对齐”拆成两个独立门槛，可迁移到其他科学语言代理和 theorem-proving benchmark。对编译错误先分 structural 与 semantic，再分别采用完整重生成和局部 patch，是可复用的 agent 设计。

在新领域中，先建立少量 gold examples，再让专家检查扩展结果，可能比直接大规模生成更容易控制语义。后处理拆分后再次编译也应成为数据管线的固定质量门。

更重要的迁移原则是记录“形式系统实际验证的 surrogate”：把领域记号折叠成 scalar、把计算提升为抽象代数、或把隐藏前提显式化，都需要单独标注，不能统一归为 proof success。相关算法和数据边界分别见 [[entities/formalscience]] 与 [[entities/formalphysics]]。

## 11. 研究机会

- 为 Lean4/Mathlib 补充 vector calculus、Dirac notation、非交换算子和物理单位/坐标几何的原生库，减少不得不接受的 drift。
- 建立不依赖单一 LLM judge 的 alignment metric，例如可执行的结构对应、领域专家抽样和形式对象 provenance。
- 把 drift taxonomy 变成训练/评估信号，训练 agent 先识别“不能忠实表示”的对象，再请求专家或换用领域库。
- 扩展到 statistical mechanics、general relativity、chemistry、biology，并报告跨域的成本、库覆盖和 contamination 审计。
- 研究无需持续人工逐条判定的 alignment protocol，同时保留 P=3 这类有限人工预算下的安全停止条件。

## 12. 可复现性

论文给出公开代码地址 https://github.com/jmeadows17/formal-science，并声称发布带 interactive UI 的 FormalScience codebase；但提供文本没有单独的 FormalPhysics dataset URL，因此 dataset_url 保持为空。基于“代码公开、方法和 prompt/算法附录较详细、数据地址与环境锁定信息未完整确认”，本页将可复现性评为 medium。

可复现线索包括：200 个相关 derivations、5 个 gold pairs、40 个 batch prompts、FormalScience alignment patience P=3、agentic baseline 的初始/纠错上限均为 25、Lean 编译结果作为 FV，以及 GPT-4.1-mini 与 Qwen2.5-Coder-7B-Instruct 两个 judge。具体 Lean4/Mathlib commit、完整原始数据发布位置、人工操作日志和每个模型的全部运行配置，论文提供文本未披露或无法确认。

源码与 benchmark 的关系、以及结果表的逐项证据见 [[meadows2026-formalscience-results]]；失败边界和可迁移建议见 [[meadows2026-formalscience-critical]]。
