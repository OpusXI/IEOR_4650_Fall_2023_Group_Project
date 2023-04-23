from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import re
import time
import csv
from tqdm import tqdm
from unidecode import unidecode

headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def convert_market_value(value):
    value = value.replace("€", "").strip()
    multiplier = 1

    if "m" in value:
        multiplier = 1000000
        value = value.replace("m", "")
    elif "k" in value:
        multiplier = 1000
        value = value.replace("k", "")

    try:
        value = int(float(value) * multiplier)
    except ValueError:
        value = None

    return value

def scrapeTeamLinks(year):
    premierLeagueSummaryPage = "https://www.transfermarkt.us/premier-league/marktwerteverein/wettbewerb/GB1"

    premierLeagueSummaryPageRequest = requests.get(premierLeagueSummaryPage, headers=headers)
    premierLeagueSummaryPageSoup = BeautifulSoup(premierLeagueSummaryPageRequest.text, "html.parser")

    # Extract all team links from the summary page table
    teamRosterLinks = []

    for link in premierLeagueSummaryPageSoup.find_all('a', href=True):
        if re.match(r'/\S+/startseite/verein/\d+/saison_id/\d+', link['href']):
            # replace the 2022 in the link with 2021 to get the 2021/2022 season
            link = link['href'].replace('2022', f'{year}')
            teamRosterLinks.append(link)
        
        uniqueTeamRosterLinks = np.unique(teamRosterLinks)
            
        
    return uniqueTeamRosterLinks

def scrapePlayerValues(teamRosterLinks, year):
    playerData = []
    for link in tqdm(teamRosterLinks, desc="Scraping team rosters", ncols=100):
        requestLink = "https://www.transfermarkt.us" + link
        teamRequest = requests.get(requestLink, headers=headers)
        teamSoup = BeautifulSoup(teamRequest.text, "html.parser")
        playerTable = teamSoup.find("table", {"class": "items"})
        playerRows = playerTable.find_all("tr")

        for row in playerRows:
            player_info = []

            # Extract player name
            player_name_cell = row.find("td", {"class": "hauptlink"})
            if player_name_cell:
                player_name = player_name_cell.find("a", {"title": True}, recursive=False)
                try:
                    player_name = unidecode(player_name)
                except AttributeError:
                    pass
                if not player_name:
                    player_name = player_name_cell.find("a", {"title": True})
                    player_name = unidecode(player_name)
                if player_name:
                    player_info.append(player_name["title"])

            # Extract market value
            market_value = row.find("td", {"class": "rechts hauptlink"})
            if market_value:
                player_info.append(convert_market_value(market_value.text.strip()))

            if len(player_info) == 2:
                playerData.append(player_info)

            time.sleep(0.25)

    playerDataframe = pd.DataFrame(playerData, columns=['full_name', 'market_value'])
    playerDataframe['year'] = year

    return playerDataframe

def keepMostRecentNonZeroSalary(df):
    groupedDataframe = df.groupby('full_name')
    result = []
    
    for name, group in groupedDataframe:
        nonZeroSalaries = group[group['market_value'] != 0]
        
        if not nonZeroSalaries.empty:
            mostRecentNonZero = nonZeroSalaries.iloc[0]
            result.append(mostRecentNonZero)
        else:
            mostRecent = group.iloc[0]
            result.append(mostRecent)
    
    return pd.DataFrame(result)

scrape = True
concat = True

if scrape:    
    teamLinks2021 = scrapeTeamLinks('2021')
    data2021 = scrapePlayerValues(teamLinks2021, "2021")

    teamLinks2020 = scrapeTeamLinks('2020')
    data2020 = scrapePlayerValues(teamLinks2020, "2020")

    teamLinks2019 = scrapeTeamLinks('2019')
    data2019 = scrapePlayerValues(teamLinks2019, "2019")
    
    teamLinks2018 = scrapeTeamLinks('2018')
    data2018 = scrapePlayerValues(teamLinks2019, "2018")
    
    teamLinks2017 = scrapeTeamLinks('2017')
    data2017 = scrapePlayerValues(teamLinks2019, "2017")
    
if concat:
    mvDatabase = pd.concat([data2021, data2020, data2019, data2018, data2017])
    finalDatabase = keepMostRecentNonZeroSalary(mvDatabase)
    finalDatabase.to_csv('./data/salaries/marketValueDatabase.csv', index=False)
