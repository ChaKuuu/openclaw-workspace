import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("Day 17: Lyapunov Direct Method + Nonlinear Stability")
print("=" * 60)

# ===== Lyapunov Indirect vs Direct =====
# Indirect: linearize, check eigenvalues (Day 13)
# Direct: find V(x), check V_dot(x)

print("""
========================================
Lyapunov Direct Method
========================================

Key Idea: Find a "energy-like" function V(x) that:
  1. V(x) > 0 for x != 0 (positive definite)
  2. V(0) = 0
  3. V_dot(x) = dV/dt <= 0 (negative semi-definite)
  => x=0 is stable

If V_dot(x) < 0 for x != 0:
  => x=0 is asymptotically stable

Physical analogy:
  V(x) = kinetic + potential energy
  V_dot = power = force * velocity
  If power <= 0 always, energy never increases
  => system settles to minimum energy state (x=0)
""")

# ===== Example 1: Simple Harmonic Oscillator =====
# x_dot = [-omega^2 * x; x]
# V = 0.5*omega^2*x^2 + 0.5*y^2 = energy
# V_dot = omega^2*x*y + y*(-omega^2*x) = 0 (conservative)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Day 17: Lyapunov Direct Method', fontsize=14)

# System 1: Damped oscillator
# x_dot = y, y_dot = -x - c*y
# V = 0.5*x^2 + 0.5*y^2  (energy)
# V_dot = x*y + y*(-x-c*y) = -c*y^2 <= 0
c = 0.5
omega = 1.0

def osc_f(x, c=0.5):
    return np.array([x[1], -omega*x[0] - c*x[1]])

def sim(x0, T=20, dt=0.01):
    N = int(T/dt)
    t = np.linspace(0, T, N)
    x = np.zeros((N, 2))
    x[0] = x0
    for i in range(N-1):
        k1 = osc_f(x[i], c)
        k2 = osc_f(x[i] + k1*dt/2, c)
        k3 = osc_f(x[i] + k2*dt/2, c)
        k4 = osc_f(x[i] + k3*dt, c)
        x[i+1] = x[i] + (k1 + 2*k2 + 2*k3 + k4)/6 * dt
    return t, x

t, x = sim([1.0, 0.0])

# Energy
V = 0.5 * x[:, 0]**2 + 0.5 * x[:, 1]**2
V_dot = x[:, 0] * x[:, 1] + x[:, 1] * (-omega*x[:, 0] - c*x[:, 1])

ax = axes[0, 0]
ax.plot(t, V, 'b-', lw=2, label='V(t) = energy')
ax.plot(t, V_dot, 'orange', lw=1.5, label='V_dot(t)')
ax.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('t (s)')
ax.set_ylabel('V / V_dot')
ax.set_title('Damped Oscillator: V decreases (Lyapunov)')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(x[:, 0], x[:, 1], 'b-', lw=1.5)
ax.scatter([0], [0], color='red', s=100, zorder=5)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Phase Portrait: Spiral to Origin')
ax.grid(True, alpha=0.3)

# ===== Example 2: Unstable system =====
# x_dot = x (unstable node)
# V = x^2, V_dot = 2x*x = 2x^2 > 0 (positive definite)
# => x=0 is unstable (V increasing)

def unstable_f(x):
    return np.array([x[0], 0.0])

t_u, x_u = sim([1.0, 0.0])
x_u[0] = 0.5
for i in range(len(t_u)-1):
    x_u[i+1] = x_u[i] + unstable_f(x_u[i]) * (t_u[i+1]-t_u[i])

ax = axes[0, 2]
ax.plot(t_u, x_u[:, 0], 'r-', lw=2, label='x(t) -> infinity')
ax.set_xlabel('t (s)')
ax.set_ylabel('x')
ax.set_title('Unstable Node: x_dot = x, V_dot > 0')
ax.legend()
ax.grid(True, alpha=0.3)

# ===== Example 3: van der Pol (limit cycle) =====
# x_dot = y
# y_dot = mu*(1-x^2)*y - x
# Conservative at mu=0, self-oscillating for mu>0
mu = 1.0

def vdp_f(x):
    return np.array([x[1], mu*(1-x[0]**2)*x[1] - x[0]])

