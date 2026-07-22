---
title: "NODE-ONet：物理编码神经 ODE 算子网络"
type: entity
created: 2026-07-23
updated: 2026-07-23
tags: [neural-operator, neural-ode, physics-encoded-network]
---

# NODE-ONet

## 定义

NODE-ONet（Deep Neural ODE Operator Network）是一种将 Neural ODE 嵌入 encoder-decoder 神经算子的物理编码算子学习框架，用于学习 PDE 参数到 PDE 解的映射。

## 核心思想

不是直接学习：

$$v\rightarrow u$$

而是学习：

$$v\rightarrow z(t)\rightarrow u$$

其中 latent dynamics 由物理编码 Neural ODE 描述。

## 与其他方法关系

- DeepONet：学习函数空间映射；
- PINN：通过 PDE residual 约束；
- PGT：物理约束 attention；
- SeisGPT：物理结构算子传播；
- NODE-ONet：连续时间 latent dynamics。

## 结构动力学启发

可用于构建连续时间结构响应算子：

$$\dot z=F_\theta(z,M,K,C,f_{NL})$$

将结构动力学参数编码到 latent evolution 中。
