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
id: paper--qiu2025-phybench-analysis
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
# PHYBench: Holistic Evaluation of Physical Perception and Reasoning in Large Language Models — 分析

^[sources/papers/qiu2025-phybench.md]

本文分析基于论文预提取文本（arXiv:2504.16074v2，论文首页标注为 2025-05-18 的 arXiv preprint）。方法细节见 [[qiu2025-phybench-method]]，实验数字见 [[qiu2025-phybench-results]]；数据集实体页为 [[entities/phybench]]，指标实体页为 [[entities/eed-score]]。

## 1. 工程背景

> **⚙️ 非线性类型：** 该论文不涉及物理非线性。PHYBench 的对象是大语言模型对物理题的感知、推理与表达式作答能力，而不是提出或求解 PDE 算子、材料/本构关系或线弹性下的动力响应模型；数据中的物理情境可能包含复杂动力学，但论文贡献属于 benchmark 与评测方法。

论文把 LLM 评测视为一个工程测量问题：如果题目过于简单、可能被预训练数据污染，或参考答案本身有错误，分数就不能稳定反映推理能力（§1；Appendix A）。

PHYBench 将问题约束为文本描述的物理情境与一个需要推导的符号表达式，要求模型从空间关系、相互作用和多个物理定律中构造长链推理（§3.1）。

该设置关注的是“能否从物理描述建立正确关系并保持推理一致性”，而不只是选择题、短数字答案或记忆事实。

## 2. Research Gap

论文指出现有 reasoning benchmark 的缺口有三类：

1. 任务过度简化，模型在 MATH-500 等数据集上的高分可能造成饱和，难以继续区分模型。
2. 题目来自公开网页、教材或考试的比例较高，模型可能在预训练阶段见过它们，产生潜在 data contamination。
3. 高难度题目的题干、答案提取与评分缺少充分验证，错误题目会把 instruction-following 或标注噪声混入推理分数。

论文还认为二值准确率不能区分“保留物理结构但系数有误”和“表达式结构完全错误”两类输出；人工过程评测虽然细致，却难以大规模执行（§2、§3.3）。

因此，研究缺口同时存在于题目构造、数据污染控制、质量校准和答案评分四个环节，而不只是缺少一个更难的题库。

## 3. 科学问题

论文考察的核心问题是：

- 一套全新且经过专家/人类校准的物理题，能否让当前推理模型显露出与人类专家的差距，并区分不同模型的推理能力？
- 将答案表示成 SymPy 表达式树后，树编辑距离能否提供比 exact-match/二值 accuracy 更细粒度的自动评分？
- 题目是否能诱发多步、多条件和长输出推理，而不是通过模式匹配或答案格式猜测完成？
- 模型的首次错误主要来自物理情境理解（physical perception, PP），还是来自在已理解情境上的后续稳健推理（robust reasoning, RR）？
- 在已有部分推理被注入错误时，模型能否发现、修复或盲目传播错误？

## 4. 研究目标

论文的目标可概括为四项：

1. 构建包含 500 道原创物理问题的 PHYBench，覆盖 mechanics、electromagnetism、thermodynamics、optics、modern physics 与 advanced physics。
2. 通过问题 formulation、专家审核、LLM 辅助审阅和大规模人类评估，筛除歧义、不可解或答案不唯一的题目。
3. 提出 Expression Edit Distance（EED）Score，以表达式树的相对编辑距离给出连续的答案相似度与部分得分。
4. 用多类 LLM、人类基线、跨 benchmark 对照、test-time scaling（TTS）及 chain-of-thought perturbation 诊断模型的推理边界。

## 5. 方法机制

论文方法由“题目构造—质量控制—符号评分—模型诊断”四层组成，完整展开见 [[qiu2025-phybench-method]]。

题目层面，最终答案必须是一个单一符号表达式；允许因子化、重排等等价形式，但拒绝方程式形式和浮点近似。题干需要定义所有变量、给出唯一可解释的物理条件，并能在不依赖外部知识的情况下求解（§3.2）。

