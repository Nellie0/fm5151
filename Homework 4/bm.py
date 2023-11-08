import numpy as np

def CRR(sigma, T, n):
    h = T / n # Number of years divided by number of periods
    u = np.exp(sigma * np.sqrt(h))
    d = np.exp(-sigma * np.sqrt(h))
    return u, d

def probability(q, r, sigma, T, n):
    h = T / n
    u = CRR(sigma, T, n)[0]
    d = CRR(sigma, T, n)[1]
    p = (np.exp((r - q) * h) - d) / (u - d)
    return p

def bm_european(S, K, q, r, sigma, T, n, isCall=True):
    h = T / n
    u = CRR(sigma, T, n)[0]
    d = CRR(sigma, T, n)[1]
    p = probability(q, r, sigma, T, n)
    prices = np.empty(n+1)
    for j in range(n + 1):
        if isCall:
            prices[j] = max(0, S * (u ** (n - j)) * (d ** j) - K)
        else:
            prices[j] = max(0, K - S * (u ** (n - j)) * (d ** j))

    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            prices[j] = np.exp(-r * h) * (p * prices[j] + (1 - p) * prices[j + 1])
    return round(prices[0], 2)

def bm_american(S, K, q, r, sigma, T, n, isCall=True):
    h = T / n
    u = CRR(sigma, T, n)[0]
    d = CRR(sigma, T, n)[1]
    p = probability(q, r, sigma, T, n)
    prices = np.empty(n+1)
    for j in range(n + 1):
        if isCall:
            prices[j] = max(0, S * (u ** (n - j)) * (d ** j) - K)
        else:
            prices[j] = max(0, K - S * (u ** (n - j)) * (d ** j))

    for i in range(n - 1, -1, -1):
        for j in range(i + 1):  
            if isCall:
                early = max(0, S * (u**(i-j) * (d * j) - K)) 
            else:
                early = max(0, K - S *(u ** (i-j)) * (d**j))
            prices[j] = max(early, np.exp(-r * h) * (p * prices[j] + (1 - p) * prices[j + 1]))
    return round(prices[0], 2)