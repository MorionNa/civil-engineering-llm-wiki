---
id: sources--articles--shenlan2026-physical-token-transolver
title: 深蓝（2026）— 从CFD到Transolver：物理世界的Token是什么？
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/webpage
- method/neural-operator
- method/transformer
keywords:
- cfd
- dynamic-mode-decomposition
- dynamic-slicing
- full-attention
- meshgraphnet
- physical-token
- physics-attention
- proper-orthogonal-decomposition
- transolver
sources:
- raw/webpages/shenlan2026-physical-token-transolver-source.md
- https://zhuanlan.zhihu.com/p/2051000407711912984
created: '2026-08-01'
updated: '2026-08-01'
confidence: medium
evidence_scope: webpage
---

# Source Note：从CFD到Transolver——物理世界的 Token 是什么？

## Source Metadata

- **作者：** 深蓝
- **来源：** 知乎专栏文章
- **原文地址：** https://zhuanlan.zhihu.com/p/2051000407711912984
- **文章编辑时间：** 截图显示为 2026-06-19 09:19
- **本次证据：** 用户提供的 7 页网页打印 PDF；技术正文位于第 1-5 页，第 6-7 页为作者卡片、推荐和评论。
- **证据性质：** 二次技术解读，不是 Transolver 原始论文，也不是独立复现实验。

## Page-Level Evidence Map

| 页码 | 主要内容 | 可用于支持的知识 |
|---|---|---|
| 1 | PINN、DeepONet、FNO、MeshGraphNet、Transolver 的方法演进；CFD 网格单元间的信息交换 | 物理求解方法可从“信息如何传播”这一共同问题理解 |
| 2 | GNN 消息传递、全注意力的 $N^2$ 关系数、二维/三维网格规模示例 | 节点级全局 Attention 在高分辨率 PDE 问题上的计算瓶颈 |
| 3 | 涡旋场与 DMD 模态 | 复杂流场可能由少量紧凑表示描述；与 POD/DMD 的降维类比 |
| 4 | Encoder 后从几何空间映射到特征表示空间；Dynamic Slicing 按特征而非固定空间位置聚合 | Slice 是输入相关的软聚合，而非固定网格分区 |
| 5 | 多对多节点-Slice 关系、Slice Token、Physics Attention、回传节点 | “物理 Token”是训练中学习出的紧凑中间表示 |

## Extracted Author Claims

### 1. 物理计算可以被统一理解为信息传播

文章把传统数值方法、图神经网络和 Transformer 放在同一条信息传播链上：传统数值方法在网格间传播，GNN 在节点间传播，而 Transformer 在 Token 间传播。这个框架用于提出核心问题：对复杂物理系统而言，什么对象才适合作为 Token？

### 2. 把每个物理节点都当作 Token 会产生不可承受的全注意力成本

文章以 $64\times64$、$512\times512$ 二维流场和 $256^3$ 三维网格说明节点数增长速度，并指出标准 Attention 需要建立约 $N^2$ 个关系。文章给出的三维示例约有 1700 万节点、$2.8\times10^{14}$ 个注意力矩阵元素；即使只以 FP16 存储该矩阵，也会超过 500 TB。该数量级用于说明节点级全局 Attention 在实际工程 PDE 上通常不可行。

### 3. 有效自由度可能远小于离散自由度

文章借助 POD、DMD 和降阶模型说明：虽然流场可能包含大量网格自由度，但真正决定系统行为的有效自由度往往更少。Transolver 被解释为试图用神经网络端到端学习这种紧凑表示，并使表示随输入动态变化。

### 4. Dynamic Slicing 在特征空间中进行输入相关的软聚合

文章强调 Slice 不是固定的空间切片。节点先经过 Encoder，从坐标、边界条件和物理量等原始输入映射为高维特征；Dynamic Slicing 再依据这些特征，让每个节点以不同权重参与多个 Slice。几何上相距很远但特征相似的节点可能进入同一 Slice，几何上相邻但状态不同的节点也可能被分配到不同 Slice。

### 5. Physics Attention 在少量 Slice Token 之间完成全局信息交换

大量节点被压缩为少量 Slice Token 后，模型不再直接构建所有节点对之间的联系，而是在 Token 之间执行全局交互，再把获得的全局信息反馈给节点。文章把这一路径概括为：Encoder 与 Dynamic Slicing 寻找紧凑状态表示，Physics Attention 在这些表示之间交换信息。

### 6. 物理 Token 不是天然存在的固定区域

文章最终把物理 Token 定义为训练过程中学习得到的一组中间表示：它们不是图像 Patch，也不必对应固定几何区域，而是能够表达复杂物理系统状态的紧凑特征组合。

## Evidence Boundaries

- 本来源是技术科普文章，适合提取解释框架、概念关系和研究启发，不足以独立确认 Transolver 的原始公式、实现细节、数据集、训练配置或 benchmark 结果。
- 文中关于 Attention 显存的数字是解释性数量级估算，未在本次 ingest 中重新计算模型的全部中间张量、Q/K/V 和训练显存。
- POD/DMD 与 Dynamic Slicing 的关系是文章给出的思想类比；不能据此把 Transolver 等同于固定线性降阶方法。
- 对结构动力学、MechConv 或 PINN 的应用属于后续迁移推论，而不是作者在本文中验证的结论。

## Generated Knowledge Pages

- [[notes/articles/shenlan2026-physical-token-transolver]]
- [[entities/transolver]]
- [[concepts/physical-token]]
- [[concepts/dynamic-slicing]]
- [[concepts/physics-attention]]
