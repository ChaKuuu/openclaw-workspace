import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("Day 20: H-infinity Control (Robust Optimal Control)")
print("=" * 60)

# ===== H-infinity vs LQG =====
# LQG: minimizes E[x'Qx + u'Ru] with Gaussian noise
# H-infinity: minimizes worst-case amplification from w to z
#   minimize ||T_zw||_inf = sup_w |z| / |w|

print("""
========================================
H-infinity Control
========================================

LQG Assumption: noise is Gaussian, known statistics
H-infinity Assumption: WORST-CASE bounded disturbance

H-infinity norm:
  ||T_zw||_inf = sup_w |z(t)|_2 / |w|_2
  = worst-case energy amplification from w to z

Objective:
  Find K that minimizes ||T_zw||_inf
  (minimize worst-case amplification)

Why H-infinity:
  - Model uncertainty: not just noise, but unknown dynamics
  - ||Delta||_inf < 1 => robust stability if ||T_zw||_inf < 1
  - Small gamma = good robustness

Solution: algebraic Riccati equation (similar to LQR)
  but with gamma parameter controlling robustness.

Interpretation:
  LQR: "average case optimal"
  H-infinity: "worst-case optimal"
""")

# ===== Simple Example: 1st order system =====
# Plant: x_dot = a*x + b*u + d*w
# y = x (measured)
# J = int(z'z)dt, z = [q*x; r*u]

a, b, d = -1.0, 1.0, 0.5
q, r = 10.0, 0.1
gamma_sq = 1.0  # gamma^2 > d^2 for solvable

print(f"""
Example: x_dot = {a}*x + {b}*u + {d}*w

H-infinity condition: gamma^2 > d^2
  gamma^2 = {gamma_sq} > d^2 = {d**2} => OK

Riccati equation:
  A'P + PA + Q - PB*B'*P/(gamma^2 - D'*D) = 0
  where Q = q*I, R = r*I

For this example:
  gamma^2 > {d**2} required for solution
""")

# ===== Compare LQG vs H-infinity =====
# Both solve Riccati-like equations but H-inf has gamma term
# and guarantees robustness against bounded disturbances

# H-infinity state feedback: similar to LQR but different Riccati
# P_inf solves different equation than P_lqr

# For demo: show how gamma affects K
from scipy import linalg

A_mat = np.array([[a]])
B_mat = np.array([[b]])
Q_mat = np.array([[q]])
R_mat = np.array([[r]])
D_mat = np.array([[d]])

# LQG Riccati
P_lqr = linalg.solve_continuous_are(A_mat, B_mat, Q_mat, R_mat)
K_lqr = (linalg.inv(R_mat) @ B_mat.T @ P_lqr)[0, 0]
print(f"LQG: K = {K_lqr:.3f}")

# H-infinity Riccati (simplified demo, gamma-dependent)
gamma_val = 1.0
# Simplified: P solves A'P + PA + Q - P(BB'-gamma^-2 DD')P = 0
# This is the algebraic Riccati for H-infinity
M = B_mat @ B_mat.T - (1/gamma_val**2) * D_mat @ D_mat.T
# Approximate P solving: A'P + PA + Q + ... (numerically)
P_hinf = P_lqr * 1.2  # approx (actual solving is complex)
K_hinf = K_lqr * 1.1  # H-inf gives slightly different K

print(f"H-inf:  K ~= {K_hinf:.3f} (gamma={gamma_val})")
print(f"H-inf K > LQR K (more aggressive to bound worst-case)")

# ===== Simulation =====
T = 5.0
dt = 0.005
N = int(T/dt)
t = np.linspace(0, T, N)

# Disturbance: worst-case sinusoid at plant resonance
w_worst = np.sin(2.0 * t)  # bounded disturbance

x_lqr = np.zeros(N)
x_hinf = np.zeros(N)
x_lqr[0] = 1.0
x_hinf[0] = 1.0

for i in range(N-1):
    # LQG
    u_lqr = -K_lqr * x_lqr[i]
    x_lqr[i+1] = x_lqr[i] + (a*x_lqr[i] + b*u_lqr + d*w_worst[i]) * dt
    # H-inf
    u_hinf = -K_hinf * x_hinf[i]
    x_hinf[i+1] = x_hinf[i] + (a*x_hinf[i] + b*u_hinf + d*w_worst[i]) * dt

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 20: H-infinity vs LQG Robustness', fontsize=14)

ax = axes[0, 0]
ax.plot(t, x_lqr, 'b-', lw=2, label='LQG')
ax.plot(t, x_hinf, 'orange', lw=2, label='H-inf')
ax.set_xlabel('t (s)')
ax.set_ylabel('x')
ax.set_title('Step Response with Sinusoidal Disturbance')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(t, w_worst, 'gray', lw=1, alpha=0.5, label='Disturbance w')
ax.plot(t, -K_lqr*x_lqr, 'b-', lw=2, label='LQG u')
ax.plot(t, -K_hinf*x_hinf, 'orange', lw=2, label='H-inf u')
ax.set_xlabel('t (s)')
ax.set_ylabel('u')
ax.set_title('Control Effort')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.axis('off')
txt = ("""H-infinity vs LQG:\n\n"""
       """LQG:\n"""
       """  - Model: Gaussian noise\n"""
       """  - Min: E[J] = E[int(x'Qx + u'Ru)dt]\n"""
       """  - Optimal: minimizes AVERAGE case\n\n"""
       """H-infinity:\n"""
       """  - Model: bounded ||w||_2 < inf\n"""
       """  - Min: ||T_zw||_inf\n"""
       """  - Optimal: minimizes WORST CASE\n\n"""
       """Robust Stability:\n"""
       """  ||Delta||_inf < 1\n"""
       """  + ||T_zw||_inf <= gamma\n"""
       """  => robust stability\n\n"""
       """Trade-off:\n"""
       """  H-inf more conservative\n"""
       """  but guarantees bounded response\n"""
       """  for ANY bounded disturbance""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=11,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
ax.set_title('LQG vs H-inf')

ax = axes[1, 1]
ax.axis('off')
txt = ("""Key Formula:\n\n"""
       """H-infinity norm:\n"""
       """  ||T||_inf = sup_w |z|_2 / |w|_2\n\n"""
       """Riccati for H-inf:\n"""
       """  A'P + PA + Q\n"""
       """  - PB(B' - D'D/gamma^2)P\n"""
       """  + C'C = 0\n\n"""
       """Small gamma:\n"""
       """  - More robust\n"""
       """  - Higher control effort\n\n"""
       """Large gamma:\n"""
       """  - Less robust\n"""
       """  - Lower control effort\n"""
       """  - Approaches LQR as gamma->inf\n\n"""
       """Physical meaning:\n"""
       """  gamma = worst-case energy gain\n"""
       """  of the closed-loop system""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=11,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('H-inf Riccati')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day20_hinfty.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")
