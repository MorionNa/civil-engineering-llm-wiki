# Mamba-3 方法：状态空间原理驱动的三项改进

## 1. Exponential-Trapezoidal Discretization

Mamba-3 从连续时变 SSM 出发：

$$\dot h(t)=A(t)h(t)+B(t)x(t)$$

推导输入积分的更高表达力离散方式。相比 Mamba-1/2 使用的 exponential-Euler，Mamba-3 引入数据依赖的梯形积分：

$$h_t=\alpha_t h_{t-1}+\beta_tB_{t-1}x_{t-1}+\gamma_tB_tx_t$$

该形式等价于在 state-input 上施加宽度为 2 的隐式卷积。

## 2. Complex-valued SSM

论文指出，仅使用实值状态转移会限制旋转型隐藏状态表达。Mamba-3 引入复值状态，并证明其可转换为带数据依赖旋转矩阵的实值 SSM。

核心思想：

```text
complex state
      ↓
rotation matrix
      ↓
data-dependent RoPE
      ↓
state tracking
```

## 3. MIMO SSM

Mamba-3 将 SISO 状态更新推广到 MIMO：

- 增加输入输出 rank；
- 将外积计算转换为矩阵乘法；
- 提高 memory-bound decode 阶段 arithmetic intensity。

## 对结构动力学启发

SSM 本质是可学习状态空间动力系统，与结构动力方程存在形式关联：

$$M\ddot{x}+C\dot{x}+Kx=F$$

未来可研究：

```text
MechConv spatial operator
          +
Mamba-style temporal state update
          +
physics residual
          ↓
large-scale structural solver
```
