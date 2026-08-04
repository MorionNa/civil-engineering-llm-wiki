---
type: entity
title: Hartree–Fock LLM prompting pipeline
tags:
- domain/ai4s
- entity/model
id: entity--hartree-fock-llm-prompting
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- quantum-many-body
- scientific-reasoning
- human-in-the-loop
- evaluation
sources:
- sources/papers/pan2025-quantum-many-body-llm.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Hartree–Fock LLM prompting pipeline

^[sources/papers/pan2025-quantum-many-body-llm.md]

## 定义

一种将量子多体 Hartree–Fock 平均场推导拆为五步、用论文特定占位符实例化、在每一步核验并把已校正结果传给下一步的 LLM 计算管线。它由 Pan 等人在 2025 年论文中用于评估 GPT-4 的研究级物理计算能力。

## 关键结构

| 组件 | 作用 |
|---|---|
| HF template | 规定自由度、Hamiltonian、Fourier 变换、Wick 分解、二次项整理和对称性化简 |
| Placeholders | 注入论文特定的粒子 flavor、符号、约定和相互作用信息；每篇超过 76 个 |
| Step prompts | 将每个概念步骤再切成可执行的原子任务 |
| Corrected state | 当前输出经专家检查后，作为下一步输入，阻断错误传播 |
| Four-layer rubric | 以 Adherence、Rigor、Knowledge、Correctness 分开评分 |
| Extraction prompt | 从论文摘录中尝试自动填充占位符，解决人工准备瓶颈 |

## 证据

在正确模板和中间纠错条件下，GPT-4 对 15 篇论文有 13 篇得到正确最终 HF Hamiltonian，跨任务平均 87.5/100。论文提供的公开仓库还包含数据目录、模板和代码。

## 边界

该实体是领域专用的提示/评测管线，不是 Hartree–Fock 理论本身，也不是通用科学 agent。它依赖人工准备占位符和专家评分，且使用历史 GPT-4 服务；没有证明模型能独立选择物理近似、发现新理论或完成自洽数值求解。

## 关联

- 论文总览：[[pan2025-quantum-many-body-llm-analysis]]
- 方法展开：[[pan2025-quantum-many-body-llm-method]]
- 结果证据：[[pan2025-quantum-many-body-llm-results]]
- 物理语言代理路线：[[lu2026-language-agents-physics-analysis]]
- 科学形式化管线：[[entities/formalscience]]
