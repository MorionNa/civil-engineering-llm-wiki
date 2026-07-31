---
id: papers--wang2021-pinn-ntk-failure-results
title: Wang et al. (2021) PINN 失败机制 — 结果展开：四个 PDE 谱偏差验证
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
keywords:
- gradient-pathology
- pde-benchmarks
- physics-informed
- pinn
- spectral-bias
sources:
- sources/papers/wang2021-pinn-ntk-failure.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
---

# 结果展开：谱偏差实证与 NTK 退火效果

## 6.1 算例概览

| 算例 | PDE 类型 | 非线性 | 关键挑战 |
|------|----------|:---:|------|
| 1D Poisson | 椭圆 | ✗ | 基准，展示基本谱偏差 |
| 波动方程 | 双曲 | ✗ | 高频色散 |
| Burgers 方程 | 抛物+双曲 | ✓ | 激波间断 |
| Allen-Cahn | 抛物 | ✓ | 相界面演化 |

## 6.2 1D Poisson 方程（基准）

### 问题
$$-\frac{d^2u}{dx^2} = f(x), \quad x \in [0, 2\pi]$$

### 关键发现
| 方法 | L² 误差 | 训练时间 |
|------|:------:|:------:|
| 标准 PINN (uniform lr) | ~10⁻¹ | 发散 |
| 手动调 λ (经验搜索) | ~10⁻⁴ | 3000 iter |
| **NTK 自适应退火** | **~10⁻⁷** | **2000 iter** |

**核心证据：**
- 标准 PINN 下 $K_{bb}$ 特征值 ≈ 10³，$K_{rr}$ 特征值 ≈ 10⁻¹
- 收敛速率差 **4 个数量级**
- NTK 退火将 PDE 残差的学习率自动提升 ~10⁴ 倍

## 6.3 波动方程

### 问题
$$\frac{\partial^2 u}{\partial t^2} - c^2 \frac{\partial^2 u}{\partial x^2} = 0$$

### 关键发现
- 标准 PINN 无法捕获高频色散，解在短波长处严重失真
- NTK 退火后准确再现行波解，包括边界反射
- 时间域 PDE 中谱偏差更严重——$K_{00}$ 和 $K_{rr}$ 特征值均远小于 $K_{bb}$

## 6.4 Burgers 方程（非线性）

### 问题
$$\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} = \nu \frac{\partial^2 u}{\partial x^2}, \quad \nu = 0.01/\pi$$

### 关键发现
- 激波区域 (梯度 ≫ 1) 的残差对网络参数的梯度极小 → **局部谱偏差**
- 标准 PINN 在激波处解完全错误（光滑化或震荡）
- NTK 退火通过提升激波区域的有效学习率，准确捕获激波位置
- L² 误差: 标准 PINN ~0.5 → NTK 退火 ~0.02（25× 改进）

## 6.5 Allen-Cahn 方程

### 问题
$$\frac{\partial u}{\partial t} = \epsilon \frac{\partial^2 u}{\partial x^2} - \frac{1}{\epsilon}(u^2 - 1)u, \quad \epsilon = 0.01$$

### 关键发现
- 相界面处 (|u| < 1) PDE 残差敏感度高 → $K_{rr}$ 特征值在界面附近更高
- 标准 PINN 偏重界面外区域（梯度大），导致界面位置偏差
- NTK 退火 → 正确的界面移动速度和形状

## 6.6 NTK 特征值分析（定量）

| PDE | λ_max(K_rr) | λ_max(K_bb) | 比值 | 失败? |
|-----|:----------:|:----------:|:----:|:---:|
| 1D Poisson | 0.12 | 1380 | 1:11500 | ✓ 严重 |
| 波动方程 | 0.08 | 892 | 1:11150 | ✓ 严重 |
| Burgers (ν=0.01) | 0.03 | 645 | 1:21500 | ✓ 严重 |
| Allen-Cahn (ε=0.01) | 0.45 | 1230 | 1:2733 | △ 部分 |

## 6.7 消融研究

| 消融项 | 效果 |
|--------|------|
| 移除自适应学习率 | L² 误差 × 100–1000 |
| 仅调 λ (不基于 NTK) | 需 100+ 次试错 |
| 仅增加网络宽度 | 对谱偏差无效 |
| 增加配点数 | 边界条件主导更严重 |

## 页内导航

- [[wang2021-pinn-ntk-failure-analysis|← 总览]]
- [[wang2021-pinn-ntk-failure-method|← 方法]]
- [[wang2021-pinn-ntk-failure-critical|批判分析 →]]

## Evidence By Source

### `sources/papers/wang2021-pinn-ntk-failure.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_jcp_2021_110768.xml`

^[sources/papers/wang2021-pinn-ntk-failure.md]
