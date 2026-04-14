# Day 15 学习笔记：变分法 + 庞特里亚金极小值原理

> 日期：2026-04-14 | Week 3 Day 1 | 用时：约30分钟

---

## 1. 变分法核心

**泛函：** J[u] = ∫L(x, u, t)dt — "函数的函数"

**欧拉-拉格朗日方程（必要条件）：**
$$\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{x}}\right) = \frac{\partial L}{\partial x}$$

物理意义：使泛函极小的轨迹必须满足此微分方程。

---

## 2. 庞特里亚金极小值原理（1956）

哈密顿函数：
$$H = L + \lambda^T f(x, u, t)$$

**最优性的必要条件：**

| 方程 | 含义 |
|------|------|
| $\dot{x} = \frac{\partial H}{\partial \lambda}$ | 状态方程 |
| $\dot{\lambda} = -\frac{\partial H}{\partial x}$ | 伴随（costate）方程 |
| $0 = \frac{\partial H}{\partial u}$ | 平稳性条件 |
| $\lambda(t_f) = \frac{\partial \phi}{\partial x(t_f)}$ | 终端边界 |
| $H(x^*, u^*, \lambda^*, t) \leq H(x^*, u, \lambda^*, t)$ | 极小值条件 |

---

## 3. 例子：最短时间问题

**系统：** $\dot{x} = u, \quad |u| \leq 1, \quad x(0)=0, \quad x(t_f)=1$

**目标：** 最小化 $t_f$

**哈密顿：** $H = 1 + \lambda u$（1代表时间代价）

**最优控制：**
$$u^* = \arg\min_{|u|\leq 1} H = \arg\min_{|u|\leq 1} (1 + \lambda u) = -\text{sign}(\lambda)$$

**即 Bang-Bang 控制：|u| 始终等于上限！**

结果：$t_f = 2.0$s，t=1.0s 时刻切换一次（加速→减速）

---

## 4. Bang-Bang vs 光滑控制（LQR）

| | Bang-Bang | 光滑 LQR |
|---|---|---|
| 最优目标 | 最小时间 | 最小 ∫(x'Qx + u'Ru)dt |
| 控制形态 | \|u\| = 1，最大能耗 | 平滑，能耗可控 |
| 切换次数 | 至少一次（线性系统） | 无限次（理论上）|
| 工程应用 | 火箭发动机、机床 | 飞行控制、机器人 |

---

## 5. 与 Week 2 的联系

Week 2 的 LQR 就是庞特里亚金原理在 **二次型代价 + 线性系统** 下的特例：

$$H = x^TQx + u^TRu + \lambda^T(Ax + Bu)$$
$$\frac{\partial H}{\partial u} = 0 \Rightarrow u^* = -\frac{1}{2}R^{-1}B^T\lambda$$

而 **伴随方程** $\dot{\lambda} = -Qx - A^T\lambda$ 的稳态解给出 **时不变的 LQR 反馈**。

---

## 代码文件

- `day15_variational.py` — Bang-Bang vs 光滑LQR仿真
- `day15_variational.png` — 位置/速度/控制对比图
