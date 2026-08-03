---
id: comparison--cycle19_ceic_m0_integration_result_20260803
title: CEIC M0 集成结果（2026-08-03）
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CEIC M0 集成结果（2026-08-03）

## 结论

CEIC 已通过本地集成闸门，可以准备一次串行远程 screen；尚未证明
official90 精度、高频收敛、独立物理误差或速度优势。

## 证据

- 12 个聚焦测试通过。
- zero-init 时，位移、速度、加速度、节点/单元力和残差与 frozen parent
  完全一致。
- 开启一次 parent equilibrium projection 时，本构 pre-hook 计数为 2。
- signed incidence 的内部冲量逐时刻抵消；非零 CEIC smoke 输出有限，构造
  EOM residual 小于 `1e-10`。
- linear、bilinear、Bouc--Wen 三种可替换本构均完成有限性 smoke，并存在
  非零 CEIC 修正路径。
- 500 节点/500 单元链划分为 16 个 halo 子图后，首个子图 35 节点、34 单元，
  forward 有限；继承的 `required_halo_hops` 在该 smoke 中为 2。

## 边界

本地人为设置的非零 CEIC 权重不是精度证据；未训练前独立 BDF2 缺陷不应被
视为通过。下一步只允许在 `/home/senna/nonlinear-pinn-next` 上启动一次保留
完整配置、日志、PID、checkpoint、prediction、metrics 和 hash 的远程 screen。
Sol high 审查曾被请求，但限时内没有返回 verdict，因此不冒充外部 GO。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
