pde.py contains a Black-Scholes-Merton PDE calculator. It requires the following variables:
  S0: The current underlying stock price
  K: The strike price
  r: The risk-free rate (as decimal)
  q: The dividend (as decimal). Enter 0 if there it's not a dividend-paying stock.
  T: The maturity out of 12 months (if it's one year, enter 1. if it's 6 months, enter 6/12).
  N: The number of time changes
  M: The number of stock price changes
  isEuropean: True for European options, False for American Options

Using the calculator has four options (in all cases, you should insert your desired variables):
  1. Do BSM_PDE(S0, K, r, q, T, M, N, isEuropean)[3] to find the current option price.
  2. Do BSM_PDE(S0, K, r, q, T, M, N, isEuropean)[2] to see the matrix of option prices.
  3. Do BSM_PDE(S0, K, r, q, T, M, N, isEuropean)[1] to see the time values used.
  4. Do BSM_PDE(S0, K, r, q, T, M, N, isEuropean)[0] to see the stock prices used.

For example, if I want to find a current stock price for a European stock, and I know that S0=100, K=102, r=0.05, q=0.01, T=1, M=100, N=100, then I can do

  BSM_PDE(100, 102, 0.05, 0.01, 1, 100, 100)[3]

Do note that if you're not sure of the values of M or N, you can use M=N=1000.
