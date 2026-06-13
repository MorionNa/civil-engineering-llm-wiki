---
title: "Wang et al. (2020) — HAT: Hardware-Aware Transformers: 论文分析"
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [neural-architecture-search, transformer, hardware-aware-nas, latency-prediction, evolutionary-search, weight-sharing-supernet, hardware-specialization, machine-translation, heterogeneous-transformer, encoder-decoder-attention, edge-inference, latency-constraint]
sources: [raw/papers/wang2020_hat.md]
methods: [supertransformer-weight-sharing, evolutionary-search-latency-constraint, latency-predictor-mlp, heterogeneous-transformer-layers, arbitrary-encoder-decoder-attention]
results: [wmt14-ende-speedup-3x, wmt14-enfr-speedup-3x, evolved-transformer-cost-12041x, quantization-25x-reduction, gpu-shallow-wide, arm-deep-thin]
failure_modes: [latency-predictor-training-data-dependency, supertransformer-proxy-ranking-approximation, fixed-design-space-coverage]
datasets: [wmt14-ende, wmt14-enfr, wmt19-ende, iwslt14-deen]
reproducibility: high
code_url:
  - https://github.com/mit-han-lab/hardware-aware-transformers
dataset_url:
  - https://www.statmt.org/wmt14/translation-task.html
confidence: high
---

# HAT: Hardware-Aware Transformers for Efficient NLP

> Hanrui Wang, Zhanghao Wu, Zhijian Liu, Han Cai, Ligeng Zhu, Chuang Gan, Song Han — MIT — ACL 2020 (CCF-A)
> **硬件感知 NAS + 权重共享 SuperTransformer → 为不同硬件搜索专用高效 Transformer，3× 加速 3.7× 压缩无精度损失**

## 1. 工程背景 (Engineering Background)

Transformer 已成为 NLP 的标配架构（Vaswani et al., 2017），但高计算量严重阻碍其在资源受限硬件上的部署。一个 Transformer-Big 模型翻译 30 词句子需执行 13G FLOPs，在 Raspberry Pi 上耗时 20 秒——这种延迟对边缘设备不可接受。更关键的是，FLOPs 并不反映实测延迟：相同 FLOPs 的模型在不同硬件上延迟可差数倍，且不同硬件对各类架构参数的敏感度截然不同（GPU 对 embedding/Hidden dim 几乎不敏感，ARM CPU 高度敏感）。因此，需要**针对每种硬件定制设计专用 Transformer**，而非用 FLOPs 做统一的效率代理。

## 2. Research Gap

已有高效 Transformer 研究存在两大盲区：(1) **以 FLOPs 替代真实延迟**——Howard et al. (2017) 和 Wu et al. (2020) 使用 FLOPs 作为效率指标，但图 2 显示相同 FLOPs 的模型延迟迥异；(2) **统一架构跨硬件部署**——Evolved Transformer (So et al., 2019) 搜索成本高达 250 GPU 年且未考虑硬件差异。**核心矛盾**：硬件平台之间的延迟影响因素截然不同，但尚无方法能低代价地为每种硬件搜索专用高效架构。

## 3. 科学问题 (Scientific Question)

**如何在不依赖 FLOPs 代理的前提下，将目标硬件的实测延迟反馈直接纳入 Transformer 架构搜索循环，实现对任意硬件的低搜索代价专门化模型设计？**

## 4. 研究目标 (Research Objective)

提出 HAT 框架：(1) 构建包含任意 encoder-decoder 注意力和异构层的大型设计空间；(2) 训练一个权重共享的 SuperTransformer 作为性能代理，消除逐个训练子网的高昂成本；(3) 训练硬件延迟预测器提供快速准确的延迟反馈；(4) 通过进化搜索找到满足延迟约束的最优 SubTransformer。最终在 WMT'14 和 IWSLT'14 机器翻译任务上实现 3× 加速、3.7× 压缩，搜索成本比 Evolved Transformer 低四个数量级。

## 5. 方法机制 (Method & Mechanism)

→ [[wang2020-hat-method]]

核心四步：(1) **设计空间**：任意 encoder-decoder attention（打破信息瓶颈）+ 异构层（每层可独立选择 head 数、hidden dim）；(2) **SuperTransformer**：训练最大的 supernet，所有 SubTransformer 通过权重共享继承性能代理——仅需一次训练，即可评估搜索空间中所有 ~10^15 个候选模型；(3) **延迟预测器**：在目标硬件上采集 2000 个（架构，实测延迟）样本，训练三层 MLP 实现即时延迟预测（RMSE ~0.1s）；(4) **进化搜索**：以延迟为硬约束、validation loss 为适应度，进化搜索 30 轮选出最优 SubTransformer，最终从头训练。

## 6. 结果证据 (Result & Evidence)

→ [[wang2020-hat-results]]

