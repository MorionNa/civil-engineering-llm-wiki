---
id: comparisons--seisgpt-vs-phylstm-cm-pinns
title: SeisGPT vs PhyLSTM vs CM-PINNs：三类物理信息结构响应预测范式
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- domain/civil-engineering
- domain/computational-mechanics
- domain/llm
- method/evaluation
- method/graph-neural-network
- method/pinn
- method/transformer
keywords:
- comparison
- cross-domain-generalization
- finite-element
- hysteresis
- lstm
- metamodeling
- nonlinear-systems
- physics-informed
- seismic-response
- structural-dynamics
- transfer-learning
- transformer
sources:
- raw/papers/meng2026-seisgpt.pdf
- raw/papers/zhang2020-phylstm.md
- raw/papers/wu2025-cm-pinn-extracted.md
created: '2026-07-16'
updated: '2026-07-31'
confidence: high
---

# SeisGPT vs PhyLSTM vs CM-PINNs

## 1. 三条技术路线

- **PhyLSTM：** 在 LSTM 时序模型中加入运动方程、状态依赖和滞回约束，用少量数据预测非线性结构响应。
- **CM-PINNs：** 在 PhyLSTM 路线上进一步显式加入本构模型计算的恢复力一致性，使网络输出符合指定材料/构件滞回规律。
- **SeisGPT：** 通过海量、多结构 NLTHA 预训练形成基础模型，把质量–刚度图、模态传播和谱修正直接写入架构，追求跨建筑与跨体系泛化。

## 2. 核心比较

| 维度 | PhyLSTM | CM-PINNs | SeisGPT |
|---|---|---|---|
| 代表论文 | Zhang et al. 2020 | Wu et al. 2025 | Meng et al. 2026 |
| 主干 | 多 LSTM | FC-SLSTM + 本构模块 | PIGNN + SDG-Mixer |
| 物理进入方式 | 主要进入 loss | loss + 显式本构恢复力 | 输入、图结构、谱传播、低保真先验 |
| 结构表示 | SDOF/MDOF 状态序列 | SDOF/MDOF + 本构状态 | 楼层 $M/K$ + 全带宽图耦合 |
| 非线性来源 | 数据驱动滞回隐变量 | 指定本构 + 数据修正 | 大规模 NLTHA 隐式学习 + 有界谱修正 |
| 数据规模 | 小样本/案例级 | 小样本/案例级 | 205 万 NLTHA、100 亿时间步 |
| 跨层数/拓扑 | 通常需固定或重新训练 | 通常需固定或重新训练 | 1–30 层、三类主训练体系共享模型 |
| 跨材料体系 | 未充分验证 | 依赖可提供的本构 | 钢/砌体/隔震零样本验证，但有性能下降 |
| 真实数据融合 | 可监督训练 | 可监督训练 | 真实域微调 + 单栋 LoRA + 稀疏传感器同化 |
| 可解释性 | 运动方程和滞回约束 | 本构恢复力最明确 | 质量–刚度谱传播可解释，材料非线性不显式 |
| 训练成本 | 低–中 | 中 | 极高 |
| 推理目标 | 单结构快速预测 | 单结构高物理一致性预测 | 多建筑、实时/建筑群尺度预测 |

## 3. 物理信息深度

### PhyLSTM：输出约束

PhyLSTM 的网络仍主要是通用 LSTM。物理通过损失检查输出是否满足：

- 位移–速度–加速度一致性；
- 运动方程；
- 滞回变量演化或恢复力关系。

优势是实现相对简单、数据需求低；缺点是物理不决定网络内部传播，跨结构拓扑能力有限。

### CM-PINNs：本构显式化

CM-PINNs 将本构模型计算出的恢复力 $f_{s2}$ 与网络预测恢复力 $f_{s1}$ 对齐。它特别适合本构已知、需要明确材料行为约束的场景。

优势：屈服、滞回和恢复力机制更可解释。
限制：本构模型需要事先选定，且当前验证仍以低维剪切结构和合成数据为主。

### SeisGPT：传播算子物理化

