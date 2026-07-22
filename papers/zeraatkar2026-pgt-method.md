---
title: "PGT 方法：Physics-Aware Attention Mechanism"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [physics-informed, transformer, pinn, attention, ai4s]
---

# PGT 方法机制

## 1. 从 PINN 到 Physics-Aware Transformer

传统 PINN 通常优化：

$$L=L_{data}+\lambda L_{physics}$$

物理只作为训练约束。PGT 的核心变化是：将物理规律引入 Transformer 的信息交互过程。

## 2. Physics-Aware Attention

标准 attention：

$$A=softmax(QK^T/\sqrt d)V$$

PGT 在 attention logits 中加入物理偏置：

$$A=softmax((QK^T+B_p)/\sqrt d)V$$

其中 $B_p$ 描述物理空间中点之间的关联强度。

## 3. 物理偏置的意义

对于 PDE 问题，距离并不是唯一关系，真正决定信息传播的是：

- 扩散距离；
- 时间因果；
- 物理传播速度；
- PDE Green function。

因此 attention 不再自由寻找相关性，而是在物理允许范围内学习。

## 4. 对结构动力学的启发

如果用于结构响应：

节点可以表示楼层或构件；

attention bias 可以设计为：

$$B_p=f(M,K,C,\Delta t)$$

例如：

- 模态相关性；
- 刚度耦合；
- 波传播距离；
- 因果时间距离。

这与 SeisGPT 的 SDG-Mixer 思想存在相似性：都是将物理传播规律嵌入网络传播机制，而不是仅作为 loss。

## 关联页面

- `[[zeraatkar2026-pgt-analysis]]`
- `[[zeraatkar2026-pgt-results]]`
- `[[zeraatkar2026-pgt-critical]]`
