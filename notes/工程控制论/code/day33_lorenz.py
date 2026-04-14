import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 33: Lorenz System and Strange Attractors")

fig = plt.figure(figsize=(16, 10))
fig.suptitle('Day 33: Lorenz Strange Attractor', fontsize=14)

# ===== Lorenz Equations =====
# x_dot = sigma*(y - x)
# y_dot = x*(rho - z) - y
# z_dot = x*y - beta*z
sigma = 10.0
beta = 8.0 / 3.0
rho_vals = [10.0, 28.0, 35.0]  # below, at, above critical

def lorenz(x, rho):
    return np.array([sigma*(x[1]-x[0]), x[0]*(rho - x[2]) - x[1], x[0]*x[1] - beta*x[2]])

T = 30.0
dt = 0.01
N = int(T/dt)
t = np.linspace(0, T, N)

for idx, rho in enumerate(rho_vals):
    ax = fig.add_subplot(2, 3, idx+1, projection='3d')
    x0 = [1.0, 1.0, 1.0]
    x_lor = np.zeros((N, 3))
    x_lor[0] = x0
    for i in range(N-1):
        k1 = lorenz(x_lor[i], rho)
        k2 = lorenz(x_lor[i] + k1*dt/2, rho)
        k3 = lorenz(x_lor[i] + k2*dt/2, rho)
        k4 = lorenz(x_lor[i] + k3*dt, rho)
        x_lor[i+1] = x_lor[i] + (k1 + 2*k2 + 2*k3 + k4)/6 * dt

    ax.plot(x_lor[:, 0], x_lor[:, 1], x_lor[:, 2], lw=0.5, alpha=0.7)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Lorenz: rho={rho}')

# ===== Sensitivity to Initial Conditions =====
ax4 = fig.add_subplot(2, 3, 4, projection='3d')
rho = 28.0
x1 = np.zeros((N, 3))
x2 = np.zeros((N, 3))
x1[0] = [1.0, 1.0, 1.0]
x2[0] = [1.001, 1.0, 1.0]  # very small difference

for i in range(N-1):
    for x_cur, x0_use in [(x1[i], x1[i]), (x2[i], x2[i])]:
        k1 = lorenz(x_cur, rho)
        k2 = lorenz(x_cur + k1*dt/2, rho)
        k3 = lorenz(x_cur + k2*dt/2, rho)
        k4 = lorenz(x_cur + k3*dt, rho)
        x_new = x_cur + (k1 + 2*k2 + 2*k3 + k4)/6 * dt
        if x_cur is x1[i]:
            x1[i+1] = x_new
        else:
            x2[i+1] = x_new

d = np.linalg.norm(x1 - x2, axis=1)
ax4.plot(x1[:, 0], x1[:, 1], x1[:, 2], 'b-', lw=0.5, alpha=0.5, label='IC 1')
ax4.plot(x2[:, 0], x2[:, 1], x2[:, 2], 'orange', lw=0.5, alpha=0.5, label='IC 2 (delta=0.001)')
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('Z')
ax4.set_title('Sensitivity: Divergence of Nearby Trajectories')
ax4.legend()

# ===== Divergence =====
ax5 = fig.add_subplot(2, 3, 5)
mask = d > 0.01
ax5.semilogy(t[mask], d[mask], 'b-', lw=1.5)
ax5.set_xlabel('t')
ax5.set_ylabel('||x1 - x2||')
ax5.set_title('Exponential Divergence (Lyapunov > 0)')
ax5.grid(True, alpha=0.3)

# ===== Summary =====
ax6 = fig.add_subplot(2, 3, 6)
ax6.axis('off')
ax6.text(0.05, 0.95,
    "Lorenz System (1963):\n\n"
    "Equations:\n"
    "  x_dot = sigma*(y - x)\n"
    "  y_dot = x*(rho - z) - y\n"
    "  z_dot = x*y - beta*z\n\n"
    "Parameters:\n"
    "  sigma = 10, beta = 8/3\n"
    "  rho_critical ~ 24.74\n\n"
    "Behavior:\n"
    "  rho < 1: stable origin\n"
    "  1 < rho < 24.74: two stable foci\n"
    "  rho > 24.74: chaos!\n\n"
    "Strange Attractor:\n"
    "  - Fractal dimension (non-integer)\n"
    "  - Infinite instability (LE > 0)\n"
    "  - Yet bounded trajectory\n"
    "  - Deterministic chaos\n\n"
    "Butterfly Effect:\n"
    "  Sensitivity to initial conditions\n"
    "  -> impossible long-term prediction\n"
    "  -> but short-term is predictable\n\n"
    "Control Connection:\n"
    "  - Chaos = both enemy and opportunity\n"
    "  - OGY exploits sensitivity (small control)\n"
    "  - Targeting: aim for desired UPO",
    transform=ax6.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax6.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day33_lorenz.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
