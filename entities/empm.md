---
id: entity--empm
title: EMPM — 具身可微材料点法框架
type: entity
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- entity/model
- evidence/paper
keywords:
- deformable-object
- differentiable-mpm
- digital-twin
- online-identification
- real-to-sim-to-real
sources:
- sources/papers/chen2026-empm.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
---

# EMPM

## 定义

EMPM 是一种由多视角 RGB-D 观测驱动的具身可微材料点法框架，用于重建、识别、模拟并渲染可变形物体。它将 MPM 连续介质力学、材料参数优化、三维点云监督和三维高斯泼溅整合在一个真实—仿真—真实流程中。^[sources/papers/chen2026-empm.md]

## 核心组成

- 多视角 RGB-D 融合与目标分割。
- 离线三维点追踪。
- 基于 Warp 实现的 APIC 风格可微 MPM。
- Fixed Corotated 弹性和 von Mises 塑性返回映射。
- Chamfer、追踪点和掩膜损失。
- 离线与在线材料参数校正。
- 由 MPM 粒子驱动的 3DGS 外观模型。

## 在本知识库中的作用

EMPM 与可微系统识别和局部粒子断裂仿真密切相关。对结构倒塌研究而言，其主要价值是证明 MPM 参数能够利用观测误差在线更新，并嵌入动作条件数字孪生；但 EMPM 本身并不是建筑倒塌求解器。

## 证据边界

本实体页基于 arXiv:2601.17251v1 全文建立，未执行代码复现或独立实验验证。

## 关联页面

- [[chen2026-empm-analysis]]
- [[chen2026-empm-method]]
- [[chen2026-empm-results]]
- [[chen2026-empm-critical]]
- [[entities/3d-gaussian-splatting]]
