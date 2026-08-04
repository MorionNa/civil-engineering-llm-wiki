---
type: paper-analysis
title: Solving olympiad geometry without human demonstrations
authors:
- Trieu H. Trinh
- Yuhuai Wu
- Quoc V. Le
- He He
- Thang Luong
year: 2024
venue: Nature
tags:
- domain/ai4s
- evidence/paper
methods:
- large-language-models
- machine-learning
- formalization
- theorem-proving
- geometry
results:
- benchmark
- evaluation
- geometry
- olympiad
failure_modes:
- geometry
- formalization
- benchmark
datasets:
- geometry
- olympiad
- benchmark
reproducibility: medium
code_url:
- https://github.com/google-deepmind/alphageometry
dataset_url: []
id: paper--trinh2024-alphageometry-results
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- scientific-reasoning
- benchmark
- evaluation
- geometry
- olympiad
- machine-learning
- formalization
- theorem-proving
- reproducibility
- Nature
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# AlphaGeometry 实验与数值结果

^[sources/papers/trinh2024-alphageometry.md]

本页只记录预提取论文文本中有明确表格、图或正文证据支持的实验结果。方法定义见 [[trinh2024-alphageometry-method]]，总体解释见 [[trinh2024-alphageometry-analysis]]。

## 1. IMO-AG-30 主结果

IMO-AG-30 包含 30 道自 2000 年以来、可翻译到本文经典几何环境的 IMO 几何题。论文称非组合几何相关题中约 75% 可以表示，并在 Supplementary Information 提供 30 题的陈述和翻译（正文 p. 4）。

| 方法 | 解决题数（30 题） | 证据位置 |
|---|---:|---|
| Wu’s method（既有最佳计算机代数方法） | 10 | Table 1，p. 5 |
| Gröbner basis | 4 | Table 1，p. 5 |
| GPT-4 直接生成自然语言证明 | 0 | Table 1，p. 5 |
| Full-angle method | 2 | Table 1，p. 5 |
| Deductive database（DD） | 7 | Table 1，p. 5 |
| DD + 人类设计启发式 | 9 | Table 1，p. 5 |
| DD + algebraic reasoning（DD+AR） | 14 | Table 1，p. 5 |
| DD+AR + GPT-4 辅助构造 | 15 | Table 1，p. 5 |
| DD+AR + 人类设计启发式 | 18 | Table 1，p. 5 |
| AlphaGeometry | 25 | Table 1，p. 5 |
| AlphaGeometry：无预训练 | 21 | Table 1，p. 5 |
| AlphaGeometry：无微调 | 23 | Table 1，p. 5 |

论文摘要和 Fig. 2 同样报告 AlphaGeometry 解决 25/30，前一最佳方法解决 10/30。

## 2. 合成数据规模与结构

论文正文报告：

- 通过随机定理前提和符号推理生成 100 million 个合成定理及其证明；
- 其中很多证明超过 200 步，最长合成证明为 247 步；
- 约 9% 的生成证明包含辅助构造，即约 9 million 个证明；
- 只有约 0.05% 的合成训练证明比测试题的平均 AlphaGeometry 证明更长；
- 最复杂的合成证明有两个辅助构造；
- 合成证明长度分布偏向短证明，但少量证明比测试集中最难题的证明长度最多长约 30%（Fig. 4，正文 p. 4）。

Methods 的工程统计补充说明：100,000 个 CPU workers 运行 72 h，先得到约 500 million examples，规范化和去重后保留 100 million unique theorem–proof examples；其中 9 million 至少包含一个辅助构造。

生成数据没有发现 IMO-AG-30 原题；在 JGEX 几何问题集合中发现近 20 个主要为中等难度和已知定理的问题（Methods p. 9）。

## 3. 训练和搜索消融

论文报告以下数值：

| 改动 | 结果 |
|---|---:|
| 完整 AlphaGeometry | 25/30 |
| 只使用 20% 原始训练数据 | 21/30 |
| 训练数据比例 20%–80% 的实验 | 20% 时已经报告 21/30；其余比例的逐点数值在预提取正文中未列出 |
| beam size 512 → 8 | 21/30 |
| 搜索深度 16 → 2，beam size 保持 512 | 21/30 |
| 无预训练 | 21/30 |
| 无微调 | 23/30 |

