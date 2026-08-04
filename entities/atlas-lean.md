---
type: entity
title: ATLAS (Autoformalized Textbook Library At Scale)
entity_type: dataset
authors:
- Ahmad Rammal
- Niket Patel
- Fabian Gloeckle
- Amaury Hayat
- Julia Kempe
- Remi Munos
- Charles Arnal
- Vivien Cabannes
year: 2026
venue: arXiv preprint
tags:
- domain/ai4s
- entity/dataset
reproducibility: medium
code_url:
- https://github.com/facebookresearch/atlas-lean
dataset_url:
- https://github.com/facebookresearch/atlas-lean
methods:
- textbook-to-Lean formalization
- dependency-graph provenance
- mechanical verification
results:
- 26 open-access mathematical textbooks
- 2,855/4,007 target statements
- over 45,000 verified Lean 4 declarations
- 483,918 Lean 4 lines in Table 1
failure_modes:
- partial coverage
- diminishing returns
- semantic misformalization
- version mismatch
datasets:
- 26 open-access mathematical textbooks
- verified Lean 4 formal libraries
id: entity--atlas-lean
status: active
project: civil-engineering-llm-wiki
keywords:
- formalization
- autoformalization
- theorem-proving
- proof-assistant
- lean
- lean-4
- mathlib
- formal-science
- mathematics-at-scale
- evaluation
- textbook-to-Lean formalization
- dependency-graph provenance
- mechanical verification
- 26 open-access mathematical textbooks
- 2,855/4,007 target statements
- over 45,000 verified Lean 4 declarations
- 483,918 Lean 4 lines in Table 1
- partial coverage
- diminishing returns
- semantic misformalization
- version mismatch
- verified Lean 4 formal libraries
- dataset
- arXiv preprint
sources:
- sources/papers/rammal2026-autoformbot-atlas.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# ATLAS

^[sources/papers/rammal2026-autoformbot-atlas.md]

## 定义

ATLAS 是 Autoformalized Textbook Library At Scale 的缩写，是论文用 AutoformBot 对 26 本开放获取数学教材生成的 verified Lean 4 formal libraries。这里按任务清单归入 dataset/data-asset 路径；它更准确地说是带源码、声明、证明和 source provenance 的正式库，而不是只含样本—标签对的传统机器学习数据集。

## 论文证据

- 摘要报告 ATLAS 超过 45,000 个 Lean 4 declarations 和约 500 thousand lines of code。
- Table 1 给出 2,855/4,007 个目标声明成功形式化（71.3%）、483,918 行 Lean 4 代码和 183,157M token estimate。
- 书目覆盖 analysis、algebra、topology、combinatorics、probability、geometry、number theory、PDE 和 theoretical computer science 等领域。
- 论文称每本书形成 self-contained Lean project，依赖 mathlib 且 builds without errors；形式声明保留回到教材源文本的 provenance。
- Appendix C 展示 Parseval、Mills’ inequality 和 Sperner’s theorem 三个代表性、sorry-free 形式化样例。

## 资产边界

ATLAS 不是完整教材库：总体成功率是 71.3%，各书覆盖率从 40.0% 到 98.9% 不等。作者在强烈 diminishing returns 阶段停止继续 formalization，因此未完成目标不是随机缺失。

“verified”主要描述 Lean 构建和论文评价 harness 的范围，并不自动保证每个形式命题忠实表达教材。Appendix G 的 Algebraic Combinatorics 专家审查发现 Lean 4.28/4.30 版本问题及两个显式 axiom，说明 ATLAS 仍需要独立语义审查、版本锁定和持续维护。

论文未披露统一的 ATLAS license、单独的数据集下载格式或预训练权重；提供文本中明确给出的数据资产入口是 GitHub 仓库。

## 关联页面

- 论文总览：[[rammal2026-autoformbot-atlas-analysis]]
- 结果证据：[[rammal2026-autoformbot-atlas-results]]
- 批判性边界：[[rammal2026-autoformbot-atlas-critical]]
- 生成算法：[[entities/autoformbot]]

## 官方链接

- ATLAS repository: https://github.com/facebookresearch/atlas-lean
- Source paper: https://arxiv.org/abs/2605.29955
