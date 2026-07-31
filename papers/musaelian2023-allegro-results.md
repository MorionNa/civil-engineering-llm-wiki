---
id: paper-musaelian2023-allegro-results
title: Musaelian et al. (2023) — Allegro 结果证据
type: paper-analysis
status: verified
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- evidence/paper
- method/transformer
keywords:
- ai4s
- deep-learning
- gpu-computing
- material-design
- neural-network
- physics-simulation
- scientific-machine-learning
- se3-equivariance
sources:
- sources/papers/musaelian2023-allegro.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: high
results:
- revmd17-accuracy
- qm9-accuracy
- temperature-transfer
- li3po4-dynamics
- strong-scaling
- hundred-million-atom-simulation
datasets:
- revised-md17
- 3bpa
- qm9
- li3po4
- silver-vacancy
reproducibility: high
---

# Allegro 结果证据

## 结果评价框架

论文围绕三个问题组织证据：

1. 严格局部表示是否会牺牲精度；
2. 局部模型能否在分布外温度和真实动力学中保持物理保真度；
3. 模型是否能在多 GPU 空间分解中扩展到千万至亿级原子。

## revised MD-17

Allegro 在 revised MD-17 的十个小分子上报告能量和力 MAE。多数分子的力误差优于或接近 NequIP，说明取消跨层 atom-centered message passing 并没有必然造成精度下降。^[raw/papers/musaelian2023-allegro-source.md]

部分力 MAE（meV/Å）：

| 分子 | ACE | NequIP | Allegro |
|---|---:|---:|---:|
| Aspirin | 17.9 | 8.2 | 7.3 |
| Azobenzene | 10.9 | 2.9 | 2.6 |
| Benzene | 0.5 | 0.3 | 0.2 |
| Ethanol | 7.3 | 2.8 | 2.1 |
| Naphthalene | 5.1 | 1.3 | 0.9 |
| Malonaldehyde | 11.1 | 5.1 | 3.6 |

^[raw/papers/musaelian2023-allegro-source.md]

结果边界：不同论文或表格中的训练设置、cutoff 和参数量不完全一致，因此这些数字证明 Allegro 具有竞争力，但不是严格的同算力 Pareto 比较。

## 3BPA 温度迁移

所有模型只在 300 K 的 500 个 3BPA 构型上训练，再测试 300、600、1200 K。Allegro 与 NequIP 显著优于 ACE、sGDML、GAP、经典力场和 ANI，说明等变模型在更高温度构象上具有更强外推。^[raw/papers/musaelian2023-allegro-source.md]

| 测试温度 | Allegro 能量 RMSE (meV) | Allegro 力 RMSE (meV/Å) | NequIP 力 RMSE (meV/Å) |
|---|---:|---:|---:|
| 300 K | 3.84 | 12.98 | 10.77 |
| 600 K | 12.07 | 29.11 | 26.37 |
| 1200 K | 42.57 | 82.96 | 76.18 |

NequIP 在该表中略优于 Allegro，但两者远优于其他局部方法。该结果支持“严格局部没有破坏等变模型的温度迁移优势”，而不是证明 Allegro 在所有精度指标上都优于 NequIP。

## QM9：化学组成空间

QM9 包含约 134k 个由 C、H、O、N、F 构成的小分子。论文比较 $U_0$、$U$、$H$、$G$ 四个能量相关目标。^[raw/papers/musaelian2023-allegro-source.md]

| 模型 | $U_0$ | $U$ | $H$ | $G$ | 单位 |
|---|---:|---:|---:|---:|---|
| DimeNet++ | 6.3 | 6.3 | 6.5 | 7.6 | meV |
| PaiNN | 5.9 | 5.7 | 6.0 | 7.4 | meV |
| Allegro, 1 layer | 5.7 | 5.3 | 5.3 | 6.6 | meV |
| Allegro, 3 layers | 4.7 | 4.4 | 4.4 | 5.7 | meV |

单层 Allegro 已优于表中已有 message-passing 与 Transformer 基线，三层模型进一步改善。这是“局部深度提高高阶局部表达，而不扩大通信半径”的关键证据。

