import numpy as np
import pandas as pd

playersFwd = pd.read_csv("./data/players/clustered_fwds.csv")
playersMid = pd.read_csv("./data/players/clustered_mids.csv")
playersDef = pd.read_csv("./data/players/clustered_defs.csv")

playersLargeDataset = pd.concat([playersFwd, playersMid, playersDef], ignore_index=True)

playersSalaryDataset = pd.read_csv("./data/salaries/scrapedSalaries.csv")

playerVector1 = playersLargeDataset['full_name'].to_numpy()
playerVector2 = playersSalaryDataset['Player'].to_numpy()

playerSearchLinks = []

#filter playersLargeDataset to only include players that do not appear in playersSalaryDataset
playersLargeDatasetFiltered = playersLargeDataset[~playersLargeDataset['full_name'].isin(playerVector2)]

#sort the filtered dataset by name
playersLargeDatasetFiltered = playersLargeDatasetFiltered.sort_values(by='performance', ascending=False)

# ensure that filtered dataset performance is > 0
playersLargeDatasetFiltered = playersLargeDatasetFiltered[playersLargeDatasetFiltered['performance'] > 0]
print(playersLargeDatasetFiltered)

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
playerNameFrame.to_csv("./data/salaries/player_names.csv", index=False)

#save the dataframe to a csv file
playerSearchLinkFrame.to_csv("./data/salaries/player_search_links.csv", index=False)        
        
