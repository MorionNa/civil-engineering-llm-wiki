---
title: "Song (2025) — RL-PINNs：强化学习驱动的单轮自适应配点"
created: 2026-07-29
updated: 2026-07-29
type: paper-analysis
tags: [physics-informed, pinn, reinforcement-learning, deep-q-network, adaptive-sampling, collocation-strategy, gradient-free-reward, delayed-reward, high-dimensional-pde, high-order-pde, scientific-machine-learning, ai4s]
sources: [raw/papers/2504.12949v1.pdf]
methods: [markov-decision-process, deep-q-network, function-variation-reward, semi-sparse-reward, single-round-adaptive-sampling]
results: [single-round-sampling, localized-feature-resolution, high-dimensional-poisson, biharmonic-equation, negligible-sampling-overhead]
failure_modes: [pretrained-solution-bias, function-variation-residual-mismatch, local-action-space, hyperparameter-sensitivity, no-code-release]
datasets: [single-peak-poisson, dual-peak-poisson, burgers-equation, wave-equation, ten-dimensional-poisson, biharmonic-equation]
reproducibility: medium
confidence: high
---

# RL-PINNs: Reinforcement Learning-Driven Adaptive Sampling for Efficient Training of PINNs

> **作者：** Zhenao Song  
> **单位：** Southeast University, School of Mathematics  
> **状态：** arXiv:2504.12949v1，2025-04-17  
> **一句话定位：** RL-PINNs 将 PINN 配点选择建模为 DQN 控制的序列决策问题，以相邻位置的网络函数变化量替代 PDE 残差作为无导数奖励，在一次独立采样阶段中寻找高变化区域，再用选出的配点完成最终 PINN 训练。

## 1. 工程背景 (Engineering Background)

PINN 的精度高度依赖 collocation points。均匀随机采样容易在光滑区域浪费配点，并遗漏尖峰、激波、传播前沿和多尺度区域。RAR、RAD 等残差自适应方法能把点移动到高残差区域，但通常需要“训练—评估候选点残差—增点—重训”的多轮循环；高维或高阶 PDE 中，候选池上的自动微分会带来较高计算成本。

## 2. Research Gap

论文将现有残差驱动自适应采样的不足概括为：

1. **多轮重训：** RAR/RAD 常执行 3–5 个采样轮次，每轮都要继续训练 PINN；
2. **候选池残差昂贵：** 每个候选点都需要计算 PDE 导数，高维和高阶算子尤其昂贵；
3. **短视选点：** 按当前残差贪心取点，可能重复覆盖局部区域，而不考虑后续整体覆盖与训练稳定性。

## 3. 科学问题 (Scientific Question)

能否把配点选择转化为一个序列决策问题，使 agent 不依赖 PDE 高阶导数，仅通过当前 PINN 近似解的局部变化识别复杂区域，并在一次采样阶段中获得可供最终训练使用的配点集合？

## 4. 研究目标 (Research Objective)

作者希望构建一个：

- 不需要多轮 PINN 重训的 adaptive sampling 流程；
- 不需要在候选池计算 PDE residual 的 reward；
- 能利用折扣回报而不是只看单点即时收益；
- 可覆盖低正则、非线性、高维和高阶 PDE 的统一框架。

需要特别区分：**本文的强化学习用于选择 collocation points，而不是在 PINN 优化停滞后直接用 RL 更新网络权重。**

## 5. 方法机制 (Method & Mechanism)

→ 详见 [[song2025-rl-pinns-method]]

RL-PINNs 分为三个阶段：

```text
初始随机配点
  → 预训练 PINN，得到暂态近似 uθ
  → DQN 在解空间中移动并收集高函数变化点
  → 将这些点一次性加入训练集
  → 最终训练 PINN
```

MDP 的核心定义：

- state：当前坐标 $x^{(t)}$；
- action：沿某一坐标轴移动 $\pm\Delta x_i$；
- transition：$x^{(t+1)}=x^{(t)}+a^{(t)}$；
- reward：若相邻状态的函数变化 $\delta u^{(t)}$ 超过阈值 $\varepsilon$，则奖励为 $\delta u^{(t)}$，否则为 0；
- policy：DQN + target network + replay buffer + 衰减探索率；
- termination：连续 5 个 episode 中，高变化点比例均达到 50%。

## 6. 结果证据 (Result & Evidence)

→ 详见 [[song2025-rl-pinns-results]]

六个 benchmark 中，RL-PINNs 的 relative $L_2$ error 均低于 UNIFORM、RAR 和 RAD：

| 案例 | RL-PINNs | 最佳对照 | 相对最佳对照改善 |
|---|---:|---:|---:|
| Single-Peak Poisson | 0.1462 | RAR 0.2871 | 49.1% |
| Dual-Peak Poisson | 0.1878 | RAR 0.3659 | 48.7% |
| Burgers | 0.0534 | RAR 0.1323 | 59.6% |
| Wave | 0.0053 | RAR 0.0339 | 84.4% |
| 10D Poisson | 0.0394 | RAR 0.0956 | 58.8% |
| Biharmonic | 0.0851 | RAR 0.1611 | 47.2% |

