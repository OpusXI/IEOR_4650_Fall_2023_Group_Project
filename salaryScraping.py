# Import all the modules required.
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model, model_selection
import time

from dataScraping import namesWithoutAccent

salarySiteRequest = requests.get("https://www.spotrac.com/epl/")
salarySoup = BeautifulSoup(salarySiteRequest.text, 'html.parser')

payroll_links = []
clubs = []

for club in salarySoup.find_all('div', attrs = {'class':'teamname'}):
    clubs.append(club.text.strip())
print("Scraped Club Links")
for paylink in salarySoup.find_all('div', attrs = {'class':'teamoption'}):
    if 'Payroll' in paylink.find('a').text:
        payroll_links.append(paylink.find('a')['href'])
print("Scraped Payroll Links")
        
# Now make a list with the payroll of each club. Also want to make a list of all the player's wages
club_payrolls = []
players = []
player_wages = []

for paylink in payroll_links:
    salaryLinkReq = requests.get(paylink)
    indivSalarySoup = BeautifulSoup(salaryLinkReq.text, 'html.parser')
    club_payroll = indivSalarySoup.find_all('td', attrs = {'class':'captotal'})[4].text
    # Remove the £ sign and the , from the salary, and then convert to an int
    club_payroll_int = int(club_payroll.replace('£', '').replace(',', ''))
    club_payrolls.append(club_payroll_int)
    
    for i in range(len(indivSalarySoup.find_all('td', attrs = {'class':'result center'}))):
        player = indivSalarySoup.find_all('td', attrs = {'class':'player'})[2*i].find('a').text
        players.append(player)
        playerWage = indivSalarySoup.find_all('td', attrs = {'class':'result center'})[i].text
        # Remove the £ sign and the , from the salary, and then convert to an int, if it's a '-' then make it 0
        if playerWage == '- ':
            playerWageInt = 'NA'
        else:
            playerWageInt = int(playerWage.replace('£', '').replace(',', ''))
        player_wages.append(playerWageInt) 
        print(f"Scraped: {paylink} - {player} - {playerWage}")
    time.sleep(0.25)
    
# Now we have all the data we need, we can make a dataframe for each list and then merge them
payrolls = pd.DataFrame({'Club':clubs, 'Anual Payroll':club_payrolls})
salaries = pd.DataFrame({'Player':players, 'Annual salary':player_wages})

# only keep the players we have data for from the other database
filteredPlayers = []
filteredWages = []
for player in namesWithoutAccent:
    if player in players:
        filteredPlayers.append(player)
        filteredWages.append(player_wages[players.index(player)])

filteredSalaries = pd.DataFrame({'Player':filteredPlayers, 'Annual salary':filteredWages})

# Save the dataframes to CSV files
payrolls.to_csv("./data/salaries/club_spending.csv", index=False)
salaries.to_csv("./data/salaries/player_salaries.csv", index=False)
filteredSalaries.to_csv("./data/salaries/filtered_player_salaries.csv", index=False)
