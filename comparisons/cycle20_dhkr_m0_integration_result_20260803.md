---
id: comparison--cycle20_dhkr_m0_integration_result_20260803
title: DHKR M0 集成结果（2026-08-03）
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# DHKR M0 集成结果（2026-08-03）

修复后的唯一 DHKR 实现已通过本地远程前闸门，可进行且只能进行一次串行 Adam
screen；尚不代表精度、高频收敛或速度通过。

## 实现约束

- 仅 scalar DOF M0；非标量直接拒绝。
- 强制 `hard_kinematic_integration=True`。
- 拒绝 `hard_kinematic_differentiation=True` 和 `bounded_response=True`。
- 新 head zero-init、有界；原 parent 本构、dynamic projection 和力平衡路径不变。
- 频率由 parent 已解析频带生成：
  `(0.01344, 0.03645, 0.09887, 0.26818)`。

## 闸门

两份 DHKR 测试共 16 项通过：parent 等价、两次本构调用、指数包络、非零
full/halo owner 等价、500-node、theta 防护、EOM，以及五步 clipped Adam 下
`u/v/a/edge-force` 四项逐项下降。parent checkpoint warm-start 和 CPU forward
预检通过。

远程 screen 只允许一次；出现非有限值、元数据/恢复失败或精度/独立物理/高模态
失败时立即停止，不换优化器、不换频带、不加后处理。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
