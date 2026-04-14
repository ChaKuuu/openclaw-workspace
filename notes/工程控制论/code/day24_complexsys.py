import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 24: Complex Systems Theory")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 24: Complex Systems Theory', fontsize=14)

r_vals = np.linspace(2.5, 4.0, 200)
ax = axes[0, 0]
for r in r_vals:
    x = 0.5
    for _ in range(500):
        x = r * x * (1 - x)
        if _ > 400:
            ax.plot(r, x, 'b,', alpha=0.3)
ax.set_xlabel('r')
ax.set_ylabel('x (steady state)')
ax.set_title('Logistic Map Bifurcation')
ax.grid(True, alpha=0.3)

N = 50
K_vals = [0.0, 1.0, 5.0]
omega = np.random.randn(N) * 0.5
theta = np.random.rand(N) * 2 * np.pi
T = 20.0
dt = 0.01
N_steps = int(T/dt)
ax = axes[0, 1]
K = 2.0
theta_sim = np.zeros((N_steps, N))
theta_sim[0] = theta
for i in range(N_steps-1):
    coupling = (K/N) * np.sum(np.sin(theta_sim[i] - theta_sim[i, :]), axis=0)
    theta_sim[i+1] = theta_sim[i] + (omega + coupling) * dt
    theta_sim[i+1] = np.mod(theta_sim[i+1], 2*np.pi)
r_order = np.abs(np.mean(np.exp(1j * theta_sim), axis=1))
t_arr = np.linspace(0, T, N_steps)
ax.plot(t_arr, r_order, 'b-', lw=1.5)
ax.set_xlabel('t')
ax.set_ylabel('Order parameter r')
ax.set_title('Kuramoto: Synchronization (K=2)')
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.axis('off')
ax.text(0.05, 0.95,
    "Complex Systems Classification:\n\n"
    "Simple: Linear因果, predictable\n\n"
    "Complicated: Many parts, linear因果\n"
    "  Example: car engine\n\n"
    "Complex: Feedback loops, emergence\n"
    "  Cannot predict from parts alone\n"
    "  Example: brain, economy\n\n"
    "Chaotic: Deterministic but unpredictable\n"
    "  Sensitive to initial conditions\n\n"
    "Kuramoto Model:\n"
    "  dtheta_i/dt = omega_i + K*coupling\n"
    "  - K small: incoherent\n"
    "  - K large: synchronized (r->1)\n\n"
    "Key: Complex != Complicated\n"
    "  Feedback + emergence = complexity",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Network Theory:\n\n"
    "Node = Agent\n"
    "Edge = Interaction/feedback\n\n"
    "Key Metrics:\n"
    "  - Degree: number of connections\n"
    "  - Clustering coeff: triangles ratio\n"
    "  - Path length: avg distance\n\n"
    "Network Types:\n"
    "  Random: Low clustering, short path\n"
    "  Small World: High clustering, short\n"
    "  Scale Free: Power-law, hub nodes\n\n"
    "Robustness:\n"
    "  Random failure: robust\n"
    "  Targeted attack: fragile\n"
    "  (hubs are vulnerability)\n\n"
    "In Control:\n"
    "  Controllability of networks\n"
    "  Minimum driver nodes = matching",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
ax.set_title('Network Properties')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day24_complexsys.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
