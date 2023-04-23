# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:52:46 2023

@author: louis
"""

import pandas as pd
from featurewiz import FeatureWiz

from sklearn.model_selection import train_test_split
#from sklearn.model_selection import KFold
#from sklearn.model_selection import cross_val_score
#from sklearn.linear_model import LinearRegression
from lazypredict.Supervised import LazyClassifier, LazyRegressor

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, r2_score

from sklearn.tree import plot_tree
import matplotlib.pyplot as plt


from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
import numpy as np

### Reading in the data
matches = pd.read_csv("data\matches\england-premier-league-matches-2017-to-2022-stats.csv")

### Subsetting the columns
cols = ['home_team_goal_count',
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
outcome = []
for i in matches.index:
    
    if matches['home_team_goal_count'][i] > matches['away_team_goal_count'][i]:
        outcome.append("Home Win")
    elif matches['home_team_goal_count'][i] == matches['away_team_goal_count'][i]:
        outcome.append("Draw")
    else:
        outcome.append("Away Win")
        
matches['outcome'] = outcome

#['home_team_goal_count',
#        'away_team_goal_count','total_goals_at_half_time',
#       'home_team_goal_count_half_time', 'away_team_goal_count_half_time'],axis=1)

### Feature Selection
X, y = matches.drop("outcome",axis=1), matches["outcome"]


features = FeatureWiz(corr_limit=0.70, feature_engg='', category_encoders='', 
                      dask_xgboost_flag=False, nrows=None, verbose=2)

X_train_selected = features.fit_transform(X, y)

### Quick test of the usefulness of the features selected by featurewiz
def train(data, target):
    X_train, X_test,y_train, y_test = train_test_split(data, target, test_size=.2, random_state=42)# fit all models
    reg = LazyClassifier(predictions=True)
    models, predictions = reg.fit(X_train, X_test, y_train, y_test)
    
    return models

print(train(X_train_selected,y))

### RF on the model

X_train, X_test, y_train, y_test = train_test_split(X_train_selected, y,
                                                    test_size=0.2, random_state=42)

# Initialize a random forest classifier and fit it to the training data
model = RandomForestClassifier(n_estimators=100, random_state=42, max_features=5,max_depth=3)
model.fit(X_train, y_train)

# Evaluate the performance of the model on the test set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Get feature importances
importances = model.feature_importances_
indices = X_train.columns.tolist()

# Print feature importances
print("Feature importances:")
for i in range(len(indices)):
    print(indices[i], ": ", importances[i])

# Print accuracy
print("Accuracy:", accuracy)

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10,10), dpi=300)
plot_tree(model.estimators_[0], filled=True, feature_names=X_train_selected.columns, ax=axes)
plt.show()

### Shouldn't use goal counts as feature as it is an outcome not an action. It is very important for
### classifying tho, so perhaps we can change the question to regressing away goals and home goals.


### REGRESSION ON GOAL COUNTS INSTEAD
def train_regression(data, target):
    X_train, X_test,y_train, y_test = train_test_split(data, target, test_size=.2, random_state=42)# fit all models
    reg = LazyRegressor(predictions=True)
    models, predictions = reg.fit(X_train, X_test, y_train, y_test)
    
    return models

### HOME GOALS FIRST
X, y = matches.drop(["outcome","home_team_goal_count",
                     'home_team_goal_count_half_time',"total_goals_at_half_time"],
                    axis=1), matches["home_team_goal_count"]


features = FeatureWiz(corr_limit=0.70, feature_engg='', category_encoders='', 
                      dask_xgboost_flag=False, nrows=None, verbose=2)

X_train_selected = features.fit_transform(X, y)

print(train_regression(X_train_selected,y))


### AWAY GOALS NOW
X, y = matches.drop(["outcome","away_team_goal_count",
                     'away_team_goal_count_half_time',"total_goals_at_half_time"],
                    axis=1), matches["away_team_goal_count"]


features = FeatureWiz(corr_limit=0.70, feature_engg='', category_encoders='', 
                      dask_xgboost_flag=True, nrows=None, verbose=2)

X_train_selected = features.fit_transform(X, y)

print(train_regression(X_train_selected,y))
### ERROR STOP FOR NOW

