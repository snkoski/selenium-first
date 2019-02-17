from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

# players = ["Lebron James", "Kobe Bryant", "Tim Duncan", "Kevin Garnett", "Steve Nash", "Jason Kidd", "Chris Paul", "Kevin Durant", "Dirk Nowitzki", "James Harden", "Tracy McGrady", "Russell Westbrook", "Dwyane Wade", "Dwight Howard", "Stephen Curry"]
players = ["Kareem Abdul-Jabbar", "Nate Archibald", "Paul Arizin", "Charles Barkley", "Rick Barry", "Elgin Baylor", "Dave Bing", "Larry Bird", "Wilt Chamberlain", "Bob Cousy", "Dave Cowens", "Billy Cunningham", "Dave DeBusschere", "Clyde Drexler", "Julius Erving", "Patrick Ewing", "Walt Frazier", "George Gervin", "Hal Greer", "John Havlicek", "Elvin Hayes", "Magic Johnson", "Sam Jones", "Michael Jordan", "Jerry Lucas", "Karl Malone", "Moses Malone", "Pete Maravich", "Kevin McHale", "George Mikan", "Earl Monroe", "Hakeem Olajuwon", "Shaquille O'Neal", "Robert Parish", "Bob Pettit", "Scottie Pippen", "Willis Reed", "Oscar Robertson", "David Robinson", "Bill Russell", "Dolph Schayes", "Bill Sharman", "John Stockton", "Isiah Thomas", "Nate Thurmond", "Wes Unseld", "Bill Walton", "Jerry West", "Lenny Wilkens", "James Worthy"]
awardList = ["Player Name", "Hall Of Fame", "All Star", "Scoring Champ", "AST Champ", "STL Champ", "TRB Champ", "BLK Champ", "NBA Champ", "All-NBA", "All-Defensive", "ABA All-Time Team", "All-ABA", "All-Defensive", "All-Rookie", "Most Improved", "AS MVP", "Def. POY", "Finals MVP", "MVP", "Sith Man", "ROY"]
players_dict = {}
data_no = 0

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")

driver = webdriver.Chrome(executable_path='/Users/flatironschool/Desktop/chromedriver', chrome_options=option)

driver.get("https://www.basketball-reference.com/")

print(driver.title)

for player in players:
    awards_dict = {"Player Name": player}
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
    award_table = soup.find('ul', {"id":"bling"})
    awards = award_table.find_all('a')
    for award in awards:
        award = str(award)
        award = award[3:-4]
        if award != "Hall of Fame":
            award = re.sub(" ","*",award,1)
            award = re.sub("x","",award)
            award = award.split("*")
            if len(award[0]) > 2:
                award[0] = 1
            awards_dict[award[1]] = award[0]
        else:
            awards_dict["Hall Of Fame"] = 1
    print(awards_dict)
    for category in awardList:
        if category in awards_dict:
            playerList.append(awards_dict[category])
        else:
            playerList.append(0)
    players_dict[data_no] = playerList
    data_no += 1
print(players_dict)

player_awards_df = pd.DataFrame.from_dict(players_dict, orient = 'index', columns = ["Player Name", "Hall Of Fame", "All Star", "Scoring Champ", "AST Champ", "STL Champ", "TRB Champ", "BLK Champ", "NBA Champ", "All-NBA", "All-Defensive", "ABA All-Time Team", "All-ABA", "All-Defensive", "All-Rookie", "Most Improved", "AS MVP", "Def. POY", "Finals MVP", "MVP", "Sixth Man", "ROY"])
                        # print(npo_all_player_games_df.head())
player_awards_df.to_csv('top_50_player_awards_df.csv')
