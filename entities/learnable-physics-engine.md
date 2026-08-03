---
id: entity--learnable-physics-engine
title: Learnable Physics Engine for Interpretable Elastoplastic Geomaterial Models
type: entity
status: draft
project: civil-engineering-llm-wiki
tags: []
sources: []
created: '2026-08-03'
updated: '2026-08-03'
confidence: low
legacy_reproducibility: low
legacy_tags:
- message-passing
- physics-simulation
- scientific-machine-learning
- metamodeling
- time-marching
- long-horizon-rollout
- parallel-computing
- limitation
legacy_sources:
- raw/papers/zhou2025-learnable-physics-engine.xml
---

# Learnable Physics Engine for Interpretable Elastoplastic Geomaterial Models

## 定义

这是 Zhou 与 Feng（2025）提出的、基于 message passing neural network（MPNN）的可学习物理引擎。它以 OSB-PD Drucker–Prager 弹塑性模型为目标，把材料点和邻域键写成图，用可解释的 elastic energy 与 yield function 网络替代部分传统本构计算，再由 MPNN 推进力状态、塑性状态和材料点位置。

它不是一个只输出应力的黑箱 constitutive surrogate，也不是学习一般 PDE 算子的 MP-PDE；它更接近“本构算法 + 图状态推进 + GPU 批处理”的混合数值引擎。→ [[zhou2025-learnable-physics-engine-analysis]]

## 身份与关键事实

| 项目 | 内容 |
|---|---|
| 原论文 | Xiao-Ping Zhou、Kai Feng（2025） |
| 题名 | *The novel learnable physics engines for interpretable elastoplastic models of geomaterials based on the message passing neural network* |
| 期刊 | *International Journal of Rock Mechanics and Mining Sciences* |
| 卷/文章号 | 194 / 106244 |
| DOI | 10.1016/j.ijrmms.2025.106244 |
| 目标模型 | OSB-PD Drucker–Prager elastoplasticity |
| 图实现 | PyTorch Geometric |
| 公开性 | XML 仅称数据可按请求提供；无公开代码 URL、数据 URL 或权重 |

## 非线性类型

主导非线性是**材料本构非线性**：塑性应变不可逆，Drucker–Prager 屈服面随塑性状态/硬化演化，力状态由 elastic energy 的导数和弹塑性状态决定。OSB-PD 的非局部积分以及图消息传递描述材料点相互作用；MPNN 中的 Tanh 是函数逼近的非线性，不应被误称为 PDE 算子非线性。

这一区分与 [[cm-pinns]] 的设计原则一致：当非线性来自本构关系时，需要显式处理 $\sigma(\varepsilon,\text{history})$ 或等价的 energy/yield/state 接口，而不是只在一个 PDE residual 中增加自动微分项。

## 核心组成

### 1. 图表示

- 节点 $v_i$：OSB-PD 材料点及其位置、位移、塑性等状态；
- 边 $e_k$：horizon 内的相互作用键、端点索引和边特征；
- 聚合：对指向节点的边消息逐元素求和，再更新节点。

### 2. 可解释弹性 energy

键伸长 $s$ 先得到体积膨胀 $\Theta$，储能拆成：

$$
\psi=\psi_k+\psi_d,
\qquad \psi_k=\frac12 k\Theta^2,
\qquad \psi_d=\mu'\,\omega\cdot(s^d)^2.
$$

网络学习 $\hat\psi_k,\hat\psi_d$，力状态由 $T=\nabla_\eta\psi$ 计算。H² Sobolev training 同时约束 energy 值、一阶导数和二阶导数，以改善力/切线的一致性和平滑性。

### 3. Level-set yield function

屈服函数以 $p,q,\zeta$ 为输入，基本形式为：

$$
F_y=J_2+\alpha_{DP}I_1-k_{DP}(\zeta).
$$

论文把不同塑性状态下的屈服面转换为 signed-distance level set，把累计塑性状态作为 pseudo-time，用 Hamilton–Jacobi 演化和有限差分速度场生成训练数据，再学习 $\hat f(p,q,\zeta)$。若 $\hat f>0$，通过自动微分 Newton 求解塑性乘子并更新塑性状态。

### 4. 三段式 MPNN

| 模块 | 作用 |
|---|---|
| MPNN1 | 图状态 → 键伸长 $s$ |
| MPNN2 | $s$ → energy、力状态、$p/q$、屈服判断、塑性更新 |
| MPNN3 | 力状态 → 合力、材料点位置和下一图状态 |

MPNN2 的代表性配置是 5 个、每层 30 单元的隐藏层，Tanh 激活；Adam 初始学习率 0.0005，每 100 epoch 将学习率乘以 0.1。

## 论文中验证的范围

- 单轴拉伸卸载的材料点/板 benchmark；
- 1 m 方板、0.2 m 刚性压头、2000 步压入；
- $10{,}000$ 材料点的圆形洞室开挖，初始应力 45 MPa、分两阶段施工；
- 20 m 高、45° 坡角的理想弹塑性边坡稳定；
- 100 个数值例子、每例 2000 步的 CPU/GPU 速度比较。

论文报告这些案例中位移、应力/压力和塑性应变场与 OSB-PD 参考结果相符，并在 3600→90,000 材料点时给出 PD 200→3000 s、surrogate 10→45 s 的端点比较。但这些是同一 OSB-PD/Drucker–Prager 合成数据域内的证据。

## 关系与边界

- 与 [[mp-pde]]：都用图消息传递和时间推进，但 MP-PDE 的目标是 PDE 解算子；本实体的目标是材料 energy/yield/state 和 OSB-PD 相互作用。
- 与 [[message-passing-reach-contract]]：图边和消息层数决定有效物理传播范围，跨分辨率/子图部署前需要 reach/halo 审计。
- 与 [[cm-pinns]]：都显式保留本构物理；CM-PINNs 把本构恢复力放进 PINN loss，本实体把本构函数装配进图 physics engine。
- 与 [[bouc-wen-model]]：Bouc–Wen 是另一类历史依赖滞回模型，可做状态接口和长期 rollout 的对照，但不是 Drucker–Prager 屈服面的等价模型。

## 局限

1. 公开 XML 未给代码、数据下载地址或权重；数据只能按请求提供，精确结果难以独立复核。
2. 物理假设集中在 OSB-PD Drucker–Prager、非关联流动和理想/线性硬化，未证明适用于各向异性、软化、损伤、率效应、孔压、循环滞回或真实裂隙岩土体。
3. 长期预测虽覆盖 2000 步，但 benchmark 已观察到累计塑性应变轻微漂移，没有任意时长稳定性证明。
4. 洞室例的塑性区更平滑可能是优势，也可能掩盖局部化；需要局部梯度和分辨率收敛验证。
5. 速度优势依赖 RTX 3080、图张量化和 PD 参考实现，不能无条件推广到所有优化 FEM/PD 求解器。

## 可复现性

| 项目 | 说明 |
|---|---|
| 等级 | 🔴 低 |
| 代码 | [] |
| 数据 | []；原文为 on request |
| 可重建 | 方法结构、主要公式、部分网络和训练设置 |
| 缺口 | 数据规模/划分、归一化、随机种子、停止标准、完整图构造、版本和逐步结果 |

## 关联论文页

- [[zhou2025-learnable-physics-engine-analysis]]
- [[zhou2025-learnable-physics-engine-method]]
- [[zhou2025-learnable-physics-engine-results]]
- [[zhou2025-learnable-physics-engine-critical]]

## Verification Needed

This page was carried over from the local workspace during the merge. Verify its source record and promote it from draft before treating the claims as independently verified.
