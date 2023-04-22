import numpy as np
import pandas as pd

playersLargeDataset = pd.read_csv("./data/players/england-premier-league-players-2017-to-2022-stats.csv")
playersSalaryDataset = pd.read_csv("./data/salaries/player_salaries.csv")

playerVector1 = playersLargeDataset['full_name'].to_numpy()
playerVector2 = playersSalaryDataset['Player'].to_numpy()

playerSearchLinks = []

for player in playerVector1:
    if player not in playerVector2:
        #replace any spaces with a +
        newPlayerName = player.replace(" ", "+")
        # create a google link with the player name and "salary"
        googleLink = "https://www.google.com/search?q=" + newPlayerName + "+salary"
        # append the link to playerSearchLinks
        playerSearchLinks.append(googleLink)
    
#output the array to a csv file
playerSearchLinks = np.array(playerSearchLinks)
playerSearchLinks = pd.DataFrame(playerSearchLinks)
playerSearchLinks.to_csv("./data/salaries/playerSearchLinks.csv", index=False)
        
        
