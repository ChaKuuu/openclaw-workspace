import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

# ===== Day 5: Nyquist Stability Criterion =====

def nyquist_curve(sys, omega_range=(-4, 2), num_points=1000):
    """计算 Nyquist 曲线"""
    omega = np.logspace(omega_range[0], omega_range[1], num_points)
    w, H = signal.freqresp(sys, omega)
    return w, H

# ===== 系统 1: G(s) = 1/(s+1) = Stable =====
print("=" * 55)
print("Nyquist Criterion Examples")
print("=" * 55)

sys_stable = signal.TransferFunction([1], [1, 1])
w1, H1 = nyquist_curve(sys_stable)

print("\nSystem 1: G(s) = 1/(s+1)  [Stable]")
print("Nyquist contour: starts at G(j0)=1, ends at origin (clockwise)")
print("Encloses -1 point? NO")
print("P=0, Z=N=0, stable")

# ===== 系统 2: G(s) = 1/(s-1) = Unstable (pole at +1) =====
sys_unstable = signal.TransferFunction([1], [-1, 1])  # s-1 = -(1-s)
print("\nSystem 2: G(s) = 1/(s-1)  [Unstable]")
print("Nyquist contour: starts at G(j0)=-1, ends at origin")
print("Encloses -1? YES (once counterclockwise)")
print("P=1 (one RHP pole), encirclements N=-1")
print("Z = N + P = -1 + 1 = 0, but -1 is ON the curve!")
print("Marginally stable or unstable...")

# ===== 系统 3: G(s) = K/(s-1), K=2 =====
sys_K2 = signal.TransferFunction([2], [-1, 1])
w3, H3 = nyquist_curve(sys_K2)
print("\nSystem 3: G(s) = 2/(s-1), K=2  [Unstable]")
print("Encloses -1? YES")
print("Z = N + P != 0, unstable")

# ===== 可视化 =====
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Nyquist Diagrams', fontsize=14)

# System 1: stable
ax = axes[0]
ax.plot(H1.real, H1.imag, 'b-', lw=2)
ax.scatter([-1], [0], marker='x', s=200, linewidths=3, color='red', label='-1 point')
ax.scatter([0], [0], marker='o', s=50, color='gray', label='Origin')
ax.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax.axvline(x=0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_title('G(s)=1/(s+1)\nStable (does not encircle -1)')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()

# System 2: unstable
w2, H2 = nyquist_curve(signal.TransferFunction([1], [-1, 1]))
ax = axes[1]
ax.plot(H2.real, H2.imag, 'r-', lw=2)
ax.scatter([-1], [0], marker='x', s=200, linewidths=3, color='red', label='-1 point')
ax.scatter([0], [0], marker='o', s=50, color='gray', label='Origin')
ax.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax.axvline(x=0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_title('G(s)=1/(s-1)\nUnstable (encircles -1)')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()

# System 3: K*unstable
ax = axes[2]
ax.plot(H3.real, H3.imag, 'orange', lw=2)
ax.scatter([-1], [0], marker='x', s=200, linewidths=3, color='red', label='-1 point')
ax.scatter([0], [0], marker='o', s=50, color='gray', label='Origin')
ax.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax.axvline(x=0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_title('G(s)=2/(s-1), K=2\nUnstable (more gain)')
ax.set_xlim(-3, 2)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day5_nyquist_basic.png', dpi=150, bbox_inches='tight')
print("\nFigure 1 saved: day5_nyquist_basic.png")

# ===== Nyquist with multiple poles =====
print("\n" + "=" * 55)
print("G(s) = 1 / ((s+1)(s+2)(s-0.5))")
sys_mixed = signal.TransferFunction([1], np.poly([-1, -2, 0.5]))
w_m, H_m = nyquist_curve(sys_mixed, omega_range=(-2, 3))
poles = sys_mixed.poles
print(f"Poles: {poles}")
print(f"RHP poles P = {sum(1 for p in poles if p.real > 0)}")

# Count encirclements of -1
def count_encirclements(H, target=-1):
    """数 -1 被包围次数（简易法：射线交点计数）"""
    x, y = H.real, H.imag
    # 射线从 target 向右延伸
    tx = target
    crossings = 0
    for i in range(len(x)-1):
        # 检查线段是否与 x=tx 的射线相交
        y1, y2 = y[i] - 0, y[i+1] - 0
        x1, x2 = x[i] - tx, x[i+1] - tx
        if (y1 > 0) != (y2 > 0):  # 穿过x轴
            # 计算交点 x 坐标
            if x1 != x2:
                ix = x1 + (x2-x1) * (-y1) / (y2-y1)
                if ix > 0:
                    crossings += 1
    return crossings

N_approx = count_encirclements(H_m, -1)
Z = N_approx + int(sum(1 for p in poles if p.real > 0))
stable = Z == 0

print(f"Nyquist encirclements N ~ {N_approx}")
print(f"Z = N + P = {N_approx} + {sum(1 for p in poles if p.real > 0)} = {Z}")
print(f"System: {'STABLE' if stable else 'UNSTABLE'}")

plt.figure(figsize=(8, 8))
plt.plot(H_m.real, H_m.imag, 'b-', lw=2)
plt.scatter([-1], [0], marker='x', s=200, linewidths=3, color='red', label='-1 point')
for p in poles:
    marker = 'x' if p.real > 0 else 'o'
    color = 'red' if p.real > 0 else 'green'
    plt.scatter([p.real], [p.imag], marker=marker, s=150, color=color, zorder=5)
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title(f'G(s) = 1/((s+1)(s+2)(s-0.5))\nP={sum(1 for p in poles if p.real > 0)} RHP poles, Z={Z}')
plt.axhline(y=0, color='gray', ls='--', alpha=0.5)
plt.axvline(x=0, color='gray', ls='--', alpha=0.5)
plt.xlim(-2, 1)
plt.ylim(-2, 2)
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day5_nyquist_mixed.png', dpi=150, bbox_inches='tight')
print("Figure 2 saved: day5_nyquist_mixed.png")

# ===== Key insight =====
print("\n" + "=" * 55)
print("Nyquist Stability Criterion (Recap)")
print("=" * 55)
print("""
Nyquist: Z = N + P
  Z = 闭环右半平面极点数（Z=0 则稳定）
  N = Nyquist曲线绕-1点的逆时针圈数
  P = 开环右半平面极点数

判断:
  P=0 (开环稳定) → N=0 则闭环稳定（不包围-1）
  P>0 → 需要额外的顺时针包围来抵消
""")
