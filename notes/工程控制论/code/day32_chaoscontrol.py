import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 32: Chaos Control - OGY Method")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 32: Chaos Control - OGY', fontsize=14)

# ===== Logistic Map =====
r_chaos = 4.0
N = 200
x_chaos = np.zeros(N)
x_chaos[0] = 0.5
for i in range(N-1):
    x_chaos[i+1] = r_chaos * x_chaos[i] * (1 - x_chaos[i])

x_star = (r_chaos - 1) / r_chaos

x_ogy = np.zeros(N)
x_ogy[0] = 0.5
r_actual = r_chaos

for i in range(N-1):
    x = x_ogy[i]
    dfdr = x * (1 - x)
    dfdx = r_actual * (1 - 2*x)
    if i > 100 and i % 20 == 0:
        delta_x = x - x_star
        if abs(dfdr) > 1e-6:
            lam_target = 0.5
            delta_r_needed = (lam_target - dfdx) * delta_x / dfdr
            delta_r_needed = np.clip(delta_r_needed, -0.1, 0.1)
            r_actual = r_chaos + delta_r_needed
        else:
            r_actual = r_chaos
    x_ogy[i+1] = r_actual * x_ogy[i] * (1 - x_ogy[i])
    r_actual = r_chaos

n_arr = np.arange(N)
ax = axes[0, 0]
ax.plot(n_arr, x_chaos, 'b-', lw=1, alpha=0.7, label='Uncontrolled')
ax.axhline(y=x_star, color='red', ls='--', lw=1.5, label=f'x*={x_star:.3f}')
ax.set_xlabel('n')
ax.set_ylabel('x_n')
ax.set_title('Logistic Map: Chaotic (r=4)')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(n_arr, x_ogy, 'orange', lw=1.5, label='OGY controlled')
ax.axhline(y=x_star, color='red', ls='--', lw=1.5, label=f'x*={x_star:.3f}')
ax.set_xlabel('n')
ax.set_ylabel('x_n')
ax.set_title('OGY Control: Stabilizing Fixed Point')
ax.legend()
ax.grid(True, alpha=0.3)

# Lyapunov exponents approximation
LE_approx = np.zeros(100)
for j in range(100):
    x_test = np.random.rand()
    s = 0.0
    for i in range(1000):
        x_test = r_chaos * x_test * (1 - x_test)
        if i > 100:
            s += np.log(abs(r_chaos * (1 - 2*x_test)))
    LE_approx[j] = s / 900.0

ax = axes[1, 0]
ax.hist(LE_approx, bins=20, color='steelblue', alpha=0.7)
ax.axvline(x=np.mean(LE_approx), color='red', lw=2, label=f'Mean LE={np.mean(LE_approx):.3f}')
ax.set_xlabel('Lyapunov Exponent')
ax.set_ylabel('Frequency')
ax.set_title('Lyapunov Exponent Distribution (Logistic r=4)')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "OGY Method (Ott, Grebogi, Yorke, 1990):\n\n"
    "Key Idea:\n"
    "  Chaos has infinite unstable periodic\n"
    "  orbits (UPOs) embedded in it\n"
    "  Small parameter perturbation can\n"
    "  stabilize desired UPO\n\n"
    "Algorithm:\n"
    "  1. Identify desired fixed point x*\n"
    "  2. Linearize: x_{n+1} = A*x_n + B*delta_r\n"
    "  3. Compute delta_r needed\n"
    "  4. Apply small delta_r (noise-level)\n\n"
    "Properties:\n"
    "  - Tiny control effort\n"
    "  - Works for high-dimensional chaos\n"
    "  - Needs periodic orbit identification\n\n"
    "Pyragas Method:\n"
    "  u(t) = K*(y(t-tau) - y(t))\n"
    "  tau = period of unstable orbit\n"
    "  Continuous version of OGY\n\n"
    "Applications:\n"
    "  - Cardiac dynamics\n"
    "  - Turbulence control\n"
    "  - Semiconductor lasers",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('OGY Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day32_chaoscontrol.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
