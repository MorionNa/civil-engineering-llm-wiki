---
id: papers--lahoti2026-mamba3-results
title: Mamba-3 结果
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
- method/transformer
sources:
- sources/papers/lahoti2026-mamba3.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# Mamba-3 结果

## Language Modeling

论文在 FineWeb-Edu 100B token 训练设置下比较 Mamba-3、Mamba-2、Gated DeltaNet 和 Transformer。

主要结论：

- Mamba-3 SISO 优于已有线性模型；
- Mamba-3 MIMO 在 SISO 基础上进一步提升；
- 在相同性能下可使用更小 state size。

## State Tracking

在 parity 和 modular arithmetic 等任务中，数据依赖 RoPE 的复值状态版本显著提升状态跟踪能力。

## Efficiency

MIMO 通过提高 arithmetic intensity，在增加计算量的同时保持接近的 decode latency。

## 局限

- 主要验证集中于语言模型；
- 固定状态模型仍存在部分检索能力不足；
- 科学计算任务尚未验证。

## Evidence By Source

### `sources/papers/lahoti2026-mamba3.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/lahoti2026-mamba3-source.md`

^[sources/papers/lahoti2026-mamba3.md]

## Related Indexes

- [[papers/index]]
- [[index]]
