---
title: "BossNAS 方法细节：Ensemble Bootstrapping 与 HyTra 搜索空间"
created: 2026-06-14
updated: 2026-06-14
type: paper-analysis
tags: [neural-architecture-search, ensemble-bootstrapping, hybra-search-space, block-wise-training, self-supervised, byol]
sources: [raw/papers/bossnas2021_iclr.pdf]
confidence: high
---

# BossNAS: 方法机制深度解析

> 回主分析页：[[li2021-bossnas-analysis]]

---

## 1. 问题形式化：NAS 的困境

**权重共享 NAS 的数学形式：**

设搜索空间 A，超级网络权重 W。训练阶段：
$$W^* = \arg\min_W \mathcal{L}_{\text{train}}(W, \mathcal{A}; x, y)$$

搜索阶段：
$$\alpha^* = \arg\min_{\forall\alpha\in\mathcal{A}} \mathcal{L}_{\text{val}}(W^*, \alpha; x, y)$$

**核心困境**：基于共享权重 $W^*$ 的架构排名不代表真实排名，因为权重高度纠缠且未对每个候选公平优化 [58, 73, 80]。

---

## 2. 块级分解：缩小权重共享空间

块级方案 [37, 46] 将超级网络在深度维度切分为 |k| 个块：
$$S(W, \mathcal{A}) = \{S_k(W_k, \mathcal{A}_k)\}$$

每个块的搜索：$\alpha^* = \{\alpha_k\}^* = \arg\min_{\forall\{\alpha_k\}\subset\mathcal{A}} \sum_{k=1}^{|k|} \lambda_k \mathcal{L}_{\text{val}}(W_k^*, \alpha_k; x_k, y_k)$

权重共享空间从 $|\mathcal{A}|$ 缩小为 $\sum_k |\mathcal{A}_k|$（对 HyTra：16 层 → 4 块 × 4 层/块，每块最多 $2^4 \times 2^4 = 256$ 候选，而非整个 $2.8\times 10^6$）。

**教师偏见问题**：中间目标 $\{x_k, y_k\}$ 由固定教师网络 T 生成——$x_1 = x$，$y_1 = T_1(x)$；$x_k = T_{k-1}(x)$，$y_k = T_k(x)$，这导致架构评分偏向教师架构。

---

## 3. Ensemble Bootstrapping 训练方案

### 3.1 Siamese 超级网络

受 BYOL [21] 启发，构建双超级网络对：
- **在线网络** $S(W, \mathcal{A})$：标准梯度更新
- **EMA 网络** $T(W^\bullet, \mathcal{A})$：指数滑动平均 $W^\bullet_t = \tau W^\bullet_{t-1} + (1-\tau)W_t$

两者共享架构空间 $\mathcal{A}$，接收同一图像的两个增强视图 $\{x^1, x^2\}$。

### 3.2 概率集成（核心创新）

在每步训练中，采样 |p| 条路径 $\{\alpha_p\} \subset \mathcal{A}_k$。关键操作：

