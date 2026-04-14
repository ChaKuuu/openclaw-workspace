import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("Day 12: Model Reference Adaptive Control (MRAC)")
print("=" * 60)

# ===== MRAC Concept =====
# Plant: y = Gp(s) * u  (unknown)
# Reference Model: ym = Gm(s) * r
# Controller adjusts its parameters to make y -> ym
#
# MIT Rule: d_theta/dt = -gamma * e * phi
# where phi = partial(ym)/partial(theta)

print("""
MRAC: Model Reference Adaptive Control

Key Idea:
  - Plant parameters UNKNOWN (e.g., unknown mass, friction)
  - Reference Model: desired behavior (how should y respond?)
  - Controller adapts its gains to make plant match reference

Architecture:
  Plant (unknown) --y--> error
                    ^
                    |
  Controller --u----+
      ^
      |
  Reference Model --ym--> e = y - ym --> MIT Rule --> theta_dot

MIT Rule:
  theta_dot = -gamma * e * phi
  (theta = controller parameter, phi = regression vector, gamma = adaptation rate)

Properties:
  - Works for plants with unknown parameters
  - gamma too small -> too slow adaptation
  - gamma too large -> oscillations / instability
""")

# ===== Simple MRAC Simulation =====
# 1st order plant: y_dot = -a*y + b*u  (a, b unknown)
# Reference model: ym_dot = -am*ym + bm*r
# Controller: u = theta1*r + theta2*y

a_true = 1.0   # unknown plant parameter
b_true = 2.0   # unknown plant parameter
am = 2.0       # desired model
bm = 2.0

gamma = 2.0     # adaptation rate

T = 5.0
dt = 0.005
N = int(T / dt)
t = np.linspace(0, T, N)

# Initial parameter estimates
theta1 = 0.0
theta2 = 0.0

y = np.zeros(N)
ym = np.zeros(N)
e = np.zeros(N)
u = np.zeros(N)
theta1_hist = np.zeros(N)
theta2_hist = np.zeros(N)

y[0] = 0.0
ym[0] = 0.0

# Reference input: step
r = np.ones(N)

for i in range(N-1):
    # Reference model
    ym_dot = -am * ym[i] + bm * r[i]
    ym[i+1] = ym[i] + ym_dot * dt
    
    # Plant (with unknown a, b)
    y_dot = -a_true * y[i] + b_true * u[i]
    y[i+1] = y[i] + y_dot * dt
    
    # Tracking error
    e[i] = y[i] - ym[i]
    
    # MRAC control law
    u[i] = theta1 * r[i] + theta2 * y[i]
    
    # MIT rule: parameter update
    # For u = theta1*r + theta2*y, phi = [r, y]
    theta1_dot = -gamma * e[i] * r[i]
    theta2_dot = -gamma * e[i] * y[i]
    theta1 = theta1 + theta1_dot * dt
    theta2 = theta2 + theta2_dot * dt
    
    theta1_hist[i] = theta1
    theta2_hist[i] = theta2

print(f"\n===== MRAC Results =====")
print(f"Final theta1: {theta1:.3f} (theoretical: {bm/b_true:.3f})")
print(f"Final theta2: {theta2:.3f} (theoretical: {(am - a_true)/b_true:.3f})")
print(f"Final error: {e[-1]:.4f}")

# ===== Plot =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 12: MRAC - Model Reference Adaptive Control', fontsize=14)

ax = axes[0, 0]
ax.plot(t, y, 'b-', lw=2, label='Plant y')
ax.plot(t, ym, 'r--', lw=2, label='Reference ym')
ax.set_xlabel('t (s)')
ax.set_ylabel('y')
ax.set_title('Plant Output vs Reference Model')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(t, e, 'purple', lw=2, label='Error e = y - ym')
ax.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('t (s)')
ax.set_ylabel('Error')
ax.set_title('Tracking Error')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(t, theta1_hist, 'b-', lw=2, label='theta1 (r gain)')
ax.plot(t, theta2_hist, 'orange', lw=2, label='theta2 (y gain)')
ax.axhline(y=bm/b_true, color='blue', ls=':', alpha=0.7, label=f'theta1*={bm/b_true:.2f}')
ax.axhline(y=(am-a_true)/b_true, color='orange', ls=':', alpha=0.7, label=f'theta2*={(am-a_true)/b_true:.2f}')
ax.set_xlabel('t (s)')
ax.set_ylabel('theta')
ax.set_title('Parameter Adaptation')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.plot(t, u, 'green', lw=2, label='Control u')
ax.set_xlabel('t (s)')
ax.set_ylabel('u')
ax.set_title('Control Signal')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:/Users\WUccc/.openclaw/workspace/notes/工程控制论/code/day12_mrac.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")

print("\n" + "=" * 60)
print("MRAC Summary")
print("=" * 60)
print(f"""
MRAC vs Previous Methods:

LQR:        Needs exact A, B matrices
Kalman:     Needs exact A, B, C, Q, R
MRAC:        Learns parameters ONLINE (no prior knowledge)

Key Formula:
  theta_dot = -gamma * e * phi
  (MIT Rule)

Gamma Effect:
  gamma large -> fast adaptation, but risk of oscillations
  gamma small -> stable, but slow convergence
""")
