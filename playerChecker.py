import numpy as np
import pandas as pd

playersFwd = pd.read_csv("./data/players/defender_cluster.csv")
playersMid = pd.read_csv("./data/players/midfielder_cluster.csv")
playersDef = pd.read_csv("./data/players/forward_cluster.csv")

playersLargeDataset = pd.concat([playersFwd, playersMid, playersDef], ignore_index=True)
# Take out all rows with 0 salary
playersLargeDatasetFiltered = playersLargeDataset[playersLargeDataset['salary'] == 0]

playerSearchLinks = []

# strip spaces from player names and replace with + for search link
for i in range(len(playersLargeDatasetFiltered)):
    playerSearchLink = playersLargeDatasetFiltered.iloc[i]['full_name'].replace(" ", "+")
    googleSearchLink = "https://www.google.com/search?q=" + playerSearchLink
    #add + salary to the end of the search link
    googleSearchLink = googleSearchLink + "+salary"
    playerSearchLinks.append(googleSearchLink)

#create a vector of player names
playerNames = playersLargeDatasetFiltered['full_name'].to_numpy()
googleSearchLinks = np.array(playerSearchLinks)

#create a dataframe of player names and search links
playerSearchLinkFrame = pd.DataFrame({'Player':playerNames, 'Search Link':googleSearchLinks})

#output player names alone to a csv file and append a comma to the end of each name
playerNameVector = playerNames + ","
playerNameFrame = pd.DataFrame({'Player':playerNameVector})

#save the dataframe to a csv file
playerSearchLinkFrame.to_csv("./data/salaries/player_search_links.csv", index=False)        
        
