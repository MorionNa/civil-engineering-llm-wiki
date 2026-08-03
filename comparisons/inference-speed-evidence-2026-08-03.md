---
id: comparison--inference-speed-evidence-2026-08-03
title: 推理效率证据：学习模型、物理 oracle 与 OpenSeesPy 缺口
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/computational-mechanics
- domain/ai4s
- method/parallel-computing
- method/evaluation
- evidence/report
keywords:
- inference speed
- OpenSeesPy
- vectorized RK4
- 50kDOF
- Newton-Raphson
sources:
- ../../../outputs/remote_temporal_parallel_dynamicprojection75_scale_speed_v2_20260731cp/scale_speed_v2.json
- ../../../outputs/remote_temporal_parallel_multiscale_modal1188_broadband2_hfjoint_width100_independentforcehinge40tail20_frombs150_v2_20260731bu/metrics_official90_spectral.json
- ../../../outputs/remote_temporal_parallel_dynamicprojection75_selected_full_v2_20260731cm/metrics_official90_spectral.json
- ../../../outputs/remote_v21_m0_fast_20260802/metrics_v2.json
- ../../../docs/plans/mtp_mechconv_v2_implementation_log_2026-07-31.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# 推理效率证据：学习模型、物理 oracle 与 OpenSeesPy 缺口

## 当前答案

目前不能声称推理效率已经满足“快于 OpenSeesPy”。项目中没有按相同结构、步数、硬件、精度和输出范围完成 OpenSeesPy 正式对比。已有速度数字只能说明模型自身可运行，或者与另一种参考求解器的相对关系。

## 已有可核验时间

| 路径 | 规模与步数 | 时间 | 可以说明什么 | 不能说明什么 |
|---|---:|---:|---|---|
| MTP-bu | 5DOF，90 cases × 1501 steps | 0.348183 s | 批量推理吞吐较高 | 未包含 OpenSeesPy 同任务计时，不能给出 speedup |
| TemporalParallel α=0.75 | 5DOF，90 × 1501 | 0.576677 s | MTP-bu 对同类 parent 更快约 1.66× | 不是对传统求解器的证明 |
| V21 physical oracle | 50DOF，1501 steps | warm 0.619668 s；cold 0.645267 s | 顺序物理 oracle 的本机时间 | 它不是学习模型，也不是 OpenSeesPy |

## 大规模执行基准

α=0.75 checkpoint 在 50/500/5k/50kDOF、65 步的 grouped-halo 路径上可执行，直接前向中位时间依次为 0.00446/0.01278/0.15198/1.51098 s；优化向量化 Bouc–Wen RK4 参考为 0.00265/0.00406/0.01568/0.13248 s。按“参考时间/神经模型时间”定义，50kDOF speedup 仅为 0.088×，即神经路径约慢 11.4×。

该结果是明确的负证据：**规模增大本身尚未带来速度优势**。同时，该次大规模路径的边力与独立物理误差也未达标，因此不能从节点响应随规模改善推导出合格的大规模替代求解器。

## 仍可能成立、但尚未验证的场景

用户提出的合理目标场景是 OpenSeesPy 在强非线性下需要较多 Newton–Raphson 迭代、回退步长或收敛重试，而学习模型保持固定前向成本。这个命题需要专门预注册：

1. 固定一个结构一个模型，固定本构、荷载、时间步和输出量；
2. 同时计入模型数据搬运与必要前后处理，排除 checkpoint 加载；
3. OpenSeesPy 报告每步迭代数、失败/重试数和收敛容差；
4. 按迭代次数分层报告 crossover，而不是只选最慢样本；
5. 只有精度门先通过的 case 才计入速度优势。

这套协议应与 [[one-structure-one-model-contract-2026-08-03]] 和 [[reproduction-failure-prevention-contract-2026-08-03]] 联用。当前结论保持 fail-closed：OpenSeesPy 速度优势尚未建立。

## Provenance

^[../../../outputs/remote_temporal_parallel_dynamicprojection75_scale_speed_v2_20260731cp/scale_speed_v2.json] ^[../../../docs/plans/mtp_mechconv_v2_implementation_log_2026-07-31.md]
