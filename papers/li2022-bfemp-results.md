---
id: paper--li2022-bfemp-results
title: "Li et al. (2022) — BFEMP 结果"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- momentum-conservation
- hertz-contact
- friction-threshold
- refinement-convergence
- three-dimensional-twist
sources:
- sources/papers/li2022-bfemp.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# BFEMP 结果

## 数值证据概览

论文提供 6 个二维算例与 1 个三维算例，覆盖动量/能量、边界分离、接触精度、静滑摩擦转变、网格细化、摩擦屈曲与三维扭转。^[sources/papers/li2022-bfemp.md]

## 碰撞环

MPM 环和 FEM 环以 40 m/s 相向碰撞。APIC 与 FLIP 均完全保持系统总动量；碰撞后总能量损失分别为 8.57% 和 9.67%。分离后 FEM 能量保持，而 MPM 能量继续因粒子–网格传递耗散下降。

## FEM 作为 MPM 边界

正弦形 FEM 边界压缩、平移并离开 MPM 方块。BFEMP 保持不穿透且分离时无数值黏附；传统 level-set 网格滑移边界出现穿透和黏附。

## Brazilian disk

细网格下，线弹性与 Neo-Hookean 结果在小变形范围内与 Hertz 接触力–接触半径关系吻合。低分辨率中半径测量呈阶梯状，随分辨率提高得到缓解。

## 临界摩擦系数

斜坡算例测试 $\mu=0,0.1,0.1999,0.2$。速度和加速度与解析解的相对误差均低于 0.01%；在临界值 $\mu=0.2$ 时加速度消失，残余速度受 $\epsilon_v$ 控制。

## 细化收敛

以 $\Delta x=1/N$、$\hat d=1/N^2$ 细化 MPM 与 FEM。高 PPC 降低曲线噪声；PPC=16 时相对于高分辨率参考解的拟合收敛阶约为 2.75。

## 摩擦屈曲

双半圆环压缩中，$\mu=0$ 最早屈曲，$\mu=0.2$ 延迟屈曲，$\mu=0.5$ 在测试位移范围内不发生屈曲，说明接触摩擦可显著改变失稳路径。

## 三维扭转

90,929 个 MPM 粒子的立方体与 3,920 个四面体的 FEM 球壳接触。滑移角随摩擦增大而增加：$\mu=0.2$ 约在 $0.3\pi$，$\mu=0.5$ 约在 $0.7\pi$，$\mu=1.0$ 未滑移。无摩擦时的残余转角来自离散界面粗糙度，并随分辨率提高减小。

## 解释边界

- Hertz 对比主要是定性至半定量的小变形验证；
- 收敛阶依赖同步缩小 $\hat d$、较高 PPC 和所选误差指标；
- 动量保持不代表能量守恒，MPM 传递耗散仍显著；
- 三维验证仅包含一个接触扭转问题；
- 论文没有提供 RC 构件、断裂或碎片接触验证。

## 关联页面

- [[li2022-bfemp-analysis]]
- [[li2022-bfemp-method]]
- [[li2022-bfemp-critical]]
