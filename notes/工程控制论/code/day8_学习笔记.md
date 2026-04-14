# Day 8 学习笔记：状态空间 + 状态反馈

> 日期：2026-04-14 | 用时：约30分钟

---

## 1. 状态空间标准形式

$$\dot{x} = Ax + Bu, \quad y = Cx + Du$$

| 矩阵 | 维度 | 含义 |
|------|------|------|
| A | n×n | 状态矩阵（决定系统固有特性）|
| B | n×m | 输入矩阵 |
| C | p×n | 输出矩阵 |
| D | p×m | 前馈矩阵 |

---

## 2. 本例：G(s) = 2/(s²+3s+2)

$$A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 2 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 \end{bmatrix}$$

**开环极点：λ₁=-1, λ₂=-2**（稳定）

---

## 3. 可控性 + 可观性

**可控性判据：**
$$C_c = [B, AB, A^2B, ..., A^{n-1}B], \quad \text{rank}(C_c) = n$$

$$\text{rank}(C_c) = 2 \rightarrow \text{完全可控 ✅}$$

**可观性判据：**
$$O = \begin{bmatrix} C \\ CA \\ CA^2 \\ ... \end{bmatrix}, \quad \text{rank}(O) = n$$

$$\text{rank}(O) = 2 \rightarrow \text{完全可观测 ✅}$$

---

## 4. 状态反馈：u = -Kx + r

**闭环系统：**
$$\dot{x} = (A - BK)x + Br$$

**极点配置：** 选择 K 使 (A-BK) 的特征值等于期望极点。

**期望极点：λd = [-3, -5]（比原来 -1,-2 更快）**

**结果：**
$$K = [6.5, 2.5]$$
$$\text{闭环极点：} \lambda_1 = -3, \quad \lambda_2 = -5 \checkmark$$

---

## 5. Ackermann 公式（单输入）

$$K = \begin{bmatrix} 0 & \cdots & 1 \end{bmatrix} C_c^{-1} p(A)$$

其中 p(A) 是以期望特征值为根的特征多项式在 A 处的值。

Python 实现：`scipy.signal.place_poles(A, B, desired_poles)`

---

## 6. 与开环对比

| | 开环 | 闭环（反馈）|
|---|---|---|
| 极点 | -1, -2 | **-3, -5** |
| 调节时间 | ~4s | ~1.5s |
| 响应速度 | 慢 | 快 |
| 类型 | 欠阻尼 | 欠阻尼（更快）|

---

## 代码文件

- `day8_state_space.py` — 状态空间 + 极点配置仿真
- `day8_state_feedback.png` — 4图对比（阶跃响应、极点图、状态轨迹、总结）
