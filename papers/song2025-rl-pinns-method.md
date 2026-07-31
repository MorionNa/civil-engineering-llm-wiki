---
id: papers--song2025-rl-pinns-method
title: RL-PINNs 方法机制
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- domain/llm
- evidence/paper
- method/pinn
- method/reinforcement-learning
keywords:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- domain/llm
- evidence/paper
- method/pinn
- method/reinforcement-learning
sources:
- sources/papers/song2025-rl-pinns.md
created: '2026-07-31'
updated: '2026-07-31'
confidence: medium
---

# RL-PINNs 方法机制

## Three-Stage Workflow

```text
初始随机配点
  ↓
预训练 PINN，得到暂态 uθ
  ↓
DQN agent 在坐标域内移动
  ↓
收集高函数变化位置
  ↓
一次性加入最终训练集
  ↓
最终 PINN 训练
```

“单轮”指采样与最终训练之间不进行多轮 PINN 重训；DQN 内部仍包含多个 episode 和状态转移。

## MDP Definition

- **State:** 当前空间/时空坐标 $x^{(t)}$；
- **Action:** 沿某一维度移动 $\pm\Delta x_i$，动作数约为 $2d$；
- **Transition:** $x^{(t+1)}=x^{(t)}+a^{(t)}$，并按定义处理边界；
- **Observation:** 预训练 PINN 在当前位置及相邻位置的前向输出；
- **Policy:** Deep Q-Network。

## Function-Variation Reward

定义相邻位置的网络输出变化 $\delta u^{(t)}$。若其超过阈值 $\varepsilon$，奖励为变化量，否则为零：

$$
r_t=\begin{cases}
\delta u^{(t)},&\delta u^{(t)}>\varepsilon,\\
0,&\text{otherwise}.
\end{cases}
$$

该 reward 不需要计算 PDE 高阶导数，因此候选探索仅需 PINN 前向推理。

## DQN Components

- online Q-network 与 target network；
- replay buffer 打破序列相关；
- Bellman MSE；
- 折扣因子 $\gamma=0.95$；
- 周期 target 同步；
- 衰减探索率；
- episode 终止与采样覆盖准则。

## Sampling Termination

论文用连续 episode 中“高变化点占比达到阈值”的条件停止探索，并从轨迹中选择新增配点。不同案例使用不同动作步长、阈值和新增点数。

## Training Details

PINN 使用多层 MLP；大多数任务用 Adam，Burgers 还使用 L-BFGS。基线包括 uniform、RAR 和 RAD。比较中需要把预训练、DQN 训练、采样和最终 PINN 训练全部计入 wall-clock。

## Assumptions

- 预训练 $u_\theta$ 已显现真实困难区域；
- 高函数变化与高训练价值相关；
- 规则域允许坐标轴局部动作；
- 局部轨迹能覆盖多峰或高维关键区域。

## Structural-Dynamics Migration Inference

state 可扩展为“时间、楼层/构件、模态、当前覆盖密度”，reward 可结合位移/速度/恢复力变化、低成本平衡代理和不确定度。对路径依赖本构，必须加入历史状态，不能只使用当前坐标。

## Related Pages

- [[song2025-rl-pinns-analysis]]
- [[song2025-rl-pinns-results]]
- [[song2025-rl-pinns-critical]]
- [[rl-pinns]]

## Evidence By Source

### `sources/papers/song2025-rl-pinns.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2504.12949v1.pdf`

^[sources/papers/song2025-rl-pinns.md]
