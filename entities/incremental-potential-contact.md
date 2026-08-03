---
id: entity--incremental-potential-contact
title: "Incremental Potential Contact（IPC）— 可行路径大变形接触求解器"
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- entity/model
- evidence/paper
keywords:
- ipc
- barrier-contact
- projected-newton
- ccd
- variational-friction
sources:
- sources/papers/li2020-incremental-potential-contact.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# Incremental Potential Contact（IPC）

## 定义

IPC 是 Li 等提出的隐式有限元接触框架。它把大变形动力学、非穿透接触与近似 Coulomb 摩擦写成增量势能最小化，并通过障碍势与 CCD 线搜索维持求解路径的几何可行性。^[sources/papers/li2020-incremental-potential-contact.md]

## 核心组成

- [[concepts/local-smooth-contact-barrier]]：零距离发散、激活距离外为零的局部光滑障碍；
- [[concepts/ccd-filtered-feasible-line-search]]：CCD 给出安全步长上界；
- projected Newton：局部 Hessian 半正定投影与 SPD 线性系统；
- 变分摩擦：静摩擦平滑与滞后耗散势；
- 三类独立容差：动力学、几何间隙、静摩擦。

## 保证条件

- 无交叉：依赖初始无交叉、障碍势和 CCD 线搜索；
- 无反转：还需使用非反转材料能；
- 动量平衡：由增量势残差容差控制；
- 摩擦：静摩擦近似精度可控，但 lagging 无一般收敛保证。

## 适用范围

适用于带自接触、外部接触、摩擦和 codimensional 障碍的网格型非线性弹性动力学。适合连续构件、软体、薄体积网格和结构碎片接触，但不直接处理断裂拓扑生成。

## 工程角色

在结构倒塌软件中，IPC 可作为高可靠碰撞层，连接纤维梁、分层壳、实体单元与断裂后碎片。它更适合承担接触可行性，而材料破坏和碎片生成应由独立模型负责。

## 关联页面

- [[li2020-incremental-potential-contact-analysis]]
- [[li2020-incremental-potential-contact-method]]
- [[li2020-incremental-potential-contact-results]]
- [[li2020-incremental-potential-contact-critical]]
- [[entities/xpbi]]
- [[entities/incompressible-crack-mpm]]
