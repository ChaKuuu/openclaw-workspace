import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("Day 18: Describing Function + Sliding Mode Control")
print("=" * 60)

# ===== Describing Function =====
# Approximate nonlinear as linear gain at fundamental frequency
# For relay: N(A) = 4d / (pi * A)  (d = relay amplitude)
# For saturation: N(A) = (2/pi) * (asin(d/A) + d*sqrt(A^2-d^2)/A^2)

print("""
========================================
Describing Function Method
========================================

Key Idea: Replace nonlinear element with equivalent linear gain
  at the fundamental frequency of a sinusoidal input.

N(A) = output fundamental / input amplitude

Common describing functions:

Relay (on/off, amplitude d):
  N(A) = 4d / (pi * A)

Saturation (linear until |u|<=d, then constant):
  N(A) = 1, A <= d
  N(A) = (2/pi) * (asin(d/A) + d*sqrt(A^2-d^2)/A^2), A > d

Backlash / Hysteresis:
  N(A) = more complex expressions

Application: Predict limit cycles in nonlinear systems
  by checking if Nyquist plot intersects -1/N(A).
""")

# ===== Describe Function for Relay =====
A = np.linspace(0.01, 3.0, 300)
d = 1.0

def relay_DF(A, d=1.0):
    return 4 * d / (np.pi * A)

def sat_DF(A, d=1.0):
    result = np.ones_like(A)
    mask = A > d
    A_large = A[mask]
    result[mask] = (2/np.pi) * (np.arcsin(d/A_large) + d*np.sqrt(A_large**2-d**2)/A_large**2)
    return result

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 18: Describing Function + Sliding Mode', fontsize=14)

ax = axes[0, 0]
ax.plot(A, relay_DF(A), 'b-', lw=2, label='Relay N(A)')
ax.plot(A, sat_DF(A), 'orange', lw=2, label='Saturation N(A)')
ax.set_xlabel('A (input amplitude)')
ax.set_ylabel('N(A)')
ax.set_title('Describing Functions')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 2)

# ===== Sliding Mode Control =====
# System: x_dot = Ax + Bu + d(t)
# Goal: make x track desired trajectory despite disturbance d(t)
# Sliding surface: s = (d/dt + lambda)^(n-1) * e
# Control law: u = -K*sign(s)

print("""
========================================
Sliding Mode Control (SMC)
========================================

Key Idea: Drive system to a predefined surface s=0,
  then slide along it to the origin despite disturbances.

Two phases:
  1. Reaching phase: u pushes x toward surface s=0
  2. Sliding phase: system stays on s=0 (invariant set)

Advantages:
  - Robust to matched disturbances (d(t) in range of B)
  - Finite-time convergence to surface
  - Order reduction: n-th order -> 1st order on surface

Disadvantages:
  - Chattering: high-frequency switching (ideal: infinite freq)
  - Requires perfect knowledge of B

Chattering reduction:
  - Boundary layer: sign(s) -> sat(s/delta)
  - Higher-order SMC (SOSMC)
""")

# ===== Sliding Mode Simulation =====
# 2nd order: x1_dot = x2, x2_dot = u + d(t)
# Surface: s = x2 + lambda*x1
# SMC: u = -K*sign(s)

lam = 2.0
K = 5.0
delta = 0.3  # boundary layer width

def smc_f(x, xd, u):
    e1 = x[0] - xd[0]
    e2 = x[1] - xd[1]
    s = e2 + lam * e1
    # Control with boundary layer
    u_unc = -K * np.sign(s)
    u_bl = -K * np.clip(s/delta, -1, 1)
    return np.array([x[1], u_bl])

T = 5.0
dt = 0.001
N = int(T/dt)
t = np.linspace(0, T, N)

# Desired trajectory
xd = np.zeros((N, 2))
xd[:, 0] = 1.0 * np.ones(N)  # step
xd[:, 1] = 0.0 * np.ones(N)

x = np.zeros((N, 2))
x[0] = [0.0, 0.0]
s_hist = np.zeros(N)

for i in range(N-1):
    e1 = x[i, 0] - xd[i, 0]
    e2 = x[i, 1] - xd[i, 1]
    s = e2 + lam * e1
    s_hist[i] = s
    u = -K * np.sign(s)
    x[i+1, 1] = x[i, 1] + u * dt
    x[i+1, 0] = x[i, 0] + x[i, 1] * dt

ax = axes[0, 1]
ax.plot(t, x[:, 0], 'b-', lw=2, label='x1 (position)')
ax.plot(t, xd[:, 0], 'r--', lw=2, label='xd (desired)')
ax.set_xlabel('t (s)')
ax.set_ylabel('x1')
ax.set_title('Sliding Mode: Position Tracking')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(t, s_hist, 'purple', lw=1.5, label='s = e2 + lambda*e1')
ax.plot(t, np.ones(N)*delta, 'gray', ls='--', alpha=0.5)
ax.plot(t, -np.ones(N)*delta, 'gray', ls='--', alpha=0.5, label='boundary layer')
ax.set_xlabel('t (s)')
ax.set_ylabel('s')
ax.set_title('Sliding Surface (chattering visible)')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
txt = ("""Key Formulas:\n\n"""
       """Describing Function:\n"""
       """  Relay: N(A) = 4d/(pi*A)\n\n"""
       """  Saturation:\n"""
       """  N(A) = 1, A <= d\n"""
       """  N(A) = (2/pi)*(asin(d/A) + ...)\n\n"""
       """Sliding Mode:\n"""
       """  Surface: s = (d+lambda)^(n-1)*e\n"""
       """  u = -K*sign(s)  (ideal)\n"""
       """  u = -K*sat(s/delta)  (practical)\n\n"""
       """Chattering:\n"""
       """  - Caused by switching at finite freq\n"""
       """  - Reduced by boundary layer\n"""
       """  - Physical interpretation:\n"""
       """    actuator cannot switch infinitely fast""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=11,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day18_nonlinearmac.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")