质量控制从 757 个 Reviewer’s Library 题目中保留 500 道，论文报告 reservation rate 为 66.1%。初始题目由 178 名北京大学物理学院学生参与贡献、改写和完善；另有 81 名学生进行大规模人类评估，其中 50 人为中国物理奥林匹克金牌级选手（§3.2、§4.2）。

EED 流程从模型输出的 `\boxed{}` 中提取最终 LaTeX，预处理格式后用 `latex2sympy_extended` 转成 SymPy 表达式；再分别 simplify，并将表达式转成规则化的表达式树。

相对编辑距离为

\[
r=\frac{\operatorname{Distance}(T_{gt},T_{gen})}{\operatorname{Size}(T_{gt})}。
\]

树编辑操作包括节点插入、删除和替换；扩展的 Zhang–Shasha 算法还支持子树插入/删除，对大于 5 个节点的子树使用折扣成本，以更贴近“完整物理分量被遗漏”的情况。

模型评测同时报告 binary accuracy 与 EED。实验中 API 模型使用各服务默认超参数；本地模型使用 temperature=0.6、top_p=0.95、max_tokens=32,768，并在 4 张 80GB NVIDIA A100 上推理（§4.1）。

## 6. 结果证据

论文摘要和 Figure 1 报告，Gemini 2.5 Pro 是最高模型，accuracy 为 36.9%，EED Score 为 49.5；人类基线分别为 61.9% 与 70.4。

Table 1 在 DeepSeek-R1 上计算的 PHYBench 平均输出长度为 10,636 tokens、平均 accuracy 为 25.0；对应 MATH-500、GPQA、OlympiadBench、AIME 2024 的平均输出长度/准确率为 1,857/97.3、6,308/71.5、5,372/58.7、7,741/79.8。

论文 bootstrap 分析报告 EED 相对 binary accuracy 的平均 sample-efficiency 提升为 204%，标准差为 80%；作者将 500 道 EED 评分题的区分能力类比为约 1,500 道二值评分题。

在 7 个模型、50 道代表题的首次错误定位中，通常超过 90% 的错误属于 RR；在 RR 中超过 90% 属于 semantic reasoning，而非对已有方程做代数操作的 symbolic reasoning（§5.1；具体分布见 [[qiu2025-phybench-results]]）。

TTS 实验显示 pass@k 随样本数平滑提升并保持模型排序；majority voting 的提升通常只有几个百分点，而 pass@k 的提升可达数十个百分点（Appendix E）。

## 7. 贡献

**题库贡献。** PHYBench 把原创性、物理情境、多步符号答案和多轮人类校准放在同一条数据生产链中；论文将其定位为用于复杂物理推理的 human-curated benchmark。

**指标贡献。** [[entities/eed-score]] 将表达式相似度转成可解释的连续分数，弥补二值 exact-match 无法表达部分正确的问题。

**诊断贡献。** PP/RR 与 semantic/symbolic 两个轴把“第一次错在哪里”拆开，并用扰动后的部分解区分 superficial、genuine 与 pseudo-genuine reasoning。

**经验贡献。** 论文通过人类基线、跨 benchmark token/accuracy 对照和 TTS 实验，证明当前模型在该设置下与物理专家仍有明显差距。

## 8. 核心知识点

- 评测难度不等于题目数量；题目是否要求建立物理关系、组合多条定律并保持长链一致性同样关键。
- 原创题目可以降低潜在记忆污染，但不能自动保证题目无歧义，仍需要专家审核和人类可解性检查。
- 最终表达式树的相似性可以作为过程评测的低成本代理，但它仍然只观察最终答案。
- “能从错误解继续算下去”不等于“理解了物理”；T1–T6 扰动协议把错误检测与纠正能力显式化。
- 论文的错误分析表明，模型通常不是不会读出题目中的变量，而是在生成非直接蕴含的新物理方程时失败。
- EED 的区分力来自连续的部分得分和较低相对不确定性，而不是来自额外的模型裁判。

