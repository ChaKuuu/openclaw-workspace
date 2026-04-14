import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg, signal

print("=" * 60)
print("Day 14: Week 2 Integration Project")
print("=" * 60)

# ===== Design Problem =====
# Satellite attitude control (2nd order rotational dynamics)
# J * theta_ddot = u  (no friction, torque input)
# State: x = [theta, omega]
# G(s) = 1/(J*s^2), J = 1

J = 1.0
A = np.array([[0, 1], [0, 0]])
B = np.array([[0], [1/J]])
C = np.array([[1, 0]])
print(f"\nSatellite attitude: J={J}")
print(f"A={A.tolist()}, B={B.flatten().tolist()}")

# ===== Step 1: Controllability =====
Cc = np.array([[B.flatten()], [A @ B.flatten()]]).reshape(2, 2)
print(f"\nControllability matrix rank: {np.linalg.matrix_rank(Cc)} (full rank)")

# ===== Step 2: State Feedback (LQR) =====
Q = np.diag([50.0, 10.0])  # penalize angle more
R = np.array([[0.1]])
P = linalg.solve_continuous_are(A, B, Q, R)
K = (linalg.inv(R) @ B.T @ P).flatten()  # shape (2,)
A_cl = A - np.outer(B.flatten(), K)
lam_cl = linalg.eigvals(A_cl)
print(f"\nLQR: K={K.round(3)}, poles={lam_cl.real.round(3)}")

# ===== Step 3: Observer Design (Kalman Filter) =====
Q_kf = np.eye(2) * 0.1
R_kf = np.array([[5.0]])
P_kf = linalg.solve_continuous_are(A.T, C.T, Q_kf, R_kf)
L = (P_kf @ C.T / R_kf[0,0]).flatten()  # observer gain
print(f"Kalman observer gain: L={L.round(3)}")

# ===== Step 4: LQG Controller =====
# u = -K * x_hat
# x_hat_dot = A*x_hat + B*u + L*(y - C*x_hat)
print(f"\nLQG Controller: K={K.round(3)}, Observer L={L.round(3)}")

# ===== Step 5: Simulate =====
np.random.seed(42)
T = 8.0
dt = 0.005
N = int(T / dt)
t = np.linspace(0, T, N)

w = np.sqrt(Q_kf.diagonal()/dt) * np.random.randn(N, 2) * 0.0  # small process noise
v_meas = np.sqrt(R_kf[0,0]) * np.random.randn(N)

x = np.zeros((N, 2))
xh = np.zeros((N, 2))
y = np.zeros(N)
u = np.zeros(N)

x[0] = [0.5, 0.0]   # initial: 0.5 rad offset, zero velocity
xh[0] = [0.0, 0.0]  # wrong initial estimate

for i in range(N-1):
    # True dynamics
    x_dot = A @ x[i] + B.flatten() * u[i]
    x[i+1] = x[i] + x_dot * dt

    # Measurement (only theta is measured)
    y[i] = C[0] @ x[i] + v_meas[i]

    # LQG control
    u[i] = -np.dot(K, xh[i])

    # Observer update
    innovation = C[0] @ xh[i]
    xh_dot = A @ xh[i] + B.flatten() * u[i] + L * (y[i] - innovation)
    xh[i+1] = xh[i] + xh_dot * dt

print(f"\nSimulation done. Final x: {x[-1].round(4)}, xh: {xh[-1].round(4)}")

# ===== Step 6: MRAC alternative (for comparison) =====
# For this simple double integrator, MRAC might be overkill
# but let's simulate one with unknown J
J_est = 0.5  # wrong estimate (half the true J)
theta_mr = np.zeros(N)
omega_mr = np.zeros(N)
u_mr = np.zeros(N)
theta1_mr = np.zeros(N)
theta2_mr = np.zeros(N)

theta_mr[0] = 0.5
xm = np.zeros(N)  # reference model

# Reference model: desired response
am, bm = 3.0, 3.0
xm[0] = 0.5

