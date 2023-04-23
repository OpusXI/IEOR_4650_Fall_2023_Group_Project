import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

PATH = "/Applications/chromedriver"
driver = webdriver.Chrome(PATH)

baseSpotRacURL = "https://www.spotrac.com/epl/rankings/"
yearsToScrape = ["2017/", "2018/", "2019/", "2020/", "2021/"]

def createDataFrame(data, year):
    df = pd.DataFrame(data, columns=["Player", "Salary"])
    df['Year'] = year
    return df

def convertSalaryToInt(salary_string):
    salary_string = salary_string.replace("£", "").replace(",", "").strip()
    return int(salary_string)

def scrapePlayerSalaries(baseURL, yearToScrape, driver):
    requestURL = baseURL + yearToScrape
    # salaryRequest = requests.get(requestURL)
    driver.get(requestURL)
    time.sleep(10)
    salarySoup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    # print(salarySoup)
    
    # Extract all player names and salaries pairwise from the table
    salaryTableBody = salarySoup.find('tbody')
    rows = salaryTableBody.find_all('tr')
    playerSalaries = []
    
    for row in rows:
        # print(row)
        playerName = row.find('h3').find('a').text.strip()
        salary = row.find("td", class_="rank-value").text.strip()
        
        playerSalaries.append([playerName, convertSalaryToInt(salary)])
    
    return playerSalaries

def outputToCSV(year):
    yearToScrape = year + "/"
    data = scrapePlayerSalaries(baseSpotRacURL, yearToScrape, driver)
    df = createDataFrame(data, year)
    df.to_csv(f"./data/salaries/spotracScrapes/scrapedSalaries{year}.csv", index=False)

# change this for whatever year you want to scrape
# outputToCSV("2021")

# import all the csvs into dataframes
df2017 = pd.read_csv('./data/salaries/spotracScrapes/scrapedSalaries2017.csv')
df2018 = pd.read_csv('./data/salaries/spotracScrapes/scrapedSalaries2018.csv')
df2019 = pd.read_csv('./data/salaries/spotracScrapes/scrapedSalaries2019.csv')
df2020 = pd.read_csv('./data/salaries/spotracScrapes/scrapedSalaries2020.csv')
df2021 = pd.read_csv('./data/salaries/spotracScrapes/scrapedSalaries2021.csv')

combinedDF = pd.concat([df2017, df2018, df2019, df2020, df2021], ignore_index=True)

playerSalaryDatabase = combinedDF.sort_values(['Year', 'Player'], ascending=[False, True])

def keepMostRecentNonZeroSalary(df):
    groupedDataframe = df.groupby('Player')
    result = []
    
    for name, group in groupedDataframe:
        nonZeroSalaries = group[group['Salary'] != 0]
        
        if not nonZeroSalaries.empty:
            mostRecentNonZero = nonZeroSalaries.iloc[0]
            result.append(mostRecentNonZero)
        else:
            mostRecent = group.iloc[0]
            result.append(mostRecent)
    
    return pd.DataFrame(result)

playerSalaryDatabaseFiltered = keepMostRecentNonZeroSalary(playerSalaryDatabase)
playerSalaryDatabaseFiltered.reset_index(drop=True, inplace=True)
playerSalaryDatabaseFiltered.to_csv('./data/salaries/scrapedSalaries.csv', index=False)