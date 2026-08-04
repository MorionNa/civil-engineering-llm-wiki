---
type: paper-analysis
title: 'UGPhysics: A Comprehensive Benchmark for Undergraduate Physics Reasoning with
  Large Language Models — Method'
authors:
- Xin Xu
- Qiyun Xu
- Tong Xiao
- Tianhao Chen
- Yuchen Yan
- Jiaxin Zhang
- Shizhe Diao
- Can Yang
- Yang Wang
year: 2025
venue: Proceedings of the 42nd International Conference on Machine Learning (PMLR
  267)
tags:
- domain/ai4s
- evidence/paper
methods:
- benchmark
- evaluation
- MARJ
- rule-based-judgment
- model-based-judgment
- zero-shot-evaluation
results:
- benchmark
- evaluation
- human-evaluation
- data-contamination
- error-analysis
failure_modes:
- physics-reasoning
- scientific-reasoning
- evaluation
- data-contamination
- large-language-models
datasets:
- UGPhysics
- undergraduate-physics-problems
reproducibility: high
code_url:
- https://github.com/YangLabHKUST/UGPhysics
dataset_url:
- https://github.com/YangLabHKUST/UGPhysics
id: paper--xu2025-ugphysics-method
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- physics-reasoning
- benchmark
- evaluation
- scientific-reasoning
- data-contamination
- reproducibility
- MARJ
- rule-based-judgment
- model-based-judgment
- zero-shot-evaluation
- human-evaluation
- error-analysis
- UGPhysics
- undergraduate-physics-problems
- Proceedings of the 42nd International Conference on Machine Learning (PMLR 267)
sources:
- sources/papers/xu2025-ugphysics.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# UGPhysics / MARJ — 方法机制

^[sources/papers/xu2025-ugphysics.md]

本页只展开数据构建、答案表示、MARJ 判定和 LLM 评测协议；总体 12 维概览见 [[xu2025-ugphysics-analysis]]，数值证据见 [[xu2025-ugphysics-results]]。MARJ 的可复用算法实体见 [[entities/marj]]，数据集实体见 [[entities/ugphysics]]。

## 1. 数据对象与总体结构

论文把 5,520 道本科物理源题组织为双语评测：原题最初为中文，之后翻译为英文，因此 Table 1 报告的文本测试实例为 11,040。数据覆盖三个域：Mechanics & Thermodynamics、Electromagnetism、Modern Physics；下分 13 个核心学科和 59 个主题（Figure 1、Table 2、Table 13）。

Table 2 报告的结构统计为：总问题数 5,520，语言数 2，域数 3，学科数 13，主题数 59，答案类型数 7，难度等级数 4；平均题目长度 82.4 tokens，平均解答长度 318.5 tokens，平均每题答案数 1.34。这里的“问题数”和翻译后的“文本实例数”是两个不同计数口径。

## 2. 题目收集与清洗

1. **来源。** 题目来自中国科学技术大学的本科物理习题资源“The Great Compendium of Physics Problems”，论文称共使用七本书。
2. **格式转换。** 团队使用 Mathpix 将原始 PDF 转成 LaTeX，再由团队人工检查和修正原 PDF 与 LaTeX。
3. **结构化。** 通过标记把内容整理为 Problem–Solution–Answer 格式，供模型生成和自动判定分离使用。
4. **去重。** 论文称基于模型 embedding 去除潜在重复或相似题目；提供文本未披露 embedding 模型、相似度阈值和保留/删除数量。
5. **文本约束。** 含图片的问题被排除，以把研究范围限定为文本物理推理；这也意味着数据集不是多模态基准。

## 3. 渐进题处理与可判定性筛选

物理题可能由多个连续小问组成，后续小问依赖前问答案或信息。论文将这类题拆成独立新题，并把所需上下文补回每个新题。与之相对，缺乏确定答案、无法稳定评估正确性的估计、证明和解释题被排除；Appendix A.1 给出 cosmic-ray flux 估计题和要求讨论介电常数的解释题作为例子。

这一步把基准的目标明确为“可自动判定的答案正确性”。它提升了规则评测可行性，但也改变了题目分布：开放式解释、证明质量和实验设计能力不在主评分中。

## 4. 双语构建与标注

所有题先以中文收集，再翻译成英文以支持双语评测。论文没有在提供文本中给出逐题翻译一致性审计、译者流程或人工翻译错误率，因此语言切片可用于评测，但不能据此自动推出两种语言完全等价。

题目按两组正交标签组织：

- **答案类型：** 六种原子类型加一种 compound 类型。compound 是按顺序排列的原子答案列表。
- **推理技能：** Knowledge Recall、Laws Application、Math Derivation、Practical Application；无法归入这些类型的题标为 Others。

论文使用 GPT-4o 作为技能分类器。技能定义分别强调公式/概念记忆、物理定律及其适用条件、从已知定律进行数学推导，以及在现实场景中建模并计算（Appendix A.3、Table 12）。

## 5. 七种答案表示

Table 3 与 Appendix Table 11 给出以下类型：

| 类型 | 缩写 | 机制要求 |
|---|---|---|
| Numerical Value | NV | 不含单位的数值；规则阶段转成科学记数法处理 |
| Expression | EX | 表达式；可做常数归一化 |
| Equation | EQ | 方程；可做常数归一化 |
| Interval | IN | 区间；比较两个端点 |
| True/False | TF | 布尔答案；先转换成统一形式 |
| Multiple Choice | MC | 选项答案；先转换成统一形式 |
| Compound | — | 多个按顺序排列的原子答案 |

