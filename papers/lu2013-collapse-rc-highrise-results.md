---
id: papers--lu2013-collapse-rc-highrise-results
title: Lu et al. (2013) 倒塌模拟结果展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
keywords:
- collapse-simulation
- high-rise-building
- seismic-response
sources:
- sources/papers/lu2013-collapse-rc-highrise.md
created: '2026-06-11'
updated: '2026-07-31'
confidence: high
---

# RC 高层倒塌模拟：三组算例结果

> 所有算例使用 El-Centro EW 1940 或 Duzce 1999 地震动，缩放到 PGA 远大于设计水准（1500–4000 gal）。隐式 Houbolt 算法求解，残差力 < 1% 最大反力收敛。

## 算例 1：10 层 RC 框架 (El-Centro, PGA=2000gal)

| 参数 | 值 |
|------|-----|
| 层高 | 首层 4.5m，其余 3m |
| 跨度 | 5m×3 跨 |
| 柱截面 | 700→600→500mm（3 段变截面） |
| 混凝土 | E₀=30GPa, fc=30MPa |
| 钢筋 | Es=200GPa, fy=400MPa |

**倒塌过程**（Fig 21）：

```
t=2.0s  框架弹塑性变形，柱钢筋开始屈服
t=3.0s  第8层柱（600→500mm截面变化处）失效加重
t=4.0s  首层和第8层形成软弱层，P-Δ效应明显
t=4.4s  首层+第8层完全倒塌，极大大位移
```

**机制**：柱截面变化处 = 刚度突变 = 应力集中 = 弱层。首层受最大侧向力，第 8 层受截面削弱。两者**同时失效**构成"双弱层"倒塌模式。

---

## 算例 2：18 层框筒 (El-Centro, PGA=1500gal)

| 参数 | 值 |
|------|-----|
| 高度 | 74.8m（+4 层地下室） |
| 核心筒 | 4 个子筒体 + 连梁，壁厚 500mm→350mm |
| 模态 | T1=1.55s(Y向平移), T2=1.30s(扭转), T3=1.15s(X向平移) |

**倒塌过程**（Fig 23）：

```
t=0.0s  初始状态
t=3.9s  首层核心筒外翼缘混凝土压碎
        （原因：轴力+倾覆弯矩，压溃主导，非剪切破坏）
t=4.9s  力重分布→周边柱轴力骤增→柱屈曲
t=6.8s  地下室与上部结构碰撞→整体倒塌
```

**关键洞察**：
1. 首层为弱层的原因：首层层高（远大于标准层）→ 最大 P-Δ 效应
2. 核心筒外翼缘先于内翼缘失效：倾覆弯矩使远轴翼缘受压最大
3. 失效链：**核心筒压溃 → 力重分布到柱 → 柱屈曲 → 碰撞倒塌**

---

## 算例 3：20 层框筒 — 双地震动对比

| 参数 | 值 |
|------|-----|
| 高度 | 79.47m |
| 柱截面 | 800→700→600mm |
| 核心筒 | 壁厚 350mm 不变 |
| 模态 | T1=2.25s(Y), T2=2.02s(X+扭转), T3=1.63s(扭转) |

**El-Centro (PGA=4000gal)** → Fig 24：
```
t=4.5s  第10层核心筒外翼缘压碎
        （触发点：混凝土强度 C40→C30 + 柱 700→600mm）
t=5.1s  柱屈曲
t=7.5s  第10层以上坠落→撞击下部→连续倒塌
```

**Duzce (PGA=4000gal)** → Fig 25，完全不同的倒塌模式：
```
t=14.5s  首层剪力墙受弯失效 + 柱出现塑性铰
t=15.5s  地下室与上部碰撞
t=16.3s  首层侧向倒塌
```

**双地震动差异原因**：
| | El-Centro 1940 | Duzce 1999 |
|---|---|---|
| 类型 | 持时型 | 脉冲型 |
| 弱层 | 第 10 层（刚度变化处） | 首层（地下连续墙中断） |
| 激发振型 | 高阶 | 低阶 |
| 倒塌时间 | 7.5s | 16.3s |

> **不同频率成分的地震动激发不同振型 → 暴露不同弱层 → 不同倒塌模式。** 抗震设计不能仅靠单一地震动评估。

---

## 失效准则敏感性 (FEMA P695, 22 条远场地震)

| 失效准则组合 | 倒塌概率 |
|------|:--:|
| 拉断 15% + 屈曲 1.0% | 63.6% |
| 拉断 10% + 屈曲 1.0% | 63.6% |
| 拉断 15% + 屈曲 0.5% | **81.8%** |

- **钢筋受拉断裂应变 (10%→15%) 基本无影响**
- **钢筋屈曲应变 (0.5%→1.0%) 影响倒塌概率 ~18 个百分点**
- 原因：框筒倒塌由混凝土压溃触发，压溃后纵筋屈曲直接决定残余承载力

## 关联页面
- [[lu2013-collapse-rc-highrise-analysis]] — 全维度概述
- [[lu2013-collapse-rc-highrise-method]] — 方法机制
- [[lu2013-collapse-rc-highrise-critical]] — 贡献 + Negative + 可迁移

## Evidence By Source

### `sources/papers/lu2013-collapse-rc-highrise.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/lu2013-collapse-rc-highrise.md`, `raw/papers/10_1002_eqe_2240.pdf`

^[sources/papers/lu2013-collapse-rc-highrise.md]
