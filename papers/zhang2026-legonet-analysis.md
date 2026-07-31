---
id: papers--zhang2026-legonet-analysis
title: Zhang et al. (2026) — LegONet：可插拔、结构保持的组合式 PDE 神经算子积木
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- evidence/paper
- method/neural-operator
- method/pinn
keywords:
- ai4s
- boundary-condition
- compositional-modeling
- dissipative-dynamics
- hamiltonian
- long-horizon-rollout
- neural-operator
- operator-learning
- operator-splitting
- pde
- scientific-machine-learning
- spectral-method
- structure-preserving
- trajectory-free-training
sources:
- sources/papers/zhang2026-legonet.md
created: '2026-07-28'
updated: '2026-07-31'
confidence: high
methods:
- boundary-adapted-baseplate
- coefficient-space-operator-block
- generator-induced-vector-field
- instantaneous-operator-matching
- strang-splitting
results:
- cross-pde-recombination
- boundary-reconfiguration
- long-horizon-stability
- structure-preservation
- ood-initial-condition-robustness
failure_modes:
- baseplate-specificity
- finite-block-library
- splitting-error
- trusted-operator-label-dependence
- same-trial-space-reference
datasets:
- ten-pde-benchmark
reproducibility: high
code_url:
- https://github.com/Yooki-YueqiWang/LegONet
---

# LegONet: Plug-and-Play Structure-Preserving Neural Operator Blocks for Compositional PDE Learning

> **作者：** Jiahao Zhang, Yueqi Wang, Guang Lin
> **单位：** Purdue University
> **状态：** arXiv:2603.07882v1，2026-03-09
> **一句话定位：** LegONet 不再为每个 PDE 训练一个端到端求解器，而是把扩散、输运、Poisson 反演等机制训练成共享系数空间上的可插拔结构保持块，再用 Strang splitting 组合成新的 PDE 求解器。

## 1. 工程背景 (Engineering Background)

神经 PDE 求解器的主要吸引力是“离线训练、在线快速复用”，但实际科学计算中的主要成本往往不是一次前向推理，而是**重新配置**：方程项被增加、删除或调参，边界条件变化，或者需要在刚性、多尺度和湍流系统上进行长时间闭环推进。多数 PINN、FNO、DeepONet 或结构保持网络仍以完整方程为训练单位，机制、边界、离散和积分器纠缠在一个模型里，导致新配置通常需要重训。

## 2. Research Gap

现有路线存在三类结构性空白：

1. **单体化：** 端到端模型学习整个 PDE 的一步映射或时空解，无法单独复用扩散、输运等已学机制；
2. **边界与机制纠缠：** 边界条件常通过 loss、padding 或训练数据间接处理，切换边界意味着改变模型或重新生成轨迹；
3. **失效不可诊断：** 长时误差上升时，很难区分是某个机制块学错，还是多机制时间组合产生了 splitting error。

## 3. 科学问题 (Scientific Question)

能否建立一个统一的边界兼容状态接口，使多个独立训练的物理机制块可以在不重训完整网络的情况下被选择、缩放、重复和重新排序，同时在组合后的长时推进中保留耗散或守恒结构，并把总误差分解到“块逼近误差”和“组合积分误差”？

## 4. 研究目标 (Research Objective)

LegONet 试图把神经 PDE 求解从“一个方程一个模型”改造成“基础表示 + 机制块库 + 显式积分器”的组合式基础设施：

- 用 boundary-adapted baseplate 从表示层硬满足边界条件；
- 在共享 coefficient state 上定义统一的块输入输出接口；
- 用耗散 E-block、守恒 H-block 和残差 R-block表示不同机制；
- 只用瞬时算子标签训练单个块，不拟合完整轨迹；
- 部署时通过 Strang splitting 组装新方程；
- 提供块级结构诊断与有限时域误差分解。

## 5. 方法机制 (Method & Mechanism)

→ 详见 [[zhang2026-legonet-method]]

目标 PDE 首先写成机制和：

$$
 u_t=\sum_{i=1}^{N_{\mathrm{blk}}}\mathcal L_i(u).
$$

非齐次边界通过 lifting $u=u_{\mathrm{lift}}+u_0$ 转成齐次问题，再用边界适配谱基展开：

$$
 u_0(x,t)\approx\sum_{k=1}^{K}a_k(t)\phi_k^{(b)}(x).
$$

所有块共享同一系数状态 $a\in\mathbb R^K$，并采用结构化模板：

$$
F_i^\theta(a)=-G_i\nabla_a E_i^\theta(a)+J_i\nabla_a H_i^\theta(a)+R_i(a),
$$

其中 $G_i\succeq0$ 产生耗散结构，$J_i^T=-J_i$ 产生 Hamiltonian 守恒结构。块通过瞬时 operator matching 独立预训练，部署时按对称 Strang 顺序组合，不需要针对目标 PDE 再训练端到端模型。

## 6. 结果证据 (Result & Evidence)

→ 详见 [[zhang2026-legonet-results]]

- 在 4 类 baseplate、10 个 1D–3D 时变 PDE 上复用相同机制原语；
- 1D Burgers 中，独立训练的扩散块和输运块组合后仍分别保持能量耗散和 Hamiltonian 数值守恒，并比 PINN、FNO、DeepONet 的闭环漂移更小；
- 2D 强迫 Navier–Stokes 在 $T=50$ 的湍流推进中相对误差保持低于 4%，而取消扩散块结构约束后误差与能量漂移显著增大；
- 3D Swift–Hohenberg 通过重复调用同一个 Laplacian 块实现高阶算子，在 ID/OOD 初值下误差约为 $10^{-5}$–$10^{-4}$，FNO 约达到 40%；
- Dirichlet、periodic 和 Neumann 边界通过切换 baseplate 处理，边界条件由表示保证而不是 loss 惩罚。

