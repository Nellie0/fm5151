from bs import BSCall, BSPut
from bm import bm_european, bm_american

S = 50
K = 70
q = 0.02
r = 0.05
T = 1
sigma = 0.2
n = 10

# 1 Black-Scholes implementation
# b) Unit tests
def test_BSCall1():
    assert BSCall(S, K, q, r, sigma, T) == 0.31

def test_BSPut1():
    assert BSPut(S, K, q, r, sigma, T) == 17.89

def test_BSCall2():
    assert BSCall(40, 30, 0.01, r, sigma, T) == 11.21

def test_BSPut2():
    assert BSPut(40, 30, 0.01, r, sigma, T) == 0.14

# Binomial model implementation
# b) Unit tests
def test_bm_european_call():
    assert bm_european(S, K, q, r, sigma, T, n) == 0.30

def test_bm_european_put():
    assert bm_european(S, K, q, r, sigma, T, n, isCall = False) == 17.88

def test_bm_american_call():
    assert bm_american(S, K, q, r, sigma, T, n) == 0.30

def test_bm_american_put():
    assert bm_american(S, K, q, r, sigma, T, n, isCall = False) == 20