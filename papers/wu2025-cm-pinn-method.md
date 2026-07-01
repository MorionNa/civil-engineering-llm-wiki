---
title: "Wu et al. (2025) — CM-PINNs 方法机制展开"
created: 2026-07-01
updated: 2026-07-01
type: paper-analysis
tags: [physics-informed, pinn, lstm, multi-lstm, finite-difference, physics-constrained-loss, adaptive-weighting, structural-dynamics, hysteresis, restoring-force]
sources: [raw/papers/wu2025-cm-pinn-extracted.md]
methods: [physics-constrained-loss, finite-difference, multi-lstm, adaptive-weighting]
confidence: high
---

# Wu et al. (2025) — CM-PINNs 方法机制展开

> 返回概述 → [[wu2025-cm-pinn-analysis]]

## 1. 总体框架

CM-PINNs 的输入是地震动加速度 $a_g(t)$，输出是结构响应全时程。它不是单网络端到端黑箱，而是由**三个 FC-SLSTM + 一个中心差分模块 + 一个非线性本构模块**协同构成。

```text
a_g(t)
  └─ FC-SLSTM1 → Z = {u, u_dot, r}
         ├─ CDM → {u_dot, u_ddot, r_dot}
         ├─ FC-SLSTM2(Z) → f_s1        # 数据驱动恢复力加速度
         ├─ FC-SLSTM3(Δu_dot, r) → r_dot_pred
         └─ NLCM/BLCM(u, history) → f_s2 # 本构模型恢复力加速度

loss = data(u,u_dot) + kinematic + EOM + constitutive + hysteresis
```

## 2. FC-SLSTM：skip + fully-connected preprocessing

传统多层 LSTM 在深层传播中会丢失浅层细节，尤其对地震响应这种长时序、强峰值、局部非平稳信号不利。FC-SLSTM 在主路径两层 LSTM 外增加一条并行 FC 预处理路径，将浅层特征过滤后与深层特征拼接，再输入第三层 LSTM。

| 组件 | 作用 |
|---|---|
| LSTM layer1/2 | 提取高层长期时序依赖 |
| FC layer1 | 预处理浅层输入特征，避免直接 skip 噪声 |
| concat | 融合浅层细节与深层抽象 |
| LSTM layer3 | 对多尺度特征再整合 |
| FC layer2 | 映射到目标输出维度 |

## 3. 状态空间与隐变量

FC-SLSTM1 输出：

$$Z(\theta_1)=\{z_1,z_2,z_3\}^T=\{u,\dot u,r\}^T$$

其中 $r$ 是**未观测滞回位移/内变量**。这一点沿袭 `[[zhang2020-phylstm-analysis]]` 的思想：不要只预测可观测位移，而要让网络显式承载滞回内部状态，否则恢复力和残余位移难以稳定预测。

CDM 模块用中心差分计算 $\dot Z=\{\dot u,\ddot u,\dot r\}$。内部时间点用中心差分，边界点用前向/后向差分，保持输出张量 shape 与输入一致。

## 4. 双恢复力：$f_{s1}$ 与 $f_{s2}$

| 恢复力 | 来源 | 含义 |
|---|---|---|
| $f_{s1}$ | FC-SLSTM2($Z$) | 数据驱动恢复力加速度，负责从状态中学习复杂局部非线性 |
| $f_{s2}$ | NLCM/BLCM($u$, history) | 本构模型计算出的物理恢复力加速度 |

损失项 $L^P_{fs}=\|f_{s2}-f_{s1}\|^2$ 强迫二者一致。这样做比只用运动方程约束更强，因为运动方程只要求某个恢复力能平衡外力，而本构约束进一步要求这个恢复力来自合理的材料/构件关系。

## 5. BLCM：双线性本构模块

SDOF 参数：自然周期 $T=1.0s$、初始刚度 $k=4\pi^2m/T^2$、屈服力 $F_y=0.98g$、屈服后刚度比 $\alpha=0.1$、阻尼比 $\xi=0.05$。

弹性阶段：

$$F_s=kx,\quad |x|\le x_y$$

塑性阶段：

$$F_s=\alpha k(x\mp x_y)\pm F_y,\quad |x|>x_y$$

Appendix A 给出张量化状态判别算法：根据 $u_i-u_{i-1}$ 和上一时刻恢复力 $R^s_{i-1}$ 更新 $R^s_i$ 与 $f^s_i$。实现时所有变量都必须是同设备张量，以保留梯度并提高矩阵化效率。

## 6. 损失函数

| 损失项 | 公式含义 | 物理作用 |
|---|---|---|
| $L^D_u$ | $u$ 预测 vs 标注位移 | 数据监督 |
| $L^D_v$ | $\dot u$ 预测 vs 标注速度 | 数据监督 |
| $L^P_v$ | $z_2-\dot z_1$ | 位移-速度一致性 |
| $L^P_e$ | $-a_g-\ddot u-CM^{-1}\dot u-f_{s1}$ | 运动方程约束 |
| $L^P_{fs}$ | $f_{s2}-f_{s1}$ | 本构模型约束 |
| $L^P_r$ | $\dot z_3-\dot r_{pred}$ | 滞回内变量演化约束 |

$$\omega_j=\left|\frac{L^D_u}{L_j+\epsilon}\right|,\quad \epsilon=10^{-8}$$

$$L_{total}=\frac{L^D_u+\sum_j\omega_jL_j}{6}$$

其中 $j\in\{L^D_v,L^P_v,L^P_e,L^P_{fs},L^P_r\}$。

## 7. 训练设置

| 项目 | 设置 |
|---|---|
| 框架 | Python 3.9 + PyTorch |
| 优化器 | Adam |
| 训练轮数 | 20,000 epochs |
| 初始学习率 | $1\times10^{-3}$ |
| 学习率阶段 | 3000 epochs 后保存/加载参数，继续以 $5\times10^{-4}$ 训练 |
| 停止策略 | early stopping 监控训练集表现 |
| 硬件 | Intel i7-11700K + NVIDIA RTX 3070 |

## 8. 与 PhyLSTM 的方法差异

| 维度 | PhyLSTM | CM-PINNs |
|---|---|---|
| 主干 | 多 LSTM | FC-SLSTM |
| 恢复力 | LSTM 学习 + 运动方程约束 | LSTM 恢复力 $f_{s1}$ + 本构恢复力 $f_{s2}$ 一致性 |
| 本构模型 | 不作为独立模块 | NLCM/BLCM 独立模块 |
| loss 平衡 | 手动/经验权重 | 自适应初始化权重 |
| 主要改进点 | 少样本物理约束 | 本构一致性 + 峰值预测改善 |

## 关联
- [[wu2025-cm-pinn-analysis]] — 论文概述
- [[wu2025-cm-pinn-results]] — 实验结果
- [[cm-pinns]] — 方法实体
- [[zhang2020-phylstm-method]] — PhyLSTM 方法对照
