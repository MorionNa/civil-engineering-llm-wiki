---
id: papers--zhang2026-legonet-critical
title: LegONet 贡献与局限
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
keywords:
- future-work
- limitation
- structure-preserving
sources:
- sources/papers/zhang2026-legonet.md
created: '2026-07-28'
updated: '2026-07-31'
confidence: high
---

# LegONet Critical Analysis

## Contribution

- 从单体 neural solver 转向组合式 operator library；
- 将结构保持性质直接写入 operator block；
- 将训练、机制和时间积分解耦。

## Negative Knowledge

- block 依赖对应 baseplate，跨表示迁移仍困难；
- 新机制需要新增 block 训练；
- 强非线性、多物理耦合仍可能产生 splitting error；
- 训练仍需要可信 operator labels。

## 对结构动力学的启发

可能迁移方向：

- 将恢复力、本构、阻尼、地震输入分别设计为可组合模块；
- 使用模态空间或图空间作为统一 coefficient interface；
- 区分本构误差和时间积分误差。

## 关联

- [[zhang2026-legonet-analysis]]
- [[legonet]]

## Evidence By Source

### `sources/papers/zhang2026-legonet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2603.07882v1.pdf`

^[sources/papers/zhang2026-legonet.md]
