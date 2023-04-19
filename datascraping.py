# Import all the modules required.
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model, model_selection
import time
from unidecode import unidecode

# Reference: https://github.com/charles-Peters/Premier-League-Moneyball/blob/master/football_player_evaluation_code.ipynb

# set base url for all future requests
premierLeagueURL = 'https://www.premierleague.com'
req = requests.get(premierLeagueURL + '/clubs')
soup = BeautifulSoup(req.text,'html.parser')
print("Club links scraped successfully!")

# Link above takes us to this page: https://www.premierleague.com/clubs now we need to extract these links to find nested links for players
# To find players, we grab the links for each club, and replace "overview" for "squad" to find the team's squad page. Once we get the HTML
# for this squad page, we can harvest the invidvidual player data.
rawTeamLinks = soup.find_all('a',attrs={'class':'indexItem'})
teamLinks = []
for link in rawTeamLinks:
    squad = link['href'].replace('overview', 'squad')
    teamLinks.append(premierLeagueURL + squad)
    
# Now that we have the links for each squad, we need to then scrape the final layer of links - for individual players from the HTML of the
# team's "squad" page.
indivPlayerLinks = []
for team in teamLinks:
    squadRequest = requests.get(team)
    squadSoup = BeautifulSoup(squadRequest.text, 'html.parser')
    players = squadSoup.find_all('a', attrs = {'class':'playerOverviewCard active'})
    for player in players:
        a = premierLeagueURL + player['href']
        indivPlayerLinks.append(a.replace('overview', 'stats'))
    time.sleep(1)
print("Player links scraped successfully!")

# We also want to harvest the player names that are in each squad - as a pseudo-key for our database
playerNames = []
for team in teamLinks:
    squadRequest = requests.get(team)
    squadSoup = BeautifulSoup(squadRequest.text, 'html.parser')
    for player in squadSoup.find_all('h4', attrs = {'class':'name'}):
        playerNames.append(player.text)
    time.sleep(1)
print("Player names scraped successfully!")

# slight issue with player names with wierd accents. They don't appear in the links but in the player name so we need to differentiate
namesWithoutAccent = []
for name in playerNames:
    namesWithoutAccent.append(unidecode(name))
    
### Player Data Harvesting - Goalkeeper ###
# We need to create a dictionary that will hold all of our player data. We will then convert this dictionary to a pandas dataframe.
# These will be the keys for our dictionary
# GOALKEEPERS
# First we collect all the stats we want into a list, along with the corresponding tags and attributes from the html doc.
goalkeeperStatsKeys = (('Name', 'div', {'class':'name t-colour'}),
                    ('Team', 'div', {'class':'info'}),
                    ('Apps', 'span', {'data-stat':'appearances'}),
                    ('Wins', 'span', {'data-stat':'wins'}),
                    ('Losses', 'span', {'data-stat':'losses'}),
                    ('Saves', 'span', {'data-stat':'saves'}),
                    ('Penalties saved', 'span', {'data-stat':'penalty_save'}),
                    ('Clean sheets', 'span', {'data-stat':'clean_sheet'}),
                    ('Goals conceded', 'span', {'data-stat':'goals_conceded'}),
                    ('Errors leading to a goal', 'span', {'data-stat':'error_lead_to_goal'}),
                    ('Passes', 'span', {'data-stat':'total_pass'}),
                    ('Accurate long balls', 'span', {'data-stat':'accurate_long_balls'}),
                    ('Yellow cards', 'span', {'data-stat':'yellow_card'}),
                    ('Red cards', 'span', {'data-stat':'red_card'}),
                    ('Fouls', 'span', {'data-stat':'fouls'}),
                    )

defenderStatsKeys = (('Name', 'div', {'class':'name t-colour'}),
                    ('Team', 'div', {'class':'info'}),
                    ('Apps', 'span', {'data-stat':'appearances'}),
                    ('Wins', 'span', {'data-stat':'wins'}),
                    ('Losses', 'span', {'data-stat':'losses'}),
                    ('Tackles', 'span', {'data-stat':'total_tackle'}),
                    ('Errors leading to a goal', 'span', {'data-stat':'error_lead_to_goal'}),
                    ('Blocked shots', 'span', {'data-stat':'blocked_scoring_att'}),
                    ('Interceptions', 'span', {'data-stat':'interception'}),
                    ('Clearances', 'span', {'data-stat':'total_clearance'}),
                    ('Recoveries', 'span', {'data-stat':'ball_recovery'}),
                    ('Duels won', 'span', {'data-stat':'duel_won'}),
                    ('Duels lost', 'span', {'data-stat':'duel_lost'}),
                    ('Goals', 'span', {'data-stat':'goals'}),
                    ('Passes', 'span', {'data-stat':'total_pass'}),
                    ('Accurate long balls', 'span', {'data-stat':'accurate_long_balls'}),
                    ('Yellow cards', 'span', {'data-stat':'yellow_card'}),
                    ('Red cards', 'span', {'data-stat':'red_card'}),
                    ('Fouls', 'span', {'data-stat':'fouls'}),
                    )

