import numpy as np
from scipy.linalg import solve_triangular

# 1. Rate helper implementations
# Convert a continuous rate to annual rate
def continuous_to_annual(r: float):
    i = np.exp(r) - 1
    return i

# Convert an annual rate to a continuous rate
def annual_to_continuous(i: float):
    r = np.log(1+i)
    return r

# Convert an annual rate to a mthly compounded rate
def annual_to_mthly(i: float, m: int):
    i_m = m * ((1 + i) ** (1/m) - 1)
    return i_m

#Convert a mthly compounded rate to annual
def mthly_to_annual(i_m: float, m: int):
    i = (i_m/m +1)**m + 1
    return i

# Converts discount factor (zero coupon bond) to continuous rate
def  zcb_to_continuous(z: float, t: float):
    r = (-1*np.log(z)) / t
    return r

# Converts continuous rate to discount factor (zero coupon bond)
def continuous_to_zcb(r: float, t: float):
    z = np.exp(-1*r*t)
    return z

# 2. Bootstrap function
# par_yields – A set of par yields
# tenors – Tenor year fractions associated with the par yield
# Returns a tuple containing the spot discount curve at half-year intervals in the first element, and the half-year tenor fractions in the second element
def bootstrap(par_yields: 'np.ndarray', tenors: 'np.ndarray'):
    tenors_inter = np.linspace(0.5, tenors[-1], int(tenors[-1]) * 2) #Create equally spaced tenors
    coupon_rates_interp = np.interp(tenors_inter, tenors, par_yields) / 100 #Interpolate for coupon rates
    coupon_rates_interp = coupon_rates_interp * np.ones((len(coupon_rates_interp),len(coupon_rates_interp))) #Broadcast to size of coupon_rates_interp
    coupon_rates_interp = np.transpose(coupon_rates_interp) #Transpose to make rows have same value
    coupon_rates_interp = np.tril(coupon_rates_interp) #Create a lower triangular matrix
    np.fill_diagonal(coupon_rates_interp, coupon_rates_interp.diagonal() + 1) #Each diagonal should start with 1
    id = np.ones(len(coupon_rates_interp)) #The right hand side of Cz = id
    z = solve_triangular(coupon_rates_interp, id,lower=True) #Find z from Cz = id
    return z

# 3. Zero bond / discount factor function
# implement a function that will allow you to get the discount factor for any time on the discount curve. 
# Takes in a time t and bootstrapped curve, curve, and returns a discount factor . If is not a provided tenor, the rate is linearly interpolated between the neighboring points.
def zcb(t:float, curve: 'tuple[np.ndarray, np.ndarray]'):
    z = curve[t]
    return z

# 4. Annuity function
# implement a function that will allow you to calculate the present value of an annuity at effective rate per period, i.
# Returns the present value of an annuity of n payments at effective yield i
def annuity(n: int, i: float):
    v = 1 / (1+i)
    A = (1 - v**n) / i
    return A