import pandas as pd
# import openpyxl as op

## Matches Data ##

# Read in data
matchPathOne = "./data/matches/england-premier-league-matches-2017-to-2018-stats.csv"
matchPathTwo = "./data/matches/england-premier-league-matches-2018-to-2019-stats.csv"
matchPathThree = "./data/matches/england-premier-league-matches-2019-to-2020-stats.csv"
matchPathFour = "./data/matches/england-premier-league-matches-2020-to-2021-stats.csv"
matchPathFive = "./data/matches/england-premier-league-matches-2021-to-2022-stats.csv"

# Put filepaths into a list
fileList = [matchPathOne, matchPathTwo, matchPathThree, matchPathFour, matchPathFive]

# Join all dataframes into one
for i in range(len(fileList)):
    if i == 0:
        df = pd.read_csv(fileList[i])
    else:
        df = pd.concat([df, pd.read_csv(fileList[i])], axis=0, ignore_index=True)
     
# Save to CSV output   
df.to_csv("./data/matches/england-premier-league-matches-2017-to-2022-stats.csv", index=False)

## Players Data ##
playerPathOne = "./data/players/england-premier-league-players-2017-to-2018-stats.csv"
playerPathTwo = "./data/players/england-premier-league-players-2018-to-2019-stats.csv"
playerPathThree = "./data/players/england-premier-league-players-2019-to-2020-stats.csv"
playerPathFour = "./data/players/england-premier-league-players-2020-to-2021-stats.csv"
playerPathFive = "./data/players/england-premier-league-players-2021-to-2022-stats.csv"

# Put filepaths and season years into a list
filePaths = [playerPathOne, playerPathTwo, playerPathThree, playerPathFour, playerPathFive]
seasons = ["2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022"]

# Join all dataframes into one, and add a column for the season for each player
for i in range(len(filePaths)):
    if i == 0:
        df = pd.read_csv(filePaths[i])
        df["Season"] = seasons[i]
    else:
        #add season to each player BEFORE appending
        temp_df = pd.read_csv(filePaths[i])
        temp_df["Season"] = seasons[i]
        #append temp_df to df
        df = pd.concat([df, temp_df], axis=0, ignore_index=True)

# save to CSV output
df.to_csv("./data/players/england-premier-league-players-2017-to-2022-stats.csv", index=False)

## League Data ##

# Read in data
matchPathOne = "./data/league/england-premier-league-teams-2017-to-2018-stats.csv"
matchPathTwo = "./data/league/england-premier-league-teams-2018-to-2019-stats.csv"
matchPathThree = "./data/league/england-premier-league-teams-2019-to-2020-stats.csv"
matchPathFour = "./data/league/england-premier-league-teams-2020-to-2021-stats.csv"
matchPathFive = "./data/league/england-premier-league-teams-2021-to-2022-stats.csv"

# Put filepaths into a list
fileList = [matchPathOne, matchPathTwo, matchPathThree, matchPathFour, matchPathFive]

# Join all dataframes into one
for i in range(len(fileList)):
    if i == 0:
        df = pd.read_csv(fileList[i])
    else:
        df = pd.concat([df, pd.read_csv(fileList[i])], axis=0, ignore_index=True)
     
# Save to CSV output   
df.to_csv("./data/league/england-premier-league-teams-2017-to-2022-stats.csv", index=False)

## League Data 2 ##

# Read in data
matchPathOne = "./data/league/england-premier-league-teams2-2017-to-2018-stats.csv"
matchPathTwo = "./data/league/england-premier-league-teams2-2018-to-2019-stats.csv"
matchPathThree = "./data/league/england-premier-league-teams2-2019-to-2020-stats.csv"
matchPathFour = "./data/league/england-premier-league-teams2-2020-to-2021-stats.csv"
matchPathFive = "./data/league/england-premier-league-teams2-2021-to-2022-stats.csv"

# Put filepaths into a list
fileList = [matchPathOne, matchPathTwo, matchPathThree, matchPathFour, matchPathFive]

# Join all dataframes into one
for i in range(len(fileList)):
    if i == 0:
        df = pd.read_csv(fileList[i])
    else:
        df = pd.concat([df, pd.read_csv(fileList[i])], axis=0, ignore_index=True)
     
# Save to CSV output   
df.to_csv("./data/league/england-premier-league-teams2-2017-to-2022-stats.csv", index=False)