---
title: "HCFF-PINN — 频率先验 Fourier 特征与初值硬约束 PINN"
created: 2026-07-16
updated: 2026-07-16
type: entity
tags: [physics-informed, pinn, neural-network, deep-learning, hard-constraint-strategies, auxiliary-function, hard-constraints, structural-dynamics, seismic-response, equation-of-motion, vibration-analysis]
sources: [raw/papers/10_1016_j_engappai_2025_113640.xml, raw/papers/extracted/10_1016_j_engappai_2025_113640_extracted.txt]
confidence: high
---

# HCFF-PINN

## 定义

HCFF-PINN（Hard Constraints and Fourier Features PINN）是 Du et al.（2026）提出的线性结构动力响应求解框架。它把两类增强组合起来：

1. **频率先验 Fourier features：** 用结构自振频率设置 Fourier 映射尺度，增强多频与高频表示。
2. **初值硬约束：** 用 $u(t)=\tanh^2(t)N(t;\theta)$ 自动满足 $u(0)=\dot u(0)=0$，删除 IC loss。

原始论文：[[du2026-hcff-pinn-analysis]]。

## 数据流

```text
t
├─ cos(Bt), sin(Bt),  B ~ N(0, σ²), σ ← 结构自然频率
└─ Fourier-feature FNN → N(t;θ)
                         ↓
                u(t)=tanh²(t)N(t;θ)
                         ↓ AD
                   u_dot(t), u_ddot(t)
                         ↓
             M u_ddot + C u_dot + K u - P(t)
                         ↓
                   only ODE loss
```

## “label-free”的边界

HCFF-PINN 不再使用初值标签和初值损失，因此相对标准 [[pinn]] 是 label-free。它仍需要结构 $M,C,K$、已知激励 $P(t)$ 和配点；验证还需要 Newmark-$\beta$ 参考解。因此不能把 label-free 解释成“无需输入数据或物理模型”。

## 与相关方法的关系

| 方法 | 共同点 | 关键区别 |
|---|---|---|
| [[at-pinn-hc]] | 都把初值/边界条件写入解形式 | AT-PINN-HC 强调时间推进和多类辅助函数；HCFF-PINN 加入模态频率 Fourier 编码且整段时域训练 |
| [[neural-tangent-kernel]] 调权 | 都关注 PINN 收敛病态 | NTK 调权保留 IC/ODE 多损失；HCFF-PINN 直接删除 IC loss |
| FF-PINN | 都用 Fourier features | FF-PINN 仍有软初值损失；HCFF-PINN 增加 $\tanh^2$ 硬约束 |

## 已验证能力

- 谐波载荷下线性 SDOF；
- 四类真实地震动下线性 3-DOF 剪切框架；
- 静力凝聚为 20 DOF 的四层线性钢框架；
- 近似频率与频率子集的鲁棒性。

数值详见 [[du2026-hcff-pinn-results]]。

## 未验证能力

- 塑性、损伤、滞回或任何非线性恢复力；
- 非零初位移/初速度的通用硬约束；
- 复杂空间边界和未经凝聚的大型有限元系统；
- 现场噪声、参数不确定性和实测结构响应。

## 使用原则

1. 先以模态分析或简化模型估计主导频带，再设置 $\sigma$。
2. 验证 $g(0)=g'(0)=0$ 只是第一步，还要检查 $g(t)$ 在整个时域有界且梯度稳定。
3. 同时报告时域、频域和分频带误差。
4. 非线性结构必须重新识别随状态变化的频率并嵌入本构方程，不能直接继承本文结论。

## 关联页面
- [[du2026-hcff-pinn-analysis]] — 12 维论文分析
- [[du2026-hcff-pinn-method]] — Fourier 与硬约束机制
- [[du2026-hcff-pinn-critical]] — 局限与研究机会
- [[pinn]] — 基础 PINN 实体
