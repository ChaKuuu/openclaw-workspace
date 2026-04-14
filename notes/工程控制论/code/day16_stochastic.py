import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 60)
print("Day 16: Stochastic Processes + Random Control")
print("=" * 60)

# ===== Random Process Basics =====
np.random.seed(42)
T = 10.0
dt = 0.01
N = int(T / dt)
t = np.linspace(0, T, N)

# White noise (idealized)
white = np.random.randn(N)
# Integrated noise (Brownian motion / Wiener process)
brownian = np.cumsum(white) * np.sqrt(dt)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Day 16: Stochastic Processes in Control', fontsize=14)

ax = axes[0, 0]
ax.plot(t, white, 'b-', lw=0.5, alpha=0.7)
ax.set_xlabel('t')
ax.set_ylabel('w(t)')
ax.set_title('White Noise (N(0,1), dt-correlated)')
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.plot(t, brownian, 'r-', lw=1.5)
ax.set_xlabel('t')
ax.set_ylabel('B(t)')
ax.set_title('Brownian Motion / Wiener Process')
ax.grid(True, alpha=0.3)

ax = axes[0, 2]
# Correlation of white noise
corr_white = np.correlate(white[:1000], white[:1000], 'full') / 1000
ax.plot(corr_white[len(corr_white)//2:], 'b-', lw=1)
ax.set_xlabel('Lag')
ax.set_ylabel('Correlation')
ax.set_title('White Noise Autocorrelation (delta function)')
ax.grid(True, alpha=0.3)

# ===== Ornstein-Uhlenbeck Process =====
# dX = -theta*X*dt + sigma*dW
# Mean-reverting process (continuous-time AR(1))
theta, sigma = 0.5, 1.0
X = np.zeros(N)
X[0] = 1.0
dW = np.sqrt(dt) * np.random.randn(N)

for i in range(N-1):
    X[i+1] = X[i] + (-theta * X[i]) * dt + sigma * dW[i]

ax = axes[1, 0]
ax.plot(t, X, 'g-', lw=1.5)
ax.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('t')
ax.set_ylabel('X(t)')
ax.set_title('Ornstein-Uhlenbeck: dX = -0.5*X*dt + dW')
ax.grid(True, alpha=0.3)

# ===== Linear Stochastic System =====
# dx = a*x*dt + b*dW
# Solution: x(t) = x(0)*exp(a*t) + b*integral(exp(a*(t-s))dW)
# Mean: E[x(t)] = x(0)*exp(a*t)
# Var: Var[x(t)] = b^2/(2a)*(exp(2a*t) - 1)

a, b = -0.5, 1.0
x0 = 1.0
n_paths = 100
X_paths = np.zeros((n_paths, N))

for p in range(n_paths):
    X_p = np.zeros(N)
    X_p[0] = x0
    dW_p = np.sqrt(dt) * np.random.randn(N)
    for i in range(N-1):
        X_p[i+1] = X_p[i] + a * X_p[i] * dt + b * dW_p[i]
    X_paths[p] = X_p

mean_x = np.mean(X_paths, axis=0)
var_x = np.var(X_paths, axis=0)
theoretical_mean = x0 * np.exp(a * t)
theoretical_var = (b**2 / (2*a)) * (np.exp(2*a*t) - 1) if a != 0 else b**2 * t

ax = axes[1, 1]
for p in range(10):
    ax.plot(t, X_paths[p], alpha=0.3)
ax.plot(t, mean_x, 'black', lw=2, label='Empirical mean')
ax.plot(t, theoretical_mean, 'r--', lw=2, label='Theoretical mean')
ax.plot(t, mean_x + np.sqrt(var_x), 'b:', lw=2, label='+1 sigma')
ax.plot(t, mean_x - np.sqrt(var_x), 'b:', lw=2, label='-1 sigma')
ax.set_xlabel('t')
ax.set_ylabel('x(t)')
ax.set_title('Linear SDE: dx = -0.5*x*dt + dW (100 paths)')
ax.legend()
ax.grid(True, alpha=0.3)

# ===== Discrete-time Kalman Filter with Random Walk =====
ax = axes[1, 2]
ax.axis('off')
txt = ("""Key Stochastic Concepts:

Wiener Process W(t):
  - W(0) = 0
  - W(t) - W(s) ~ N(0, t-s)
  - Continuous but nowhere differentiable
  - dW ~ N(0, dt)

Itô Calculus:
  - dW^2 = dt
  - dW * dt = 0
  - (dW)^n for n>=3 = 0

Linear SDE: dx = a*x*dt + b*dW
  Solution: x(t) = x(0)*e^(at)
  Mean: E[x(t)] = x(0)*e^(at)
  Var: Var[x(t)] = b^2/(2a)*(e^(2at)-1)

Kalman Filter with noise:
  - Process noise Q -> plant uncertainty
  - Measurement noise R -> sensor quality
  - K_ss = P*C^T / R
  - Large Q -> trust model less -> K larger
  - Large R -> trust sensor less -> K smaller
""")
ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=10,
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.5))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day16_stochastic.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")

# ===== Kalman Filter with Random Disturbance =====
print("\n" + "=" * 60)
print("Kalman Filter: Process Noise + Measurement Noise")
print("=" * 60)
print("""
System:
  x_k+1 = A*x_k + B*u_k + w_k   (w_k ~ N(0, Q))
  y_k = C*x_k + v_k              (v_k ~ N(0, R))

Kalman Gain (steady-state):
  P = A*P*A' + Q - A*P*C'*S^-1*C*P*A + ...  (Riccati)
  K = P*C'*R^-1

Design insight:
  Q large -> plant noise large -> rely less on model -> K larger
  R large -> sensor noise large -> rely less on measurement -> K smaller

This is why Kalman filter is "optimal" - it optimally trades off
between model prediction and actual measurement based on their
relative uncertainty.
""")
