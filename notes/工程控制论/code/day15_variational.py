import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import linalg

print("=" * 60)
print("Day 15: Variational + Pontryagin Minimum Principle")
print("=" * 60)

# ===== Bang-Bang vs Smooth Optimal Control =====
# Problem: x_dot = u, |u| <= 1, x(0)=0, x(tf)=1, minimize tf
# Bang-Bang: accelerate at +1 for tf/2, then -1 for tf/2
# tf_min = 2*(xf-x0)/umax = 2.0s

u_max = 1.0
x0, xf = 0.0, 1.0
tf = 2.0 * (xf - x0) / u_max
dt = 0.001
N = int(tf / dt) + 10
t = np.linspace(0, tf, N)

# Bang-bang trajectory
def sim_bangbang(x0, tf, N, u_max=1.0):
    t = np.linspace(0, tf, N)
    x = np.zeros(N)
    v = np.zeros(N)
    u = np.zeros(N)
    x[0] = x0
    for i in range(N-1):
        u[i] = u_max if i < N//2 else -u_max
        if i < N-1:
            v[i+1] = v[i] + u[i] * dt
            x[i+1] = x[i] + v[i] * dt
    return t, x, v, u

t_bb, x_bb, v_bb, u_bb = sim_bangbang(x0, tf, N)

# LQR smooth control for comparison
A = np.array([[0.0, 1.0], [0.0, 0.0]])
B = np.array([[0.0], [1.0]])
Q = np.diag([100.0, 1.0])
R = np.array([[0.1]])
P_lqr = linalg.solve_continuous_are(A, B, Q, R)
K_lqr = (linalg.inv(R) @ B.T @ P_lqr).flatten()

x_sm = np.zeros(N)
v_sm = np.zeros(N)
u_sm = np.zeros(N)
x_sm[0] = x0
v_sm[0] = 0.0

for i in range(N-1):
    u_raw = -np.dot(K_lqr, [x_sm[i], v_sm[i]])
    u_sm[i] = max(-u_max, min(u_max, u_raw))
    v_sm[i+1] = v_sm[i] + u_sm[i] * dt
    x_sm[i+1] = x_sm[i] + v_sm[i] * dt

# Find convergence times
def find_time(x, t, target=0.999):
    idx = np.where(x >= target)[0]
    return t[idx[0]] if len(idx) > 0 else None

t_bb_end = find_time(x_bb, t)
t_sm_end = find_time(x_sm, t)

print(f"\nOptimal time (Bang-Bang): {tf:.3f}s")
print(f"Bang-Bang reaches x=1 at: {t_bb_end:.3f}s")
if t_sm_end:
    print(f"Smooth (clamped LQR) reaches x=1 at: {t_sm_end:.3f}s")
    print(f"Bang-Bang is {(t_sm_end/t_bb_end-1)*100:.0f}% faster")
else:
    print("Smooth (clamped LQR): did not reach x=1 in time range")

# ===== Plot =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 15: Variational Methods + Pontryagin Minimum Principle', fontsize=14)

ax = axes[0, 0]
mask_bb = x_bb <= 1.05
mask_sm = x_sm <= 1.05
ax.plot(t_bb[mask_bb], x_bb[mask_bb], 'b-', lw=2, label='Bang-Bang x')
ax.plot(t_bb[mask_sm], x_sm[mask_sm], 'orange', lw=2, label='Smooth x')
ax.axhline(y=1, color='red', ls='--', alpha=0.7, label='Target')
ax.axvline(x=t_bb_end, color='blue', ls=':', alpha=0.5, label=f't={t_bb_end:.2f}s')
ax.set_xlabel('t (s)')
ax.set_ylabel('x')
ax.set_title('Position: Bang-Bang vs Smooth')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(t_bb[mask_bb], v_bb[mask_bb], 'b-', lw=2, label='Bang-Bang v')
ax.plot(t_bb[mask_sm], v_sm[mask_sm], 'orange', lw=2, label='Smooth v')
ax.set_xlabel('t (s)')
ax.set_ylabel('v')
ax.set_title('Velocity')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(t_bb[mask_bb], u_bb[mask_bb], 'b-', lw=2, label='Bang-Bang u')
ax.plot(t_bb[mask_sm], u_sm[mask_sm], 'orange', lw=2, label='Smooth u')
ax.axhline(y=1, color='gray', ls='--', alpha=0.5)
ax.axhline(y=-1, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('t (s)')
ax.set_ylabel('u')
ax.set_title('Control: Bang-Bang vs Smooth')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
txt = ("Key:\n\n"
       "Euler-Lagrange: d/dt(∂L/∂xdot) = ∂L/∂x\n\n"
       "Pontryagin Minimum Principle:\n"
       "  H = L + λ·f(x,u)\n"
       "  xdot = ∂H/∂λ\n"
       "  λdot = -∂H/∂x\n"
       "  u* = argmin H\n\n"
       "Bang-Bang: H = 1 + λu\n"
       "  u* = -sign(λ) = ±1\n"
       "  -> Time-optimal but high energy\n\n"
       "Smooth (LQR): J = int(x'Qx + u'Ru)dt\n"
       "  u* = -R^-1 B' P x\n"
       "  -> Trades time vs control effort")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=11,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day15_variational.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")

print("""
============================================================
KEY FORMULAS - Variational + Pontryagin
============================================================

Functional: J[u] = integral L(x, u, t) dt

Euler-Lagrange Equation:
  d/dt(∂L/∂x_dot) = ∂L/∂x

Hamiltonian: H = L + λ^T f(x, u, t)

Pontryagin Necessary Conditions:
  1. x_dot = ∂H/∂λ
  2. λ_dot = -∂H/∂x  (costate)
  3. 0 = ∂H/∂u       (stationarity)
  4. λ(t_f) = ∂φ/∂x(t_f)  (transversality)
  5. H(x*, u*, λ*, t) <= H(x*, u, λ*, t)  (minimum)

For linear-quadratic:
  H = x'Qx + u'Ru + λ'(Ax + Bu)
  u* = -1/2 * R^-1 * B' * λ  (if unconstrained)
  u* = -sign(λ)  (bang-bang, if |u|<=umax)
""")
