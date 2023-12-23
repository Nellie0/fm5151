"""
API Routes for Zen Nilpferd
"""
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from mysql.connector import MySQLConnection

import insertdata

import models

app = FastAPI()


class BasicChecksMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, conn: MySQLConnection):
        super().__init__(app)
        self._conn = conn

    async def dispatch(self, request, call_next):
        if not self._conn.is_connected():
            try:
                # We expect the environment variable MYSQL_HOST will to be
                # present if we're running within a container.
                host = os.environ.get("MYSQL_HOST", "127.0.0.1")
                # Port is always the within container network default port, even
                # if another, e.g. 3307, is exposed to the Docker host.
                port = 3306
                print(f"Connecting to host '{host}', port '{port}'")
                self._conn.connect(host=host, port=port, user="root")
            except Exception as e:
                return JSONResponse(
                    status_code=503, content=f"Database unavailable: {e}"
                )

        result = await call_next(request)
        # ensure we commit each time to avoid select statement caching
        self._conn.commit()
        return result


conn: MySQLConnection = MySQLConnection()
middleware = [Middleware(BasicChecksMiddleware, conn=conn)]
app = FastAPI(title="Zen Nilpferd's Quant API", version="0.0.1", middleware=middleware)

# ==========================================================================
#                            YOUR IMPLEMENTATION
#                               BELOW HERE!!!
# NOTES:
#   - Use the global `conn` variable for the MySQL connection
# ==========================================================================


@app.get("/")
def root():
    if conn.is_connected():
        return "All is well!"

@app.get("/assumptions/{id}")
def assumptions(id: int) -> models.ProjectionAssumptions:
    # Your implementation here
    cursor = conn.cursor()
    query = ("SELECT * FROM zen_nilpferd.assumptions WHERE id = %s;") 
    # I am not too sure if I can call straight from zen_nilpferd, or if I must use insertdata.py. Both return "Not Found" when going to http://127.0.0.1:8000/assumption/1
    result = cursor.execute(query, id).fetchall()

    # Defining individual variables from result
    mortality_multiplier = "mortality_multiplier" in result
    wd_age = "wd_age" in result
    min_wd_delay = "min_wd_delay" in result

    # This is my attempt at instead using a dictionary. However, I still continue to get "Not Found" when going to 127.0.0.1:8000/assumption/1
    dict = {}
    dict["mortality_multiplier"] = cursor.execute("SELECT mortality_multiplier FROM zen_nilpferd.assumptions")
    dict["wd_age"] = cursor.execute("SELECT wd_age FROM zen_nilpferd.assumptions")
    dict["min_wd_delay"] = cursor.execute("SELECT min_wd_delay FROM zen_nilpferd.assumptions")

    if id not in result:
        raise HTTPException(status_code = 404, detail = "ID not found")

    return models.ProjectionAssumptions(**dict)


@app.get("/parameters/{id}")
def parameters(id: int) -> models.ProjectionParameters:
    # Your implementation here
    cursor = conn.cursor()
    query = ("SELECT * FROM parameters = %s WHERE id = %s;")
    result = cursor.execute(query, (insertdata.parameters, id)).fetchall()

    # Defining individual variables from result
    proj_periods = "proj_periods" in result
    num_paths = "num_paths" in result
    seed = "seed" in result

    if id not in result:
        raise HTTPException(status_code = 404, detail = "ID not found")

    return models.ProjectionParameters(proj_periods = proj_periods, num_paths = num_paths, seed = seed)


@app.get("/policies")
def policies(id: Optional[int] = None) -> list[models.PolicyholderRecord]:
    # Your implementation here
    cursor = conn.cursor()
    query = ("SELECT * FROM policies = %s WHERE id = %s;")
    result = cursor.execute(query, (insertdata.policies, id)).fetchall()

    # Defining individual variables from result
    issue_age = "issue_age" in result
    initial_premium = "initial_premium" in result
    fee_pct_av = "fee_pct_av" in result
    benefit_type = "benefit_type" in result
    ratchet_type = "ratchet_type" in result
    guarantee_wd_rate = "guarantee_wd_rate" in result

    if (id not in result) or (id == None):
        return None

    return models.PolicyholderRecord(id = id, issue_age = issue_age, initial_premium = initial_premium, fee_pct_av = fee_pct_av, benefit_type = benefit_type, ratchet_type = ratchet_type, guarantee_wd_rate = guarantee_wd_rate)


@app.get("/scenario/{id}")
def scenario(id: int) -> models.ScenarioParameters:
    # Your implementation here
    cursor = conn.cursor()
    query = ("SELECT * FROM scenario = %s WHERE id = %s;")
    result = cursor.execute(query, (insertdata.scenarios, id)).fetchall()

    # Defining individual variables from result
    risk_free_rate = "risk_free_rate" in result
    dividend_yield = "dividend_yield" in result
    volatility = "volatility" in result

    if id not in result:
        raise HTTPException(status_code = 404, detail = "ID not found")

    return models.ScenarioParameters(risk_free_rate = risk_free_rate, dividend_yield = dividend_yield, volatility = volatility)

@app.get("/mortality")
def mortality() -> models.MortalityTable:
    # Your implementation here
    cursor = conn.cursor()
    query = ("SELECT * FROM mortality = %s WHERE id = %s;")
    result = cursor.execute(query, (insertdata.query, id)).fetchall()

    # Defining individual variables from result
    qx = "qx" in result

    return models.MortalityTable(qx = qx)