- **WMT'14 En-De**：HAT 在 Raspberry Pi 上比 Transformer-Big **3× 加速、3.7× 压缩**，BLEU 持平；比 Evolved Transformer **2.7× 加速、搜索成本仅 1/12,041**
- **WMT'14 En-Fr**：3× 加速、3.6× 压缩；4-bit 量化后模型缩小 **25×**，BLEU 仅降 0.1
- **WMT'19 En-De / IWSLT'14 De-En**：GPU 上 1.8× 加速
- **设计洞察**：GPU 偏好浅而宽（dimension scaling 不降低延迟），ARM CPU 偏好深而瘦（embed dim 是延迟瓶颈）
- **权重继承有效性**：SubTransformer 继承权重与从头训练的 BLEU 高度一致（排名相同），且微调可节省 4× 训练步

## 7. 贡献 (Contribution)

→ [[wang2020-hat-critical]]

1. **首次硬件感知 NLP NAS**：直接将实测延迟反馈引入模型设计循环，为不同硬件搜索专用架构，而非依赖 FLOPs 代理
2. **低代价大搜索空间搜索**：SuperTransformer 权重共享使搜索成本比 Evolved Transformer 低 12,041×（CO2 排放从 626,000 lbs 降至 52 lbs）
3. **设计洞察**：揭示 GPU 偏好浅宽模型、ARM CPU 偏好深瘦模型，以及任意 encoder-decoder attention 的价值（50% 的 decoder 层关注多个 encoder 层）

## 8. 核心知识点 (Core Knowledge)

→ [[wang2020-hat-critical]]

1. **FLOPs ≠ 延迟**——实测延迟受硬件特性（缓存、并行度、内存带宽）影响，不能替代
2. **SuperTransformer 权重共享**——训练一个最大 supernet，子网直接继承权重评估 → 排序准确且零增量成本
3. **延迟预测器**——MLP 从架构参数直接预测延迟，比在线测量快数百倍
4. **硬件差异化设计**——GPU 瓶颈在序列长度/层数，ARM CPU 瓶颈在 embedding/Hidden dim

## 9. Negative Knowledge

→ [[wang2020-hat-critical]]

- **延迟预测器依赖训练数据**：需为每种新硬件采集 2000 个样本训练预测器，大规模硬件矩阵难以 scale
- **SuperTransformer 代理排序不完美**：继承权重 BLEU 与从头训练 BLEU 的排序一致但非精确预测，可能漏掉好架构
- **设计空间固定**：Q/K/V 向量维度固定为 512，encoder 层数固定为 6，未探索更多维度
- **仅验证机器翻译**：未扩展到其他 NLP 任务（分类、问答等），设计洞察的泛化性未证明

## 10. 可迁移知识 (Transferable Knowledge)

→ [[wang2020-hat-critical]]

| 知识 | → 迁移 |
|------|--------|
| 延迟预测器替代 FLOPs 的硬件感知设计范式 | 任何需要硬件效率优化的模型设计（CNN、ViT、LLM） |
| SuperTransformer 训练一次评估所有子网 | 所有 NAS 场景，特别是大搜索空间的低成本评估 |
| 任意 encoder-decoder attention 打破信息瓶颈 | 任何 seq2seq 架构（翻译、摘要、语音识别） |
| 异构层让不同层有不同容量 | 任何深层网络的层差异化设计 |

## 11. 研究机会 (Research Opportunity)

→ [[wang2020-hat-critical]]

- HAT + 更多 NAS 搜索空间（kernel size、FFN activation、normalization 类型）
- 延迟预测器泛化：训练一个跨硬件泛化的延迟模型，而非每种硬件独立采集数据
- HAT for Decoder-Only LLM：将 HAT 框架扩展到 GPT 类架构的推理效率优化
- 多目标搜索：同时优化延迟、模型大小、能耗

## 12. 可复现性 (Reproducibility)

**🟢 高复现性** — 代码 + 预训练 SuperTransformer 完全开源

| 项目 | 说明 |
|------|------|
| **等级** | 🟢 高 |
| **官方代码** | `https://github.com/mit-han-lab/hardware-aware-transformers` |
| **数据集** | WMT'14 En-De/En-Fr, WMT'19 En-De, IWSLT'14 De-En（全公开） |
| **协议** | MIT |
| **复现要点** | 需 GPU 训练 SuperTransformer（约 200 GPU 小时）；延迟预测器需在目标硬件上采集 2000 样本；论文提供预训练 SuperTransformer checkpoint |

## 关联页面

- [[wang2020-hat-method]] — SuperTransformer + 延迟预测器 + 进化搜索展开
- [[wang2020-hat-results]] — 四任务三硬件完整实验数据
- [[wang2020-hat-critical]] — 贡献·Negative·可迁移·研究机会
- [[chen2021-tenas-analysis]] — TE-NAS 也是低代价 NAS，但面向 CNN 且训练-free vs HAT 的权重共享范式
- [[jiang2024-mixtral-of-experts-analysis]] — Mixtral MoE 也是 Transformer 效率优化，但路线不同（稀疏激活 vs 架构搜索）
