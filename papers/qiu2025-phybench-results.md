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
id: paper--qiu2025-phybench-results
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
# PHYBench — 结果证据

^[sources/papers/qiu2025-phybench.md]

本页只整理论文正文、附录表格与图注中明确报告的实验/数值证据。方法机制见 [[qiu2025-phybench-method]]，总体解释见 [[qiu2025-phybench-analysis]]；EED 定义见 [[entities/eed-score]]。

## 1. 人类基线（§4.2）

| 项目 | 论文报告值 |
|---|---:|
| 参与学生 | 81 |
| 中国物理奥林匹克金牌级选手 | 50 |
| 有效答卷 | 559 |
| Accuracy | 61.9 ± 2.1% |
| EED Score | 70.4 ± 1.8 |
| 人类 accuracy 上四分位数 | 71.4% |
| 人类 EED 上四分位数 | 80.4 |
| 基线不确定性 | 10,000 次 bootstrap resamples |

论文报告，在 99% confidence level 下，人类专家在两个指标上均显著优于所有被评估的 LLM。

## 2. 主结果（摘要、Figure 1、Table 4）

摘要和 Figure 1 报告，Gemini 2.5 Pro 是最高模型，accuracy=36.9%，EED Score=49.5；人类基线为 accuracy=61.9%、EED=70.4。

Table 4 的 bootstrap 汇总使用另一组精确显示值；下表保留表中原值。`SEED` 为 EED 平均值，`ACC` 为 accuracy，`σ` 为标准差，`CV` 为相对标准差，Efficiency 为相对 ACC 的采样效率。

| Model | SEED | ACC | σEED | σACC | CVEED (%) | CVACC (%) | Efficiency |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gemini 2.5 Pro | 49.40 | 36.65 | 1.71 | 1.97 | 3.47 | 5.38 | 240.79% |
| o3 (high) | 46.30 | 34.58 | 1.72 | 1.91 | 3.71 | 5.53 | 221.48% |
| o4 mini (high) | 41.95 | 29.33 | 1.68 | 1.83 | 4.01 | 6.25 | 242.84% |
| DeepSeek-R1 | 37.78 | 24.88 | 1.59 | 1.71 | 4.20 | 6.87 | 267.24% |
| o3 mini (high) | 37.22 | 24.92 | 1.57 | 1.69 | 4.21 | 6.77 | 258.06% |
| o4 mini | 36.44 | 24.77 | 1.66 | 1.72 | 4.54 | 6.95 | 233.88% |
| o3 mini | 33.21 | 21.13 | 1.59 | 1.65 | 4.79 | 7.79 | 264.18% |
| Grok 3 Beta | 31.94 | 21.09 | 1.56 | 1.59 | 4.90 | 7.53 | 236.67% |
| Gemini 2.0 Flash Thinking | 30.25 | 17.93 | 1.48 | 1.51 | 4.88 | 8.40 | 296.31% |
| o1 | 27.46 | 10.72 | 2.03 | 1.27 | 7.40 | 11.86 | 257.09% |
| Claude 3.7 Sonnet Thinking | 27.12 | 15.25 | 1.44 | 1.43 | 5.30 | 9.40 | 314.68% |
| GPT-4.1 | 23.71 | 13.18 | 1.44 | 1.41 | 6.07 | 10.68 | 309.90% |
| DeepSeek-V3 | 24.17 | 13.45 | 1.39 | 1.38 | 5.75 | 10.27 | 318.79% |
| o3 mini (low) | 25.34 | 8.13 | 1.85 | 1.13 | 7.29 | 13.88 | 362.12% |
| Claude 3.7 Sonnet | 23.73 | 12.78 | 1.35 | 1.34 | 5.71 | 10.46 | 335.79% |
| GPT-4o | 15.35 | 6.89 | 1.11 | 1.04 | 7.26 | 15.12 | 434.02% |
| Qwen2.5-max | 13.92 | 6.03 | 1.04 | 0.96 | 7.44 | 15.83 | 452.20% |
| QwQ-32B | 4.54 | 1.58 | 0.94 | 0.51 | 20.77 | 32.26 | 241.21% |
| DeepSeek-R1-Distill-Qwen-32B | 3.19 | 0.70 | 0.71 | 0.35 | 22.30 | 49.56 | 493.72% |

论文在主文中据此报告：EED 与 accuracy 给出的模型排序几乎相同，但 EED 的分布更宽、相对统计不确定性更低。

## 3. 与其他 benchmark 的对照（Table 1）

Table 1 的 Average Output Tokens 与 Average Accuracy 均由 DeepSeek-R1 计算。

| Dataset | Data Scale | Avg. Output Tokens | Avg. Accuracy | Scoring Type |
|---|---:|---:|---:|---|
| MATH-500 | 500 | 1,857 | 97.3 | Binary |
| GPQA | 448 | 6,308 | 71.5 | Binary |
| OlympiadBench | 8K | 5,372 | 58.7 | Binary |
| AIME 2024 | 30 | 7,741 | 79.8 | Binary |
| PHYBench | 500 | 10,636 | 25.0 | Detailed |

## 4. EED 采样效率与模型区分（Appendix C）

论文使用 1,000 次 bootstrap resamples 分析两种评分的统计不确定性。

以 `Sample Efficiency=(CV_ACC/CV_EED)^2` 计算，EED 相对 accuracy 的平均提升为 204%，标准差为 80%。

