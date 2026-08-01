---
id: paper--chen2026-empm-method
title: Chen 等（2026）— EMPM 方法机制
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
keywords:
- apic
- differentiable-mpm
- online-system-identification
- particle-grid
- real-to-sim-to-real
sources:
- sources/papers/chen2026-empm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
evidence_scope: full-text
---

# EMPM 方法机制

## 架构与数据流

```text
多视角 RGB-D 视频
  → Grounded SAM2 分割
  → 融合三维点云与三维追踪点
  → 将控制器运动转换为边界速度
  → 可微 MPM 时程推进
  → Chamfer / 追踪 / 掩膜损失
  → 梯度法或 CMA-ES 更新参数
  → MPM 粒子预测与高斯渲染
```

论文图 2 将系统划分为数据预处理、模型优化和下游机器人任务三个部分。^[sources/papers/chen2026-empm.md]

## 状态变量与材料参数

时刻 $t$ 的粒子状态包括位置 $x_p$、速度 $v_p$ 和变形梯度 $F_p$。动作条件状态转移写为

$$\hat X_{t+1}=f_\theta(X_t,u_t),$$

其中 $u_t$ 为手或夹爪运动，$\theta$ 包含杨氏模量 $E$、泊松比 $\nu$、密度 $\rho$ 和塑性屈服应力 $y$。

## MPM 更新过程

模拟器采用 APIC 风格的粒子到网格传递，在网格上考虑应力、重力、接触和控制器速度约束，随后执行网格到粒子传递并更新变形梯度。弹性部分采用 Fixed Corotated 模型，塑性部分采用 von Mises 返回映射。手或机器人运动作为 Dirichlet 边界速度进入网格更新，桌面与夹爪接触采用 Coulomb 摩擦。^[sources/papers/chen2026-empm.md]

## 离线参数识别

离线损失由三维 Chamfer 距离和追踪粒子平方误差组成：

$$L_{offline}=\lambda_{dist}\sum_t Chamfer(\hat X_t,\tilde X_t)+\lambda_{trk}\sum_t\sum_{j\in T_t}\lVert\hat X_{t,j}-\tilde X^{trk}_{t,j}\rVert_2^2.$$

Warp 对完整时程推进求导。作者同时保留 CMA-ES 零阶优化选项，以降低反向传播内存需求或执行更激进的参数搜索。

## 在线自适应识别

在线阶段持续将 RGB-D 图像分割并反投影为三维点云。由于长时点追踪在遮挡下不可靠，在线校正不再使用追踪点损失。系统仅在接近静力平衡的时刻执行固定 $H$ 步推进，并最小化

$$L_{online}=\lambda_{dist}L_{dist}+\lambda_{mask}L_{mask}.$$

每次校正得到的新材料参数会替换当前模拟参数。

## 外观耦合

初始点云同时用于建立三维高斯泼溅模型。高斯中心通过线性混合蒙皮跟随邻近 MPM 粒子运动，从而渲染可变形物体的逼真外观。

## 假设与失效边界

- 材料参数在整个物体内部保持常量。
- 在线更新仅在近似平衡状态执行。
- 假设分割、深度和相机标定可靠。
- 离线识别高度依赖点追踪，遮挡会显著降低追踪质量。
- 论文验证的是参数识别和动力学推进，而非闭环自主控制。

## 关联页面

- [[chen2026-empm-analysis]]
- [[chen2026-empm-results]]
- [[chen2026-empm-critical]]
- [[entities/empm]]
