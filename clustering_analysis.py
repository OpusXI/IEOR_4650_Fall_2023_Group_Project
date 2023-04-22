# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:41:33 2023

@author: louis
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


### CLUSTERING ###

## Features that were selected from the player_statistical_analysis.py
selected_features = ['full_name', 'position','shot_conversion_rate_overall',
                      'shots_on_target_total_overall', 
                      'passes_completed_total_overall', 'shots_total_overall',
                      'duels_total_overall', 'min_per_card_overall',
                      'assists_away']

players_master = pd.read_csv("data\players\england-premier-league-players-2017-to-2022-stats.csv")
curr_players = players_master[players_master['Season']=='2021-2022']
curr_players = curr_players[curr_players['appearances_overall']>0]


def positions_clustering(df,position,weights,n_clusters,output=True,plot=False):
    
    df = df[df['position']==position][selected_features]
    X = df.drop(['full_name','position'],axis=1)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)


    # Perform KMeans clustering and find optimal number of clusters
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    
    # Plot elbow curve
    if plot==True:
        plt.plot(range(1, 11), wcss)
        plt.title('Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()
    ####################################

    # Clustering of players
    n_clusters = n_clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    df['cluster'] = clusters
    
    # Addubg weightage the featuers to rank the players
    weights = weights
    
    df['performance'] = (X*weights).sum(axis=1)        # Used scaled data here, but should it be unscaled?

    df['rankings'] = [0]*len(df)    # Create a column with empty rankings
    rankings_in_cluster = {}
    for i in range(n_clusters):
        cluster_data = df[df['cluster']==i]
        cluster_data = cluster_data.sort_values(by='performance', ascending=False)
        rankings_in_cluster = cluster_data.index.values 
        
        for j in range(len(cluster_data)):
            df.loc[rankings_in_cluster[j],'rankings'] = j+1
    
    
    
    if output == True:
        
        for i in range(n_clusters):
            print("#########################################################")
            print(f'Cluster {i}:')
            cluster_data = df[df['cluster']==i]
            names = ','.join(cluster_data['full_name'].tolist())
            print("The players in the cluster are:" + names)
            
            cluster_means = cluster_data.drop('full_name',axis=1).mean()
            print("------------------------------------------")
            print("The mean values of this cluster are:")
            print(cluster_means)
            print("------------------------------------------")
            print('Their rankings are as follows:')
            print(cluster_data.sort_values(by='rankings',ascending=True)[['full_name','performance','rankings']])
            
    return df

## Adjust the weights according to their position

weights = [0.4, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
z = positions_clustering(curr_players, 'Forward', weights, 6, output=True)

weights = [0.4, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
z = positions_clustering(curr_players, 'Midfielder', weights, 6, output=True)

weights = [0.4, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
z = positions_clustering(curr_players, 'Defender', weights, 6,output=True)

