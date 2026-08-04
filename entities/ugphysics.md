---
type: entity
title: UGPhysics benchmark
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
- entity/dataset
methods:
- benchmark
- evaluation
- data-contamination
- zero-shot-evaluation
results:
- benchmark
- evaluation
- data-contamination
- error-analysis
failure_modes:
- data-contamination
- evaluation
- physics-reasoning
- scientific-reasoning
datasets:
- UGPhysics
- undergraduate-physics-problems
reproducibility: high
code_url:
- https://github.com/YangLabHKUST/UGPhysics
dataset_url:
- https://github.com/YangLabHKUST/UGPhysics
id: entity--ugphysics
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
- zero-shot-evaluation
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
# Dataset entity: UGPhysics

^[sources/papers/xu2025-ugphysics.md]

## 1. 定义

UGPhysics 是 Xu 等人在 2025 年提出的本科物理推理基准，用于评估大语言模型在文本物理问题上的解题能力。它不是物理仿真器或训练好的模型，而是带有参考解答、答案类型、物理学科/主题和推理技能标签的评测数据集。论文总览见 [[xu2025-ugphysics-analysis]]，方法细节见 [[xu2025-ugphysics-method]]。

## 2. 规模与组织

- 5,520 道源问题；原题为中文并翻译成英文，论文称双语文本实例共 11,040。
- 3 个域：Mechanics & Thermodynamics、Electromagnetism、Modern Physics。
- 13 个本科物理核心学科、59 个主题、4 个难度等级。
- 7 种答案类型：NV、EX、EQ、IN、TF、MC 和 compound。
- 4 类主要物理推理技能：Knowledge Recall、Laws Application、Math Derivation、Practical Application；其他题标为 Others。
- Table 2 报告平均题目长度 82.4 tokens、平均解答长度 318.5 tokens、平均答案数 1.34。

## 3. 构建证据

题目来自中国科学技术大学的七本科大学物理习题书。作者使用 Mathpix 将 PDF 转为 LaTeX，并人工复核原始 PDF 与转换结果，再整理成 Problem–Solution–Answer 格式。模型 embedding 被用于去除潜在重复或相似题；含图题被排除。

渐进题被拆为独立问题，并补回后续小问所需信息。估计、证明和解释等缺乏确定答案的题被过滤，以使最终答案可以自动判定。题目先为中文，之后翻译为英文以支持双语评测。

## 4. 证据与用途

UGPhysics 支持按域、学科、主题、语言、答案类型和推理技能报告 LLM 准确率。论文用它评估 31 个模型，并报告 OpenAI-o1-mini 主叙述总体准确率 49.78%、DeepSeek-R1-Distill-Llama-70B 40.17%；Table 5 另列的新增 DeepSeek-R1 为 56.34%，与摘要/正文排名陈述存在未解释的口径差异，详见 [[xu2025-ugphysics-results]]。

论文还用 5-gram 预测检测若干模型的潜在数据污染，并对 100 个 OpenAI-o1-mini 错误样本做人类失败类型标注。UGPhysics 的答案判定由 [[entities/marj]] 支持。

## 5. 适用边界

- 只包含文本题，不能直接衡量图像、实验装置和多模态物理理解。
- 过滤了开放式估计、证明和解释题，结果更接近“可自动判分的本科物理解题”而非完整教育评价。
- 论文未在提供文本中披露每本习题书的完整书目、逐题翻译审计、去重 embedding/阈值和全部人工标注明细。
- 泄漏检测只覆盖若干模型子集；低污染比例不能证明整个题库对所有模型都无记忆污染。

## 6. 关联页面

数据集方法与构建流程：[[xu2025-ugphysics-method]]；实验数值：[[xu2025-ugphysics-results]]；失败边界：[[xu2025-ugphysics-critical]]；答案判定算法：[[entities/marj]]。
