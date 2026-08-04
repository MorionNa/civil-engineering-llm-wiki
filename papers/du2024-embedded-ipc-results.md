---
id: paper--du2024-embedded-ipc-results
title: "Du et al. (2024) — Embedded IPC 结果"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- teddy-bear-grasp
- finray-gripper
- real-time
- convergence
sources:
- sources/papers/du2024-embedded-ipc.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# Embedded IPC 结果与证据

## 玩具熊抓取
高分辨率熊网格 410 顶点/1207 单元；中分辨率 173/533；低分辨率 34/61。泡夹爪保持全空间，仅熊使用 Embedded IPC。^[sources/papers/du2024-embedded-ipc.md]

## 收敛与效率
所有方法对时间步呈一阶收敛。低分辨率嵌入相比全空间 IPC 报告约 2.0× 加速；$h=0.02$ s 时达到约 1.8× 实时。多线程相对单线程仅约 1.4×，基线实现并行度不同。

## 接触力
摩擦方向趋向解析结果；较粗嵌入产生更全局的变形和更大挤压力。Drake 接触对更多，作者推测与其允许轻微穿透有关。

## 薄板放置
FinRay 夹爪抓取薄板并插入碗架。Embedded IPC 模拟出夹爪弯曲并保持无穿透；Drake 的近似模型存在局部穿透，Isaac Sim 在紧密接触中出现深穿透和不稳定。

## 现实一致性边界
所有模拟与真实轨迹均有状态偏差，来源包括标定、测量、物性、接触近似和运动控制误差；误差会随接触序列累积。

## 关联页面
- [[du2024-embedded-ipc-analysis]]
- [[du2024-embedded-ipc-method]]
- [[du2024-embedded-ipc-critical]]
- [[entities/embedded-ipc]]
