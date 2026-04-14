import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("Day 13: Nonlinear Systems - Phase Plane & Stability")
print("=" * 60)

# ===== Why Nonlinear Matters =====
print("""
Linear:  F = ma, superposition holds
Nonlinear: F = ma + m*theta*omega^2  (centrifugal term in pendulum)

Key Differences:
  Linear:    Solutions are EXACT, superposition works
  Nonlinear: Most have NO closed-form solution

Common Nonlinearities:
  - Saturation (actuator limits)
  - Deadzone (play in mechanical systems)
  - Friction (stiction, Coulomb)
  - Relay (on/off control)
  - Quadratic drag: F = -c*v*|v|
""")

# ===== Phase Plane: Linear vs Nonlinear =====
# Linear: x_dot = A*x
# Nonlinear: x_dot = f(x)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Day 13: Linear vs Nonlinear Phase Planes', fontsize=14)

# --- Linear harmonic oscillator ---
A = np.array([[0, 1], [-1, 0]])  # x_dot = -y, y_dot = x

def simulate_linear(A, x0, T=10, dt=0.01):
    N = int(T/dt)
    t = np.linspace(0, T, N)
    x = np.zeros((N, 2))
    x[0] = x0
    for i in range(N-1):
        x[i+1] = x[i] + A @ x[i] * dt
    return t, x

# Linear trajectories from different initial conditions
colors = ['blue', 'green', 'red', 'orange', 'purple']
for idx, x0 in enumerate([[1,0], [0.5, 0.5], [0, 1], [-1, 0.5], [0.7, -0.3]]):
    t, x = simulate_linear(A, x0)
    axes[0, 0].plot(x[:, 0], x[:, 1], color=colors[idx], lw=1.5, alpha=0.7)
axes[0, 0].scatter([0], [0], color='black', s=50, zorder=5)
axes[0, 0].set_xlabel('x1')
axes[0, 0].set_ylabel('x2')
axes[0, 0].set_title('Linear: Centers (neutrally stable)')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_aspect('equal')
axes[0, 0].axhline(y=0, color='gray', lw=0.5)
axes[0, 0].axvline(x=0, color='gray', lw=0.5)

# --- Nonlinear pendulum ---
def pendulum_f(x):
    x1, x2 = x
    return np.array([x2, -np.sin(x1) - 0.5*x2])

def simulate_nonlinear(f, x0, T=15, dt=0.01):
    N = int(T/dt)
    t = np.linspace(0, T, N)
    x = np.zeros((N, 2))
    x[0] = x0
    for i in range(N-1):
        k1 = f(x[i])
        k2 = f(x[i] + k1*dt/2)
        k3 = f(x[i] + k2*dt/2)
        k4 = f(x[i] + k3*dt)
        x[i+1] = x[i] + (k1 + 2*k2 + 2*k3 + k4)/6 * dt
    return t, x

for idx, x0 in enumerate([[0.5, 0], [1.0, 0], [1.5, 0], [2.5, 0], [3.0, 0]]):
    t, x = simulate_nonlinear(pendulum_f, x0)
    # Plot only stable region
    mask = np.abs(x[:, 0]) < 4
    axes[0, 1].plot(x[mask, 0], x[mask, 1], color=colors[idx], lw=1.5, alpha=0.7)

axes[0, 1].scatter([0], [0], color='black', s=50, zorder=5, label='Equilibrium')
axes[0, 1].scatter([np.pi, -np.pi], [0, 0], color='red', s=50, zorder=5, label='Unstable eq')
axes[0, 1].set_xlabel('theta (x1)')
axes[0, 1].set_ylabel('omega (x2)')
axes[0, 1].set_title('Nonlinear: Pendulum Phase Plane')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# --- Phase portrait features ---
# Separatrix
t, x = simulate_nonlinear(pendulum_f, [np.pi - 0.001, 0])
mask = np.abs(x[:, 0]) < 5
axes[0, 2].plot(x[mask, 0], x[mask, 1], 'b-', lw=2, label='Homoclinic orbit (separatrix)')
axes[0, 2].scatter([0], [0], color='black', s=50, zorder=5)
axes[0, 2].scatter([np.pi, -np.pi], [0, 0], color='red', s=50, zorder=5)
axes[0, 2].set_xlabel('theta')
axes[0, 2].set_ylabel('omega')
axes[0, 2].set_title('Separatrix (separates oscillation from rotation)')
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

