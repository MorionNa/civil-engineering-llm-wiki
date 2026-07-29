---
title: "Hu et al. (2022) — XPINN 五类 PDE 泛化结果"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [physics-informed, pinn, domain-decomposition, xpinn, pde, benchmark, cross-domain-generalization]
sources: [raw/papers/hu2022-xpinn-generalization.pdf]
results: [cross-domain-generalization, benchmark]
datasets: [synthetic-data]
confidence: high
---

# XPINN 五类 PDE 泛化结果

> 返回 [[hu2022-xpinn-generalization-analysis]] · 方法 [[hu2022-xpinn-generalization-method]] · 实体 [[xpinn]]

## 1. 结果矩阵

| PDE | PINN relative L2 | XPINN relative L2 | bound (PINN/XPINN) | 结论 |
|---|---:|---:|---:|---|
| KdV | 6.899e-1 | 6.955e-1 | 100% / 121.08% | 相近，PINN 略优 |
| Heat | 1.778e-3 | 4.490e-3 | 100% / 243.22% | PINN 明显优 |
| Advection | 2.052e-1 | 1.617e-1 | 100% / 66.59% | XPINN 优 |
| Poisson | 5.553e-2 | 1.108e-1（最佳 XPINN3） | 100% / 106.28% | PINN 优 |
| Euler | 3.4604e-2 | 1.048e-2（AM） | 100% / 81.09% | 结构对齐 XPINN 优 |

来源：PDF pp. 12–18, Tables 1–6。

## 2. KdV：近似平衡

复杂振荡区与平滑区分开后，局部复杂度降低，但每域数据更少；两项近乎抵消，测试误差几乎相同。

## 3. Heat：样本稀释占主导

上下分区使 top 子网 complexity 达 PINN 的 156.24%；XPINN 误差约为 PINN 的 2.5 倍。分区没有带来足够的目标简化。

## 4. Advection：对齐间断路径有效

三个子域内目标近似常值，各子网 complexity 为 PINN 的 40.53%/53.16%/79.95%，XPINN 误差更低。注意正文一句把 0.2052 与 0.1617 的主语写反，应以 Table 3 为准。

## 5. Poisson：loss 竞争

XPINN1 界面误差大；加一阶导界面正则得到 XPINN2 后，边界误差上升；提高边界权重得到 XPINN3 后界面误差又反弹。最佳 XPINN 仍比 PINN 差约 2 倍。（PDF pp. 16–17, Tables 4–5, Figure 9）

## 6. Euler：分区质量决定方向

沿激波带划分 XPINN-AM 将常值区与复杂带隔离，误差为 0.01048；简单上下划分 XPINN-TB 为 0.035722，与/略差于 PINN 0.034604。

## 7. 文本一致性审计

PDF 结论段把 heat 同时列入 XPINN 胜/败示例，并提到正文五题之外的 wave；因此知识库采用表格重建结果，不传播该总结句。

## 8. 有界结论

XPINN 的优势来自分区与解结构对齐，而非“子网更多”。真实应用应在未知真解、非 oracle 分区下重新验证。

> 页面导航：[[hu2022-xpinn-generalization-analysis]] · [[hu2022-xpinn-generalization-method]] · [[hu2022-xpinn-generalization-critical]] · [[pinn]]