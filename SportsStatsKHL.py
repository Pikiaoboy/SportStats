import csv
from selenium import webdriver
from bs4 import BeautifulSoup,Comment
import time 
import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

#Set website base url
base_url = "http://www.sportstats.com/hockey/russia/khl/"
season_url = "http://www.sportstats.com"
# sport="Australian Rules"

#Set output location
base_file = "C:\\Temp\\Results\\SportStats-Output\\"
DB_KHL=base_file+"DB_KHL-2.csv"

#Initialise file
with open(DB_KHL,'w') as f:
    f.write("Date,Home Team, Away Team, Result,Total\n")



#function to change pages
def next_page(page_number):
    #Move to next page
    print("In page function - loading " +str(page_number))
    driver.find_element_by_class_name("table-paging").find_elements_by_tag_name('a')[page_number].click() 
    time.sleep(3)
    return

def next_season(season_number):
    #Move to next page
    print("In season function - loading " + season_links[season_number].text.strip())
    season_link=season_links[season_number].get('href')
    driver.get(season_url+season_link)
    time.sleep(6)
    driver.find_element_by_link_text("Main").click()
    time.sleep(3)
    return

#load browser driver 
driver = webdriver.Chrome()
driver.get(base_url)
driver.find_element_by_link_text("Results").click()
time.sleep(3)
driver.find_element_by_link_text("Main").click()
time.sleep(3)


#Total number of pages and seasons

season_link_total=len(driver.find_element_by_xpath("//div[@class='season stages']").find_elements_by_tag_name('a'))



#results loop would start here

#season loop
for season_num in range(1, season_link_total):
    #loop for seasons
    soup=BeautifulSoup(driver.page_source, 'lxml')
    season_links=soup.find("div",class_="season stages").find_all("a")
    #match_soup=soup.find("div",class_="tableShadow")
    page_link_total=len(driver.find_element_by_class_name("table-paging").find_elements_by_tag_name('a') )
    #page_links=soup.find("div",class_="table-paging").find_all("a")
    print("Season "+str(season_num)+" loading")

    #page loop
    for page_num in range (1, page_link_total):
    #for page_num in range (1, 2):
        next_page(page_num)

    page_soup=BeautifulSoup(driver.page_source, 'lxml')
    matches_soup=page_soup.find("div",class_="tableShadow")
    print("Page " + str(page_num) + " loaded")
    game_dates = matches_soup.find_all("tr",class_="table-league-header")
    match_group_stats = matches_soup.find_all("tbody")

    for i in range(0,len(match_group_stats)-1):
        game_date=game_dates[i].th.span.text.strip()
        match_stats = match_group_stats[i]
        home_teams=match_stats.find_all("td", class_="table-home")
        away_teams=match_stats.find_all("td", class_="table-away")
        results_teams=match_stats.find_all("td", class_="result-neutral")
        for x in range(0,len(home_teams)-1):
            with open(DB_KHL, 'a') as a:
                a.write(game_date[4:]+","+home_teams[x].text+","+away_teams[x].text+","+results_teams[x].text+","+str(sum(map(int,re.sub("\D","",results_teams[x].text))))+"\n")
                #print(game_date[4:]+","+home_teams[i].text+","+results_teams[i].text+","+away_teams[i].text)

    next_season(season_num)
#results loop will end here


print("Complete")



