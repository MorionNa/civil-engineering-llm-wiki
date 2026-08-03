---
id: paper--moseley2023-fbpinn-critical
title: Moseley et al. (2023) — FBPINN 批判与 MechConv 迁移
type: paper-analysis
status: draft
project: civil-engineering-llm-wiki
tags: []
sources:
- sources/papers/moseley2023-fbpinn
created: '2026-07-31'
updated: '2026-07-31'
confidence: low
legacy_tags:
- limitation
- future-work
- spatial-partitioning
- spectral-bias
legacy_sources:
- raw/papers/10_1007_s10444_023_10065_9.pdf
- raw/papers/extracted/10_1007_s10444_023_10065_9_extracted.txt
evidence_scope: local workspace source record pending canonical verification
---

# 批判性分析

## 贡献
局部归一化把域分解与谱偏差直接联系起来；平滑窗解表示减少额外接口损失；论文也坦率报告了与传统方法的巨大训练时间差。

## Negative Knowledge
1. 单层局部通信在子域很多时不够，需粗层补充。
2. 子域重叠数随维度增长，可能产生组合爆炸。
3. 断裂/强不连续恰落接口时，窗函数求和会使拟合更难。
4. 报告的前向 FLOPs 不等于完整 wall-clock。
5. 单 GPU 10 h 对比 FD 1 min，不能声称训练比经典法快。
6. 每个 PDE 实例重新训练，不是端到端条件算子。

## 对结构动力的采用
- 采用局部尺度化、halo、分区调度和接口敏感性诊断；
- 采用 [[multilevel-fbpinn]] 粗层以避免大子域数通信退化；
- 不对本构状态无条件平均；强非线性构件应核心单归属；
- 训练条件化算子，正式推理一次前向，不逐案例优化。

## 通过阈值建议
同一全图与任意合法分区的核心预测最大差应接近浮点容差；扩大 DOF 时显存近似 \(O(|V_\mathrm{sub}|T)\)，误差不随分区数系统恶化，且 direct inference 在同误差下快于优化 Newmark。

## 关联页面
- [[moseley2023-fbpinn-analysis]]
- [[fbpinn]]
- [[multilevel-fbpinn]]

^[sources/papers/moseley2023-fbpinn]
