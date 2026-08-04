---
type: entity
title: AlphaGeometry
tags:
- domain/ai4s
- entity/model
id: entity--alphageometry
status: active
project: civil-engineering-llm-wiki
keywords:
- large-language-models
- scientific-reasoning
- geometry
- olympiad
- machine-learning
- theorem-proving
- formalization
- reproducibility
sources:
- sources/papers/trinh2024-alphageometry.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# AlphaGeometry

^[sources/papers/trinh2024-alphageometry.md]

## 定义

AlphaGeometry 是 Trieu H. Trinh、Yuhuai Wu、Quoc V. Le、He He 和 Thang Luong 在 2024 年 Nature 论文中提出的欧氏平面几何定理证明系统。它是神经符号系统：Transformer 语言模型提出辅助构造，DD+AR 符号引擎负责确定性演绎和验证。

对应论文总览见 [[trinh2024-alphageometry-analysis]]，详细机制见 [[trinh2024-alphageometry-method]]。

## 结构

- **语言模型**：从 [[entities/alphageometry-synthetic]] 的合成定理—证明数据训练；预训练全部合成证明，再对含辅助构造的子集微调。
- **符号引擎**：structured deductive database（DD）执行几何规则闭包，algebraic reasoning（AR）通过 Gaussian elimination 处理角度、比值、距离和几何常数。
- **搜索接口**：语言模型每轮生成一条辅助构造，符号引擎加入该构造后重新计算闭包；推理使用 beam search。
- **证明输出**：语言模型输出与符号引擎输出交错，成功路径经过逻辑和数值验证，并可用模板翻译成自然语言。

## 论文中的模型配置

论文 Methods 报告 Transformer 有 12 层、1,024 embedding dimension、8 个 attention heads、4,096 维 dense layer、ReLU 激活和 151 million 参数（不含输入/输出 embedding layers）。Tokenizer 词表大小为 757，最大上下文为 1,024 tokens，使用 5% dropout。

论文报告在 IMO-AG-30 上解决 25/30；无预训练为 21/30，无微调为 23/30。更大 231 题集合上的解决比例为 98.7%。

## 边界

AlphaGeometry 只在本文专用经典几何表示中工作，不能据此称为覆盖完整 IMO 或所有数学领域的通用证明器。论文报告其当前规则不包含若干人类高层工具；证明成功也可能输出超过 100 步的低层证明。

论文未披露完整 100 million 合成训练语料的独立下载 URL，不能仅凭本文确认完全相同训练分布的端到端复现。代码和模型 checkpoint 地址为 <https://github.com/google-deepmind/alphageometry>。

## 关联页面

模型结果见 [[trinh2024-alphageometry-results]]，失败边界与迁移机会见 [[trinh2024-alphageometry-critical]]。本实体不代表一个通用 theorem-prover 占位类别，而只记录论文中实际提出并评测的 AlphaGeometry 系统。
