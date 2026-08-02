---
id: paper--yu2024-xpbi-results
title: "Yu et al. (2024) — XPBI 结果"
type: paper-results
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- scalability
- continuum-materials
- convergence
- real-time-interaction
sources:
- sources/papers/yu2024-xpbi.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# XPBI 结果

## 材料覆盖

论文展示 Von Mises 塑性面条与金属、Drucker–Prager 砂、NACC 雪与脆性断裂、Herschel–Bulkley 剪切变稀/变稠材料，并与布料和位置流体耦合。^[sources/papers/yu2024-xpbi.md]

## 与基线比较

- 相比点摩擦式 vanilla XPBD，XPBI 能更准确重现砂堆摩擦角与连续介质形态；
- 与 MPM 相比，XPBI 在砂碰撞与塌落中保持更均匀的粒子间距，避免明显聚集和网格间隙；
- 全隐式塑性避免半隐式时间步末回映射导致的过度弹性和拉伸伪影；
- 与 Gissler 等半隐式雪模型相比，XPBI 在 $10^{-4}$ s 与 $10^{-3}$ s 时间步下给出更一致的行为。

## 收敛证据

悬臂梁算例比较 $E=10^4,10^5,10^6$ Pa。着色 Gauss–Seidel 在高刚度和较大时间步下稳定收敛，而 Jacobi 在高刚度时表现较差。论文因此在大规模高刚度场景中采用着色 Gauss–Seidel。

## 规模与性能

| 场景 | 最大粒子数 | 平均秒/帧 |
|---|---:|---:|
| Noodles | 1.18M | 46.3 |
| Cloth coupling | 1.10M | 24.3 |
| Camponotus fracture | 1.12M | 37.3 |
| Dam breach | 4.00M | 138.8 |
| Hourglass | 1.01M | 30.9 |
| Hitman snow | 1.05M | 38.9 |
| Snow dive | 2.48M | 78.2 |
| Wrist VR | 20K | 0.015 |

缩放实验从 8K、56K、400K 到 3M 粒子，平均每粒子计算时间依次约为 0.30、0.098、0.058、0.037 ms，说明更大规模能更充分利用 GPU。

## 时间开销组成

Hourglass 案例中，非弹性约束求解占主要开销；邻域搜索、碰撞检测、XSPH 和状态更新占较小但不可忽略的比例。时间步过大需要更多 GS 迭代，过小则放大每步固定开销，作者实践选择 $5\times10^{-5}$–$2\times10^{-4}$ s。

## 结果边界

这些性能数值来自 RTX 4090 和特定实现；多数高分辨率案例不是实时。结果主要证明图形学可用性、稳定性和尺度扩展，不构成工程材料试验标定或守恒误差验证。

## 关联页面

- [[yu2024-xpbi-analysis]]
- [[yu2024-xpbi-method]]
- [[yu2024-xpbi-critical]]
