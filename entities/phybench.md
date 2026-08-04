---
type: entity
title: PHYBench
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
- entity/dataset
methods:
- human-curation
- question-formulation
- expert-review
- human-baseline
- symbolic-expression-evaluation
- test-time-scaling
- perturbation-testing
results:
- 500-problems
- human-baseline
- model-ranking
- EED-score
- accuracy
- robustness-analysis
failure_modes:
- topic-imbalance
- olympiad-level-bias
- text-only
- data-contamination
- flawed-items
- semantic-reasoning
- superficial-reasoning
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
id: entity--phybench
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- physics-reasoning
- scientific-reasoning
- benchmark
- evaluation
- data-contamination
- reproducibility
- human-curation
- question-formulation
- expert-review
- human-baseline
- symbolic-expression-evaluation
- test-time-scaling
- perturbation-testing
- 500-problems
- model-ranking
- EED-score
- accuracy
- robustness-analysis
- topic-imbalance
- olympiad-level-bias
- text-only
- flawed-items
- semantic-reasoning
- superficial-reasoning
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
# Dataset entity: PHYBench

^[sources/papers/qiu2025-phybench.md]

## 1. 定义

PHYBench 是 Qiu 等人在 2025 年论文中提出的、面向大语言模型 physical perception and reasoning 的物理推理 benchmark。最终数据集包含 500 道 text-only 物理问题，要求模型从给定情境推导一个单一的符号表达式；数据集实体对应论文总览 [[qiu2025-phybench-analysis]]。

## 2. 构造证据

- 覆盖 mechanics、electromagnetism、thermodynamics、optics、modern physics 和 advanced physics。
- 难度从高中物理到本科课程和 Physics Olympiad。
- 178 名北京大学物理学院学生参与题目贡献、改写和完善。
- 题目经过 Question Bank、专家审核、Reviewer’s Library 和人类评估等环节。
- 81 名北京大学学生参与最终人类评估，其中 50 人为中国物理奥林匹克金牌级选手。
- 757 道 Reviewer’s Library 题目中保留 500 道，论文报告 reservation rate 为 66.1%。
- 题目要求变量定义清楚、物理条件精确、答案唯一且无需外部知识；允许等价的符号表达式形式。

## 3. 评测接口

统一 prompt 要求逐步解答，并将可读的 LaTeX 最终答案放入 `\boxed{}`。

评测同时使用 binary accuracy 与 [[entities/eed-score]]；后者对 canonical SymPy expression tree 计算结构相似度并给部分得分。

论文报告 PHYBench 平均输出更长、平均分更低，并能更清楚地区分 reasoning 与 general models；逐项数字见 [[qiu2025-phybench-results]]。

## 4. 边界与失败模式

- 论文明确指出题目以 Olympiad-level 难度为主，主题分布不均，不能直接外推到 research-level reasoning。
- 数据集是 text-only，不覆盖图像、实验装置或视觉物理感知。
- 论文称题目为 original 且不易通过互联网直接搜索，但构造中包含对物理练习的改编，提供文本不等于完整的预训练污染审计。
- 题目最终答案以符号表达式为中心，不能单独评估完整中间推理过程。

## 5. 关联页面

完整方法：[[qiu2025-phybench-method]]。

实验结果：[[qiu2025-phybench-results]]。

指标实体：[[entities/eed-score]]。

## 6. 公开性

论文摘要称 benchmark results and dataset publicly available at [phybench.cn](https://www.phybench.cn/)。本证据文本没有提供专属代码仓库或逐题输出下载链接，因此记录为 medium reproducibility。