midfielderStatsKeys = (('Name', 'div', {'class':'name t-colour'}),
                    ('Team', 'div', {'class':'info'}),
                    ('Apps', 'span', {'data-stat':'appearances'}),
                    ('Wins', 'span', {'data-stat':'wins'}),
                    ('Losses', 'span', {'data-stat':'losses'}),
                    ('Goals', 'span', {'data-stat':'goals'}),
                    ('Freekicks scored', 'span', {'data-stat':'att_freekick_goal'}),
                    ('Assists', 'span', {'data-stat':'goal_assist'}),
                    ('Shots', 'span', {'data-stat':'total_scoring_att'}),
                    ('Shots on target', 'span', {'data-stat':'ontarget_scoring_att'}),
                    ('Passes', 'span', {'data-stat':'total_pass'}),
                    ('Big chances created', 'span', {'data-stat':'big_chance_created'}),
                    ('Crosses', 'span', {'data-stat':'total_cross'}),
                    ('Tackles', 'span', {'data-stat':'total_tackle'}),
                    ('Interceptions', 'span', {'data-stat':'interception'}),
                    ('Yellow cards', 'span', {'data-stat':'yellow_card'}),
                    ('Red cards', 'span', {'data-stat':'red_card'}),
                    ('Fouls', 'span', {'data-stat':'fouls'}),
                    )

forwardsStatsKeys = (('Name', 'div', {'class':'name t-colour'}),
                    ('Team', 'div', {'class':'info'}),
                    ('Apps', 'span', {'data-stat':'appearances'}),
                    ('Wins', 'span', {'data-stat':'wins'}),
                    ('Losses', 'span', {'data-stat':'losses'}),
                    ('Goals', 'span', {'data-stat':'goals'}),
                    ('Headed goals', 'span', {'data-stat':'att_hd_goal'}),
                    ('Penalties scored', 'span', {'data-stat':'att_pen_goal'}),
                    ('Freekicks scored', 'span', {'data-stat':'att_freekick_goal'}),
                    ('Assists', 'span', {'data-stat':'goal_assist'}),
                    ('Shots', 'span', {'data-stat':'total_scoring_att'}),
                    ('Shots on target', 'span', {'data-stat':'ontarget_scoring_att'}),
                    ('Hit woodworks', 'span', {'data-stat':'hit_woodwork'}),
                    ('Big chances missed', 'span', {'data-stat':'big_chance_missed'}),
                    ('Passes', 'span', {'data-stat':'total_pass'}),
                    ('Big chances created', 'span', {'data-stat':'big_chance_created'}),
                    ('Yellow cards', 'span', {'data-stat':'yellow_card'}),
                    ('Red cards', 'span', {'data-stat':'red_card'}),
                    ('Fouls', 'span', {'data-stat':'fouls'}),
                    ('Offsides', 'span', {'data-stat':'total_offside'}),
                    )

# Create an empty dictionary of lists to contain the stats for each player
goalkeeperStats = {stat: [] for stat, tags, attrs in goalkeeperStatsKeys}
defenderStats = {stat: [] for stat, tags, attrs in defenderStatsKeys}
midfielderStats = {stat: [] for stat, tags, attrs in midfielderStatsKeys}
forwardStats = {stat: [] for stat, tags, attrs in forwardsStatsKeys}

