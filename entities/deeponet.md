---
id: entities--deeponet
title: DeepONet — 深度算子网络 (Deep Operator Network)
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- entity/model
- method/neural-operator
- method/pinn
keywords:
- ai4s
- deep-learning
- deeponet
- domain/ai4s
- entity/model
- metamodeling
- method/neural-operator
- method/pinn
- neural-network
- neural-operator
- operator-learning
- physics-informed
sources:
- raw/papers/10_1016_j_cma_2022_114587_extracted.txt
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
---

# DeepONet — 深度算子网络

## 定义

DeepONet（Deep Operator Network）是一种**神经算子**架构，由 Lu et al. (2021, Nature Machine Intelligence) 提出，用于学习**函数空间之间的映射**（即算子）。与标准神经网络学习有限维向量间的映射不同，DeepONet 学习的是无限维函数空间之间的映射关系。

$$G: u(x) \mapsto G(u)(y)$$

其中 u(x) 是输入函数（如初始条件、边界条件、参数场），G(u)(y) 是输出函数（如 PDE 的解在任意位置 y 的值）。

## 架构

DeepONet 由两个子网络组成：

```
输入函数 u (在 m 个传感器点采样)         输出位置 y
         ↓                                      ↓
    Branch Net ──→ [b₁, b₂, ..., bₚ]      Trunk Net ──→ [t₁, t₂, ..., tₚ]
         ↓                                      ↓
         └──────── Σ b_k · t_k  ────────────────┘
                        ↓
                   G(u)(y)  (输出函数在 y 处的值)
```

- **Branch Net（分支网络）：** 编码输入函数 u，输出 p 维特征向量 [b₁, ..., bₚ]
- **Trunk Net（主干网络）：** 编码输出位置 y，输出 p 维基函数 [t₁(y), ..., tₚ(y)]
- **输出：** 二者内积 `G(u)(y) = Σᵢ bᵢ(u) · tᵢ(y)`

### 关键性质

| 性质 | 说明 |
|------|------|
| 非线性近似 | 万能算子近似定理：单隐层 DeepONet 可逼近任意连续算子 |
| 输入函数离散化 | Branch 接受任意维度的传感器采样，理论上可处理任意分辨率 |
| 零样本泛化 | 训练完成后，对新输入函数仅需运行 Branch（Truck 网络不变） |
| 物理一致性 | 可嵌入物理约束（PDE 残差、变分能量等）实现 physics-informed 训练 |

## 历史脉络

| 时间 | 事件 |
|------|------|
| 1995 | Chen & Chen 证明神经网络万能算子近似定理 |
| 2021 | Lu et al. 提出 DeepONet 实用架构，发表于 Nature Machine Intelligence |
| 2022 | Goswami et al. 提出 V-DeepONet — 将变分能量物理约束引入 DeepONet |
| 2022- | 系列工作：PI-DeepONet、MIONet（多输入算子）、DeepONet + FNO 对比 |

## 与 PINN 的对比

| | DeepONet | PINN |
|---|---|---|
| 学习对象 | **算子**（函数空间 → 函数空间） | **单函数**（时空域 → 标量/向量） |
| 参数化 PDE | 天然支持，一次训练覆盖所有参数 | 需每次从头训练 |
| 推理速度 | 毫秒级 | 毫秒级（但需逐参数重训练） |
| 训练数据 | 需要 PDE 参数-解对（或多个参数下的物理损失） | 仅需物理损失（无数据） |

## V-DeepONet 变体

V-DeepONet（Goswami et al., 2022）将 DeepONet 的物理约束从 PDE 残差形式改为**变分能量形式**：

- 损失函数 = 系统总势能（弹性能 + 断裂能 + 外力功）
- 天然适合能量驱动系统（如断裂力学、相变）
- 混合训练：少量 FEM 标记数据 + 全域变分能量损失

> 详见 [[goswami2022-variational-deeponet-analysis]]

## 关联论文（本 Wiki）

- [[goswami2022-variational-deeponet-analysis]] — V-DeepONet：变分 DeepONet 用于裂纹路径预测
- [[goswami2022-variational-deeponet-method]] — V-DeepONet 方法展开
- [[pinn]] — PINN：另一种物理信息学习范式（单函数求解 vs 算子学习）
- [[wang2023-pinn-spurious-analysis]] — PINN 伪解问题（DeepONet 的物理约束同样需要关注）

## 关联资源

- 原始论文：Lu et al. (2021) "Learning nonlinear operators via DeepONet", Nature Machine Intelligence
- DeepXDE 库：内置 DeepONet 实现 `deepxde.nn.DeepONet`
- 综述：Operator Learning for Scientific Computing (arXiv 综述)

## Evidence By Source

### `raw/papers/10_1016_j_cma_2022_114587_extracted.txt`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/10_1016_j_cma_2022_114587_extracted.txt]
