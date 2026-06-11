---
title: "AVBD 实验结果展开"
created: 2026-06-11
updated: 2026-06-11
type: concept
tags: [rigid-body-dynamics, constraint-solver, gpu-computing]
sources: [raw/papers/giles2025-avbd.md]
confidence: high
---

# AVBD 实验结果

> 对比对象：VBD、XPBD (iterations/substeps)、Sequential Impulse。所有实验 Δt=1/60s，参数固定。

## 实验 1：高刚度比 — 交替弹簧块 (Fig 2 & 4)

10 个 block 由交替刚度（ratio=10,000）的弹簧连接。**AVBD 1 iter > VBD 100 iter**。

| 方法 | 迭代/子步数 | 结果 |
|------|:--:|------|
| VBD | 5 iter | 弱弹簧过度拉伸 |
| VBD | 100 iter | 改善但仍明显 |
| VBD | 30 substeps | 接近收敛 |
| AVBD | **5 iter** | 与参考解视觉无差别 |
| AVBD | 1 iter + warm-start | 与 5 iter 同等效果 |

**结论：** 渐进刚度递增 + warm-start 根本性解决了 VBD 的刚度比退化。

## 实验 2：硬约束 — 旗杆 (Fig 5)

1500 顶点 + 6000 弹簧的旗子，通过硬约束固定在由 20 个刚体段组成的可变形旗杆上。

| 方法 | 迭代数 | 结果 |
|------|:--:|------|
| VBD | 20 | 旗杆过度拉伸 |
| AVBD | **5** | 硬约束维持，旗杆合理弯曲 |
| AVBD | 20 | 动画质量进一步提升 |

**结论：** AVBD 即使低迭代数也能维持硬约束，VBD 无法。

## 实验 3：高绝对刚度 — 纸牌塔 (Fig 6)

超轻纸牌塔需要极高静态摩擦力维持。AVBD 用硬约束 → 不需要高 k 值 → 球撞到后正确倒塌。VBD 的高 k 使动能项被势能项淹没 → 纸牌"变重"，球被弹开。

## 实验 4：高质量比 — 50 体摆锤链 (Fig 7, 8, 9)

50 刚体 + 球关节连接 + 末端重物（50,000:1 质量比）。

| 方法 | 配置 | 结果 |
|------|------|------|
| AVBD | 20 iter | 约束误差稳定低值 ✅ |
| AVBD | 5 iter | 少量拉伸，仍可接受 |
| VBD | 20 iter | 明显拉伸 |
| VBD | 5 iter | 严重拉伸 |
| XPBD | 20 substeps | 拉伸 + 高质量比不稳定振荡 |
| XPBD | 50 iter | 完全失败，摆锤坠地 |
| Seq Imp | 50 iter | 无法产生摆动 |

**约束误差曲线** (Fig 8)：AVBD 20 iter 约束误差始终最低且无振荡，XPBD 有明显振荡。

**双球 + 链** (Fig 9)：dual 方法 (XPBD/Seq Imp) 因质量比直接崩溃，AVBD 保持链长，VBD 有过度拉伸。

## 实验 5：碰撞 & 堆叠 — 锁子甲 (Fig 12)

重球坠落锁子甲。

| 方法 | 15 iter/substeps | 结果 |
|------|------|------|
| AVBD | 15 iter | **所有接触维持**，无视觉伪影 ✅ |
| Seq Imp | 15 iter | 球穿过锁子甲 |
| XPBD | 15 substeps | 球附近接触维持，角落失效 |
| VBD | 15 iter | 角落接触在球碰到前已失效 |

**原因**：AVBD 硬约束能产生任意大力维持接触；VBD 二次势能不能产生足够约束力。

## 实验 6：破墙 (Fig 13)

砖墙由可断裂硬约束连接，三个重球撞击。

| 方法 | 结果 |
|------|------|
| AVBD | 正确断裂 + 残留约束维持 ✅ |
| Seq Imp | 初始断裂后整体弯曲倒塌 |
| XPBD | 橡胶状撕裂，不自然断裂位置 |
| VBD | 不折断，整面墙弯曲 |

## 实验 7：摩擦行为 (Fig 11)

不同摩擦系数的方块在平面上滑行至停止。AVBD stiffness rescaling 方案 1 iter 即可匹配 Seq Imp 4 iter 的摩擦行为。

## 实验 8：大规模性能 (Table 1, Fig 1 & 3)

GPU (RTX 4090)，所有方法参数以场景不崩溃的最小迭代数。

| 场景 | 方法 | 迭代/子步 | 耗时 | 备注 |
|------|------|:--:|------|------|
| **110k blocks** | AVBD | 4 iter | **3.5ms** | 稳定堆叠 |
| (Fig 1) | Seq Imp | 15 iter | 14.1ms | |
| | XPBD | 6 sub | 19.5ms | |
| | VBD | 15 iter | 10.8ms | |
| **510k blocks** | AVBD | 3 iter | **10.3ms** | 稳定堆叠 |
| (Fig 3) | Seq Imp | 27 iter | 78.4ms | |
| | XPBD | 26 sub | 524.7ms | 仍塌陷 |
| | VBD | 8 iter | 26.5ms | |

**关键洞察**：AVBD 的性能优势主要来自 **更低的所需迭代数**，而非每迭代计算量。XPBD 在 510k 场景甚至 26 substeps 后仍塌陷——稳定性是决定相对性能的首要因素。

## 实验 9：参数敏感性 (Fig 15, Table 2)

50 体摆锤链 quasi-static 测试：

- **β**（刚度递增速率）：quasi-static 场景下 warm-start 主导，β 影响小。过大可能过度硬化。
- **α**（残留误差消解）：α=0 → 爆裂修正；α=1 → 误差累积（需 post-stabilization）。α=0.95 平衡最优。
- **γ**（warm-start 保留）：γ=0 → 无 warm-start，收敛差（链坠地）。γ=0.99 最优。γ=1 无效（不允许刚度下降）。

## 关联页面
- [[giles2025-avbd-analysis]] — 全维度概述
- [[giles2025-avbd-method]] — 方法机制
- [[giles2025-avbd-critical]] — 贡献 + 局限性 + 可迁移
