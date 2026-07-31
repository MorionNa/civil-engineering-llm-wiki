---
title: "Batzner et al. (2022) — NequIP 方法机制"
created: 2026-07-31
updated: 2026-07-31
type: paper-analysis
tags: [neural-network, deep-learning, physics-simulation, scientific-machine-learning, ai4s, material-design]
sources: [raw/papers/batzner2022-nequip-source.md]
confidence: high
---

# NequIP 方法机制

## 1. 问题定义

给定原子种类 $\{Z_i\}$ 与原子坐标 $\{\mathbf r_i\}$，模型预测系统总势能与原子力：

$$
E_{\mathrm{pot}}=\sum_i E_{i,\mathrm{atomic}},
\qquad
\mathbf F_i=-\nabla_{\mathbf r_i}E_{\mathrm{pot}}.
$$

先预测势能再求导，使原子力天然满足能量一致性，而不是将每个力分量独立回归。

## 2. 局部原子图

以截断半径 $r_c$ 构建原子邻接图：

- 节点：原子种类和节点特征；
- 边：相对位移 $\mathbf r_{ij}=\mathbf r_j-\mathbf r_i$；
- 距离 $r_{ij}$ 进入径向网络；
- 方向 $\hat{\mathbf r}_{ij}$ 进入球谐函数。

截断邻域使单层计算随原子数近线性增长，但多层消息传递会扩大有效感受野。

## 3. O(3) 不可约表示

每个节点特征由多个 O(3) 不可约表示的直和组成：

$$
V^{(l,p)}_{acm},
$$

其中：

- $l=0$：标量；
- $l=1$：向量；
- $l\ge 2$：高阶张量；
- $p\in\{+1,-1\}$：反演奇偶性；
- $m=-l,\ldots,l$：表示分量；
- $c$：通道索引。

这种组织方式使网络内部特征在旋转、反射和坐标变换下按已知规则变化。

## 4. 等变卷积滤波器

卷积滤波器写成径向函数和球谐函数的乘积：

$$
S_m^{(l)}(\mathbf r_{ij})
=R(r_{ij})Y_m^{(l)}(\hat{\mathbf r}_{ij}).
$$

径向函数由 Bessel 距离基、平滑截断包络和 MLP 构成：

$$
R(r_{ij})=W_n\sigma(\cdots\sigma(W_1B(r_{ij}))).
$$

所有可学习权重位于旋转不变的径向部分，方向变化由球谐函数显式承担。

## 5. Clebsch–Gordan 张量积

输入特征与方向滤波器通过 Clebsch–Gordan 张量积组合：

$$
l_i\otimes l_f\rightarrow l_o,
\qquad
|l_i-l_f|\le l_o\le l_i+l_f.
$$

同时满足奇偶性选择规则：

$$
p_o=p_ip_f.
$$

模型设置最大旋转阶 $l_{\max}$，舍弃输出阶数超过该上限的张量积路径。若只保留 $0\otimes0\rightarrow0$，网络就退化为只处理标量的不变 GNN。

## 6. Interaction Block

每个交互块包含：

1. 原子级 self-interaction；
2. 等变卷积；
3. 相同 $(l,p)$ 输出路径的拼接与通道混合；
4. ResNet 式残差更新；
5. 保持等变性的门控非线性。

偶标量使用 SiLU，奇标量使用 tanh；高阶张量由标量门控，以避免普通逐元素激活破坏等变性。

## 7. 输出与训练损失

最终只读取 $l=0$ 标量特征，并输出每原子势能。训练使用能量和力的加权均方损失：

$$
\mathcal L
=\lambda_E\|\hat E-E\|_2^2
+\lambda_F\frac{1}{3N}
\sum_{i=1}^{N}\sum_{\alpha=1}^{3}
\left|-
\frac{\partial \hat E}{\partial r_{i,\alpha}}
-F_{i,\alpha}\right|^2.
$$

论文建议能量与力的默认相对权重考虑原子数平方，因为能量是全局量，而力是局部多分量量。

## 8. 计算图

```text
原子坐标/种类
      ↓
cutoff neighbor list
      ↓
scalar embedding
      ↓
[radial MLP × spherical harmonics]
      ↓
Clebsch–Gordan tensor product
      ↓
scalar/vector/higher-order features
      ↓
多层 interaction blocks
      ↓
每原子能量 → 总势能
      ↓
autodiff → 原子力
```

## 9. 与后续模型的关系

- [[allegro]] 保留等变张量积思想，但去除跨层 atom-centered message passing，以严格局部 pair 表示提高扩展性；
- [[sevennet]] 保留 NequIP 类消息传递，通过逐层正向特征通信和反向梯度通信实现空间分解；
- 对结构动力，可将局部坐标、位移、力和构件方向组织为等变特征，再与 MechConv 的矩阵边权和动力平衡残差组合。

## 关联页面

- [[batzner2022-nequip-analysis]]
- [[batzner2022-nequip-results]]
- [[batzner2022-nequip-critical]]
- [[nequip]]
- [[allegro]]
- [[sevennet]]