采样时间在 3.32–35.45 s 之间；与约 588–3591 s 的 PINN 训练时间相比，作者报告其占比很低。采样图显示 agent 倾向于集中于高斯峰、Burgers 激波、波前、10D 原点邻域和双调和方程高曲率区域。

## 7. 贡献 (Contribution)

1. 将 PINN adaptive sampling 明确表述为 MDP，并以 DQN 学习局部移动策略；
2. 提出函数变化量 reward，避免候选池上的 PDE residual 自动微分；
3. 使用阈值化 semi-sparse reward 与折扣回报，尝试降低冗余选点；
4. 将多轮 RAR/RAD 流程改为“预训练—一次采样阶段—最终训练”；
5. 在低正则、非线性、高维和高阶六类合成 PDE 上进行统一测试。

## 8. 核心知识点 (Core Knowledge)

- **配点问题可以视为主动探索。** agent 不必在固定大候选池中逐点打分，而可沿状态空间移动。
- **代理指标不一定需要 PDE residual。** 函数变化量只需前向推理，适合导数昂贵的高阶 PDE。
- **一次采样不等于一次决策。** RL-PINNs 仍运行多个 episode 和多个局部移动，只是不在采样阶段之间反复重训 PINN。
- **采样策略依赖预训练解。** agent 看到的是 $u_\theta$ 的变化，而不是未知真解的变化。
- **RL 在本文中优化“在哪里训练”，而不是“怎样更新参数”。**

## 9. Negative Knowledge

→ 详见 [[song2025-rl-pinns-critical]]

- function variation 与 PDE residual 不等价；局部平坦但方程不满足的区域可能得不到高奖励；
- agent 依赖预训练 PINN，若初始网络完全漏掉某个特征，采样策略可能无法发现它；
- state 仅包含当前坐标，没有显式表示已选点集合、覆盖度、PINN 不确定度或训练状态；
- 论文所称 delayed reward 主要表现为阈值化即时奖励加折扣回报，并非显式终局奖励；
- 没有 reward、阈值、action step、discount factor 和终止准则的系统消融；
- 只测试规则矩形域和已知解析解，没有复杂几何、逆问题、噪声数据或真实工程 PDE；
- 未提供代码仓库，复现仍需根据算法和超参数自行实现。

## 10. 可迁移知识 (Transferable Knowledge)

| 机制 | 向结构动力/PINN 迁移 |
|---|---|
| function variation reward | 用位移、速度、恢复力或内变量变化寻找高非线性时空区域 |
| local action | 在时间—楼层—模态—构件坐标中逐步探索困难区域 |
| semi-sparse reward | 过滤响应近似不变的冗余时刻和自由度 |
| one sampling stage | 在正式长时训练前固定一批高价值物理配点，降低反复求高阶残差成本 |
| replay buffer | 保存不同地震动/结构参数下的高价值采样轨迹 |

## 11. 研究机会 (Research Opportunity)

1. 将 reward 从单一 $|\Delta u_\theta|$ 扩展为响应变化、方程残差低成本代理、能量不平衡和不确定度的多目标组合；
2. 对连续高维空间采用 actor–critic、SAC 或基于 proposal distribution 的策略，避免 $2d$ 离散动作和局部随机游走；
3. 将 state 扩展为“坐标 + 已覆盖密度 + 模态/构件属性 + 当前 PINN 训练阶段”；
4. 交替执行少量 PINN 更新和 policy 更新，缓解固定预训练解带来的 bootstrap bias；
5. 对结构地震响应，重点采样屈服启动、刚度退化、卸载反向、峰值响应和能量突变区域；
6. 与 causal sampling、RAR/RAD、importance sampling 和 curriculum time marching 做等 wall-clock 对比；
7. 区分“RL 选点后继续梯度训练”和“RL 直接后训练网络权重”，后者需要完全不同的状态、动作与奖励设计。

## 12. 可复现性 (Reproducibility)

| 项目 | 评价 |
|---|---|
| 等级 | 🟡 中等 |
| 网络 | PINN 7 层 `[64,128,256,512,256,128,64]`，DQN 两层 `[128,64]` |
| 优化 | Adam；Burgers 额外使用 L-BFGS；给出主要学习率和训练步数 |
| RL | $\gamma=0.95$，target 每 5 episode 同步，探索概率 $0.5/n$，阈值和动作步长逐案例给出 |
| 数据/案例 | 六个 PDE、解析解、初始配点与新增点数量均给出 |
| 硬件 | 论文报告 NVIDIA RTX 4090、PyTorch 2.4.0 |
| 缺口 | 无公开代码；随机种子、重复实验方差、部分实现边界处理细节未充分说明 |

## 关联页面

- [[rl-pinns]]
- [[gao2025-adaptive-loss-pinn-analysis]]
- [[wang2024-causal-pinn-analysis]]
- [[wang2021-pinn-ntk-failure-analysis]]
- [[luo2025-pinn-pde-review-analysis]]
- [[optimizer-for-ai4s-and-physics-models]]
