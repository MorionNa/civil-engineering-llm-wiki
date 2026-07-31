---
title: "Batzner et al. (2022) — NequIP 实验结果"
created: 2026-07-31
updated: 2026-07-31
type: paper-analysis
tags: [neural-network, deep-learning, physics-simulation, scientific-machine-learning, ai4s, material-design]
sources: [raw/papers/batzner2022-nequip-source.md]
confidence: high
---

# NequIP 实验结果

## 1. 实验覆盖

论文使用多类体系验证 NequIP：

- 原始 MD-17 与 revised MD-17 小分子；
- CCSD/CCSD(T) 高精度量化化学标签；
- 液态水与三种冰相；
- Cu(110) 表面的甲酸根脱氢反应；
- 非晶 Li$_4$P$_2$O$_7$；
- 超离子导体 Li$_{6.75}$P$_3$S$_{11}$；
- 液态水样本效率消融。

## 2. MD-17 与 revised MD-17

在每个分子仅使用 950 个训练构型和 50 个验证构型的条件下，NequIP 与 SchNet、DimeNet、sGDML、PaiNN、SpookyNet、GemNet、NewtonNet、UNiTE、ACE 等方法比较。

### 代表性 revised MD-17 结果

| 分子 | 指标 | NequIP $l=0$ | $l=1$ | $l=2$ | $l=3$ |
|---|---:|---:|---:|---:|---:|
| Aspirin | Energy MAE (meV) | 25.2 | 3.8 | 2.4 | 2.3 |
| Aspirin | Force MAE (meV/Å) | 42.2 | 12.6 | 8.5 | 8.2 |
| Benzene | Energy MAE (meV) | 3.2 | 0.09 | 0.06 | 0.04 |
| Benzene | Force MAE (meV/Å) | 10.3 | 0.4 | 0.4 | 0.3 |
| Naphthalene | Energy MAE (meV) | 14.7 | 0.4 | 0.3 | 0.2 |
| Naphthalene | Force MAE (meV/Å) | 20.6 | 2.1 | 1.4 | 1.3 |

最显著的变化发生在 $l=0\rightarrow1$：加入向量等变特征后，误差大幅下降。提高到 $l=2$ 或 $l=3$ 通常继续改善，但边际收益变小。

论文还指出，原始 MD-17 的能量标签噪声更高，因此跨方法比较应优先采用 revised MD-17。

## 3. Water / Ice：1000 倍数据差异

NequIP 在液态水与三种冰相的联合任务中只使用 133 个训练结构，而对照 DeepMD 使用 133,500 个结构。

### 力 RMSE（meV/Å）

| 系统 | NequIP force-only | NequIP joint setting c | DeepMD |
|---|---:|---:|---:|
| Liquid water | 11.9 | 11.6 | 40.4 |
| Ice Ih (b) | 10.2 | 9.9 | 43.3 |
| Ice Ih (c) | 12.0 | 11.7 | 26.8 |
| Ice Ih (d) | 9.8 | 9.5 | 25.4 |

尽管训练数据仅约为 DeepMD 的 0.1%，NequIP 在四个子系统的力误差上都更低。能量与力权重的选择存在明显折中：提高能量权重可降低能量误差，但会略微提高力误差。

## 4. Formate / Cu(110) 反应体系

该数据集同时包含金属键、共价键、表面吸附与电荷转移。NequIP 使用 2500 个训练结构，报告：

- C 力 MAE：19.9 meV/Å；
- O 力 MAE：71.3 meV/Å；
- H 力 MAE：13.0 meV/Å；
- Cu 力 MAE：47.6 meV/Å；
- 四元素等权平均力 MAE：38.4 meV/Å；
- 能量 MAE：0.50 meV/atom。

该结果说明统一等变架构能够处理成分和键合机制高度异质的反应体系，但论文没有进一步报告反应速率或势垒动力学验证。

## 5. Li$_4$P$_2$O$_7$ 非晶玻璃

模型仅使用高温熔融轨迹中的 1000 个结构训练，却在未见过的 600 K 淬火玻璃轨迹上测试。

| 数据 | Energy MAE (meV/atom) | Force MAE (meV/Å) |
|---|---:|---:|
| Melt test | 0.4 | 34.0 |
| Quench OOD | 0.5 | 21.3 |

NequIP 驱动的 10 组 50 ps 分子动力学能较好复现 AIMD 的：

- 径向分布函数；
- P–O–O 四面体角分布；
- O–P–P 桥联角分布。

这说明低点误差之外，模型还在结构统计量和未见相态上表现出较强泛化。

## 6. LiPS 超离子传输

训练集从 10、100、1000 增加到 2500 个结构时，误差持续下降：

| 训练规模 | Energy MAE (meV/atom) | Force MAE (meV/Å) |
|---:|---:|---:|
| 10 | 2.03 | 97.8 |
| 100 | 0.44 | 25.8 |
| 1000 | 0.12 | 7.7 |
| 2500 | 0.08 | 4.7 |

使用 2500 个结构训练的模型预测 Li 扩散率为：

$$
D_{\mathrm{NequIP}}=1.25\times10^{-5}\ \mathrm{cm^2/s},
$$

AIMD 为：

$$
D_{\mathrm{AIMD}}=1.37\times10^{-5}\ \mathrm{cm^2/s},
$$

相对误差约 9%。

## 7. 等变性与学习曲线

论文在液态水上比较 $l=0,1,2,3$，并将训练集规模从 10 增加到 1000。

关键现象：

1. 所有等变模型均显著优于纯标量 $l=0$ 网络；
2. $l=0\rightarrow1$ 不仅下移误差曲线，还改变了 log-log 学习曲线斜率；
3. $l>1$ 主要继续下移曲线，未进一步显著改变斜率；
4. 控制参数量或特征数量后，该趋势仍存在。

因此论文把高数据效率归因于等变表示本身，而不只是更大的网络。

## 8. 结果边界

- 各任务使用不同超参数，结果不能直接解释为统一配置下的全面胜出；
- 论文主要验证精度与样本效率，没有提供大规模多 GPU 推理基准；
- 力误差较低不自动保证所有稀有事件、反应势垒或长程输运均准确；
- 一些体系只验证结构统计量或短时动力学，不能视为任意长时间稳定性的证明。

## 关联页面

- [[batzner2022-nequip-analysis]]
- [[batzner2022-nequip-method]]
- [[batzner2022-nequip-critical]]
- [[nequip]]
- [[allegro]]
- [[sevennet]]
