---
id: comparison--mtp-mechconv-v2-evidence
title: MTP-MechConv v2：时间并行、消息可达性与多层子图证据对照
type: comparison
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- neural-operator
- message-passing
- structural-dynamics
- equation-of-motion
- spatial-partitioning
- hard-constraints
- hysteresis
- spectral-bias
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117441.pdf
- raw/papers/10_1016_j_cma_2025_118476.pdf
- raw/papers/10_1016_j_cma_2024_117116.pdf
- raw/papers/arxiv_2202_03376.pdf
- raw/papers/10_1007_s10444_023_10065_9.pdf
---

# MTP-MechConv v2 证据对照

## 问题定义
目标不是逐案例用 PINN 优化出一个解，而是训练一个条件化、端到端结构动力算子：支持矩阵边权和 halo 子图，替换本构后主干可复用，覆盖真实结构低/高频，并把 \(M\ddot x+C\dot x+f_\mathrm{int}=F\) 写进架构。正式推理不得依赖 Newmark/FEM 修正。

## 五篇论文的采用边界

| 来源 | 可采用机制 | 不能据此声称 |
|---|---|---|
| [[list2025-unrolled-training-analysis]] | 训练输入覆盖部署状态分布；相同参数量比较；展开课程 | correction 结果证明纯 E2E 更强 |
| [[tesan2025-under-reaching-analysis]] | 物理 reach contract；固定参数量做消息深度消融 | 规则方格公式可原样套任意结构图 |
| [[dolean2024-multilevel-fbpinn-analysis]] | 粗层全局通信 + 细层局部高频；强/弱缩放 | 单 GPU 坐标 PINN 已证明图/硬件任意规模 |
| [[brandstetter2022-mp-pde-analysis]] | 相对状态差、物理参数条件化、temporal bundling | learned update 自动严格满足动力平衡；原速度表公平 |
| [[moseley2023-fbpinn-analysis]] | 子域尺度化、重叠通信、接口敏感性与调度 | FBPINN 已比优化 FEM 快 |

List 等人的核心证据是自回归闭环分布偏移；整段时间并行算子不应机械加入 solver-in-loop。可迁移的是训练期预测扰动/教师闭环状态覆盖，以及 direct 与 correction 指标分栏。^[raw/papers/10_1016_j_cma_2024_117441.pdf]

Tesan 等人的下界说明固定深度在更大图上可能结构性失败；但对局部结构动力图，应把它转化为“细层物理传播预算 + 粗层跨域路径”，而不是按图直径堆叠上千层。^[raw/papers/10_1016_j_cma_2025_118476.pdf]

Dolean 与 Moseley 共同表明，局部尺度化有利于高频，但大量子域还需要粗层全局通信；两篇也都没有证明现有训练比传统数值法快，因此本项目必须把“一次训练、多次直接推理”与“逐案例求解”严格区分。^[raw/papers/10_1016_j_cma_2024_117116.pdf] ^[raw/papers/10_1007_s10444_023_10065_9.pdf]

Brandstetter 等人的图条件化和 temporal bundling 支持跨拓扑与减少调用次数，但其更新没有硬平衡，且原数值速度基线未优化；只能迁移架构原则，不能迁移速度结论。^[raw/papers/arxiv_2202_03376.pdf]

## 冻结前的 v2 架构草案

1. **时间主干**：稳定因果 pole-residue/FFT 与多尺度 FIR 一次输出整段 \(x,v\)，初值用解析 lifting 硬编码；高频 residual 只修正时间特征，不绕过物理层。
2. **细图主干**：每条构件边携带矩阵权重/局部坐标变换，MechConv 使用相对位移、速度和物理参数；核心节点输出、halo 节点只供上下文。
3. **粗图通信**：按楼层/子结构聚合质量、阻尼和连接摘要，执行少量稀疏粗层消息，再 prolong 到细图；细层直通路径保留高频。
4. **本构插件**：统一 `initialize / update / force / tangent / dissipation` 契约；linear、bilinear、Bouc-Wen 共用时间/空间主干，只替换边状态模块和小 adapter。
5. **严格平衡层**：网络预测 \(x,v\) 与本构状态，插件计算 \(f_\mathrm{int}\)，再令 \(a=M^{-1}(F-Cv-f_\mathrm{int})\)。Balance R² 是恒等校验，不作为唯一精度证据。
6. **风险训练**：平均数据/频谱损失之外加入最差样本 CVaR，且按频带、本构、幅值和结构规模分层采样。
7. **推理**：主结果只统计 direct forward；任何梯度 refinement 单独作为失败保险，不参与端到端达标。

## 不可退让的验证

| 维度 | 通过条件 |
|---|---|
| 精度 | pooled \(R^2_{x,v,a,\mathrm{edge}}\ge0.9\)，或每个样本四项均 \(>0.8\) |
| 物理 | 平衡残差接近浮点误差；另报真实 \(a\)、边内力、本构状态/耗散，防止硬平衡指标作弊 |
| 高频 | 预注册真实模态频带；高频子集 \(R^2_{x,v,a,\mathrm{edge}}\ge0.9\) 作为主晋级门槛 |
| 子图 | 多种合法分区下核心输出与全图输出在数值容差内等价 |
| 跨本构 | linear/bilinear/Bouc-Wen 独立测试；主干参数复用率和新增训练成本透明 |
| 规模 | 50/500/5000 DOF 报误差、峰值显存、延迟与吞吐；不得只由 5DOF 外推 |
| 速度 | 同硬件、同精度、优化 Newmark/FEM；含预热、同步和数据搬运，分别报告单样本与批量 |

## 预期失败分流
- 高频不达标但低频已达标：先增加真实频带覆盖和残差头容量，不增加空间深度。
- 大图随直径退化：检查 reach contract 与粗图，而非仅增加训练 epoch。
- 更换本构后全面崩溃：检查插件状态/力接口和条件化，禁止重写时间主干掩盖耦合错误。
- Balance 为 1 但 \(a\) 或边力差：判定为硬平衡指标作弊，按预测物理量失败处理。
- 神经推理只在批量下快：如实限定为高吞吐场景，不宣称低延迟替代 Newmark。

## 关联页面
- [[mtp-mechconv-v2]]
- [[message-passing-reach-contract]]
- [[multilevel-fbpinn]]
- [[unrolled-training]]
- [[mp-pde]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
