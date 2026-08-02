---
id: paper--yu2024-xpbi-method
title: "Yu et al. (2024) — XPBI 方法"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- velocity-primary-xpbd
- kernel-gradient-correction
- implicit-return-mapping
- colored-gauss-seidel
sources:
- sources/papers/yu2024-xpbi.md
created: '2026-08-02'
updated: '2026-08-02'
confidence: high
---

# XPBI 方法

## 总体结构

XPBI 以粒子速度而非位置作为主要未知量。每个材料粒子携带变形梯度与本构状态，并由能量诱导的 XPBD 约束和塑性回映射共同更新。^[sources/papers/yu2024-xpbi.md]

## 1. 弹性能约束

作者采用 Hencky 应变形式的 StVK 能量，并把单粒子能量写成单个非线性约束 $C(F)=\sqrt{2\Psi(F)}$，顺应性取 $1/V^0$。该写法减少约束数量，并允许在主伸长空间内结合解析回映射。

## 2. 更新拉格朗日变形梯度

变形梯度按

$$F_p^{n+1}=(I+\Delta t\nabla v^{n+1}(x_p^n))F_p^n$$

更新。当前配置始终作为参考，因此无需保存初始网格拓扑。该步骤把问题转化为稳定估计速度梯度。

## 3. 平滑核梯度修正

采用 Wendland 核，并用重现一阶场的修正矩阵 $L_p$ 修正核梯度。矩阵求逆使用 SVD 伪逆，降低邻域缺失和病态邻域导致的数值不稳定。

## 4. 塑性内循环

在每次 XPBD 迭代中：

1. 根据当前速度估计试算变形梯度；
2. 通过本构回映射 $Z(\cdot)$ 投影至屈服面；
3. 用投影后的状态计算约束和乘子增量；
4. 更新速度并进入下一固定点迭代。

该设计把塑性放在隐式约束求解内部，而不是时间步末尾一次性处理。

## 5. 并行与稳定化

- 粒子邻域由均匀网格搜索重建；
- 使用 $2^d$ 颜色的 Gauss–Seidel 并行处理无依赖单元；
- XSPH 平滑抑制高刚度振荡；
- 点–点距离约束修正粒子聚集，并保持位置与变形梯度的一致性；
- 最终以同一后处理速度更新位置与持久变形梯度。

## 支持本构

论文演示 Von Mises、Drucker–Prager、非关联 Cam-Clay 与 Herschel–Bulkley，但算法接口本质上依赖“能量约束 + 回映射算子”，具有可替换本构结构。

## 假设与边界

方法依赖足够密集、分布合理的粒子邻域；固定点塑性收敛未被定量监控；大刚度仍需要适当小时间步和阻尼。

## 关联页面

- [[yu2024-xpbi-analysis]]
- [[yu2024-xpbi-results]]
- [[yu2024-xpbi-critical]]
- [[entities/xpbi]]