SeisGPT 让 $D=M^{-1/2}KM^{-1/2}$ 同时定义图连接和模态谱基，再以阻尼旋转传播 latent state。物理不是额外 loss，而是网络的“坐标系”和“信息传播规则”。

优势：适合大规模、多结构预训练和跨建筑共享。
限制：材料非线性由数据和有理谱修正隐式表示，不如 CM-PINNs 的本构机制明确。

## 4. 选型建议

### 选 PhyLSTM

- 只有少量结构响应数据；
- 结构层数和拓扑固定；
- 目标是快速构建研究原型；
- 需要比纯 LSTM 更好的物理一致性，但无需大规模跨结构泛化。

### 选 CM-PINNs

- 已知或可近似结构本构；
- 重点是屈服、恢复力和滞回变量的物理可信性；
- 数据较少，但本构和运动方程明确；
- 需要研究可替换本构、材料参数反演或退化机制。

### 选 SeisGPT

- 需要一个模型处理大量不同建筑；
- 可获得楼层质量、等效刚度和大量模拟数据；
- 需要建筑群/实时推理、真实域微调或稀疏传感器重建；
- 能承担高昂预训练成本，或直接使用已发布模型和数据。

## 5. 不能简单比较的指标

三者数据、结构规模和任务设置差异很大，不能直接用一个 FNMAE 或 $R$ 排名：

- PhyLSTM/CM-PINNs 常对单结构或低维系统做内插/外推；
- SeisGPT 重点是未见建筑、多体系和多任务迁移；
- SeisGPT 的误差按楼层峰值归一化，而早期论文可能采用全局误差或峰值误差；
- SeisGPT 使用超大规模 FE 标签，性能优势与数据规模、架构和训练成本共同相关。

## 6. 最有价值的混合路线

三者不是互斥方案。可以构建：

```text
SeisGPT 大规模预训练表示
  + CM-PINNs 式可替换本构约束
  + PhyLSTM 式状态/滞回一致性 loss
  + 少量真实传感器 LoRA / 数据同化
```

具体研究方向：

1. 用 SeisGPT encoder 编码不同建筑 $M/K$ 与拓扑；
2. 在 decoder 中加入构件/楼层本构状态 token；
3. 用显式恢复力或塑性功约束有理谱修正；
4. 在不同本构之间做条件化或 mixture-of-experts；
5. 用真实监测数据对本构参数和 LoRA 同时更新。

## 7. 对城市尺度地震研究的意义

| 层级 | 更合适的方法 |
|---|---|
| 大量建筑快速时程 | SeisGPT / 类基础模型 |
| 重点建筑、已知本构 | CM-PINNs |
| 小数据方法验证与原型 | PhyLSTM |
| 构件损伤与材料机制 | CM-PINNs + 精细模型 |
| 城市损失与修复排序 | SeisGPT 响应 → 损伤/损失代理 |
| 倒塌后接触碎片 | 三者均不够，需显式动力/接触模拟 |

## 8. 综合判断

- **PhyLSTM** 奠定了结构响应的物理约束序列学习范式；
- **CM-PINNs** 把材料本构从隐式黑箱变为显式约束；
- **SeisGPT** 将问题扩展为跨建筑基础模型，并把结构动力学写入表示和传播算子。

若研究目标是“一个模型处理多类城市建筑”，SeisGPT 路线更有潜力；若目标是“保证特定结构的材料行为正确”，CM-PINNs 更具机制优势。下一阶段最值得研究的是两者结合，而不是简单用更大的数据模型替代显式本构。

## 关联页面

- `[[meng2026-seisgpt-analysis]]`
- `[[seisgpt]]`
- `[[zhang2020-phylstm-analysis]]`
- `[[wu2025-cm-pinn-analysis]]`
- `[[phylstm2-vs-phylstm3-vs-lstm]]`
- `[[physics-constrained-training-failure-modes]]`

## Evidence By Source

### `raw/papers/meng2026-seisgpt.pdf`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。

^[raw/papers/meng2026-seisgpt.pdf]
