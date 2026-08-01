---
id: sources--papers--chen2026-empm
title: "Chen 等（2026）— EMPM：面向可变形物体建模与仿真的具身材料点法"
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
keywords:
- differentiable-mpm
- deformable-object
- digital-twin
- gaussian-splatting
- material-identification
- online-adaptation
- robotics
sources:
- raw/papers/chen2026-empm-source.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
evidence_scope: full-text
code_url: []
dataset_url: []
---

# 来源记录：EMPM

## 文献信息

- **题目：** EMPM: Embodied MPM for Modeling and Simulation of Deformable Objects
- **作者：** Yunuo Chen、Yafei Hu、Lingfeng Sun、Tushar Kusnur、Laura Herlant、Chenfanfu Jiang
- **机构：** Robotics and AI Institute；UCLA
- **版本：** arXiv:2601.17251v1，2026-01-24
- **项目网页：** https://embodied-mpm.github.io
- **证据：** 用户提供的 9 页全文 PDF。

## 证据范围

论文提出一个真实—仿真—真实流程，将多视角 RGB-D 重建、三维高斯泼溅外观建模、可微材料点法、离线参数识别与在线校正结合起来。实验覆盖弹性和弹塑性物体，并与 PhysTwin、PGND 进行比较，同时展示双臂 Franka 操控的概念验证。

## 页码映射

- **第 1–2 页：** 研究动机、贡献和相关工作。
- **第 3–5 页：** 系统流程、MPM 方程、离线和在线识别。
- **第 5–8 页：** 实验设置、定性与定量结果、应用和限制。
- **第 9 页：** 参考文献。

## 生成的知识页

- [[papers/chen2026-empm-analysis]]
- [[papers/chen2026-empm-method]]
- [[papers/chen2026-empm-results]]
- [[papers/chen2026-empm-critical]]
- [[entities/empm]]
