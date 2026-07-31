---
title: "Park et al. (2024) SevenNet Critical Analysis"
created: 2026-07-31
updated: 2026-07-31
type: paper-critical
---

# SevenNet Critical Analysis

## Contributions

1. 解决 GNN-IP 多层 message passing 导致的并行通信困难；
2. 保持 NequIP 模型结构不变；
3. 通过 forward/reverse communication 实现大规模 MD；
4. 开源 SevenNet 工具链。

## Negative Knowledge

- 测试主要集中于材料原子系统；
- 通信效率依赖 GPU 利用率；
- 异质系统和超大 GPU 数量下同步成本可能增加；
- 不同图结构需要针对通信策略调整。

## 对结构动力 PINN / MechConv 的启发

SevenNet 的核心思想与大规模结构图学习高度相关：

```text
large graph
 ↓
partition
 ↓
local message passing
 ↓
boundary feature exchange
 ↓
global response
```

可迁移方向：

1. 建筑结构图拆分训练；
2. 子结构并行 PINN 求解；
3. MechConv 中跨子图边界信息交换；
4. 千自由度结构动力响应的大规模推理。

## Research Opportunity

未来可研究：

- Physics-aware graph partition；
- Mechanical ghost nodes；
- Substructure PINN with communication；
- Distributed neural operator for structural dynamics。
