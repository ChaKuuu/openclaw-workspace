import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 23: Human-Machine Systems")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 23: Human-Machine Systems', fontsize=14)

ax = axes[0, 0]
f = np.linspace(0.01, 5, 400)
K_h = 5.0
tau_h = 0.25
omega = 2 * np.pi * f
Y_h_mag = K_h * np.ones_like(f)
ax.semilogx(f, 20*np.log10(Y_h_mag), 'b-', lw=2)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('|Y_h| (dB)')
ax.set_title('Human Operator Magnitude')
ax.grid(True, alpha=0.3, which='both')

modes = ['Manual', 'Supervisory', 'Automatic', 'Adaptive']
automation = [0, 0.3, 0.7, 1.0]
perf = [0.4, 0.8, 0.9, 0.85]
cost = [0.3, 0.4, 0.7, 0.9]
x_pos = np.arange(len(modes))
width = 0.35
ax = axes[0, 1]
ax.bar(x_pos - width/2, perf, width, label='Performance', color='steelblue', alpha=0.8)
ax.bar(x_pos + width/2, cost, width, label='Cost', color='orange', alpha=0.8)
ax.set_ylabel('Level')
ax.set_title('Automation Level vs Performance')
ax.set_xticks(x_pos)
ax.set_xticklabels(modes)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

tasks = ['Single', 'Dual', 'Triple', 'Overflow']
workload = [0.2, 0.5, 0.75, 0.95]
error_prob = [0.01, 0.05, 0.15, 0.40]
ax = axes[1, 0]
ax.plot(workload, error_prob, 'ro-', lw=2, ms=8)
ax.fill_between(workload, error_prob, alpha=0.2, color='red')
ax.set_xlabel('Mental Workload (0-1)')
ax.set_ylabel('Error Probability')
ax.set_title('Performance vs Arousal')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(0, 0.5)

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Human-Machine Control:\n\n"
    "Human Operator Model:\n"
    "  Y_h = K_h * exp(-tau_h*s) / s\n"
    "  tau_h = 0.2-0.3s reaction delay\n\n"
    "Key Properties:\n"
    "  - Nonlinear (attention limits)\n"
    "  - Adaptive (learns task)\n"
    "  - Handles novel situations\n\n"
    "Automation Levels:\n"
    "  1. Manual (human does all)\n"
    "  2. Aid (AI assists)\n"
    "  3. Shared (equal partnership)\n"
    "  4. Supervised (AI leads)\n"
    "  5. Full automation\n\n"
    "Best: Human judgment + AI precision",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day23_humanmachine.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
