---
title: "Guo & Xu (2026) Phy-RLK 方法：Newmark-β 残差门控与 KAN 解码"
created: 2026-07-16
updated: 2026-07-16
type: paper-analysis
tags: [physics-informed, neural-network, lstm, sequence-modeling, deep-learning, structural-dynamics, seismic-response, equation-of-motion, restoring-force]
sources: [raw/papers/10_1016_j_cma_2025_118422.xml]
methods: [physical-residual-lstm, newmark-beta-residual, embedded-physics, kan-decoder, bidirectional-mimo, minmax-normalization, adam, early-stopping]
results: [architecture-ablation, bidirectional-response-prediction]
failure_modes: [data-loss-only, restoring-force-interface-ambiguity, structure-specific-retraining]
datasets: [srm-bidirectional-ground-motions, opensees-six-story-rc-frame, opensees-five-story-rc-frame]
reproducibility: low
code_url: []
dataset_url: []
confidence: high
contested: false
contradictions: []
---

# 方法展开：Phy-RLK = 物理残差 LSTM + KAN

> 返回概述 → [[guo2026-phy-rlk-analysis]]；模型实体 → [[phy-rlk]]

## 5.1 输入—输出

输入为双向地震加速度序列 $[\ddot u_{gx}(t),\ddot u_{gy}(t)]$；输出为每层、两个方向的 $\hat u,\dot{\hat u},\ddot{\hat u}$。张量采用 `[batch, sequence length, input/output size]`，因此它是多输入—多输出的逐时刻监督代理。

```text
双向地震动 x/y
  → 3 层 physical-residual LSTM
  → x/y 时序隐特征
  → 各层各方向 KAN decoder
  → acceleration + velocity + displacement
```

## 5.2 动力平衡与 Newmark-β

$$M\ddot u+C\dot u+F_s(u,\dot u)=-M\Gamma\ddot u_g,$$

其中 $F_s$ 是非线性恢复力。作者把阻尼与恢复力合并为质量归一化恢复力 $F_{mrf}$，写成递归加速度平衡，再用 Newmark-β 更新：

$$\dot u_{n+1}=\dot u_n+[(1-\gamma)\ddot u_n+\gamma\ddot u_{n+1}]\Delta t,$$

$$u_{n+1}=u_n+\dot u_n\Delta t+[(1/2-\beta)\ddot u_n+\beta\ddot u_{n+1}](\Delta t)^2,$$

取 $\gamma=0.5,\beta=0.25$。为避免提取文本中的符号歧义，可将三类残差理解为：预测加速度偏离动力平衡解、预测速度偏离 Newmark 速度更新、预测位移偏离 Newmark 位移更新。

## 5.3 物理残差变换

三类原始偏差经可训练矩阵和 tanh 映射：

$$R_a=\tanh(W_a[\ddot{\hat u}-\ddot u_{eq}]),$$
$$R_v=\tanh(W_v[\dot{\hat u}-\dot u_{Newmark}]),\qquad
R_u=\tanh(W_u[\hat u-u_{Newmark}]).$$

tanh 将幅值限制在 $[-1,1]$，$W_a,W_v,W_u$ 学习三类残差对状态更新的相对影响。与 [[cm-pinns]] 把物理写进 loss 不同，这里的残差进入网络前向传播。

## 5.4 修改 LSTM cell

经典 LSTM 为：

$$C_t=f_t\odot C_{t-1}+i_t\odot\tilde C_t,\qquad h_t=o_t\odot\tanh(C_t).$$

Phy-RL/Phy-RLK 改为：

$$C_t=f_t\odot C_{t-1}+i_t\odot\tilde C_t+R_{u,v,a},$$
$$o_t=\sigma(W_o[h_{t-1},x_t]+b_o)+R_{u,v,a}.$$

残差既修正长期记忆，又修正输出通路，形成输入到非线性层输出的短连接。注意第二式把残差加到 sigmoid 后，$o_t$ 不再必然处于 $[0,1]$；论文没有单独分析这一变化的稳定性。

## 5.5 KAN 解码器

三层物理残差 LSTM 生成 $x/y$ 隐特征后，KAN 为每层、每方向学习独立的 B-spline 一元映射，再组合为加速度、速度与位移输出。KAN 在这里是**响应解码器**，不是像 [[kin]] 那样用 KAN 作为 PDE/能量求解器骨干；Concrete01、Steel01/02、Pinching4 也未直接写入 KAN。

## 5.6 损失函数

$$\mathcal L_{data}=\frac1N\sum_{d\in\{x,y\}}
(\|\hat u_d-u_d\|_2^2+\|\dot{\hat u}_d-\dot u_d\|_2^2+\|\ddot{\hat u}_d-\ddot u_d\|_2^2).$$

训练**只有 data loss**。所以“物理残差”是 inductive bias，不是硬约束，也不是像 [[phylstm2]] / [[phylstm3]] 那样可单独加权和监控的 physics loss。

## 5.7 训练流程

| 环节 | 配置 |
|------|------|
| 归一化 | MinMaxScaler 到 $[-1,1]$ |
| 序列 | 30 s / 0.02 s，sequence length=1500 |
| 网络 | 3 层 residual LSTM；hidden size=64；KAN decoder |
| 优化 | Adam，lr=0.001，batch=16 |
| residual 激活 | tanh |
| 训练 | 最多 1500 epochs；validation early stopping；patience=20 |
| 硬件 | Intel i5-13600KF + NVIDIA RTX 4080 |

网格搜索覆盖 batch 8/16/32/64、lr 0.1/0.01/0.001、hidden size 32/64/128，以及 sigmoid/ReLU/tanh。原文一处写“64 hidden layers”，结合搜索变量应解读为 **hidden size 64**，不是 64 层 LSTM。

## 5.8 数据生成

- SRM 生成 144 组经反应谱迭代修正的双向人工地震动；$y$ 向 PGA 为 $x$ 向的 85%；
- 六层 RC：0.1–1.0 g 共 10 个强度级，每级 115 训练、29 测试；
- 五层 RC：0–1.5 g、步长 0.1 g，共 15 个强度级，分层随机 8:2；
- OpenSees NLTHA 生成监督标签。

## 页内导航

- [[guo2026-phy-rlk-analysis|← 概述]]
- [[guo2026-phy-rlk-results|结果 →]]
- [[guo2026-phy-rlk-critical|批判分析 →]]
