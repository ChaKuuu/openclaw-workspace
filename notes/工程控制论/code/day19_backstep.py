import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg

print("=" * 60)
print("Day 19: Backstepping + Feedback Linearization")
print("=" * 60)

# ===== Backstepping =====
# For systems in strict-feedback form:
#   x1_dot = x2 + phi1(x1)
#   x2_dot = u + phi2(x1, x2)
# Design K such that x -> 0
#
# Step 1: Treat x2 as virtual control for x1
#   Let z1 = x1, define error e1 = z1 - alpha1
#   alpha1 = -z1  (stabilize x1 subsystem)
#
# Step 2: z2 = x2 - alpha1, design u to stabilize z2

print("""
========================================
Backstepping Control
========================================

Purpose: Stabilize systems in strict-feedback form
  x1_dot = x2 + phi1(x1)
  x2_dot = u + phi2(x1, x2)
  ...
  xn_dot = u + phin(x)

Key Idea: Design virtual control alpha_i for each subsystem,
  then backpropagate errors to design final u.

Step-by-step (2nd order example):
  z1 = x1
  V1 = 0.5*z1^2
  alpha1 = -z1  (stabilizes x1 subsystem)

  z2 = x2 - alpha1 = x2 + z1
  V = V1 + 0.5*z2^2
  V_dot = z1*(x2+phi1) + z2*(u+phi2 - dalpha1/dx1*x2)
  u = -z1 - phi1 - phi2 + (dalpha1/dx1)*x2 - z2

Advantage: Handles uncertainties by canceling phi(x)
""")

# ===== Feedback Linearization =====
# Exact linearization: find u = alpha(x) + beta(x)*v
# such that the closed loop is linear
#
# For x_dot = f(x) + g(x)*u
# Lie derivative: Lf h = (dh/dx)*f
# Input-output linearization: differentiate until u appears

print("""
========================================
Feedback Linearization
========================================

Idea: Cancel nonlinearities with control law
  u = (1/L_g L_f^(r-1) h) * (-L_f^r h + v)
  => results in linear controlled system: y^(r) = v

Relative Degree r: number of times we must differentiate
  output to see input u in the equation.

Example: x_dot = sin(x) + u
  y = x
  L_f h = dh/dx * f = 1 * sin(x) = sin(x)
  ...but u doesn't appear yet (r=1)

  u = -sin(x) + v  => x_dot = v
  Now linear: x_dot = v

Two types:
  1. Input-Output Linearization: makes y = linear
  2. Input-State Linearization: makes full x = linear
""")

# ===== Example: Pendulum Feedback Linearization =====
# x1 = theta, x2 = omega
# x1_dot = x2
# x2_dot = -g/l*sin(x1) - c*x2 + u/J
# y = x1
#
# Differentiate y: y_dot = x2
# Differentiate again: y_ddot = -g/l*sin(x1) - c*x2 + u/J
# u appears! So relative degree r=2 (full order)
#
# u = J*(v + g/l*sin(x1) + c*x2)
# => y_ddot = v
# => Linear! Now apply LQR to v

g_l = 1.0
c = 0.5
J = 1.0

# Linearized model around x=0
A = np.array([[0, 1], [-g_l, -c/J]])
B = np.array([[0], [1/J]])
Q = np.diag([10.0, 1.0])
R = np.array([[0.1]])
P = linalg.solve_continuous_are(A, B, Q, R)
K = (linalg.inv(R) @ B.T @ P).flatten()

def f_nonlin(x):
    return np.array([x[1], -g_l*np.sin(x[0]) - c/J*x[1]])

T = 8.0
dt = 0.005
N = int(T/dt)
t = np.linspace(0, T, N)

# FB linearization + LQR
x_fb = np.zeros((N, 2))
x_fb[0] = [np.pi - 0.1, 0.0]

x_lin = np.zeros((N, 2))
x_lin[0] = [np.pi - 0.1, 0.0]

# PD control (baseline)
Kp, Kd = 10.0, 5.0

for i in range(N-1):
    # Feedback linearization + LQR
    u_fb = J * (np.dot(K, [-x_fb[i, 0], -x_fb[i, 1]]) + g_l*np.sin(x_fb[i, 0]) + c/J*x_fb[i, 1])
    x_fb[i+1, 1] = x_fb[i, 1] + (-g_l*np.sin(x_fb[i, 0]) - c/J*x_fb[i, 1] + u_fb/J) * dt
    x_fb[i+1, 0] = x_fb[i, 0] + x_fb[i, 1] * dt

    # Simple PD control (for comparison)
    u_pd = -Kp * x_lin[i, 0] - Kd * x_lin[i, 1]
    x_lin[i+1, 1] = x_lin[i, 1] + (-g_l*np.sin(x_lin[i, 0]) - c/J*x_lin[i, 1] + u_pd/J) * dt
    x_lin[i+1, 0] = x_lin[i, 0] + x_lin[i, 1] * dt

# ===== Plot =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 19: Backstepping + Feedback Linearization', fontsize=14)

ax = axes[0, 0]
ax.plot(t, x_fb[:, 0], 'b-', lw=2, label='FB Linearization + LQR')
ax.plot(t, x_lin[:, 0], 'orange', lw=2, label='PD only')
ax.axhline(y=0, color='red', ls='--', alpha=0.7, label='Target')
ax.set_xlabel('t (s)')
ax.set_ylabel('theta (rad)')
ax.set_title('Pendulum: FB Linearization vs PD')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(t, x_fb[:, 1], 'b-', lw=2, label='FB Linearization omega')
ax.plot(t, x_lin[:, 1], 'orange', lw=2, label='PD omega')
ax.set_xlabel('t (s)')
ax.set_ylabel('omega (rad/s)')
ax.set_title('Angular Velocity')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(x_fb[:, 0], x_fb[:, 1], 'b-', lw=1.5, label='FB Linear')
ax.plot(x_lin[:, 0], x_lin[:, 1], 'orange', lw=1.5, label='PD')
ax.scatter([0], [0], color='red', s=100, zorder=5, label='Origin')
ax.set_xlabel('theta')
ax.set_ylabel('omega')
ax.set_title('Phase Portrait')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
txt = ("""Backstepping:\n\n"""
       """Strict-feedback form:\n"""
       """  x1_dot = x2 + phi1(x1)\n"""
       """  x2_dot = u + phi2(x1,x2)\n\n"""
       """Virtual control alpha1 = -z1\n"""
       """Error: z2 = x2 - alpha1\n"""
       """u = -z1 - phi1 - phi2 + ...\n\n"""
       """Feedback Linearization:\n\n"""
       """u = (1/LgLfr-1h)(-Lfrh + v)\n\n"""
       """For pendulum:\n"""
       """  u = J*(v + g/l*sin(x1) + c*x2)\n"""
       """  => y_ddot = v (linear)\n\n"""
       """Then apply linear control (LQR)\n\n"""
       """Key insight:\n"""
       """  FB Linearization: exact cancellation\n"""
       """  Backstepping: partial cancellation\n"""
       """  Both require accurate model""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=11,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day19_backstep.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")
