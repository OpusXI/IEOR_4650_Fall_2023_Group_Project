from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import re
import time
import csv
from tqdm import tqdm

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

def scrapeTeamLinks():
    premierLeagueSummaryPage = "https://www.transfermarkt.us/premier-league/marktwerteverein/wettbewerb/GB1"

    premierLeagueSummaryPageRequest = requests.get(premierLeagueSummaryPage, headers=headers)
    premierLeagueSummaryPageSoup = BeautifulSoup(premierLeagueSummaryPageRequest.text, "html.parser")

    # Extract all team links from the summary page table
    teamRosterLinks = []

    for link in premierLeagueSummaryPageSoup.find_all('a', href=True):
        if re.match(r'/\S+/startseite/verein/\d+/saison_id/\d+', link['href']):
            # replace the 2022 in the link with 2021 to get the 2021/2022 season
            link = link['href'].replace('2022', '2021')
            teamRosterLinks.append(link)
        
        uniqueTeamRosterLinks = np.unique(teamRosterLinks)
            
        
    return uniqueTeamRosterLinks

def scrapePlayerValues(teamRosterLinks):
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
                if not player_name:
                    player_name = player_name_cell.find("a", {"title": True})
                if player_name:
                    player_info.append(player_name["title"])

            # Extract market value
            market_value = row.find("td", {"class": "rechts hauptlink"})
            if market_value:
                player_info.append(convert_market_value(market_value.text.strip()))

            if len(player_info) == 2:
                playerData.append(player_info)

            time.sleep(0.25)

    with open('./data/salaries/marketValues.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for player in playerData:
            writer.writerow(player)

    return playerData

        
teamLinks = scrapeTeamLinks()
# print(teamLinks)
scrapePlayerValues(teamLinks)
