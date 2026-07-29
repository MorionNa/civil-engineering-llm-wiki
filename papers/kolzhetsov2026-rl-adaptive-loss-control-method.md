---
title: "Kolzhetsov et al. (2026) — RL Adaptive Loss Control 方法"
created: 2026-07-29
updated: 2026-07-29
type: paper-analysis
tags: [physics-informed, pinn, reinforcement-learning, adaptive-weighting]
sources: [raw/papers/kolzhetsov2026-accelerating-pinn-training-extracted.txt]
confidence: high
---

# Method

## RL 环境定义

作者将 PINN 训练过程视为环境交互：agent 在每个训练阶段选择损失权重调整动作，以最大化长期训练收益。

状态：

$$s_t=(\lambda_{PDE},\lambda_{IC},\lambda_{BC})$$

动作：

$$s_{t+1}=s_t+a_t$$

即对三个损失权重施加连续扰动。

## Reward

奖励由两个部分组成：

1. 与固定权重 baseline 相比的归一化训练收益；
2. temporal shaping，用于估计当前 RL 训练相对 baseline 提前的 epoch 数。

最终：

$$R(t)=N(t)+S(t)$$

## Agent

论文比较三类方案：

- 离散状态/动作 + DQN；
- 连续控制单 agent DDPG；
- 多 agent DDPG，每个 agent 负责固定训练区间。

最终采用多 agent DDPG，通过时间窗口隐式编码训练阶段。

## 与结构动力 PINN 的关联

该方法可扩展到：

- 平衡方程损失；
- 本构关系损失；
- 初始条件损失；
- 数据监督损失；
- 能量一致性损失。

但需要扩展状态，否则仅靠权重无法反映非线性结构当前屈服、卸载和损伤状态。

## 关联

- [[kolzhetsov2026-rl-adaptive-loss-control-analysis]]
- [[adaptive-loss-weighting-pinn]]
- [[rathore2024-pinn-loss-landscape-analysis]]
