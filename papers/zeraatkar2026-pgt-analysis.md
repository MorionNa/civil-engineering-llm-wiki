---
title: "Zeraatkar et al. (2026) — Physics-Guided Transformer (PGT): Physics-Aware Attention Mechanism for PINNs"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [physics-informed, transformer, pinn, attention, diffusion-models, heat-equation, navier-stokes, uncertainty-quantification, ai4s]
sources: [arXiv:2603.27929]
confidence: medium
---

# Physics-Guided Transformer (PGT): Physics-Aware Attention Mechanism for PINNs

> **作者：** Ehsan Zeraatkar, Rodion Podorozhny, Jelena Tešić  
> **来源：** arXiv:2603.27929 (2026)  
> **一句话定位：** PGT 不再仅通过 PINN loss 强迫网络满足 PDE，而是将物理传播规律直接嵌入 Transformer attention，通过 physics-aware attention bias 引导信息交互。citeturn0academia12

## 1. 工程背景

PINN 通常采用：

$$L=L_{data}+\lambda L_{PDE}$$

通过 PDE residual 约束神经网络。然而在稀疏数据、复杂动力过程和多尺度问题中，PDE loss 容易出现梯度不平衡、优化不稳定以及数据拟合与物理一致性冲突。PGT 试图将物理知识从训练目标提升到网络表示层。citeturn0academia12

## 2. 核心思想

传统 Transformer：

$$Attention(Q,K,V)=softmax(QK^T/\sqrt d)V$$

PGT 修改 attention logits：

$$Attention=softmax((QK^T+B_{physics})/\sqrt d)V$$

其中 $B_{physics}$ 由物理传播核构造，使注意力权重具有 PDE 相关的空间和时间传播倾向。citeturn0academia12

## 3. 方法机制

→ `[[zeraatkar2026-pgt-method]]`

主要组成：

1. **Physics-aware attention**：在 attention score 中加入 heat-kernel-derived bias；
2. **Physics-conditioned context tokens**：查询坐标根据物理距离和传播规律选择上下文；
3. **FiLM-modulated sinusoidal implicit network**：通过 FiLM 调节隐式网络的频谱响应；
4. **PDE reconstruction**：用于稀疏观测下连续物理场恢复。

## 4. 实验结果

→ `[[zeraatkar2026-pgt-results]]`

测试：

- 一维 heat equation；
- 二维 incompressible Navier–Stokes cylinder wake。

结果：

- 稀疏 heat equation（100 observations）：relative L2 error = 5.9×10⁻³；
- Navier–Stokes：PDE residual = 8.3×10⁻⁴，relative error = 0.034。

相比仅优化 PDE residual 或数据误差的方法，PGT 能同时保持较低物理残差和较高重构精度。citeturn0academia12

## 5. 与传统 PINN 的区别

| | PINN | PGT |
|-|-|-|
|物理进入位置|loss|attention机制|
|主要约束|PDE residual|传播规则|
|优化困难|梯度权重平衡|减少物理-数据冲突|
|数据需求|通常较高|强调稀疏观测|

## 6. 对结构动力学 PINN 的启示

PGT 提供了一种区别于 CM-PINNs 和 SeisGPT 的路线：

- CM-PINNs：把本构关系加入约束；
- SeisGPT：把结构动力学算子加入表示传播；
- PGT：把物理传播规律加入 attention。

对于结构动力响应预测，可以考虑构造：

$$B_{physics}=f(M,K,C,\Delta t)$$

让 attention 根据结构模态传播、楼层耦合和因果时间关系自动调整，而不是完全依赖数据学习。

## 7. Negative Knowledge

→ `[[zeraatkar2026-pgt-critical]]`

- 当前验证集中于 PDE 场重构，而非结构动力学；
- physics bias 依赖已知传播规律，复杂非线性本构仍需额外建模；
- heat kernel 对扩散型过程天然适配，对结构滞回、冲击和倒塌问题需要重新设计；
- 目前不能证明 attention 中物理偏置可以替代显式动力学方程。

## 关联页面

- `[[pinn]]`
- `[[seisgpt]]`
- `[[cm-pinns]]`
- `[[zeraatkar2026-pgt-method]]`
- `[[zeraatkar2026-pgt-results]]`
