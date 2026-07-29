---
title: "Kolzhetsov et al. (2026) — RL Adaptive Loss Control 结果"
created: 2026-07-29
updated: 2026-07-29
type: paper-analysis
tags: [physics-informed, pinn, reinforcement-learning, benchmark]
sources: [raw/papers/kolzhetsov2026-accelerating-pinn-training-extracted.txt]
confidence: high
---

# Results

## Benchmark

论文测试：

- 一维热传导方程；
- 非线性 Schrödinger 方程；
- 不可压 Navier–Stokes 方程。

## Main Result

对于一维热传导方程，RL 动态调权相比固定权重达到目标 loss 所需 epoch 减少约 25%。

论文报告 RL 解与 baseline 解的相对误差低于 $10^{-8}\%$，说明动态调权没有明显降低解一致性。

## Comparison

图 2 对比：

- baseline fixed weighting；
- GradNorm；
- Adaptive Loss Scaling；
- RL-agent。

同时展示 total loss、BC loss、IC loss 和 PDE loss 演化。

## Limitations of evidence

论文没有给出统一 wall-clock 加速、训练成本、随机重复实验和完整数值表，因此不能直接推断 RL 方法在所有 PINN 场景中都具有总体计算优势。

## 关联

- [[kolzhetsov2026-rl-adaptive-loss-control-analysis]]
- [[kolzhetsov2026-rl-adaptive-loss-control-critical]]
