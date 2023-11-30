from pde import BSM_PDE
import numpy as np

S = 100
K = 102
r = 0.05
q = 0.01
T = 1
sigma = 0.2
M = 100
N = 1000

def test_shape_BSM_PDE():
    assert np.shape(BSM_PDE(S, K, r, q, sigma, T, M, N)[2]) == (N+1, M+1)

def test_element_BSM_PDE():
    assert BSM_PDE(S, K, r, q, sigma, T, M, N)[3] == 0

def test_element_BSM_PDE2():
    assert BSM_PDE(45, 40, r, q, sigma, 5/12, M, N)[3] == 5.33