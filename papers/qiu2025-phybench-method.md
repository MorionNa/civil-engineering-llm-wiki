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
id: paper--qiu2025-phybench-method
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
# PHYBench — 方法机制

^[sources/papers/qiu2025-phybench.md]

本页展开 [[qiu2025-phybench-analysis]] 的第 5 维，聚焦题目生产、EED Score、模型评测和诊断协议。数值结果集中在 [[qiu2025-phybench-results]]；可复现性判断见 [[qiu2025-phybench-critical]] 与 [[entities/eed-score]]。

## 1. 任务对象与答案接口

PHYBench 将每道题设计为一个具体物理情境，要求模型根据给定条件推导一个关键物理量的符号表达式（§3.1）。

题目覆盖 mechanics、electromagnetism、thermodynamics、optics、modern physics 和 advanced physics。

难度从高中物理、大学本科课程延伸到 Physics Olympiad 题目；论文强调这些题目不要求外部知识，难点在于从文字建立物理关系、选择定律、组合条件并完成长链推导。

最终答案接口有三个约束：

- 答案应是单个 symbolic expression，例如论文示例中的 `2mg + 4mv_0^2/l`。
- 允许等价的因子化、重排或其他表达式形式。
- 拒绝方程式形式和浮点近似，以便由符号等价与树结构进行自动比较。

题干也必须满足变量定义清楚、物理条件精确、解释唯一和无需未声明假设等要求（§3.2）。

## 2. 题目构造与质量控制

### 2.1 Problem formulation

论文称题目由原有物理练习改编、构造和完善而来，来源同时包含 non-public 与 publicly available problems，但作者称这些材料不容易通过直接互联网搜索或标准参考文献发现。

所有最终题目是 text-only，不包含 multimodal input。

每道题围绕现实或可解释的物理场景组织，并指定一个需要符号表示的目标量。

### 2.2 多轮审核管线

论文给出的流程可以写成：

`题目贡献/改写 → Question Bank → 专家审核与返修 → Reviewer’s Library → 人类评估 → PHYBench`

初始构造、改写和完善共有 178 名北京大学物理学院学生参与。

题目上传到内部 Question Bank 后分配给专家 reviewer；不符合 symbolic-answer、precise-statement 或可解性要求时，reviewer 直接修改或退回 contributor。

审阅者可以查看 o1、DeepSeek-R1 等 LLM 的 zero-shot 输出，借此发现歧义或误导性表述。

这些闭源模型只用于 evaluation/审阅辅助，不参与题目构造，也不访问 ground truth 或内部 annotations。

通过反复修改，直到模型输出能够稳定体现题目意图后，题目才进入 Reviewer’s Library。

最后有 81 名北京大学学生独立作答子集并反馈 clarity、solution uniqueness 和 potential ambiguity；其中 50 人为中国物理奥林匹克金牌级选手。

论文报告 Reviewer’s Library 中 757 题最终保留 500 题，reservation rate 为 66.1%。这 500 题构成最终 PHYBench，并用于人类基线。

## 3. EED Score 的输入预处理

EED Score 是 model-free 的最终表达式评分器，实体页见 [[entities/eed-score]]。

### 3.1 取出模型最终答案

统一 prompt 要求模型给出逐步解答，并把最终答案放入 `\boxed{}`。

评分流程先从字符串形式的 LaTeX 中抽取 `\boxed{}` 内容，忽略 box 外的额外文本。

论文说明，box 内允许有额外文字或命令，但必须只出现一个表达式。

之后移除格式命令和完整 `begin...end` 环境等非标准 LaTeX 结构，使结果可以被解析。

### 3.2 LaTeX 到 SymPy

规范化后的 LaTeX 由 `latex2sympy_extended` 转换为与 SymPy 兼容的 symbolic expression。

为提高 simplify 的计算效率，论文假设符号变量为 positive。

对 ground truth（gt）和 generated expression（gen）分别执行 SymPy `simplify()`。

准确率判定使用 `equals` 方法；论文描述该检查结合 symbolic simplification 与 numerical verification。

