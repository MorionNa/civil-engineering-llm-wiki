---
id: paper--feng2026-mpm-lite-results
title: "Feng et al. (2026) — MPM Lite 结果证据"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- explicit-mpm
- implicit-mpm
- ppc-scaling
- performance
- material-versatility
sources:
- sources/papers/feng2026-mpm-lite.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
evidence_scope: full-text
---

# 结果与证据

## 显式 Jelly 对比

含 114 万粒子的 Jelly 算例运行 3 s、120 fps、$\Delta x=1/256\,\mathrm m$。传统 MPM、MLS-MPM、CK-MPM 和 MPM Lite 总耗时分别为 404.1、389.3、247.7 和 215.4 s；MPM Lite 相对传统 MPM 加速 1.88 倍。^[sources/papers/feng2026-mpm-lite.md]

## 隐式弹性与能量行为

不同刚度悬臂梁的静态挠曲与理论主曲线、传统隐式 MPM 保持一致。振荡果冻和悬臂梁的总能量耗散曲线与传统隐式 MPM 几乎重合，说明性能提升未明显改变所比较场景的数值耗散。

## 隐式与显式砂体

同一 Drucker–Prager 坍落砂算例中，显式时间步 $10^{-5}$ s、总耗时 431.7 s；隐式时间步 $10^{-3}$ s、总耗时 72.3 s，获得 5.97 倍加速。

## PPC 扩展性

扭转玩具在 PPC 为 8、12、16、20、24 时，MPM Lite 总耗时约为 63.5、68.1、70.5、72.8、77.1 s；传统隐式 MPM 则从 300.3 增至 1225.4 s。对应加速比从 4.7 倍升至 15.9 倍，直接支持“网格求解阶段与 PPC 解耦”的核心主张。

## 与 VBD 耦合

双材料扭转杆 5 s 仿真中，Newton-PCG 耗时 401.7 s，VBD 耗时 197.1 s，约 2 倍加速，形变行为视觉上相近。该结果说明固定六面体积分结构可复用现成优化求解器。

## 百万粒子材料算例

- 522–523 万粒子超弹性玩具：VBD，约 3.70 s/frame；文中另报告 0.22 s/time step，较 $\Delta t=10^{-5}$ s 的显式替代方案快 11.8 倍；
- 289 万粒子挤压面条：von Mises 塑性；
- 204 万粒子蚂蚁糖果：NACC 脆性断裂；
- 804 万粒子滚雪球：雪塑性；
- 193 万粒子砂水：Drucker–Prager + 基于 $J$ 的水模型；
- 123 万粒子金属轮：$E=10^8$ Pa 的 von Mises 塑性；
- 244 万粒子奶油：Herschel–Bulkley 黏塑性。

## 塑性、守恒与内存

固定点全隐式塑性正确形成砂土摩擦锥，半隐式“Newton 后再回映”方案产生错误砂堆。两弹性立方体碰撞的总线动量最大绝对值为 $7.11\times10^{-15}$ kg·m/s；旋转杆角动量相对误差为 $1.02\times10^{-4}$。隐式求解器内存主要随网格分辨率而非 PPC 增长。

## 解释边界

- 所有性能来自 RTX Pro 6000 + Intel i9-9980XE 的特定实现与场景；
- “视觉一致”不等同于严格误差等价；
- 材料覆盖证明框架兼容性，不代表每一类本构均完成工程级标定；
- 高 PPC 加速主要来自隐式积分阶段，完整流程仍包含粒子相关成本；
- 论文报告的薄结构、弯曲和强子单元变化偏软问题不应被性能结果掩盖。

## 关联页面

- [[papers/feng2026-mpm-lite-analysis]]
- [[papers/feng2026-mpm-lite-method]]
- [[papers/feng2026-mpm-lite-critical]]
- [[entities/mpm-lite]]
