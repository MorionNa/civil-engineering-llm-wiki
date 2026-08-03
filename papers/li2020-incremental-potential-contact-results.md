---
id: paper--li2020-incremental-potential-contact-results
title: "Li et al. (2020) — IPC 结果与证据"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- contact-benchmark
- large-deformation
- scaling
- accuracy
- friction
sources:
- sources/papers/li2020-incremental-potential-contact.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# IPC 结果与证据

## 基础接触测试

IPC 通过了精确对齐点–点、平行边–边、狭缝贴合和 Erleben 接触测试。高速球以 10、100 和 1000 m/s 撞击 0.02 m 薄板，在 $h=0.02$ s 下均未发生 tunneling。^[sources/papers/li2020-incremental-potential-contact.md]

## 大变形与复杂障碍物

论文演示了：

- 海豚穿过紧窄无厚度漏斗；
- 薄体积垫与杆件持续扭转 100 s；
- 六面压缩器中的极端压缩与释放；
- 面、线段和点障碍物上的 codimensional contact；
- 软体集合被压过狭窄管道后重新分离。

这些算例在所用非反转材料能下保持无交叉、无反转。

## 摩擦证据

- 斜面块在 $\mu=0.5$ 时静止、$\mu=0.49$ 时滑动，与解析阈值一致；
- 20 m 高砌体拱和卡片屋在相应摩擦系数下维持稳定，降低摩擦后失稳；
- 滚轮与细杆算例重现 stick–slip；
- 高速/大变形摩擦案例通常只使用一次 lagging，因此摩擦方向与法向力幅值可能不完全一致。

## 时间步鲁棒性

扭转杆测试将时间步从 0.002 s 增至 2 s。算法在全部测试步长下完成求解，但过大步长显著增加单步非线性成本；大步长更适合作为强接触准静态平衡工具，而非高频动力学精确计算。

## 规模与性能

- 最高分辨率扭转 Armadillo：219K 节点、928K 四面体；
- 最大模型 squishy ball：688K 节点、2.314M 四面体、1.064M 表面三角形；
- 最繁忙算例每步最高约 498K 接触；
- 论文摘要报告总体测试覆盖至 2.3M 四面体和 498K contacts/time step。

标准体积模型中，迭代数随分辨率大致保持平坦，时间和内存近似线性增长；全部节点位于表面的薄垫模型则出现轻微超线性时间增长。

## 精度控制

IPC 分别控制：

1. 动力学残差 $\epsilon_d$；
2. 几何间隙 $\hat d$；
3. 静摩擦阈值 $\epsilon_v$。

论文测试材料刚度最高至 $2\times10^{11}$ Pa，并报告可求解至 $\epsilon_d=10^{-7}$ m/s、$\epsilon_v=10^{-8}$ m/s、$\hat d=1\ \mu$m；同时在更松容差下仍保持几何可行性。

## 加速与成本证据

CCD 的保守 CFL 过滤平均减少约 50% CCD 成本，对总模拟时间改善约 10%。精确有理数 CCD 比浮点实现约慢 30 倍，仅用于若干压力测试的后验检查。

## 对比边界

论文与 Verschoor–Jalba、SOFA、Houdini、COMSOL、ANSYS 及统一 SQP-type 实现进行比较，并报告其他方法在参数变化下的穿透、非收敛或漂移。需要注意，这些结论对应 2020 年版本、作者的场景设置与实现，不应直接外推到软件的后续版本。

## 关联页面

- [[li2020-incremental-potential-contact-analysis]]
- [[li2020-incremental-potential-contact-method]]
- [[li2020-incremental-potential-contact-critical]]
- [[entities/incremental-potential-contact]]
