---
id: paper--li2022-bfemp-method
title: "Li et al. (2022) — BFEMP 方法机制"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- variational-time-integration
- particle-simplex-contact
- projected-newton
- lagged-friction
- continuous-collision-detection
sources:
- sources/papers/li2022-bfemp.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# BFEMP 方法机制

## 1. 统一增量势

BFEMP 将 FEM 节点和 MPM 网格节点堆叠为统一自由度。对 backward Euler 或 Newmark-β，惯性与超弹性能组成增量势：

$$\Pi(x)=\frac12\lVert x-\hat x^n\rVert_M^2+2\alpha\beta\Delta t^2\Psi(x).$$

FEM 和 MPM 在无接触时各自独立；接触势加入后形成单体求解。^[sources/papers/li2022-bfemp.md]

## 2. 两种离散的状态流

- FEM：线性三角形/四面体，总拉格朗日节点自由度；
- MPM：材料粒子承载历史，笛卡尔网格承载隐式求解自由度，采用二次 B 样条；
- 粒子–网格传递可选 APIC、PIC 或 FLIP。

接触力先作用在粒子位置，再通过粒子位置对网格节点位置的导数，以链式法则映射至 MPM 网格自由度。

## 3. 粒子–单纯形障碍接触

二维使用粒子–边距离，三维使用粒子–三角形距离。障碍密度为

$$b(d,\hat d)=\begin{cases}-\kappa(d/\hat d-1)^2\ln(d/\hat d),&0<d<\hat d,\\0,&d\ge\hat d.\end{cases}$$

其在零距离发散，在激活距离外为零。边界积分由粒子权重离散；为避免最近边/面 `min` 运算的非光滑性，论文用边界原语障碍求和并对节点/边重复贡献进行补偿。

## 4. 摩擦势

Coulomb 摩擦在速度阈值 $\epsilon_v$ 附近平滑。接触集、法向力幅值和切向基在一次非线性最小化内固定，由上一轮更新，从而构造可积的滞后耗散伪势。外层交替执行：

1. 固定摩擦算子求解增量势；
2. 更新接触集、法向力和切向基；
3. 直到摩擦残差收敛。

## 5. 非线性求解

每个局部弹性、障碍与摩擦 Hessian 投影为半正定，再与质量矩阵组装。投影 Newton 方向由 CHOLMOD 求解，Armijo 回溯保证能量下降。

初始线搜索步长取所有约束临界步长的 0.9 倍：

- CCD 给出粒子–FEM 原语距离降至零的临界值；
- 变形梯度行列式多项式根给出 $\det F=0$ 的临界值。

因此所有后续回溯步均保持不穿透与非退化。

## 6. MPM 不规则边界

当 FEM 节点位移全部给定时，FEM 域不再是未知结构，而成为显式几何边界。该边界可移动、分离并具有可控摩擦，避免传统网格速度边界的涂抹穿透和分离黏连。

## 7. 输入与输出

- 输入：FEM 网格及材料、MPM 粒子/网格及材料、时间积分参数、摩擦系数；
- 关键参数：接触激活距离 $\hat d$、障碍刚度 $\kappa$、静摩擦阈值 $\epsilon_v$、Newton 容差 $\epsilon_d$；
- 输出：FEM 下一步节点状态与 MPM 下一步粒子状态。

## 8. 假设与边界

- 初始 FEM 与 MPM 域必须不重叠；
- 粒子表面权重假设粒子分布近似均匀；
- 不穿透约束针对粒子中心和 FEM 边界，未考虑粒子域形状；
- 摩擦 lagging 对任意大时间步不保证收敛；
- 不包含切割、离散类型转换和拓扑重构。

## 关联页面

- [[li2022-bfemp-analysis]]
- [[li2022-bfemp-results]]
- [[li2022-bfemp-critical]]
- [[entities/bfemp]]
