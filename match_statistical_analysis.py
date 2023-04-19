# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:52:46 2023

@author: louis
"""

import pandas as pd
from sklearn import linear_model
from verstack import FeatureSelector
from featurewiz import featurewiz

### Reading in the data
matches = pd.read_csv("data\matches\england-premier-league-matches-2017-to-2022-stats.csv")

### Subsetting the columns
cols = ['home_team_name','away_team_name','home_team_goal_count',
        'away_team_goal_count','total_goals_at_half_time',
       'home_team_goal_count_half_time', 'away_team_goal_count_half_time',
       'home_team_corner_count', 'away_team_corner_count',
       'home_team_yellow_cards', 'home_team_red_cards',
       'away_team_yellow_cards', 'away_team_red_cards',
       'home_team_first_half_cards', 'home_team_second_half_cards',
       'away_team_first_half_cards', 'away_team_second_half_cards',
       'home_team_shots', 'away_team_shots', 'home_team_shots_on_target',
       'away_team_shots_on_target', 'home_team_shots_off_target',
       'away_team_shots_off_target', 'home_team_fouls', 'away_team_fouls',
       'home_team_possession', 'away_team_possession']

matches = matches[cols]

### Calculating the points earned by the home team and adding to dataframe
home_team_pts = []
for i in matches.index:
    
    if matches['home_team_goal_count'][i] > matches['away_team_goal_count'][i]:
        home_team_pts.append(3)
    elif matches['home_team_goal_count'][i] == matches['away_team_goal_count'][i]:
        home_team_pts.append(1)
    else:
        home_team_pts.append(0)
        
matches['home_team_pts'] = home_team_pts

### Feature Selection
features = matches.iloc[:,2:26]
target = matches.iloc[:,27]
data = pd.merge(features,target,left_index=True,right_index=True)


features, train = featurewiz(data,'home_team_pts',corr_limit=0.7,verbose=2,sep=",",header=0,test_data="",feature_engg="",category_encoders="")



"""### Linear Regression on all columns
X = matches.iloc[:,2:26]
y = matches.iloc[:,27]

regr = linear_model.LinearRegression()
regr.fit(X,y)

print(regr.coef_)"""