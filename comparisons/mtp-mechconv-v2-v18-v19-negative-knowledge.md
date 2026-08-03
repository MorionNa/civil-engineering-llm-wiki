---
id: comparison--mtp-mechconv-v2-v18-v19-negative-knowledge
title: MTP-MechConv v2：V18–V19 长时载体证伪与退化边界
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
- equation-of-motion
- spectral-method
- parallel-computing
- limitation
legacy_sources:
- raw/papers/arxiv_2111_00396v3.pdf
- raw/papers/arxiv_math_0504461v1.pdf
---

# V18–V19 证据账本

## 论文机制与项目反例

|路线|论文可支持|项目正式结果|判定|
|---|---|---|---|
|S4/长卷积|特殊 SSM 可在卷积与递推视图间切换|可支持共享因果边历史头，不能精确替代任意 (M,C,K)|条件采用|
|快速卷积求积|Laplace/生成函数与轮廓分块可降低某类历史卷积成本|V19 使用固定 z 轮廓直接解真实结构频点，不继承在线 (O(\log N)) 内存结论|条件采用|
|V18 全谱 Chebyshev-FFT|短步 Chebyshev 与 FFT 都合法|32 阶在 50DOF/1501 步 fit/val 最大尺度误差 3.472/2.974|硬否决|
|V19 Thomas-ZCQ|实际频点避免 V18 的长时相位低阶逼近|warm/cold 39.55×/33.58× 加速，但显存 397.9 MB，对 RK4 为 18.35×|硬否决完整目标|

V18 证明“短步低阶可逼近”不能推出“所有长滞后仍是低阶”。V19 则证明直接频点解可恢复速度潜力，但全时程频谱与大 dilation TCN 工作区不满足预注册任意规模显存门。^[raw/papers/arxiv_2111_00396v3.pdf] ^[raw/papers/arxiv_math_0504461v1.pdf]

## 当前可完成性判断

冻结的 V19 无法同时满足速度和任意规模扩展，且按实验合同不得通过换 PCR、降精度、缩短 FFT 或删除第二载体事后补救。现阶段没有经过证据验证的架构同时满足高精度、严格平衡、跨本构和任意规模四项，因此不能宣称核心目标已经可完成。

## 需用户批准的退化方案

唯一建议的退化是保留 V19 的 33–40× 时间优势，把 50DOF 显存门从“相对 RK4 ≤2×”改为“绝对 ≤512 MB”，并把任意规模结论降级为“待 owner/separator 实测”；训练仍须等待正确性、因果性和一般稀疏门。该修改牺牲已证明的任意规模内存保证，不能自动执行。

## 关联页面

- [[gu2022-s4-analysis]]
- [[schadle2006-fast-convolution-quadrature-analysis]]
- [[mtp-mechconv-v2-experiment-ledger]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
