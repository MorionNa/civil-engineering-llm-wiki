---
id: papers--dai2024-deepseek-moe-method
title: Dai et al. (2024) — DeepSeekMoE 方法展开
type: paper-analysis
status: active
project: civil-engineering-llm-wiki
tags:
- domain/llm
- evidence/paper
- method/transformer
keywords:
- gating-network
- load-balancing
- mixture-of-experts
- sparse-moe
- top-k-routing
sources:
- sources/papers/dai2024-deepseek-moe.md
created: '2026-06-13'
updated: '2026-07-31'
confidence: high
---

# DeepSeekMoE 方法机制

← 返回总览：[[dai2024-deepseek-moe-analysis]]

## 架构演进（Figure 1）

```
(a) 传统 Top-2 Routing (GShard)
    N 个全尺寸专家，每个 token 激活 K=2 个
    组合数：C(16,2) = 120

(b) + 细粒度专家分割
    每个专家拆成 m 个 (m=4)，共 mN 个更小专家
    激活 mK 个，保持总计算量不变
    组合数：C(64,8) ≈ 4.4×10⁹

(c) + 共享专家隔离 (= DeepSeekMoE)
    新增 Ks 个共享专家（始终激活）
    路由专家 = mN - Ks，激活 K' = mK - Ks
```

## 细粒度专家分割（Fine-Grained Expert Segmentation）

### 动机
专家数量有限时，分配给同一专家的 token 覆盖多样知识类型，导致专家参数混杂、难以高效利用。

### 实现
将每个 FFN 专家的中间隐藏维度缩小为 1/m：
- 专家参数量不变（N 个全尺寸 = mN 个 1/m 尺寸）
- 激活专家数从 K 增加到 mK
- 计算量不变（mN × 1/m × K × m = N × K × original）

### 公式

```
h_t^l = Σ_{i=1}^{mN} g_{i,t} · FFN_i(u_t^l) + u_t^l

g_{i,t} = s_{i,t}  if s_{i,t} ∈ Topk({s_{j,t} | 1≤j≤mN}, mK)
          0       otherwise

s_{i,t} = Softmax_i(u_t^l · e_i^l)
```

### 组合灵活性
以 N=16, m=4 为例：从 120 种可能组合 → 44 亿种，显著提升知识获取的精确性和针对性。

## 共享专家隔离（Shared Expert Isolation）

### 动机
不同 token 可能需要共同知识（如语法、基础语义），导致多个路由专家重复学习 → 参数冗余。

### 实现
隔离 Ks 个专家为共享专家，无论路由结果如何，每个 token 必定经过它们。路由专家数量减少 Ks 以保持计算量不变。

### 完整 DeepSeekMoE 公式

```
h_t^l = Σ_{i=1}^{Ks} FFN_i(u_t^l)                    ← 共享专家（始终激活）
      + Σ_{i=Ks+1}^{mN} g_{i,t} · FFN_i(u_t^l)      ← 路由专家（Top-K 激活）
      + u_t^l

g_{i,t} = s_{i,t}  if s_{i,t} ∈ Topk({s_{j,t} | Ks+1≤j≤mN}, mK-Ks)
          0       otherwise
```

与 GShard 的关系：共享专家隔离的原型可追溯到 Rajbhandari et al. (2022) 和 Elbayad et al. (2023)，但 DeepSeekMoE 从不同角度（专家特化）推导出该策略。

## 负载均衡（Load Balance）

采用 **expert-level balance loss**（同 Shazeer et al., 2017）：

```
L_Bal = α · Σ_{i=1}^{N'} f_i · P_i

f_i = (N' / K'T) · Σ_t 1(Token t selects Expert i)   ← 实际选择频率
P_i = (1/T) · Σ_t s_{i,t}                              ← 平均路由概率
```

其中 α 为平衡因子（2B: 0.01, 16B: 0.001），N' = mN - Ks，K' = mK - Ks。

## 模型配置

### DeepSeekMoE 2B（验证实验）
| 参数 | 值 |
|------|-----|
| Transformer 层数 | 9 |
| 隐藏维度 | 1280 |
| 总专家参数 | 16× 标准 FFN |
| 激活专家参数 | 2× 标准 FFN |
| 共享专家 | 1 |
| 路由专家 | 63 (m=4 分割) |
| 激活路由专家 | 7 (mK-Ks=8-1) |
| 总参数 | ~2B |
| 激活参数 | ~0.3B |
| 训练 token | 100B |
| 词表大小 | 8K (BPE) |

### DeepSeekMoE 16B（扩展实验）
| 参数 | 值 |
|------|-----|
| Transformer 层数 | 28 |
| 隐藏维度 | 2048 |
| MoE 层 | 第 2-28 层（第 1 层用密集 FFN） |
| 共享专家 | 2 |
| 路由专家 | 64 (m=4) |
| 激活路由专家 | 6 |
| 总参数 | ~16.4B |
| 激活参数 | ~2.8B |
| 训练 token | 2T |
| 词表大小 | 100K (BPE) |
| FLOPs per 4K tokens | 74.4T (vs Llama2 7B: 187.9T) |

## 关键设计决策

1. **第 1 层不用 MoE**：观察到首层负载均衡收敛特别慢，保留密集 FFN
2. **所有其他 FFN 替换为 MoE**：最大化参数效率
3. **平衡因子随规模递减**：2B 用 α=0.01，16B 用 α=0.001
4. **中英双语训练**：corpus 涵盖英文和中文，tokenizer 100K 词表

← 返回总览：[[dai2024-deepseek-moe-analysis]]
→ 实验结果：[[dai2024-deepseek-moe-results]]

## Evidence By Source

### `sources/papers/dai2024-deepseek-moe.md`

- Key point: 本页内容由所列来源整理；跨领域应用明确作为迁移推论或研究建议。
- Evidence location: 详见正文中的章节、表格、公式与可复现性说明。
- Original material: `raw/papers/dai2024_deepseek_moe.pdf`

^[sources/papers/dai2024-deepseek-moe.md]