for i in range(N-1):
    # Reference model (desired 2nd order response)
    xm_dot = -am * xm[i] + bm * 0  # step input = 0, start from init
    xm[i+1] = xm[i] + xm_dot * dt

    # MRAC for double integrator: u = theta1*r + theta2*theta
    r = 0.0  # no reference input, just regulation
    e_mr = theta_mr[i] - xm[i]
    u_mr[i] = theta1_mr[i] * r + theta2_mr[i] * theta_mr[i]

    # Parameter update (MIT rule)
    gamma = 0.5
    theta1_mr[i+1] = theta1_mr[i] - gamma * e_mr * r * dt
    theta2_mr[i+1] = theta2_mr[i] - gamma * e_mr * theta_mr[i] * dt

    # Plant with wrong J
    theta_dot = omega_mr[i]
    omega_dot = u_mr[i] / J_est
    theta_mr[i+1] = theta_mr[i] + theta_dot * dt
    omega_mr[i+1] = omega_mr[i] + omega_dot * dt

# ===== Plot =====
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Day 14: Week 2 Integration - Satellite Attitude LQG Control', fontsize=14)

ax = axes[0, 0]
ax.plot(t, x[:,0], 'b-', lw=2, label='True theta')
ax.plot(t, xh[:,0], 'g--', lw=2, label='Estimated theta')
ax.plot(t, y, 'r.', ms=2, alpha=0.3, label='Measurement')
ax.set_xlabel('t (s)')
ax.set_ylabel('theta (rad)')
ax.set_title('Angle: True vs Estimated vs Measured')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(t, x[:,1], 'b-', lw=2, label='True omega')
ax.plot(t, xh[:,1], 'g--', lw=2, label='Estimated omega')
ax.set_xlabel('t (s)')
ax.set_ylabel('omega (rad/s)')
ax.set_title('Angular Velocity')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 2]
ax.plot(t, u, 'purple', lw=2, label='u = -K*xh')
ax.set_xlabel('t (s)')
ax.set_ylabel('Torque u')
ax.set_title('Control Torque')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(t, x[:,0]-xh[:,0], 'b-', lw=1.5, label='theta error')
ax.plot(t, x[:,1]-xh[:,1], 'orange', lw=1.5, label='omega error')
ax.set_xlabel('t (s)')
ax.set_ylabel('Error')
ax.set_title('Estimation Error')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.plot(x[:,0], x[:,1], 'b-', lw=2, label='True trajectory')
ax.plot(xh[:,0], xh[:,1], 'g--', lw=2, label='Est trajectory')
ax.scatter([0.5], [0], color='red', s=100, zorder=5, label='Start')
ax.scatter([0], [0], color='black', s=100, zorder=5, label='Origin')
ax.set_xlabel('theta')
ax.set_ylabel('omega')
ax.set_title('Phase Plane')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 2]
ax.axis('off')
txt = (f"Week 2 Summary:\n\n"
       f"Plant: 2nd order integrator\n"
       f"  A={A.flatten()}, B={B.flatten()}\n\n"
       f"LQR: K={K.round(2)}\n"
       f"  CL poles: {lam_cl.real.round(2)}\n\n"
       f"Kalman: L={L.round(2)}\n"
       f"  (theta only measured)\n\n"
       f"MRAC: online adaptation\n"
       f"  (unknown inertia)\n\n"
       f"Key insight:\n"
       f"  LQG = LQR + Kalman\n"
       f"  Separation principle holds\n"
       f"  -> design independently!")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=11,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Week 2 Integration Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day14_integration.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")

print("\n" + "=" * 60)
print("WEEK 2 COMPLETE - Key Takeaways")
print("=" * 60)
print(f"""
Week 2 Architecture (Linear Modern Control):

Day 8:  State Space
  x_dot = Ax + Bu, y = Cx + Du
  Controllability: rank(Cc) = n
  Observability: rank(O) = n

Day 9:  LQR (Optimal Control)
  min J = integral(x'Qx + u'Ru)dt
  K = R^(-1)*B'*P  (Riccati)

Day 10: Kalman Filter (Optimal Estimation)
  Predict: x_hat_dot, P_dot
  Correct: K = P*C'*R^(-1)

Day 11: LQG = LQR + Kalman
  Separation principle: design independently!

Day 12: MRAC (Adaptive Control)
  MIT rule: theta_dot = -gamma*e*phi
  Online learning for unknown parameters

Day 13: Nonlinear
  Phase plane, limit cycles, Lyapunov indirect

Day 14: Integration Project
  Satellite attitude: LQG controller
  Complete Week 2 architecture!
""")
