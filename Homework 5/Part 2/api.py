import numpy as np
import pandas as pd
import yfinance as yf
import uvicorn
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from scipy.stats import norm
from bs import BSCall, BSPut
import nest_asyncio

nest_asyncio.apply()
app = FastAPI()

class OptionParams(BaseModel):
    ticker: str
    K: float
    r: float
    q: float
    sigma: float
    T: float
    isCall: bool

def get_returns(ticker: str, range: Optional[str] = None, interval: Optional[str] = None) -> pd.Series:
    try:
        stock = yf.Ticker(ticker)
        data = stock.info('currentPrice')
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting stock price: {str(e)}")

def BS(params: OptionParams):
    # parameters for easy access
    S = get_returns(params.ticker)
    K = params.K
    r = params.r
    q = params.q
    sigma = params.sigma
    T = params.T
    isCall = params.isCall

    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Getting BS Option Price
    if isCall == True:
        oPrice = BSCall(S, K, r, q, sigma, T)
    elif isCall == False:
        oPrice == BSPut(S, K, r, q, sigma, T)
    else:
        raise ValueError("Invalid option type. True for Call, False for Put")
    
    # Greeks
    delta = norm.cdf(d1) if isCall ==  True else -norm.cdf(-d1)
    theta = (-S * sigma * norm.cdf(d1)) / (2 * np.sqrt(T)) - (r - q) * K * np.exp(-(r - q) *T) * norm.cdf(d2) if isCall == True else (-S * sigma * norm.cdf(d1)) / (2 * np.sqrt(T)) + (r - q) * K * np.exp(-(r - q) *T) * norm.cdf(-d2)
    rho = K * T * np.exp(-(r - q) * T) * norm.cdf(d2) if isCall == True else -K * T * np.exp(-(r - q) * T) * norm.cdf(-d2)
    vega = S * norm.cdf(d1) * np.sqrt(T)
    gamma = norm.cdf(d1) / (S * sigma * np.sqrt(T))

    # Print
    return 2

@app.get("/hw5/black-scholes/{ticker}")
def calculate_black_scholes(params:OptionParams):
    try:
        result = BS(params)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)