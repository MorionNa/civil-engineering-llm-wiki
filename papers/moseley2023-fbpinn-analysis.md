---
id: paper--moseley2023-fbpinn-analysis
title: Moseley et al. (2023) — FBPINN：有限基域分解 PINN
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/moseley2023-fbpinn
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_methods:
- overlapping-domain-decomposition
- windowed-local-networks
- local-input-normalization
- subdomain-scheduling
legacy_results:
- high-frequency-convergence
- multiscale-convergence
- theoretical-parallel-scaling
legacy_failure_modes:
- interface-discontinuity
- high-dimensional-overlap
- per-instance-training-cost
legacy_datasets:
- sinusoidal-ode
- multiscale-ode
- burgers-equation
- wave-equation
legacy_reproducibility: high
legacy_code_url:
- https://github.com/benmoseley/FBPINNs
legacy_dataset_url:
- https://github.com/benmoseley/FBPINNs
legacy_tags:
- physics-informed
- pinn
- spatial-partitioning
- spectral-bias
- multi-scale-context
- parallel-computing
- scientific-machine-learning
legacy_sources:
- raw/papers/10_1007_s10444_023_10065_9.pdf
- raw/papers/extracted/10_1007_s10444_023_10065_9_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# Finite Basis Physics-Informed Neural Networks

## 1. 工程背景
标准 PINN 在大域和高频/多尺度解上受到全局非凸优化复杂度与谱偏差影响。传统有限元的局部基与域分解提示：可把全局问题拆成多个重叠、局部归一化的小网络。

## 2. Research Gap
既有域分解 PINN 常需额外界面损失，并且没有把局部频率重标度、并行训练调度和连续全局解表示统一起来。

## 3. 科学问题
能否用紧支撑窗函数和局部网络构造连续全局解，使高频问题在每个子域内变成较低频问题，同时让训练计算随子域数近线性扩展？

## 4. 研究目标
提出 FBPINN，在一维低/高/混频、二维问题、Burgers 和时空波动方程上与标准 PINN、Fourier feature PINN 比较准确率、训练步和前向 FLOPs。

## 5. 方法机制
域被划为重叠子域；每个局部网络输入独立归一到 \([-1,1]\)，输出乘平滑窗，再对重叠输出求和。全局连续性由表示构造获得，不增加界面 loss；训练可采用全激活或逐子域/时间推进调度。→ [[moseley2023-fbpinn-method]]

## 6. 结果证据
在频率 \(\omega=15\) 的一维问题上，30 个小子域网络比深宽全局 PINN 更快达到高精度，并使用低多个数量级的前向 FLOPs；混频问题中标准 PINN 的误差约差两个数量级。→ [[moseley2023-fbpinn-results]]

## 7. 贡献
论文把局部归一化解释为高频到低频的尺度变换，并给出仅在重叠区通信的并行训练算法和多类高频/大域案例。

## 8. 核心知识点
子图/子域的价值不只来自显存拆分，还来自局部尺度化；平滑重叠可以减少硬接口损失。但子域数增大后仍需要 [[multilevel-fbpinn]] 的粗层通信。

## 9. Negative Knowledge
论文的波动方程训练约需单 GPU 10 h，而有限差分单 CPU 约 1 min；作者仅把并行版本和算子族训练作为未来可能。论文没有证明单次前向就优于 FEM，也没有结构本构插件。→ [[moseley2023-fbpinn-critical]]

## 10. 可迁移知识

| 机制 | 对结构图的迁移 |
|---|---|
| 局部输入归一化 | 子图坐标、构件长度、局部频率/刚度尺度化 |
| 平滑重叠 | halo 上下文 + 核心节点单写出，或经验证的 partition weights |
| 激活调度 | 按时间/区域残差课程训练，避免所有子图同时高成本更新 |
| 接口位置敏感 | 分区边界避开强非线性铰/刚度突变，或增加其 halo |

## 11. 研究机会
将 FBPINN 的局部尺度化与 MechConv 的矩阵边、粗图通信和可替换本构结合，训练一个条件化解算子而非每个荷载/结构重新优化。

## 12. 可复现性

| 项目 | 说明 |
|---|---|
| 等级 | 🟢 高 |
| 代码/数据 | 官方代码公开，数据均由方程合成 |
| 比较 | 同采样密度、相同约束与框架下比较 PINN/FBPINN |
| 硬件 | 多数非一维实验单 Titan V；论文未实测多 GPU |
| 边界 | FLOPs 主要计网络前向，不含全部训练开销 |

## 关联页面
- [[fbpinn]]
- [[multilevel-fbpinn]]
- [[message-passing-reach-contract]]

^[sources/papers/moseley2023-fbpinn]
