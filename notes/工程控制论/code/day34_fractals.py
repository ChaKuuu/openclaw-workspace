import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 34: Fractals and Dimension")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 34: Fractals and Lyapunov Dimension', fontsize=14)

# ===== Koch Snowflake =====
def koch(order, p1, p2):
    if order == 0:
        return [p1, p2]
    pA = p1
    pB = (2*p1 + p2) / 3
    pD = (p1 + 2*p2) / 3
    angle = np.pi / 3
    pC = pB + (pD - pB) * np.exp(1j * angle)
    return (koch(order-1, pA, pB) + koch(order-1, pB, pC) + koch(order-1, pC, pD) + koch(order-1, pD, pB))

ax = axes[0, 0]
pts = koch(3, 0, 1)
xs = [z.real for z in pts]
ys = [z.imag for z in pts]
ax.fill(xs, ys, color='steelblue', alpha=0.3)
ax.plot(xs, ys, 'b-', lw=0.5)
ax.set_title('Koch Snowflake (order=3)')
ax.set_aspect('equal')
ax.axis('off')

# ===== Logistic Map Bifurcation -> Lyapunov =====
mu_vals = np.linspace(2.5, 4.0, 500)
LE_map = np.zeros_like(mu_vals)

for idx, mu in enumerate(mu_vals):
    x = 0.5
    s = 0.0
    for i in range(1000):
        x = mu * x * (1 - x)
        if i > 200:
            s += np.log(abs(mu * (1 - 2*x)))
    LE_map[idx] = s / 800.0

ax = axes[0, 1]
ax.plot(mu_vals, LE_map, 'b-', lw=1.5)
ax.axhline(y=0, color='red', ls='--', lw=1.5, label='LE=0 threshold')
ax.fill_between(mu_vals, LE_map, where=(LE_map<0), alpha=0.2, color='blue', label='Periodic (LE<0)')
ax.fill_between(mu_vals, LE_map, where=(LE_map>0), alpha=0.2, color='red', label='Chaotic (LE>0)')
ax.set_xlabel('mu')
ax.set_ylabel('Lyapunov Exponent')
ax.set_title('Lyapunov Exponent: Logistic Map')
ax.legend()
ax.grid(True, alpha=0.3)

# ===== Kaplan-Yorke Dimension =====
# For Lorenz: sigma=10, beta=8/3, rho=28
# LE1 + LE2 + LE3 = sigma + sigma - rho - beta - 1 = ?
# Actually compute numerically

def lyapunov_lorenz(rho, N=5000):
    sigma, beta = 10.0, 8.0/3.0
    x = [1.0, 1.0, 1.0]
    LE = np.zeros(3)
    for _ in range(N):
        x_new = np.array([
            sigma*(x[1]-x[0]),
            x[0]*(rho - x[2]) - x[1],
            x[0]*x[1] - beta*x[2]
        ])
        LE += np.abs(x_new)**2
        x = x_new * 0.1
    LE = np.log(np.sqrt(LE/N))
    return LE

rho_range = np.linspace(1, 50, 50)
D_KY = np.zeros(len(rho_range))
for idx, rho in enumerate(rho_range):
    LEs = lyapunov_lorenz(rho, N=1000)
    LEs_sorted = np.sort(LEs)[::-1]
    k = 0
    while k < 3 and LEs_sorted[k] > 0:
        k += 1
    if k == 0:
        D_KY[idx] = 0
    elif k == 3:
        D_KY[idx] = 3
    else:
        D_KY[idx] = k + sum(LEs_sorted[:k]) / abs(LEs_sorted[k])

ax = axes[1, 0]
ax.plot(rho_range, D_KY, 'purple', lw=2)
ax.axvline(x=24.74, color='red', ls='--', lw=2, label='Chaos onset')
ax.set_xlabel('rho')
ax.set_ylabel('Kaplan-Yorke Dimension')
ax.set_title('Lyapunov Dimension: Lorenz vs rho')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Fractal Dimension:\n\n"
    "Box-Counting Dimension:\n"
    "  D_0 = lim_{eps->0} log(N(eps)) / log(1/eps)\n\n"
    "Information Dimension:\n"
    "  D_1 = lim_{eps->0} H(eps) / log(1/eps)\n\n"
    "Lyapunov Dimension (Kaplan-Yorke):\n"
    "  D_KY = k + sum(LE_i) / |LE_{k+1}|\n"
    "  where k = max{j: sum_{i=1}^{j} LE_i >= 0}\n\n"
    "For Lorenz (rho=28):\n"
    "  LE = [0.906, 0, -14.572]\n"
    "  D_KY = 2 + 0.906/14.572 = 2.062\n\n"
    "Key Properties:\n"
    "  - Integer for smooth attractors\n"
    "  - Fractional for fractal attractors\n"
    "  - Strange = fractal + chaotic\n\n"
    "Box-Counting Algorithm:\n"
    "  1. Cover set with N(eps) boxes size eps\n"
    "  2. Repeat for smaller eps\n"
    "  3. Slope = fractal dimension",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day34_fractals.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
