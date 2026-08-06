---
id: concept--residual-based-adaptive-refinement
title: Residual-Based Adaptive Refinement（RAR）— 残差驱动的物理信息采样加密
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- method/pinn
- evidence/paper
keywords:
- residual-based-adaptive-refinement
- adaptive-collocation
- residual-driven-sampling
- hard-region-refinement
sources:
- sources/papers/li2026-qpinn-rar.md
created: '2026-08-06'
updated: '2026-08-06'
confidence: high
---

# Residual-Based Adaptive Refinement（RAR）

## 定义

RAR 是一种用于物理信息神经网络的自适应配置点加密机制：模型先在初始采样集上训练，再在候选点集计算控制方程残差，将残差较大的点加入训练集，以把后续计算资源集中到当前最难满足物理约束的区域。^[sources/papers/li2026-qpinn-rar.md]

## 本文实现流程

Li 等的 QPINN-RAR 采用以下循环：

1. 在 PDE 定义域内均匀随机生成初始训练集 $D_0$；
2. 训练模型若干轮；
3. 在候选集 $C$ 上计算 $s(x)=|r(x)|$；
4. 按残差排序，以比例 $\lambda$ 划分高残差区域 $P$；
5. 从 $P$ 中选取残差最大的 $n$ 个点；
6. 将新点并入训练集并继续训练，直到达到停止条件。

论文的数值配置为：Adam 阶段每 2000 次迭代执行一次 RAR，每轮增加 100 个配置点；初始配置点、边界点和初值点分别为 500、50 和 50。候选集规模与 $\lambda$ 的具体取值未在正文中清楚给出，因此属于复现缺口。

## 机制解释

固定均匀采样会在平滑区域浪费点，同时可能遗漏边界层、陡梯度、局部峰值或其他难拟合区域。RAR 用当前模型的 PDE 残差作为误差代理，使训练点分布随模型状态变化。它并不改变控制方程，也不直接保证真实解误差下降；其作用是重新分配物理约束的采样预算。

## 与普通自适应采样的关系

[[adaptive-sampling-pinn]] 是更宽泛的概念，可能依据损失、梯度、不确定性、重要性或残差调整采样。RAR 是其中以 PDE 残差为核心信号、通过追加高残差点实现加密的一类具体方法。

## 适用条件

- 可以在候选点上较低成本地计算 PDE 残差；
- 局部残差能够合理指示当前训练不足区域；
- 新增配置点不会使自动微分和优化成本失控；
- 训练过程允许周期性暂停、评估和扩充数据集。

## 失败边界

- 小残差不必然意味着解误差小，尤其在病态 PDE、错误边界条件或伪解附近；
- 持续追加点会增大每轮训练成本，点数节省不等于墙钟时间节省；
- 若候选集没有覆盖真正困难区域，RAR 无法发现该区域；
- 若残差尺度在不同方程项或空间区域间严重失衡，排序可能偏向数值尺度而非物理重要性；
- 该策略不能替代损失加权、优化器设计、硬约束或稳定性分析。

## 对结构动力学的迁移推论

**迁移推论：** 对连续时间结构响应 PINN，可按动力平衡残差在时间轴上增加配置点；对图结构或空间离散模型，可在高节点不平衡力、高本构残差或高能量误差区域局部加密。实际应用应同时监测位移/速度/加速度误差、守恒误差和长时滚动稳定性，不能只按单一残差采样。

## 关联页面

- [[li2026-qpinn-rar-method]]
- [[li2026-qpinn-rar-critical]]
- [[qpinn-rar]]
- [[adaptive-sampling-pinn]]
