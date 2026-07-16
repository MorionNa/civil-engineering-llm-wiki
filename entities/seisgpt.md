---
title: "SeisGPT"
created: 2026-07-16
updated: 2026-07-16
type: entity
tags: [physics-informed, metamodeling, deep-learning, sequence-modeling, transformer, lora, structural-dynamics, nonlinear-systems, seismic-response, finite-element, high-rise-building, real-time-simulation, gpu-computing, transfer-learning, cross-domain-generalization, ida]
sources: [raw/papers/meng2026-seisgpt.pdf, raw/papers/meng2026-seisgpt-extracted.md]
confidence: high
---

# SeisGPT

> **类型：** 物理信息结构动力学基础模型  
> **作者团队：** 同济大学防灾国家重点实验室  
> **期刊：** *Nature Communications* (2026, Article in Press)  
> **DOI：** 10.1038/s41467-026-75508-5  
> **代码与数据：** https://doi.org/10.6084/m9.figshare.29957834

## 定义

SeisGPT 是一个面向多层建筑楼层响应预测的预训练模型。它以外部激励、简化楼层响应、楼层质量矩阵和等效刚度矩阵为输入，通过质量–刚度感知图编码器和 Spectral Duhamel–Green (SDG) Mixer，预测未见建筑的楼层加速度与相对位移时程。

其核心思想是把结构动力学知识直接写进网络传播机制，而不仅是写进损失函数：

```text
M/K → 质量归一化结构算子 → 图消息传递
                         → 特征分解/模态基
                         → 阻尼旋转 + 相位推进
                         → 有界谱修正 → 非线性响应
```

## 模型家族

| 版本 | 训练方式 | 用途 |
|---|---|---|
| SeisGPT-Base | 27 万级合成结构、205 万 NLTHA 预训练 | 未见建筑直接预测、跨体系零样本 |
| SeisGPT-Enhanced | Base + 694 个真实建筑 FE 数据微调 | 实际建筑高保真响应预测 |
| Building-specific SeisGPT | Enhanced + 1–9 条响应 LoRA | 单栋数字孪生个性化 |
| SeisGPT-R | 稀疏响应预训练 + 真实数据微调 | 少量传感器重建全楼响应 |

## 关键组件

### SDR 低保真物理先验

从精细 FE 模型凝聚楼层质量 $M$ 和全带宽刚度 $K$，用 Newmark-β 计算线性粗响应。深层模型学习从粗响应到非线性高保真响应的修正。

### PIGNN 结构编码器

以楼层为节点，以 $D=M^{-1/2}KM^{-1/2}$ 的非零耦合作为边，把质量和刚度直接注入图注意力。

### SDG-Mixer

将楼层算子提升到固定 token space，执行可微特征分解，在模态域中用阻尼旋转传播，再用有界有理函数修正非线性与模型误差。

### 稀疏观测门控

SeisGPT-R 在结构图编码后融合传感器特征：有可靠观测时更多信任数据，无观测楼层更多依赖结构先验。

## 训练规模

- 270,694 个建筑模型；
- 2,053,880 次非线性时程分析；
- 约 100 亿楼层响应时间步；
- 框架、框架–剪力墙、剪力墙三类主训练体系；
- 694 个真实建筑 FE 模型用于领域微调；
- 26,000 条地震、白噪声、地铁振动和冲击激励。

## 代表性能

- 未见 RC 建筑：加速度 FNMAE 约 0.022，位移 FNMAE 约 0.042–0.063；
- 真实建筑：加速度 $R=0.9829$，位移 $R=0.9423$；
- 零样本钢/砌体/隔震：$R=0.9675/0.8654/0.8841$；
- 1 条记录 LoRA：位移 $R$ 从 0.942 提升到 0.962；
- 1,000 步推理 392.43 ms，较 CPU FEA 加速约 6,000–61,000 倍；
- IDA LS1–LS4 阈值强度 $R>0.95$；
- 振动台稀疏重建在一个 43 层缩尺模型上比对应 FEM 更接近实测位移。

## 适用场景

- 城市/区域建筑群快速楼层时程预测；
- 实时地震响应与数字孪生；
- 稀疏传感器响应重建；
- 建筑专属少样本适配；
- IDA、易损性和灾后损伤状态快速筛查；
- 精细 FEM 前的高风险样本筛选。

## 适用边界

- 当前主要适用于 1–30 层、可楼层化表示的建筑；
- 需要可获得或可估计的楼层 $M/K$；
- 不覆盖失稳后的倒塌、断裂、碰撞和碎片运动；
- 训练标签依赖 FE 本构和建模假设；
- 对时间步长偏移敏感；
- 尚无校准不确定度，安全决策需 FEM/试验复核。

## 与 PhyLSTM / CM-PINNs 的区别

- `[[zhang2020-phylstm-analysis]]`：面向小规模结构、用 LSTM + 运动方程/滞回约束训练；
- `[[wu2025-cm-pinn-analysis]]`：进一步显式引入本构恢复力一致性；
- SeisGPT：以超大规模多结构预训练为核心，把质量–刚度和模态传播写入架构，追求跨建筑与跨体系迁移。

详见 `[[seisgpt-vs-phylstm-cm-pinns]]`。

## 关联论文

- `[[meng2026-seisgpt-analysis]]` — 12 维总览
- `[[meng2026-seisgpt-method]]` — 架构与公式
- `[[meng2026-seisgpt-results]]` — 实验结果
- `[[meng2026-seisgpt-critical]]` — 批判性分析

## 关联实体

- `[[pinn]]` — 物理信息学习基础范式
- `[[phylstm2]]` / `[[phylstm3]]` — 物理约束结构响应序列模型
- `[[cm-pinns]]` — 本构模型约束响应预测框架
- `[[peer-strong-motion-database]]` — 地震动数据来源相关实体
