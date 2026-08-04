---
type: paper-analysis
title: Beam elements with frictional contact in the material point method
authors:
- Jingu Kang
- Michael A. Homel
- Eric B. Herbold
year: 2022
venue: International Journal for Numerical Methods in Engineering
doi: 10.1002/nme.6886
tags:
- domain/computational-mechanics
- evidence/paper
methods:
- CPDI2
- beam-particle
- multi-velocity-field-contact
- Coulomb-friction
- Euler-Bernoulli
- Timoshenko
- explicit-time-integration
results:
- analytical-validation
- finite-element-comparison
- dynamic-contact
- fiber-mixing
failure_modes:
- contact-gap
- grid-resolution-dependence
- no-angular-momentum-contact
- small-strain-beam-constitutive-assumption
datasets:
- paper-defined-numerical-benchmarks
reproducibility: medium
code_url: []
dataset_url: []
id: paper--kang2022-beam-contact-mpm-results
status: active
project: civil-engineering-llm-wiki
keywords:
- computational-mechanics
- material-point-method
- contact-mechanics
- friction
- beam-elements
- large-deformation
- numerical-methods
- coupled-methods
- reproducibility
- CPDI2
- beam-particle
- multi-velocity-field-contact
- Coulomb-friction
- Euler-Bernoulli
- Timoshenko
- explicit-time-integration
- analytical-validation
- finite-element-comparison
- dynamic-contact
- fiber-mixing
- contact-gap
- grid-resolution-dependence
- no-angular-momentum-contact
- small-strain-beam-constitutive-assumption
- paper-defined-numerical-benchmarks
- International Journal for Numerical Methods in Engineering
sources:
- sources/papers/kang2022-beam-contact-mpm.md
created: '2026-08-04'
updated: '2026-08-04'
confidence: high
evidence_scope: full-text
---
# Results：beam particle 的验证与接触算例

^[sources/papers/kang2022-beam-contact-mpm.md]

> 本页只整理论文第 4 节及图 4–15 中有文本证据的数值/实验对照结果。方法定义见 [[kang2022-beam-contact-mpm-method]]，总览见 [[kang2022-beam-contact-mpm-analysis]]。

## 1. 统一设置

论文第 4 节说明：除第 4.5 节厚梁外，弯曲行为采用 Euler–Bernoulli 梁理论；所有 beam-particle 与 CPDI2 solid-particle 结果采用显式时间积分。时间步约为 `Δt = 0.4 l_g sqrt(ρ_0/E)`。以下数值均来自论文设定或图注，不对图线做额外数字化。

## 2. 纯弯曲悬臂梁：Fig. 4

### 设定

- 直悬臂梁，矩形截面；`L = 10`，`b = 1`，`h = 0.1`。
- 弯曲刚度为 `EI_z = L`；端部施加逐步增加的集中弯矩。
- 采用 25 个 beam particles，背景网格尺寸为梁粒子长度的一半，即 `l_g = 0.5 l_b`。
- 文中给出 `M = 0.5π、π、1.5π、2π` 时分别形成四分之一圆、半圆、四分之三圆和闭合圆形状。

### 结果

Fig. 4A 显示初始形状和随弯矩增加的连续大转动形状，梁粒子上的弯矩沿长度均匀分布，与端部施加弯矩一致。Fig. 4B 中，`x` 和 `y` 方向的端部位移—弯矩关系与精确解析解比较，论文报告二者“very good agreement”。

论文还报告，同一悬臂梁用 5 个 beam particles 可得到 practically identical result，但这一结果未在图中展示。

## 3. 空间六边形框架屈曲：Fig. 5

### 设定

- 框架包含 12 个梁构件；每个 24 in 长的构件用 6 个 beam particles 离散。
- 框架高度 `H = 1.75 in`。
- `E = 439,800 lb/in²`，`G = 159,000 lb/in²`，截面面积 `A = 0.494 in²`。
- 截面二次矩 `I_y = I_z = 0.02 in⁴`，极惯性矩 `I_x = 0.0331 in⁴`。
- 顶点施加竖直方向恒速位移，速度为 `0.05 in/s`；六个顶点采用 roller boundary conditions。

