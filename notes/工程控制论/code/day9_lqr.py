import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg

# ===== Day 9: LQR (Linear Quadratic Regulator) =====

print("=" * 60)
print("Day 9: Linear Quadratic Regulator (LQR)")
print("=" * 60)

# ===== System =====
A = np.array([[0, 1], [-2, -3]], dtype=float)
B = np.array([[0], [2]], dtype=float)
Q = np.diag([10.0, 1.0])   # State cost (penalize position more)
R = np.array([[0.1]])         # Input cost (small control effort)
print("\nSystem:")
print(f"  A = {A.tolist()}")
print(f"  B = {B.flatten().tolist()}")
print(f"  Q = diag({Q.diagonal()})  (state weight)")
print(f"  R = {R.flatten()}  (control weight)")

# ===== LQR Solution =====
# Solve Riccati: A^T*P + P*A - P*B*R^(-1)*B^T*P + Q = 0
# K = R^(-1) * B^T * P
# u = -K*x
P = linalg.solve_continuous_are(A, B, Q, R)
K = linalg.inv(R) @ B.T @ P
A_cl = A - B @ K
lam_cl = linalg.eigvals(A_cl)

print(f"\n===== LQR Solution =====")
print(f"P = \n{P.round(4)}")
print(f"\nK = R^-1 * B^T * P = {K.flatten().round(4)}")
print(f"\nCL poles: {lam_cl.real.round(4)}")

# ===== Compare: Pole Placement vs LQR =====
# Pole placement at -3, -5 (from Day 8)
from scipy import signal
desired = np.array([-3.0, -5.0])
result = signal.place_poles(A, B, desired)
K_pp = result.gain_matrix
A_cl_pp = A - B @ K_pp
lam_cl_pp = linalg.eigvals(A_cl_pp)

print(f"\n===== Comparison: Pole Placement vs LQR =====")
print(f"Pole Placement: K = {K_pp.flatten().round(4)}, poles = {lam_cl_pp.real.round(2)}")
print(f"LQR:            K = {K.flatten().round(4)}, poles = {lam_cl.real.round(2)}")
print(f"\nLQR gives: smaller control effort (minimizes u^T*R*u + x^T*Q*x)")

# ===== Simulation =====
t = np.linspace(0, 5, 500)
dt = t[1] - t[0]

def sim(Acl, x0, label):
    x = np.zeros((len(t), 2))
    u = np.zeros(len(t))
    cost = 0
    for i in range(len(t)-1):
        u[i] = -K_pp.flatten() @ x[i] if label.startswith('PP') else -K.flatten() @ x[i]
        cost += (x[i] @ Q @ x[i] + u[i]**2 * R[0,0]) * dt
        x[i+1] = x[i] + (Acl @ x[i] + B.flatten() * u[i]) * dt
    return x, u, cost

x0 = np.array([1.0, 0.0])  # initial state: pos=1, vel=0

x_lqr, u_lqr, cost_lqr = sim(A_cl, x0, 'LQR')
x_pp, u_pp, cost_pp = sim(A_cl_pp, x0, 'PP')

print(f"\n===== Cost Comparison =====")
print(f"LQR total cost (J = int(x'Qx + u'Ru dt)): {cost_lqr:.4f}")
print(f"Pole Placement total cost: {cost_pp:.4f}")
print(f"LQR reduces cost by: {(1 - cost_lqr/cost_pp)*100:.1f}%")

# ===== Plot =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 9: LQR Optimal Control', fontsize=14)

ax = axes[0, 0]
ax.plot(t, x_pp[:, 0], 'b-', lw=2, label='Pole Placement x1')
ax.plot(t, x_lqr[:, 0], 'g--', lw=2, label='LQR x1')
ax.set_xlabel('t (s)')
ax.set_ylabel('Position x1')
ax.set_title('Position Response')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(t, u_pp, 'b-', lw=2, label='Pole Placement u')
ax.plot(t, u_lqr, 'g--', lw=2, label='LQR u')
ax.set_xlabel('t (s)')
ax.set_ylabel('Control u')
ax.set_title('Control Effort')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(t, x_pp[:, 0], 'b-', lw=2, label='PP x1')
ax.plot(t, x_pp[:, 1], 'orange', lw=2, label='PP x2')
ax.plot(t, x_lqr[:, 0], 'g--', lw=2, label='LQR x1')
ax.plot(t, x_lqr[:, 1], 'r--', lw=2, label='LQR x2')
ax.set_xlabel('t (s)')
ax.set_ylabel('State')
ax.set_title('All States: Pole Placement vs LQR')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
txt = (f"LQR Results:\n"
       f"  K = {K.flatten().round(3)}\n"
       f"  CL poles: {lam_cl.real.round(2)}\n\n"
       f"Cost Comparison:\n"
       f"  Pole Placement: {cost_pp:.4f}\n"
       f"  LQR:            {cost_lqr:.4f}\n"
       f"  Improvement:    {(1-cost_lqr/cost_pp)*100:.1f}%\n\n"
       f"LQR finds K that minimizes:\n"
       f"  J = int(x'Qx + u'Ru) dt\n"
       f"  subject to x_dot = Ax + Bu")
ax.text(0.1, 0.9, txt, transform=ax.transAxes, va='top', fontsize=11, fontfamily='monospace')
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day9_lqr.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")

# ===== Key Formulas =====
print("\n" + "=" * 60)
print("KEY FORMULAS - LQR")
print("=" * 60)
print("""
Continuous-time LQR:

Minimize:
  J = integral (x'Qx + u'Ru) dt
  subject to: x_dot = Ax + Bu

Solution (Riccati Equation):
  A'P + PA - PB*R^(-1)*B'P + Q = 0

Optimal Feedback:
  K = R^(-1) * B' * P
  u = -K*x

Properties:
  - LQR guarantees closed-loop stability
  - Trades off: state deviation vs control effort
  - Q large -> aggressive state tracking
  - R large -> conservative control
""")
