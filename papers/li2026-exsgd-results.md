---
title: "ExSGD 实验结果"
created: 2026-07-30
updated: 2026-07-30
type: paper-analysis
---

# Results & Evidence

实验数据：

- WHU-Aerial
- WHU-Sat
- PHB

比较方法：

- Adam
- NAG
- NAdam
- LAMB
- N-LAMB
- AdaBelief
- Shampoo

主要结论：

- ExSGD 在不同 batch size 下均保持较优 F1 和 IoU；
- 在超大 batch 条件下仍保持稳定训练；
- 历史梯度增强和层级学习率两个模块均有效。

论文报告 ExSGD 在三个建筑提取数据集上相比现有优化方法获得最高约 14.3% F1 和 16.56% IoU 提升。