论文将 beam size 8 描述为相对 512 的 64 倍缩减；因此达到 21/30 并不等于搜索预算完全不影响性能，而是该设置下仍超过表中最强人类启发式基线的 18/30。

## 4. 更大测试集

论文在 231 道几何题上评估，题目来源包括教科书例题与练习、地区奥林匹克和著名定理；其中包括 five circles theorem、Morley’s theorem、Sawayama–Thébault theorem 等更复杂题目。

| 方法 | 解决比例 |
|---|---:|
| AlphaGeometry | 98.7% |
| DD+AR + 人类设计启发式 | 92.2% |
| Wu’s method | 75% |

论文报告不同方法的总体排名与 IMO-AG-30 一致（正文 p. 6；Extended Data Fig. 6b）。

## 5. IMO 年份与专家评价

论文报告 AlphaGeometry 解决了 2000 年和 2015 年 IMO 中的全部几何题。这两个年份在论文中被用作可能达到奖牌阈值的检验。

作者把这些解答提交给一名美国 IMO 队教练进行评估。该专家建议 AlphaGeometry 解答可获满分，从而超过相应年份 14/42 的奖牌阈值。该结果只针对几何题解答的专家评价，不等同于在完整 IMO（还包括其他数学领域及人类时间/工具限制）中实际参赛。

## 6. 证明长度与人的难度

Fig. 6 将 AlphaGeometry 的证明长度与 IMO 参赛者平均分数比较：

- 人类平均得分最低的三个已解决问题，AlphaGeometry 也需要异常长的证明，并需要语言模型构造；
- 对人类平均分大于 4.5 的较容易问题，论文观察到人类得分与 AlphaGeometry 证明长度没有相关性，报告 p > 0.06；
- 图中标记了 2000 P6、2015 P3、2019 P6 等同时对人类和 AlphaGeometry 都较难的题。

## 7. 泛化结果与生成的广度

论文报告合成数据能够重新发现几何文献中的部分复杂定理和引理，尽管起点是随机前提。生成结果通常不具有人类发现定理时的对称性偏好，因此覆盖了更宽的欧氏几何情形。

与此同时，100 million unique theorem–proof examples 中没有发现 IMO-AG-30 题目。论文据此报告，已探索的合成空间仍比当前数据集合大，不能把测试题性能解释为训练样本逐题复制。

## 8. 代表性解答与失败

Fig. 5 报告在翻译后的 IMO 2004 P1 中，traceback 找到一个未使用前提，从而得到更一般的版本：O 不必是 BC 的中点，P 仍位于 BC 直线上。不过原题要求 P 位于 B、C 之间，而推广证明不保证这个 betweenness 条件。

Extended Data Fig. 2 报告 IMO 2004 P1 的机器证明与人类证明都识别了 M、N 关于 O 的对称轴；AlphaGeometry 构造 K 来显式表示这条轴，而人类直接使用已有点 R。该机器证明在五点共圆部分使用很长的低层步骤。

Extended Data Fig. 3 报告 IMO 2000 P6 的 AlphaGeometry 解答包含两个辅助构造和超过 100 个演绎步骤；人类解答使用复数和合适坐标系，机器解答因此更冗长、较不直观。

Extended Data Fig. 4 报告 IMO 2019 P2 是 AlphaGeometry 的未解决题之一；人类解答使用辅助构造和 barycentric coordinates。当向 AlphaGeometry 提供合成证明所需的真实辅助构造时，论文仍以其现有符号规则报告相关限制。

Extended Data Fig. 5 报告 IMO 2008 P6 是 AlphaGeometry 未解决题，也是 30 题中人类平均得分最低的一题（0.28/7）。人类解答用四个辅助构造、Pitot theorem 和 homothety；这些高层工具不在当前符号引擎的规则中，即使提供人类辅助构造也没有得到解。

## 9. 可复现性相关事实

论文在 Code availability 中给出 <https://github.com/google-deepmind/alphageometry>，并说明 code 和 model checkpoint 可用。Data availability 中说明支撑发现的数据位于 Extended Data、Supplementary Information 和 source data。

论文文本没有给出独立的完整合成训练语料 URL，也没有在本文中报告可直接下载的 100 million 例数据集地址。因此 dataset_url 在四个论文页中保持为 []；这不否认论文补充材料中的 source data 可用，只表示没有可从提供文本确认的独立数据集链接。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[trinh2024-alphageometry-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | https://github.com/google-deepmind/alphageometry |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
