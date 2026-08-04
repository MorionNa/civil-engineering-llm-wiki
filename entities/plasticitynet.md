---
id: entity--plasticitynet
title: PlasticityNet
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- entity/model
keywords:
- learned-elastoplastic-energy
- optimization-time-integration
- fem
- mpm
sources:
- sources/papers/plasticitynet-2022.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# PlasticityNet

## 定义

PlasticityNet 是一种学习局部弹塑性势能族的模型，使经典弹性应力与塑性回映射组合能够进入优化型隐式时间积分。^[sources/papers/plasticitynet-2022.md]

## 核心接口

- 输入：当前变形梯度 $F$、展开点 $F_0$、可选硬化状态 $h$；
- 输出：标量局部势能；
- 训练目标：势能梯度匹配目标弹塑性应力；
- 求解方式：外层更新 $F_0$ 的固定点 + 内层 FEM/MPM 能量最小化。

## 能力

论文展示砂、雪、金属、学习回映射及 BFEMP 双向耦合，且同一思想可用于 FEM 和 MPM。

## 边界

固定点不保证普遍收敛；稳定正则可能增加黏性；参数变化泛化有限；验证主要是数值与图形学场景。

## 项目角色

它是“神经模块替换低层本构/势能，而非替代完整物理求解器”的代表实体，可与 [[entities/xpbi]]、[[entities/bfemp]] 和 [[entities/incompressible-crack-mpm]] 比较。

## 关联页面

- [[plasticitynet-2022-analysis]]
- [[concepts/local-elastoplastic-potential-family]]
- [[concepts/fixed-point-optimization-plasticity]]
