import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal

# ===== Day 4: Bode Diagram + Frequency Response =====

# 定义系统
# G(s) = K / (Ts + 1)  惯性环节
K, T = 2.0, 1.0
sys_inertia = signal.TransferFunction([K], [T, 1])

# 频率范围
omega = np.logspace(-2, 2, 500)  # 0.01 to 100 rad/s

# 计算频率响应
w, H = signal.freqresp(sys_inertia, omega)
mag = np.abs(H)
phase = np.angle(H, deg=True)

# ===== 解析近似（折线）=====
# 惯性环节: |G(jw)| = K / sqrt(1 + (wT)^2)
# 相角: ang = -arctan(wT)
mag_analytical = K / np.sqrt(1 + (omega * T)**2)
phase_analytical = -np.degrees(np.arctan(omega * T))

# ===== 转折频率 = 1/T = 1 rad/s =====
wc = 1 / T

# ===== 手绘折线近似的关键点 =====
# 低频: 0dB (K=2 = 20*log10(2) = 6.02dB)
mag_low_db = 20 * np.log10(K)
# 高频斜率: -20dB/dec
# 在wc处: 6.02dB
# wc之后: 每10倍频下降20dB

# 幅值图
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle('Bode Diagram: G(s) = K/(Ts+1), K=2, T=1', fontsize=14)

# ===== 幅值图 =====
ax1 = axes[0]
ax1.semilogx(omega, 20*np.log10(mag), 'b-', lw=2, label='Numerical')
ax1.semilogx(omega, 20*np.log10(mag_analytical), 'r--', lw=1.5, label='Analytical')

# 折线近似
# 低频: 6.02dB 水平线
omega_low = omega[omega < wc]
omega_high = omega[omega >= wc]
mag_low_db_line = np.full_like(omega_low, mag_low_db, dtype=float)
mag_high_db = mag_low_db - 20*np.log10(omega_high * T)
ax1.semilogx(omega_low, mag_low_db_line, 'g-', lw=2, label='Asymptotic')
ax1.semilogx(omega_high, mag_high_db, 'g-', lw=2)

# 转折频率标注
ax1.axvline(x=wc, color='orange', linestyle='--', alpha=0.7, label=f'Corner freq wc=1 rad/s')
ax1.axhline(y=mag_low_db, color='gray', linestyle=':', alpha=0.5)
ax1.axvline(x=10, ymin=0, ymax=1, color='purple', linestyle='--', alpha=0.5)

# 标注关键值
ax1.scatter([wc], [mag_low_db], color='red', zorder=5, s=80)
ax1.annotate(f'({wc:.1f}, {mag_low_db:.1f}dB)', xy=(wc, mag_low_db),
            xytext=(wc*2, mag_low_db+3), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='gray'))

ax1.set_ylabel('Magnitude (dB)')
ax1.set_title('Magnitude Plot')
ax1.legend()
ax1.grid(True, which='both', alpha=0.3)
ax1.set_ylim(-40, 20)

# ===== 相角图 =====
ax2 = axes[1]
ax2.semilogx(omega, phase, 'b-', lw=2, label='Numerical')
ax2.semilogx(omega, phase_analytical, 'r--', lw=1.5, label='Analytical')

# 折线近似相角
phase_low = np.full_like(omega_low, 0, dtype=float)
phase_high = -90 * np.ones_like(omega_high)
phase_high[omega_high * T < 0.1] = 0
phase_high[omega_high * T > 10] = -90
# 简单折线: -45deg/dec at wc
phase_asymp = np.zeros_like(omega)
for i, w_val in enumerate(omega):
    if w_val < wc / 10:
        phase_asymp[i] = 0
    elif w_val > wc * 10:
        phase_asymp[i] = -90
    else:
        phase_asymp[i] = -45 * np.log10(w_val * T)
