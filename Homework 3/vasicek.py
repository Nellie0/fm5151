import numpy as np
from scipy.stats import norm

# 1 Analytical implementations
# a) Short rate expectation and variance
def determ_rt(a: float, b: float, r0: float, t: int) -> float:
    eat = np.exp(-a * t)
    return r0 * eat + b * (1 - eat)

def  vasicek_rt_mean(a: float, b: float, r0: float, t: float):
    return r0 * np.exp(-a * t) + b * (1 - np.exp(-a * t))

def  vasicek_rt_var(a: float, sigma: float, t: float):
    return (sigma**2 / (2 * a)) * (1 - np.exp(-2 * a * t))

# b) Bonds
def  vasicek_zcb_att(a: float, b: float, sigma: float, t: float, T: float, btt: float):
    return np.exp((((btt - T + t) * (a**2 * b - (sigma**2 / 2))) / (a**2)) 
                  - ((sigma**2 * btt**2) / (4 * a)))

def  vasicek_zcb_btt(a: float, t: float, T: float):
    return (1 / a) * (1 - np.exp(-a * (T - t)))

def  vasicek_zcb(a: float, b: float, sigma: float, rt: float, t: float, T: float):
    B = vasicek_zcb_btt(a, t, T)
    A = vasicek_zcb_att(a, b, sigma, t, T, B)
    return A * np.exp(-B * rt)

# c) Bond options
def  vasicek_sz(a: float, sigma: float, TO: float, TB: float):
    B = vasicek_zcb_btt(a, TO, TB)
    std_dev = vasicek_rt_var(a, sigma, TO)
    return B * np.sqrt(std_dev)

def  vasicek_d1(a: float, b: float, sigma: float, r0: float, K: float, TO: float, TB: float):
    sz = vasicek_sz(a, sigma, TO, TB)
    zcbO = vasicek_zcb(a, b, sigma, r0, 0, TO)
    zcbB = vasicek_zcb(a, b, sigma, r0, 0, TB)
    return (1 / sz) * np.log(zcbB / (K * zcbO)) + (sz / 2)

def  vasicek_d2(a: float, b: float, sigma: float, r0: float, K: float, TO: float, TB: float):
    sz = vasicek_sz(a, sigma, TO, TB)
    d1 = vasicek_d1(a, b, sigma, r0, K, TO, TB)
    return d1 - sz

def  vasicek_zcb_call(a: float, b: float, sigma: float, r0: float, K: float, TO: float, TB: float):
    zcbO = vasicek_zcb(a, b, sigma, r0, 0, TO)
    zcbB = vasicek_zcb(a, b, sigma, r0, 0, TB)
    d1 = vasicek_d1(a, b, sigma, r0, K, TO, TB)
    d2 = vasicek_d2(a, b, sigma, r0, K, TO, TB)
    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)
    return (zcbB * Nd1) - (K * zcbO * Nd2)

def  vasicek_zcb_put(a: float, b: float, sigma: float, r0: float, K: float, TO: float, TB: float):
    zcbO = vasicek_zcb(a, b, sigma, r0, 0, TO)
    zcbB = vasicek_zcb(a, b, sigma, r0, 0, TB)
    d1 = vasicek_d1(a, b, sigma, r0, K, TO, TB)
    d2 = vasicek_d2(a, b, sigma, r0, K, TO, TB)
    Nd1 = norm.cdf(-d1)
    Nd2 = norm.cdf(-d2)
    return (K * zcbO * Nd2) - (zcbB * Nd1)

# 2 Short rate simulation
# a) Implementation

def determ_approx_rts(a: float, b: float, sigma: float, r0: float, T: float, n: int):
    epsilon = np.random.standard_normal(size = T)
    h = T / n
    rts = np.empty(n + 1)
    rts[0] = r0
    for i in range(1,n+1):
        rts[i] = rts[i-1] + (a * (b - rts[i-1]) * h) + (sigma * epsilon[i-1] * np.sqrt(h))
    return rts

# Pricing instruments
# a) Reprice zero coupon bonds

def determ_approx_rts_integral(rts: np.ndarray, t: float, T: float, h: float):
    start = int(round(t / h, 0))
    end = int(round(T / h, 0))
    return np.sum(rts[start : end]) * h

def determ_approx_zcb(a: float, b: float, sigma: float, r0: float, t: int, T: int, n: int):
    rts = determ_approx_rts(a, b, sigma, r0, T, n)
    rtssum = determ_approx_rts_integral(rts, t, T, T / n)
    return np.exp(-rtssum)

# b) Reprice call and put options

def determ_approx_option(rts, t, T, h, Vt):
    return np.mean(np.exp(-determ_approx_rts_integral(rts, t, T, h)) * Vt)