t_vdp = np.linspace(0, 30, 3000)
dt_vdp = t_vdp[1] - t_vdp[0]
x_vdp = np.zeros((len(t_vdp), 2))
x_vdp[0] = [0.1, 0.1]

for i in range(len(t_vdp)-1):
    k1 = vdp_f(x_vdp[i])
    k2 = vdp_f(x_vdp[i] + k1*dt_vdp/2)
    k3 = vdp_f(x_vdp[i] + k2*dt_vdp/2)
    k4 = vdp_f(x_vdp[i] + k3*dt_vdp)
    x_vdp[i+1] = x_vdp[i] + (k1 + 2*k2 + 2*k3 + k4)/6 * dt_vdp

ax = axes[1, 0]
ax.plot(x_vdp[:, 0], x_vdp[:, 1], 'b-', lw=1)
for ic in [[2.0, 0], [0.5, -2.0], [3.0, 0]]:
    x0 = ic
    x_t = np.zeros((len(t_vdp), 2))
    x_t[0] = x0
    for i in range(len(t_vdp)-1):
        k1 = vdp_f(x_t[i])
        k2 = vdp_f(x_t[i] + k1*dt_vdp/2)
        k3 = vdp_f(x_t[i] + k2*dt_vdp/2)
        k4 = vdp_f(x_t[i] + k3*dt_vdp)
        x_t[i+1] = x_t[i] + (k1 + 2*k2 + 2*k3 + k4)/6 * dt_vdp
    ax.plot(x_t[:, 0], x_t[:, 1], 'orange', lw=1, alpha=0.7)
ax.scatter([0], [0], color='red', s=50)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('van der Pol: Limit Cycle (self-oscillation)')
ax.grid(True, alpha=0.3)

# ===== Example 4: Pendulum with friction =====
# x1 = theta, x2 = omega
# x1_dot = x2
# x2_dot = -sin(x1) - c*x2
# V = -cos(x1) + 1 + 0.5*x2^2  (potential + kinetic)

c_fric = 0.5

def pend_f(x):
    return np.array([x[1], -np.sin(x[1]) - c_fric * x[0]])

t_p = np.linspace(0, 20, 2000)
dt_p = t_p[1] - t_p[0]
x_p = np.zeros((len(t_p), 2))
x_p[0] = [np.pi - 0.1, 0.5]

for i in range(len(t_p)-1):
    k1 = pend_f(x_p[i])
    k2 = pend_f(x_p[i] + k1*dt_p/2)
    k3 = pend_f(x_p[i] + k2*dt_p/2)
    k4 = pend_f(x_p[i] + k3*dt_p)
    x_p[i+1] = x_p[i] + (k1 + 2*k2 + 2*k3 + k4)/6 * dt_p

V_pend = -np.cos(x_p[:, 0]) + 1 + 0.5*x_p[:, 0]**2

ax = axes[1, 1]
ax.plot(t_p, x_p[:, 0], 'b-', lw=2, label='theta')
ax.plot(t_p, x_p[:, 1], 'orange', lw=2, label='omega')
ax.set_xlabel('t (s)')
ax.set_ylabel('theta / omega')
ax.set_title('Pendulum with Friction: settles to bottom')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 2]
ax.axis('off')
txt = ("""Lyapunov Direct Method:

Step 1: Guess a V(x) >= 0
  - Usually: quadratic form V = x'Px
  - Or: energy-like function

Step 2: Compute V_dot = (dV/dx)*f(x)
  - dV/dt along system trajectories

Step 3: Check sign of V_dot
  - V_dot < 0 everywhere => asymptotically stable
  - V_dot <= 0 (not identically 0) => stable
  - V_dot > 0 near origin => unstable

Key Theorems:

1. Lyapunov Stability Theorem:
   V > 0, V_dot <= 0 => stable

2. LaSalle's Invariance Principle:
   V > 0, V_dot <= 0
   + no trajectories stay in
     {x: V_dot = 0} except x=0
   => asymptotically stable

3. Converse Theorems:
   If system is stable => there exists
   a Lyapunov function (but finding it is hard)

4. Instability Theorem:
   V > 0 near origin but V_dot > 0
   => origin is unstable
""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=10,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Lyapunov Theorems')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day17_lyapunov.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")
