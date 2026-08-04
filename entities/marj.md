---
type: entity
title: MARJ (Model-Assistant Rule-based Judgment)
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
- entity/model
methods:
- MARJ
- rule-based-judgment
- model-based-judgment
- answer-normalization
- human-evaluation
results:
- evaluation
- human-evaluation
- benchmark
failure_modes:
- evaluation
- physics-reasoning
- large-language-models
- scientific-reasoning
datasets:
- UGPhysics
- undergraduate-physics-problems
reproducibility: high
code_url:
- https://github.com/YangLabHKUST/UGPhysics
dataset_url:
- https://github.com/YangLabHKUST/UGPhysics
id: entity--marj
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- physics-reasoning
- benchmark
- evaluation
- scientific-reasoning
- reproducibility
- MARJ
- rule-based-judgment
- model-based-judgment
- answer-normalization
- human-evaluation
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
# Algorithm entity: MARJ

^[sources/papers/xu2025-ugphysics.md]

## 1. 定义

MARJ 是 Model-Assistant Rule-based Judgment 的缩写，是 UGPhysics 配套的答案正确性评测流水线。它不是被评测的物理求解模型，而是一个“规则优先、模型兜底”的两阶段判定器。论文总览见 [[xu2025-ugphysics-analysis]]，完整方法见 [[xu2025-ugphysics-method]]。

## 2. 输入与级联结构

算法接收问题 (P)、参考解答 (S)、黄金答案列表 (GT)、模型解答 (s) 和模型答案列表 (A)。

1. 若 (A) 与 (GT) 的答案数量不一致，直接返回 False。
2. 第一阶段按答案类型做规则匹配：直接相等、标准化、数值容差、常数归一化或区间端点比较。
3. 若规则阶段未接受答案，将问题、参考答案和模型输出整体交给第二阶段 GPT-4o judge。
4. 多答案题按列表顺序处理；论文正文说明只要有一个答案偏离黄金答案，整体规则结果标记为 False。

因此，MARJ 的核心不是两个 judge 的平均，而是把可精确计算的案例留给规则，把复杂表达式交给模型解释。

## 3. 类型化规则

- **TF/MC：** 将模型答案与黄金答案变换为同一标准形式后比较。
- **NV：** 转换为科学记数法，只比较基数并允许相对误差，以覆盖单位差异或舍入。提供文本中该误差阈值的指数损坏，具体阈值无法从提供文本确认。
- **EX/EQ：** 删除物理常数后归一化，再按表达式或方程比较。
- **IN：** 读取区间两个端点，把端点视作 NV 或 EX 后比较。
- **Compound：** 按多个原子答案的顺序处理，先检查答案列表长度。

物理常数清单见论文 Appendix Table 16，包含光速、引力常数、Avogadro 常数、气体常数、基本电荷、电子/质子质量、真空介电常数、真空磁导率、Planck 常数、Boltzmann 常数等。去除常数与数值容差是物理领域专用的归一化假设。

## 4. 模型复核阶段

规则阶段标记为 False 的案例由 GPT-4o 评估。few-shot judging prompt 要求模型注意题目中给出的物理常数和等价量；论文称该长 prompt 将在代码仓库中发布。该设计提升了规则系统面对复杂答案时的灵活性，但使 MARJ 依赖 GPT-4o 的版本、提示和物理判断能力。

## 5. 论文证据

在随机抽取的 100 个测试例上，MARJ 与人工 gold standard 的 accuracy 为 98%（Section 5.2）。作者还报告，Sympy 对容易直接验证的答案很高效，而 MARJ 能处理不适合纯规则判定的复杂答案，详见 [[xu2025-ugphysics-results]]。

## 6. 适用范围与失败边界

- 适合 UGPhysics 这类答案确定、可抽取、答案类型已知的文本物理题。
- 不应把它当作开放式证明质量、教学解释质量或含图物理推理的通用评审器。
- 98% 只来自 100 个样本，论文未提供按学科/答案类型的完整误差矩阵或大规模人工复核。
- 规则阶段的物理常数删除、区间端点比较和数值容差可能把某些物理上有条件的等价性简化掉。
- 第二阶段使用 GPT-4o；论文未在提供文本中给出与多个独立专家 judge 的系统消融，因此无法把 98% 分解为规则阶段和模型阶段各自的贡献。

## 7. 关联页面

数据集实体：[[entities/ugphysics]]；方法页：[[xu2025-ugphysics-method]]；总体分析：[[xu2025-ugphysics-analysis]]；结果与人工验证：[[xu2025-ugphysics-results]]；批判边界：[[xu2025-ugphysics-critical]]。
