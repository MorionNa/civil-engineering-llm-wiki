---
id: comparison--cycle14_v26_rcpp-result-20260803
title: Cycle 14：V26-RCPP-MechConv 结果
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
---

# Cycle 14：V26-RCPP-MechConv 结果

日期：2026-08-03
状态：**NO-GO；未训练；未启动远程 GPU**

## 一句话判断

V26 将父模型输出映射为物理残差，再做一次因果残差修正和最终硬 EOM 闭合；结构接口与局部 oracle 成立，但真实输入上的残差读出秩亏且留出工况力误差恶化，不能进入正式训练。

## 可复用证据

- M0：独立 `a_kin` 残差 RMS `0.1719943`，父模型 EOM 残差 `3.74e-17`，辅助力无泄漏。
- M1：2/50 步局部精确 oracle 的修正后残差均为 `0`。
- M2：linear、bilinear、Bouc–Wen 重放一致；Bouc–Wen 只声明 sequential-local，不虚报 consistent tangent。
- M4/M5：因果前缀、u-v、重放和最终独立 EOM 通过。
- M6/M7：仅为合成零 halo 与本地 CPU 范围内的接口/计时检查。

## 否证证据

M3 失败：留出力相对 RMS `1.040846` 对比父模型 `0.166289`；特征秩 `3`、条件数 `6.86e15`；最终 R² 的加速度和力分别为 `-2.1131`、`-0.0834`，而父模型为 `0.9533`、`0.9723`。`v-a` 也没有达到改善门槛。

## 文献边界

本轮下载并核验的 neural preconditioner、residual corrector 和 NOEM 文献支持“用残差/变分校正或子域耦合提升 PDE 求解”的研究方向，但没有证明本项目所需的无迭代硬动力学闭合、可替换非线性本构、真实 owner/halo 扩展或大变形端到端直接推理。因此它们只能作为设计依据，不能替代 M3 和远程基线证据。

## 后续门槛

保留 V26 作为失败候选审计材料。下一候选必须先在真实输入上消除秩亏和力闭合恶化，并通过 M3；在此之前不增加训练预算，不宣称规模化或加速达标。

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.

## Related Pages

- [[comparisons/index]]
- [[index]]
