# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:24:52 2023

@author: louis
"""

import pandas as pd
from numpy import mean
import numpy as np

import scipy.stats as stats
from featurewiz import FeatureWiz

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LassoCV, Lasso
from lazypredict.Supervised import LazyRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

### DATA CLEANING AND PREPRING ###
players = pd.read_csv("data\players\england-premier-league-players-2017-to-2022-stats.csv")
players = pd.concat([players[players['Season']=='2020-2021'],
                    players[players['Season']=='2021-2022']],axis=0)
players = players[players['appearances_overall']>0]
  
    
cols_to_drop = ['Season','shirt_number','full_name','age','birthday',
                'birthday_GMT','league','season','Current Club',
                'minutes_played_overall','minutes_played_home',
                'minutes_played_away','nationality','appearances_overall',
                'appearances_home','appearances_away']

players = players.drop(cols_to_drop,axis=1)

outfield_players = players[players['position'] != 'Goalkeeper']
goalkeepers = players[players['position'] == 'Goalkeeper']

attack_players = pd.concat([players[players['position'] == 'Foward'],
                    players[players['position'] == 'Midfielder']],axis=0)
defence_players = pd.concat([players[players['position'] == 'Midfielder'],
                    players[players['position'] == 'Defender']],axis=0)

for i in range(len(players.columns)):
    print(players.columns[i])

def extra_cleaning(X):
    # Dropping columns with NA values
    X = X.dropna(axis=1)
    
    # Checking if there is any negative values that may crash featurewiz
    more_cols_to_drop = (X<0).any()[(X<0).any()==True].index.tolist()
    X = X.drop(more_cols_to_drop,axis=1)
    
    # Checking if there is columns with only 0 that may crash featurewiz; 
    # make sure to export to csv the columns you are going to delete to check
    more_cols_to_drop = (X==0).all()[(X==0).all()==True].index.tolist()
    X = X.drop(more_cols_to_drop,axis=1)
    
    return X

### ANALYZING WHAT CONTRIBUTES TO GOALS (ATTACKING PLAYERS)###

cols_to_drop = ['position','goals_overall','goals_home','goals_away',
                'penalty_goals', 'penalty_misses', 'goals_per_90_overall',
                'goals_per_90_home', 'goals_per_90_away','min_per_goal_overall',
                'hattricks_total_overall','two_goals_in_a_game_total_overall',
                'three_goals_in_a_game_total_overall',
                'two_goals_in_a_game_percentage_overall',
                'three_goals_in_a_game_percentage_overall',
                'goals_involved_per90_percentile_overall',
                'goals_per90_percentile_overall', 'goals_per90_percentile_away',
                'goals_per90_percentile_home','man_of_the_match_total_overall',
                'annual_salary_eur','annual_salary_eur_percentile', 
                'annual_salary_gbp','annual_salary_usd','rank_in_league_top_attackers',
                'rank_in_league_top_midfielders','rank_in_club_top_scorer',
                'sm_goals_scored_total_overall', 'xg_per_90_overall',
                'xg_per_game_overall','xg_per90_percentile_overall',
                'goals_involved_per_90_overall', 'xg_total_overall']      ## SHOULD I INCLUDE xg_total_overall

## Need to cast target variable to float so that featurewize know it is regression.
X, y = attack_players.drop(cols_to_drop,axis=1), attack_players['goals_overall'].astype('float')

# DROPPING ROW 2323 (LITTLE WIERD)
X = X.drop(index=X.loc[2323].name)
y = y.drop(2323)

X = extra_cleaning(X)

### FEATURE SELECTION ###
features = FeatureWiz(corr_limit=0.70, feature_engg='', category_encoders='', 
                      dask_xgboost_flag=False, nrows=None, verbose=2)

X_train_selected = features.fit_transform(X, y)

### LINEAR REGRESSION ###
### Quick test of the usefulness of the features selected by featurewiz
def train(data, target):
    X_train, X_test,y_train, y_test = train_test_split(data, target, test_size=.2, random_state=42)# fit all models
    reg = LazyRegressor(predictions=True)
    models, predictions = reg.fit(X_train, X_test, y_train, y_test)
    
    return models

print(train(X_train_selected,y))

### Linear Regression on selected features

def lasso_reg_output(X,y):
    
    col_names = X.columns
    X = StandardScaler().fit_transform(X)
    lasso_CV = LassoCV(cv=5)
    lasso_CV.fit(X,y)
    
    model = Lasso(alpha=lasso_CV.alpha_)
    model.fit(X,y)

    output = {
        'Features':col_names,
        'Coef':model.coef_}
    
    return pd.DataFrame(output)

X_selected = X_train_selected

linear_model = lasso_reg_output(X_selected,y)
linear_model = linear_model.sort_values('Coef')

print(linear_model)

# If expected goal is not used then shot_conversion_rate_overall and
# shots_on_target_total_overall are the two most important features
# they have a regression cocefficient of 0.72 and 2.29 respectively.
# expected goal was removed because they aren't actions that a player 
# can control

### ANALYZING WHAT CONTRIBUTES TO CLEAN SHEETS (DENFENDERS) ###

generic_cols_to_drop = ['position','man_of_the_match_total_overall',
                'annual_salary_eur','annual_salary_eur_percentile', 
                'annual_salary_gbp','annual_salary_usd','rank_in_league_top_attackers',
                'rank_in_league_top_midfielders','rank_in_club_top_scorer',
                'ratings_total_overall']

defence_players = defence_players.drop(generic_cols_to_drop,axis=1)

clean_sheets_cols_to_drop = ["clean_sheets_overall", "clean_sheets_home",
                             "clean_sheets_away", "conceded_overall",
                             "conceded_home", "conceded_away",
                             "xg_faced_per_90_overall",
                             "xg_faced_per90_percentile_overall",
                             "xg_faced_per_game_overall",
                             "xg_faced_total_overall",
                             'clean_sheets_percentage_percentile_overall',
                             'conceded_per_90_overall',
                             'conceded_per90_percentile_overall',
                             'min_per_conceded_overall',
                             'min_per_conceded_percentile_overall',
                             'sm_matches_recorded_total_overall',
                             'sm_matches_recorded_total_overall']  ## What is sm_matches

outcome_cols_to_drop = ['goals_overall','goals_home','goals_away',
                'penalty_goals', 'penalty_misses', 'goals_per_90_overall',
                'goals_per_90_home', 'goals_per_90_away','min_per_goal_overall',
                'hattricks_total_overall','two_goals_in_a_game_total_overall',
                'three_goals_in_a_game_total_overall',
                'two_goals_in_a_game_percentage_overall',
                'three_goals_in_a_game_percentage_overall',
                'goals_involved_per90_percentile_overall',
                'goals_per90_percentile_overall', 'goals_per90_percentile_away',
                'goals_per90_percentile_home','sm_goals_scored_total_overall', 
                'xg_per_90_overall',
                'xg_per_game_overall','xg_per90_percentile_overall',
                'goals_involved_per_90_overall', 'xg_total_overall',
                'average_rating_percentile_overall','games_subbed_in_percentile_overall',
                'games_subbed_in']

## Need to cast target variable to float so that featurewize know it is regression.
X = defence_players.drop(clean_sheets_cols_to_drop,axis=1)
X = X.drop(outcome_cols_to_drop,axis=1)
y = defence_players['clean_sheets_overall'].astype('float')

# DROPPING ROW 2323 (LITTLE WIERD)
X = X.drop(index=X.loc[2323].name)
y = y.drop(2323)

X = extra_cleaning(X)

### FEATURE SELECTION ###
features = FeatureWiz(corr_limit=0.70, feature_engg='', category_encoders='', 
                      dask_xgboost_flag=False, nrows=None, verbose=2)

X_train_selected = features.fit_transform(X, y)

### LINEAR REGRESSION ###
### Quick test of the usefulness of the features selected by featurewiz
print(train(X_train_selected,y))

### LASSO REGRESSION ###
X_selected = X_train_selected

linear_model = lasso_reg_output(X_selected,y)
linear_model = linear_model.sort_values('Coef')

print(linear_model)

# From LASSO, we see that passes_completed_total_overall (2.77), shots_total_overall (0.44),
# duels_total_overall (0.38), min_per_card_overall (0.38), assists_away (0.37) are most important
# features for predicting clean sheets.


###############################################################
### CLUSTERING ###
selected_featueres = ['full_name', 'position','shot_conversion_rate_overall',
                      'shots_on_target_total_overall', 
                      'passes_completed_total_overall', 'shots_total_overall',
                      'duels_total_overall', 'min_per_card_overall',
                      'assists_away']

curr_players = pd.read_csv("data\players\england-premier-league-players-2017-to-2022-stats.csv")
curr_players = curr_players[curr_players['Season']=='2021-2022']
curr_players = curr_players[curr_players['position']=='Forward']
curr_players = curr_players[curr_players['appearances_overall']>0]
  
players_selected_features = curr_players[selected_featueres]
players_selected_features = players_selected_features.drop(['full_name','position'],axis=1)

scaler = StandardScaler()
X = scaler.fit_transform(players_selected_features)


# Perform KMeans clustering and find optimal number of clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Plot elbow curve
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()


# Cluster players using KMeans
kmeans = KMeans(n_clusters=6, random_state=42)
clusters = kmeans.fit_predict(X)

# Assign player names to each cluster
cluster_labels = {}
for i, cluster in enumerate(clusters):
    if cluster not in cluster_labels:
        cluster_labels[cluster] = []
    cluster_labels[cluster].append(curr_players.iloc[i]['full_name'])

# Print player names in each cluster
for i in range(6):
    print(f'Cluster {i}: {", ".join(cluster_labels[i])}')
    
    
cluster_stats = pd.concat([curr_players['full_name'], players_selected_features], axis=1)
cluster_stats['cluster'] = clusters
cluster_means = cluster_stats.groupby('cluster').mean()

# Print player names and mean statistics in each cluster
for i in range(6):
    print(f'Cluster {i}: {", ".join(cluster_labels[i])}')
    print(cluster_means.loc[i])
    print('---------------------------')