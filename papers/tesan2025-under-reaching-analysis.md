---
id: paper--tesan2025-under-reaching-analysis
title: Tesan et al. (2025) — 消息传递 PDE 求解器的 under-reaching 与 CFL 下界
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/tesan2025-under-reaching
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_methods:
- physics-guided-message-reach
- shared-weight-message-passing
- rollout-sensitivity-analysis
legacy_results:
- message-passing-lower-bound
- rollout-stability
- geometry-extrapolation
legacy_failure_modes:
- under-reaching
- over-smoothing
- domain-size-extrapolation
legacy_datasets:
- wave-equation
- heat-equation
- poisson-equation
- incremental-forming
legacy_reproducibility: medium
legacy_tags:
- neural-network
- physics-simulation
- pde
- message-passing
- long-horizon-rollout
- spatial-partitioning
legacy_sources:
- raw/papers/10_1016_j_cma_2025_118476.pdf
- raw/papers/extracted/10_1016_j_cma_2025_118476_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# On the under-reaching phenomenon in message-passing neural PDE solvers

## 1. 工程背景
图神经求解器只能通过邻边逐跳传递信息。若每个预测步的消息传播距离落后于真实物理影响距离，网络即使有足够参数也无法形成正确解；这类结构性失败被称为 under-reaching。

## 2. Research Gap
消息传递层数通常靠网格搜索选择，未与波速、时间步、网格尺度或图直径建立可计算关系。深层图网络的误差也常被笼统归因于优化、over-smoothing 或 over-squashing。

## 3. 科学问题
能否按 PDE 类型给出消息跳数的物理下界，并证明跨过下界后误差趋于饱和，而不是依赖无限加深网络？

## 4. 研究目标
对双曲、抛物和椭圆问题分别建立消息传播下界，并在波、热扩散、Poisson 和三维弹塑性增量成形上固定参数量、改变共享权消息迭代数进行验证。

## 5. 方法机制
双曲问题要求消息传播至少跑在物理波前之前；在二维方格上给出 \(M>\lceil\sqrt{2}c\Delta t/\Delta x\rceil\)。抛物/椭圆问题按其建模假设要求每个推理步覆盖全域，使用 \(M=L/\Delta x\)。→ [[tesan2025-under-reaching-method]]

## 6. 结果证据
波动算例的理论阈值分别为 4 和 8 跳；低于阈值时长滚动失败，达到阈值后误差迅速饱和。热扩散和 Poisson 的阈值随域长/网格尺度变为 10、20 等；越过阈值继续加跳数收益很小，部分算例因 over-smoothing 略有退化。→ [[tesan2025-under-reaching-results]]

## 7. 贡献
论文把消息层数从经验超参数变为物理可审计的传播预算，并把“参数不足”与“感受野不足”区分开。

## 8. 核心知识点
图连通不等于一次推理拥有足够物理信息。消息迭代数、时间步与空间离散共同决定能否表示传播；对更大图固定跳数外推可能必然失败。

## 9. Negative Knowledge
抛物/椭圆全域下界基于特定局部消息图和单尺度处理器，不证明所有粗网格、多重网格或全局算子都必须线性增加深度。其弹塑性结构算例是准静态增量成形，不是 \(M\ddot x+C\dot x+f_\mathrm{int}=F\) 动力学。→ [[tesan2025-under-reaching-critical]]

## 10. 可迁移知识

| 论文结论 | 对 MechConv/halo 的迁移 |
|---|---|
| 传播距离不得落后于波前 | 用模态/波速、\(\Delta t\)、构件尺度制定最小细层感受野 |
| 大域固定跳数可能失败 | 训练/验证必须含扩大图和不同分区，而非只在 5DOF 内随机切分 |
| 越过阈值后收益饱和 | 不盲目堆叠 MechConv；达到 reach contract 后用粗层通信 |
| 共享权隔离参数量影响 | 消息深度消融保持参数量近似一致 |

## 11. 研究机会
结构离散系统需要把连续波速下界改写为图上的局部传播时间或模态群速度，并验证多层粗图能否以 \(O(\log N)\) 路径提供全局修正，同时不破坏矩阵边权和局部平衡。

## 12. 可复现性

| 项目 | 说明 |
|---|---|
| 等级 | 🟡 中 |
| 数据 | 4 类合成数据，每类约 1000 个模拟，80/10/10 划分 |
| 控制 | 共享处理器权重，消息迭代数改变但参数量固定，多随机种子 |
| 公开性 | 全文给出方程、阈值和数据表；本地全文未确认官方代码链接 |
| 边界 | 方形/规则域假设用于隔离 over-squashing；动力结构未直接验证 |

## 关联页面
- [[message-passing-reach-contract]]
- [[mp-pde]]
- [[multilevel-fbpinn]]

^[sources/papers/tesan2025-under-reaching]