### 结果

Fig. 5A 给出初始和分析结束时的框架形状。Fig. 5B 的 force–displacement 响应与 Griggs 的实验研究结果以及既有数值分析结果比较良好。论文将该对照描述为覆盖实验研究的屈曲前范围和既有 beam-column 数值分析的屈曲后范围。

## 4. 悬臂梁动力响应：Fig. 6

### 设定

- 矩形截面面积 `A = 1 m²`，梁长 `L = 100 m`。
- `ρ = 1.0 kg/m³`，`E = 1.0 × 10⁸ Pa`，`ν = 0`。
- 梁初始静止，施加集中端部力 `P = 10.0 N`。
- 采用 5、20、50 个 MPM beam particles，并与 50 个 FEM beam elements 对照。

### 结果

端部位移按静态挠度 `δ_stat = PL³/(3EI)` 归一化。响应围绕静态挠度振荡，最大端部挠度为静态挠度的两倍，论文将其作为动态放大现象。

按 Euler–Bernoulli 理论，最低自然频率为 `f_theory = 0.16152 Hz`，相应周期 `T = 6.191 s`。论文报告：超过 20 个 beam particles 时，振荡周期与理论值吻合良好；50 个 MPM beam particles 与 50 个 FEM beam elements 的动态响应吻合良好（Fig. 6）。

## 5. 45° 曲悬臂梁：Fig. 7

### 设定

- 曲梁位于 `X–Y` 平面，平均半径 100 in，矩形截面面积 `1 in²`。
- 用 10 个直 beam particles 近似，背景网格单元尺寸为 10 in。
- 左端固定，自由端施加 `z` 方向阶跃荷载；最终荷载为 `P = 600 lb`，中间图示荷载为 `P = 300 lb`。
- `E = 10⁷ psi`，`ν = 0`。

### 结果

该算例同时包含多轴挠曲、剪切、伸长和扭转。Fig. 7A 展示 `P = 300 lb` 和 `P = 600 lb` 的形状；Fig. 7B 中 beam-particle 的 `x`、`y`、`z` 方向端部位移与 FEM 分析结果相同。论文还报告，使用 5 个 beam particles 也取得相同精度。

## 6. 自重下大变形振动：Figs. 8–10

### 设定

- 悬臂梁初始水平，受重力体力；`L = 4 m`，`b = 1 m`，`h = 1 m`。
- `ρ_0 = 1050 kg/m³`，`E = 1 × 10⁶ Pa`，`ν = 0.3`，`g = 10 m/s²`。
- 这是厚梁算例，beam particle formulation 使用 Timoshenko 梁理论，并计入剪切刚度。

### 结果

Fig. 8 给出 `t = 0.0`、`1.2 s` 和 `2.7 s` 的大变形振动构形。Fig. 9 比较 CPDI2 与不同梁理论下 beam particles 的端部竖向位移时间历程：计入剪切变形的 beam-particle 响应接近 CPDI2；不计入剪切的 Euler–Bernoulli 结果端部位移较小。

Fig. 10 的 `t = 0.5 s` 最大主应力对照显示：CPDI2 粒子在固定端附近上下表面出现最大应力，分布没有明显的 spurious/highly oscillatory values；beam-particle 应力沿厚度线性插值得到的轮廓与 CPDI2 结果相近。

## 7. 纤维在斜板/水平板上的摩擦堆积：Fig. 11

### 设定

- 一束纤维落到倾斜板并滑向水平板；板由 CPDI2 solid particles 表示并视为刚体。
- 每根纤维用 30 个 beam particles 表示，截面为圆形，长径比 `l_f/d_f = 30`。
- 纤维和 CPDI2 粒子使用相同的 Coulomb 摩擦系数，分别测试 `μ = 0、0.3、0.6`。
- 图示为真实时间 `t = 1.5 s` 的构形。

### 结果

Fig. 11 展示了不同摩擦系数下纤维滑移和堆积。论文报告，借助粒子域跟踪，即使纤维发生大转动，也能够表示滑动摩擦；纤维运动随摩擦接触条件变化。该算例还被用来说明普通 MPM 的 extension instability 会产生数值断裂，从而难以得到合理的纤维堆积响应。

