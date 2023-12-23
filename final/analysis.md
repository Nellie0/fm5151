1. I'm not sure if the GMWB is fairly priced. I think so.
2.
  a) The lower the fee rate, the higher the cost. This is due to multiple reasons, but mainly the ending:

      dpv_wd_claims = np.sum(wd_claim * discount * prob_surv)
      dpv_fees = np.sum(fee * discount * prob_surv)
      cost = np.mean(dpv_wd_claims) - np.mean(dpv_fees)

which suggests that the higher the fee, the lower the cost since dpv_fees is being subtracted.
  b) The higher the guarantee withdrawal rate, the higher the withdrawal amount. This means that the withdrawal claim will be higher, and thus, the cost will also be higher.
  
  c) Volatility is used in 

      av_after_return[t] = av_after_fee[t] * np.exp(risk_free_rate - dividend_yield - 0.5 * volatility**2) + volatility * np.random.standard_normal()

which means that the higher the volatility, the higher the account value after return. Thus, the account value after withdrawal is higher, which lowers the withdrawal claim. This means that in fact, the cost is lower when volatility is higher.
  
  d) Mortality multiplier affects the probability of survival, which innately increases the dpv_fees. Thus, the cost goes higher as the mortality multiplier goes higher.
  
  e) If the withdrawal age is not low enough, then the policyholder cannot withdraw. In other words, wd_amount = 0, and so the cost is equal to zero. If the withdrawal age is too low, then the other factor to consider is the minimum withdrawal delay.
  
  f) If the minimum withdrawal delay is too low, then the duration of the policy does not have to be high for the withdrawal amount to go higher than zero. This means that the policy cost increases as the min_wd_delay increases.
