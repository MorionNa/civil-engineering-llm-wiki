---
id: papers--li2026-sgno-method
title: SGNO 方法机制
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/graph-neural-network
keywords:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/graph-neural-network
sources:
- sources/papers/li2026-sgno.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# SGNO 方法机制

## Problem Formulation

SGNO 学习周期域演化 PDE 的单步算子 $w_n\mapsto w_{n+1}$，训练阶段采用 one-step teacher forcing，推理阶段闭环迭代自身预测。其目标是控制重复传播时的谱幅值和相位漂移。

## Overall Architecture

```text
当前状态 w_n + 空间坐标
        ↓
Lift 到 latent field
        ↓
多层 SGNO block
  ├─ spectral carry path
  └─ learned correction path
        ↓
Projection
        ↓
下一步状态 w_{n+1}
```

## Spectral Carry Path

对 latent field 的 Fourier 系数，SGNO 使用受约束生成元传播：

$$
\widehat v_{n+1}^{carry}(k)=\exp(\Delta t\,\lambda_k)\widehat v_n(k),
\qquad \operatorname{Re}(\lambda_k)\le 0.
$$

非正实部限制重复传播中的无控制增益，适合扩散、耗散和受控色散过程。参数可随模态学习，但稳定约束作用于 carry 主干。

## Learned Correction Path

非线性、相位、闭合误差和未建模耦合由学习修正项负责。单层可以概括为：

$$
v^{\ell+1}=\mathcal C_{\Lambda_\ell}(v^\ell)+\mathcal N_{\theta_\ell}(v^\ell,x),
$$

其中 $\mathcal C$ 是谱 carry，$\mathcal N$ 是局部/谱混合的可学习修正。该结构受 exponential time differencing 的“线性传播 + 非线性强迫”启发，但不是对特定 ETD 格式的逐项复制。

## Layer Composition

每层同时包含局部路径和截断 Fourier 路径。局部路径处理点态混合，谱路径处理长程模态传播；多层参数可以 untied。输入和坐标经过 lifting，最终 projection 恢复物理通道。

## Training

训练损失是一步均方误差：

$$
\mathcal L=\mathbb E|f_\theta(w_n)-w_{n+1}|_2^2.
$$

模型不依赖长 rollout 反向传播，因此训练成本接近普通单步神经算子。长时稳定性主要来自更新结构与参数约束，而不是 rollout loss。

## Spectral Diagnostics

除 state-space nRMSE 外，论文计算：

- spectral energy error；
- low-band energy error；
- phase error；
- rollout error growth。

这些指标用于区分幅值耗散/爆炸、位置相位偏移和非线性模态错误。

## Assumptions

- 周期边界和 Fourier 表示是核心前提；
- 线性/半线性主干应能由谱生成元近似；
- 截断模态数限制可表达频率范围；
- 非正 carry 不约束 correction 路径，因此整体模型并非无条件稳定。

## Structural-Dynamics Migration Inference

在模态空间可用

$$
q_{n+1}=\mathcal C_{\Lambda}(q_n)+\mathcal N_\theta(q_n,z_n,F_n)
$$

表示线性模态传播与非线性本构修正。对大结构，可将 carry 作用于局部/全局模态，correction 由 MechConv 与本构状态模块完成。该迁移需要处理非周期边界和非正交局部模态。

## Related Pages

- [[li2026-sgno-analysis]]
- [[li2026-sgno-results]]
- [[li2026-sgno-critical]]
- [[sgno]]

## Evidence By Source

### `sources/papers/li2026-sgno.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2602.18801v2.pdf`

^[sources/papers/li2026-sgno.md]
