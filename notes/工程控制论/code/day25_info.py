import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 25: Information Theory")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 25: Information Theory', fontsize=14)

p = np.linspace(0.001, 0.999, 200)
H_binary = -p * np.log2(p) - (1-p) * np.log2(1-p)
ax = axes[0, 0]
ax.plot(p, H_binary, 'b-', lw=2)
ax.set_xlabel('p (probability)')
ax.set_ylabel('H(p) bits')
ax.set_title('Binary Entropy H(p)')
ax.grid(True, alpha=0.3)
ax.annotate('Max at p=0.5\nH=1 bit', xy=(0.5, 1.0), fontsize=10, ha='center', xytext=(0.7, 0.8), arrowprops=dict(arrowstyle='->', color='gray'))

p_err = np.linspace(0, 0.5, 200)
C_bsc = 1 - (-p_err * np.log2(p_err) - (1-p_err) * np.log2(1-p_err))
ax = axes[0, 1]
ax.plot(p_err, C_bsc, 'orange', lw=2)
ax.set_xlabel('Error probability p')
ax.set_ylabel('Channel Capacity C')
ax.set_title('BSC: C = 1 - H(p)')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 0.5)
ax.set_ylim(0, 1)
ax.axhline(y=1, color='gray', ls='--', alpha=0.5)

SNR_db = np.linspace(-10, 20, 200)
SNR = 10**(SNR_db/10)
capacity_awgn = np.log2(1 + SNR)
ax = axes[1, 0]
ax.plot(SNR_db, capacity_awgn, 'g-', lw=2)
ax.set_xlabel('SNR (dB)')
ax.set_ylabel('Capacity (bits/channel use)')
ax.set_title('AWGN: C = log2(1+SNR)')
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Shannon Information Theory:\n\n"
    "Entropy:\n"
    "  H(X) = -sum(p*log2(p)) bits\n"
    "  Measures uncertainty in X\n\n"
    "Mutual Information:\n"
    "  I(X;Y) = H(X) - H(X|Y)\n"
    "  = H(Y) - H(Y|X)\n"
    "  Information shared between X and Y\n\n"
    "Channel Capacity:\n"
    "  BSC: C = 1 - H(p_error) bits/use\n"
    "  AWGN: C = log2(1+SNR) bits/use\n\n"
    "Noisy Coding Theorem:\n"
    "  For rate R < C: arbitrarily low BER\n"
    "  For rate R > C: errors unavoidable\n\n"
    "Connection to Control:\n"
    "  Feedback = side information\n"
    "  Can double effective capacity\n"
    "  Sensor fusion = info combining",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day25_info.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
