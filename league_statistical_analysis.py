# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 18:12:31 2023

@author: louis
"""
import pandas as pd
from numpy import mean

import scipy.stats as stats
from featurewiz import FeatureWiz

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from lazypredict.Supervised import LazyRegressor

### Reading in the data and data cleaning
league = pd.read_csv("data\league\england-premier-league-teams-2017-to-2022-stats.csv")

cols_drop_1 = ['league_position_home','league_position_away','goal_difference','win_percentage',
 "btts_count", "btts_count_home", "btts_count_away", "draw_percentage_overall", "draw_percentage_home",
 "draw_percentage_away", "loss_percentage_ovearll", "loss_percentage_home",
 "loss_percentage_away", "btts_percentage", "btts_percentage_home", "btts_percentage_away",
 "btts_half_time", "btts_half_time_home", "btts_half_time_away",
 "btts_half_time_percentage", "btts_half_time_percentage_home", "btts_half_time_percentage_away",
 "over05_count", "over15_count", "over25_count", "over35_count", "over45_count", "over55_count",
 "over05_count_home", "over15_count_home", "over25_count_home", "over35_count_home", "over45_count_home",
 "over55_count_home", "over05_count_away", "over15_count_away", "over25_count_away", "over35_count_away",
 "over45_count_away", "over55_count_away", "under05_count", "under15_count", "under25_count", "under35_count",
 "under45_count", "under55_count", "under05_count_home", "under15_count_home", "under25_count_home",
 "under35_count_home", "under45_count_home", "under55_count_home", "under05_count_away", "under15_count_away",
 "under25_count_away", "under35_count_away", "under45_count_away", "under55_count_away", "over05_percentage",
 "over15_percentage", "over25_percentage", "over35_percentage", "over45_percentage", "over55_percentage",
 "over05_percentage_home", "over15_percentage_home", "over25_percentage_home", "over35_percentage_home",
 "over45_percentage_home", "over55_percentage_home", "over05_percentage_away", "over15_percentage_away",
 "over25_percentage_away", "over35_percentage_away", "over45_percentage_away", "over55_percentage_away",
 "under05_percentage", "under15_percentage", "under25_percentage", "under35_percentage", "under45_percentage",
 "under55_percentage", "under05_percentage_home", "under15_percentage_home", "under25_percentage_home",
 "under35_percentage_home", "under45_percentage_home", "under55_percentage_home", "under05_percentage_away",
 "under15_percentage_away", "under25_percentage_away", "under35_percentage_away", "under45_percentage_away",
 "under55_percentage_away", "over05_count_half_time", "over15_count_half_time","over25_count_half_time", 
 "over05_count_half_time_home", "over15_count_half_time_home", "over25_count_half_time_home", 
 "over05_count_half_time_away", "over15_count_half_time_away", "over25_count_half_time_away", 
 "over05_half_time_percentage", "over15_half_time_percentage", "over25_half_time_percentage", 
 "over05_half_time_percentage_home", "over15_half_time_percentage_home", "over25_half_time_percentage_home", 
 "over05_half_time_percentage_away", "over15_half_time_percentage_away", "over25_half_time_percentage_away",
 "win_percentage", "win_percentage_home", "win_percentage_away", "home_advantage_percentage",
 "points_per_game_half_time", "points_per_game_half_time_home", "points_per_game_half_time_away",
 "over145_corners_percentage", "over65_corners_percentage",
 "over75_corners_percentage", "over85_corners_percentage", "over95_corners_percentage",
 "over105_corners_percentage", "over115_corners_percentage", "over125_corners_percentage",
 "over135_corners_percentage", "fts_percentage", "fts_percentage_home", "fts_percentage_away", "first_team_to_score_percentage",
 "first_team_to_score_percentage_home", "first_team_to_score_percentage_away", "clean_sheet_half_time",
 "clean_sheet_half_time_home", "clean_sheet_half_time_away", "clean_sheet_half_time_percentage",
 "clean_sheet_half_time_percentage_home", "clean_sheet_half_time_percentage_away", "fts_half_time",
 "fts_half_time_home", "fts_half_time_away", "fts_half_time_percentage", "fts_half_time_percentage_home",
 "fts_half_time_percentage_away", "leading_at_half_time_percentage", "leading_at_half_time_percentage_home", "leading_at_half_time_percentage_away",
 "draw_at_half_time_percentage", "draw_at_half_time_percentage_home", "draw_at_half_time_percentage_away",
 "losing_at_half_time_percentage", "losing_at_half_time_percentage_home", "losing_at_half_time_percentage_away",
 "total_goals_per_match_half_time", "total_goals_per_match_half_time_home", "total_goals_per_match_half_time_away",
 "goals_scored_per_match_half_time", "goals_scored_per_match_half_time_home", "goals_scored_per_match_half_time_away",
 "goals_conceded_per_match_half_time", "goals_conceded_per_match_half_time_home", "goals_conceded_per_match_half_time_away",
 "goals_scored_half_time", "goals_scored_half_time_home", "goals_scored_half_time_away",
 "goals_conceded_half_time", "goals_conceded_half_time_home", "goals_conceded_half_time_away",
 "goal_difference_half_time", "goal_difference_half_time_home", "goal_difference_half_time_away",
 "leading_at_half_time", "leading_at_half_time_home", "leading_at_half_time_away",
 "draw_at_half_time", "draw_at_half_time_home", "draw_at_half_time_away",
 "losing_at_half_time", "losing_at_half_time_home", "losing_at_half_time_away",
 "goals_scored_min_0_to_10", "goals_scored_min_11_to_20", "goals_scored_min_21_to_30",
 "goals_scored_min_31_to_40", "goals_scored_min_41_to_50", "goals_scored_min_51_to_60",
 "goals_scored_min_61_to_70", "goals_scored_min_71_to_80", "goals_scored_min_81_to_90",
 "goals_conceded_min_0_to_10", "goals_conceded_min_11_to_20", "goals_conceded_min_21_to_30",
 "goals_conceded_min_31_to_40", "goals_conceded_min_41_to_50", "goals_conceded_min_51_to_60"]

### These columns should be dropped, but for some reason once dropped it creates
### an error with FeatureWiz
cols_drop_3 =  ["goals_conceded_min_61_to_70","goals_conceded_min_71_to_80","goals_conceded_min_81_to_90"]

### Creating a column of points earned by the team
league['points'] = (league['wins']*3) + league['draws']

### Dropping the unnecessary columns
league = league.iloc[:,18:]
league = league.drop(cols_drop_1,axis=1)

### Seperating the league data to top 4 teams and non-top 4 teams
top4 = league[league['league_position'] <= 4]
non_top4 = league[league['league_position'] > 4]

### Drop extra columns
league = league.drop(["league_position","performance_rank"],axis=1)


### Feature Selection
X_train, y = league.drop('points',axis=1), league['points']

features = FeatureWiz(corr_limit=0.70, feature_engg='', category_encoders='', 
                      dask_xgboost_flag=False, nrows=None, verbose=2)

X_train_selected = features.fit_transform(X_train, y)

### Quick test of the usefulness of the features selected by featurewiz
def train(data, target):
    X_train, X_test,y_train, y_test = train_test_split(data, target, test_size=.2, random_state=42)# fit all models
    reg = LazyRegressor(predictions=True)
    models, predictions = reg.fit(X_train, X_test, y_train, y_test)
    
    return models

train(X_train_selected,y)

### Check that the features selected are statistically significant between
### top 4 and non-top 4 teams

def significant_test(df1,df2):
    stat = []
    p_values = []
    
    for col in df1.columns:
        
        group1 = df1[col].array
        group2 = df2[col].array
        p = stats.ttest_ind(a=group1, b=group2, equal_var=True).pvalue
        stat.append(col)
        p_values.append(p)
    
    d = {'stats':stat,'p-value':p_values}
    p_values = pd.DataFrame(d).sort_values('p-value')
    
    pd.set_option('display.float_format',  '{:,}'.format)
    
    desirable_stats = p_values[p_values['p-value']<0.01]
    sig_diff_features = desirable_stats['stats'].to_list()
    
    print(desirable_stats)
    
    return sig_diff_features

selected_features = X_train_selected.columns
top4 = top4[selected_features]
non_top4 = non_top4[selected_features]

selected_features = significant_test(top4,non_top4)

# From the p-values output we can see that all the selected features
# are indeed statistically significant between two groups

### Linear Regression on selected features

def lin_reg_output(X,y):
    
    cv = KFold(n_splits=5, random_state=1, shuffle=True)
    model = LinearRegression()
    scores = cross_val_score(model, X, y,
                         cv=cv, n_jobs=-1, scoring='r2')
    
    model.fit(X,y)

    output = {
        'Features':model.feature_names_in_,
        'Coef':model.coef_}
    
    print("The mean accuracy of the model is:" + str(mean(scores)))
    print("-----------------------------------------------------")
    print("The coefficients of the featuers are as follows:")
    print(pd.DataFrame(output))
    
    return model

X_selected = X_train[selected_features]

linear_model = lin_reg_output(X_selected,y)
    
    



















