---
id: comparison--mtp-mechconv-v2-v19-scalability-and-correctness-correction
title: MTP-MechConv v2：V19 可扩展性口径修正与 M0-B 正确性否决
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- structural-dynamics
- mechconv
- convolution-quadrature
- negative-knowledge
- experiment
legacy_sources:
- raw/papers/arxiv_2111_00396v3.pdf
- raw/papers/arxiv_math_0504461v1.pdf
---

# V19 口径修正与正确性证据

本页取代 [[mtp-mechconv-v2-v18-v19-negative-knowledge]] 中“因相对显存高于 RK4 而硬否决”的结论。用户最新定义是：可扩展性要求大规模结构能够训练和推理，不要求显存低于竞争方法。

## M0-A 重新分类

- 50DOF、1501 步、L=4096 的 absolute peak 为 397,906,944 B。
- warm/cold 相对向量化非线性 RK4 分别快 39.551/33.581 倍。
- 因此速度可行性通过；397.9 MB 只作为绝对资源记录。
- 该结果仍不能证明一般矩阵边权、owner/separator 子图和大规模训练可行。

## M0-B 新的硬否决

ZCQ 与同一梯形顺序参考的 u/v/a 相对最大误差均小于 6.41e-12，频域残差小于 9.45e-14；从最低模态到第 49 模态的 10 组幅相审计也全部通过。由此确认直接频域载波本身没有长时相位或高频精度问题。

但是，用连续/RK4 真值定义 `g*=M a_truth+K0 u_truth` 后，回放 R² 为：u=0.999670、v=0.946651、a=0.226474、平均=0.724265，未满足冻结的每项 0.995、平均 0.999 门。根因是连续采样轨迹不严格满足梯形离散运动学；硬加速度公式会放大高模态位移误差。

因此 V19 当前“连续真值 g* + 梯形 ZCQ”接口被否决，M0-C、训练和大规模实验均未解锁。允许用户选择的后继只有：四阶 A 稳定 RK-CQ、内部子步梯形 ZCQ，或明确把教师口径改为同一 Newmark-β 离散。不得通过放宽加速度门或推理后 Newmark 校正掩盖失败。

## 论文边界

S4 的近线性长卷积机制不能证明任意结构动力学矩阵 resolvent 的正确性或速度；快速 oblivious convolution quadrature 的复杂度结论依赖其 Laplace/sectorial 假设，也不能直接替当前无阻尼结构频域实现背书。项目判断以本次正式数值审计为准。

## 关联页面

- [[gu2022-s4-analysis]]
- [[schadle2006-fast-convolution-quadrature-analysis]]
- [[mtp-mechconv-v2-experiment-ledger]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
