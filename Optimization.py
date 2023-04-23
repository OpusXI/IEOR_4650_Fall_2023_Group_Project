import pandas as pd
from numpy import mean
import numpy as np

import scipy.stats as stats
# from featurewiz import FeatureWiz

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LassoCV, Lasso
# from lazypredict.Supervised import LazyRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from gurobipy import Model, GRB, quicksum, max_

forwardCluster = pd.read_csv('./data/players/forward_cluster.csv')
midfielderCluster = pd.read_csv('./data/players/midfielder_cluster.csv')
defenderCluster = pd.read_csv('./data/players/defender_cluster.csv')
goalkeeperCluster = pd.read_csv('./data/players/goalkeeper_cluster.csv')

totalFrame = pd.concat([forwardCluster, midfielderCluster, defenderCluster, goalkeeperCluster])

def team_builder(df, budget, num_gk, num_def, num_mid, num_for):
    try:
        indices = df['full_name']
        perf = dict(zip(indices,df['performance']))
        salary = dict(zip(indices,df['salary']))
        player_position = list(zip(df['full_name'],df['position']))

        # Create the model
        m = Model()

        # Create the decision variables
        x = m.addVars(df['full_name'], vtype=GRB.BINARY, name="x")

        # Set the objective function
        m.setObjective(quicksum(perf[i]*x[i] for i in indices), GRB.MAXIMIZE)

        # Add the constraints
        m.addConstr(quicksum(salary[i]*x[i] for i in indices) <= budget, name='salary')

        m.addConstr(quicksum([x[i] for i, position in player_position if position=='Goalkeeper'])== num_gk)

        m.addConstr(quicksum([x[i] for i, position in player_position if position=='Defender'])== num_def)

        m.addConstr(quicksum([x[i] for i, position in player_position if position=='Midfielder']) == num_mid)

        m.addConstr(quicksum([x[i] for i, position in player_position if position=='Forward']) == num_for)


        # Solve the model
        m.optimize()

        selected_indices = [v.index for v in m.getVars() if v.x > 1e-6]
        r = df.iloc[selected_indices][['full_name','position', 'salary']]
        team_stats = r[['full_name','position','salary']]
        
        return team_stats
    except AttributeError:
        return "There are no teams that meet the budget."


team = team_builder(totalFrame, 1000, 1, 4, 4, 2)
print(team)
