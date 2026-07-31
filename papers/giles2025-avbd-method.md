---
id: papers--giles2025-avbd-method
title: AVBD 方法机制展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
keywords:
- augmented-lagrangian
- hard-constraints
- high-stiffness-ratio
- primal-method
sources:
- sources/papers/giles2025-avbd.md
created: '2026-06-11'
updated: '2026-07-31'
confidence: high
---

# AVBD 方法机制

> 本文核心创新：将 VBD 的纯 primal 迭代扩展为 **primal-dual hybrid**，用 augmented Lagrangian 处理硬约束，用渐进刚度递增克服刚度比退化。

## 核心算法流程

```
每帧：
  1. 碰撞检测（BVH 宽/窄相） + 顶点着色
  2. 初始猜测 + warm-start (γ=0.99 缩放上帧 k, λ)
  3. for n iterations:
       for each color c:  (并行)
         对同色所有顶点 i:  (并行，Gauss-Seidel 序)
           构建本地 H_i f_i → 解 H_i⁻¹ f_i 更新位置
       for each force j:  (并行)
         更新 dual 变量 λ_j (Eq 11) + 刚度 k_j (Eq 12/16)
  4. 计算速度
```

与 VBD 的区别：多了标记为红色的部分——dual 变量初始化、dual/刚度更新步骤、硬约束的 Lagrange 项。

## 硬约束（Augmented Lagrangian）

原始 VBD 只能用二次势能 E = ½kC² 建模约束，k 大 → 收敛慢，k=∞ 不可行。

**AVBD 方案**（Eq 8）：
- 约束能量：E_j^(n) = ½ k_j^(n) C_j² + λ_j^(n) C_j
- k_j^(n)：迭代 n 时的**有限**刚度（从 k_start 起步）
- λ_j^(n)：Lagrange 乘子 / dual 变量，初始为 0
- 约束力：f_ij = -(k_j C_j + λ_j) · ∂C_j/∂x_i

**关键思想**：k 只是控制 dual 变量增长速度的"学习率"，收敛结果不依赖 k。即使 k 保持小值，λ 逐渐累积也能完美满足约束。

**Dual 更新**（Eq 11）：λ^(n+1) = k^(n) C_j(x) + λ^(n)
**刚度更新**（Eq 12）：k^(n+1) = k^(n) + β|C_j(x)|，β=10（不敏感，β∈[1,1000] 效果类似）

## 不等式约束 & 摩擦接触

通过 clamp Lagrange multiplier 实现 force bound：

- 定义 λ⁺ = k C_j + λ（Eq 13）
- Clamp：λ_min ≤ λ⁺ ≤ λ_max（Eq 14 的 stiffness rescaling 修正 Hessian）
- 刚度只在约束未饱和时递增（Eq 12 仅在 λ_min < λ⁺ < λ_max 时生效）

**摩擦接触**（Eq 15）：3D 约束 C = [t̂ b̂ n̂]^T (r_a - r_b)
- 法向：λ_n ≥ 0（只推不拉）
- 切向（摩擦）：||λ_tb|| ≤ μ λ_n（Coulomb friction cone）
- 支持静/动摩擦系数切换：上帧 ||λ_tb|| < μ_s λ_n → 静摩擦 μ_s，否则动摩擦 μ_d

## 高刚度比问题

**问题根源**：VBD 逐顶点 Gauss-Seidel 时，局部解偏向最陡梯度（即最硬力），弱力信息无法全局传播（Fig 2a-d）。

**解决方案**（Eq 16）：对有限刚度力也使用渐进递增——
k^(n+1) = min(k*, k^(n) + β|C_j|)

早期用小 k（降低有效刚度比）→ 弱力有机会传播 → 逐步提升 k 到实际值 k* → 收敛到精确解。

## Hessian 近似

硬约束的 Hessian 包含非正定项 G_ij（constraint 二阶导 × λ⁺），可能导致系统不可逆。

**解决方案**：用 G_ij 各列的 norm 构成对角近似 G̃_ij = diag(||G_ij,c||)，保证正定对称 → 可用高效 LDL^T 分解。本质是 quasi-Newton step。

## 防爆裂修正 (α)

硬约束在低迭代数下可能被违反 → 下帧会施加极大修正力注入动能。

**解决方案**（Eq 18）：C_j(x) = C_j*(x) - α C_j*(x_t)，α=0.95

忽略上帧残留误差的 95%，在多个帧内逐步消解（类似 Baumgarte stabilization）。

## Warm-start (γ)

将上帧收敛后的 k 和 λ 缩放后作为当前帧初始值（Eq 19）：

k^(0) = max(γ k_t, k_start)，λ^(0) = α γ λ_t，γ=0.99

注意：γ 必须 <1，否则 k 只增不减，可能锁死在未来不需要大 k 的帧。λ 额外乘 α 避免把上帧残留误差的能量带入 warm-start。

## 参数表

| 参数 | 范围 | 默认值 | 作用 |
|------|------|--------|------|
| β | (0,∞) | 10 | 刚度递增速率 |
| α | [0,1] | 0.95 | 残留误差消解比例 |
| γ | [0,1) | 0.99 | warm-start 保留比例 |
| k_start | >0 | — | 初始刚度（不敏感） |

## 并行化

与 VBD 相同：greedy vertex coloring（着色数远少于 XPBD 的 constraint coloring）。dual update 也对所有约束并行执行。仅增加一个 all-constraints parallel pass。

## 关联页面
- [[giles2025-avbd-analysis]] — 全维度概述
- [[giles2025-avbd-results]] — 实验结果
- [[giles2025-avbd-critical]] — 贡献 + 局限性 + 可迁移

## Evidence By Source

### `sources/papers/giles2025-avbd.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/giles2025-avbd.md`

^[sources/papers/giles2025-avbd.md]
