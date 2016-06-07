from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime as datetime
import random
import re
import os


def initDriver(url):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver', port = 5938)
    driver.get(url)
#    time.sleep(random.random()) # Let the user actually see something!
    return driver

'''
def scrappTournament(curDate, url):
    
    if type(table) is list:
        table = table[0]
    trs = table.find_elements(By.TAG_NAME, "tr")
    k = 0 
    dt = ''
    lines1 = []
    for tr in trs:
        k += 1
        if k == 1:
            continue
        s = tr.get_attribute('outerHTML')
        if s.find('sheduleTableSeparator') != -1:
            sdt = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute('innerHTML')
            dt = datetime.datetime.strptime(sdt, "%d.%m.%Y").date().strftime("%Y-%m-%d")
            print(dt)
        else:
            tds = tr.find_elements(By.TAG_NAME, "td")
            tt = tds[0].get_attribute('innerHTML')
            p1 = tds[2].find_elements(By.TAG_NAME, "a")[0].get_attribute('innerHTML')
            p2 = tds[3].find_elements(By.TAG_NAME, "a")[0].get_attribute('innerHTML')
            sets_score = tds[4].get_attribute('innerHTML')
            match_score = tds[5].get_attribute('innerHTML')
            lines1.append(dt + '\t' + tt + '\t' + p1 + '\t' + p2 + '\t' + sets_score + '\t' + match_score + '\n')
            lines2.append(sets_score)
            print(dt + ' ' + tt + '\t' + p1 + '\t' + p2 + '\t' + sets_score + '\t' + match_score)

    driver.close()
'''    
                
def updatePlayers(mw, driver):
    playersDict = dict()
    with open('data/propingpong/propingpong_players_' + mw + '.txt', 'r') as fin:
        for line in fin:
            tokens = line.split('\t')
            tokens = [e.strip() for e in tokens]
            playersDict[tokens[0]] = tokens[1]

    table = driver.find_elements_by_xpath('//*//table[@class = "main"]')

#    return playersDict
    
    s = table[1].get_attribute('outerHTML')
#    print(s[:200])
#    print(len(s))
    indexesPlayers = [[m.start(), m.end(), 0] for m in re.finditer('<a href=\"profile.php(.)*</a>', s)]
    for e in indexesPlayers:
        href = s[e[0]:e[1]]
        tokens = href.split('"')
        playerId = tokens[1].split('=')[1]
        tokens1 = href.split('>')
        playerName = tokens1[1].split('<')[0]
        if not (playerId in playersDict):
            print((playerId, playerName))
            playersDict[playerId] = playerName  
            with open('data/propingpong/propingpong_players_' + mw + '.txt', 'a') as fout:
                fout.write(playerId + '\t' + playerName + '\n')
    return playersDict
                
def getPlayersRankings(mw, playersDict):
    playersRankings = dict()
    for f in os.listdir('data/propingpong/ranking_rus'):
        with open('data/propingpong/ranking_rus/' + f, 'r') as fin:
            for line in fin:
                tokens = line.split('\t')
                tokens = [e.strip() for e in tokens]
                playersRankings[f[:7] + '\t' + tokens[0]] = line
    return playersRankings

months = dict(zip(['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'], list(range(1,13))))

def updateRankings(mw, driver, playersRankings):
    table = driver.find_elements_by_xpath('//*//table[@class = "main"]')
    
    s = table[1].get_attribute('outerHTML')
#    print(s[:200])
#    print(len(s))
    indexesPlayers = [[m.start(), m.end(), 0] for m in re.finditer('<a href=\"profile.php(.)*</a>', s)]
    for e in indexesPlayers:
        href = s[e[0]:e[1]]
        print(href)
        tokens = href.split('"')
        playerId = tokens[1].split('=')[1]
        url = 'http://propingpong.ru/alldata.php?player=' + playerId
        tokens1 = href.split('>')
        playerName = tokens1[1].split('<')[0]

        driver.get(url)
        table = driver.find_elements_by_xpath('//*//table[@class = "main"]')
        tr = table[1].find_element_by_xpath('//tr')
#        for tr in trs:
        tds = tr.find_elements_by_xpath('//td[@class = "main"]') + tr.find_elements_by_xpath('//td[@class = "mainempty"]') 
        for i in range(0, len(tds), 4):
            print(i)
            idate = tds[i].text + '-' + str(months[tds[i + 1].text]).zfill(2)
            rt = tds[i + 2].text
            rg = tds[i + 3].text
            key = idate + '\t' + playerId
            print(idate + '\t' + playerId + '\t' + rt + '\t' + rg)
            if not (key in playersRankings):
                print(playerId + '\t' + rt + '\t' + rg)
                with open('data/propingpong/ranking_rus/' + idate + '_' + mw + '.txt', 'a') as fout:
                    fout.write(playerId + '\t' + rt + '\t' + rg + '\n')
#        break
    
    
def main():

    for mw in ['men', 'women']:
        url = 'http://propingpong.ru/rating_rf.php?gender=' + str(int(mw == 'men')) + '&&page=1'
        driver = initDriver(url)
        playersDict = updatePlayers(mw, driver)
        playersRankings = getPlayersRankings(mw, playersDict)
        updateRankings(mw, driver, playersRankings)
        driver.quit()        

    

if __name__ == "__main__":
    main()