**EMA 网络生成集成目标：**
$$\widehat{T}_k(\{\alpha_p\}; \{x'_p\}) = \frac{1}{|p|} \sum_{p=1}^{|p|} T_k(W^\bullet, \alpha_p; x'_p)$$

**在线网络每条路径学习预测该集成：**
$$\mathcal{L}_{\text{train}} = \left\| S_k(W_k, \alpha_p; x_p) - \widehat{T}_k(W^\bullet_k, \{\alpha_p\}; \{x'_p\}) \right\|_2^2$$

**为什么要集成？** 没有集成时，每条路径 bootstrap 自己的 EMA 版本 —— 权重共享导致优化目标不一致，训练不稳定。集成提供了**所有路径共享的优化目标**，使权重共享下的多条路径协调收敛。

### 3.3 隐空间投影

为避免增强（如 random crop）导致的逐像素差异影响训练，以及保证不同感受野/分辨率候选的泛化性，将中间表示投影到隐空间后再计算 L2 距离。

---

## 4. 无监督架构评估：向种群中心搜索

### 4.1 为什么对比学习 loss 不能直接 rank？

对比学习的 loss 反映的是表示学习质量，但不等价于架构在下游任务上的性能。此外，输入视图和目标是随机采样的，存在方差。

### 4.2 种群中心评估

对于块级搜索空间 $\mathcal{A}_k$（通常 256 个候选），遍历所有架构（而非采样子集）：

**种群概率集成：**
$$\widehat{S}_k(\mathcal{A}_k; x^2) = \frac{1}{|\mathcal{A}_k|} \sum_{\alpha\in\mathcal{A}_k} S_k(\alpha; x^2)$$

**每个架构的评分（到中心的距离）：**
$$\mathcal{L}_{\text{val}}(\alpha; x) = \|S_k(\alpha; x^1) - \widehat{S}_k(\mathcal{A}_k; x^2)\|_2^2$$

**最终搜索（各块评分加权求和）：**
$$\alpha^* = \arg\min_{\forall\alpha\in\mathcal{A}} \sum_{k=1}^{|k|} \lambda_k \mathcal{L}_{\text{val}}(\alpha; x_k)$$

其中 $\{\lambda_k\}$ 可通过线性回归从少量样本中学习（类似 DONNA [46]）。

这样做有两重去偏：一组固定增强视图（$\{x^1, x^2\}$ 对所有候选相同）→ 消除增强方差；所有架构与同一中心比较 → 公平。

---

## 5. HyTra 混合搜索空间设计

### 5.1 候选构建块

| 块类型 | 组件 | 复杂度 |
|---------|------|--------|
| **ResConv** | 3×3 卷积残差瓶颈（ResNet 风格） | O(C² + HW·C²) |
| **ResAtt** | 多头自注意力 + 隐式位置编码（深度可分离卷积），去掉 BoTNet 的显式 content-position 分支 | O(HW·C²) |

**隐式位置编码的创新**：将 CPVT 的块间位置编码思想与 BoTNet 结合，用 3×3 深度可分离卷积替代乘法位置编码，计算量从 O(CW³) 降至 O(CW²)，且该模块同时负责下采样。

### 5.2 Fabric-like 网络结构

HyTra 的设计灵感来自 Convolutional Neural Fabrics [57]：

- 共 L=16 层 choice block（与 ResNet-50 对齐）
- 起始为 ResNet stem（7×7 卷积 + max pooling，降采样至 1/4）
- 每层可选择保持分辨率或降采样 2×（最低至 1/32）
- Transformer 块（ResAtt）仅在后两个尺度（1/16, 1/32）可用（因早期大分辨率时自注意力计算量过重）
- 总架构数 ≈ 2.8×10⁶

该搜索空间同时包含纯 CNN（ResNet-50 风格）、纯 Transformer（ViT 风格，固定序列长度）和混合架构（BoTNet 风格）。

### 5.3 块级划分

将 16 层分为 4 块，每块 4 层。每块内候选为 {ResConv, ResAtt} × {keep, downsample}，共 4⁴=256 个候选架构。权重仅在块内共享。

---

## 6. 训练与搜索流程

### 6.1 超参配置

| 配置项 | 值 |
|--------|-----|
| 每块训练 epoch | 20（ImageNet）/ 30（CIFAR） |
| 每步采样路径数 |p| | 4 |
| 优化器 | LARS |
| 基础学习率 | 4.8（batch 4096） |
| 学习率调度 | cosine decay |
| EMA 动量 τ | 0.996（遵循 BYOL） |
| 增强策略 | BYOL 标准增强 |

### 6.2 搜索后 Retraining

- **BossNet-T (HyTra)：** AdamW, lr=1e-3, cosine, batch=1024, weight decay=0.05, 模型 EMA=0.99996（遵循 DeiT）
- **BossNet-M (MBConv)：** RMSprop, lr=0.256, batch=4096, momentum=0.9（遵循 EfficientNet）

---

*上接 [[li2021-bossnas-analysis]] | 实验结果 [[li2021-bossnas-results]] | 批判分析 [[li2021-bossnas-critical]]*