## 7. 贡献 (Contribution)

1. **机制级神经算子库：** 将 PDE 求解器拆成可独立训练和复用的单用途 operator blocks；
2. **共享 baseplate 接口：** 用边界适配谱表示统一块输入输出，并把边界处理从学习任务中剥离；
3. **结构保持块模板：** 通过固定 $G/J$ 与可学习标量生成元实现离散耗散/守恒；
4. **trajectory-free training：** 只匹配瞬时算子更新，不依赖完整时程轨迹；
5. **显式组合部署：** PDE 变化被转化为块选择、缩放、重复和排序问题；
6. **可归因误差界：** 总误差由块 mismatch 与二阶 Strang splitting error 组成。

## 8. 核心知识点 (Core Knowledge)

- **可复用性需要公共状态接口。** 仅把多个网络串联并不等于模块化；所有块必须在相同、边界兼容且含义稳定的状态空间上工作。
- **结构应进入向量场参数化。** 对耗散机制学习 $E$ 并使用 $-G\nabla E$，对守恒机制学习 $H$ 并使用 $J\nabla H$，比自由回归整个向量场更容易维持长期性质。
- **学习器与积分器应解耦。** 机制块描述“微分方程右端是什么”，Strang splitting 描述“多个右端怎样在时间上组合”。
- **不使用轨迹不等于无监督。** LegONet 仍需要可信离散算子提供大量瞬时 coefficient-space 标签。
- **长时误差可分层诊断。** 减小块验证误差与减小时间步/提高 splitting 阶数对应两类不同改进方向。

## 9. Negative Knowledge

→ 详见 [[zhang2026-legonet-critical]]

- 块只在兼容 baseplate 上可直接复用；几何、边界类型或 trial space 改变仍需新 baseplate 或跨 baseplate 映射；
- 新非线性、约束、非局部机制和多物理项需要继续训练新块，当前并非通用无限算子库；
- 强非对易与刚性耦合仍可能积累 splitting error；
- 理论依赖紧集包含、Lipschitz、二阶子步和稳定参考宏步等假设；
- 实验参考解与 LegONet 使用相同 trial space、投影和 splitting schedule，主要隔离了块学习误差，并未独立验证完整空间/时间离散误差；
- PINN、DeepONet 并未在所有 2D/3D案例中参与对比。

## 10. 可迁移知识 (Transferable Knowledge)

| LegONet 机制 | 向结构动力学迁移 |
|---|---|
| boundary-adapted baseplate | 用模态基、约束消元基或有限元降阶基硬满足支座与连接边界 |
| 共享 coefficient state | 将不同结构机制统一投影到模态/子结构/图谱状态 |
| E-block | 阻尼、塑性耗散、损伤演化等非增能机制 |
| H-block | 弹性势能、惯性—弹性守恒传播和无阻尼子系统 |
| R-block | 地震输入、控制力、接触冲击和无法写成生成元的闭合项 |
| operator matching | 从有限元状态采样直接学习恢复力/切线/演化率，而非训练完整地震时程 |
| block mismatch + splitting error | 区分本构代理误差与时间积分/耦合误差 |

## 11. 研究机会 (Research Opportunity)

以下为结合结构动力学需求得到的迁移推断：

1. 将二阶结构方程转为 $[u,v,z]$ 一阶扩展状态，其中 $z$ 表示塑性、损伤和滞回内变量；
2. 建立“弹性传播块 + 阻尼块 + 可替换本构块 + 地震输入块”的结构动力学 operator library；
3. 用有限元约束模态、Craig–Bampton 子结构或质量归一化图谱作为跨结构 baseplate；
4. 研究不同自由度与不同拓扑之间的 coefficient interface 对齐，突破块的 baseplate-specific 限制；
5. 对强路径依赖本构使用状态依赖 $G/J$、增量势能或热力学一致的内部变量生成元；
6. 用自动 block discovery 从控制方程或 OpenSees 模型中识别机制、组合顺序和适当积分器；
7. 将局部构件块与全局平衡块结合，扩展到上百/上千自由度非线性结构响应。

## 12. 可复现性 (Reproducibility)

| 项目 | 评价 |
|---|---|
| 等级 | 🟢 高 |
| 代码 | 作者给出公开 GitHub 仓库 |
| 训练数据 | 系数先验、20,000 个块训练样本和标签生成方式有说明 |
| 网络/优化 | 给出主要 block 架构、AdamW、学习率、epoch、batch 与 StepLR 设置 |
| 推进设置 | 各 PDE 的时间步、终止时间、baseplate、积分方法和 splitting 顺序较完整 |
| 理论 | 主定理、假设和证明在正文及补充材料中给出 |
| 注意 | 仍需依赖作者代码确认全部实现细节与运行资源 |

## 关联页面

- [[legonet]]
- [[zhang2026-legonet-method]]
- [[zhang2026-legonet-results]]
- [[zhang2026-legonet-critical]]
- [[li2025-node-onet-analysis]]
- [[li2026-sgno-analysis]]
- [[zeraatkar2026-pgt-analysis]]
- [[sojitra2026-fedonet-analysis]]

## Evidence By Source

### `sources/papers/zhang2026-legonet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/2603.07882v1.pdf`

^[sources/papers/zhang2026-legonet.md]
