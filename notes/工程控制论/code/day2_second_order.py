import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

# ===== Day 2: 二阶系统 + 阻尼比 =====

def second_order_step(K, wn, zeta, t):
    """二阶系统单位阶跃响应
    G(s) = K*wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
    
    zeta < 1: 欠阻尼 → 振荡收敛
    zeta = 1: 临界阻尼
    zeta > 1: 过阻尼
    """
    sys = signal.TransferFunction([K * wn**2], [1, 2*zeta*wn, wn**2])
    t_out, y_out = signal.step(sys, T=t)
    return t_out, y_out

def analytical_underdamped(K, wn, zeta, t):
    """欠阻尼解析解"""
    wd = wn * np.sqrt(1 - zeta**2)  # 阻尼自然频率
    sigma = zeta * wn               # 衰减系数
    y = K * (1 - np.exp(-sigma*t) * np.cos(wd*t) 
             - (zeta/np.sqrt(1-zeta**2)) * np.exp(-sigma*t) * np.sin(wd*t))
    return y

# 参数
K = 1.0
wn = 2.0  # 自然频率
t = np.linspace(0, 6, 1000)

# 欠阻尼不同zeta
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(f'Second-Order System: G(s) = K*wn^2 / (s^2 + 2*zeta*wn*s + wn^2)\n K={K}, wn={wn}', fontsize=13)

zetas = [0.1, 0.3, 0.5, 0.707, 0.9, 1.0, 1.5, 2.0]
colors = plt.cm.RdYlGn(np.linspace(0.1, 0.9, len(zetas)))

for i, zeta in enumerate(zetas):
    t_out, y_out = second_order_step(K, wn, zeta, t)
    
    if zeta < 1:
        label = f'Underdamped zeta={zeta}'
        Mp = np.exp(-np.pi * zeta / np.sqrt(1-zeta**2))
        tp = np.pi / (wn * np.sqrt(1-zeta**2))
        # 找到峰值
        peak_idx = np.argmax(y_out)
        y_peak = y_out[peak_idx]
        t_peak = t_out[peak_idx]
        overshoot = (y_peak - K) / K * 100
        axes[0,0].axhline(y=K*(1+Mp), color='gray', linestyle=':', alpha=0.3)
        axes[0,0].plot(t_out, y_out, color=colors[i], linewidth=2, label=label)
        if zeta == 0.3:
            axes[0,0].axvline(x=tp, color='orange', linestyle='--', alpha=0.7, label=f'tp={tp:.2f}s')
            axes[0,0].scatter([tp], [y_peak], color='red', zorder=5)
    elif zeta == 1:
        label = f'Critical zeta={zeta}'
        axes[0,0].plot(t_out, y_out, color=colors[i], linewidth=2.5, label=label)
    else:
        label = f'Overdamped zeta={zeta}'
        axes[0,0].plot(t_out, y_out, color=colors[i], linewidth=1.5, label=label)

axes[0,0].axhline(y=K, color='black', linestyle='-', alpha=0.3)
axes[0,0].set_title('Step Response - All Damping Ratios')
axes[0,0].set_xlabel('t (s)')
axes[0,0].set_ylabel('y(t)')
axes[0,0].legend(fontsize=7, loc='lower right')
axes[0,0].grid(True, alpha=0.3)
axes[0,0].set_ylim(0, 2.5)

# ===== Peak Time, Overshoot vs zeta =====
zetas_fine = np.linspace(0.01, 0.99, 100)
Mp_vals = [np.exp(-np.pi * z / np.sqrt(1-z**2)) * 100 for z in zetas_fine]
tp_vals = [np.pi / (wn * np.sqrt(1-z**2)) for z in zetas_fine]

axes[0,1].plot(zetas_fine, Mp_vals, 'b-', linewidth=2)
axes[0,1].set_title('Overshoot Mp vs Damping Ratio zeta')
axes[0,1].set_xlabel('zeta')
axes[0,1].set_ylabel('Mp (%)')
axes[0,1].grid(True, alpha=0.3)
axes[0,1].axvline(x=0.707, color='red', linestyle='--', alpha=0.7, label='zeta=0.707 (Butterworth)')
axes[0,1].legend()

axes[1,0].plot(zetas_fine, tp_vals, 'g-', linewidth=2)
axes[1,0].set_title('Peak Time tp vs Damping Ratio zeta')
axes[1,0].set_xlabel('zeta')
axes[1,0].set_ylabel('tp (s)')
axes[1,0].grid(True, alpha=0.3)

# ===== Settling time (2% criterion) =====
zetas_ts = np.linspace(0.01, 2.0, 200)
ts_2pct = [4 / (z * wn) for z in zetas_ts]  # 2% criterion: ts ≈ 4/(zeta*wn)

axes[1,1].plot(zetas_ts, ts_2pct, 'r-', linewidth=2)
axes[1,1].set_title('Settling Time ts (2%) vs Damping Ratio')
axes[1,1].set_xlabel('zeta')
axes[1,1].set_ylabel('ts (s)')
axes[1,1].grid(True, alpha=0.3)
axes[1,1].axvline(x=1.0, color='green', linestyle='--', alpha=0.7, label='Critical damping')
axes[1,1].legend()

plt.tight_layout()
output_path = 'C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day2_second_order.png'
plt.savefig(output_path, dpi=150)
print(f"Figure saved: {output_path}")

# ===== Key formulas =====
print("\n===== Key Formulas =====")
print(f"Natural frequency wn = {wn} rad/s")
print(f"Damping ratio zeta varies from 0.1 to 2.0")

for zeta in [0.1, 0.3, 0.5, 0.707, 1.0]:
    if zeta < 1:
        wd = wn * np.sqrt(1 - zeta**2)
        Mp = np.exp(-np.pi * zeta / np.sqrt(1-zeta**2)) * 100
        tp = np.pi / wd
        ts = 4 / (zeta * wn)
        print(f"\nzeta={zeta} (Underdamped):")
        print(f"  Mp  = {Mp:.2f}% (overshoot)")
        print(f"  tp  = {tp:.3f}s (peak time)")
        print(f"  ts  = {ts:.3f}s (settling time, 2%)")
        print(f"  wd  = {wd:.3f} rad/s (damped frequency)")
    elif zeta == 1:
        print(f"\nzeta={zeta} (Critical):")
        print(f"  ts  = {4/(zeta*wn):.3f}s (settling time, 2%)")
    else:
        print(f"\nzeta={zeta} (Overdamped)")
