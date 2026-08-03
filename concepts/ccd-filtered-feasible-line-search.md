---
id: concept--ccd-filtered-feasible-line-search
title: "CCD 过滤的可行线搜索 — 让每个 Newton 步保持无碰撞"
type: concept
status: active
project: civil-engineering-llm-wiki
tags:
- domain/computational-mechanics
- evidence/paper
keywords:
- continuous-collision-detection
- feasible-line-search
- newton-method
- contact-robustness
sources:
- sources/papers/li2020-incremental-potential-contact.md
created: '2026-08-03'
updated: '2026-08-03'
confidence: high
---

# CCD 过滤的可行线搜索

## 定义

在非线性接触求解中，先使用连续碰撞检测计算沿搜索方向不发生首次碰撞的最大安全步长，再从该上界执行能量回溯线搜索。这样每次迭代都留在可行域，而不是只在收敛终点检查穿透。^[sources/papers/li2020-incremental-potential-contact.md]

## 为什么需要

即使 [[concepts/local-smooth-contact-barrier]] 在零距离处发散，普通 Newton 步仍可能越过障碍并落到另一侧的低能状态。仅检查离散终点也无法排除路径中间的 tunneling。

## 工作流程

1. 计算 Newton 搜索方向；
2. 对候选接触原语执行 CCD；
3. 得到安全步长上界；
4. 从该步长开始回溯，直至能量下降；
5. 对非反转材料同时施加单元反转步长过滤。

## 加速机制

IPC 使用空间哈希、距离过滤和 CFL 风格的保守相对运动界限，只对可能接近的原语对执行昂贵 CCD。论文报告该过滤平均减少约 50% CCD 成本，并使总时间改善约 10%。

## 边界

- 浮点 CCD 仍受退化和舍入误差影响；
- 精确有理数 CCD 更可靠但代价显著；
- 安全步长可能过于保守，降低 Newton 进展；
- 必须保证初始状态无交叉；
- 无反转还依赖材料能和对应的反转检测。

## 迁移价值

这是一种通用“求解路径可行性”设计，可用于结构碎片接触、壳体自接触、钢筋穿透防止和粒子—网格混合接触，而不局限于 IPC 的具体障碍函数。

## 关联页面

- [[entities/incremental-potential-contact]]
- [[li2020-incremental-potential-contact-method]]
- [[concepts/local-smooth-contact-barrier]]
