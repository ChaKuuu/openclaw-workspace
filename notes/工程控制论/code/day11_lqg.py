import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg

print("=" * 60)
print("Day 11: LQG = LQR + Kalman Filter")
print("=" * 60)

A = np.array([[0.0, 1.0], [-2.0, -3.0]])
B = np.array([[0.0], [2.0]])
C = np.array([[1.0, 0.0]])

Q_lqr = np.diag([10.0, 1.0])
R_lqr = np.array([[0.1]])
P_lqr = linalg.solve_continuous_are(A, B, Q_lqr, R_lqr)
K_lqr = (linalg.inv(R_lqr) @ B.T @ P_lqr).flatten()
A_cl = A - np.outer(B, K_lqr)
print(f"LQR K: {K_lqr.round(3)}, CL poles: {linalg.eigvals(A_cl).real.round(2)}")

Q_kf = np.eye(2) * 0.5
R_kf = np.array([[2.0]])
P_kf = linalg.solve_continuous_are(A.T, C.T, Q_kf, R_kf)
K_kf = (P_kf @ C.T / R_kf[0,0]).flatten()
print(f"Kalman Kf: {K_kf.round(3)}")

np.random.seed(42)
T = 5.0
dt = 0.005
N = int(T / dt)
t = np.linspace(0, T, N)

w = np.sqrt(Q_kf.diagonal()/dt) * np.random.randn(N, 2)
v = np.sqrt(R_kf[0,0]) * np.random.randn(N)

x = np.zeros((N, 2))
xh = np.zeros((N, 2))
y = np.zeros(N)
u = np.zeros(N)

x[0, 0] = 1.0
x[0, 1] = 0.0
xh[0, 0] = 0.0
xh[0, 1] = 0.0

for i in range(N-1):
    u[i] = -np.dot(K_lqr, xh[i])
    x_dot = np.dot(A, x[i]) + np.dot(B.flatten(), u[i]) + w[i]
    x[i+1] = x[i] + x_dot * dt
    y[i] = np.dot(C, x[i])[0] + v[i]
    xh_dot = np.dot(A, xh[i]) + np.dot(B.flatten(), u[i]) + K_kf * (y[i] - np.dot(C, xh[i]))
    xh[i+1] = xh[i] + xh_dot * dt

print(f"Done. Final true: {x[-1]}, final est: {xh[-1]}")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 11: LQG = LQR + Kalman Filter', fontsize=14)

ax = axes[0, 0]
ax.plot(t, x[:,0], 'b-', lw=2, label='True x1')
ax.plot(t, xh[:,0], 'g--', lw=2, label='Est x1')
ax.plot(t[::10], y[::10], 'r.', ms=3, alpha=0.4, label='Meas')
ax.set_xlabel('t')
ax.set_ylabel('x1')
ax.set_title('Position')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(t, x[:,1], 'b-', lw=2, label='True x2')
ax.plot(t, xh[:,1], 'g--', lw=2, label='Est x2')
ax.set_xlabel('t')
ax.set_ylabel('x2')
ax.set_title('Velocity')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(t, x[:,0]-xh[:,0], 'b-', lw=1.5, label='x1 error')
ax.plot(t, x[:,1]-xh[:,1], 'orange', lw=1.5, label='x2 error')
ax.set_xlabel('t')
ax.set_ylabel('Error')
ax.set_title('Estimation Error')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.plot(t, u, 'purple', lw=2, label='u=-K_lqr*xh')
ax.set_xlabel('t')
ax.set_ylabel('Control')
ax.set_title('LQR Control (uses estimated state)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day11_lqg.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
