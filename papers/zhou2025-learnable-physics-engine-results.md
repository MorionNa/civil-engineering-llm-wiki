---
title: "Zhou & Feng (2025) — Learnable Physics Engine 数值结果"
created: 2026-07-28
updated: 2026-07-28
type: paper-analysis
tags: [scientific-machine-learning, message-passing-neural-network, learnable-physics-engine, peridynamics, elastoplasticity, geomaterials, gpu-computing, synthetic-data]
sources: [raw/papers/zhou2025-learnable-physics-engine.xml]
results: [gpu-computing, synthetic-data]
datasets: [synthetic-data]
confidence: high
---

# Learnable Physics Engine 数值结果

> 返回 [[zhou2025-learnable-physics-engine-analysis]] · 方法 [[zhou2025-learnable-physics-engine-method]] · 实体 [[learnable-physics-engine]]

## 1. 证据范围

全文 XML 包含 19 幅图、3 个算法流程、训练/测试和三类工程几何。结果主要以场图和绝对误差图呈现，缺统一数值表。

## 2. 能量与屈服模块

Figures 8–10 显示能量网络在独立测试集上能拟合能量及导数，理想弹塑性与线性硬化的屈服 level set 也能复现单轴加载路径。正文未给统一 RMSE/置信区间。

## 3. 卸载路径基准

板的单轴拉伸—卸载中，等效应力预测误差被描述为可忽略；累计等效塑性应变在连续前向中出现轻微误差积累。（原文 Figure 11）这说明路径推进可行，也揭示内变量递推是长期误差源。

## 4. 冲头压入

刚性冲头压入后比较位移、等效应力和累计塑性应变。作者报告经过 2000 步前向预测，最大绝对误差比参考值小 1–2 个数量级。（Figures 12–13）

## 5. 圆洞开挖

10,000 个材料点，先建立 45 MPa 原位应力，再删除圆洞区域模拟开挖。位移最大绝对误差约比实际量级低一个数量级；网络预测塑性区更平滑。更平滑可能来自高阶连续网络，不能直接等同于更物理真实。（Figures 14–15）

## 6. 边坡稳定

20 m 高、45°坡、`E=20 MPa`、`ν=0.35`、`c=4 kPa`、`φ=10°`；位移最大误差约低一个数量级，等效压力/塑性应变场与 PD 参考接近。（Figures 16–18）

## 7. 计算效率

100 个案例、每个 2000 步；AMD 5950X CPU + RTX 3080 GPU。

| 材料点数 | OSB-PD | LPE |
|---:|---:|---:|
| 3,600 | ~200 s | ~10 s |
| 90,000 | ~3000 s | ~45 s |

作者概括约两数量级加速。（Figure 19）该比较未计数据生成、训练与硬件差异的总成本。

## 8. 有界结论

结果支持“在同源 OSB-PD 合成分布内的快速代理”，不支持“真实岩土本构已被发现”或“总研究成本始终低两个数量级”。

> 页面导航：[[zhou2025-learnable-physics-engine-analysis]] · [[zhou2025-learnable-physics-engine-method]] · [[zhou2025-learnable-physics-engine-critical]] · [[pinn]]