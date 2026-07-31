---
id: papers--li2025-localized-waves-pinn-analysis
title: Li & Wang (2025) — Bäcklund 变换约束 PINN 生成非线性 PDE 局域波：论文分析
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- evidence/paper
- method/pinn
keywords:
- ai4s
- collocation-strategy
- deep-learning
- neural-network
- nonlinear-systems
- physics-informed
- physics-simulation
- pinn
- soft-constraint
- synthetic-data
sources:
- sources/papers/li2025-localized-waves-pinn.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- backlund-transformation
- multi-output-pinn
- automatic-differentiation
- latin-hypercube-sampling
- lbfgs
- xavier-initialization
- adaptive-loss-weighting
results:
- one-soliton
- two-soliton
- flat-top-wave
- stair-wave
- gaussian-wave-evolution
failure_modes:
- irreversible-transformation
- no-v-reference-solution
- missing-weight-update-rule
- missing-code
- multi-wave-cost-growth
- waveform-terminology-ambiguity
datasets:
- modified-kdv-one-soliton
- modified-kdv-two-soliton
- gaussian-initial-wave
reproducibility: low
---

# Data-driven localized waves via transformation and PINN

> **作者：** Nan Li, Ming Wang
> **期刊：** *Nonlinear Dynamics*, 113, 2559–2568（正式卷期 2025；online 2024-10-01）
> **DOI：** 10.1007/s11071-024-10359-7

## 1. 工程背景

> **⚠️ 非线性类型：** **PDE 算子非线性**——非线性来自控制方程中的 $v_x\sin^2v$、$v_x^3$ 与 $u^2u_x$，不涉及塑性、损伤、超弹性等**材料本构非线性**。本文研究的是非线性色散波及局域波生成；PINN 通过自动微分把算子非线性写入残差，与 [[raissi2019-pinn-analysis]] 同类，而不是结构材料本构识别问题。

非线性色散方程用于描述非线性光学、等离子体与流体界面波。含三角非线性项的目标方程难以直接解析求解，而其局域波形态又是理解传播、相互作用与稳定性的基础。

## 2. Research Gap

目标方程

$$v_t-\frac32v_x\sin^2v-\frac12v_x^3-v_{xxx}=0$$

可经 $u=\sin v-v_x$ 映射到 modified KdV（mKdV）方程，但该变换只能由已知 $v$ 直接得到 $u$，不能由已知 $u$ 唯一、显式地反解 $v$。已有 PINN 多为单方程求解；作者关注“以一个方程的初边值，在同一网络中联立恢复两个方程的解”。

## 3. 科学问题

能否把不可直接逆用的 Bäcklund 关系变成神经网络软约束，在只有 mKdV 初边值数据时，同时得到 mKdV 解 $u$ 与无标签目标方程解 $v$？得到的 $v$ 是否同时满足目标 PDE 与变换关系，并呈现可解释的局域波形？

## 4. 研究目标

构建一个双输出 [[pinn]]，联合最小化 $u$ 的初边值误差、mKdV 残差、目标方程残差和 Bäcklund 残差；用单孤子、双孤子及高斯初波验证该机制，并观察目标方程中难以解析获得的新局域波。

## 5. 方法机制

同一前馈网络接收 $(x,t)$ 并输出 $(\hat u,\hat v)$。训练只给 $u$ 的初边值；$v$ 没有观测标签，而由两条 PDE 和

$$\mathrm{BT}=\hat u-\sin\hat v+\hat v_x$$

共同约束。总损失为四项加权 MSE；内部配点用 Latin hypercube sampling，导数由自动微分获得，网络采用 4 个隐藏层、每层 100 个神经元、tanh、Xavier 初始化和 L-BFGS。详见 [[li2025-localized-waves-pinn-method]] 与方法实体 [[backlund-transformation-pinn]]。

## 6. 结果证据

