---
title: "Physics-Guided Transformer (PGT)"
created: 2026-07-16
updated: 2026-07-16
type: entity
tags: [physics-informed, transformer, pinn, attention, ai4s]
---

# Physics-Guided Transformer (PGT)

PGT 是一种将物理规律嵌入 Transformer attention 的 PINN 方法。

## 核心思想

区别于传统 PINN：

$$Loss=Data+Physics$$

PGT 修改 attention：

$$Attention=PhysicsAware(Q,K,V)$$

使网络的信息传播符合物理规律。

## 与其他方法关系

|方法|物理进入位置|
|-|-|
|PINN|loss|
|CM-PINNs|loss+本构|
|PGT|attention传播|
|SeisGPT|结构算子+传播模块|

## 结构动力学启发

PGT 可用于设计：

- 质量刚度 attention；
- 模态 attention；
- 因果时间 attention；
- 构件拓扑 attention。

## 关联

- `[[pinn]]`
- `[[seisgpt]]`
- `[[cm-pinns]]`
