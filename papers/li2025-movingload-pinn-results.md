---
id: papers--li2025-movingload-pinn-results
title: Li et al. (2025) — 实验结果：五组数值实验验证
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
keywords:
- bridge-dynamics
- equation-of-motion
- physics-informed
- pinn
- structural-dynamics
- synthetic-data
sources:
- sources/papers/li2025-movingload-pinn.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
results:
- bridge-dynamics
- moving-load-response
- nondimensional-pde
- uniform-beam
- non-uniform-beam
- parameter-identification
- inverse-problem
---

# Li et al. (2025) — 实验结果展开

> 返回概述 → [[li2025-movingload-pinn-analysis]]

---

## 实验概览

论文通过五组数值实验系统验证了所提方法的有效性，覆盖正问题和反问题两种场景。所有案例的参考解由有限元方法（FEM）提供。

| Case | 桥型 | 已知量 | 未知量 | PINN 模式 | 验证指标 |
|------|------|--------|--------|-----------|----------|
| 1 | 均匀梁 | 全部参数 | 无 | DP | 位移时程 vs FEM |
| 2 | 非均匀梁 | 全部参数 | 无 | DP | 位移时程 vs FEM |
| 3 | 均匀梁 | 除 P 外全部 | 移动荷载大小 P | DPD | P 推断精度 |
| 4 | 均匀梁 | 除 E 外全部 | 弹性模量 E | DPD | E 推断精度 |
| 5 | 均匀梁 | 除边界外全部 | 边界约束刚度 | DPD | 边界刚度推断精度 |

---

## Case 1: 均匀梁 (PINN-DP 正问题)

**设置：** 简支均匀 Euler-Bernoulli 梁，跨径 L，抗弯刚度 EI，线密度 ρA，移动恒载 P 以匀速 v 通过。

**关键参数：**
- 阻尼比 $\xi = 0.02$
- 无量纲速度 $\bar{v} = 0.25$
- 高斯近似参数 $\sigma = L/200$

**结果：**

| 指标 | 数值 |
|------|------|
| 跨中挠度时程 vs FEM | 高度吻合（相对 L2 误差 < 2%） |
| 最大挠度时刻 | 准确捕获（误差 < 1%） |
| 荷载离开后的自由振动 | 振幅和相位均与 FEM 一致 |

**消融研究 — 傅里叶嵌入效果：**

| 配置 | 相对 L2 误差 |
|------|-------------|
| 无傅里叶嵌入 | ~8% |
| k=5 傅里叶嵌入 | ~2% |
| k=10 傅里叶嵌入 | ~1.5% |

→ 傅里叶嵌入显著提升精度，k 从 5 到 10 边际改善递减。

**消融研究 — 因果权重效果：**

| 配置 | 相对 L2 误差 | 现象 |
|------|-------------|------|
| 无因果权重 | ~5% | 早期时刻有明显偏差 |
| 有因果权重 | ~2% | 全时域误差均匀分布 |

---

## Case 2: 非均匀梁 (PINN-DP 正问题)

**设置：** 简支变截面梁，截面高度沿跨径线性变化：$h(x) = h_0[1 + \alpha(x/L - 0.5)]$。

**挑战：** 变截面导致 $EI(x)$ 和 $\rho A(x)$ 沿跨径变化，PDE 中出现变系数和空间导数耦合项。

**结果：**

| 指标 | 数值 |
|------|------|
| 跨中挠度时程 vs FEM | 吻合良好（相对 L2 误差 < 3%） |
| 截面变化处 | 响应过渡平滑，无非物理振荡 |
| 最大挠度 | 较均匀梁增大（因刚度降低），PINN 准确捕获 |

> **关键发现：** 非均匀梁的变系数 PDE 对 PINN 的自动微分求导能力提出了更高要求——$\frac{\partial^2}{\partial x^2}[EI(x)\frac{\partial^2 u}{\partial x^2}]$ 项需要计算四阶导数，但 PINN 仍能稳定求解。

---

## Case 3: 未知移动荷载 (PINN-DPD 反问题)

**设置：** 均匀梁，荷载大小 P 未知。在跨中布置 1 个监测点，记录挠度时程 $u_{obs}(L/2, t)$。

**结果：**

| 指标 | 数值 |
|------|------|
| P 推断误差 | < 0.5% |
| 所需监测数据量 | 跨中单点约 200 个时步 |
| 收敛速度 | ~8,000 Adam + ~3,000 L-BFGS |

**对监测数据量的敏感性：**

| 监测数据（时步数） | P 推断误差 |
|-------------------|-----------|
| 50 | ~3% |
| 100 | ~1.2% |
| 200 | < 0.5% |
| 全时程 (500) | < 0.3% |

→ 仅需约 100-200 时步的单点监测数据即可获得高精度参数推断。

---

## Case 4: 未知弹性模量 (PINN-DPD 反问题)

**设置：** 均匀梁，弹性模量 E 未知。同样在跨中布置 1 个监测点。

**挑战：** E 出现在 PDE 的四阶导数项系数中，对解的全貌（频率、振幅）影响更为全局，推断难度大于荷载大小。

**结果：**

| 指标 | 数值 |
|------|------|
| E 推断误差 | < 1% |
| 所需监测数据量 | 跨中单点约 200 个时步 |

**推断过程中的频率自校准：** 由于 E 直接影响桥梁固有频率 $\omega_n = n^2\pi^2\sqrt{EI/(\rho A L^4)}$，PINN 本质上是通过匹配监测数据中的振动频率来自动推断 E。

---

## Case 5: 未知边界条件 (PINN-DPD 反问题)

**设置：** 均匀梁，边界条件未知。实际边界为弹性支撑（介于简支和固支之间），将弹性约束刚度 $k_\theta$ 作为待推断参数。

**挑战：** 边界条件对全梁响应的影响主要集中在支座附近和低频模态——仅靠跨中测点可能难以区分不同的边界约束。

**结果：**

| 指标 | 数值 |
|------|------|
| $k_\theta$ 推断误差 | < 2% |
| 所需监测数据量 | 跨中单点约 200 个时步 |

> **洞察：** 即使监测点不位于支座附近（仅跨中），PINN 仍能通过物理约束将边界信息"传播"到监测位置，实现边界参数的间接推断。

---

## 5.6 应用讨论

论文进一步讨论了方法的工程应用前景：
- **SHM 实时评估：** 将少量传感器数据输入 PINN-DPD 可实时推断桥梁状态参数
- **荷载识别：** 从响应反推通过的车辆重量——桥梁动态称重（BWIM）的新途径
- **损伤检测：** 弹性模量 E 的降低可间接指示结构损伤

---

## 结果总结

| 维度 | 结论 |
|------|------|
| 正问题精度 | PINN-DP 与 FEM 参考解高度吻合（L2 误差 < 3%） |
| 反问题精度 | 单测点、少量数据即可高精度推断参数（误差 < 2%） |
| 傅里叶嵌入 | 将精度从 ~8% 提升至 ~2%，是关键增强 |
| 因果权重 | 消除早期偏差，使全时域误差均匀化 |
| 数据效率 | 100-200 时步测点数据足够高精度反演 |

## 关联页面

- [[li2025-movingload-pinn-analysis]] — 返回概述
- [[li2025-movingload-pinn-method]] — 方法机制
- [[li2025-movingload-pinn-critical]] — 贡献 / Negative / 可迁移
- [[pinn]] — 物理信息神经网络实体

## Evidence By Source

### `sources/papers/li2025-movingload-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_aei_2025_103215_extracted.txt`

^[sources/papers/li2025-movingload-pinn.md]
