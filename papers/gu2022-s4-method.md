---
id: paper--gu2022-s4-method
title: Gu et al. (2022) S4 — 方法
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/gu2022-s4
created: '2026-08-01'
updated: '2026-08-01'
confidence: low
legacy_tags:
- sequence-modeling
- spectral-method
- parallel-computing
- long-horizon-rollout
legacy_sources:
- raw/papers/arxiv_2111_00396v3.pdf
evidence_scope: local workspace source record pending canonical verification
---

# S4 方法机制

## 状态空间与双执行视图

连续模型为 (dot x=Ax+Bu, y=Cx+Du)。离散后既可递推，也可写成核 (K=(CB,CAB,ldots)) 与输入的非循环卷积；已知核时可用 FFT 并行计算整段输出。^[raw/papers/arxiv_2111_00396v3.pdf]

## NPLR/DPLR 结构

S4 将 HiPPO 状态矩阵表示为 normal-plus-low-rank，并稳定转换为 diagonal-plus-low-rank。Woodbury 恒等式把生成函数中的矩阵逆规约为少量 Cauchy 矩阵-向量乘。

## 复杂度边界

论文定理给出卷积核生成可规约为常数次 Cauchy 乘，理论运算量近似 (widetilde O(N+L))、空间 (O(N+L))。论文同时说明实际 GPU 代码采用易并行的朴素 (O(NL)) Cauchy 核并借助 PyKeOps 控制内存，因此理论复杂度不能与实测实现混为一谈。^[raw/papers/arxiv_2111_00396v3.pdf]

## 对本项目的接口

S4 适合共享的边历史编码器：输入相对位移、速度和材料参数，输出本构残差或内变量；最终 (B^	op f_e) 与硬加速度仍由 [[mtp-mechconv-v2]] 负责。它不提供真实稀疏 (M,C,K) 的精确频点解。

## 关联页面

- [[gu2022-s4-analysis]]
- [[structured-state-space-s4]]
- [[gu2022-s4-critical]]
