import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

# ===== Day 3: Routh-Hurwitz Stability Criterion (CORRECT) =====

def routh_array(coeffs):
    """正确构建 Routh 数组"""
    n = len(coeffs) - 1  # 多项式阶数
    
    # row1: a_n, a_{n-2}, a_{n-4}, ... (偶次幂系数)
    # row2: a_{n-1}, a_{n-3}, a_{n-5}, ... (奇次幂系数)
    row1 = coeffs[0::2][::-1]   # [a_n, a_{n-2}, ...]
    row2 = coeffs[1::2][::-1] if len(coeffs) > 1 else []  # [a_{n-1}, a_{n-3}, ...]
    
    # 补齐使两行长度一致
    max_len = max(len(row1), len(row2))
    while len(row1) < max_len: row1.append(0)
    while len(row2) < max_len: row2.append(0)
    
    rows = [row1, row2]
    powers = [n, n-1]  # 对应每行的阶次
    
    while len(rows[-1]) > 1 and len(powers) <= n:
        prev = rows[-2]
        curr = rows[-1]
        next_row = []
        
        for i in range(len(curr) - 1):
            a = curr[0]
            if abs(a) < 1e-12:
                val = 0
            else:
                b = prev[i+1] if i+1 < len(prev) else 0
                val = (curr[i+1] * prev[0] - curr[0] * b) / a
            next_row.append(round(val, 6))
        
        rows.append(next_row)
        powers.append(powers[-1] - 2)
    
    return rows, powers[:len(rows)]

def is_stable(coeffs):
    rows, powers = routh_array(coeffs)
    first_col = [row[0] for row in rows]
    stable = all(v > 0 for v in first_col)
    return stable, rows, powers, first_col

def print_routh(coeffs):
    n = len(coeffs) - 1
    print(f"\n特征方程: ", end="")
    terms = []
    for i, c in enumerate(coeffs):
        power = n - i
        if abs(c) > 0:
            if power == 0: terms.append(f"{c}")
            elif power == 1: terms.append(f"{c}s")
            else: terms.append(f"{c}s^{power}")
    print(" + ".join(terms).replace("+ -", "- "))
    
    rows, powers = routh_array(coeffs)
    print("Routh Array:")
    for row, pwr in zip(rows, powers):
        print(f"  s^{pwr:2d}:  {'  '.join(f'{v:10.4f}' for v in row)}")
    
    fc = [row[0] for row in rows]
    stable = all(v > 0 for v in fc)
    print(f"第一列: {[round(v,4) for v in fc]}")
    print(f"稳定: {stable}")
    return stable

# ===== Tests =====
tests = [
    ([1, 2, 3, 4], "3阶稳定系统"),
    ([1, 2, 3, -4], "3阶不稳定系统"),
    ([1, 2, 3, 4, 5], "4阶系统"),
    ([1, 2, 3, -4, 5], "4阶不稳定"),
]

for coeffs, name in tests:
    print("=" * 55)
    stable = print_routh(coeffs)
    poles = np.roots(coeffs)
    print(f"极点: {[f'{p:.3f}' for p in poles]}")
    print(f"scipy判定: {'STABLE' if all(p.real < 0 for p in poles) else 'UNSTABLE'}")

# ===== 可视化 =====
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Routh Stability Criterion - Pole Maps', fontsize=14)

systems = [
    ([1, 2, 3, 4], 'Stable: s^3+2s^2+3s+4'),
    ([1, 2, 3, -4], 'Unstable: s^3+2s^2+3s-4'),
    ([1, 2, 3, 4, 5], 'Stable: s^4+2s^3+3s^2+4s+5'),
    ([1, 2, 3, -4, 5], 'Unstable: s^4+2s^3+3s^2-4s+5'),
]

for idx, (coeffs, name) in enumerate(systems):
    ax = axes[idx//2, idx%2]
    poles = np.roots(coeffs)
    ax.scatter(poles.real, poles.imag, marker='x', s=150, linewidths=3, color='red', zorder=5)
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'b--', alpha=0.3, label='Unit circle')
    ax.axvline(x=0, color='gray', ls='--', alpha=0.4)
    ax.axhline(y=0, color='gray', ls='--', alpha=0.4)
    ax.set_xlim(-5, 1.5)
    ax.set_ylim(-4, 4)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    stable = all(p.real < 0 for p in poles)
    status = 'STABLE' if stable else 'UNSTABLE'
    ax.set_title(name)
    ax.text(0.02, 0.98, status, transform=ax.transAxes,
           color='green' if stable else 'red', fontsize=15, fontweight='bold', va='top')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day3_routh.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")

# ===== K临界稳定 =====
print("\n" + "=" * 55)
print("K临界稳定: G(s)=K / (s^3 + 2s^2 + 3s + K)")
K_range = np.linspace(0.1, 20, 300)
stable_arr = [1 if all(np.roots([1,2,3,K]).real < 0) else 0 for K in K_range]

critical_K = None
for i in range(1, len(K_range)):
    if stable_arr[i-1] == 1 and stable_arr[i] == 0:
        critical_K = K_range[i]
        break

plt.figure(figsize=(10, 4))
plt.fill_between(K_range, stable_arr, alpha=0.3, color='green')
plt.plot(K_range, stable_arr, 'b-', lw=2)
if critical_K:
    plt.axvline(x=critical_K, color='red', ls='--', lw=2, label=f'K_cr = {critical_K:.3f}')
plt.xlabel('Gain K')
plt.ylabel('Stable (1) / Unstable (0)')
plt.title('Stability vs K: s^3 + 2s^2 + 3s + K')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day3_K_stability.png', dpi=150, bbox_inches='tight')
print(f"Figure 2 saved! K_cr = {critical_K:.3f}" if critical_K else "Not found")
