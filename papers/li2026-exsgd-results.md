---
id: papers--li2026-exsgd-results
title: ExSGD 实验结果
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
sources:
- sources/papers/li2026-exsgd.md
created: '2026-07-30'
updated: '2026-07-31'
confidence: medium
---

# Results & Evidence

实验数据：

- WHU-Aerial
- WHU-Sat
- PHB

比较方法：

- Adam
- NAG
- NAdam
- LAMB
- N-LAMB
- AdaBelief
- Shampoo

主要结论：

- ExSGD 在不同 batch size 下均保持较优 F1 和 IoU；
- 在超大 batch 条件下仍保持稳定训练；
- 历史梯度增强和层级学习率两个模块均有效。

论文报告 ExSGD 在三个建筑提取数据集上相比现有优化方法获得最高约 14.3% F1 和 16.56% IoU 提升。

## Evidence By Source

### `sources/papers/li2026-exsgd.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/li2026-exsgd-source.md`

^[sources/papers/li2026-exsgd.md]

## Related Indexes

- [[papers/index]]
- [[index]]
