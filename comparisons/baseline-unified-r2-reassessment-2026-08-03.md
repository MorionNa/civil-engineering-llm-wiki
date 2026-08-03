---
id: comparison--baseline-unified-r2-reassessment-2026-08-03
title: PhyLSTM3 与 CM-PINN 的统一 R² 复算
type: comparison
status: active
project: civil-engineering-llm-wiki
tags:
- domain/civil-engineering
- domain/ai4s
- method/pinn
- method/evaluation
- evidence/report
keywords:
- PhyLSTM3
- CM-PINN
- pooled R2
- macro R2
- worst-case R2
sources:
- ../../../reproductions/phylstm/outputs_paper_full/phylstm3_predictions.mat
- ../../../reproductions/phylstm/outputs_paper_full/phylstm3_metrics.json
- ../../../reproductions/cm-pinn/outputs_10000_lbfgs500/predictions.npz
- ../../../reproductions/cm-pinn/outputs_10000_lbfgs500/metrics.json
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# PhyLSTM3 与 CM-PINN 的统一 R² 复算

原复现报告主要使用 relative L2 和相关系数，不能直接与 MTP 的 R² 横比。本页从保存的 full-resolution 预测重新计算同一定义的 R²，并同时保留 pooled、逐 case 平均（macro）和最差 case，避免 pooled 指标掩盖失败样本。

## 复算结果

| 模型与运行 | pooled R²（u/v/a/F） | macro R²(u) | worst-case R²(u) | 训练速度记录 |
|---|---:|---:|---:|---|
| PhyLSTM3 `paper_full` | 0.894854 / 0.998518 / 0.998772 / 0.998364 | 0.850615 | 0.000454 | 保存的 metrics 未包含训练总时间；当前不可核验 |
| CM-PINN `10000+LBFGS500` | 0.773015 / 0.991062 / 0.995075 / 0.994049 | 0.636436 | -0.408546 | 保存的 metrics 未包含训练总时间；当前不可核验 |

## 含义

- 两个基线的速度、加速度和恢复力 pooled R² 很高，但位移尾部明显较弱。
- MTP-bu 的 pooled 位移 0.954046、最差位移 0.801149，优于这两个已复算基线；但 MTP-bu 的加速度与恢复力 pooled R² 低于 PhyLSTM3，因此不能写成“所有通道全面优于 PhyLSTM3”。
- 训练时间缺失就是证据缺口，不能用文件修改时间或日志长度代替。后续所有基线必须输出 wall-clock 总时间、epoch/step、硬件、batch、分辨率和 checkpoint 选择成本。

这次复算只解决“指标定义一致”问题，尚未解决训练预算、标签比例、超参数搜索成本和随机种子是否一致。完整排名应以 [[current-structural-pinn-ranking-2026-08-03]] 为准，并遵守 [[reproduction-failure-prevention-contract-2026-08-03]]。

## Provenance

^[../../../reproductions/phylstm/outputs_paper_full/phylstm3_predictions.mat] ^[../../../reproductions/cm-pinn/outputs_10000_lbfgs500/predictions.npz]
