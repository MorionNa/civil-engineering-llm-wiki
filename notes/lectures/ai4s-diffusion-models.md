---
title: "扩散生成模型：从物理原理到蛋白质设计（AI4S 第二讲）"
created: 2026-06-11
updated: 2026-06-11
type: lecture
tags: [diffusion-models, ddpm, ddim, stable-diffusion, latent-diffusion, score-based-models, langevin-dynamics, classifier-free-guidance, lora, dpo, controlnet, protein-design, rfdiffusion, protpainter, alphafold3, se3-equivariance, ai4s, scientific-discovery]
sources: [raw/articles/diffusion-models-ai4s-lecture2-bilibili.md]
methods: [diffusion-models, ddpm, ddim, stable-diffusion, latent-diffusion, score-based-models, langevin-dynamics, classifier-free-guidance, lora, dpo, controlnet]
confidence: high
---

# 扩散生成模型：从物理原理到蛋白质设计

> **来源：** [B站 BV15t5m68E3w](https://www.bilibili.com/video/BV15t5m68E3w) | 主讲：章敏（浙江大学 × Datawhale × 魔搭社区）
> **活动：** Hello Universe! AI4S 第一课 VOL.04

---

## 核心内容

### 一、扩散模型的物理直觉

扩散模型的核心思想来自**非平衡热力学**：

| 过程 | 描述 | 类比 |
|------|------|------|
| **正向（破坏）** | 逐步加高斯噪声 → 纯随机噪声 | 热力学第二定律：墨水在水中扩散，熵增 |
| **反向（创造）** | 从噪声逐步去噪 → 恢复清晰图像 | 逆转时间，墨水重新聚集成一滴 |

### 二、发展简史

```
2015 — 非平衡热力学 + 深度学习 (Sohl-Dickstein)
2019 — Score-Based Generative Modeling (Song & Ermon)
2020 — DDPM (Ho et al.)
2021 — SDE / Classifier Guidance (Song / Dhariwal & Nichol)
2022 — Latent Diffusion / Stable Diffusion (Rombach)
2023+ — RFDiffusion / DALL-E 3 / Sora / ControlNet / Suno
```

### 三、数学核心

**Score Function（数据的引力场）：**
$$s(x) = \nabla_x \log p(x)$$

将数据分布想象成一座山——山顶=真实图片（高概率），山脚=噪声（低概率）。Score function 是山坡的坡度向量场，告诉每个点"往哪里最快到达山顶"。神经网络学习这个梯度场。

**Langevin Dynamics 采样：**
$$x_{t+1} = x_t + \varepsilon_t \cdot \nabla_x \log p(x) + \sqrt{2\varepsilon_t} \cdot z_t$$

随机行走 + 梯度指引 = 从任意噪声点沿梯度"爬回"数据流形。

**DDPM 前向过程（一步直达）：**
$$x_t = \sqrt{\bar{\alpha}_t} \cdot x_0 + \sqrt{1 - \bar{\alpha}_t} \cdot \varepsilon$$

核心优点：无需逐步迭代，可直接采样任意时刻 t，训练效率提升数个数量级。

**训练目标（猜噪声游戏）：**
$$\mathcal{L} = \|\varepsilon - \varepsilon_\theta(x_t, t)\|^2$$

给网络一张加了噪的图，问"我加了什么噪？"猜得越准（$\varepsilon_\theta \approx \varepsilon$），去噪能力越强。训练时随机选择 t，使网络学会在所有噪声水平上都准确预测。

**DDIM 加速：** 从 1000 步降到 50 步，画质几乎无损——反向过程可视为确定性的 ODE。

### 四、Stable Diffusion 架构革新

三阶段工作流：

| 阶段 | 组件 | 作用 |
|------|------|------|
| 感知压缩 | VAE Encoder | 像素空间 → 潜空间（48×压缩），计算量减 16-64 倍 |
| 潜空间扩散 | U-Net | 在 latent space 加噪/去噪，消费级显卡即可运行 |
| 感知重建 | VAE Decoder | 潜向量 → 高清像素图像 |

**U-Net 关键设计：**
- U 型结构：左编码（提取特征）→ 右解码（恢复细节）
- Skip Connections：像高速公路直传低级特征
- Cross-Attention：每层"询问"CLIP 文本编码器——"Prompt 说什么？"

**CLIP：** OpenAI 用 4 亿对 (图像, 文本) 训练，让配对的图文在向量空间靠近，实现文本→图像的语义桥梁。

### 五、精准控制与微调

| 技术 | 原理 | 特点 |
|------|------|------|
| **CFG** | 平衡无条件/有条件生成的"温差"：$w \times (Cond - Uncond)$ | w≈7 为甜点 |
| **LoRA** | 低秩分解 $\Delta W = BA$，只训练极小矩阵 | 参数减少 >10,000× |
| **DPO** | 直接在偏好数据上优化，跳过奖励模型和 PPO | 价值观对齐，从"能"到"好" |
| **ControlNet** | 复制 U-Net Encoder 作为控制层 | 空间条件：边缘图、姿态、深度 |
| **DreamBooth** | 微调整个 U-Net 绑定特定主体 | 效果好，文件大 |

### 六、前沿案例：蛋白质设计

**RFDiffusion (Baker Lab)：**
- 将扩散模型从像素空间拓展到 **SE(3) 空间**（旋转+平移），生成 3D 原子坐标
- 应用：结合剂设计、骨架 scaffold、对称复合物
- 传统方法数天→数周，RFDiffusion 数小时→分钟

**ProtPainter (Jia Lab)：**
- 拓扑引导：精确控制蛋白质折叠方式
- Draw or Drag：在 3D 空间中"画"曲线或拖拽结构，模型自动调整原子坐标保持物理合理性

**AlphaFold 3 范式转变：**

| | AF2 | AF3 |
|--|-----|-----|
| 结构模块 | IPA（等变注意力） | **Diffusion Module** |
| 原子级别 | IPA 内置 | SE(3) 等变 |
| 多分子 | 仅蛋白质 | 蛋白质+DNA+RNA+配体 |
| 核心范式 | Transformer 编码 | 扩散去噪（坐标空间） |

### 七、开放挑战

- **采样速度：** 50+ 步仍需时间，实时生成困难
- **安全与版权：** 潜在生物危害；训练数据含版权作品
- **对齐/可控性：** 细粒度控制不稳定的幻觉
- **因果性问题：** 扩散模型学习统计相关性 ≠ 物理因果律（如蛋白质折叠不一定符合内生物理规律）

---

## 核心知识点

1. **扩散模型 = 热力学 + 深度学习**：正向加噪（熵增）+ 反向去噪（创造秩序）
2. **Score Function 是本质**：学习数据分布的梯度场，而非直接生成
3. **一步直达公式是关键突破**：$\sqrt{\bar{\alpha}} \cdot x_0 + \sqrt{1-\bar{\alpha}} \cdot \varepsilon$ 让训练可行
4. **Latent Diffusion 是工程突破口**：压缩 48 倍让消费级显卡可用
5. **CFG + LoRA + DPO 构成完整控制栈**：从指令遵循到风格微调到价值观对齐
6. **蛋白质设计是 AI4S 标杆案例**：SE(3) 空间扩散 + 物理约束 = 从头设计新蛋白
7. **AlphaFold 3 用 Diffusion 替代 IPA**：范式从 Transformer 编码转向扩散去噪

---

## 可迁移知识

| 知识点 | 如何迁移 |
|--------|---------|
| 一步直达加噪公式 | 任何需要时序数据增强的场景可用此技巧加速训练 |
| Latent Space 压缩思路 | 高维问题先压缩再建模，适用于 PDE 求解、分子模拟 |
| LoRA 低秩微调 | 任何大模型微调场景——PINN、蛋白质模型、物理模拟模型 |
| DPO 偏好对齐 | 从"能求解"到"解得漂亮"的优化——PDE 求解器生成网格质量、物理合理性 |
| SE(3) 等变扩散 | 3D 物理场景（分子动力学、机器人操作、流体模拟）的生成建模 |
| CFG 温度控制 | 物理约束强度的可调参数——PINN 的边界条件权重自适应 |

---

## 关联

- [[ai4s-pinn-deepxde-tutorial]] — PINN 入门到实战（AI4S 第一讲）
- [[zhang2020-phylstm-analysis]] — PhyLSTM 物理约束学习
- [[wang2023-pinn-spurious-analysis]] — PINN 训练失败模式
