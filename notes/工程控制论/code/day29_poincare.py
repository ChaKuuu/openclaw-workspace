import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("Day 29: Poincare Section + Homoclinic/ Heteroclinic Orbits")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 29: Poincare Section & Homoclinic Orbits', fontsize=14)

# ===== Duffing Oscillator =====
# x_ddot + delta*x_dot + x + x^3 = gamma*cos(omega*t)
# Forced Duffing: shows chaos for certain parameters

delta = 0.05
gamma = 0.4
omega = 1.0

def duffing(x, t):
    return np.array([x[1], gamma*np.cos(omega*t) - delta*x[1] - x[0] - x[0]**3])

T = 200.0
dt = 0.01
N = int(T/dt)
t = np.linspace(0, T, N)
x = np.zeros((N, 2))
x[0] = [0.1, 0.0]

for i in range(N-1):
    k1 = duffing(x[i], t[i])
    k2 = duffing(x[i] + k1*dt/2, t[i] + dt/2)
    k3 = duffing(x[i] + k2*dt/2, t[i] + dt/2)
    k4 = duffing(x[i] + k3*dt, t[i] + dt)
    x[i+1] = x[i] + (k1 + 2*k2 + 2*k3 + k4)/6 * dt

# Discard transient
x_transient = 10000
t_trim = t[x_transient:]
x_trim = x[x_transient:]

# Poincare section: sample at driving period T_drive = 2*pi/omega
T_drive = 2*np.pi/omega
n_drive = int(T_drive/dt)
poincare_x = x_trim[::n_drive, 0]
poincare_y = x_trim[::n_drive, 1]

ax = axes[0, 0]
ax.plot(x_trim[::5, 0], x_trim[::5, 1], 'b-', lw=0.3, alpha=0.5)
ax.set_xlabel('x')
ax.set_ylabel('dx/dt')
ax.set_title('Duffing Oscillator: Full Trajectory')
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(poincare_x, poincare_y, 'r.', ms=3, alpha=0.6)
ax.set_xlabel('x (at t = n*T_drive)')
ax.set_ylabel('dx/dt (at t = n*T_drive)')
ax.set_title('Poincare Section (forced Duffing)')
ax.grid(True, alpha=0.3)

# ===== Pendulum Homoclinic Orbit =====
# x_ddot + sin(x) = 0  (undamped pendulum)
# Homoclinic orbit at E = 2 (separatrix)

def pend_undamped(x):
    return np.array([x[1], -np.sin(x[0])])

E_vals = [0.5, 1.0, 1.9, 2.0, 2.1]
ax = axes[1, 0]
for E in E_vals:
    x_init = [0.01, np.sqrt(2*E)]
    x_orbit = np.zeros((2000, 2))
    x_orbit[0] = x_init
    for i in range(1999):
        k1 = pend_undamped(x_orbit[i])
        k2 = pend_undamped(x_orbit[i] + k1*0.05)
        k3 = pend_undamped(x_orbit[i] + k2*0.05)
        k4 = pend_undamped(x_orbit[i] + k3*0.05)
        x_orbit[i+1] = x_orbit[i] + (k1 + 2*k2 + 2*k3 + k4)/6 * 0.05
        if x_orbit[i+1, 0] > 4 or x_orbit[i+1, 0] < -4:
            break
    style = 'k--' if E == 2.0 else 'b-'
    lw = 2 if E == 2.0 else 1
    ax.plot(x_orbit[:, 0], x_orbit[:, 1], style, lw=lw, label=f'E={E}', alpha=0.8)

ax.set_xlabel('theta')
ax.set_ylabel('omega')
ax.set_title('Undamped Pendulum: Energy Levels (E=2 is separatrix)')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Poincare Section:\n\n"
    "  - Sample state at multiples of T_drive\n"
    "  - Reduces n-dim to (n-1)-dim map\n"
    "  - Periodic orbit -> discrete points\n"
    "  - Quasi-periodic -> closed curve\n"
    "  - Chaos -> fractal scatter\n\n"
    "Homoclinic Orbit (Separatrix):\n\n"
    "  - Connects a saddle to itself\n"
    "  - Energy = 2 for undamped pendulum\n"
    "  - Separates oscillation from rotation\n"
    "  - Perturbations -> homoclinic tangle\n"
    "    (gateway to chaos)\n\n"
    "Heteroclinic Orbit:\n\n"
    "  - Connects TWO different saddles\n"
    "  - Used in slow manifold analysis\n"
    "  - Perturbed -> complex dynamics\n\n"
    "Key Insight:\n"
    "  Separatrix = boundary between\n"
    "  qualitatively different behaviors\n"
    "  Near separatrix = sensitive to\n"
    "  small perturbations = chaos",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day29_poincare.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