提示模板要求模型给出推导过程并以显式的最终答案结束，同时约定答案中不包含单位，以便后续提取与匹配。

## 6. MARJ 的两阶段判定

MARJ（Model-Assistant Rule-based Judgment）接收问题 (P)、参考解答 (S)、黄金答案列表 (GT)、模型解答 (s) 和模型答案列表 (A)。Algorithm 1 的抽象流程是：

```text
若 len(A) ≠ len(GT)，返回 False
逐一比较 gt 与 a：
  先尝试直接相等
  再按答案类型做规则归一化
  任一答案匹配则记录通过
全部规则都未通过时，调用 ModelJudge(P, S, GT, s, A)
```

正文补充说明：多答案题逐一评估，若有一个答案偏离参考答案，整体规则结果为 False；模型判定阶段则把同一题的所有答案放进一个评估 prompt 中共同判断。

## 7. 第一阶段：类型化规则

- **TF/MC。** 将模型答案与黄金答案变换到同一标准形式后比较。
- **NV。** 把答案变成科学记数法，只比较基数，并允许相对误差以覆盖单位差异或舍入。提供文本中该阈值的负指数发生字符损坏，具体数值无法从提供文本确认；不要据此补写一个指数。
- **EX/EQ。** 删除物理常数后归一化，再分别按表达式或方程比较。物理常数清单见 Appendix Table 16，包含 (c,G,N_A,R,e,m_e,m_p,epsilon_0,mu_0,h,k) 等。
- **IN。** 读取两个端点，将端点视作 NV 或 EX 后比较。
- **答案数量。** 模型答案列表与黄金列表长度不同，直接判定 False。

这种规则阶段为易算、可规范化的答案提供高精度与效率；它不试图用字符串比较覆盖所有物理等价表达。

## 8. 第二阶段：模型复核

只有规则阶段标记为 False 的案例才进入第二阶段，由 GPT-4o 作为判定模型。作者手工设计了基于 few-shot 的长 prompt，要求判定器关注题目中定义的等价量和物理常数，处理规则系统不适合的复杂表达式。论文称该 judging prompt 将在代码仓库中发布。

因此 MARJ 不是“规则与模型投票”的对称集成，而是一个规则优先、模型兜底的级联：

\[
\text{MARJ}(x)=
\begin{cases}
\text{RuleMatch}(x), & \text{规则能处理并匹配};\\
\text{GPT-4o-Judge}(x), & \text{规则阶段标记为 False}.
\end{cases}
\]

第二阶段带来灵活性，同时将评测结果与 GPT-4o 的版本、提示和判断偏差绑定；人工验证规模只有 100 个随机测试例。

## 9. LLM 评测协议

论文评估 31 个领先 LLM，分为闭源商业模型、开源通用模型、数学专门模型和 o1-like 模型。代表性模型包括 OpenAI-o1-mini、GPT-4o、GPT-4o-mini、LLaMA-3.1/3.3、Qwen2.5、Qwen2.5-Math、DeepSeekMath、QwQ-32B-Preview 和 DeepSeek-R1-Distill 系列；完整清单在 Appendix B.1。

实验协议包括：

1. 零样本 prompt；按学科和答案类型定制模板，帮助答案抽取和规则匹配。
2. 使用 vLLM 加速开源模型评测。
3. 主体 Section 4.1 写明最大输出长度 4,096 tokens、greedy decoding、temperature 0；NuminaMath-CoT-7B 等受其 SFT 配置约束。
4. Appendix B.3 对 OpenAI-o1-mini 和 o1-like LLMs 写明最大输出长度 8,192；对 OpenAI-o1-mini 还说明 API 温度受限为 1。正文与附录的设置口径应在复现时逐项核对。

## 10. 数据污染检测

论文沿用 n-gram accuracy 思路：把题目和解答拼接，在随机选取的 (K) 个位置抽取 5-gram；如果模型预测的 5-gram 与数据集实际 5-gram 匹配，则把样本标记为 contaminated。Table 6 同时统计 contaminated 与 contaminated & Correct 两类数量/比例。

检测只在若干模型子集上执行。该流程能发现明显的记忆信号，但不是对训练语料完全去污染的证明；随机位置选择、模型 API 和 n-gram 预测协议都会影响检测灵敏度。

## 11. 人工验证与误差标注

MARJ 验证从测试例中随机抽取 100 例，人工先标注模型解答是否符合黄金答案，再将其作为 gold standard 与 MARJ 结果比较。论文报告 98% accuracy。另从 OpenAI-o1-mini 的错误答案中选取 100 例，由人工标注失败原因，形成 Figure 4 的错误分类。

## 12. 方法边界

方法适合文本、答案确定、可按类型抽取的本科物理题。它没有解决含图题、开放式证明或解释的自动评分；没有在本文中训练新的物理求解模型；GPT-4o 既参与技能标注又参与部分答案判定，可能引入同源模型偏差。去重模型和数值容忍阈值的完整实现细节需以公开仓库为准；若提供文本缺少某个实现参数，应标为“论文未披露/无法从提供文本确认”。

相关证据表和模型数值见 [[xu2025-ugphysics-results]]，贡献与可迁移边界见 [[xu2025-ugphysics-critical]]。
