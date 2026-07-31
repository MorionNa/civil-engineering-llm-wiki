---
id: papers--du2026-hcff-pinn-analysis
title: Du et al. (2026) — HCFF-PINN：频率先验 Fourier 特征与初值硬约束的无标签结构动力求解
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- evidence/paper
- method/pinn
keywords:
- adam-lbfgs
- auxiliary-function
- benchmark
- collocation-strategy
- deep-learning
- equation-of-motion
- finite-element
- ground-motion
- hard-constraint-strategies
- hard-constraints
- neural-network
- physics-informed
- pinn
- sdof
- seismic-response
- structural-dynamics
- synthetic-data
- two-phase-optimization
- vibration-analysis
sources:
- sources/papers/du2026-hcff-pinn.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
methods:
- physics-guided-fourier-features
- hard-initial-conditions
- tanh-squared-modulation
- automatic-differentiation
- adam-lbfgs-optimization
results:
- mixed-frequency-error-reduction
- high-frequency-reconstruction
- multi-degree-of-freedom-validation
- cross-ground-motion-robustness
failure_modes:
- frequency-prior-mismatch
- hard-constraint-function-mismatch
- high-dimensional-boundary-generalization
- nonlinear-structure-unvalidated
datasets:
- synthetic-harmonic-loads
- northridge-symlar
- gazli-karakyr
- kocaeli-duzce
- el-centro-array
- san-simeon-diablo-canyon
reproducibility: medium
---

# A label-free physics informed neural network with hard constraints and Fourier features spectrally-enhanced for multi-frequency seismic structural dynamic response

> **论文：** Ke Du, Zehua Huang, Jiaxin Li, Dongwang Tao, Zhuoshi Chen (2026), *Engineering Applications of Artificial Intelligence*, 166, 113640. DOI: 10.1016/j.engappai.2025.113640
> **核心定位：** HCFF-PINN 用结构自振频率引导 Fourier 特征以缓解谱偏差，再用 $\tanh^2(t)$ 把静止初值硬编码进输出，使训练目标只保留运动方程残差。
> **“无标签”的准确含义：** 不再需要初值采样点及 IC loss；仍需已知结构参数、外部荷载/地震动和时域配点。

## 1. 工程背景 (Engineering Background)
> **⚠️ 非线性类型：线性结构动力响应；本文没有验证物理非线性。** 全部算例均满足常系数线性方程 $M\ddot u+C\dot u+Ku=P(t)$，SDOF、3-DOF 剪切框架及四层线性钢框架均未包含塑性、损伤、接触或非线性恢复力。非线性只存在于神经网络激活、$\tanh^2(t)$ 调制和非凸训练中；论文把“nonlinear systems”列为未来扩展，不是已验证能力。这与同样处理线弹性振动的 [[at-pinn-hc]] 可比。

地震响应同时包含低频主能量与高频局部分量。Newmark-$\beta$ 等积分法成熟，但在高频、批量求解或反问题中仍有数值耗散和迭代成本；标准 [[pinn]] 又倾向先学习低频，并因 ODE 与初值损失收敛率不同而训练失衡。

## 2. Research Gap
Fourier 特征能够缓解全连接网络的谱偏差，但频率参数若缺乏物理引导可能选错；动态损失权重只能调节 ODE/IC loss 的相对贡献，不能改变二者不同的 NTK 谱。已有硬约束可消除部分软约束损失，但面向多频地震结构响应时，如何同时利用结构频率先验并选择稳定的初值调制函数仍缺系统验证。

## 3. 科学问题 (Scientific Question)
能否从结构动力学先验出发，同时改变网络的频谱表示与约束方式：让 Fourier 基覆盖结构主导频率，并把零初位移、零初速度直接写进解空间，从而在不使用初值标签的情况下稳定求解多频地震响应？

## 4. 研究目标 (Research Objective)
提出 [[hcff-pinn]]：以结构自振频率初始化 Fourier feature parameters，以 $u(t)=\tanh^2(t)N(t;\theta)$ 精确满足静止初值，只最小化 ODE 残差；在 SDOF、3-DOF 地震响应、四类地震动和静力凝聚后的四层钢框架上，与 PINN、FF-PINN、G-PINN、SA-PINN 和 PI-KAN 比较。

## 5. 方法机制 (Method & Mechanism)
Fourier 映射为 $\gamma(t)=[\cos(Bt),\sin(Bt)]$，$B\sim\mathcal N(0,\sigma^2)$；$\sigma$ 由结构阻尼自振频率或多阶频率给定，使 [[neural-tangent-kernel]] 的高频特征方向获得更有利的表示。硬约束输出 $u(t)=g(t)N(t;\theta)$ 选择 $g(t)=\tanh^2(t)$，因 $g(0)=g'(0)=0$，所以 $u(0)=\dot u(0)=0$，总损失只剩 ODE residual。→ [[du2026-hcff-pinn-method]]