论文将其解释为：在该 benchmark 上，500 道 EED 评分题可以提供约等于 1,500 道 binary accuracy 题的区分能力。

Table 5 报告 Gemini 2.5 Pro 相对于除 o3 外其他模型的 pairwise advantage confidence 为 99%，相对于 o3 为 90%。

Table 5 还显示，top performers（Gemini 2.5 Pro、o3、o4 mini）、mid-tier（DeepSeek-R1、o3 mini）、non-reasoning（GPT-4.1、DeepSeek-V3）与 legacy non-reasoning（GPT-4o）之间存在清晰的性能层级。

在 EED baseline、penalty 和 subtree discount 的参数变化实验（Table 6）中，大多数模型排名保持稳定；少数模型的波动为 ±1 名左右，主要出现在 pairwise confidence 低于 70% 的比较中。

Table 6 的平均 Efficiency 在列出的参数设置下分别报告为 289%、100%、217%、191%、175%、237%、211%、424%、305% 和 257%。

## 5. Test-time scaling（Figure 5、Table 7）

Figure 5 的 pass@k 曲线显示，k 增大时 accuracy 平滑提升；majority voting 曲线仍保留模型间的性能分离。

Table 7 的 PHYBench TTS 数值如下：

| Model | pass@1 | pass@32 | vote32 | Boundary of pass@k |
|---|---:|---:|---:|---:|
| Gemini 2.5 Pro | 38.71 | 65.91 | 41.97 | 74.9 |
| Gemini 2.5 Flash | 34.25 | 62.78 | 41.22 | 71.2 |
| DeepSeek-R1 | 25.06 | 50.88 | 28.65 | 81.3 |
| o4 mini | 23.20 | 52.10 | 24.60 | 78.6 |
| DeepSeek-V3 | 11.79 | 29.90 | 13.53 | not fitted |
| GPT-4o | 4.97 | 18.19 | 5.38 | not fitted |

Appendix E 文字报告，majority voting 通常只带来几个百分点的 accuracy 提升，而 pass@k 在 reasoning 与 non-reasoning 模型上经常带来数十个百分点的提升。

## 6. 首次错误分布（Table 2）

Table 2 统计 7 个模型在 50 道代表题上的首次错误类型。PP 是 physical perception，RR 是 robust reasoning；Sem 与 Sym 是 RR 内部的 semantic/symbolic 比例。

| Metric (%) | Gemini 2.5 Pro | DeepSeek-R1 | DeepSeek-V3 | o4 mini | o3 mini | o1-preview | GPT-4o |
|---|---:|---:|---:|---:|---:|---:|---:|
| Accuracy | 40 | 27 | 14 | 27 | 19 | 18 | 5 |
| PP | 9 | 4 | 5 | 6 | 10 | 12 | 21 |
| RR | 91 | 96 | 95 | 94 | 90 | 88 | 79 |
| Sem | 94 | 91 | 87 | 99 | 99 | 95 | 90 |
| Sym | 6 | 9 | 13 | 1 | 1 | 5 | 10 |

## 7. 受污染部分解下的鲁棒性（Table 3）

Table 3 的列为 Original、Correct 以及六种扰动：T1（删平方项）、T2（运算符反转）、T3（T1+T2）、T4（删 h）、T5（T2+T4）、T6（改写公式）。数值均为 accuracy（%）。

| Model | Original | Correct | T1 | T2 | T3 | T4 | T5 | T6 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Gemini 2.5 Pro | 97 | 100 | 93 | 95 | 100 | 78 | 95 | 100 |
| DeepSeek-R1 | 97 | 98 | 64 | 39 | 99 | 37 | 78 | 94 |
| DeepSeek-V3 | 66 | 93 | 0 | 97 | 73 | 0 | 0 | 12 |
| o3 mini | 98 | 98 | 88 | 85 | 97 | 73 | 90 | 95 |
| o4 mini | 83 | 89 | 55 | 70 | 72 | 34 | 54 | 90 |
| o1-preview | 94 | 81 | 9 | 15 | 70 | 10 | 14 | 83 |
| GPT-4o | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

论文文字还给出一个具体变化：DeepSeek-R1 在 T4（删除 h 项）下的 accuracy 从 97% 降至 37%。

## 8. EED 示例（Figure 2）

Figure 2 的示例问题是三球与不可伸长细绳组成的动力学情境，要求求中间绳瞬时张力。

图注标明比较了 DeepSeek-R1 与 GPT-4o 生成的回答以及 ground truth，并同时给出 EED 与 accuracy。

抽取文本中三个展示结果的 EED 分数为 100、47、13；相应 ACC 分数为 100、0、0。

该图展示的是同一道题中，表达式完全正确、部分保留结构但有误和结构性错误能够被 EED 分开；这里仅记录图中报告的分数，不对抽取后公式乱码作额外推断。

## 9. 论文结论中的结果性陈述

论文将 PHYBench 概括为：输出 token 更多、模型平均分更低、reasoning 与 general models 的分离更清楚，并在 pass@k 与 majority voting 下保持模型排序。

论文还报告当前模型的主要失败来自多步、多条件推理中引入错误方程，以及缺乏发现或纠正这些中间错误的能力。

这些结果的边界和未披露项见 [[qiu2025-phybench-critical]]；数据集的定义和公开入口见 [[entities/phybench]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[qiu2025-phybench-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | https://www.phybench.cn/ |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
