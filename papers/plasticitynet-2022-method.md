---
id: paper--plasticitynet-2022-method
title: "Li et al. (2022) — PlasticityNet 方法"
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- domain/ai4s
- evidence/paper
keywords:
- local-potential
- gradient-matching
- return-mapping
- fixed-point-iteration
sources:
- sources/papers/plasticitynet-2022.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
---

# PlasticityNet 方法

## 1. 优化时间积分背景

无塑性时，若 $P(F)=\partial\Psi/\partial F$，隐式 Euler 可写为质量惯性项与材料势能之和的最小化问题。线搜索使刚性材料和大时间步下的求解比直接非线性方程更稳健。^[sources/papers/plasticitynet-2022.md]

## 2. 塑性力的可积性障碍

有限应变塑性写作 $F=F_EF_P$，试算弹性变形经回映射 $Z(F_E^{tr})$ 投影。目标应力场

$$G(F)=\tau(Z(F))F^{-T}$$

通常 Jacobian 非对称，因此不存在全局势满足 $\partial\Psi/\partial F=G(F)$。

## 3. 局部势能族

PlasticityNet 学习 $\Psi(F,F_0)$，只要求在 $F_0$ 附近逼近目标力，并在展开点精确。作者使用

$$\Psi_\theta(F,F_0)=NN_\theta(F,F_0)-\left(\nabla_FNN_\theta(F_0,F_0)-G(F_0)\right):F.$$

该线性修正保证 $\nabla_F\Psi_\theta(F_0,F_0)=G(F_0)$。训练损失是在邻域样本上最小化 $\lVert\nabla_F\Psi_\theta-G(F)\rVert_F^2$。

## 4. 硬化状态

对金属与雪，网络额外接受硬化变量 $h$。为保持对 $F$ 的可积性，单次最小化中固定 $h$，在外层固定点更新时根据 $F_0$ 重算。

## 5. 固定点优化积分

每个时间步交替执行：

1. 固定 $F_0^j$ 与 $h^j$；
2. 用 $\Psi_\theta(F,F_0^j,h^j)$ 求解一次优化时间积分；
3. 由所得速度/位置更新 $F_0^{j+1}$；
4. 重复若干次直至固定点。

收敛时，展开点与新时刻变形一致，恢复目标弹塑性隐式方程。

## 6. 稳定正则项

仿真阶段加入

$$\frac{\mu}{2}\lVert F-F_0\rVert_F^2,$$

其中 $\mu$ 为剪切模量。它在 $F=F_0$ 处梯度为零，不改变固定点，但提升大步长和高刚度下的局部稳定性；代价是可能增加人工黏性。

## 7. 学习体积保持回映射

对无闭式投影的等向材料，在 Hencky 主应变空间沿等体积方向预测塑性增量 $\delta\gamma$，并以屈服面隐式函数作为训练监督，使投影保持 $\det Z(F)=\det F$。

## 8. 训练与集成

- 输入通过 SVD 随机旋转并在主对数伸长邻域采样；
- 砂/金属扰动范围为 $[-0.1,0.1]^d$，雪为 $[-0.2,0.2]^d$；
- MLP 使用 Adam，在单张 RTX 3090 上训练；
- PyTorch 模型经 TorchScript 加载至 C++ FEM/MPM 求解器。

## 假设与边界

局部近似依赖 $F$ 与 $F_0$ 足够接近；固定点不保证任意场景收敛；训练未显式约束 Hessian、凸性或能量下界。

## 关联页面

- [[plasticitynet-2022-analysis]]
- [[plasticitynet-2022-results]]
- [[plasticitynet-2022-critical]]
- [[entities/plasticitynet]]
- [[concepts/local-elastoplastic-potential-family]]
- [[concepts/fixed-point-optimization-plasticity]]
