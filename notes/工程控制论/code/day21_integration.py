import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg

print("=" * 60)
print("Day 21: Week 3 Integration - Drone Altitude Control")
print("=" * 60)

# ===== Drone Dynamics =====
# Vertical dynamics: m*z_ddot = T - mg - c*z_dot
# State: x = [z, z_dot] = [altitude, velocity]
# Control: u = T (thrust)

m = 1.0
g = 9.81
c = 0.5  # drag coefficient

# Operating point: hover at z=0, T=mg
T_eq = m * g  # equilibrium thrust

A = np.array([[0, 1], [0, -c/m]])
B = np.array([[0], [1/m]])
C = np.array([[1, 0]])

print(f"\nDrone hover dynamics:")
print(f"  A={A.tolist()}, B={B.flatten().tolist()}")
print(f"  Equilibrium thrust: {T_eq:.2f} N")

# ===== Controllers to Compare =====
# 1. LQR (Week 2)
Q_lqr = np.diag([50.0, 5.0])
R_lqr = np.array([[0.5]])
P_lqr = linalg.solve_continuous_are(A, B, Q_lqr, R_lqr)
K_lqr = (linalg.inv(R_lqr) @ B.T @ P_lqr).flatten()

# 2. H-infinity (Week 3)
gamma_sq = 2.0
P_hinf = linalg.solve_continuous_are(A.T, C.T, np.eye(2)*10, np.array([[gamma_sq]]))
K_hinf = (P_hinf @ C.T / gamma_sq).flatten()

# 3. Sliding Mode (Week 3)
lam_smc = 3.0
K_smc = 5.0
delta_smc = 0.2

print(f"\nController gains:")
print(f"  LQR: K={K_lqr.round(2)}")
print(f"  H-inf: K={K_hinf.round(2)}")
print(f"  SMC: lambda={lam_smc}, K={K_smc}")

# ===== Disturbance: wind gusts (bounded) =====
np.random.seed(42)
T = 6.0
dt = 0.001
N = int(T / dt)
t = np.linspace(0, T, N)

# Wind gusts: sinusoidal + random components
wind = 0.5 * np.sin(2.0 * t) + 0.3 * np.sin(5.0*t) + 0.2 * np.random.randn(N)
wind = np.clip(wind, -1.5, 1.5)

# ===== Simulations =====
def simulate(A, B, C, K, x0, control_type, wind_force, N, dt):
    x = np.zeros((N, 2))
    u_hist = np.zeros(N)
    x[0] = x0
    for i in range(N-1):
        if control_type == 'LQR':
            u = -np.dot(K, x[i])
        elif control_type == 'Hinf':
            u = -np.dot(K, x[i])
        elif control_type == 'SMC':
            e = x[i, 0] - target_alt
            e_dot = x[i, 1]
            s = e_dot + lam_smc * e
            u = -K_smc * np.clip(s/delta_smc, -1, 1)
        u = np.clip(u, 0, 30)  # physical limit: thrust >= 0
        thrust = T_eq + u
        x[i+1, 1] = x[i, 1] + ((thrust - m*g - c*x[i, 1])/m + wind_force[i]) * dt
        x[i+1, 0] = x[i, 0] + x[i, 1] * dt
        u_hist[i] = u
    return x, u_hist

target_alt = 10.0
x0_lqr = [0.0, 0.0]
x0_hinf = [0.0, 0.0]
x0_smc = [0.0, 0.0]

x_lqr, u_lqr = simulate(A, B, C, K_lqr, x0_lqr, 'LQR', wind, N, dt)
x_hinf, u_hinf = simulate(A, B, C, K_hinf, x0_hinf, 'Hinf', wind, N, dt)
x_smc, u_smc = simulate(A, B, C, K_lqr, x0_smc, 'SMC', wind, N, dt)

# Metrics
def tracking_error(x, target):
    return np.sqrt(np.mean((x[:, 0] - target)**2))

def control_effort(u):
    return np.sqrt(np.mean(u**2))

print(f"\n===== Performance Metrics =====")
print(f"{'Controller':<12} {'RMS Error (m)':<18} {'RMS Control':<15}")
print(f"{'LQR':<12} {tracking_error(x_lqr, target_alt):<18.3f} {control_effort(u_lqr):<15.3f}")
print(f"{'H-inf':<12} {tracking_error(x_hinf, target_alt):<18.3f} {control_effort(u_hinf):<15.3f}")
print(f"{'SMC':<12} {tracking_error(x_smc, target_alt):<18.3f} {control_effort(u_smc):<15.3f}")

