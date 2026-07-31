---
id: papers--goswami2022-variational-deeponet-results
title: Goswami et al. (2022) — 结果证据展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/ai4s
- evidence/paper
- method/neural-operator
- method/pinn
keywords:
- brittle-fracture
- crack-path-prediction
- deeponet
- interpolation-extrapolation
- phase-field-fracture
- physics-informed
- surrogate-model
sources:
- sources/papers/goswami2022-variational-deeponet.md
created: '2026-06-27'
updated: '2026-07-31'
confidence: high
results:
- single-edge-notch-tension
- l-shape-panel
- interior-crack
- edge-crack
- relative-l2-error
- interpolation
- extrapolation
datasets:
- phase-field-fracture-benchmarks
---

# Goswami et al. (2022) — 结果证据展开

> 返回概述 → [[goswami2022-variational-deeponet-analysis]]

## 验证基准

| 基准 | 描述 | 关键挑战 |
|------|------|---------|
| 单边缺口拉伸试验 (Single-Edge Notch) | 矩形板单侧预制裂纹，顶部拉伸 | 经典 I 型裂纹，裂纹路径简单但应力集中强 |
| L 形面板 (L-Shape Panel) | L 形混凝土面板，顶部加载 | 复杂几何，裂纹路径弯曲，考验模型空间泛化 |

### 输入参数空间

训练时覆盖初始裂纹的 **位置** 和 **长度** 变化：
- 边缘裂纹：裂纹位于边界不同位置
- 内部裂纹：裂纹位于内部不同位置 + 不同倾角
- 测试时：内插（训练域内新裂纹配置）+ 外推（训练域外裂纹配置）

---

## 核心结果

### 1. V-DeepONet 预测精度

| 指标 | 内插任务 | 外推任务 |
|------|---------|---------|
| 损伤场 d 的相对 L2 误差 | **低** (< 3%) | 中 (< 8%) |
| 位移场 u 的相对 L2 误差 | **低** (< 2%) | 中 (< 6%) |
| 裂纹路径一致性 | 优秀 | 良好 |

> **关键发现：** V-DeepONet 在内插任务上接近高保真 FEM 精度，在外推任务上保持可用精度。物理变分约束是外推泛化的关键——纯数据驱动方法外推严重退化。

### 2. 混合训练 vs 纯数据驱动

| 训练策略 | 数据量 | 内插误差 | 外推误差 | 物理合理性 |
|---------|-------|---------|---------|-----------|
| 纯数据驱动 DeepONet | 大量 | 中 | **高** | 弱 |
| 纯物理驱动 V-DeepONet | 0 | 不稳定 | 高 | 中等（可能收敛到局部极小） |
| **混合训练 V-DeepONet** | **少量** | **低** | **中** | **强** |

> 物理能量约束 = 正则化器 + 数据增强器，在数据稀缺下至关重要。

### 3. 单边缺口拉伸 — 裂纹路径

V-DeepONet 预测的损伤场显示：
- 裂纹从缺口尖端起始，沿水平方向扩展（I 型断裂的预期行为）
- 预测的损伤带宽度和位置与 FEM 结果高度一致
- 不同初始缺口长度下的裂纹路径均能正确捕捉
- 在外推至训练域外更长的缺口时，裂尖位置预测略有偏差但路径方向正确

### 4. L 形面板 — 弯曲裂纹路径

- L 形面板内角处应力集中引发裂纹，路径呈弯曲轨迹
- V-DeepONet 成功复现弯曲裂纹路径
- 损伤场的空间分布（裂纹带位置和宽度）与 FEM 良好吻合
- 证明 V-DeepONet 可处理非直线裂纹的复杂拓扑

### 5. 推理效率

| | 高保真 FEM | V-DeepONet |
|---|---|---|
| 单次求解时间 | 分钟级（高分辨率网格） | **毫秒级**（一次前向传播） |
| 参数扫描 | 每次重跑 | 一次训练覆盖全部 |
| 裂纹配置泛化 | ✗ 无法泛化 | ✓ 即时预测 |

---

## 与 PINN 类方法的结果特点对比

| | V-DeepONet | PINN (如 [[wang2023-pinn-spurious-analysis]]) |
|---|---|---|
| 输出范型 | 函数 → 函数映射（算子） | 单函数解 |
| 参数变化 | 一次训练覆盖 | 需重新训练 |
| 物理约束 | 变分能量 | PDE 残差 |
| 伪解风险 | 低（能量最小化） | 中-高（残差可小而解错） |

---

## 关联

- [[goswami2022-variational-deeponet-analysis]] — 概述
- [[goswami2022-variational-deeponet-method]] — 方法展开
- [[deeponet]] — DeepONet 神经算子
- [[wang2023-pinn-spurious-analysis]] — PINN 物理约束对比

## Evidence By Source

### `sources/papers/goswami2022-variational-deeponet.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/10_1016_j_cma_2022_114587_extracted.txt`

^[sources/papers/goswami2022-variational-deeponet.md]
