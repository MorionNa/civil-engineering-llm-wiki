---
id: paper--moseley2023-fbpinn-method
title: Moseley et al. (2023) — FBPINN 方法
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/moseley2023-fbpinn
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- physics-informed
- pinn
- spatial-partitioning
- spectral-bias
- parallel-computing
legacy_sources:
- raw/papers/10_1007_s10444_023_10065_9.pdf
- raw/papers/extracted/10_1007_s10444_023_10065_9_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# FBPINN 方法机制

## 解表示
对重叠子域 \(\Omega_i\)，局部网络 \(NN_i\) 先接收局部归一化坐标，再乘可微窗 \(\omega_i\)。全局解为局部输出之和，并可再施加边界/初值硬约束算子：
\[
\hat u(x)=C\!\left[\sum_i \omega_i(x)\,NN_i(\operatorname{norm}_i(x))\right].
\]

窗在子域外近零，并在相邻重叠区充分相交。增大重叠通常提高通信和准确率，但会增加重复网络求值。

## 高频重标度
同一全局频率在更小子域、重新归一到 \([-1,1]\) 后呈现较低有效频率，因此小局部网络更容易训练。这与只增加全局 Fourier feature 不同。

## 并行训练
每个子域可独立计算局部输出与导数；仅在重叠采样点交换并求和。论文算法对邻域输出可 detach，使各局部参数反传并行；每个重叠区必须使用一致采样点。

若每个子域的点数和网络大小固定，总训练工作随子域数线性增长；配足并行资源时理论 wall-clock 可近似保持。但论文只实测单线程/单 GPU。

## 训练调度
全激活适合简单问题；时空波动使用 time-marching scheduler，逐步激活时间相邻子域。局部困难区还可采用自适应分区和激活策略。

## 结构图迁移
图中不直接使用坐标窗求和矩阵内力。更安全的实现是：halo 节点提供上下文，核心节点唯一写出；只有经全图等价测试后，才对重叠位移/速度使用 partition weights。

## 关联页面
- [[moseley2023-fbpinn-analysis]]
- [[moseley2023-fbpinn-results]]
- [[fbpinn]]

^[sources/papers/moseley2023-fbpinn]
