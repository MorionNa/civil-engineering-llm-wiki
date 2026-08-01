---
id: sources--papers--juel2026-stabilized-fractional-step-mpm
title: "Juel et al. (2026) — 稳定化分步双相 MPM"
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- double-point-mpm
- fractional-step
- hydromechanical-coupling
- pressure-gradient-projection
- spgp
- tpic-pressure
- two-phase-mpm
sources:
- raw/papers/juel2026-stabilized-fractional-step-mpm-source.md
created: '2026-08-01'
updated: '2026-08-01'
confidence: high
evidence_scope: full-text
code_url: []
dataset_url: []
---

# 来源记录：稳定化分步双相 MPM

## 文献信息

- **英文题名：** A stabilized fractional-step MPM with pressure gradient projection for coupled hydromechanical extreme deformations
- **作者：** Mikkel Metzsch Juel、Hervé Vicari、Yidong Zhao、Lars Blatny、Chenfanfu Jiang、Johan Gaume
- **期刊：** Computer Methods in Applied Mechanics and Engineering, 461 (2026), 119140
- **DOI：** 10.1016/j.cma.2026.119140
- **证据范围：** 用户提供的 40 页正式全文。

## 证据地图

- 第 1–3 页：问题背景、增量/非增量分步法矛盾、主要贡献。
- 第 4–17 页：双相连续体、双点 MPM、压力与阻力时间离散、压力泊松方程、SPGP 与自由液面。
- 第 18–31 页：固结、渗流、溃坝、穿过多孔介质的溃坝、三维饱和球碰撞与性能分析。
- 第 31–36 页：结论、核修正、耦合校正方程、粒子重排和临界时间步。

## 证据边界

论文验证的是饱和固–液两相大变形、低渗透和相分离问题。未包含非饱和、热耦合、塑性固相、真实滑坡全尺度案例或独立代码复现。本知识库中的建筑倒塌、地震液化和区域灾害迁移内容均单独标记为迁移推论。

## 生成页面

- [[papers/juel2026-stabilized-fractional-step-mpm-analysis]]
- [[papers/juel2026-stabilized-fractional-step-mpm-method]]
- [[papers/juel2026-stabilized-fractional-step-mpm-results]]
- [[papers/juel2026-stabilized-fractional-step-mpm-critical]]
- [[entities/stabilized-fractional-step-two-phase-mpm]]
- [[concepts/stabilized-pressure-gradient-projection]]
- [[concepts/tpic-pressure-mapping]]
