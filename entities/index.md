# Entities Index

> 模型、算法、组织、数据集、人物 — wiki 中引用的所有实体。

## 模型 (Models)

### 大语言模型
- [[switch-transformer]] — Switch Transformer: MoE k=1 routing, 万亿参数, 4× T5-XXL 加速
- [[gshard]] — GShard: 自动分片+条件计算, 600B MoE Transformer
- [[mixtral-8x7b]] — Mixtral 8×7B: 8 专家 Top-2, 首个开源实用级 MoE LLM
- [[deepseek-moe]] — DeepSeekMoE: 细粒度专家分割+共享专家隔离
- [[glm-5]] — GLM-5.0: 全球第四、开源第一 (AI Index v4.0)
- [[hydroglm]] — HydroGLM: 水利水电行业大模型, 总评 88.6 碾压 DeepSeek

### 语义分割模型
- [[u-net]] — U-Net: Encoder-decoder + skip connections, 小样本语义分割
- [[pspnet]] — PSPNet: 金字塔池化, ImageNet 2016 场景解析冠军
- [[deeplabv3plus]] — DeepLabv3+: ASPP encoder + simple decoder, VOC 89.0%
- [[hrnet]] — HRNet: 高分辨率并行卷积, Cityscapes 81.6%
- [[segformer]] — SegFormer: Hierarchical Transformer + MLP decoder

### NAS 模型
- [[hat]] — HAT: 首个 Hardware-Aware NAS for Transformer
- [[autoformer]] — AutoFormer: 首个 ViT 专用 NAS, one-shot supernet
- [[nas-bert]] — NAS-BERT: BERT 压缩 NAS, 5M-60M task-agnostic

## 物理信息结构响应模型
- [[seisgpt]] — SeisGPT: 质量–刚度图 + SDG-Mixer，多建筑预训练、LoRA 个性化与稀疏传感器重建

## 算法 (Algorithms)
- [[te-nas]] — TE-NAS: Training-free NAS via NTK + 线性区域
- [[avbd]] — AVBD: Augmented Lagrangian VBD，硬约束物理仿真
- [[phylstm2]] — PhyLSTM2: 双 LSTM, physics-constrained 非线性滞回元模型
- [[phylstm3]] — PhyLSTM3: 三 LSTM, 增强非线表征
- [[bouc-wen-model]] — Bouc-Wen: 率相关滞回模型
- [[pseudo-time-stepping]] — 伪时间步进: PINN PDE 残差伪解解决方案
- [[cm-pinns]] — CM-PINNs: 本构模型约束 PINN，预测非线性结构地震响应

## 组织 (Organizations)
- [[zhipu-ai]] — 智谱AI: GLM/ChatGLM 系列大模型
- [[guoneng-bigdata]] — 国能大数据: HydroGLM 总体架构
- [[daduhe-company]] — 大渡河公司: 水利水电业务落地
- [[tsinghua-dhe]] — 清华大学水利系: 水利专业支持

## 数据集 (Datasets)
- [[nasbench201]] — NAS-Bench-201: 15,625 架构 NAS benchmark
- [[ade20k]] — ADE20K: 场景解析 benchmark, 150 类
- [[cityscapes]] — Cityscapes: 城市场景理解, 19 类
- [[peer-strong-motion-database]] — PEER: 强震记录数据库
