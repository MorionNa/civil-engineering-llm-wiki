---
id: papers--li2025-localized-waves-pinn-method
title: Li & Wang (2025) — Bäcklund 变换约束双输出 PINN：方法机制
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- evidence/paper
- method/pinn
keywords:
- ai4s
- collocation-strategy
- deep-learning
- neural-network
- nonlinear-systems
- physics-informed
- physics-simulation
- pinn
- soft-constraint
sources:
- sources/papers/li2025-localized-waves-pinn.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- backlund-transformation
- multi-output-pinn
- automatic-differentiation
- latin-hypercube-sampling
- lbfgs
- xavier-initialization
- adaptive-loss-weighting
results:
- two-equation-simultaneous-solution
- unsupervised-v-reconstruction
failure_modes:
- irreversible-transformation
- missing-weight-update-rule
- soft-constraint-nonuniqueness
- missing-code
datasets:
- modified-kdv-one-soliton
- modified-kdv-two-soliton
- gaussian-initial-wave
reproducibility: low
---

# Li & Wang (2025) — 方法机制

> 返回总览：[[li2025-localized-waves-pinn-analysis]]；中心方法实体：[[backlund-transformation-pinn]]

## 5.1 两条非线性 PDE 与非可逆关系

目标方程记为 $G(v)=0$：

$$G(v)=v_t-\frac32v_x\sin^2v-\frac12v_x^3-v_{xxx}.$$

mKdV 方程记为 $F(u)=0$：

$$F(u)=u_t-\frac32u^2u_x-u_{xxx}.$$

二者通过 Bäcklund 关系连接：

$$u=\sin v-v_x,\qquad BT(u,v)=u-\sin v+v_x=0.$$

若 $v$ 已知，$u$ 可直接计算；若 $u$ 已知，关系变成关于 $v$ 的非线性一阶微分约束，不能直接给出唯一显式解。因此网络并非“学习一个已知逆公式”，而是同时满足 $F=0$、$G=0$ 与 $BT=0$ 来寻找可行解。

## 5.2 双输出网络与信息流

```text
(x,t) ──► 4×100 tanh 前馈网络 ──► û(x,t) ──AD──► F(û)
                              └──► v̂(x,t) ──AD──► G(v̂)
                                  û,v̂,v̂x ─────► BT(û,v̂)
u 的初值/边值 ─────────────────────────────────► MSE_u
```

网络同时输出 $\hat u$ 和 $\hat v$。只有 $u$ 的初边界样本进入数据项；$v$ 没有观测标签，因此作者称其为无监督生成。与经典 [[raissi2019-pinn-method]] 相比，关键变化是增加第二个输出、第二条 PDE 残差和跨输出变换残差。

## 5.3 四项联合损失

$$\mathcal L=\omega_{IC}MSE_u+\omega_FMSE_F+\omega_GMSE_G+\omega_{BT}MSE_{BT},$$

其中

$$MSE_u=\frac1{N_u}\sum_{n=1}^{N_u}|\hat u(x_u^n,t_u^n)-u^n|^2,$$

$$MSE_F=\frac1{N_f}\sum_{n=1}^{N_f}|F(\hat u(x_f^n,t_f^n))|^2,$$

$$MSE_G=\frac1{N_f}\sum_{n=1}^{N_f}|G(\hat v(x_f^n,t_f^n))|^2,$$

$$MSE_{BT}=\frac1{N_f}\sum_{n=1}^{N_f}|BT(\hat u,\hat v)|^2.$$

这四项分别承担“锚定已知解、保证源方程、保证目标方程、耦合两解”的角色。目标方程残差尤其重要：它补足 Bäcklund 逆向关系缺乏唯一显式解的问题，但仍不构成数学唯一性证明。

## 5.4 采样、网络与优化

| 组件 | 论文给出的设置 |
|------|----------------|
| 初边界点 | 单波案例 $N_u=200$ |
| 内部配点 | 单波案例 $N_f=10{,}000$，Latin hypercube sampling |
| 架构 | 4 个隐藏层，每层 100 个神经元；输入 $(x,t)$，输出 $(u,v)$ |
| 激活函数 | tanh |
| 初始化 | Xavier |
| 优化器 | limited-memory quasi-Newton（L-BFGS） |
| 导数 | 自动微分，最高到三阶空间导数 |
| 损失权重 | 论文只说“随训练调整”，没有给出更新公式 |

与 [[pinn]] 常见的 Adam→L-BFGS 两阶段训练不同，本文正文只明确写了 L-BFGS，不应擅自补入 Adam。缺少权重策略使四项残差的实际平衡无法严格复现。

## 5.5 初边值设置

mKdV 采用 Dirichlet 边界：

$$u(x_{lb},t)=u_1(t),\quad u(x_{ub},t)=u_2(t),\quad u(x,t_0)=u_0(x).$$

三类输入为：一孤子 $u=2k\operatorname{sech}(kx+k^3t)$、论文给出的双孤子解析式、以及 $u_0(x)=e^{-x^2/20}$ 且两侧边界为零的高斯波包。解析/程序生成数据仅用于 $u$；$v$ 由关系约束恢复。

## 5.6 方法定位

- 相对 [[wang2023-pinn-spurious-method]]：本文没有处理残差伪解，而是增加一个物理关系残差；两者可组合。
- 相对 [[wang2024-kinn-method]]：本文创新在损失约束图，不在网络骨干；理论上可把 MLP 换成 KAN。
- 相对普通多任务学习：两个输出不是松散任务，而是由精确的微分变换耦合。

## 复现警示

双波实验没有在正文完整披露 $k_1,k_2,\alpha,\beta$ 的取值，Gaussian 案例也没有完整报告时间区间、采样数和相对误差；此外没有代码、随机种子、浮点精度、停止准则或硬件。因此只能可靠重建方法框架，不能保证逐数值复现。

## 关联页面

- [[li2025-localized-waves-pinn-results]] — 每组设置与指标
- [[li2025-localized-waves-pinn-critical]] — 逆变换、多解性与软约束风险
- [[raissi2019-pinn-analysis]] — 经典算子非线性 PINN
- [[pinn]] — PINN 实体页

## Evidence By Source

### `sources/papers/li2025-localized-waves-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1007_s11071-024-10359-7.pdf`

^[sources/papers/li2025-localized-waves-pinn.md]