# --- Lyapunov Stability Definitions ---
ax = axes[1, 0]
ax.axis('off')
txt = ("""Lyapunov Stability Definitions:

1. 渐近稳定 (Asymptotically Stable):
   x_e is stable + x(t) -> x_e as t -> inf
   (linear stable = asymptotically stable)

2. 局部稳定 (Stable):
   For any R, exists r s.t. ||x(0)-x_e||<r
   => ||x(t)-x_e||<R for all t>0

3. 全局稳定 (Globally Asymptotically Stable):
   Stable + x(t)->x_e from ANY initial condition

4. 不稳定 (Unstable):
   Not stable (small perturbation grows)

Key Theorem (Lyapunov Indirect Method):
  If linearized system is asymptotically
  stable => original nonlinear is locally
  asymptotically stable (near equilibrium)
""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=10,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax.set_title('Lyapunov Stability')

# --- Phase plane structures ---
ax = axes[1, 1]
ax.axis('off')
txt = ("""Phase Plane Critical Points:

Type 1: Node (节点)
  - All trajectories approach the point
  - Stable node: both eigenvalues < 0
  - Unstable node: both eigenvalues > 0

Type 2: Spiral (焦点)
  - Trajectories spiral in (or out)
  - Damped oscillation
  - Complex eigenvalues with neg real part

Type 3: Center (中心)
  - Closed orbits around the point
  - Neutrally stable (marginal)
  - Pure imaginary eigenvalues

Type 4: Saddle (鞍点)
  - One stable, one unstable direction
  - Hyperbolic (unstable equilibrium)
  - Separatrices divide phase plane

Type 5: Limit Cycle (极限环)
  - Isolated closed trajectory
  - Self-oscillation (relaxation, PLL)
  - Stable: nearby orbits spiral in
  - Unstable: nearby orbits spiral out
""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=10,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.5))
ax.set_title('Phase Plane Classification')

# --- van der Pol oscillator (limit cycle) ---
ax = axes[1, 2]
mu = 1.0
def vdp_f(x):
    x1, x2 = x
    return np.array([x2, mu*(1 - x1**2)*x2 - x1])

for x0 in [[0.1, 0.1], [2.0, 2.0], [0.5, -2.0], [3.0, 0]]:
    t, x = simulate_nonlinear(vdp_f, x0, T=30, dt=0.01)
    ax.plot(x[:, 0], x[:, 1], lw=1, alpha=0.7)
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_title('van der Pol: Stable Limit Cycle')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day13_nonlinear.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")

# ===== Key Formula: Lyapunov Indirect Method =====
print("\n" + "=" * 60)
print("KEY: Lyapunov Indirect Method")
print("=" * 60)
print("""
Step 1: Find equilibrium x_e (solve f(x_e) = 0)
Step 2: Linearize: A = df/dx | x_e
Step 3: Check eigenvalues of A:
  - All Re(lambda) < 0 => locally asymptotically stable
  - Any Re(lambda) > 0 => unstable
  - Pure imaginary (no other >0) => need higher-order terms

Example: Pendulum at (0,0)
  f(x) = [x2, -sin(x1) - 0.5*x2]
  A = [[0, 1], [-cos(x1), -0.5]] | (0,0)
    = [[0, 1], [-1, -0.5]]
  eigenvalues: solve det(lambda*I - A) = 0
  lambda^2 + 0.5*lambda + 1 = 0
  lambda = [-0.25 +/- sqrt(0.0625 - 1)] = -0.25 +/- i*0.968
  => Re(lambda) < 0 => locally asymptotically stable
  => small-angle pendulum is stable
""")
