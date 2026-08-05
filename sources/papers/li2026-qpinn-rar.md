---
id: sources--papers--li2026-qpinn-rar
title: "Li et al. (2026) — QPINN-RAR"
type: source
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/computational-mechanics
- evidence/paper
keywords:
- quantum-physics-informed-neural-network
- qpin
- residual-based-adaptive-refinement
- adaptive-collocation
- parametrized-quantum-circuit
sources:
- raw/papers/li2026-qpinn-rar-source.md
created: '2026-08-06'
updated: '2026-08-06'
confidence: high
evidence_scope: full-text
reproducibility: medium
code_url: []
dataset_url: []
contradictions:
- Section III opening reverses the stated solution-type descriptions of the Burgers and diffusion examples.
- The equation labelled as a diffusion equation contains a nonlinear advection term, while the reported exact solution does not satisfy that displayed equation.
---

# 来源记录：QPINN-RAR

## 文献信息

- **英文题名：** Quantum physics-informed neural network with residual-based adaptive refinement for solving partial differential equations
- **作者：** Le Li、Junkai Yang、Qingle Wang、Zhichao Zhang
- **期刊：** Physical Review Research 8, 033042 (2026)
- **DOI：** 10.1103/lb19-wv6f
- **收稿 / 接收 / 发表：** 2026-04-23 / 2026-06-22 / 2026-07-10
- **证据范围：** 用户提供的 12 页正式全文。
- **开放许可：** 论文标注为 Creative Commons Attribution 4.0。
- **代码与数据：** 未给出公开代码；数据不公开，可向作者合理申请。

## 证据地图

- **第 1–2 页：** PINN、量子物理信息网络、固定采样问题、RAR 研究动机与主要贡献声明。
- **第 2–3 页：** RAR 算法：候选集残差计算、按高残差比例划分、Top-$n$ 加点与迭代训练；图 1 展示三维热方程上的采样过程。
- **第 3–5 页：** QPINN-RAR 总体流程、一般 PDE 表达、初值/边界/PDE 残差损失、经典前后处理网络及五量子比特 PQC；图 2 和图 3 展示架构。
- **第 4–5 页：** Adam→L-BFGS 两阶段优化、RAR 周期、加点数量、停止阈值、初始采样规模和十次独立运行设置。
- **第 5–6 页：** 一维黏性 Burgers 方程；表 I、图 4–5 给出参数量、损失、相对 $L_2$ 误差、迭代数和误差分布。
- **第 7–8 页：** 标为“一维扩散方程”的算例；表 II、图 6–7 给出比较结果。
- **第 7–10 页：** 三维热方程；表 III、图 8–9 给出参数效率、误差和二维切片结果。
- **第 9 页：** 结论、同分布验证边界、真实量子硬件噪声/退相干/门误差等未来工作。

## 证据边界

论文比较的是在 PennyLane 与 PyTorch 中实现的混合量子—经典模型，未报告真实量子硬件实验、端到端墙钟时间、量子门执行成本或相对于经典网络的计算加速。因此，正文支持“参数量更少和特定基准误差更低”，不支持“已经实现量子计算加速”。

三个算例均具有解析参考解，训练与测试来自相同问题设置。论文未验证复杂几何、变化边界/初值、工程材料非线性、长时间滚动预测、真实硬件噪声或样本外问题族泛化。

## 内部一致性警报

1. 第 III 节开头把 Burgers 与扩散算例的“三角/非三角函数解”描述写反，随后 III.A、III.B 的分节文字又恢复为 Burgers 非三角、扩散三角。
2. 式 (8) 被称为扩散方程，但显示式包含 $u\,u_x$ 非线性对流项；文中同时给出 $u=\sin(\pi x)e^{-t}$ 为精确解。该解不满足所显示的含非线性对流项方程。知识页因此分别记录“论文报告结果”与“方程一致性疑问”，不把该算例当作无争议的扩散基准。
3. 算法 1 第 2 步写作“Train the PINN”，而算法标题和上下文是 QPINN 的 RAR；这更可能是表述遗留，不能据此判断实际训练对象发生变化。

## 生成与更新页面

- [[papers/li2026-qpinn-rar-analysis]]
- [[papers/li2026-qpinn-rar-method]]
- [[papers/li2026-qpinn-rar-results]]
- [[papers/li2026-qpinn-rar-critical]]
- [[entities/qpinn-rar]]
- [[concepts/adaptive-sampling-pinn]]
