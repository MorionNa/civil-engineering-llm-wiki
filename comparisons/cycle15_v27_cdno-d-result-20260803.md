---
id: comparison--cycle15_v27_cdno-d-result-20260803
title: Cycle 15：V27-CDNO-D 结果与否证
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 15：V27-CDNO-D 结果与否证

## 状态

**NO-GO；已有远程训练；冻结；不重复训练。**

## 结果摘要

CDNO-D 用独立因果隐式 BDF1/BDF2 + 可替换 step constitutive teacher 生成训练池轨迹，再蒸馏回原有 TemporalParallelMatrixMechConv。teacher residual 达到 `8.63e-8`，本地 linear/bilinear/Bouc–Wen 和 student expressivity 门通过，短前缀 loss 下降 `74.48%`。

但完整 v2 remote official90 screen 失败：pooled R²(u/v/a/edge-force) 为 `0.915150/0.957640/0.916148/0.963266`，均低于冻结父模型；worst-u 只有 `0.706167`；独立加速度/力 RMS 为 `0.038115/0.055395`，比父模型 `0.034003/0.049418` 更差；高模态 edge-force score 为 `0.746114`。构造 EOM residual 很小并不改变该结论。

## 知识更新

离散物理 teacher 是可靠的 offline oracle，但“teacher 精确”不等于“temporal-parallel student 能表达并泛化 teacher”。这与此前 V25/V26 的经验共同说明：当前瓶颈已经从物理约束实现转移到部署表示的状态推进/频带表达能力；再做 post-hoc correction、低秩读出、额外投影或只改 loss 都属于已否证家族。

## 退化与停止

保留 CDNO-D 作为离线 teacher 和本构审计工具，生产模型退回 V25 父模型。没有用户对“改变部署时间推进/状态表示并承担新的速度与跨本构实验成本”的明确授权前，不继续开新的远程 screen。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
