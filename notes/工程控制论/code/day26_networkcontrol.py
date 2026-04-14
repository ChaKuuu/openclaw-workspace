import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 26: Networked Control Systems")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 26: Networked Control Systems', fontsize=14)

tau_vals = [0.0, 0.1, 0.2, 0.5]
t = np.linspace(0, 10, 500)
omega_n = 2.0
zeta = 0.5
ax = axes[0, 0]
for tau in tau_vals:
    zeta_eff = zeta / (1 + 2*tau)
    omega_d = omega_n * np.sqrt(max(0, 1-zeta_eff**2))
    response = 1 - (1/np.sqrt(1-zeta_eff**2)) * np.exp(-zeta_eff*omega_n*t) * np.cos(omega_d*t - np.arccos(max(-1,min(1,zeta_eff))))
    response = np.clip(response, 0, 2)
    ax.plot(t, response, lw=2, label=f'tau={tau}s')
ax.set_xlabel('t (s)')
ax.set_ylabel('Step response')
ax.set_title('Effect of Network Delay')
ax.legend()
ax.grid(True, alpha=0.3)

np.random.seed(42)
T = 5.0
dt = 0.01
N = int(T/dt)
t = np.linspace(0, T, N)
u_base = np.ones(N)
ax = axes[0, 1]
for p_loss in [0.0, 0.1, 0.3, 0.5]:
    u_delayed = np.zeros(N)
    last_u = 0.0
    for i in range(N):
        if np.random.rand() > p_loss:
            last_u = u_base[i]
        u_delayed[i] = last_u
    ax.plot(t, u_delayed, alpha=0.7, lw=1.5, label=f'p_loss={p_loss}')
ax.set_xlabel('t (s)')
ax.set_ylabel('Control signal')
ax.set_title('Effect of Packet Loss')
ax.legend()
ax.grid(True, alpha=0.3)

N_agents = 5
A = np.array([[0,1,1,0,0],[1,0,1,1,0],[1,1,0,1,1],[0,1,1,0,1],[0,0,1,1,0]])
D = np.diag(A.sum(axis=1))
L = D - A
x0 = np.array([1.0, 0.8, 0.5, 0.2, 0.0])
x_t = np.zeros((N, N_agents))
x_t[0] = x0
K_cons = 0.5
for i in range(N-1):
    x_t[i+1] = x_t[i] + K_cons * np.dot(L, x_t[i]) * dt
ax = axes[1, 0]
for i in range(N_agents):
    ax.plot(t, x_t[:, i], lw=1.5, label=f'Agent {i+1}')
ax.axhline(y=np.mean(x0), color='black', ls='--', lw=2, label='Consensus')
ax.set_xlabel('t (s)')
ax.set_ylabel('State')
ax.set_title('Consensus Protocol')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Networked Control Systems:\n\n"
    "Key Challenges:\n"
    "  1. Network Delay tau\n"
    "     - Reduces effective damping\n"
    "     - Can destabilize if too large\n\n"
    "  2. Packet Loss\n"
    "     - Zero-order hold (ZOH)\n"
    "     - Missed packets -> stale control\n\n"
    "  3. Quantization\n"
    "     - Finite bits for communication\n\n"
    "Consensus Protocol:\n"
    "  dx_i/dt = sum_j a_ij(x_j - x_i)\n"
    "  -> All agents converge to average\n\n"
    "Distributed Control:\n"
    "  - No central coordinator\n"
    "  - Only local information\n"
    "  - Emergent global behavior\n\n"
    "Applications:\n"
    "  - Drone swarms\n"
    "  - Smart grid\n"
    "  - Vehicle platooning\n"
    "  - Sensor networks",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day26_networkcontrol.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
