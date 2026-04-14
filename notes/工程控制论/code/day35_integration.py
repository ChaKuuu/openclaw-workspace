import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 35: Phase 1 Integration - Chaos to Control")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Day 35: From Chaos to Control - Integration Project', fontsize=14)

# ===== Phase Space of Real Systems =====
# Show progression: stable -> Hopf -> chaos

omega_n = 1.0
zeta_vals = [2.0, 0.5, 0.0, -0.1]
T = 20.0
dt = 0.01
N = int(T/dt)
t = np.linspace(0, T, N)

for idx, zeta in enumerate(zeta_vals):
    ax = axes[0, idx % 3]
    if zeta >= 0:
        x = np.zeros((N, 2))
        x[0] = [1.0, 0.0]
        for i in range(N-1):
            x[i+1, 1] = x[i, 1] + (-2*zeta*omega_n*x[i, 1] - omega_n**2*x[i, 0]) * dt
            x[i+1, 0] = x[i, 0] + x[i, 1] * dt
        color = 'green' if zeta > 0 else 'blue'
        ax.plot(x[::5, 0], x[::5, 1], 'b-', lw=1.5, alpha=0.7)
        ax.set_title(f'Damped Oscillator zeta={zeta}')
    else:
        # Negative damping = blow up
        x = np.zeros((N, 2))
        x[0] = [0.1, 0.0]
        for i in range(N-1):
            x[i+1, 1] = x[i, 1] + (-2*zeta*omega_n*x[i, 1] - omega_n**2*x[i, 0]) * dt
            x[i+1, 0] = x[i, 0] + x[i, 1] * dt
            if np.abs(x[i+1, 0]) > 100:
                break
        ax.plot(x[:i+1:5, 0], x[:i+1:5, 1], 'r-', lw=1.5)
        ax.set_title(f'Negative Damping: Explosion (zeta={zeta})')
    ax.set_xlabel('x')
    ax.set_ylabel('dx/dt')
    ax.grid(True, alpha=0.3)

# ===== Chaos to Control Summary =====
ax = axes[1, 0]
ax.axis('off')
ax.text(0.05, 0.95,
    "Phase 1 Summary: Chaos Theory\n\n"
    "Core Concepts:\n"
    "  - Sensitivity to IC (butterfly effect)\n"
    "  - Strange attractors (fractal dim)\n"
    "  - Period doubling route to chaos\n"
    "  - Shilnikov theorem (homoclinic)\n\n"
    "Bifurcations:\n"
    "  - Saddle-node: birth of cycle\n"
    "  - Hopf: equilibrium -> LC\n"
    "  - Period-doubling: 1T -> 2T -> chaos\n"
    "  - Crisis: sudden chaos boundary change\n\n"
    "Control Methods:\n"
    "  - OGY: tiny parameter perturbation\n"
    "  - Pyragas: time-delayed feedback\n"
    "  - Backstepping: recursive design\n"
    "  - SMC: robust to chaos\n\n"
    "Key Insight:\n"
    "  Chaos is not random - it has\n"
    "  structure (UPOs). Small control\n"
    "  can stabilize desired UPO.",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Chaos Theory Summary')

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Phase 1 vs Previous Weeks:\n\n"
    "Week 1-2 (Linear):\n"
    "  All eigenvalues have Re<0\n"
    "  -> Asymptotically stable\n"
    "  -> No interesting dynamics\n\n"
    "Week 3 (Nonlinear):\n"
    "  Limit cycles, bifurcations\n"
    "  -> Qualitative change\n"
    "  -> Center manifold theory\n\n"
    "Phase 1 (Chaos):\n"
    "  Strange attractors\n"
    "  -> Deterministic yet unpredictable\n"
    "  -> Sensitive to perturbation\n"
    "  -> OGY exploits this sensitivity\n\n"
    "From Control Perspective:\n"
    "  - Chaos = enemy in most systems\n"
    "    (power grids, lasers, hearts)\n"
    "  - Chaos = opportunity\n"
    "    (mixing, encryption, diversity)\n"
    "  - Control theory provides tools\n"
    "    for both suppressing and\n"
    "    exploiting chaos",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
ax.set_title('Phase 1 Integration')

ax = axes[1, 2]
ax.axis('off')
ax.text(0.05, 0.95,
    "====== 35-DAY COMPLETE ======\n\n"
    "Classical Control (Week 1):\n"
    "  Routh, Bode, Nyquist, PID\n\n"
    "Modern Control (Week 2):\n"
    "  LQR, Kalman, LQG\n\n"
    "Advanced Nonlin+Robust (Week 3):\n"
    "  Lyapunov, Hinf, SMC\n\n"
    "Phase 1 - Chaos (Days 29-35):\n"
    "  Poincare, Hopf, OGY, Lorenz\n\n"
    "====== ALL COMPLETE ======\n\n"
    "钱学森《工程控制论》\n"
    "+ Chaos Control Theory\n"
    "+ Fractal Dynamics\n"
    "+ Phase 1 Advanced Topics\n"
    "35 DAYS OF CONTROL THEORY!",
    transform=ax.transAxes, va='top', fontsize=13,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))
ax.set_title('Final Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day35_integration.png', dpi=150, bbox_inches='tight')
print("\n" + "="*60)
print("PHASE 1 COMPLETE!")
print("35 DAYS OF CONTROL THEORY DONE!")
print("="*60)