## 8. 六边形框架落到刚性球：Fig. 12–13

### 设定

- 重复六边形框架落到刚性球上；球和地板由 CPDI2 solid particles 表示。
- 每个边长 `l_s = 0.5 m` 的六边形边用 4 个 beam particles 离散；刚性球半径 `r_s = 3l_s`。
- 使用与前一算例相同的橡胶材料设定；摩擦系数 `μ = 0.3`。
- Fig. 12 给出 `t = 0.3 s、0.6 s、0.9 s` 的下落/碰撞构形。

### 结果

框架先撞击球面，随后沿球面和地板变形并滑动。Fig. 13 在 `t = 1.2 s` 比较弯曲刚度 `k_f = EI` 与 `k_f = 500EI`：

| 弯曲刚度 | 论文图示/文字报告的构形结果 |
|---|---|
| `k_f = EI` | 与球和地板形成较多接触点；部分六边形单元高度畸变，并在球底部附近向自身折叠。 |
| `k_f = 500EI` | 接触点较少，六边形图案的畸变较小。 |

## 9. 混合两类柔性纤维：Figs. 14–15

### 设定

- 1000 根纤维，共 50,000 个 beam particles；背景网格为 `100 × 100 × 50`。
- 搅拌杆绕盒子中心转动，角速度为 `5.0 s⁻¹`；搅拌杆和盒子由高刚度 CPDI2 particles 表示。
- 软纤维：`E = 1.0 MPa`，`ν = 0.3`，`ρ = 1000 kg/m³`，长度 10 mm，圆形直径 0.5 mm。
- 硬纤维：`E = 100.0 MPa`，`ν = 0.3`，`ρ = 10,000 kg/m³`，长度 10 mm，矩形截面面积 `0.52 mm²`。
- 重力 `g = 10 m/s²`；比较纤维间 `μ = 0` 和 `μ = 0.3`。

### 结果

Fig. 14 展示了无摩擦和有摩擦时两类纤维的动态接触混合构形。软纤维因为挠曲和转动更大而倾向于团聚；论文观察到 clumping-like 和 segregation 现象。

当 `μ = 0` 时，两类纤维不发生混合，而是分别成组运动。Fig. 15 的 `t = 1.0 s` 速度分布显示，`μ = 0.3` 时纤维比零摩擦情况更团聚；零摩擦时速度分布呈由搅拌杆和纤维运动形成的圆形图案。

论文据此说明，显式表示单根纤维可以捕获纤维数量和取向对混合/放置过程的影响；这些结果是定性过程示范，没有报告独立的混合指数或误差条带。

## 10. 结果证据边界

- 解析解对照、FEM 对照和 Griggs 实验曲线均以图形或文字比较呈现；提供文本没有可下载的原始数值表。
- 接触算例主要报告构形、滑移、堆积、团聚和速度分布等图示/定性结果，未报告统一的接触误差指标。
- 论文的数据声明称大部分支撑数据已呈现在文章中，其他数据可向通讯作者合理请求；提供文本未给出代码或数据仓库 URL。

## 11. 可复现性

结果复现所需的核心参数、粒子数、网格尺寸和图示时间点在文中多处给出，但公开代码和数据包未披露。因此本页继承 `reproducibility: medium`，`code_url: []`，`dataset_url: []`。方法重建请见 [[kang2022-beam-contact-mpm-method]]，失败边界请见 [[kang2022-beam-contact-mpm-critical]]。

## 12. 可复现性（Reproducibility）

**🟡 中复现性** — 本页沿用该论文总览的复现等级；详细复现要点请参阅 [[kang2022-beam-contact-mpm-analysis]]。

| 项目 | 说明 |
|---|---|
| **等级** | 🟡 中复现性 |
| **官方代码** | 无公开代码 |
| **数据集** | 无外部数据集 URL（或使用论文内/合成数据） |
| **复现要点** | 需要固定论文所述版本、参数、数据处理和评估协议；未披露的关键细节不能由本页推断。 |
