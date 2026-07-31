---
id: papers--xiong2025-confseq-results
title: ConfSeq 实验结果：四大任务全面 SOTA
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- evidence/paper
keywords:
- 3d-molecular-generation
- drug-discovery
- molecular-conformation
- virtual-screening
sources:
- sources/papers/xiong2025-confseq.md
created: '2026-06-24'
updated: '2026-07-31'
confidence: high
---

# ConfSeq 实验结果

> 来源：`[[xiong2025-confseq-analysis]]` | 本节展开第 6 维度

## 任务一：3D 构象预测 (GEOM-Drugs)

### 关键指标

| 模型 | COV-P ↑ | COV-R ↑ | MAT-P ↓ (Å) | MAT-R ↓ (Å) |
|------|---------|---------|-------------|-------------|
| Tor. Diff. (前 SOTA) | 47.9% | 63.3% | 0.86 | 0.73 |
| **ConfSeq** | **58.4%** | **64.5%** | **0.77** | **0.72** |
| 提升 | **+10.5 pp** | +1.2 pp | **-0.09** | -0.01 |

**COV-P 领先 10.5 个百分点——架构改进产生最大收益在 Precision 上。**

### 按可旋转键数分析
不同键数范围下 ConfSeq 一致最优（参见 Supplementary Fig. 1-2）。在 <1Å 和 <1.5Å 阈值下的 Coverage 均最高。

### 温度控制实验
`MAT-P vs MAT-R` 曲线在左下角——无论偏好 Precision 还是 Coverage，ConfSeq 都提供最优解。

## 任务二：无条件 3D 分子生成 (GEOM-Drugs)

### 2D 指标

| 模型 | Validity V(%) | Uniqueness U(%) | V×U(%) |
|------|-------------|----------------|--------|
| EDM | 84.95 | 100.00 | 84.95 |
| GeoLDM | 87.18 | 99.98 | 87.16 |
| GCDM | 95.24 | 98.52 | 93.83 |
| **ConfSeq** | **99.87** | **99.00** | **98.87** |
| 训练集 | 97.88 | 98.14 | 96.06 |

**接近 100% 化学有效性**，远超所有扩散基线。

### 3D 质量

| 模型 | PB-validity ↑ | min RMSD ↓ | 二面角 MMD ↓ | 键角 MMD ↓ |
|------|-------------|------------|------------|----------|
| EDM | 25.84 | 0.1884 | 0.03541 | 0.4215 |
| GeoLDM | 39.77 | 0.1505 | 0.00620 | 0.0899 |
| GCDM | 77.40 | 0.1044 | 0.00502 | 0.0607 |
| **ConfSeq** | **83.00** | **0.1024** | **0.00040** | **0.0546** |
| 训练集 | 92.30 | 0.1143 | 0.00016 | 7.7e-5 |

### 采样速度

| 模型 | 速度 (s/mol) |
|------|-------------|
| EDM | 9.64 |
| GeoLDM | 37.62 |
| GCDM | 42.20 |
| **ConfSeq** | **0.019** |
| **加速比** | **~500—2200×** |

### 理化性质分布
QED、SAS、LogP、TPSA 分布均最接近训练集；ChemNet 嵌入和 E3FP 指纹的 Frechet 距离最小。

## 任务三：形状条件 3D 分子生成 (MOSES)

- 生成分子满足 2D 有效性 ≈ 100%
- PB-validity 最高
- 形状相似性和 2D 相似性均优于 SQUID 和 ShapeMol

## 任务四：3D 分子表征学习

### PDB 配体聚类
UMAP 可视化显示三大簇：簇 A (激酶抑制剂，芳香性高)、簇 B (蛋白酶抑制剂，柔性大)、簇 C (糖苷酶抑制剂，极性高)。

### 虚拟筛选

| 指标 | 数据集 | ConfSeq | E3FP | SHAFTS | LSalign |
|------|--------|---------|------|--------|---------|
| AUC | DUDE | **0.76** | 0.49 | 0.42 | 0.40 |
| BEDROC | DUDE | **0.41** | 0.14 | 0.08 | 0.08 |
| 5.0% EF | DUDE | **7.12** | 2.61 | 2.26 | 1.52 |
| AUC | PCBA | **0.60** | 0.53 | 0.37 | 0.40 |

### 超大规模虚拟筛选
预计算 **9800 万 PubChem** 3D 嵌入，单 CPU **1 分钟**完成全库相似性搜索。

## 药物发现案例

发现多个新型抑制剂：
- **STING 抑制剂**：IC₅₀ = 0.338–3.51 μM
- **ALDH1B1 抑制剂**：活性水平具体数值见正式发表版

## Evidence By Source

### `sources/papers/xiong2025-confseq.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1101_2025.05.07.652440.pdf`

^[sources/papers/xiong2025-confseq.md]

## Related Indexes

- [[papers/index]]
