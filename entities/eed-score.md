---
type: entity
title: Expression Edit Distance (EED) Score
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
- entity/model
methods:
- LaTeX-normalization
- latex2sympy-extended
- SymPy
- expression-tree
- Zhang-Shasha-algorithm
- tree-edit-distance
- partial-credit-scoring
- subtree-edit-discount
results:
- EED-score
- accuracy
- sample-efficiency
- model-ranking
- robustness-analysis
failure_modes:
- format-parsing
- symbolic-conversion
- final-answer-only
- no-dimensional-check
- threshold-sensitivity
- noncanonical-semantics
datasets:
- PHYBench
reproducibility: medium
code_url: []
dataset_url:
- https://www.phybench.cn/
id: entity--eed-score
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- physics-reasoning
- scientific-reasoning
- benchmark
- evaluation
- machine-learning
- reproducibility
- LaTeX-normalization
- latex2sympy-extended
- SymPy
- expression-tree
- Zhang-Shasha-algorithm
- tree-edit-distance
- partial-credit-scoring
- subtree-edit-discount
- EED-score
- accuracy
- sample-efficiency
- model-ranking
- robustness-analysis
- format-parsing
- symbolic-conversion
- final-answer-only
- no-dimensional-check
- threshold-sensitivity
- noncanonical-semantics
- PHYBench
- arXiv preprint
sources:
- sources/papers/qiu2025-phybench.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Algorithm/metric entity: Expression Edit Distance (EED) Score

^[sources/papers/qiu2025-phybench.md]

## 1. 定义

Expression Edit Distance（EED）Score 是 PHYBench 论文提出的、用于比较模型生成表达式与 ground-truth 表达式的 model-free、rule-based 评分指标。它不是物理求解器，也不是完整 chain-of-thought verifier；方法展开见 [[qiu2025-phybench-method]]。

## 2. 计算机制

1. 从模型输出的 `\boxed{}` 中取出最终 LaTeX 表达式。
2. 移除格式命令等非标准结构，并使用 `latex2sympy_extended` 转成 SymPy symbolic expression。
3. 对 gt 与 gen 分别执行 `simplify()`；表达式变量按论文说明假设为 positive。
4. 将两个表达式转成规则化 expression trees。
5. 用节点插入、删除、替换及子树插入/删除计算扩展 Zhang–Shasha tree edit distance。
6. 将编辑距离除以 ground-truth tree size，得到相对距离 `r`，再按分段函数输出 0–100 分。

论文给出的默认形式为 `100`（`r=0`）、`60-100r`（`0<r<0.6`）和 `0`（`r>0.6`）。提供的文本没有单独规定 `r=0.6` 的边界归属，复现时应显式固定。

子树成本为 `min(x, 0.6(x-5)+5)`，用于降低大于 5 个节点的整体物理分量被插入/删除时的累计代价。

## 3. 与 Accuracy 的区别

Accuracy 只在 simplify(gt) 与 simplify(gen) 等价时记 100，否则记 0。

EED 能把系数错误、局部结构错误和整体结构错误区分开，给出部分正确性分数；论文 Figure 2 展示了三个回答获得 EED 100、47、13 而 ACC 为 100、0、0 的例子。

论文 Table 4 的 bootstrap 汇总报告 EED 相对 binary accuracy 的平均 sample-efficiency 提升为 204%，标准差为 80%。

## 4. 适用范围

EED 适用于答案可以稳定规范化为单个 symbolic expression 的任务，尤其适配 [[entities/phybench]] 的物理表达式题。

它适合做大规模、低人工成本的最终答案比较，也适合作为模型排序和 TTS 分析的连续信号。

## 5. 失败边界

- LaTeX 提取、解析、SymPy 转换或计算失败时，论文流程返回 0。
- 最终表达式评分看不到中间步骤，因此不能发现“中间物理定律错、最后偶然抵消”的过程问题。
- 表达式树节点近似等权，不显式检查量纲、单位、边界条件、守恒律或物理可行性。
- 折扣系数、baseline、penalty 与阈值是评测设计参数，不应未经校准直接迁移到其他领域。
- 不同但物理等价的表达式能否被 canonicalization 统一，受 LaTeX parser、SymPy simplify 和变量假设影响。

## 6. 研究边界与后续方向

论文建议把 EED 与 unit analysis、symbolic dimensional validation 等 physics-informed checks 结合。

更完整的方向是将最终表达式分数与过程级标注、守恒律验证、可执行数值检查和可审计的中间步骤结合；这些扩展不属于论文当前已经实现的 EED。

## 7. 关联页面

总览：[[qiu2025-phybench-analysis]]。

实验结果：[[qiu2025-phybench-results]]。

批判性边界：[[qiu2025-phybench-critical]]。