若格式、转换或计算阶段出现错误，EED 返回 0；论文特别指出 distilled models 更容易触发此类输入格式失败。

## 4. 表达式树与编辑距离

### 4.1 树表示

SymPy expression tree 将常数、变量、函数和基本二元运算表示为节点。

对 gt 与 gen 构造规则化的表达式树，分别记为 `T_gt` 和 `T_gen`。

基本编辑操作是节点插入、节点删除和节点更新/替换；算法寻找把 `T_gt` 变成 `T_gen` 的最小操作代价。

相对编辑距离定义为：

\[
r = \frac{\operatorname{Distance}(T_{gt},T_{gen})}{\operatorname{Size}(T_{gt})}。
\]

论文采用 dynamic-programming 的 Zhang–Shasha tree-edit-distance 算法。

论文给出的复杂度为时间 `O(n_1 n_2 d_1 d_2)`、空间 `O(n_1 n_2)`，其中 `n_i` 是树节点数、`d_i` 是对应树的最大深度。

作者认为对 PHYBench 的表达式规模，这一计算成本相对于 `simplify()` 的时间是可接受的。

### 4.2 分段评分

论文正文给出的默认评分为：

\[
\operatorname{score}(r)=
\begin{cases}
100, & r=0,\\
60-100r, & 0<r<0.6,\\
0, & r>0.6.
\end{cases}
\]

因此 exact match 得 100；小的结构或系数错误仍可获得最高 60 分区间内的部分得分；距离足够大的答案得 0。

提供的抽取文本没有单独说明 `r=0.6` 的边界归属，复现实现时应固定并公开该边界约定。

### 4.3 子树编辑折扣

单纯逐节点计数会把一个完整物理分量的遗漏拆成许多独立错误。

为此，论文加入 subtree insertion/deletion；子树大小为 `x` 时，成本为：

\[
\operatorname{Cost}(\operatorname{InsertTree}(T),\operatorname{DeleteTree}(T))
=\min\bigl(x,\;0.6(x-5)+5\bigr)。
\]

当 `x≤5` 时退化为普通节点成本；较大的整棵子树享受折扣。

作者把该设计解释为对“表达式中某个有物理意义的整体分量被删掉或插入”的更合理处理。

扩展后的算法仍使用 extended Zhang–Shasha，并保持论文给出的时间与空间复杂度形式。

## 5. Accuracy 与 EED 的并行评测

Accuracy 是二值的：

\[
\operatorname{score}_{ACC}=\begin{cases}
100,& \operatorname{equals}(\operatorname{simplify}(gt),\operatorname{simplify}(gen))=\text{True},\\
0,& \text{otherwise}。
\end{cases}
\]

EED 则利用相对树距离给部分分。

Figure 2 用三个回答示例展示同一个问题上，表达式完全等价、系数有误和结构性错误可以得到不同 EED 分数，而 accuracy 只保留正确/错误两档。

## 6. 模型、提示和硬件设置

API 模型包括 GPT-4o、GPT-4.1、o1、o3-mini、o3、o4-mini、Claude 3.7 Sonnet、Claude 3.7 Sonnet Thinking、Gemini 2.0 Flash Thinking、Gemini 2.5 Pro、DeepSeek-V3、DeepSeek-R1、Qwen2.5-max 和 Grok 3 Beta。

本地评测模型包括 DeepSeek-R1-Distill-Qwen-32B 与 QwQ-32B。

API 评测使用各服务的默认超参数。

本地模型使用 temperature=0.6、top_p=0.95、max_tokens=32,768。

推理使用四张 NVIDIA A100 Tensor Core GPU，每张显存 80GB。

Appendix D 的统一 prompt 为：要求模型作为 physics expert，阅读题目、提供 step-by-step solution，并把可读的 LaTeX 最终答案写在 `\boxed{}` 中。

自动评测只抽取 box 内部的 LaTeX，忽略 box 外内容。

## 7. 人类基线协议

81 名北京大学物理学院学生各分配 8 道题；论文最终获得 559 份、且属于公开 PHYBench 范围内的有效答卷。

