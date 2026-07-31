---
id: paper-batzner2022-nequip-results
title: "Batzner et al. (2022) — NequIP 结果证据"
type: paper-analysis
status: verified
project: civil-engineering-llm-wiki
tags: [neural-network, deep-learning, physics-simulation, scientific-machine-learning, ai4s, material-design, se3-equivariance]
sources: [raw/papers/batzner2022-nequip-source.md]
created: 2026-07-31
updated: 2026-07-31
confidence: high
results: [md17-accuracy, water-ice-data-efficiency, glass-transfer, lithium-diffusivity, learning-curve-slope]
datasets: [original-md17, revised-md17, water-and-ice, formate-on-cu, li4p2o7, lips]
reproducibility: high
---

# NequIP 结果证据

## 评价范围

论文不是只在一个小分子基准上比较误差，而是覆盖：

- 原始 MD-17 与 revised MD-17；
- 高阶量子化学 CCSD/CCSD(T) 小分子数据；
- 液态水与三种冰相；
- Cu(110) 表面甲酸根脱氢反应；
- Li$_4$P$_2$O$_7$ 非晶玻璃形成；
- Li$_{6.75}$P$_3$S$_{11}$ 超离子输运；
- 液态水的样本效率消融。

^[raw/papers/batzner2022-nequip-source.md]

## MD-17：少量训练构型下的精度

原始 MD-17 实验统一使用 1000 个训练与验证构型。论文报告 NequIP 在多数分子的能量和力 MAE 上优于 SchNet、DimeNet、sGDML、PaiNN、SpookyNet、GemNet、NewtonNet 和 UNiTE 等方法。^[raw/papers/batzner2022-nequip-source.md]

部分原始 MD-17 力 MAE（meV/Å）：

| 分子 | SchNet | DimeNet | PaiNN | NequIP $l=3$ |
|---|---:|---:|---:|---:|
| Aspirin | 58.5 | 21.6 | 14.7 | 8.0 |
| Ethanol | 16.9 | 10.0 | 9.7 | 3.1 |
| Naphthalene | 25.2 | 9.3 | 3.3 | 1.7 |
| Toluene | 24.7 | 9.4 | 4.1 | 2.0 |

^[raw/papers/batzner2022-nequip-source.md]

## revised MD-17：旋转阶数消融

论文比较 $l=0,1,2,3$。$l=0$ 对应只含标量的 invariant GNN；从 $l=0$ 增加到 $l=1$ 通常带来最大的误差下降，$l=2$、$l=3$ 进一步改善部分分子。^[raw/papers/batzner2022-nequip-source.md]

示例力 MAE（meV/Å）：

| 分子 | $l=0$ | $l=1$ | $l=2$ | $l=3$ |
|---|---:|---:|---:|---:|
| Aspirin | 42.2 | 12.6 | 8.5 | 8.2 |
| Azobenzene | 34.4 | 4.5 | 3.3 | 2.9 |
| Ethanol | 11.9 | 6.5 | 3.5 | 2.8 |
| Naphthalene | 20.6 | 2.1 | 1.4 | 1.3 |

该消融说明性能差异不能只归因于“换了一个更深网络”，而与内部张量表示和等变交互直接相关。^[raw/papers/batzner2022-nequip-source.md]

## 水与冰：1000 倍训练数据差异

DeepMD 基线使用 133,500 个水/冰构型；NequIP 只从同一数据来源抽取 133 个训练构型。尽管数据量约少 1000 倍，NequIP 在液态水和三种冰相的力 RMSE 上均优于文中 DeepMD 结果。^[raw/papers/batzner2022-nequip-source.md]

| 系统 | NequIP 最低力 RMSE (meV/Å) | DeepMD 力 RMSE (meV/Å) |
|---|---:|---:|
| Liquid water | 11.6 | 40.4 |
| Ice Ih (b) | 9.9 | 43.3 |
| Ice Ih (c) | 11.7 | 26.8 |
| Ice Ih (d) | 9.5 | 25.4 |

不同能量/力权重会改变误差平衡：增大能量权重可显著改善能量误差，但力误差会略升。因此“数据效率高”不意味着所有损失分量可以同时无代价最优。^[raw/papers/batzner2022-nequip-source.md]

## Cu 表面反应

在包含金属键、共价键和电荷转移的甲酸根/Cu(110) 体系中，模型使用 2500 个训练构型。论文报告平均元素加权力 MAE 为 38.4 meV/Å，能量 MAE 为 0.50 meV/atom，说明等变模型能够覆盖多元素、反应型表面体系。^[raw/papers/batzner2022-nequip-source.md]

## Li$_4$P$_2$O$_7$：跨温度与跨相态迁移

模型只在 3000 K 熔融轨迹的 1000 个构型上训练，但在 600 K 淬火玻璃轨迹上仍取得较低误差。随后开展十组 50 ps NequIP 分子动力学，径向分布和两类角分布与 AIMD 基本一致。^[raw/papers/batzner2022-nequip-source.md]

| 测试集 | 能量 MAE (meV/atom) | 力 MAE (meV/Å) |
|---|---:|---:|
| Melt | 0.4 | 34.0 |
| Quench | 0.5 | 21.3 |

这一结果支持“训练数据之外的温度/结构状态仍可保持一定物理保真度”，但它只涉及同一材料体系内的迁移，不能等同于跨材料普适泛化。

## LiPS：扩散动力学

随训练集从 10 增加到 2500 个构型，LiPS 力 MAE 从 97.8 降到 4.7 meV/Å。使用 2500 构型训练的模型预测 Li 扩散率：

$$
D_{\mathrm{NequIP}}=1.25\times10^{-5}\ \mathrm{cm^2/s},
$$

而 AIMD 为：

$$
D_{\mathrm{AIMD}}=1.37\times10^{-5}\ \mathrm{cm^2/s}.
$$

相对差异约 9%。^[raw/papers/batzner2022-nequip-source.md]

## 学习曲线：不只是整体平移

液态水实验比较 $l=0,1,2,3$ 与训练集规模 10–1000。等变网络在所有规模上均优于 $l=0$，且从 $l=0$ 到 $l\ge1$ 后，误差—样本数的 log-log 学习曲线斜率发生变化。论文据此认为等变先验不仅降低常数项，还改变了随数据增长的学习速度。^[raw/papers/batzner2022-nequip-source.md]

更高旋转阶 $l>1$ 主要继续平移学习曲线，并未再次显著改变斜率。该结果提示：最关键的结构变化可能是从纯标量不变表示进入包含方向张量的等变表示，而不是无限提高张量阶数。

## 结果解读边界

- MD-17 的不同版本具有不同噪声水平，应优先比较 revised MD-17；
- 模型在不同数据集上采用不同超参数，跨任务表格不能视作统一固定配置的结果；
- 结构/动力学分布一致不代表所有热力学、反应或长程输运性质均已验证；
- 少样本优势依赖已知 E(3) 对称性与局部相互作用假设。

## 关联页面

- [[batzner2022-nequip-analysis]]
- [[batzner2022-nequip-method]]
- [[batzner2022-nequip-critical]]
- [[nequip]]
- [[allegro]]
- [[sevennet]]
