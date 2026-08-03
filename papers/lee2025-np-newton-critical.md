---
id: papers--lee2025-np-newton-critical
title: Lee et al. (2025) — NP-Newton 批判与迁移边界
type: paper-analysis
status: verified
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
- method/evaluation
keywords:
- negative-knowledge
- structural-dynamics-transfer
- solver-certification
sources:
- sources/papers/lee2025-np-newton.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
reproducibility: medium
code_url: []
dataset_url: []
---

# NP-Newton 批判、Negative Knowledge 与迁移机会

## 贡献判定

论文最有价值的贡献不是某个特定 MIONet，而是“学习非线性预条件路径 + 原残差最终认证”的职责分离。该结构天然避免把网络内部代数恒等式误当作独立物理正确性。

## Negative Knowledge

1. **容易问题会负加速。** 小变形 Newton-LS 已很快，额外神经调用使墙钟变差。
2. **不是无标签。** 训练目标来自大量 Newton 中间态与收敛解；生成成本必须计入方法账本。
3. **根集合等价需谨慎。** 论文目标仍以原 (F(v)) 收敛为准，但学习映射本身没有保证全局单射、分支选择或跨分岔正确。
4. **没有动力学历史。** Neo-Hookean 是准静态；Bouc-Wen/塑性/损伤的 commit/rollback 语义未处理。
5. **规模证据有限。** 最大列出的网格是 16,641 DOF Poisson；尚非 50kDOF 结构时程。
6. **代码缺失。** 网络和超参数较详细，但无公开仓库与预训练权重。

## 不应照搬

- 不应每个时间步无条件调用 FPNO；应以残差、预测置信度或预计 Newton 次数门控。
- 不应让网络直接提交本构历史；必须由原插件在校正接受后 commit。
- 不应把“收敛更快”当作响应预测准确；仍需 (u/v/a/F) R²、最差样本与独立 EOM。
- 不应忽略基线的稀疏线性求解器、容差、预条件、回退和加载步协议。

## 对 nonlinear-pinn 的迁移推论

候选应采用结构专属的 **physics-certified neural predictor/preconditioner**：

1. MTP/模态算子先给出时间步候选；
2. 原离散 EOM 与可插拔本构计算独立残差；
3. 仅在困难步调用残差条件校正；
4. 原 Newton/信赖域完成少步收敛并给出证书；
5. 若校正失败，回退原求解器并把该 case 计入速度与失败率。

这可直接攻击 [[inference-speed-evidence-2026-08-03]] 中“Newton 高迭代场景才可能有速度优势”的缺口，同时保留 [[current-structural-pinn-ranking-2026-08-03]] 的精度要求。

## 研究机会

- 以已有 MTP-bu 作为初值器，而不是重新训练完全无标签网络。
- 将空间校正限制到活动塑性/滞回边或子结构，避免 50kDOF 全局神经开销。
- 对低频简单步禁用校正，对突加载/高频/强滞回步启用。
- 与 [[fixed-point-neural-operator]] 的有界步长结合，同时增加信赖域接受比和能量/耗散 veto。

## 可复现性结论

**🟡 中复现性。** 方程、数据规模、网络宽度、训练时间、硬件、容差和结果表完整；公开代码、权重与数据生成脚本缺失。

## Evidence By Source

^[sources/papers/lee2025-np-newton.md]