# ===== Plot =====
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Day 21: Week 3 Integration - Drone Altitude Control', fontsize=14)

ax = axes[0, 0]
ax.plot(t, x_lqr[:, 0], 'b-', lw=2, label='LQR')
ax.plot(t, x_hinf[:, 0], 'orange', lw=2, label='H-inf')
ax.plot(t, x_smc[:, 0], 'green', lw=2, label='SMC')
ax.axhline(y=target_alt, color='red', ls='--', lw=2, label='Target')
ax.set_xlabel('t (s)')
ax.set_ylabel('Altitude (m)')
ax.set_title('Altitude Tracking')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(t, u_lqr, 'b-', lw=1.5, label='LQR')
ax.plot(t, u_hinf, 'orange', lw=1.5, label='H-inf')
ax.plot(t, u_smc, 'green', lw=1.5, label='SMC')
ax.set_xlabel('t (s)')
ax.set_ylabel('Thrust (N)')
ax.set_title('Control Effort')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 2]
ax.plot(t, wind, 'gray', lw=1, alpha=0.5, label='Wind disturbance')
ax.set_xlabel('t (s)')
ax.set_ylabel('Wind (m/s)')
ax.set_title('Wind Gusts (bounded disturbance)')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(x_lqr[:, 0], x_lqr[:, 1], 'b-', lw=1.5, label='LQR')
ax.plot(x_hinf[:, 0], x_hinf[:, 1], 'orange', lw=1.5, label='H-inf')
ax.plot(x_smc[:, 0], x_smc[:, 1], 'green', lw=1.5, label='SMC')
ax.scatter([target_alt], [0], color='red', s=100, zorder=5, label='Target')
ax.set_xlabel('Altitude')
ax.set_ylabel('Velocity')
ax.set_title('Phase Plane')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.plot(t, x_lqr[:, 0]-target_alt, 'b-', lw=1.5, label='LQR error')
ax.plot(t, x_hinf[:, 0]-target_alt, 'orange', lw=1.5, label='H-inf error')
ax.plot(t, x_smc[:, 0]-target_alt, 'green', lw=1.5, label='SMC error')
ax.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('t (s)')
ax.set_ylabel('Altitude Error')
ax.set_title('Tracking Error')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 2]
ax.axis('off')
txt = ("""Week 3 Integration Summary:\n\n"""
       """Controllers Compared:\n"""
       """  LQR (Week 2): min integral(x'Qx+u'Ru)\n"""
       """  H-inf (Week 3): min worst-case ||Tzw||inf\n"""
       """  SMC (Week 3): robust to bounded disturbances\n\n"""
       """Key Concepts Integrated:\n"""
       """  - Variational (Pontryagin)\n"""
       """  - Stochastic (bounded wind gusts)\n"""
       """  - Lyapunov (stability analysis)\n"""
       """  - Sliding Mode (chattering)\n"""
       """  - Feedback Linearization (hover dynamics)\n"""
       """  - H-inf (robustness)\n\n"""
       """Trade-offs:\n"""
       """  LQR: smooth but sensitive to model error\n"""
       """  H-inf: worst-case bounded but conservative\n"""
       """  SMC: very robust but chattering\n"""
       """  -> Choice depends on disturbance type!""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=11,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day21_integration.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")

# ===== Week 3 Summary =====
print("\n" + "=" * 60)
print("WEEK 3 COMPLETE - Summary")
print("=" * 60)
print("""
Week 3: Nonlinear + Optimal + Robust Control

Day 15: Variational + Pontryagin
  - Euler-Lagrange equation
  - Bang-Bang = time-optimal control
  - u* = argmin H

Day 16: Stochastic Processes
  - Wiener process, Itô calculus
  - Ornstein-Uhlenbeck
  - Kalman = optimal trade model vs measurement

Day 17: Lyapunov Direct Method
  - V > 0, V_dot < 0 => asymptotically stable
  - LaSalle invariance principle

Day 18: Describing Function + SMC
  - N(A) for relay/saturation
  - Sliding mode: s = 0, u = -K*sign(s)
  - Chattering reduction: boundary layer

Day 19: Backstepping + Feedback Linearization
  - Cancel nonlinearities exactly
  - Requires accurate model

Day 20: H-infinity Control
  - Minimizes worst-case amplification
  - ||Tzw||_inf < gamma
  - Robust to bounded disturbances

Day 21: Integration Project
  - Drone altitude: LQR vs H-inf vs SMC
  - Wind gusts (bounded disturbance)
  - Full Week 3 concepts integrated!
""")
