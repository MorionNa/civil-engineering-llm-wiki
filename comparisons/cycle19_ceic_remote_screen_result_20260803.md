---
id: comparison--cycle19_ceic_remote_screen_result_20260803
title: CEIC 远程 screen 结果（2026-08-03）
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# CEIC 远程 screen 结果（2026-08-03）

## 结论

本次 screen 为 NO-GO：训练在第一次优化器更新时因
`FloatingPointError: SOAP preconditioner contains non-finite values` 退出。
没有产生可用的精度、高频、EOM 或速度指标，也没有选择 CEIC checkpoint。

这只能归类为训练稳定性失败，不能据此声称 CEIC 相对 parent 有精度退化或
改进。按照搜索约定，本轮停止，不切换优化器重试。

## 可追溯性

- 远程主机：`senna@172.22.53.130`
- 代码根：`/home/senna/nonlinear-pinn-next`
- 运行目录：`outputs/remote_ceic_screen_v2_20260803a`
- 本地取回目录：`outputs/remote_ceic_screen_v2_20260803a/`
- 已保存 resolved config、resolved run metadata、初始 checkpoint 和完整日志。
- 未生成 epoch metrics、prediction、候选 checkpoint 或 final metrics。

当前 active model 仍为 frozen parent；CEIC 只保留为本地通过、远程未资格化的
实验分支。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
