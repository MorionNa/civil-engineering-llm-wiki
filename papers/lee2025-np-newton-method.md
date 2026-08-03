---
id: papers--lee2025-np-newton-method
title: Lee et al. (2025) — NP-Newton 方法机制
type: paper-analysis
status: verified
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
- method/neural-operator
keywords:
- right-preconditioning
- FPNO
- MIONet
- Newton
sources:
- sources/papers/lee2025-np-newton.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
reproducibility: medium
code_url: []
dataset_url: []
---

# NP-Newton 方法机制

## 原问题与右预条件

目标仍是求 (F(u^star)=0)。若 (Mapprox F^{-1})，论文对复合残差 (widetilde F(u)=F(M(u))) 应用 Newton：

[
v^{(k)}=M(u^{(k)}),qquad
u^{(k+1)}=v^{(k)}-lambda_k[F'(v^{(k)})]^{-1}F(v^{(k)}).
]

因此学习器不会替换 (F)、Jacobian 或最终终止条件。关联 [[np-newton]]。

## FPNO

令 (r=F(u))、(	ilde r=r/|r|_2)，则：

[
eta=	anh(|r|_2N(	ilde r)),qquad
G(u)=u+eta G_B(u).
]

- (G_B) 是 MIONet 骨干，输出场校正。
- (N) 只输出标量步长。
- (etain(-1,1))，允许负步长绕开不平衡非线性导致的错误下降方向。
- (|r|	o0) 时 (G(u)	o u)，降低近根处扰动。

## 训练数据与损失

1. 从幅值 (10^{-4})–(10^{-2}) 的高斯随机场采样初值。
2. 用传统 Newton 完整求解并保存每个中间迭代 (u_j^{(i)}) 与收敛解 (u_j^star)。
3. 训练“当前迭代点/问题参数 → 收敛解”的映射。
4. 使用带 (epsilon=10^{-4}) 的相对 MSE，AdamW、batch 100、weight decay (5	imes10^{-4})、学习率 (10^{-4})。
5. 验证误差连续 1000 epoch 不改善时停止。

这一路线依赖求解器生成的监督标签，不属于严格 label-free。

## 求解与终止

FEniCS 负责有限元离散与训练样本；PETSc/petsc4py 实现 Newton，MUMPS 解每个线性化系统。任一条件满足即终止：

[
|r^{(i)}|_2le10^{-15}
quad	ext{或}quad
|r^{(i)}|_2/|r^{(0)}|_2le10^{-9}.
]

## 面向本项目的受限迁移

对非线性动力学，合理映射是“每个时间步的隐式离散残差 → 候选状态校正”，而不是用 FPNO 直接生成整段未认证轨迹。本构历史只能在候选被原残差/耗散/边界门接受后提交。需与 [[fixed-point-neural-operator]]、[[inference-speed-evidence-2026-08-03]] 联用。

## 假设与失败边界

- 论文简化讨论假设 Jacobian 非奇异；奇异/分岔需伪逆、LM 或弧长法。
- 神经预条件成本在容易问题上可能大于节省的 Newton 工作。
- 从粗网格到细网格的效果依赖算子表达与坐标编码，不等于任意拓扑迁移。

## Evidence By Source

^[sources/papers/lee2025-np-newton.md]

