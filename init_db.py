import requests
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


def get_team_urls(url):
    # 리그별 팀 리스트 웹스크래핑 해오기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    divs = soup.select('#teamList > ul.list_teamplayer > li')

    team_urls = []
    for div in divs:
        a = div.select_one('div > a')
        if a is not None:
            base_url = 'https://sports.daum.net/'
            url = base_url + a['href']
            team_urls.append(url)
    # print(teams_url)
    return team_urls


def get_player_urls(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome('/Users/user/Downloads/chromedriver', options=options)
    # driver.implicitly_wait(3)없애도 잘 작동됨
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.select('#teamViewSquadWrap> ul >li ')

    # print(divs)
    # # teamList > ul.list_teamplayer > li:nth-child(2) > div > div > a:nth-child(2)
    # teamViewSquadWrap > ul:nth-child(2) > li:nth-child(3) > a > div > strong
    # teamViewSquadWrap > ul:nth-child(2) > li:nth-child(3) > a > div > strong
    # teamViewSquadWrap > ul:nth-child(2) > li:nth-child(1) > a > div > strong
    players_url = []
    for div in divs:
        a = div.select_one('a.link_thumb')
        # print(a)
        if a is not None:
            base_url = 'https://sports.daum.net'
            url = base_url + a['href']
            players_url.append(url)
    # print(players_url)
    return players_url


def get_player_info(url):
    # 선수 url에 접근해서 웹스크래핑으로 선수 정보 가져온다
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    img_url = soup.select_one('#playerInfo > div.basic_feature > span > span.info_thumb > img')['src']
    name = soup.select_one('#playerInfo > div.basic_feature > div > h4').text
    position = soup.select_one(
        '#playerInfo > div.basic_feature > div > div.info_detail > div:nth-child(2) > dl:nth-child(1) > dd').text
    #news = soup.select_one('#viewNews > div > ul:nth-child(2) > li > div > strong').text
    # playerInfo > div.basic_feature > span > span.info_thumb > img
    # viewNews > div > ul:nth-child(2) > li > div > strong > a
    # viewNews > div > ul:nth-child(2) > li > div > strong
    feature = soup.find('dl', class_='list_condition')
    if feature is None:
        match = '0'
        goal = '0'
        assi = '0'
    else:
        match = soup.select_one('#playerInfo > div.condition_feature > div > dl:nth-child(1) > dd').text
        goal = soup.select_one('#playerInfo > div.condition_feature > div > dl:nth-child(2) > dd').text
        assi = soup.select_one('#playerInfo > div.condition_feature > div > dl:nth-child(3) > dd').text


    player_info = {
        'img_url': img_url,
        'name': name,
        'position': position,
        'match': match,
        'goal': goal,
        'assi': assi,
        #'news': news,
        'like': 0,
        'pre_like':0

    }


    #print(news)

    db.myfantasystar.insert_one(player_info)



## 실행하기 (리그 추가하기)
league_urls = ['https://sports.daum.net/team/epl']
for league in league_urls:
    team_urls = get_team_urls(league)
    for team in team_urls:
        player_urls = get_player_urls(team)
        for player in player_urls:
            # print(player)
            get_player_info(player)



# get_player_info('https://sports.daum.net/player/epl/17102/news#1')
