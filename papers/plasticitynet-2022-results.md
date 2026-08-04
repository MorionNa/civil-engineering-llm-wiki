---
id: paper--plasticitynet-2022-results
title: "Li et al. (2022) — PlasticityNet 结果"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
keywords:
- sand
- snow
- metal
- bfemp
- timestep
sources:
- sources/papers/plasticitynet-2022.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# PlasticityNet 结果与证据

## 1. 实验配置

所有目标数据由解析回映射配合小时间步显式积分生成。神经势在单张 RTX 3090 上训练，并嵌入 C++ FEM/MPM 求解器。^[sources/papers/plasticitynet-2022.md]

## 2. 二维计算成本

|案例|PlasticityNet 时间步|PlasticityNet 秒/帧|显式时间步|显式秒/帧|
|---|---:|---:|---:|---:|
|砂柱|1e-3 s|12.58|1e-5 s|6.20|
|雪球|1e-3 s|35.56|1e-5 s|6.78|
|StVK + von Mises 金属|1e-2 s|1.08|1e-5 s|5.39|
|Neo-Hookean + 金属|1e-2 s|1.03|1e-5 s|7.88|
|MPM–FEM 耦合|1e-3 s|38.90|1e-6 s|184.58|

这张表说明“大时间步”与“单帧更快”不是同一概念：砂雪隐式单帧更贵，但金属和 BFEMP 因显式稳定步极小而获得墙钟优势。

## 3. 砂与雪

- StVK + Drucker–Prager 砂柱在相同步长和放大 100 倍步长下均与显式参考视觉接近；
- Neo-Hookean + 非关联 Cam-Clay 雪在大步长下保持稳定，但数值阻尼增加，行为与参考逐渐偏离；
- IoU 曲线用于比较 MPM 网格质量分布。

## 4. 金属

- StVK + von Mises 金属框架在 FEM + IPC 中承受压板；
- PlasticityNet 可使用原始高刚度和 1e-2 s 步长，而显式参考为可完成计算而降低 Young 模量；
- Neo-Hookean 弹性下没有闭式 von Mises 回映射，学习投影避免逐单元非线性求根，并产生定性相近结果。

## 5. BFEMP 耦合

刚性 FEM 弹性体落入 MPM 砂体时，隐式 PlasticityNet–BFEMP 使用比显式 BFEMP 大 1000 倍的时间步，报告约 5 倍墙钟加速；小步长显式 MPM 还因频繁粒子–网格传递表现出更强耗散。

## 6. 表示消融

- 全局 $\Psi(F)$：砂柱表现为弹性体，初始帧收缩并跳起；
- 只在单位阵做修正：仍不能捕捉塑性；
- 使用 $F_0$ 但修正点错误：小变形可用，大变形快速偏离；
- 最终的展开点精确修正形式获得正确结果。

## 7. 稳定性消融与三维

无正则项时金属框架首步即离开静止构型，砂柱出现粒子非物理分离。论文还展示 3D 砂、雪、金属；金属步长为 1e-2 s，砂雪为满足 MPM CFL 使用 1e-3 s。

## 8. 证据边界

结果基于数值参考和图形学任务，不包含真实材料实验标定、统计误差条或结构工程尺度验证。论文目标是证明优化积分兼容性，而非证明所有材料都比专用显式求解器更快。

## 关联页面

- [[plasticitynet-2022-analysis]]
- [[plasticitynet-2022-method]]
- [[plasticitynet-2022-critical]]
- [[entities/plasticitynet]]