## 9. Negative Knowledge

- PHYBench 的题目主要覆盖高中到 Physics Olympiad/本科课程难度；论文明确承认题目以 Olympiad-level 为主且主题分布不均，因此不能直接外推到 research-level scientific reasoning。
- EED 只检查最终符号表达式的结构相似度，不评估完整中间推理；一个模型可能通过错误或不稳健的过程到达相近的最终表达式。
- EED 将表达式树节点近似等权处理，当前实现不显式检查量纲、物理可行性或守恒律；论文把 physics-informed/unit-analysis augmentation 列为未来方向。
- LaTeX 提取、格式化、转换或计算失败时分数直接为 0，这会把答案格式错误与推理错误混在一起，且论文指出 distilled models 更容易出现此类问题。
- 题目是 text-only，论文未证明该 benchmark 能评估真实视觉感知或多模态物理理解。
- TTS 的 pass@k 代表“从多个答案中存在正确答案”的上界型测量，不等于模型具有可靠的自我选择能力；majority voting 的弱提升反而说明选择机制仍有限。
- 论文没有给出本论文专属代码仓库；只有题库/结果网站 URL，无法据此声称端到端实验可无条件重跑。

## 10. 可迁移知识

- 在科学 benchmark 设计中，应把原创性、题干精确性、参考答案校验、人类可解性和评分协议当作一个闭环，而不是分开处理。
- 对具有结构化答案的任务，可以先做 canonicalization，再用结构距离提供部分得分；这一思路可迁移到方程、程序 AST 或形式化表达式，但需要任务特定的语义校验。
- 将错误定位拆成“情境建模/语义决策”和“既有表达式上的符号运算”，有助于区分数据、模型和工具链的责任。
- 用受控错误注入测试模型是否会盲目延续上下文，是检验 chain-of-thought 稳健性和 superficial reasoning 的可复用实验范式。
- bootstrap、pairwise confidence 和 TTS 曲线可以一起报告，避免只用单一平均 accuracy 做模型排名。

## 11. 研究机会

1. 将 EED 与量纲分析、守恒律、边界条件和物理可行性检查结合，构建过程感知且可扩展的物理评分器。
2. 扩大 PHYBench 的主题、难度和研究级问题覆盖，并报告按领域、难度与题型分层的统计，而不是只给总体分数。
3. 将 text-only 题目扩展为图、示意图、实验装置和时空场等多模态版本，单独评估感知错误与推理错误。
4. 研究能否利用 EED/过程标签进行训练、验证器学习或 test-time self-correction，直接改善 semantic reasoning。
5. 用公开模型、固定版本和公开逐题输出建立可审计的复现实验，验证 204% sample-efficiency 结论在不同模型和评分参数下是否稳定。

## 12. 可复现性

**等级：medium（中等）。** 论文给出了题目构造约束、审核流程、EED 计算步骤、统一 prompt、部分采样设置、硬件配置与统计方法；PHYBench 数据集和 benchmark 结果通过 [phybench.cn](https://www.phybench.cn/) 公开。

但论文文本没有给出本论文代码仓库，`code_url: []`；也没有在提供文本中列出可下载的逐题模型输出、全部标注审阅记录或完整运行脚本。因此，独立研究者可以重建主要方法和评测协议，但无法仅凭论文保证逐数字复现全部 API 实验。

复现时至少需要固定：题库版本、模型服务版本/日期、API 默认参数、局部模型解码参数、`latex2sympy_extended` 与 SymPy 版本、`\boxed{}` 提取规则、EED 的边界参数、bootstrap 重采样策略以及 TTS 的题目子集。

本页与子页的关系见 [[qiu2025-phybench-method]]、[[qiu2025-phybench-results]] 和 [[qiu2025-phybench-critical]]；实体入口见 [[entities/phybench]] 与 [[entities/eed-score]]。