## 6. 结果证据 (Result & Evidence)
标准 PINN 在混频 SDOF 上相对 $L_2$ 误差为 38%，高频段为 58%；加入 Fourier 特征后，FF-PINN 在低频/混频工况降至 0.03%/0.36%。3-DOF Northridge 工况中 HCFF-PINN 各响应误差约 0.24%–0.30%，训练 713 s；FF-PINN 训练 881 s，PI-KAN 1532 s。四条地震动的时域和频域误差均低于 0.5%，结论报告 MDOF 相比 FF-PINN 改善 30%–60%。→ [[du2026-hcff-pinn-results]]

## 7. 贡献 (Contribution)
1. 把结构自振频率转化为 Fourier 特征先验，用物理频谱而非盲目随机尺度指导编码。
2. 用架构级初值硬约束删除 IC loss，将 ODE/IC 多目标训练变为单残差目标。
3. 在谐波、真实地震动、3-DOF 及凝聚后的 20-DOF 线性钢框架上验证频谱增强与硬约束的协同效应。→ [[du2026-hcff-pinn-critical]]

## 8. 核心知识点 (Core Knowledge)
HCFF-PINN 分别在“表示”和“优化目标”两处动手：Fourier 特征让网络更容易表示高频，硬约束则从目标函数中消除 IC 分量。它不是单纯调 loss 权重，也不同于 [[at-pinn-hc]] 的时间推进与多类辅助函数框架；本文并未证明对材料非线性或非线性运动方程有效。

## 9. Negative Knowledge
频率参数需要落在主导能量频带附近，极端偏离的 $[60,120]$ rad/s 会显著增误差；$\tanh^2(t)$ 仅自动满足零初位移/零初速度，非零初值和复杂边界需重新构造 lifting/modulation。四层框架仍是线弹性且先做静力凝聚，真正高维、复杂边界和非线性结构尚未验证。论文没有公开代码或数据链接，地震数据声明为“可按请求提供”。

## 10. 可迁移知识 (Transferable Knowledge)

| 知识 | 可迁移方向 | 迁移方式 |
|---|---|---|
| 物理频率指导 Fourier 编码 | 风振、机械振动、波传播 | 用模态分析或简化模型给出频带，而非任意设 $\sigma$ |
| 硬约束删除损失项 | 初值 ODE/PDE、守恒约束 | 构造满足目标条件及其必要导数的 lifting 函数 |
| 时域 + 频域联合评价 | 任意振动代理模型 | 同时报告全时域和分频带误差，避免总误差掩盖高频失败 |
| 先验不确定性压力测试 | 参数不确定结构 | 用近似频率、子集频率和极端偏差做敏感性分析 |

## 11. 研究机会 (Research Opportunity)
下一步应研究可训练或自适应选择的频率参数、非零初值与复杂边界的通用硬约束生成器，并在不凝聚的高维有限元系统、刚度退化/塑性/滞回结构及参数反演上验证。还需要与 [[du2026-hcff-pinn-method]] 中的频率先验进行消融，区分 Fourier 编码、硬约束和两者协同的独立收益。

## 12. 可复现性 (Reproducibility)

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中 |
| **官方代码** | 未提供公开仓库 |
| **数据集** | PEER NGA-West2 地震记录与 San Simeon 记录；全文未给公开下载链接，声明数据可按请求提供 |
| **已披露训练配置** | 4 层×50 神经元，tanh，lr=0.001，2000 interior points；MDOF/钢框架使用 Adam 5000 步 + L-BFGS 5000 步 |
| **复现要点** | 用结构自然频率设置多组 $\sigma$；严格实现 $u=\tanh^2(t)N$；以 Newmark-$\beta$ 为参考；同时核对时域与分频带误差 |
| **缺口** | 无代码、随机种子、硬件说明和可直接下载的数据清单；随机 Fourier 特征维数/采样复现实务仍不充分 |

## 关联页面
- [[hcff-pinn]] — 本文新方法实体
- [[pinn]] — 标准 PINN 范式
- [[neural-tangent-kernel]] — 谱偏差与多损失收敛率分析工具
- [[at-pinn-hc]] — 另一条结构振动硬约束路线

## Evidence By Source

### `sources/papers/du2026-hcff-pinn.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_engappai_2025_113640.xml`, `raw/papers/extracted/10_1016_j_engappai_2025_113640_extracted.txt`

^[sources/papers/du2026-hcff-pinn.md]
