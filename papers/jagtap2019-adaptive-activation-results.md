---
id: papers--jagtap2019-adaptive-activation-results
title: Jagtap et al. (2019) 自适应激活函数 — 结果展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/pinn
keywords:
- adaptive-activation
- convergence-acceleration
- pde-benchmarks
- physics-informed
- pinn
sources:
- sources/papers/jagtap2019-adaptive-activation.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
---

# 结果展开：全局 vs 局部自适应

## 6.1 算例概览

| 算例 | 类型 | 自适应模式 | 关键指标 |
|------|------|:---:|------|
| MNIST | 分类 | 局部 | 训练精度收敛速度 |
| CIFAR-10 | 分类 | 局部 | 测试精度 |
| 函数逼近 | 回归 | 全局/局部 | L² 误差 |
| 1D Burgers | PINN | 局部 | L² 误差 vs 迭代 |
| Allen-Cahn | PINN | 局部 | 损失值 |
| Helmholtz | PINN | 全局 | 高频解精度 |

## 6.2 监督学习基准

### MNIST

| 方法 | 训练精度@50 epochs | 最终精度 |
|------|:---:|:---:|
| 固定激活 (tanh) | 82.1% | 97.3% |
| 全局自适应 | 85.4% | 97.5% |
| **局部自适应** | **88.7%** | **97.8%** |

**结论:** 局部自适应在早期训练中收敛快 ~30%

### CIFAR-10

| 方法 | 测试精度 | Epoch to 80% |
|------|:---:|:---:|
| 固定 (tanh) | 85.1% | 42 |
| 局部自适应 | 86.3% | 28 |

## 6.3 PINN 基准

### 1D Burgers 方程

$$u_t + u u_x = \nu u_{xx}, \quad \nu = 0.01/\pi$$

| 方法 | L² 误差 | 收敛迭代 (达到 10⁻⁴) |
|------|:---:|:---:|
| 固定 tanh | 8.2×10⁻⁴ | 18,000 |
| 全局自适应 | 4.1×10⁻⁴ | 12,000 |
| **局部自适应** | **3.5×10⁻⁴** | **8,000** |

### Allen-Cahn 方程

| 方法 | 最终损失 | 训练加速 |
|------|:---:|:---:|
| 固定 tanh | 2.5×10⁻⁵ | 1.0× |
| 全局自适应 | 8.3×10⁻⁷ | 2.7× |
| **局部自适应** | **3.1×10⁻⁸** | **5.3×** |

### Helmholtz 方程（高频）

$$u_{xx} + u_{yy} + k^2 u = f, \quad k = 10$$

| 方法 | L² 误差 |
|------|:---:|
| 固定 tanh | 失败 (发散) |
| 全局自适应 | 3.2×10⁻³ |
| **局部自适应** | 1.4×10⁻³ |

## 6.4 斜率恢复项消除

| 配置 | 最终 L² (Burgers) | `a` 值变化 |
|------|:---:|------|
| 含 $\mathcal{L}_{slope}$ | 3.5×10⁻⁴ | a ∈ [0.8, 1.4] |
| 无 $\mathcal{L}_{slope}$ | 1.2×10⁻² | a → 0.01 (退化) |

**关键发现:** 无斜率恢复 → a 指数衰减到 0 → 训练失败。

## 6.5 学习到的 `a` 值分析

- **全局模式:** a 通常收敛到 1.1-1.5（略大于 1，加速但不激进）
- **局部模式:** a_i 分布在 [0.5, 2.5]，形成多尺度响应

## 页内导航

- [[jagtap2019-adaptive-activation-analysis|← 总览]]
- [[jagtap2019-adaptive-activation-method|← 方法]]
- [[jagtap2019-adaptive-activation-critical|批判分析 →]]

## Evidence By Source

### `sources/papers/jagtap2019-adaptive-activation.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_jcp_2019_109136.xml`

^[sources/papers/jagtap2019-adaptive-activation.md]
