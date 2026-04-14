# Day 21 学习笔记：Week 3 整合项目 — 无人机高度控制

> 日期：2026-04-14 | Week 3 Day 7 | 用时：约30分钟

---

## 项目：无人机高度控制

**动力学：**
$$m\ddot{z} = T - mg - c\dot{z}$$

**状态空间：**
$$x = \begin{bmatrix} z \\ \dot{z} \end{bmatrix}, \quad A = \begin{bmatrix} 0 & 1 \\ 0 & -c/m \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 1/m \end{bmatrix}$$

**扰动：** 风 gusts（有界，|w| ≤ 1.5 m/s）

---

## 三种控制器对比

| 控制器 | 基础 | 特点 | 适用场景 |
|--------|------|------|---------|
| **LQR** | Week 2 | 二次型最优，均方意义 | 高斯噪声，模型精确 |
| **H∞** | Week 3 | 最坏情况最优 | 有界扰动，模型不确定 |
| **SMC** | Week 3 | 滑模，阶次降低 | 强扰动，参数不确定 |

---

## Week 3 知识总图

```
Week 3 主线：超越线性

线性最优控制 (Week 2)
  └── LQR: J = ∫(x'Qx + u'Ru)dt
       └── Riccati方程

变分法基础
  ├── 泛函 J[u] = ∫L dt
  ├── Euler-Lagrange方程
  └── 庞特里亚金极小值原理

非线性控制
  ├── Lyapunov 直接法
  ├── 描述函数法
  ├── 滑模控制（SMC）
  ├── 反步法（Backstepping）
  └── 反馈线性化

鲁棒最优
  └── H∞: min ||Tzw||∞（最坏情况）
```

---

## Week 1-3 三周完整体系

```
经典控制（Week 1）
  传递函数 → 频率法 → PID
       ↓
  稳定性：Routh / Nyquist / Bode
       ↓
现代控制（Week 2）
  状态空间 → LQR → 卡尔曼滤波
       ↓
  最优估计 + 分离原理
       ↓
非线性+鲁棒（Week 3）
  变分法 → 庞特里亚金
       ↓
  Lyapunov直接法 / 滑模 / 反步
       ↓
  H∞ 鲁棒最优控制
```

---

**三周完成：** 21天 × 2文件 = 42个文件。控制理论完整体系建立 ✅
