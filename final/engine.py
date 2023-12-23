"""Your pricing engine implementation"""

import requests
import json
from fastapi import FastAPI
import numpy as np
from typing import Optional

app = FastAPI()

@app.get("/engine")
def main(assumption_id: int, parameter_id: int, scenario_id: int, policy_id: Optional[int] = None):
    # Request for the models from api
    assumption = json.dumps(requests.get("http://localhost:8000/assumptions/{id}", params = {"id": assumption_id}))
    parameter = json.dumps(requests.get("http://localhost:8000/parameters/{id}", params = {"id": parameter_id}))
    scenario = json.dumps(requests.get("http://localhost:8000/scenarios/{id}", params = {"id": scenario_id}))
    policy = json.dumps(requests.get("http://localhost:8000/policies/{id}", params = {"id": policy_id}))
    mortality = json.dumps(requests.get("http://localhost:8000/mortality/{id}"))

    # Define variables from models
    mortality_multiplier = "mortality_multiplier" in assumption
    wd_age = "wd_age" in assumption
    min_wd_delay = "min_wd_delay" in assumption
    proj_periods = "proj_periods" in parameter
    num_paths = "num_paths" in parameter
    risk_free_rate = "risk_free_rate" in scenario
    dividend_yield = "dividend_yield" in scenario
    volatility = "volatility" in scenario
    issue_age = "issue_age" in policy
    initial_premium = "initial_premium" in policy
    fee_pct_av = "fee_pct_av" in policy
    benefit_type = "benefit_type" in policy
    ratchet_type = "ratchet_type" in policy
    guarantee_wd_rate = "guarantee_wd_Rate" in policy
    qx = np.asarray("qx" in mortality)

    # Defining independent vectors
    age = np.arange(issue_age, 116)
    duration = np.arange(proj_periods + 1)
    prob_surv = np.zeros(num_paths)
    prob_surv[0] = 1
    for i in age:
        prob_surv[i] = prob_surv[i-1] * (1 - qx[i] * mortality_multiplier)
    discount = np.exp(-risk_free_rate * duration)

    # Beginning the engine
    av_end_of_period = benefit_base = remaining_principal = np.zeros(num_paths)
    av_beg_of_period = av_after_return = av_after_fee = fee = av_after_wd = wd_claim = np.zeros(num_paths)
    for i in range(1, num_paths + 1):
        # Initialization
        av_end_of_period[0] = remaining_principal[0] = initial_premium
        benefit_base[i] = initial_premium

        for t in range(1, proj_periods):
            av_beg_of_period[t] = av_end_of_period[t-1]
            fee[t] = av_beg_of_period[t] * fee_pct_av
            av_after_fee[t] = av_beg_of_period[t] - fee[t]
            av_after_return[t] = av_after_fee[t] * np.exp(risk_free_rate - dividend_yield - 0.5 * volatility**2) + volatility * np.random.standard_normal()
            wd_amount = 0
            if (age[t] > wd_age) and (duration[t] > min_wd_delay):
                if benefit_type == "FOR_LIFE":
                    wd_amount = benefit_base[t] * guarantee_wd_rate
                elif benefit_type == "PRINCIPAL_BACK":
                    wd_amount = min(benefit_base[t] * guarantee_wd_rate, max(remaining_principal[t], av_after_return[t]))
            remaining_principal[t] = remaining_principal[t-1] - wd_amount
            av_after_wd[t] = av_after_return[t] - wd_amount
            wd_claim[t] = max(wd_amount - av_after_wd[t], 0)

    dpv_wd_claims = np.sum(wd_claim * discount * prob_surv)
    dpv_fees = np.sum(fee * discount * prob_surv)
    cost = np.mean(dpv_wd_claims) - np.mean(dpv_fees)

    return cost

if __name__ == "__main__":
    main()