ax2.semilogx(omega, phase_asymp, 'g-', lw=2, label='Asymptotic')
ax2.axvline(x=wc, color='orange', linestyle='--', alpha=0.7, label=f'wc={wc}')
ax2.axhline(y=-45, color='gray', linestyle=':', alpha=0.5)

ax2.set_xlabel('Frequency (rad/s)')
ax2.set_ylabel('Phase (deg)')
ax2.set_title('Phase Plot')
ax2.legend()
ax2.grid(True, which='both', alpha=0.3)
ax2.set_ylim(-100, 10)

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day4_bode_inertia.png', dpi=150, bbox_inches='tight')
print("Figure 1 saved: day4_bode_inertia.png")

# ===== 二阶系统的 Bode 图 =====
print("\n===== Bode: Second Order System =====")
wn, zeta = 2.0, 0.3
sys2 = signal.TransferFunction([wn**2], [1, 2*zeta*wn, wn**2])
w2, H2 = signal.freqresp(sys2, omega)
mag2 = np.abs(H2)
phase2 = np.angle(H2, deg=True)

fig2, axes2 = plt.subplots(2, 1, figsize=(12, 8))
fig2.suptitle(f'Bode Diagram: G(s) = wn^2/(s^2+2*zeta*wn*s+wn^2)\n wn={wn}, zeta={zeta}', fontsize=14)

# 峰值
peak_idx = np.argmax(mag2)
peak_mag = mag2[peak_idx]
peak_w = w2[peak_idx]
peak_db = 20*np.log10(peak_mag)
resonance_db = peak_db - 20*np.log10(1)  # 相对0dB的峰值

axes2[0].semilogx(w2, 20*np.log10(mag2), 'b-', lw=2)
axes2[0].axvline(x=peak_w, color='red', linestyle='--', alpha=0.7, label=f'Peak: w={peak_w:.2f}, {peak_db:.1f}dB')
axes2[0].axhline(y=0, color='gray', linestyle=':', alpha=0.5)
axes2[0].set_ylabel('Magnitude (dB)')
axes2[0].set_title('Magnitude - Resonance Peak')
axes2[0].legend()
axes2[0].grid(True, which='both', alpha=0.3)

axes2[1].semilogx(w2, phase2, 'b-', lw=2)
axes2[1].axvline(x=wn, color='orange', linestyle='--', alpha=0.7, label=f'wn={wn}')
axes2[1].set_xlabel('Frequency (rad/s)')
axes2[1].set_ylabel('Phase (deg)')
axes2[1].set_title('Phase')
axes2[1].legend()
axes2[1].grid(True, which='both', alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day4_bode_second_order.png', dpi=150, bbox_inches='tight')
print("Figure 2 saved: day4_bode_second_order.png")
print(f"\nResonance peak: {resonance_db:.1f} dB at w={peak_w:.2f} rad/s")

# ===== 关键公式打印 =====
print("\n" + "=" * 55)
print("KEY FORMULAS - Frequency Response")
print("=" * 55)
print(f"\nInertia: G(s) = K/(Ts+1)")
print(f"  |G(jw)| = K / sqrt(1 + (wT)^2)")
print(f"  ang G(jw) = -arctan(wT)")
print(f"  Corner freq: wc = 1/T = {1/T} rad/s")
print(f"  At wc: |G| = K/sqrt(2) = {K/np.sqrt(2):.3f} ({20*np.log10(K/np.sqrt(2)):.2f} dB)")

print(f"\nSecond Order: wn={wn}, zeta={zeta}")
print(f"  Mr = 1/(2*zeta*sqrt(1-zeta^2)) (resonance peak)")
if zeta < 1/np.sqrt(2):
    Mr = 1/(2*zeta*np.sqrt(1-zeta**2))
    print(f"  Mr = {Mr:.2f} ({20*np.log10(Mr):.2f} dB)")
    print(f"  Peak frequency: wp = wn*sqrt(1-2*zeta^2) = {wn*np.sqrt(1-2*zeta**2):.3f}")
else:
    print(f"  No resonance peak (zeta >= 1/sqrt(2))")
