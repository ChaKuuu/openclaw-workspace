import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("Day 22: System Engineering - Reliability & Redundancy")
print("=" * 60)

# ===== Reliability Basics =====
# Reliability R(t) = P(system works at time t)
# Failure rate lambda: R(t) = exp(-lambda*t)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 22: Reliability & Redundancy', fontsize=14)

t = np.linspace(0, 10, 500)
lam = 0.2

R = np.exp(-lam * t)
F = 1 - R  # CDF

ax = axes[0, 0]
ax.plot(t, R, 'b-', lw=2, label='R(t) = exp(-lambda*t)')
ax.plot(t, F, 'r-', lw=2, label='F(t) = 1 - R(t)')
ax.set_xlabel('t')
ax.set_ylabel('Probability')
ax.set_title('Reliability Function R(t)')
ax.legend()
ax.grid(True, alpha=0.3)

# ===== Redundancy =====
# Series: R_s = R1 * R2 * ... * Rn
# Parallel: R_p = 1 - (1-R1)*(1-R2)*...
# 2-out-of-3: R_2oo3 = R1*R2*R3 + 3*R1*R2*(1-R3) + ...

R1_vals = np.linspace(0.5, 0.99, 100)
R_series = R1_vals ** 2
R_parallel = 1 - (1-R1_vals)**2
R_2oo3 = 3*R1_vals**2 - 2*R1_vals**3

ax = axes[0, 1]
ax.plot(R1_vals, R_series, 'b-', lw=2, label='Series (2 components)')
ax.plot(R1_vals, R_parallel, 'orange', lw=2, label='Parallel (2 components)')
ax.plot(R1_vals, R_2oo3, 'green', lw=2, label='2-out-of-3 voting')
ax.set_xlabel('Individual component reliability')
ax.set_ylabel('System reliability')
ax.set_title('Redundancy Strategies')
ax.legend()
ax.grid(True, alpha=0.3)

# ===== MTBF (Mean Time Between Failures) =====
# MTBF = 1/lambda for exponential failure
# For parallel: MTBF_parallel = 1/lambda + 1/(2*lambda)

mtbf_series = 1/lam
mtbf_parallel = 1/lam + 1/(2*lam)
mtbf_2oo3 = 5/(6*lam)

ax = axes[1, 0]
labels = ['Series\n(2 comp)', 'Parallel\n(2 comp)', '2-out-of-3']
mtbfs = [mtbf_series, mtbf_parallel, mtbf_2oo3]
colors = ['blue', 'orange', 'green']
ax.bar(labels, mtbfs, color=colors, alpha=0.7)
ax.set_ylabel('MTBF (hours)')
ax.set_title(f'MTBF Comparison (lambda={lam}/hr)')
for i, v in enumerate(mtbfs):
    ax.text(i, v + 0.3, f'{v:.1f}', ha='center', fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# ===== Safety Analysis =====
ax = axes[1, 1]
ax.axis('off')
txt = ("""Reliability Engineering:\n\n"""
       """Reliability R(t):\n"""
       """  R(t) = exp(-lambda*t)\n"""
       """  lambda = failure rate (/hr)\n\n"""
       """Series System:\n"""
       """  R_s = R1 * R2 * ... * Rn\n"""
       """  Any failure -> system fails\n\n"""
       """Parallel (Redundant):\n"""
       """  R_p = 1 - prod(1-Ri)\n"""
       """  All must fail -> system fails\n\n"""
       """2-out-of-3 Voting:\n"""
       """  R_2oo3 = 3R^3 - 2R^2\n"""
       """  Tolerates 1 failure\n\n"""
       """MTBF:\n"""
       """  Series: MTBF = 1/lambda\n"""
       """  Parallel: MTBF = 1/lambda + 1/(2*lambda)\n\n"""
       """Key Insight:\n"""
       """  Redundancy trades cost for safety\n"""
       """  Voting systems are common in aerospace\n"""
       """  Triple Modular Redundancy (TMR) is standard\n""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=11,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day22_reliability.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
