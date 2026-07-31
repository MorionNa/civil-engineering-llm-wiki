---
id: paper-batzner2022-nequip-method
title: Batzner et al. (2022) — NequIP 方法机制
type: paper-analysis
status: verified
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- evidence/paper
keywords:
- deep-learning
- material-design
- neural-network
- physics-simulation
- scientific-machine-learning
- se3-equivariance
sources:
- sources/papers/batzner2022-nequip.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: high
methods:
- e3-equivariance
- tensor-field-network
- spherical-harmonics
- radial-network
- clebsch-gordan-tensor-product
- energy-conserving-force-field
reproducibility: high
---

# NequIP 方法机制

## 输入、输出与物理约束

NequIP 的输入是原子种类 $Z_i$ 与三维坐标 $\mathbf r_i$。模型在 cutoff 邻接图上预测每个原子的标量势能 $E_i$，再汇总为系统总势能：

$$
E_{\mathrm{pot}}=\sum_i E_i.
$$

原子力由总势能对坐标的负梯度获得：

$$
\mathbf F_i=-\nabla_{\mathbf r_i}E_{\mathrm{pot}}.
$$

因此，平移和旋转后的力会按几何规则变换，同时力场与一个标量势能保持一致。^[raw/papers/batzner2022-nequip-source.md]

## 原子图与局部邻域

每个原子是图节点；距离小于 cutoff $r_c$ 的原子对形成边。卷积仅在局部邻域内进行，因此单层计算量随原子数近似线性增长。周期体系通过邻居列表处理周期镜像。^[raw/papers/batzner2022-nequip-source.md]

多层消息传递会扩大最终节点表示的有效感受野：即使每层只访问 $r_c$ 邻域，经过多层后信息仍可跨越多跳邻域。该性质提高表达能力，但也是分布式扩展时的通信来源。

## O(3) 不可约表示

每个节点的隐藏特征不是普通标量向量，而是不同 O(3) 不可约表示的直和：

- $l=0$：标量；
- $l=1$：向量；
- $l\ge 2$：更高阶几何张量；
- $p\in\{+1,-1\}$：反演下的奇偶性。

同一 $l$ 下有 $2l+1$ 个表示分量。网络参数对这些表示分量共享，以保证旋转后输出严格按对应表示矩阵变换。^[raw/papers/batzner2022-nequip-source.md]

## 等变卷积滤波器

边方向滤波器由径向函数和球谐函数相乘得到：

$$
S_m^{(l)}(\mathbf r_{ij})
=R(r_{ij})Y_m^{(l)}(\hat{\mathbf r}_{ij}).
$$

其中：

- $R(r_{ij})$ 是旋转不变的可学习径向网络；
- $Y_m^{(l)}(\hat{\mathbf r}_{ij})$ 表示边方向；
- 距离先经 Bessel 基和光滑多项式 envelope 编码；
- envelope 在 cutoff 处平滑衰减，降低邻居进出截断范围时的不连续性。

^[raw/papers/batzner2022-nequip-source.md]

## Clebsch–Gordan 张量积

输入特征与边滤波器通过 Clebsch–Gordan 系数进行等变张量积。若输入阶数为 $l_i$、滤波器阶数为 $l_f$，输出允许的阶数满足：

$$
|l_i-l_f|\le l_o\le l_i+l_f.
$$

奇偶性满足：

$$
p_o=p_i p_f.
$$

网络只保留不超过超参数 $l_{\max}$ 的输出表示，并将产生相同 $(l_o,p_o)$ 的路径拼接、线性混合。^[raw/papers/batzner2022-nequip-source.md]

## Interaction block

一个 interaction block 主要包括：

```text
邻居张量特征
      ↓
等变卷积：径向权重 × 球谐 × 张量积
      ↓
按输出 irrep 拼接与线性混合
      ↓
等变 gate 非线性
      ↓
ResNet-style 残差更新
```

偶标量使用 SiLU，奇标量使用 tanh；非标量通道由门控标量调制。残差支路使用按元素种类区分的自交互权重。^[raw/papers/batzner2022-nequip-source.md]

## Output block

最终 interaction block 的偶标量特征被两层 atom-wise self-interaction 映射为每原子单一标量能量。原子能求和后，通过自动微分计算全部力分量。

## 损失函数

训练目标是能量误差与力误差的加权和：

$$
\mathcal L
=\lambda_E|\hat E-E|_2^2
+\lambda_F\frac{1}{3N}
\sum_{i=1}^{N}\sum_{\alpha=1}^{3}
\left|-
\frac{\partial \hat E}{\partial r_{i,\alpha}}-F_{i,\alpha}\right|^2.
$$

论文针对不同体系调整 $\lambda_E$、$\lambda_F$、cutoff、特征数和 $l_{\max}$。对固定规模体系，目标能量减去训练集均值，能量和力按训练集力分量 RMS 缩放；对水/冰混合规模体系采用按原子能量初始化的尺度与偏置。^[raw/papers/batzner2022-nequip-source.md]

## 训练设置

- 小分子通常使用 5 个 interaction blocks、batch size 5；
- 周期体系通常使用 6 个 interaction blocks、batch size 1；
- 优化器为 Adam AMSGrad；
- 按验证集力损失执行学习率衰减；
- 用指数移动平均权重评估验证集和最终模型；
- 训练使用 float32 和单张 NVIDIA V100。

^[raw/papers/batzner2022-nequip-source.md]

## 方法边界

- E(3) 等变性约束坐标变换，但不等同于长程物理或材料本构正确；
- cutoff 和层数共同决定可访问的空间范围；
- 势能求导保证保守力，但训练和推理时需要额外梯度计算；
- $l_{\max}$、通道数和张量积路径增加时，显存与计算成本显著上升。

## 关联页面

- [[batzner2022-nequip-analysis]]
- [[batzner2022-nequip-results]]
- [[batzner2022-nequip-critical]]
- [[nequip]]
- [[allegro]]
- [[sevennet]]

## Evidence By Source

### `sources/papers/batzner2022-nequip.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/batzner2022-nequip-source.md`

^[sources/papers/batzner2022-nequip.md]
