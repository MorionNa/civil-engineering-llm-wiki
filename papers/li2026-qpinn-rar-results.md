---
id: paper--li2026-qpinn-rar-results
title: "Li et al. (2026) — QPINN-RAR 结果证据"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- method/pinn
- evidence/paper
keywords:
- relative-l2-error
- parameter-efficiency
- ten-independent-runs
- burgers-equation
- three-dimensional-heat-equation
sources:
- sources/papers/li2026-qpinn-rar.md
created: '2026-08-06'
updated: '2026-08-06'
confidence: high
evidence_scope: full-text
reproducibility: medium
---

# QPINN-RAR 结果与证据

## 评价设置

论文比较 PINN、PINN-RAR、QPINN 和 QPINN-RAR。训练之外随机抽取 10000 个评价点；所有表格结果均为十次独立运行的均值±标准差。指标包括可训练参数量 $N_p$、最终损失、相对 $L_2$ 误差和收敛迭代数。^[sources/papers/li2026-qpinn-rar.md]

## 一维黏性 Burgers 方程

参数设置为 $\nu=0.01$，定义域 $(x,t)\in[-1,1]\times[0,1]$。表 I 报告：

| 方法 | 参数量 | Loss ($\times10^{-8}$) | 相对 $L_2$ ($\times10^{-4}$) | Epoch |
|---|---:|---:|---:|---:|
| PINN | 2128 | $18.70\pm19.90$ | $7.90\pm4.33$ | $10642\pm341$ |
| PINN-RAR | 2128 | $9.96\pm7.85$ | $6.20\pm2.04$ | $10750\pm360$ |
| QPINN | 1186 | $7.67\pm5.58$ | $5.13\pm2.44$ | $11201\pm622$ |
| QPINN-RAR | 1186 | $6.05\pm2.39$ | $4.96\pm1.38$ | $11140\pm360$ |

QPINN-RAR 相对 PINN、PINN-RAR、QPINN 的平均相对误差分别降低约 37.22%、20.00% 和 3.31%。参数量较经典 PINN 减少约 44.27%，但收敛迭代数并未减少。图 4 的均值—标准差曲线显示 QPINN-RAR 后期误差最低且波动带较窄；图 5 的单随机种子误差图显示四种方法均能恢复整体解形态，差异主要集中在局部误差幅值。

## 论文标为“一维扩散方程”的算例

表 II 报告：

| 方法 | 参数量 | Loss ($\times10^{-6}$) | 相对 $L_2$ ($\times10^{-4}$) | Epoch |
|---|---:|---:|---:|---:|
| PINN | 2128 | $1.37\pm0.90$ | $2.97\pm1.07$ | $10793\pm194$ |
| PINN-RAR | 2128 | $1.65\pm2.61$ | $2.41\pm1.26$ | $10890\pm449$ |
| QPINN | 1186 | $1.28\pm1.27$ | $2.65\pm1.17$ | $10596\pm381$ |
| QPINN-RAR | 1186 | $0.80\pm0.66$ | $2.03\pm0.83$ | $10769\pm263$ |

按论文表格，QPINN-RAR 相对 PINN、PINN-RAR、QPINN 的平均误差分别降低约 31.65%、15.77% 和 23.40%，且四种方法的迭代数相近。图 6–7 显示 QPINN-RAR 的平均误差和局部误差分布较低。

### 方程一致性警报

该算例在正文中被称为 diffusion equation，但显示式包含 $u\,u_x$ 非线性对流项，同时给出 $u(x,t)=\sin(\pi x)e^{-t}$ 为解析解。该解析解不满足所显示的含非线性对流项方程。因此，上述数字只能表述为“论文表 II 报告的结果”，不能无条件视为对该显示方程的有效验证。复现时必须核对作者实际实现的 PDE。

## 三维热方程

定义域为 $(x,y,z)\in[0,1]^3$、$t\in(0,2)$，解析解为：

$$
u_{exact}=e^{-0.3\pi^2t}\sin(\pi x)\sin(\pi y)\sin(\pi z).
$$

表 III 报告：

| 方法 | 参数量 | Loss ($\times10^{-6}$) | 相对 $L_2$ ($\times10^{-2}$) | Epoch |
|---|---:|---:|---:|---:|
| PINN | 2221 | $2.72\pm1.31$ | $2.80\pm1.09$ | $16020\pm1028$ |
| PINN-RAR | 2221 | $2.58\pm1.75$ | $2.03\pm0.54$ | $15915\pm623$ |
| QPINN | 1226 | $9.48\pm5.37$ | $2.03\pm0.57$ | $16081\pm1295$ |
| QPINN-RAR | 1226 | $5.44\pm2.92$ | $1.69\pm0.62$ | $16924\pm843$ |

QPINN-RAR 相对 PINN、PINN-RAR、QPINN 的平均误差分别降低约 39.64%、16.75% 和 16.75%，参数量较经典网络减少约 44.80%。但 QPINN-RAR 的平均迭代数最高，且其最终 loss 并非最低：PINN-RAR 的表中 loss 更低。这说明“较低 PDE 训练损失”和“较低测试相对误差”在该算例中并不完全一致。

## 横向证据解释

- **量子模块效应：** QPINN 相比 PINN 在 Burgers 算例有明显误差改善，在第二算例改善有限，在三维热方程与 PINN-RAR 平均误差相同。
- **RAR效应：** PINN-RAR 通常优于 PINN；QPINN-RAR 在三个表格中均优于 QPINN，说明自适应加点是较稳定的增益来源。
- **组合效应：** QPINN-RAR 的最佳平均误差成立于本文三组实验，但相对 QPINN 的 Burgers 改善仅约 3.31%，需要结合标准差和重复实验看待，而不能只看单次曲线。
- **参数效率：** 约 44% 的参数减少是明确表格证据；计算效率、内存效率和真实量子优势没有相应墙钟时间证据。

## 结果边界

三个实验均是有解析解、固定方程和同分布评价点的单实例拟合。论文未报告复杂边界、参数扫描、几何变化、噪声数据、逆问题、真实硬件、统一训练时间或总能耗。因此结果支持“本文设置下参数更少、平均测试误差较低”，不支持对工程 PDE 或量子计算加速作普遍结论。

## 关联页面

- [[li2026-qpinn-rar-analysis]]
- [[li2026-qpinn-rar-method]]
- [[li2026-qpinn-rar-critical]]
- [[qpinn-rar]]
- [[residual-based-adaptive-refinement]]
