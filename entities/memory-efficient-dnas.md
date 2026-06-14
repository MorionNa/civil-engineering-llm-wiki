---
title: "DARTSformer (Memory-Efficient DARTS for Transformers)"
created: 2026-06-14
updated: 2026-06-14
type: entity
tags: [neural-architecture-search, transformer, memory-efficient, reversible-networks, differentiable-search, darts, machine-translation]
sources: [raw/papers/memory_efficient_dnas2021.pdf]
confidence: high
---

# DARTSformer

DARTSformer 是 Yuekai Zhao, Li Dong, Yelong Shen, Zhihua Zhang, Furu Wei, Weizhu Chen（北京大学 & 微软）在 ACL-IJCNLP 2021 Findings 提出的内存高效可微分 Transformer 架构搜索方法。通过将 multi-split reversible network 与 DARTS (Differentiable Architecture Search) 结合，使 Transformer 架构搜索的内存消耗减半，首次实现在 hidden size d=960 下的大规模可微分搜索。

## 关键信息

- **类型**: method / architecture
- **提出**: Yuekai Zhao, Li Dong, Yelong Shen, Zhihua Zhang, Furu Wei, Weizhu Chen (Peking University & Microsoft)
- **发表**: ACL-IJCNLP 2021 (Findings) | arXiv: 2105.14669
- **核心贡献**: 将多分割可逆网络与 DARTS 结合，通过 backpropagation-with-reconstruction 算法仅存储最后一层输出，使 Transformer 架构搜索可用大 hidden size 和丰富候选操作

## 核心组件

- **Multi-split reversible network**: 输入沿 embedding 维度分为 n 等分，每分经 Gₖ 变换后相加输出，输出可逆重构输入
- **Gₖ = Pooling + Mixed operation search node**: pooling 融合其他 split 信息 → softmax 加权 13-14 种候选操作
- **BP-with-reconstruction (Algorithm 1)**: 反向传播时从顶层输出逐层重构中间输入，仅存最后一层激活。搜索阶段增加 ~33% 计算但省去 O(|O|×n) 存储
- **候选操作集**: Standard Conv (3,5,7,11) + Dynamic Conv (3,7,11,15) + Self/Cross Attention (8 heads) + GLU + FFN + Zero + Identity

## 关键结果

- **WMT'14 En-De base**: 28.4 BLEU vs Transformer 27.7 (+0.7) vs Evolved Transformer 28.2 (+0.2)
- **WMT'14 En-Fr base**: 40.1 BLEU
- **WMT'18 En-Cs base**: 27.9 BLEU vs Transformer 27.0 (+0.9)
- **Big model En-De**: 29.8 BLEU (SOTA)
- **搜索成本**: ~$1,250 (8×V100, 40h) vs Evolved Transformer ~$150,000 (200 TPU)
- **参数效率**: base model (65M) 达到原 Transformer big (210M) 的 BLEU，节省 69% 参数

## 关联页面

- [[zhao2021-memory-efficient-dnas-analysis]] — 12 维度完整分析
- [[zhao2021-memory-efficient-dnas-method]] — Multi-split reversible / BP-with-reconstruction / DARTS 算法详解
- [[zhao2021-memory-efficient-dnas-results]] — WMT'14/WMT'18 完整实验数据
- [[zhao2021-memory-efficient-dnas-critical]] — 贡献·知识点·局限·可迁移·研究机会
- [[autoformer]] — 同样使用 DARTS 搜索 Transformer 架构（CV 领域）
- [[hat]] — HAT: 进化-based NAS for Transformer，方法论对比
