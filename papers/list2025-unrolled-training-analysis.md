---
id: paper--list2025-unrolled-training-analysis
title: List et al. (2025) — 瞬态神经物理模拟器的展开训练与可微性
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/list2025-unrolled-training
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_methods:
- one-step-training
- non-differentiable-unrolling
- differentiable-unrolling
- prediction-correction-comparison
legacy_results:
- distribution-shift-reduction
- rollout-accuracy
- parameter-scaling
legacy_failure_modes:
- state-distribution-shift
- weak-parameter-scaling
- solver-dependent-inference
legacy_datasets:
- kuramoto-sivashinsky
- kolmogorov-flow
- cylinder-wake
- aerofoil-flow
legacy_reproducibility: high
legacy_code_url:
- https://github.com/tum-pbs/unrolling
legacy_dataset_url:
- https://github.com/tum-pbs/unrolling
legacy_tags:
- neural-network
- sequence-modeling
- time-marching
- autoregressive-rollout
- long-horizon-rollout
- physics-simulation
- scientific-machine-learning
legacy_sources:
- raw/papers/10_1016_j_cma_2024_117441.pdf
- raw/papers/extracted/10_1016_j_cma_2024_117441_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# Differentiability in unrolled training of neural physics simulators on transient dynamics

## 1. 工程背景
瞬态代理在测试时会反复读取自己的预测，因此单步训练分布与闭环推理分布不同。误差不仅累积，还会把模型推入训练时从未见过的状态。本文用卷积网络和图网络、多个非线性流体系统及 3000 余个模型，系统拆分“看到闭环状态”和“跨时间反向传播”两种效应。

## 2. Research Gap
既有工作常把展开训练的收益全部归因于长程梯度，也常在没有可微传统求解器时退回单步训练。缺少统一实验回答：仅展开但截断时间梯度是否已能缓解分布偏移，以及纯预测与带数值求解器的修正任务是否服从相同规律。

## 3. 科学问题
展开训练的主要收益究竟来自闭环状态分布、长程梯度，还是数值求解器提供的强先验；这些结论能否跨物理系统、架构、网络规模和数值格式保持？

## 4. 研究目标
比较 ONE（单步）、NOG（展开但切断时间梯度）和 WIG（完整可微展开），并在 prediction 与 correction 两种任务中测量推理误差、长时统计、参数缩放和计算成本。

## 5. 方法机制
ONE 只在真值状态上训练一步；NOG 在闭环链中生成输入，但不让梯度穿过前序模拟步；WIG 对整段链完整反传。Prediction 完全由网络推进；correction 则把数值求解器的部分步与网络修正组合。→ [[list2025-unrolled-training-method]]

## 6. 结果证据
在 correction 任务中，NOG 相对 ONE 平均降低 33% 误差，WIG 平均改善 92%；prediction 的误差大致比对应 correction 高一个数量级。增加参数量的经验收敛率约为 \(n^{-1/3}\)，明显弱于经典数值离散。→ [[list2025-unrolled-training-results]]

## 7. 贡献
论文把“闭环分布暴露”和“长程梯度”实验解耦，证明不可微展开本身已有稳定收益；同时给出 prediction/correction 的公平架构对照和参数缩放负面结果。

## 8. 核心知识点
只用真值前态做单步监督会造成部署分布偏移；训练时把模型预测重新喂回模型，即使截断跨步梯度，也能显著改善闭环推理。但数值求解器先验仍是主要优势来源之一。

## 9. Negative Knowledge
本文不证明纯神经 E2E 比数值法更准或更快；相反，作者认为 correction 更实用，并报告网络参数缩放较差。物理系统主要是非线性流体而非结构滞回；因此不能把其 correction 结论直接用作“结构动力端到端推理”的证据。→ [[list2025-unrolled-training-critical]]

## 10. 可迁移知识

| 论文机制 | 对结构动力代理的条件化迁移 |
|---|---|
| NOG 闭环状态暴露 | 可用于训练期教师轨迹扰动或自预测输入课程；正式推理不必带求解器 |
| WIG 长程梯度 | 只在短展开、显存允许且确有累积误差时消融 |
| Prediction/correction 分开报告 | 端到端主指标不得与求解器修正结果混合 |
| 参数缩放审计 | 优先增加物理结构、数据覆盖和局部/粗层通信，不盲目加宽网络 |

## 11. 研究机会
对整段时间并行神经算子，需要验证“全轨迹一次输出”是否已经消除自回归分布偏移；若没有，应比较输入扰动、教师闭环样本和短展开，而不是默认采用 solver-in-loop。

## 12. 可复现性

| 项目 | 说明 |
|---|---|
| 等级 | 🟢 高 |
| 代码/数据 | 官方仓库公开 |
| 规模 | 多系统、多架构、8–20 随机种子，合计 3000+ 模型 |
| 关键控制 | 相同架构与参数量下比较 ONE/NOG/WIG |
| 边界 | correction 的优势依赖数值求解器；结构非线性未验证 |

## 关联页面
- [[unrolled-training]] — 三种展开训练范式
- [[mp-pde]] — pushforward 训练的相邻方案
- [[neural-operator]] — 整段算子与自回归算子的区别

^[sources/papers/list2025-unrolled-training]
