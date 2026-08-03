---
id: comparison--current-structural-pinn-ranking-2026-08-03
title: 当前结构动力学 PINN 排名与六项目标差距（2026-08-03）
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
- MTP-bu
- TemporalParallel
- PhyLSTM3
- CM-PINN
- OpenSeesPy
- worst-case R2
sources:
- ../../../outputs/remote_temporal_parallel_multiscale_modal1188_broadband2_hfjoint_width100_independentforcehinge40tail20_frombs150_v2_20260731bu/metrics_official90_spectral.json
- ../../../outputs/remote_temporal_parallel_multiscale_modal1188_broadband2_hfjoint_width100_independentforcehinge40tail20_frombs150_v2_20260731bu/training_summary.json
- ../../../outputs/remote_temporal_parallel_dynamicprojection75_selected_full_v2_20260731cm/metrics_official90_spectral.json
- ../../../outputs/remote_v21_m0_fast_20260802/metrics_v2.json
- ../../../reproductions/phylstm/outputs_paper_full/phylstm3_predictions.mat
- ../../../reproductions/cm-pinn/outputs_10000_lbfgs500/predictions.npz
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# 当前结构动力学 PINN 排名与六项目标差距（2026-08-03）

## 结论先行

在当前**学习模型**中，MTP-bu 最接近精度要求：5DOF、90 个测试激励、1501 步上，四个主要响应量的 pooled R² 全部大于 0.9，四个最差样本 R² 也全部大于 0.8。但它还没有满足完整目标：没有 4–5 个公平 PINN 基线的全指标优势，没有 OpenSeesPy 速度证书，高频边力指标不足，也没有完成“换本构后仍同时保持精度与速度”的证明。

V21 physical oracle 的精度最高，但它是顺序物理 oracle，不是训练得到的 PINN，不能作为“本方法已超过其他 PINN”的结论。

## 当前可核验排名

| 候选 | 任务身份 | pooled R²（u/v/a/F） | 最差样本 R²（u/v/a/F） | 90-case 推理 | 训练速度 | 当前判断 |
|---|---|---:|---:|---:|---:|---|
| **MTP-bu** | 5DOF 学习模型 | 0.954046 / 0.967563 / 0.920841 / 0.964075 | 0.801149 / 0.943559 / 0.875757 / 0.926525 | 0.348183 s | 150 epochs，1434.685 s（约 23.9 min，9.56 s/epoch） | 学习模型中最接近要求 |
| **TemporalParallel α=0.75 parent** | 5DOF 学习模型 | 0.919638 / 0.959551 / 0.920780 / 0.964072 | u 最差 0.738534；其余见源文件 | 0.576677 s | 原训练耗时未随选中 checkpoint 保存 | pooled 过线但最差位移未过线 |
| **V21 physical oracle** | 50DOF 顺序物理 oracle | 0.999994 / 0.999948 / 0.999938 / 0.999792 | 未按同一 90-case 口径报告 | warm 0.619668 s；cold 0.645267 s | 无训练 | 精度上界/诊断工具，不是 PINN |

MTP-bu 的独立平衡力和独立加速度相对 RMS 分别为 0.099285 与 0.068314；高模态边力能量分数为 0.764225。后者说明 pooled 精度合格并不代表高频边力已经合格。

## 对六项目标的判定

| 目标 | 当前状态 | 证据边界 |
|---|---|---|
| SDOF–50kDOF 精度达到阈值 | **部分满足** | MTP-bu 在 5DOF 达标；V21 oracle 在 50DOF 达标；SDOF 与 500/5k/50kDOF 尚无同协议、每结构单独训练的完整证明 |
| 优于 4–5 个 PINN 网络 | **未满足** | 已有 PhyLSTM3、CM-PINN 的统一 R²复算，但尚未形成 4–5 个同数据、同预算、同输出量的正式矩阵；且 MTP-bu 并非所有通道都高于 PhyLSTM3 |
| 推理快于 OpenSeesPy | **未满足** | 尚无 OpenSeesPy 正式基准；对优化向量化 Bouc–Wen RK4 的大规模基准反而更慢，见 [[inference-speed-evidence-2026-08-03]] |
| 报告训练速度 | **部分满足** | MTP-bu 已报告；部分历史 checkpoint 和复现基线没有可靠训练总时间，必须标为缺失，不能按文件时间推断 |
| 本构可插拔且性能保持 | **未满足** | 存在本构接口和跨本构试验，但没有“替换后同一套精度 + 推理速度门”联合通过的证据 |
| 低频与项目定义高频均合格 | **未满足** | MTP-bu 高频边力 0.764225 未过 0.8；6 m 素混凝土梁突加竖向荷载工况尚未作为统一正式门执行 |
| 不依赖标签 | **非硬门，当前未满足** | 当前最强学习模型依赖标签；既有 label-free 路线出现 null branch |

## 解释边界

统一基线复算见 [[baseline-unified-r2-reassessment-2026-08-03]]；“一结构一模型”的正式边界见 [[one-structure-one-model-contract-2026-08-03]]。当前可以主张的是“5DOF 上已有一个满足核心 R² 门的候选”，不能主张“SDOF–50kDOF、速度、本构和高低频目标已经全部完成”。

## Provenance

^[../../../outputs/remote_temporal_parallel_multiscale_modal1188_broadband2_hfjoint_width100_independentforcehinge40tail20_frombs150_v2_20260731bu/metrics_official90_spectral.json] ^[../../../outputs/remote_v21_m0_fast_20260802/metrics_v2.json]
