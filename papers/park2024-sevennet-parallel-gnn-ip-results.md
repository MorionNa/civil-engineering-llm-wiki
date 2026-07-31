---
title: "Park et al. (2024) SevenNet Results"
created: 2026-07-31
updated: 2026-07-31
type: paper-results
---

# SevenNet 实验结果

## Parallel efficiency

论文在 GPU 集群上测试：

- weak scaling；
- strong scaling。

32 GPU 弱扩展测试中保持超过 80% 并行效率。

## SevenNet-0

使用 Materials Project 数据训练通用 GNN-IP：

- 89 种元素；
- M3GNet 数据集。

测试指标：

- energy MAE: 24 meV/atom；
- force MAE: 0.067 eV/Å；
- stress MAE: 0.65 GPa。

## Large-scale MD

SevenNet-0 用于：

- 非晶 Si3N4；
- 112,000 atoms；
- GPU 集群 melt-quench 模拟。

论文报告 60 ps 模拟约 12.7 小时。

## 主要结论

GNN-IP 不再局限于小尺度材料模拟，可以通过专门并行算法进入大规模 MD 场景。
