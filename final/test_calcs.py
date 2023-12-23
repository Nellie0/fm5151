import engine
import api
import models

def test_assumptions():
    assert api.assumptions(1) == models.ProjectionAssumptions(mortality_multiplier = 1.0, wd_age = 65, min_wd_delay = 10)

def test_parameters():
    assert api.parameters(1) == models.ProjectionParameters(proj_periods = 30, num_paths = 1000, seed = 0)

def test_scenario():
    assert api.scenario(1) == models.ScenarioParameters(risk_free_rate = 0.05, dividend_yield = 0.01, volatility = 0.15)

def test_engine():
    assert engine.main(1, 1, 1)