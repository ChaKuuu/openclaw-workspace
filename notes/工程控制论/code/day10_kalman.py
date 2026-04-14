import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg

print("=" * 60)
print("Day 10: Kalman Filter")
print("=" * 60)

# ===== System: 1st order =====
a, b, c = -1.0, 1.0, 1.0
dt = 0.01
Q = np.array([[0.1]])
R = np.array([[1.0]])

print(f"\nSystem: x_dot = {a}*x + {b}*u + w")
print(f"Measurement: y = {c}*x + v")
print(f"Q = {Q[0,0]}, R = {R[0,0]}")

# P_ss analytically: solve 2*A*P + Q - P^2*C^2/R = 0
A_val, C_val, Q_val, R_val = -1.0, 1.0, 0.1, 1.0
P_ss_val = (A_val + np.sqrt(A_val**2 + Q_val * C_val**2 / R_val)) / (C_val**2 / R_val)
print(f"\nSteady-state P (analytical) = {P_ss_val:.4f}")

# ===== Simulate =====
np.random.seed(42)
T = 5.0
N = int(T / dt)
t = np.linspace(0, T, N)

w = np.sqrt(Q[0,0]/dt) * np.random.randn(N)
v = np.sqrt(R[0,0]) * np.random.randn(N)

x_true = np.zeros(N)
y_meas = np.zeros(N)
x_est = np.zeros(N)
P_diag = np.zeros(N)

x = 0.0
x_hat = 0.0
P = 1.0

for i in range(N):
    u = 1.0
    x_dot = a * x + b * u + w[i]
    x = x + x_dot * dt
    x_true[i] = x
    y = c * x + v[i]
    y_meas[i] = y
    
    x_hat_dot = a * x_hat + b * u
    P_dot = a * P + P * a + Q[0,0]
    x_hat = x_hat + x_hat_dot * dt
    P = P + P_dot * dt
    
    S = np.array([[c * P * c + R[0,0]]])
    K = np.array([[P * c / S[0,0]]])
    x_hat = x_hat + K[0,0] * (y - c * x_hat)
    P = (1 - K[0,0] * c) * P
    
    x_est[i] = x_hat
    P_diag[i] = P

print(f"\nMeasurement noise: {np.std(y_meas - x_true):.4f}")
print(f"Estimation error: {np.std(x_est - x_true):.4f}")

# ===== Plot =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 10: Kalman Filter', fontsize=14)

ax = axes[0, 0]
ax.plot(t, x_true, 'b-', lw=1.5, label='True State', alpha=0.8)
ax.plot(t, y_meas, 'r.', ms=2, alpha=0.3, label='Measurement')
ax.plot(t, x_est, 'g-', lw=2, label='Kalman Estimate')
ax.set_xlabel('t (s)')
ax.set_ylabel('x')
ax.set_title('True vs Measured vs Estimated')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.fill_between(t, x_est-3*np.sqrt(P_diag), x_est+3*np.sqrt(P_diag), alpha=0.3, color='green', label='3-sigma')
ax.plot(t, x_est, 'g-', lw=2, label='Estimate')
ax.plot(t, x_true, 'b-', lw=1.5, alpha=0.7, label='True')
ax.set_xlabel('t (s)')
ax.set_ylabel('x')
ax.set_title('Estimate with Uncertainty')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(t, np.abs(x_est - x_true), 'r-', lw=1.5, label='Abs Error')
ax.plot(t, 3*np.sqrt(P_diag), 'g--', lw=2, label='3-sigma bound')
ax.set_xlabel('t (s)')
ax.set_ylabel('Error')
ax.set_title('Estimation Error vs Bound')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.plot(t, P_diag, 'purple', lw=2, label='P(t)')
ax.axhline(y=P_ss_val, color='red', ls='--', label=f'Steady-state={P_ss_val:.3f}')
ax.set_xlabel('t (s)')
ax.set_ylabel('Covariance')
ax.set_title('Error Covariance Convergence')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day10_kalman.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")

print("\n" + "=" * 60)
print("KEY: Kalman Filter")
print("=" * 60)
print("""
Predict:
  x_hat_dot = A*x_hat + B*u
  P_dot = A*P + P*A^T + Q

Correct:
  K = P*C^T * R^(-1)
  x_hat = x_hat + K*(y - C*x_hat)
  P = (I - K*C)*P

Kalman Gain:
  K_ss = P_ss*C^T/R
  - R small (good sensor) -> K large -> trust measurement
  - Q large (noisy process) -> K small -> trust model
""")
