# Mamba-3 结果

## Language Modeling

论文在 FineWeb-Edu 100B token 训练设置下比较 Mamba-3、Mamba-2、Gated DeltaNet 和 Transformer。

主要结论：

- Mamba-3 SISO 优于已有线性模型；
- Mamba-3 MIMO 在 SISO 基础上进一步提升；
- 在相同性能下可使用更小 state size。

## State Tracking

在 parity 和 modular arithmetic 等任务中，数据依赖 RoPE 的复值状态版本显著提升状态跟踪能力。

## Efficiency

MIMO 通过提高 arithmetic intensity，在增加计算量的同时保持接近的 decode latency。

## 局限

- 主要验证集中于语言模型；
- 固定状态模型仍存在部分检索能力不足；
- 科学计算任务尚未验证。
