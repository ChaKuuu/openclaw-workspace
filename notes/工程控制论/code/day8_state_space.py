import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal, linalg

print("=" * 60)
print("Day 8: State Space + State Feedback")
print("=" * 60)

# ===== Plant: G(s) = 2/(s^2+3s+2) =====
A = np.array([[0, 1], [-2, -3]], dtype=float)
B = np.array([[0], [2]], dtype=float)
C = np.array([[1, 0]], dtype=float)
D = np.array([[0]], dtype=float)

print("\nPlant: G(s) = 2/(s^2+3s+2)")
print("State-space: x_dot = A*x + B*u")

lam = linalg.eigvals(A)
print(f"\nOL poles: {lam.real}")
print(f"Controllable: {np.linalg.matrix_rank(np.hstack([B, A@B])) == 2}")
print(f"Observable: {np.linalg.matrix_rank(np.vstack([C, C@A])) == 2}")

# ===== Pole Placement =====
desired = np.array([-3.0, -5.0])
result = signal.place_poles(A, B, desired)
K = result.gain_matrix
A_cl = A - B @ K
lam_cl = linalg.eigvals(A_cl)
print(f"\nState Feedback K: {K.flatten()}")
print(f"CL poles: {lam_cl.real}")

# ===== Step Response =====
t = np.linspace(0, 5, 500)
sys_ol = signal.TransferFunction([2], [1, 3, 2])
_, y_ol = signal.step(sys_ol, T=t)

# Closed-loop simulation
sys_cl = signal.StateSpace(A_cl, B, C, D)
_, y_cl_vec, _ = signal.lsim(sys_cl, U=np.ones_like(t), T=t, X0=np.zeros(2))
y_cl = y_cl_vec

# ===== Plot =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Day 8: State Space + Pole Placement', fontsize=14)

ax = axes[0, 0]
ax.plot(t, y_ol, 'b-', lw=2, label='Open Loop')
ax.plot(t, y_cl, 'g-', lw=2, label='Closed Loop (K feedback)')
ax.axhline(y=1, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('t (s)')
ax.set_ylabel('y(t)')
ax.set_title('Step Response: OL vs CL')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 5)
ax.set_ylim(0, 2.5)

ax = axes[0, 1]
ax.scatter(lam.real, lam.imag, marker='o', s=120, color='blue', zorder=5, label=f'OL: {lam.real}')
ax.scatter(lam_cl.real, lam_cl.imag, marker='x', s=150, lw=3, color='red', zorder=5, label=f'CL: {lam_cl.real.round(1)}')
ax.axvline(x=0, color='gray', ls='--', alpha=0.5)
ax.axhline(y=0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_title('Pole Map')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

ax = axes[1, 0]
ax.plot(t, y_cl, 'g-', lw=2, label='CL Response')
ax.axhline(y=1, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('t (s)')
ax.set_ylabel('y(t)')
ax.set_title('Closed-Loop Step Response')
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
ax.axis('off')
txt = ("State Space:\n"
       "  x_dot = A*x + B*u\n"
       "  A = [[0,1],[-2,-3]]\n"
       "  B = [[0],[2]]\n\n"
       f"OL poles: {lam.real}\n"
       f"CL poles: {lam_cl.real.round(1)}\n\n"
       f"Feedback K: {K.flatten()}\n"
       "-> Poles moved faster")
ax.text(0.1, 0.9, txt, transform=ax.transAxes, va='top', fontsize=11, fontfamily='monospace')
ax.set_title('Summary')

plt.tight_layout()
plt.savefig('C:/Users/WUccc/.openclaw/workspace/notes/工程控制论/code/day8_state_feedback.png', dpi=150, bbox_inches='tight')
print("\nFigure saved!")