需要注意：QM9 模型参数量达到百万级，不能与材料扩展实验中约九千参数的小模型混为同一配置。

## Li$_3$PO$_4$：结构与动力学

训练数据来自 3000 K 熔融和 600 K 淬火 AIMD。用于动力学与扩展实验的小模型只有约 9058 个权重，测试集能量 MAE 为 1.7 meV/atom，力 MAE 为 73.4 meV/Å。^[raw/papers/musaelian2023-allegro-source.md]

论文开展十组 600 K、50 ps 的 Allegro MD：

- 全原子径向分布函数与 AIMD 基本一致；
- P–O–O 四面体角分布与 AIMD 一致；
- Li 均方位移曲线与 AIMD 接近。

该实验的价值在于：同一个小模型既用于物理保真度验证，也用于后续扩展测试，避免用一个大模型报告精度、另一个小模型报告速度。

## 计算复杂度

论文总结 Allegro 的主要扩展性质：

- 对原子数 $N$：$O(N)$；
- 对每原子邻居数 $M$：$O(M)$；
- 对元素种类数 $S$：学习通道数可保持 $O(1)$，不同于显式按元素组合扩张的局部基。

^[raw/papers/musaelian2023-allegro-source.md]

这里的 $O(1)$ 指网络通道维度可与元素数解耦，不表示多元素体系的训练难度和数据需求完全不随元素数增长。

## 强扩展：421,824 原子 Li$_3$PO$_4$

固定系统规模，A100 GPU 从 1 增至 64。^[raw/papers/musaelian2023-allegro-source.md]

| GPU 数 | 速度 (ns/day) | 微秒/(atom·step) |
|---:|---:|---:|
| 1 | 0.518 | 0.552 |
| 2 | 1.006 | 0.284 |
| 4 | 1.994 | 0.143 |
| 8 | 3.810 | 0.075 |
| 16 | 6.974 | 0.041 |
| 32 | 11.530 | 0.025 |
| 64 | 15.515 | 0.018 |

从 1 到 32 GPU 接近线性加速，64 GPU 后边际收益下降，反映固定问题规模下通信和每 GPU 工作量不足开始占主导。

## 超大规模模拟

论文报告：

| 材料 | 原子数 | GPU 数 | 速度 (ns/day) | 微秒/(atom·step) |
|---|---:|---:|---:|---:|
| Li$_3$PO$_4$ | 50,331,648 | 128 | 0.274 | 0.013 |
| Ag vacancy | 100,640,512 | 128 | 1.539 | 0.003 |

^[raw/papers/musaelian2023-allegro-source.md]

这证明严格局部等变势可以进入亿原子尺度；但它不是对长时间统计收敛、所有硬件平台或所有网络容量的普遍性能保证。

## 理论结果：与 ACE 的复杂度差异

论文展开 Allegro 和 ACE 的迭代张量积，指出二者共享局部角向多体核心。ACE 保留全部径向—化学基索引，其成本随基维和体阶增长；Allegro 通过每层可学习通道混合把特征压缩回固定宽度。^[raw/papers/musaelian2023-allegro-source.md]

作者将 Allegro 相对 ACE 的性能优势部分归因于：后层环境权重依赖前层完整标量潜表示，使高阶交互可根据低阶环境自适应加权。论文将这一解释标为假设，而非已严格证明的因果结论。

## 结果解读边界

- “一亿原子可运行”不等于“大模型也能同样扩展”；
- 严格局部基准未覆盖显式长程静电项；
- QM9、分子动力学和扩展实验采用不同模型容量；
- 对 3BPA，NequIP 略优于 Allegro，不能只摘录 Allegro 的优势；
- 强扩展随 GPU 数增加出现饱和，需结合每 GPU 原子数判断效率。

## 关联页面

- [[musaelian2023-allegro-analysis]]
- [[musaelian2023-allegro-method]]
- [[musaelian2023-allegro-critical]]
- [[allegro]]
- [[nequip]]
- [[sevennet]]

## Evidence By Source

### `sources/papers/musaelian2023-allegro.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/musaelian2023-allegro-source.md`

^[sources/papers/musaelian2023-allegro.md]
