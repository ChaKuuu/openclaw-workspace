import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Day 27: Particle Filter")
np.random.seed(42)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 27: Particle Filter', fontsize=14)

T = 5.0
dt = 0.05
N_steps = int(T/dt)
t = np.linspace(0, T, N_steps)
x_true = np.zeros(N_steps)
x_true[0] = 0.0
for i in range(N_steps-1):
    x_true[i+1] = x_true[i] + 0.05 * np.random.randn()
y_meas = x_true**2 / 20 + 0.1 * np.random.randn(N_steps)

N_particles = 500
particles = np.zeros((N_steps, N_particles))
weights = np.zeros((N_steps, N_particles))
x_est = np.zeros(N_steps)
std_est = np.zeros(N_steps)

particles[0] = np.random.randn(N_particles) * 0.5
weights[0] = np.ones(N_particles) / N_particles
x_est[0] = np.mean(particles[0])

for k in range(1, N_steps):
    particles[k] = particles[k-1] + 0.05 * np.random.randn(N_particles)
    sigma_v = 0.1
    residuals = y_meas[k] - particles[k]**2/20
    likelihood = np.exp(-residuals**2 / (2 * sigma_v**2))
    weights[k] = likelihood * weights[k-1]
    wsum = np.sum(weights[k])
    if wsum > 0:
        weights[k] /= wsum
    x_est[k] = np.sum(weights[k] * particles[k])
    var_est = np.sum(weights[k] * (particles[k] - x_est[k])**2)
    std_est[k] = np.sqrt(var_est)
    ess = 1.0 / np.sum(weights[k]**2) if np.sum(weights[k]**2) > 0 else N_particles
    if ess < N_particles/2:
        cumsum = np.cumsum(weights[k])
        cumsum[-1] = 1.0
        uu = np.random.rand(N_particles) / N_particles
        idx = np.arange(N_particles) / N_particles
        resample_idx = np.searchsorted(cumsum, uu + idx)
        particles[k] = particles[k, resample_idx]
        weights[k] = np.ones(N_particles) / N_particles

ax = axes[0, 0]
ax.plot(t, x_true, 'b-', lw=2, label='True state')
ax.plot(t, x_est, 'orange', lw=2, label='PF estimate')
ax.fill_between(t, x_est - 2*std_est, x_est + 2*std_est, alpha=0.2, color='orange')
ax.set_xlabel('t (s)')
ax.set_ylabel('x')
ax.set_title('Particle Filter: Nonlinear Tracking')
ax.legend()
ax.grid(True, alpha=0.3)

x_ekf = np.zeros(N_steps)
P_ekf = np.zeros(N_steps)
x_ekf[0] = 0.0
P_ekf[0] = 0.25
Q = 0.05**2
R = 0.1**2
for k in range(1, N_steps):
    P_pred = P_ekf[k-1] + Q
    H = max(0.01, x_ekf[k-1] / 10)
    S = H * P_pred * H + R
    K = P_pred * H / S if S > 0 else 0
    x_ekf[k] = x_ekf[k-1] + K * (y_meas[k] - x_ekf[k-1]**2/20)
    P_ekf[k] = (1 - K*H) * P_pred

ax = axes[0, 1]
ax.plot(t, x_true, 'b-', lw=2, label='True')
ax.plot(t, x_est, 'orange', lw=2, label='PF')
ax.plot(t, x_ekf, 'green', lw=2, alpha=0.7, label='EKF')
ax.set_xlabel('t (s)')
ax.set_ylabel('x')
ax.set_title('PF vs EKF (Nonlinear)')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.plot(t, std_est, 'orange', lw=2, label='PF std')
ax.plot(t, 2*np.sqrt(P_ekf), 'green', lw=2, alpha=0.7, label='EKF std')
ax.set_xlabel('t (s)')
ax.set_ylabel('Uncertainty')
ax.set_title('Estimated Uncertainty')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
ax.text(0.05, 0.95,
    "Particle Filter (Sequential Monte Carlo):\n\n"
    "Algorithm:\n"
    "  1. Predict: x_k ~ p(x_k | x_{k-1})\n"
    "  2. Weight: w_k ~ p(y_k | x_k)\n"
    "  3. Resample when ESS < threshold\n\n"
    "Key Properties:\n"
    "  - Nonparametric: no Gaussian needed\n"
    "  - Handles ANY nonlinearity\n"
    "  - Monte Carlo: N particles -> accuracy\n"
    "  - Complexity: O(N) per step\n\n"
    "vs Kalman Filter:\n"
    "  KF: Linear + Gaussian only\n"
    "  EKF: Linearizes (Jacobian)\n"
    "  PF: No approximation needed\n\n"
    "Effective Sample Size:\n"
    "  ESS = 1/sum(w_i^2)\n"
    "  ESS < N/2 -> resample\n\n"
    "Applications:\n"
    "  - Robot localization (SLAM)\n"
    "  - Target tracking\n"
    "  - Nonlinear/non-Gaussian systems",
    transform=ax.transAxes, va='top', fontsize=11,
    fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day27_particle.png', dpi=150, bbox_inches='tight')
print("Figure saved!")
