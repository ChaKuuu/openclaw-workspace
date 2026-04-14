# Day 16 学习笔记：随机过程 + 随机控制

> 日期：2026-04-14 | Week 3 Day 2 | 用时：约30分钟

---

## 1. 随机过程基础

**白噪声（White Noise）：**
- 功率谱密度恒定（所有频率等能量）
- 相关时间 = 0（$\delta$ 函数相关）
- 数学上不可微，积分有意义

**布朗运动 / Wiener 过程 W(t)：**
$$W(0) = 0, \quad W(t) - W(s) \sim N(0, t-s)$$
- 连续但处处不可导
- $dW \sim N(0, dt)$

---

## 2. Itô 微积分规则

| 规则 | 含义 |
|------|------|
| $dW^2 = dt$ | 二次变差 |
| $dW \cdot dt = 0$ | 混合项消失 |
| $(dW)^n = 0$ (n≥3) | 高阶项为零 |

---

## 3. 线性随机微分方程

$$dx = a \cdot x \, dt + b \, dW$$

**解析解：**
$$x(t) = x(0) e^{at} + b \int_0^t e^{a(t-s)} dW(s)$$

**统计特性：**
$$E[x(t)] = x(0) e^{at}$$
$$\text{Var}[x(t)] = \frac{b^2}{2a}(e^{2at} - 1)$$

---

## 4. Ornstein-Uhlenbeck 过程

$$dX = -\theta X \, dt + \sigma \, dW$$

- $\theta > 0$：均值回复力（回归到0）
- 物理含义： Langevin 方程（摩擦 + 随机力）
- 稳态分布：$X \sim N(0, \frac{\sigma^2}{2\theta})$

---

## 5. 卡尔曼滤波的随机解释

$$Q \text{ 大} \Rightarrow K \text{ 大} \Rightarrow \text{更信任测量}$$
$$R \text{ 大} \Rightarrow K \text{ 小} \Rightarrow \text{更信任模型预测}$$

**"最优" = 在模型不确定性和测量不确定性之间最优分配信任**

---

## 代码文件

- `day16_stochastic.py` — 白噪声/布朗运动/OU过程仿真
- `day16_stochastic.png` — 6图：各种随机过程
