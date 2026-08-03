---
id: comparison--cycle12_v24_psg-result-20260802
title: Cycle 12：V24-PSG-MechConv 实测结果
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 12：V24-PSG-MechConv 实测结果

V24 v12 小链预检通过 replay/passivity、独立 EOM、梯形运动学、2/4/8 owner 分区一致性和本地 90 步速度，但 DC 长窗扰动出现非有限值，high-frequency 与 smooth-random 的 h1501 force relative RMS 分别为 `0.065554` 和 `0.087931`，均超过 `0.05`。因此 V24 是 `failed_pretraining_gate`，没有远程训练或准确率声明。

结构性通过不等于预测准确：边局部被动性、严格 `B^T f_e` 和 hard EOM 只能保证传播器的物理 bookkeeping 与分区一致性；它们没有自动解决真实动力输入的高频响应和长窗稳定性。这一失败是本轮停止条件，不应通过增加训练预算或放宽门槛绕过。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