# Now fill this dictionary with the relevant information.
for pslink in indivPlayerLinks:
    playerRequest = requests.get(pslink)
    playerSoup = BeautifulSoup(playerRequest.text, 'html.parser')
    position = playerSoup.find_all('div', attrs = {'class':'info'})[1].text
    if position == 'Goalkeeper':
        for stat, tags, attrs in goalkeeperStatsKeys:
            if int(playerSoup.find('span', attrs = {'data-stat':'appearances'}).text) != 0: 
                if stat == 'Name':
                    goalkeeperStats[stat].append(unidecode(playerSoup.find(tags, attrs = attrs).text.strip()))
                elif stat == 'Team':
                    goalkeeperStats[stat].append(playerSoup.find_all(tags, attrs = attrs)[0].text.strip())
                else:
                    goalkeeperStats[stat].append(int(playerSoup.find(tags, attrs = attrs).text.replace(',', '').strip()))
    
    elif position == "Defender":
        #repeat for defenders
        for stat, tags, attrs in defenderStatsKeys:
            if int(playerSoup.find('span', attrs = {'data-stat':'appearances'}).text) != 0: 
                if stat == 'Name':
                    defenderStats[stat].append(unidecode(playerSoup.find(tags, attrs = attrs).text.strip()))
                elif stat == 'Team':
                    defenderStats[stat].append(playerSoup.find_all(tags, attrs = attrs)[0].text.strip())
                else:
                    defenderStats[stat].append(int(playerSoup.find(tags, attrs = attrs).text.replace(',', '').strip()))
    
    elif position == "Midfielder":
        #repeat for midfielders
        for stat, tags, attrs in midfielderStatsKeys:
            if int(playerSoup.find('span', attrs = {'data-stat':'appearances'}).text) != 0: 
                if stat == 'Name':
                    midfielderStats[stat].append(unidecode(playerSoup.find(tags, attrs = attrs).text.strip()))
                elif stat == 'Team':
                    midfielderStats[stat].append(playerSoup.find_all(tags, attrs = attrs)[0].text.strip())
                else:
                    midfielderStats[stat].append(int(playerSoup.find(tags, attrs = attrs).text.replace(',', '').strip()))
    
    elif position == "Forward":
        #repeat for forwards
        for stat, tags, attrs in forwardsStatsKeys:
            if int(playerSoup.find('span', attrs = {'data-stat':'appearances'}).text) != 0: 
                if stat == 'Name':
                    forwardStats[stat].append(unidecode(playerSoup.find(tags, attrs = attrs).text.strip()))
                elif stat == 'Team':
                    forwardStats[stat].append(playerSoup.find_all(tags, attrs = attrs)[0].text.strip())
                else:
                    forwardStats[stat].append(int(playerSoup.find(tags, attrs = attrs).text.replace(',', '').strip()))

    print(f"scraped: {pslink} - {position}")
    time.sleep(1)

gkAllStats = pd.DataFrame(goalkeeperStats)
defAllStats = pd.DataFrame(defenderStats)
midAllStats = pd.DataFrame(midfielderStats)
fwdAllStats = pd.DataFrame(forwardStats)

### Average GK Data to per game stats ###
avgGKStats = pd.DataFrame({'Name':gkAllStats['Name'], 
                    'Win rate':gkAllStats['Wins'] / gkAllStats['Apps'], 
                    'Loss rate':gkAllStats['Losses'] / gkAllStats['Apps']})

for stat,_,_ in goalkeeperStatsKeys[5:]:
    avgGKStats['Average ' + stat] = gkAllStats[stat] / gkAllStats['Apps']

### Average Def Data to per game stats ###
avgDefStats = pd.DataFrame({'Name':defAllStats['Name'],
                            'Win rate':defAllStats['Wins'] / defAllStats['Apps'],
                            'Loss rate':defAllStats['Losses'] / defAllStats['Apps']})

for stat,_,_ in defenderStatsKeys[5:]:
    avgDefStats['Average ' + stat] = defAllStats[stat] / defAllStats['Apps']

### Average Mid Data to per game stats ###
avgMidStats = pd.DataFrame({'Name':midAllStats['Name'],
                            'Win rate':midAllStats['Wins'] / midAllStats['Apps'],
                            'Loss rate':midAllStats['Losses'] / midAllStats['Apps']})

for stat,_,_ in midfielderStatsKeys[5:]:
    avgMidStats['Average ' + stat] = midAllStats[stat] / midAllStats['Apps']
    
### Average Fwd Data to per game stats ###
avgFwdStats = pd.DataFrame({'Name':fwdAllStats['Name'],
                            'Win rate':fwdAllStats['Wins'] / fwdAllStats['Apps'],
                            'Loss rate':fwdAllStats['Losses'] / fwdAllStats['Apps']})

for stat,_,_ in forwardsStatsKeys[5:]:
    avgFwdStats['Average ' + stat] = fwdAllStats[stat] / fwdAllStats['Apps']

# save the dataframes to csv files
avgGKStats.to_csv('./data/scraped/avgGKStats.csv', index=False)
avgDefStats.to_csv('./data/scraped/avgDefStats.csv', index=False)
avgMidStats.to_csv('./data/scraped/avgMidStats.csv', index=False)
avgFwdStats.to_csv('./data/scraped/avgFwdStats.csv', index=False)