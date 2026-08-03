---
id: comparison--mtp-mechconv-v2-impulse-bridge-negative-20260802
title: MTP-MechConv v2：硬冲量桥接 screen 的负知识
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-02'
updated: '2026-08-02'
confidence: low
legacy_tags:
- mechconv
- impulse-formulation
- hard-eom
- temporal-parallel
- negative-knowledge
legacy_sources:
- ../../../../docs/plans/temporal_parallel_impulse_bridge_screen_20260802.md
- ../../../../outputs/remote_impulse_bridge_screen25_20260802/metrics.json
---

# 负知识

对已有 temporal-parallel 最佳 checkpoint 只训练 `edge_head`/高频 edge head，并把 edge force 送入硬冲量 prefix，能够把离散 EOM 与运动学残差压到约 `1e-6`，但 official90 位移 R² 为 `-19.78`，速度 R² 为 `0.789`。这证明“硬闭合层 + 原有 edge proposal”不是可直接组合的架构。

因此不能用构造出的 EOM 指标替代响应精度，也不能继续靠增加 epoch 掩盖 proposal 与 hard trajectory 的不一致。保留 [[mtp-mechconv-v2-v21-m0-causal-audit]] 的物理审计组件，生产候选仍是 [[mtp-mechconv-v2-experiment-ledger]] 中的 temporal-parallel checkpoint。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
