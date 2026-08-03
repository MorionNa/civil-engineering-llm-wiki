---
id: paper--brandstetter2022-mp-pde-method
title: Brandstetter et al. (2022) — MP-PDE 方法
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/brandstetter2022-mp-pde
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- message-passing
- pde
- time-marching
- autoregressive-rollout
legacy_sources:
- raw/papers/arxiv_2202_03376.pdf
- raw/papers/extracted/arxiv_2202_03376_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# MP-PDE 架构与稳定训练

## Encode-Process-Decode
- Encoder：把节点解、坐标、边界和方程参数映射到隐空间。
- Processor：使用相对坐标 \(x_j-x_i\)、状态差 \(u_i-u_j\) 和 PDE 参数构造消息，重复共享权更新。
- Decoder：浅层一维卷积沿时间通道输出增量，保持 \(\Delta t\to0\) 时的一致性动机。

消息差分形式与局部导数离散相似；作者指出一层、两层、三层局部聚合可分别包含 FDM、FVM 和 WENO 类结构的表示。

## Temporal bundling
一次调用同步预测 \(K\) 个未来切片：
\[
u_0\mapsto (u_1,\ldots,u_K).
\]
因此网络调用次数和闭环分布偏移次数都约减少 \(K\) 倍，但它仍是分块自回归，并非任意长时间的一次全局算子。

## Pushforward
先把模型展开 \(N\) 次生成偏移输入，切断这些前序调用的梯度，再对下一组 \(K\) 个目标反传。论文常用最大 2 步展开；高斯噪声的稳定性/精度折衷不如模型自身 pushforward 扰动。

## 条件化
显式输入方程系数和边界标签后，跨 PDE 参数与边界组合泛化明显改善。对结构动力，这支持把本构与物理参数作为插件/条件接口，而不是让网络从轨迹暗中猜测。

## 关联页面
- [[brandstetter2022-mp-pde-analysis]]
- [[brandstetter2022-mp-pde-results]]
- [[mp-pde]]

^[sources/papers/brandstetter2022-mp-pde]
