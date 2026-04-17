"""
Day 36 - Pontryagin Maximum Principle (PMP)
工程控制论 Phase 2 Week 5 Day 1

核心：三件套
1. H = L + λᵀf          # 哈密顿函数
2. λ̇ = -∂H/∂x          # 协态方程
3. ∂H/∂u = 0            # 控制方程

与 LQR 对比：
- LQR: 线性系统 + 二次型代价 → Riccati 方程（解析解）
- PMP: 任意系统 + 任意代价 → 边值问题（通常需数值解）

例：最速降线问题
H = 1 + λ₁v + λ₂y
λ̇₁ = 0 → λ₁ = const
∂H/∂θ = λ₁cosθ = 0 → θ = π/2
答案：摆线

倒立摆仿真：
- PD控制（简化PMP）：末端角度发散
- BVP求解：奇异雅可比（需更好的初始猜测）

结论：对于非线性系统，PMP的实际应用需要：
1. 梯度下降法
2. Shooting method
3. 或直接用 LQR 的线性化近似
"""