- $k=1$ 单孤子：$u$ 的相对 $L_2$ 误差为 $5.190663\times10^{-4}$，平均 630 次迭代、38.1618 s；$MSE_G=1.798\times10^{-6}$、$MSE_{BT}=3.707\times10^{-7}$。
- $k=-1$ 案例：相对 $L_2$ 误差 $7.744260\times10^{-4}$，平均 772 次迭代、29.2134 s；目标方程输出呈近似 flat-top 形态。
- 双波案例：相对 $L_2$ 误差增至 $3.123852\times10^{-3}$，约 16,166 次迭代、1,949.1901 s；$v$ 呈阶梯形，计算代价显著增加。
- 高斯初波：$MSE_G=8.803\times10^{-6}$、$MSE_F=8.965\times10^{-6}$，得到作者称为 soliton/antisoliton 的传播形态。完整证据见 [[li2025-localized-waves-pinn-results]]。

## 7. 贡献

本文把解析变换从“求解公式”改造成“跨方程物理约束”，使不可直接逆用的 Bäcklund 关系可通过联合残差训练数值反演；同时展示一个网络、单侧初边值监督下的双方程输出。贡献不是新 PINN 骨干，而是约束图的设计。

## 8. 核心知识点

1. 已知 $u$ 时，Bäcklund 关系本身不足以唯一确定 $v$；目标 PDE 残差承担了正则化与物理解筛选作用。
2. “$v$ 无监督”不等于无先验：它受到 $G(v)=0$ 与 BT 两类强先验约束。
3. 联立约束可生成解析法难处理的波形，但小残差并非唯一性或正确性的严格证明；这与 [[wang2023-pinn-spurious-analysis]] 的警示直接相关。

## 9. Negative Knowledge

- 论文没有 $v$ 的解析解或独立高精度数值基准，主要以 PDE/BT 残差和图形连续性论证正确性。
- Bäcklund 逆问题的唯一性未证明；不同初值、网络初始化可能落到不同可行 $v$。
- “残差权重随训练调整”没有给出具体更新公式；代码、随机种子、硬件和软件版本均未公开。
- 双波案例迭代数与耗时比单波大约高一个数量级以上，显示方法对波形复杂度敏感。
- 公式 $u=2k\operatorname{sech}(kx+k^3t)$ 对 $k=\pm1$ 都是光滑有符号脉冲；论文把其中一种称作 “cuspon”，与通常要求尖点/导数奇异的术语存在疑点。详见 [[li2025-localized-waves-pinn-critical]]。

## 10. 可迁移知识

对存在 Miura、Darboux、守恒律或本构映射的方程组，可把解析关系写成额外残差，与各控制方程共同训练；这是一种“关系约束 + 方程约束”的弱逆变换模板。与 [[wang2024-kinn-analysis]] 的骨干网络改造互补：前者改约束图，后者改函数逼近器。

## 11. 研究机会

应首先用独立谱方法/FDM 验证 $v$，研究逆变换的多解性与初值敏感性；随后可引入硬 Bäcklund 约束、自适应权重、残差自适应采样，或用 KAN/KINN 替换 MLP，并系统测试多孤子与碰撞过程的复杂度扩展。

## 12. 可复现性

**🔴 低复现性**——标准数学 PDE 无外部数据依赖，首个单波案例参数较完整，但关键权重更新规则、双波常数、若干时域设置、代码与运行环境缺失。

| 项目 | 说明 |
|------|------|
| **等级** | 🔴 低 |
| **官方代码** | 未提供 |
| **数据集** | 解析 mKdV 单/双波与程序生成的高斯初值；论文声明未使用外部数据 |
| **协议** | 无代码/数据协议 |
| **复现要点** | 双输出 4×100 tanh 网络；LHS 配点；Xavier + L-BFGS；必须自行定义损失权重更新，并报告多随机种子 |

## 关联页面

- [[li2025-localized-waves-pinn-method]] — 四项损失与联合约束机制
- [[li2025-localized-waves-pinn-results]] — 三组实验与数值证据
- [[li2025-localized-waves-pinn-critical]] — 局限、迁移和研究机会
- [[pinn]] — 基础方法实体
- [[raissi2019-pinn-analysis]] — 非线性 PDE 的经典 PINN 基线
- [[wang2023-pinn-spurious-analysis]] — 小残差不保证真解
- [[wang2024-kinn-analysis]] — 可替换骨干网络的相关路线

## Evidence By Source

### `sources/papers/li2025-localized-waves-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1007_s11071-024-10359-7.pdf`

^[sources/papers/li2025-localized-waves-pinn.md]
