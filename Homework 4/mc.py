import numpy as np

def mc(S, K, q, r, sigma, T, n, Call = True, Antithetic = False):
    sim = np.random.standard_normal(n)
    if Antithetic:
        sim = np.concatenate((sim, -sim))
    ST = [S * np.exp((r - q - (0.5 * sigma**2)) * T + (sigma * np.sqrt(T) * x)) for x in sim]
    if Call:
        payoff = [max(Si - K, 0) for Si in ST]
    else:
        payoff = [max(K - Si,0) for Si in ST]
    return np.mean(payoff) * np.exp(-r * T), np.sqrt(np.var(payoff) / n)