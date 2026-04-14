import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 28: FINAL - Personal ACS + Qian Xuesen System")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Day 28: Personal ACS Algorithm + System Integration', fontsize=14)

T = 30.0
dt = 0.1
N = int(T/dt)
t = np.linspace(0, T, N)
C = np.zeros(N)
C[0] = 0.1
u_study = np.ones(N) * 1.0
decay = 0.05
for i in range(N-1):
    C[i+1] = C[i] + (u_study[i] - decay * C[i]) * dt

desired_C = 1.0 * np.ones(N)
e = desired_C - C
Kp, Ki, Kd = 2.0, 0.5, 0.3
integral_e = np.cumsum(e) * dt
derivative_e = np.gradient(e, dt)
u_adaptive = np.clip(Kp * e + Ki * integral_e + Kd * derivative_e, 0, 2)
C_adaptive = np.zeros(N)
C_adaptive[0] = 0.1
for i in range(N-1):
    C_adaptive[i+1] = C_adaptive[i] + (u_adaptive[i] - decay * C_adaptive[i]) * dt

ax = axes[0, 0]
ax.plot(t, C, 'b--', lw=2, alpha=0.7, label='Constant study')
ax.plot(t, C_adaptive, 'orange', lw=2, label='ACS adaptive')
ax.axhline(y=1.0, color='red', ls=':', alpha=0.5, label='Goal C=1')
ax.set_xlabel('Days')
ax.set_ylabel('Capability C')
ax.set_title('Personal ACS: Capability Growth')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.axis('off')
ax.text(0.02, 0.98,
    "28-Day Control Theory Journey:\n\n"
    "WEEK 1 (Days 1-7): Classical Control\n"
    "  - Transfer functions, Bode, Nyquist\n"
    "  - PID, Routh-Hurwitz\n"
    "  - Foundation: stability above all\n\n"
    "WEEK 2 (Days 8-14): Modern Control\n"
    "  - State space, LQR\n"
    "  - Kalman Filter, LQG\n"
    "  - Separation principle\n\n"
    "WEEK 3 (Days 15-21): Advanced\n"
    "  - Variational, Pontryagin\n"
    "  - Lyapunov, Sliding Mode\n"
    "  - H-infinity, Feedback Linearization\n\n"
    "WEEK 4 (Days 22-28): Applications\n"
    "  - Reliability, Redundancy\n"
    "  - Human-Machine, Complex Systems\n"
    "  - Information Theory\n"
    "  - Networked Control\n"
    "  - Particle Filter\n"
    "  - Qian Xuesen System Thinking",
    transform=ax.transAxes, va='top', fontsize=10.5,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
ax.set_title('Knowledge Map')

ax = axes[1, 0]
ax.axis('off')
ax.text(0.02, 0.98,
    "Qian Xuesen's System Framework:\n\n"
    "Core: Open Complex Giant System\n"
    "  = Multi-level + Human-in-loop\n"
    "  + Cross-disciplinary\n\n"
    "Methodology:\n"
    "  'From Qualitative to Quantitative\n"
    "   Integrated Methodology'\n\n"
    "Four Pillars:\n"
    "  1. Systems Theory\n"
    "  2. Cybernetics\n"
    "  3. Information Theory\n"
    "  4. Operations Research\n\n"
    "Evolution:\n"
    "  Simple -> Complicated\n"
    "  -> Complex (feedback-rich)\n"
    "  -> Open Complex Giant\n"
    "    (human/social dimension)\n\n"
    "Key Insight:\n"
    "  'Reductionism fails for\n"
    "   open complex giant systems.\n"
    "   You need the integrated\n"
    "   methodology.'",
    transform=ax.transAxes, va='top', fontsize=10.5,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))
ax.set_title("Qian Xuesen's System Thinking")

ax = axes[1, 1]
ax.axis('off')
ax.text(0.02, 0.98,
    "Personal ACS Algorithm\n"
    "(Based on Control Theory):\n\n"
    "ACT:\n"
    "  - PID-like learning controller\n"
    "  - Kp=react, Ki=persist, Kd=anticipate\n\n"
    "PERCEIVE:\n"
    "  - Kalman filter for state estimation\n"
    "  - Filter noise from feedback signals\n"
    "  - Estimate true progress vs apparent\n\n"
    "REFLECT:\n"
    "  - Lyapunov analysis: is V decreasing?\n"
    "  - If V_dot > 0: Bang-Bang intervention\n"
    "  - If stable: continue current strategy\n\n"
    "ADAPT:\n"
    "  - MRAC: adjust parameters online\n"
    "  - Based on tracking error\n\n"
    "System Integration:\n"
    "  - Use all 28 days as sensor data\n"
    "  - Integrate across domains\n"
    "  - Build robust personal system\n\n"
    "=== 28 DAYS COMPLETE ===\n"
    "控制论 Journey Done!\n"
    "钱学森《工程控制论》Finished!",
    transform=ax.transAxes, va='top', fontsize=10.5,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))
ax.set_title('Personal ACS Algorithm')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day28_final.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
print("\n" + "="*60)
print("28-DAY CONTROL THEORY JOURNEY COMPLETE!")
print("="*60)
