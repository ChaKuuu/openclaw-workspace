import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 31: Hopf Bifurcation")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 31: Hopf Bifurcation', fontsize=14)

# ===== Hopf: Complex Eigenvalues Cross Imag Axis =====
# Normal form: r_dot = mu*r - r^3
# theta_dot = omega + beta*r^2

mu_vals = np.linspace(-0.5, 0.5, 100)
r_eq = np.sqrt(np.maximum(mu_vals, 0))

ax = axes[0, 0]
ax.plot(mu_vals, r_eq, 'b-', lw=2, label='Stable limit cycle (r>0)')
ax.plot(mu_vals, np.zeros_like(mu_vals), 'r--', lw=1.5, label='Unstable equilibrium')
ax.axvline(x=0, color='green', ls=':', lw=2, label='Hopf at mu=0')
ax.set_xlabel('mu')
ax.set_ylabel('r_eq')
ax.set_title('Hopf: Supercritical - Stable Limit Cycle from mu>0')
ax.legend()
ax.grid(True, alpha=0.3)

# ===== Hopf Animation (static simulation) =====
# Hopf normal form: z_dot = (mu + i)*z - |z|^2*z
# In polar: r_dot = mu*r - r^3, theta_dot = 1

mu = 0.2  # supercritical
T = 10.0
dt = 0.01
N = int(T/dt)
t = np.linspace(0, T, N)
r = np.zeros(N)
theta = np.zeros(N)
r[0] = 0.1
theta[0] = 0.0

for i in range(N-1):
    r[i+1] = r[i] + (mu*r[i] - r[i]**3) * dt
    theta[i+1] = theta[i] + 1.0 * dt

x = r * np.cos(theta)
y = r * np.sin(theta)

ax = axes[0, 1]
ax.plot(x, y, 'b-', lw=1.5)
ax.set_xlabel('Re(z)')
ax.set_ylabel('Im(z)')
ax.set_title(f'Hopf Normal Form: Limit Cycle (mu={mu})')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)

# ===== Supercritical vs Subcritical =====
mu_sub = -0.2  # subcritical
r_sub = np.zeros(N)
r_sub[0] = 0.3  # start close to origin

for i in range(N-1):
    r_sub[i+1] = r_sub[i] + (mu_sub*r_sub[i] + r_sub[i]**3) * dt
    if r_sub[i+1] > 10:
        r_sub[i+1:] = 10.0
        break

ax = axes[1, 0]
ax.plot(t[:500], r[:500], 'b-', lw=2, label='Subcritical: r grows')
ax.plot(t[:500], -r[:500], 'b-', lw=2)
ax.axhline(y=0, color='red', ls='--', lw=1.5)
ax.set_xlabel('t')
ax.set_ylabel('r')
ax.set_title('Subcritical Hopf: Unstable Limit Cycle Collapses')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Hopf Bifurcation:\n\n"
    "When:\n"
    "  - A pair of complex eigenvalues\n"
    "    cross the imaginary axis\n"
    "  - Re(lambda) changes sign\n\n"
    "Normal Form (polar):\n"
    "  r_dot = mu*r - r^3  (supercritical)\n"
    "  theta_dot = omega + beta*r^2\n\n"
    "Types:\n"
    "  Supercritical (mu > 0):\n"
    "    - Stable equilibrium -> stable LC\n"
    "    - Birth of stable limit cycle\n"
    "    - Soft transition\n\n"
    "  Subcritical (mu < 0):\n"
    "    - Unstable LC shrinks -> jumps\n"
    "    - Catastrophic (hysteresis)\n"
    "    - Hard transition\n\n"
    "Examples:\n"
    "  - Flutter (airplane wing)\n"
    "  - Glycolytic oscillation\n"
    "  - Predator-prey cycles\n"
    "  - Neural oscillations\n\n"
    "Detection:\n"
    "  - Trace = 0 at bifurcation\n"
    "  - Det(A) > 0, Trace crosses 0",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day31_hopf.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
