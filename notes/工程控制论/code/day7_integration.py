import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

# ===== Day 7: Integration Project =====

print("=" * 60)
print("Day 7: 综合项目 - 二阶系统 + PID + Bode + 稳定性分析")
print("=" * 60)

# ===== Plant: 二阶系统 G(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2) =====
wn, zeta = 2.0, 0.3
G = signal.TransferFunction([wn**2], [1, 2*zeta*wn, wn**2])
print(f"\nPlant: G(s) = {wn}² / (s² + 2*{zeta}*{wn}s + {wn}²)")
print(f"     = {wn**2} / (s² + {2*zeta*wn}s + {wn**2})")

# Step 1: 开环阶跃响应
t = np.linspace(0, 10, 1000)
t_out, y_ol = signal.step(G, T=t)

# Step 2: PID 参数（Z-N 整定估计）
# 估计延时 theta=0.5（保守）
Kp, Ki, Kd = 1.5, 0.8, 0.4
print(f"\nPID Parameters: Kp={Kp}, Ki={Ki}, Kd={Kd}")

# Step 3: 闭环传递函数
# C(s) = (Kd*s² + Kp*s + Ki) / s
# T(s) = C*G / (1 + C*G)
# 特征: s(s² + 2*zeta*wn*s + wn²) + wn²(Kd*s² + Kp*s + Ki) = 0
# s³ + (2*zeta*wn + wn²*Kd)s² + (wn²*Kp + wn²)s + wn²*Ki = 0
char = [1, 2*zeta*wn + wn**2*Kd, wn**2*Kp + wn**2, wn**2*Ki]
cl_poles = np.roots(char)
stable = all(p.real < 0 for p in cl_poles)
print(f"\n闭环极点: {[f'{p:.3f}' for p in cl_poles]}")
print(f"稳定: {stable}")

# 闭环阶跃响应
num_cl = [wn**2*Kd, wn**2*Kp, wn**2*Ki, 0]
den_cl = char
T_cl = signal.TransferFunction(num_cl, den_cl)
t_cl, y_cl = signal.step(T_cl, T=t)

# Step 4: Bode 图
omega = np.logspace(-1, 2, 500)
w_ol, H_ol = signal.freqresp(G, omega)
mag_ol = 20 * np.log10(np.abs(H_ol))
phase_ol = np.angle(H_ol, deg=True)

# 闭环 Bode
w_cl, H_cl = signal.freqresp(T_cl, omega)
mag_cl = 20 * np.log10(np.abs(H_cl))
phase_cl = np.angle(H_cl, deg=True)

# 带宽（-3dB 截止频率）
bw_idx = np.where(mag_cl <= -3)[0]
bw = w_cl[bw_idx[0]] if len(bw_idx) > 0 else np.nan

# 相位裕度（在增益交叉频率）
gc_idx = np.where(mag_ol >= 0)[0]
if len(gc_idx) > 0:
    gc_freq = w_ol[gc_idx[0]]
    gc_phase = phase_ol[gc_idx[0]]
    pm = 180 + gc_phase
else:
    pm = np.nan

print(f"\n性能指标:")
print(f"  带宽 (BW-3dB): {bw:.3f} rad/s")
print(f"  相位裕度 (PM): {pm:.1f}°" if not np.isnan(pm) else "  相位裕度: N/A")

# ===== 可视化 =====
fig = plt.figure(figsize=(16, 12))

# 1. 阶跃响应对比
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(t_out, y_ol, 'b-', lw=2, label='Open Loop')
ax1.plot(t_cl, y_cl, 'g-', lw=2, label='Closed Loop (PID)')
ax1.axhline(y=1, color='gray', ls='--', alpha=0.5)
ax1.set_xlabel('t (s)')
ax1.set_ylabel('y(t)')
ax1.set_title('Step Response Comparison')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 2)

# 2. 极点位置
ax2 = fig.add_subplot(2, 2, 2)
ax2.scatter([p.real for p in cl_poles], [p.imag for p in cl_poles], 
           marker='x', s=150, lw=3, color='red', label='CL Poles', zorder=5)
ol_poles = np.roots([1, 2*zeta*wn, wn**2])
ax2.scatter([p.real for p in ol_poles], [p.imag for p in ol_poles],
           marker='o', s=100, color='blue', label='OL Poles', zorder=5)
ax2.axvline(x=0, color='gray', ls='--', alpha=0.5)
ax2.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax2.set_xlabel('Real')
ax2.set_ylabel('Imaginary')
ax2.set_title(f'Pole Map (Stable: {stable})')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_aspect('equal')

# 3. 开环 Bode 幅值
ax3 = fig.add_subplot(2, 2, 3)
ax3.semilogx(w_ol, mag_ol, 'b-', lw=2, label='Open Loop')
ax3.semilogx(w_cl, mag_cl, 'g--', lw=1.5, label='Closed Loop')
ax3.axhline(y=0, color='gray', ls=':', alpha=0.5)
ax3.set_xlabel('Frequency (rad/s)')
ax3.set_ylabel('Magnitude (dB)')
ax3.set_title(f'Bode Magnitude (BW={bw:.2f} rad/s)')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_ylim(-40, 20)

# 4. 开环 Bode 相位
ax4 = fig.add_subplot(2, 2, 4)
ax4.semilogx(w_ol, phase_ol, 'b-', lw=2, label='Open Loop')
ax4.semilogx(w_cl, phase_cl, 'g--', lw=1.5, label='Closed Loop')
ax4.axhline(y=-180, color='gray', ls=':', alpha=0.5)
ax4.axhline(y=-90, color='gray', ls=':', alpha=0.3)
if not np.isnan(pm):
    ax4.axvline(x=gc_freq, color='orange', ls='--', alpha=0.7, label=f'GC freq, PM={pm:.1f}°')
ax4.set_xlabel('Frequency (rad/s)')
ax4.set_ylabel('Phase (deg)')
ax4.set_title('Bode Phase')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.suptitle('Day 7 Integration: 2nd Order + PID + Bode + Stability', fontsize=14)
plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day7_integration.png', dpi=150, bbox_inches='tight')
print("\nFigure saved: day7_integration.png")

# ===== 最终汇总 =====
print("\n" + "=" * 60)
print("Week 1 Summary: 工程控制论 数学推导")
print("=" * 60)
print("""
Day 1: 传递函数 + 典型环节阶跃响应
  - 4种环节: 比例/惯性/积分/微分
  - 惯性环节: y=K(1-e^{-t/T}), T=63.2%时间常数

Day 2: 二阶系统 + 阻尼比
  - 欠阻尼/临界/过阻尼三类
  - Mp, tp, ts 公式
  - Butterworth最优: zeta=0.707

Day 3: Routh-Hurwitz 稳定性判据
  - 第一列同号 = 稳定
  - K临界稳定计算

Day 4: Bode 图 + 频率特性
  - 折线近似法
  - 谐振峰值 Mr
  - 带宽概念

Day 5: Nyquist 稳定性判据
  - Z = N + P
  - 包围-1点判断稳定性

Day 6: PID 控制 + Ziegler-Nichols
  - P/I/D 三项作用
  - Z-N 整定公式

Day 7: 整合项目
  - 二阶系统 + PID + Bode + 稳定性
""")
