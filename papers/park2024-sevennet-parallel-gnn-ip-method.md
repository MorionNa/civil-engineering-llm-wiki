---
id: paper-park2024-sevennet-parallel-gnn-ip-method
title: "Park et al. (2024) — SevenNet 并行方法"
type: paper-analysis
status: verified
project: civil-engineering-llm-wiki
tags: [neural-network, deep-learning, physics-simulation, scientific-machine-learning, distributed-training, gpu-computing, material-design]
sources: [raw/papers/park2024-sevennet-parallel-gnn-ip-source.md]
created: 2026-07-31
updated: 2026-07-31
confidence: high
methods: [spatial-decomposition, ghost-atoms, layerwise-forward-communication, reverse-gradient-communication, nequip-backbone, lammps-integration]
reproducibility: high
---

# SevenNet 并行方法

## 问题定义

对 $L$ 层 message-passing GNN-IP，节点 $i$ 的最终特征依赖最多 $L$ 跳邻域。若每层 cutoff 为 $r_c$，一次性 halo 方案需要为每个子域准备近似 $Lr_c$ 宽的扩展区域，并在本地重复计算远程节点的中间特征。^[raw/papers/park2024-sevennet-parallel-gnn-ip-source.md]

SevenNet 的目标是保持单次通信范围为 $r_c$，通过逐层通信隐藏特征实现与完整图相同的前向结果，并在能量求导时执行对应的反向梯度通信。

## 空间分解

模拟盒被划分为多个空间子域，每张 GPU/MPI rank 负责：

- 位于本地子域内的 owned atoms；
- 位于 cutoff 邻域内、由其他子域拥有的 ghost atoms；
- 本地与 ghost 原子之间的图边；
- 本地原子的能量和最终力。

```text
全局原子域
┌───────────┬───────────┐
│  rank A   │  rank B   │
│ owned     │ owned     │
│ + ghost B │ + ghost A │
└───────────┴───────────┘
```

原子坐标和元素等基础信息由传统 MD 邻域交换提供；GNN 中新增的是每层节点隐藏状态和反向梯度通信。

## 正向通信

设第 $l$ 层节点特征为 $h_i^{(l)}$。每个子域先用当前可见的 owned/ghost 特征执行本地 message passing：

$$
h_i^{(l+1)}
=U^{(l)}\left(
h_i^{(l)},
\sum_{j\in\mathcal N(i)}M^{(l)}
\left(h_i^{(l)},h_j^{(l)},e_{ij}\right)
\right).
$$

完成该层后，owned 边界原子的 $h_i^{(l+1)}$ 被发送到需要其作为 ghost 的相邻子域，覆盖旧 ghost 特征。然后下一层继续本地计算。^[raw/papers/park2024-sevennet-parallel-gnn-ip-source.md]

```text
第 l 层本地计算
      ↓
打包 owned 边界节点 h^(l+1)
      ↓
邻域通信
      ↓
更新 ghost 节点 h^(l+1)
      ↓
进入第 l+1 层
```

这种方案把一次宽 halo 复制改为 $L$ 次窄 halo 特征交换。

## 能量归属

为避免重复计数，每个 rank 只累加其 owned atoms 的原子能：

$$
E=\sum_{r}\sum_{i\in\Omega_r^{\mathrm{owned}}}E_i.
$$

ghost atoms 参与邻域计算，但不在当前 rank 重复贡献原子能。

## 反向梯度通信

原子力通过总能量对原子坐标求导得到。由于 forward 中 ghost 特征来自其他 rank，反向传播时对 ghost 特征的梯度必须返回其 owner：

$$
\frac{\partial E}{\partial h_j^{(l)}}
=\sum_{r\ \mathrm{using}\ j\ \mathrm{as\ ghost}}
\frac{\partial E_r}{\partial h_{j,r}^{(l)}}.
$$

反向阶段按层的逆序执行：

```text
能量梯度
   ↓
第 L 层本地反向
   ↓
将 ghost feature gradient 发回 owner
   ↓
owner 对梯度求和
   ↓
第 L-1 层本地反向
   ↓
……
   ↓
坐标梯度 → 原子力
```

因此，forward communication 交换节点值，reverse communication 交换节点特征梯度。^[raw/papers/park2024-sevennet-parallel-gnn-ip-source.md]

## 与一次扩展 halo 的比较

| 方案 | 通信次数 | 内存/冗余 | 特点 |
|---|---:|---|---|
| 一次宽 halo | 较少 | 保存 $Lr_c$ 区域，重复计算多 | 实现直接，但随层数迅速膨胀 |
| SevenNet 逐层通信 | 每层一次正向 + 一次反向 | halo 保持 $r_c$，通信隐藏特征 | 降低冗余，增加消息启动与带宽需求 |
| [[allegro]] 严格局部 | 无跨层节点特征通信 | pair 特征显存较高 | 改变架构，固定有效通信半径 |

## NequIP/SevenNet 模型骨干

SevenNet 使用 E(3) 等变消息传递骨干，继承 [[nequip]] 的：

- 原子图与局部 cutoff；
- 标量和高阶张量隐藏特征；
- 球谐与张量积等变交互；
- 原子能求和；
- 总能量自动微分得到力。

并行算法的目标不是近似或裁剪这些运算，而是保持分布式输出与单域模型一致。

## SevenNet-0 训练

论文报告 SevenNet-0 使用 Materials Project/M3GNet 数据集训练，覆盖 89 种元素。模型用于展示通用预训练原子势和大规模材料 MD。^[raw/papers/park2024-sevennet-parallel-gnn-ip-source.md]

知识库需要区分两个层次：

1. **并行算法：** 可作用于 NequIP 类 GNN-IP；
2. **SevenNet-0 模型：** 使用特定数据和超参数训练的通用势。

并行算法正确不意味着 SevenNet-0 对任意新材料都已验证。

## LAMMPS 集成

SevenNet 将模型与 LAMMPS 的空间分解、邻居列表和时间积分连接：

- LAMMPS 管理坐标、周期边界、原子迁移和邻居列表；
- SevenNet 执行 GNN 前向、逐层特征通信和力计算；
- GPU 负责张量运算；
- MPI/NCCL 等通信路径负责 rank 间数据交换。

## 复杂度与性能因素

主要计算量随以下因素增长：

- owned 原子数；
- 平均邻居数；
- message-passing 层数；
- 每个 irrep 的通道数；
- 通信边界原子数；
- 隐藏特征的张量阶与精度。

通信时间近似取决于：

$$
T_{comm}\approx
L\left(\alpha + \beta N_{boundary}d_h\right),
$$

其中 $\alpha$ 是消息启动延迟，$\beta$ 是单位数据传输成本，$d_h$ 是隐藏特征维度。这一表达是系统分析近似，不是原论文给出的严格公式。

## 方法边界

- 网络层数越深，正向和反向通信轮数越多；
- 子域过小会使通信和 kernel 启动超过本地计算；
- 不均匀原子密度会导致负载失衡；
- 长程物理需要额外通信或显式求解器；
- 通信精度压缩可能改变力和能量一致性，需要单独验证。

## 关联页面

- [[park2024-sevennet-parallel-gnn-ip-analysis]]
- [[park2024-sevennet-parallel-gnn-ip-results]]
- [[park2024-sevennet-parallel-gnn-ip-critical]]
- [[sevennet]]
- [[nequip]]
- [[allegro]]
