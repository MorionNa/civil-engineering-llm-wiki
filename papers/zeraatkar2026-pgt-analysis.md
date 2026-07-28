---
title: "Physics-Guided Transformer (PGT)：面向 PINN 的物理感知注意力机制"
created: 2026-07-22
updated: 2026-07-22
type: paper-analysis
tags: [physics-informed, pinn, transformer, physics-aware-attention, scientific-machine-learning]
sources: [raw/papers/2603.27929v1.pdf]
confidence: high
---

# Physics-Guided Transformer (PGT)：面向 PINN 的物理感知注意力机制

## 1. 工程背景

物理信息神经网络（PINN）通过在损失函数中加入控制方程残差，使神经网络满足物理规律。然而，当观测数据稀疏、方程存在多尺度特征或优化问题复杂时，仅依靠 PDE residual 约束容易产生梯度不平衡、训练不稳定等问题。PGT 提出的核心思想是：**物理规律不应只作为损失函数中的外部约束，而应进入神经网络的信息传播过程。**

论文针对由偏微分方程控制的连续物理场重构问题开展研究，验证对象包括一维热扩散方程和二维不可压缩 Navier–Stokes 方程。fileciteturn103file0L6-L18

## 2. 科学问题

如何让 Transformer 的注意力机制具备物理传播规律，使模型在稀疏观测条件下仍能够：

- 保持 PDE 约束一致性；
- 避免纯数据驱动 attention 的非物理信息传播；
- 提升复杂动力系统重构能力。

## 3. 核心思想

传统 Transformer：

$$Attention(Q,K,V)=softmax(QK^T/\sqrt d)V$$

PGT 修改 attention：

$$Attention(Q,K,V)=softmax(QK^T/\sqrt d+\Gamma)V$$

其中，$\Gamma$ 为由 PDE Green 函数构造的物理偏置。

也就是说：

> 普通 Transformer 学习“哪些信息相关”；PGT 让物理规律提前决定“哪些信息可能传播”。

## 4. 方法机制

### 4.1 Physics-aware Attention

PGT定义：

$$\Gamma_{ij}=logG(x_i-x_j,t_i-t_j;\theta_p)$$

其中：

- $G$ 为控制方程对应的 Green 函数；
- $\theta_p$ 为物理参数。

对于未来时间或不存在物理传播关系的位置，设置：

$$\Gamma=-\infty$$

使其经过 softmax 后权重为 0。fileciteturn103file0L204-L213

### 4.2 热核物理偏置

对于扩散问题：

$$\Gamma_{ij}=-\frac{||x_i-x_j||^2}{4\alpha\Delta t}-\frac d2log(4\pi\alpha\Delta t)$$

该项编码：

- 空间局部性；
- 扩散尺度；
- 时间因果性。

论文指出，不同类型 PDE 可以替换不同 Green 函数，例如波动方程使用有限传播速度约束。fileciteturn103file0L214-L235

## 5. 网络结构

PGT包括：

1. 物理感知 Transformer encoder；
2. query-coordinate cross attention；
3. FiLM 调制 SIREN 隐式解码器。

输入的稀疏观测首先转换为 context tokens，然后通过 physics-guided attention 建立物理一致的潜在表示，再查询任意时空位置得到连续场。fileciteturn103file0L160-L165

## 6. 损失函数设计

PGT并非完全取消物理 loss，而是采用：

$$L=\frac{1}{2\sigma^2_{data}}L_{data}+\frac{1}{2\sigma^2_{PDE}}L_{PDE}+\frac{1}{2\sigma^2_{BC}}L_{BC}+\frac{1}{2\sigma^2_{IC}}L_{IC}$$

包括：

### 数据误差

$$L_{data}=||u_\theta-u^{obs}||^2$$

### PDE残差

$$L_{PDE}=||F(u_\theta)-f||^2$$

### 边界条件和初始条件

$$L_{BC},L_{IC}$$

不同于传统 PINN 手动设置权重，PGT通过可学习的不确定度参数自动调整各项权重。fileciteturn103file0L279-L281 fileciteturn103file0L336-L368

## 7. 实验结果

### 热扩散方程

100个观测点条件下：

- Relative L2 error = $5.9\times10^{-3}$；
- 相比 PINN 提升约38倍。fileciteturn103file0L21-L23

### Navier–Stokes

1500个散点观测：

- PDE residual = $8.3\times10^{-4}$；
- Relative L2 error = 0.034。fileciteturn103file0L24-L29

## 8. 消融分析

论文证明：

- 去掉 physics-guided attention，重构精度明显下降；
- 去掉 PDE loss，物理残差增加；
- 二者不是替代关系，而是互补关系。fileciteturn103file0L570-L584

## 9. 对结构动力学研究的启示

PGT提供了一种新的物理信息神经网络设计方向：

传统结构PINN：

$$L=L_{data}+\lambda L_{equilibrium}$$

PGT思想：

$$Attention=Attention(Q,K)+\Gamma_{physics}$$

对于结构动力响应，可构造：

$$\Gamma=f(M,K,C,\Phi,t)$$

使 attention 感知：

- 模态耦合；
- 楼层连接关系；
- 波传播路径；
- 阻尼衰减。

## 10. Negative Knowledge

- 当前验证主要针对 PDE 场重构，而非结构滞回动力学；
- Green函数需要已知物理传播规律；
- 未显式描述材料本构非线性；
- 对倒塌、接触、断裂等强非线性问题仍需进一步研究。

## 11. 可迁移知识

|机制|可迁移方向|
|-|-|
|Physics-aware attention|将结构动力学算子加入 Transformer 信息传播|
|Green函数偏置|构造符合物理传播规律的 attention kernel|
|物理架构+物理loss|结合显式约束和数据学习|
|不确定度权重|自动平衡多物理约束|

## 12. 与相关方法关系

|方法|物理进入位置|
|-|-|
|CM-PINNs|本构关系和物理方程约束|
|PGT|注意力传播机制|
|SeisGPT|结构算子和谱传播|

三者代表物理信息神经网络发展的不同方向。

## 关联页面

- [[pgt]]
- [[pinn]]
- [[cm-pinns]]
- [[seisgpt]]
