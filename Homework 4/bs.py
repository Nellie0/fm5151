import numpy as np
from scipy.stats import norm

def BSCall(S, K, q, r, sigma, T):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    d1 = norm.cdf(d1)
    d2 = norm.cdf(d2)
    return round(S * np.exp(-q * T) * d1 - (K * np.exp(-r * T) * d2),2)

def BSPut(S, K, q, r, sigma, T):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    d1 = norm.cdf(-d1)
    d2 = norm.cdf(-d2)
    return round(K * np.exp(-r * T) * d2 - (S* np.exp(-q * T) * d1),2)
    