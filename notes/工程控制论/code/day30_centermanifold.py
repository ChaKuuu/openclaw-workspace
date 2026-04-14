import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 30: Center Manifold Theory")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 30: Center Manifold Theory', fontsize=14)

# ===== Center Manifold: Concept =====
# Near bifurcation: slow dynamics on center manifold
# Fast dynamics decay exponentially
# Governing equation: h satisfies Dh*f(h) - g(h) = 0

# Example: saddle-node on a circle
# x_dot = a + x^2
# y_dot = -y
# Center manifold: y = h(x) ~ O(x^2)

a_vals = np.linspace(-1, 1, 100)
x_eq = np.sqrt(-a_vals)
x_eq = np.where(a_vals < 0, np.nan, x_eq)

ax = axes[0, 0]
ax.plot(a_vals, x_eq, 'b-', lw=2, label='Stable fixed point (x=sqrt(-a))')
ax.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax.axvline(x=0, color='red', ls='--', lw=2, label='Bifurcation at a=0')
ax.set_xlabel('a')
ax.set_ylabel('x_eq')
ax.set_title('Saddle-Node Bifurcation: x_dot = a + x^2')
ax.legend()
ax.grid(True, alpha=0.3)

# ===== Pitchfork with noise =====
# x_dot = mu*x - x^3
# Center manifold: y = h(x) ~ x^3
# Reduced dynamics on center: x_dot = mu*x - x^3

mu_vals = np.linspace(-2, 2, 100)
x_ss = np.sqrt(np.maximum(mu_vals, 0))

ax = axes[0, 1]
ax.plot(mu_vals, x_ss, 'b-', lw=2, label='Stable branches')
ax.plot(mu_vals, -x_ss, 'b-', lw=2)
ax.plot(mu_vals, np.zeros_like(mu_vals), 'r--', lw=1.5, label='Unstable (saddle)')
ax.axvline(x=0, color='gray', ls=':', alpha=0.5)
ax.set_xlabel('mu')
ax.set_ylabel('x_eq')
ax.set_title('Pitchfork: x_dot = mu*x - x^3')
ax.legend()
ax.grid(True, alpha=0.3)

# ===== Normal Forms =====
ax = axes[1, 0]
ax.axis('off')
ax.text(0.05, 0.95,
    "Center Manifold Theory:\n\n"
    "Key Idea:\n"
    "  Near bifurcation, dynamics on center\n"
    "  manifold (slow) decouple from fast\n"
    "  stable directions.\n\n"
    "Algorithm:\n"
    "  1. Linearize: find eigenvalues on axis\n"
    "  2. Separate: center vs stable eigenspaces\n"
    "  3. Guess: h(x) = a*x^2 + b*x^3 + ...\n"
    "  4. Substitute into:\n"
    "     Dh*f(x,h(x)) - g(x,h(x)) = 0\n"
    "  5. Solve for coefficients\n\n"
    "Normal Forms:\n"
    "  Saddle-node: x_dot = s + x^2\n"
    "  Transcritical: x_dot = mu*x - x^2\n"
    "  Pitchfork: x_dot = mu*x - x^3\n"
    "  Hopf: r_dot = mu*r - r^3\n"
    "         theta_dot = omega\n\n"
    "Applications:\n"
    "  - Bifurcation analysis\n"
    "  - Model reduction\n"
    "  - Flutter instability\n"
    "  - Cell differentiation (gene networks)",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

# ===== Lyapunov-Schmidt Reduction =====
ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Lyapunov-Schmidt Reduction:\n\n"
    "Purpose:\n"
    "  Reduce n-dim to 1-2 dim near\n"
    "  bifurcation using projection.\n\n"
    "Method:\n"
    "  P = projection onto center subspace\n"
    "  Q = projection onto range of L\n"
    "  where L = Df(x0) (linearization)\n\n"
    "  B(u,v) = P*D^2f(x0)(u,v)\n"
    "  C(u,v,w) = P*D^3f(x0)(u,v,w)\n\n"
    "  Bifurcation equation:\n"
    "  0 = mu*u + a*u^3 + O(mu*u^2, u^5)\n\n"
    "Connection to Control:\n"
    "  - Input-output linearization\n"
    "    uses similar projections\n"
    "  - Normal forms = canonical forms\n"
    "    in control system design\n"
    "  - Center manifold = slow variable\n"
    "    selection in hierarchical control",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
ax.set_title('Lyapunov-Schmidt')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day30_centermanifold.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