人类同时按 accuracy 与 EED 评分，以便和模型使用相同的最终答案接口。

不确定性由 bootstrap 重采样估计；正文报告使用 10,000 次 bootstrap resamples 计算人类基线不确定性。

## 8. TTS 与跨 benchmark 对照

TTS 对 PHYBench 使用公开的 100 道题；AIME 2024 使用全部 30 题；OlympiadBench、MATH-500 和 GPQA 各抽取 72 题。

OlympiadBench 的 72 题由 36 道数学题和 36 道 physics、且后者标记为 `answer_type=Expression` 的题组成。

每个模型每道题评估 16 次；部分较小模型额外重复。

pass@k 取采样答案中的最高 accuracy/EED；majority voting 把等价表达式当作相同答案。

只有当题目中超过 90% 的样本数大于某个 k 时，图中才绘制对应点。

pass@k 的上界使用随 `x=log k` 变化的指数衰减拟合：

\[
Acc = Boundary - Gain\cdot\exp(-x/x_0)。
\]

其中 Boundary 是估计上界，Gain 是从增加采样数获得的总提升，`x_0` 是趋近上界的衰减尺度。

## 9. 错误定位协议

论文在 50 道代表题的 solution trace 中定位每个模型的第一次错误。

若错误来自抽象物理场景，如漏掉变量、误识别关键量或误解关系，标为 PP（Physical Perception）。

其他错误标为 RR（Robust Reasoning），包括选择错误公式、组合条件失败或无法完成推导。

RR 再分为 semantic reasoning 与 symbolic reasoning：前者生成不由先前方程直接蕴含的新方程，后者只对已有方程做化简、代入等逻辑操作。

该双轴标注将“理解物理情境的决策节点”和“沿推理链连接已有表达式的步骤”分离，具体比例见 [[qiu2025-phybench-results]]。

## 10. Chain-of-thought poisoning

扰动协议保留原题，截断参考解，并在部分解中注入一个系统性错误；随后给模型 `prompt → poisoned CoT → continue` 对话，要求它不要从 Step 1 重启。

八种条件由两个 baseline 和六种 toxin 构成：

- F1：只给原始问题。
- F2：给出正确的部分解，用于检查部分推理上下文本身的影响。
- T1：删除引力公式 `(R_m+h)^2` 的平方项。
- T2：把 `(R_m+h)^2` 改为 `(R_m-h)^2`，反转运算符。
- T3：同时使用 T1 与 T2，把它改成 `(R_m-h)`。
- T4：删除 `h` 项，保留平方，改成 `R_m^2`。
- T5：同时使用 T2 与 T4，改成 `R_m`。
- T6：改写 hydrostatic equilibrium 方程，反转物理依赖关系。

模型若盲目沿用有错的部分解，标志着 superficial reasoning；若通过语义理解修复错误，属于 genuine reasoning；若只通过量纲或极限等一致性检查修复部分错误，则属于 pseudo-genuine reasoning。

## 11. 机制假设与实现边界

EED 假设 gt/gen 都能成功转换成可比较的 SymPy 表达式；它不替代题目内容的物理验证。

“变量为 positive”的 simplify 假设可能影响符号等价，应在复现时显式记录。

最终答案抽取要求唯一 box 表达式，因此格式协议本身会影响得分分布。

模型 API 使用默认参数，服务版本、系统提示和推理预算未在提供文本中完全展开；这些是跨时间复现的关键变量。

## 12. 方法小结

该方法把 benchmark 设计、符号表达式规范化、结构距离评分和受控错误注入连接起来。

其逻辑链为：原创且审核过的物理题 → 可解析的单表达式答案 → canonical SymPy tree → 二值与连续评分 → 模型排名、TTS 和错误类型诊断。

与 [[qiu2025-phybench-analysis]] 的 12 维总览配合阅读时，应把 EED 看作最终答案评估器，而不是完整 reasoning trace verifier；结果证据详见 [[qiu2025-phybench-results]]，数据集边界详见 [[entities/phybench]]。
