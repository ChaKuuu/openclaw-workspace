import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

# ===== Day 1: 典型环节阶跃响应 =====
T = 1.0
K = 2.0
t = np.linspace(0, 5, 1000)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Typical Element Step Responses (K=2, T=1)', fontsize=14)

# 1. 比例环节 K
sys_K = signal.TransferFunction([K], [1])
t_out, y_out = signal.step(sys_K, T=t)
axes[0,0].plot(t_out, y_out, 'b-', linewidth=2)
axes[0,0].set_title(f'Proportional K={K}\n y(t) = {K}')
axes[0,0].set_xlabel('t (s)')
axes[0,0].set_ylabel('y(t)')
axes[0,0].grid(True, alpha=0.3)
axes[0,0].set_ylim(0, K*1.5)

# 2. 惯性环节 K/(Ts+1)
sys_inertia = signal.TransferFunction([K], [T, 1])
t_out, y_out = signal.step(sys_inertia, T=t)
y_analytical = K * (1 - np.exp(-t/T))
axes[0,1].plot(t_out, y_out, 'b-', linewidth=2, label='Numerical')
axes[0,1].plot(t, y_analytical, 'r--', linewidth=1.5, label='Analytical K(1-e^{-t/T})')
axes[0,1].axhline(y=K, color='gray', linestyle=':', alpha=0.5)
axes[0,1].axvline(x=T, color='green', linestyle='--', alpha=0.5, label=f't=T: y={K*(1-np.exp(-1)):.3f}')
axes[0,1].set_title(f'Inertial Element K/(Ts+1)\n T={T}s, K={K}')
axes[0,1].set_xlabel('t (s)')
axes[0,1].set_ylabel('y(t)')
axes[0,1].legend(fontsize=8)
axes[0,1].grid(True, alpha=0.3)

# 3. 积分环节 K/s
sys_int = signal.TransferFunction([K], [1, 0])
t_out, y_out = signal.step(sys_int, T=t)
axes[1,0].plot(t_out, y_out, 'b-', linewidth=2)
axes[1,0].plot(t, K*t, 'r--', linewidth=1.5, label=f'Analytical: {K}*t')
axes[1,0].set_title(f'Integral Element K/s\n y(t) = {K}*t (unbounded)')
axes[1,0].set_xlabel('t (s)')
axes[1,0].set_ylabel('y(t)')
axes[1,0].legend(fontsize=8)
axes[1,0].grid(True, alpha=0.3)

# 4. 实际微分 K*s/(Ts+1)
sys_deriv = signal.TransferFunction([K, 0], [T, 1])
t_out, y_out = signal.step(sys_deriv, T=t)
axes[1,1].plot(t_out, y_out, 'b-', linewidth=2)
axes[1,1].axvline(x=0, color='gray', linestyle=':', alpha=0.5)
axes[1,1].set_title(f'Practical Derivative K*s/(Ts+1)\n Step: (K/T)*e^{-t/T}')
axes[1,1].set_xlabel('t (s)')
axes[1,1].set_ylabel('y(t)')
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
output_path = 'C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day1_step_responses.png'
plt.savefig(output_path, dpi=150)
print(f"Figure saved: {output_path}")

# ===== Time constant physical meaning =====
print("\n===== Time Constant Verification =====")
for tau in [0.5, 1.0, 2.0, 3.0]:
    y_at_tau = K * (1 - np.exp(-1))
    y_at_3t = K * (1 - np.exp(-3))
    print(f"T={tau}s: at t=T y={y_at_tau:.3f} ({y_at_tau/K*100:.1f}%), at t=3T y={y_at_3t:.3f} ({y_at_3t/K*100:.1f}%)")

# ===== Key insight =====
print("\n===== Key Insight =====")
print("Inertial element: y(t) = K * (1 - e^(-t/T))")
print("At t=T:   y = K * 0.632 (63.2% of final value)")
print("At t=2T:  y = K * 0.865 (86.5%)")
print("At t=3T:  y = K * 0.950 (95.0%)")
print("At t=4T:  y = K * 0.982 (98.2%)")
print("At t=5T:  y = K * 0.993 (99.3%)")
print("\nPhysical meaning: T is the time to reach 63.2% of final value")
