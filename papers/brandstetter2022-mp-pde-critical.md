---
id: paper--brandstetter2022-mp-pde-critical
title: Brandstetter et al. (2022) — MP-PDE 批判与结构动力迁移
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/brandstetter2022-mp-pde
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- limitation
- future-work
- message-passing
- physics-simulation
legacy_sources:
- raw/papers/arxiv_2202_03376.pdf
- raw/papers/extracted/arxiv_2202_03376_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 批判性分析

## 贡献
MP-PDE 把离散拓扑灵活性、物理参数条件化和闭环稳定训练合并到一个端到端图框架；pushforward 的训练分布设计可复现且成本有限。

## Negative Knowledge
1. 模型是数据驱动 learned solver，没有保证 \(Kx+Cv+Ma=F\)。
2. 边特征不是一般矩阵边算子，也没有可替换滞回状态接口。
3. Temporal bundling 仍需多次调用，存在自回归漂移。
4. 高质量真值生成是最难部分；数据成本没有消失。
5. 作者自己的优化数值求解器后来快多个数量级，原表不能作为普适速度优势。
6. 缺少误差上界和失败检测。

## 对 MTP-MechConv 的采用
- 采用：相对状态差、参数条件化、图拓扑泛化、训练期 pushforward 思想。
- 修改：时间主干使用稳定整段因果算子，空间消息乘矩阵边权，本构由插件计算。
- 拒绝：把 learned state update 直接当严格物理；引用未优化数值基线宣称加速。

## 可证伪门槛
在固定误差目标下，direct inference 必须比同硬件优化 Newmark/FEM 更快；若只在大批量快，应明确标注吞吐而非单样本延迟。平衡、边内力、本构状态和 halo 等价须独立报告。

## 关联页面
- [[brandstetter2022-mp-pde-analysis]]
- [[mp-pde]]
- [[message-passing-reach-contract]]

^[sources/papers/brandstetter2022-mp-pde]
