from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

players = ["Lebron James", "Kobe Bryant", "Tim Duncan", "Kevin Garnett", "Steve Nash", "Jason Kidd", "Chris Paul", "Kevin Durant", "Dirk Nowitzki", "James Harden", "Tracy McGrady", "Russell Westbrook", "Dwyane Wade", "Dwight Howard", "Stephen Curry"]
# players = ["Kareem Abdul-Jabbar", "Nate Archibald", "Paul Arizin", "Charles Barkley", "Rick Barry", "Elgin Baylor", "Dave Bing", "Larry Bird", "Wilt Chamberlain", "Bob Cousy", "Dave Cowens", "Billy Cunningham", "Dave DeBusschere", "Clyde Drexler", "Julius Erving", "Patrick Ewing", "Walt Frazier", "George Gervin", "Hal Greer", "John Havlicek", "Elvin Hayes", "Magic Johnson", "Sam Jones", "Michael Jordan", "Jerry Lucas", "Karl Malone", "Moses Malone", "Pete Maravich", "Kevin McHale", "George Mikan", "Earl Monroe", "Hakeem Olajuwon", "Shaquille O'Neal", "Robert Parish", "Bob Pettit", "Scottie Pippen", "Willis Reed", "Oscar Robertson", "David Robinson", "Bill Russell", "Dolph Schayes", "Bill Sharman", "John Stockton", "Isiah Thomas", "Nate Thurmond", "Wes Unseld", "Bill Walton", "Jerry West", "Lenny Wilkens", "James Worthy"]

# players = ["Kareem Abdul-Jabbar", "Nate Archibald", "Paul Arizin", "Charles Barkley"]
statList = ["Player Name", "G", "PTS", "TRB", "AST", "FG%", "FG3%", "FT%", "eFG%", "PER", "WS"]
players_dict = {}
data_no = 0

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")

driver = webdriver.Chrome(executable_path='/Users/flatironschool/Desktop/chromedriver', chrome_options=option)

driver.get("https://www.basketball-reference.com/")

print(driver.title)

for player in players:
    stats_dict = {"Player Name": player}
    career_stats = []
    playerList = []
    inputElement = driver.find_element_by_name("search")

    inputElement.send_keys(player)

    inputElement.submit()

    url = driver.current_url
    print("URL", url)
    if url[-4:] != "html":
        playerLink = driver.find_element_by_partial_link_text(player)
        playerLink.click()
        url = driver.current_url
    response = requests.get(url)
    data = response.text
    soup = bs(data, 'html.parser')
    stats_table = soup.find('div', {"class":"stats_pullout"})
    stats_div = stats_table.find_all('div')
    for div in stats_div:
        h = div.find('h4')
        paragraphs = div.find_all('p')
        for p in paragraphs:
            stats_dict[h.text] = p.text
    for category in statList:
        if category in stats_dict:
            career_stats.append(stats_dict[category])
        else:
            career_stats.append(0)
    players_dict[data_no] = career_stats
    data_no += 1
print(players_dict)

career_stats_df = pd.DataFrame.from_dict(players_dict, orient = 'index', columns = ["Player Name", "G", "PTS", "TRB", "AST", "FG%", "FG3%", "FT%", "eFG%", "PER", "WS"])
                        # print(npo_all_player_games_df.head())
career_stats_df.to_csv('recent_career_stats_df.csv')
