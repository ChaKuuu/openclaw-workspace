import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

# ===== Day 6: PID Control + Ziegler-Nichols =====

def closed_loop_pid(Kp, Ki, Kd, G_num, G_den):
    """计算PID闭环传递函数
    C(s) = (Kd*s^2 + Kp*s + Ki) / s
    T(s) = C*G / (1 + C*G)
    
    特征方程: s(s^2 + 3s + 2) + 2(Kd*s^2 + Kp*s + Ki) = 0
    即: s^3 + (3+2Kd)s^2 + (2+2Kp)s + 2Ki = 0
    """
    # 特征多项式系数
    cl_char = [1, 3 + 2*Kd, 2 + 2*Kp, 2*Ki]
    
    # 检查稳定性
    poles = np.roots(cl_char)
    stable = all(p.real < 0 for p in poles)
    
    # 闭环传递函数
    # T(s) = 2*(Kd*s^2 + Kp*s + Ki) / [s^3 + (3+2Kd)s^2 + (2+2Kp)s + 2Ki]
    # 分子: 2*Kd*s^2 + 2*Kp*s + 2*Ki
    num = [2*Kd, 2*Kp, 2*Ki, 0]  # 补0因为分子是2次，分母是3次
    den = cl_char
    # 实际上需要约分...用signal直接构造
    sys_cl = signal.TransferFunction(num, den)
    return sys_cl, poles, stable

# ===== Plant: G(s) = 2 / (s^2 + 3s + 2) =====
G_num, G_den = [2], [1, 3, 2]
print("=" * 55)
print("PID Control - Ziegler-Nichols Tuning")
print("=" * 55)
print("\nPlant: G(s) = 2 / (s^2 + 3s + 2) = 2/((s+1)(s+2))")

# ===== Ziegler-Nichols Step Response Method =====
# 估计: K=2, T=1, theta=0.3
K, T, theta = 2.0, 1.0, 0.3
print(f"\nEstimated FOPDT: K={K}, T={T}, theta={theta}")
Kp_zig = 1.2 * T / (K * theta)
Ti_zig = 2 * theta
Td_zig = 0.5 * theta
Ki_zig = Kp_zig / Ti_zig
Kd_zig = Kp_zig * Td_zig
print(f"Z-N PID: Kp={Kp_zig:.3f}, Ki={Ki_zig:.3f}, Kd={Kd_zig:.3f}")

# ===== 对比配置 =====
configs = [
    (Kp_zig, Ki_zig, Kd_zig, 'Ziegler-Nichols'),
    (2.0, 0.5, 1.0, 'Manual Set 1'),
    (1.0, 0.2, 0.5, 'Manual Set 2'),
    (0, 0, 0, 'Open Loop'),
]

t = np.linspace(0, 10, 1000)
results = []

print("\n" + "=" * 55)
print("Performance Analysis")
print("=" * 55)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('PID Control - Step Response Comparison', fontsize=14)

for idx, (Kp, Ki, Kd, name) in enumerate(configs):
    ax = axes[idx // 2, idx % 2]
    
    if Kp == 0 and Ki == 0 and Kd == 0:
        sys_ol = signal.TransferFunction(G_num, G_den)
        t_out, y_out = signal.step(sys_ol, T=t)
        ax.plot(t_out, y_out, 'r-', lw=2, label='Open Loop')
        poles_str = "[-1, -2]"
    else:
        sys_cl, poles, stable = closed_loop_pid(Kp, Ki, Kd, G_num, G_den)
        if not stable:
            ax.plot(t, np.zeros_like(t) + 1.1, 'gray', lw=1, label='UNSTABLE')
            ax.text(5, 1.1, 'UNSTABLE', fontsize=12, color='red')
            poles_str = str([f'{p.real:.2f}' for p in poles])
            Mp, ts, y_ss = float('nan'), float('nan'), float('nan')
        else:
            t_out, y_out = signal.step(sys_cl, T=t)
            ax.plot(t_out, y_out, 'b-', lw=2, label=f'PID: {name}')
            
            # 指标计算
            y_peak = np.max(y_out)
            overshoot = (y_peak - 1) * 100 if y_peak > 1 else 0
            idx_settled = np.where(np.abs(y_out - 1) < 0.02)[0]
            ts = t_out[idx_settled[0]] if len(idx_settled) > 0 else float('nan')
            y_ss = y_out[-1]
            poles_str = str([f'{p.real:.2f}' for p in poles])
            
            ax.axhline(y=1, color='gray', ls='--', alpha=0.5)
            ax.set_title(f'{name}\nKp={Kp:.2f}, Ki={Ki:.2f}, Kd={Kd:.2f}\nMp={overshoot:.1f}%, ts={ts:.2f}s, y_ss={y_ss:.3f}\nPoles: {poles_str}')
            results.append((name, overshoot, ts, y_ss, stable))
    
    ax.axhline(y=1, color='gray', ls='--', alpha=0.5)
    ax.set_xlabel('t (s)')
    ax.set_ylabel('y(t)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.5)

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day6_pid_comparison.png', dpi=150, bbox_inches='tight')
print("Figure 1 saved!")

# ===== PID 三项物理作用 =====
print("\n" + "=" * 55)
print("PID Physical Meaning")
print("=" * 55)
print("""
比例 P:
  u(t) = Kp * e(t)
  - 即时响应误差，成比例放大
  - Kp大 → 响应快，但超调大，振荡多
  - Kp小 → 迟钝，稳态误差残留

积分 I:
  u(t) = Ki * ∫e(t)dt
  - 累积历史误差，消除稳态误差
  - Ki大 → 消除稳态误差快，但超调大
  - Ki小 → 积分作用弱，消除误差慢

微分 D:
  u(t) = Kd * de(t)/dt
  - 预测误差趋势，提前制动
  - Kd大 → 抑制超调，但噪声敏感
  - Kd小 → 微分作用弱，抑制超调效果差

Ziegler-Nichols 经验整定（适用于一阶延时系统）:
  Kp = 1.2*T/(K*L), Ti=2*L, Td=0.5*L
  （基于阶跃响应法）
""")
