---
id: entity--embedded-ipc
title: Embedded IPC
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- entity/model
keywords:
- reduced-ipc
- collision-embedding
- robot-manipulation
sources:
- sources/papers/du2024-embedded-ipc.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# Embedded IPC

## 定义
在低分辨率四面体自由度上求解弹性，在高分辨率原表面上计算 IPC 障碍与摩擦，再通过线性映射投影回约化坐标。^[sources/papers/du2024-embedded-ipc.md]

## 能力与边界
可在接触丰富机器人任务中达到交互速度并保持 IPC 可行路径；小子空间会锁定，当前仅支持体积软体且嵌入网格需启发式构造。

## 关联页面
- [[du2024-embedded-ipc-analysis]]
- [[concepts/coarse-elasticity-fine-contact-embedding]]
- [[concepts/reduced-coordinate-ipc]]
- [[entities/incremental-potential-contact]]
