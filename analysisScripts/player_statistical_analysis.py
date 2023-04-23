# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:24:52 2023

@author: louis
"""

import pandas as pd
from featurewiz import FeatureWiz

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LassoCV, Lasso
from lazypredict.Supervised import LazyRegressor
from sklearn.preprocessing import StandardScaler

### DATA CLEANING AND PREPRING ###
players = pd.read_csv("data\players\england-premier-league-players-2017-to-2022-stats.csv")
players = pd.concat([players[players['Season']=='2020-2021'],
                    players[players['Season']=='2021-2022']],axis=0)
players = players[players['appearances_overall']>0]

### Creating new dataframes for each position
goalkeepers = players[players['position'] == 'Goalkeeper']
attack_players = pd.concat([players[players['position'] == 'Foward'],
                    players[players['position'] == 'Midfielder']],axis=0)
defence_players = pd.concat([players[players['position'] == 'Midfielder'],
                    players[players['position'] == 'Defender']],axis=0)

def cleaning(df, cols_to_drop):
    # Dropping the columns specified by user
    df = df.drop(cols_to_drop,axis=1)
    
    # Dropping columns with NA values
    df = df.dropna(axis=1)
    
    # Checking if there is any negative values that may crash featurewiz
    more_cols_to_drop = (df<0).any()[(df<0).any()==True].index.tolist()
    df = df.drop(more_cols_to_drop,axis=1)
    
    # Checking if there is columns with only 0 that may crash featurewiz; 
    # make sure to export to csv the columns you are going to delete to check
    more_cols_to_drop = (df==0).all()[(df==0).all()==True].index.tolist()
    df = df.drop(more_cols_to_drop,axis=1)
    
    return df
  
# Columns that are not related to the performance
generic_cols = ['Season','shirt_number','full_name','age','birthday',
                'birthday_GMT','league','season','Current Club',
                'minutes_played_overall','minutes_played_home',
                'minutes_played_away','nationality','appearances_overall',
                'appearances_home','appearances_away',
                'man_of_the_match_total_overall', 'annual_salary_eur',
                'annual_salary_eur_percentile', 'annual_salary_gbp',
                'annual_salary_usd', 'rank_in_league_top_attackers',
                'rank_in_league_top_midfielders','rank_in_club_top_scorer',
                'ratings_total_overall','position']


# Columns that are outcomes. It should be dropped as they are not actions.
outcome_cols = ['goals_home','goals_away','penalty_goals',
                'penalty_misses', 'goals_per_90_overall', 'goals_per_90_home',
                'goals_per_90_away','min_per_goal_overall',
                'hattricks_total_overall','two_goals_in_a_game_total_overall',
                'three_goals_in_a_game_total_overall',
                'two_goals_in_a_game_percentage_overall',
                'three_goals_in_a_game_percentage_overall',
                'goals_involved_per90_percentile_overall',
                'goals_per90_percentile_overall',
                'goals_per90_percentile_away','goals_per90_percentile_home',
                'sm_goals_scored_total_overall',
                'xg_per_90_overall','xg_per_game_overall',
                'xg_per90_percentile_overall','goals_involved_per_90_overall',
                'xg_total_overall','average_rating_percentile_overall',
                'games_subbed_in_percentile_overall','games_subbed_in',
                 "clean_sheets_home",
                "clean_sheets_away", "conceded_home","conceded_overall",
                "conceded_away","xg_faced_per_90_overall",
                "xg_faced_per90_percentile_overall",
                "xg_faced_per_game_overall","xg_faced_total_overall",
                'clean_sheets_percentage_percentile_overall',
                'conceded_per_90_overall','conceded_per90_percentile_overall',
                'min_per_conceded_overall',
                'min_per_conceded_percentile_overall',
                'sm_matches_recorded_total_overall',
                'sm_matches_recorded_total_overall','average_rating_overall',
                'games_started_percentile_overall',
                'npxg_per90_percentile_overall','games_subbed_out',
                'games_started', 'games_subbed_out_percentile_overall']

## SHOULD I INCLUDE xg_total_overall, and what is sm_games

cols_to_drop = generic_cols + outcome_cols
attack_players = cleaning(attack_players,cols_to_drop)
defence_players = cleaning(defence_players,cols_to_drop)
goalkeepers = cleaning(goalkeepers,cols_to_drop)

# Dropped row 2323 (it is a little weird)
attack_players  = attack_players.drop(2323)
defence_players  = defence_players.drop(2323)

###############################################################################

### FEATURE SELECTION ###
def feature_selection_by_featurewiz(df,target):
    
    ## Need to cast target variable to float so that featurewize know it is 
    # regression.
    
    X = df.drop([target],axis=1)
    y = df[target].astype('float')

    features = FeatureWiz(corr_limit=0.70, feature_engg='', 
                          category_encoders='', dask_xgboost_flag=False,
                          nrows=None, verbose=2)

    X_selected = features.fit_transform(X, y)
    
    return X_selected

### MODEL COMPARISON ###
### Quick test of the usefulness of the features selected by featurewiz
def model_compare(data, target):
    
    # Fit all models
    X_train, X_test,y_train, y_test = train_test_split(data, target, 
                                                       test_size=.2, 
                                                       random_state=42)
    
    reg = LazyRegressor(predictions=True)
    models, predictions = reg.fit(X_train, X_test, y_train, y_test)
    
    return models

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

###############################################################################

### ATTACKER ANALYSIS (GOALS_OVERALL AS TARGET) ###
attack_players_selected = feature_selection_by_featurewiz(attack_players,
                                                          'goals_overall')
print(model_compare(attack_players_selected,
                    attack_players['goals_overall'].astype('float'))[:10])
attack_model = lasso_reg_output(attack_players_selected,
                                attack_players['goals_overall'].astype('float'))
attack_model = attack_model.sort_values('Coef',ascending=False).head()

print(attack_model)

# If expected goal is not used then shot_conversion_rate_overall and
# shots_on_target_total_overall are the two most important features
# they have a regression cocefficient of 0.76 and 2.44 respectively.
# expected goal was removed because they aren't actions that a player 
# can control

###############################################################################

### DEFENDER ANALYSIS (CLEAN_SHEETS_OVERAL AS TARGET)###

defence_players_selected = feature_selection_by_featurewiz(defence_players,           
                                                           'clean_sheets_overall')
print(model_compare(defence_players_selected,
                    defence_players['clean_sheets_overall'].astype('float'))[:10])

defence_model = lasso_reg_output(defence_players_selected,
                                defence_players['clean_sheets_overall'].astype('float'))
defence_model = defence_model.sort_values('Coef',ascending=False)

print(defence_model)

# From LASSO, we see that passes_completed_total_overall (2.74), 
# key_passes_total_overall (0.50), shots_off_target_total_overall (0.43),
# assists_per90_percentile_overall (0.40), min_per_card_overall (0.33)
# duels_total_overall  (0.26) are most important features for predicting 
# clean sheets.

###############################################################################

### GOALKEEPER ANALYSIS ###

# But used 'saves_per_game_overall" , "passes_completed_total_overall"
# and save_percentage_overall as feature.

"""
### The analysis below doesn't quite work

goalkeepers_X = goalkeepers[['saves_per_game_overall',
                             "passes_completed_total_overall"]]

#goalkeepers_X = StandardScaler().fit_transform(goalkeepers_X)

goalkeepers_y = goalkeepers['clean_sheets_overall']

print(model_compare(goalkeepers_X,goalkeepers_y))

goalkeeper_model = lasso_reg_output(goalkeepers_X,
                                goalkeepers_y)
goalkeeper_model = goalkeeper_model.sort_values('Coef',ascending=False)

print(goalkeeper_model)
"""