---
id: concept--plasticity-in-the-loop-xpbd
title: XPBD 内循环塑性 — 约束迭代与回映射交替
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- fixed-point
- implicit-plasticity
- return-mapping
- xpbd
sources:
- sources/papers/yu2024-xpbi.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# XPBD 内循环塑性

## 定义

该策略不在时间步末尾一次性执行塑性回映射，而是在每次 XPBD 迭代中交替更新试算变形梯度、屈服面投影、约束乘子与速度，形成关于变形梯度的固定点。^[sources/papers/yu2024-xpbi.md]

## 机制

当前速度给出试算 $F^{E,tr}$，本构算子 $Z$ 将其投影至允许状态；投影后的状态用于计算弹性能约束与速度修正。下一次迭代再以新速度重算试算状态，直到完成预设 XPBD 迭代。

## 相对半隐式更新的意义

时间步末回映射会让求解过程使用屈服面外应力，导致材料在迭代中表现得过度弹性并产生伪影。内循环塑性让屈服约束从求解开始就影响速度和接触响应。

## 边界

“隐式”不等于已证明收敛。XPBI 论文没有监控塑性固定点的定量残差，而主要依靠少量迭代获得视觉合理结果。工程求解应增加本构残差、互补条件和自动停止准则。

## 关联页面

- [[entities/xpbi]]
- [[concepts/velocity-gradient-updated-lagrangian]]
- [[yu2024-xpbi-method]]
- [[yu2024-xpbi-critical]]
