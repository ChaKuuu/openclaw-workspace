# Day 18 学习笔记：描述函数法 + 滑模控制

> 日期：2026-04-14 | Week 3 Day 4 | 用时：约30分钟

---

## 1. 描述函数法（近似分析）

**核心思想：** 将非线性环节近似为线性增益（针对基波分量）

$$N(A) = \frac{\text{输出基波幅值}}{\text{输入幅值}}$$

**继电特性：**
$$N(A) = \frac{4d}{\pi A}$$

**应用：** 预测非线性系统中的极限环
- 如果 Nyquist 曲线与 $-1/N(A)$ 有交点 → 可能存在极限环

---

## 2. 滑模控制（SMC）

**两阶段：**
1. **趋近阶段**：u 将状态推向滑模面 s=0
2. **滑动阶段**：系统在 s=0 上滑向原点（对扰动不敏感）

**滑模面：**
$$s = \left(\frac{d}{dt} + \lambda\right)^{n-1} e$$

**控制律：**
$$u = -K \cdot \text{sign}(s) \quad \text{（理想）}$$
$$u = -K \cdot \text{sat}\left(\frac{s}{\delta}\right) \quad \text{（边界层，实际）}$$

---

## 3. 抖振（Chattering）

**原因：** 有限切换频率导致高频振荡

**解决方案：**
- 边界层：sign → sat
- 二阶滑模（SOSMC）
- 观测器补偿

---

## 代码文件

- `day18_nonlinearmac.py` — 描述函数 + SMC仿真
- `day18_nonlinearmac.png` — 滑模跟踪/抖振/描述函数图
