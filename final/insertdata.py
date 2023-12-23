"""Your implementation for inserting db/*.csv files into the MySQL database"""

import pandas as pd

assumptions = pd.read_csv('db/assumptions.csv')
mortality = pd.read_csv('db/mortality.csv')
parameters = pd.read_csv('db/parameters.csv')
policies = pd.read_csv('db/policies.csv')
scenarios = pd.read_csv('db/scenarios.csv')