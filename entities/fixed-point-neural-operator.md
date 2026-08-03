---
id: entity--fixed-point-neural-operator
title: Fixed-Point Neural Operator (FPNO)
type: entity
status: verified
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- method/neural-operator
keywords:
- FPNO
- residual-conditioned-step
- nonlinear-preconditioner
- MIONet
sources:
- sources/papers/lee2025-np-newton.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# Fixed-Point Neural Operator (FPNO)

## 定义

FPNO 是 [[np-newton]] 的非线性右预条件器。对当前迭代 (u)，先算原残差 (r=F(u))，再以归一化残差预测有界标量步长，并由骨干神经算子输出校正方向：

[
G(u)=u+eta G_B(u),qquad
eta=	anh!left(lVert r
Vert_2 N(r/lVert r
Vert_2)
ight).
]

当残差趋于零时 (eta	o0)，故预条件器趋近恒等映射。允许 (eta<0) 是其处理不平衡非线性的关键设计。

## 训练证据

训练样本来自传统 Newton 轨迹的“当前迭代点 → 已收敛解”对，因此不是无标签方法。论文以 MIONet 为骨干，但明确允许替换为 DeepONet、FNO 或其他算子。

## 项目迁移边界

在非线性结构动力学中，输入必须包含时间步状态、外荷载、原残差和本构历史；输出只能作为候选校正，不能绕过原 EOM、本构提交、边界条件和耗散检查。关联 [[physics-constrained-training-failure-modes]] 与 [[inference-speed-evidence-2026-08-03]]。

## 关联

- [[lee2025-np-newton-method]]
- [[np-newton]]
- [[one-structure-one-model-contract-2026-08-03]]
- [[fixed-mdof5-mtp-strict-label-free-v1-nogo-20260803]]

## Evidence By Source

^[sources/papers/lee2025-np-newton.md]
