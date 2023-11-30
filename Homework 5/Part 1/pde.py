import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded

def BSM_PDE(S0, K, r, q, sigma, T, M, N, isEuropean=True):
    S_max = 3 * K
    S_min = K / 3
    dt = T / N

    # Create grid
    S_val = np.linspace(S_min, S_max, M+1)
    t = np.linspace(0, T, N+1)
    V = np.zeros((N+1, M+1))

    # Boundary condition
    V[0,:] = np.maximum(S_val - K, 0)

    # Coefficients
    a = 0.5 * dt * ((r-q) * np.arange(M+1) - sigma**2 * np.arange(M+1)**2)
    b = 1 + dt * (sigma**2 * np.arange(M+1)**2 + (r-q))
    c = -0.5 * dt * ((r-q) * np.arange(M+1) + sigma**2 * np.arange(M+1)**2)

    # Ensure non-singularity by adding a small positive term to the diagonal
    epsilon = 1e-8
    b[1:M] += epsilon

    # Loop over time
    for i in range(1, N+1):
        # RHS of the linear system
        rhs = V[i-1, 1:M] + c[1:M] * V[i-1, 0:M-1] + b[1:M] * V[i-1, 1:M] + a[1:M] * V[i-1, 2:M+1]

        # Solve the linear system using solve_banded
        A = np.vstack([c[1:M], b[1:M], a[1:M]])
        V[i, 1:M] = solve_banded((1, 1), A, rhs)

        # Further boundary conditions
        if isEuropean == True:
            V[i, 0] = 0
        elif isEuropean == False:
            V[i, 0] = max(S_val[0] - K, 0)
        V[i, M] = (S_max - K) * np.exp(-r * t[i])

    oPrice = V[0, np.searchsorted(S_val, S0)]

    return S_val, t, V, np.round(oPrice,2)