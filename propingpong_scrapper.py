from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime as datetime
import random
import re
import os
from os import walk


def initDriver(url):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver', port = 5938)
    driver.get(url)
    #time.sleep(2) # Let the user actually see something!
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
                
def updateRusPlayers(mw, driver):
    playersDict = dict()
    playersDictInv = dict()
    with open('data/propingpong/propingpong_players_' + mw + '.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            tokens = [e.strip() for e in tokens]
            if len(tokens[1]) > 0:
                playersDict[tokens[1]] = tokens[0]
            playersDictInv[tokens[0]] = tokens[1:]

    table = driver.find_elements_by_xpath('//*//table[@class = "main"][@width="98%"]')

    s = table[0].get_attribute('outerHTML')
#    print(s[:200])
#    print(len(s))
    indexesPlayers = [[m.start(), m.end(), 0] for m in re.finditer('<a href=\"profile.php(.)*</a>', s)]
    for e in indexesPlayers:
        href = s[e[0]:e[1]]
        tokens = href.split('"')
        playerId = tokens[1].split('=')[1].strip()
        tokens1 = href.split('>')
        playerName = tokens1[1].split('<')[0].strip()
        if not (playerId in playersDict):
            print((playerId, playerName))
            playersDict[playerId] = playerName  

        if playerName in playersDictInv:
            if playersDictInv[playerName][0] == '':
                playersDictInv[playerName][0] = playerId
            elif playersDictInv[playerName][0] != playerId:
                print('COLLISION: ' + playerName + '\t' + playersDictInv[playerName][0] + '\t' + playerId)
        else:
            playersDictInv[playerName] = [playerId, '']

    with open('data/propingpong/propingpong_players_' + mw + '.txt', 'w', encoding='utf-8') as fout:
        for k,v in sorted(playersDictInv.items(), key = lambda x: x[1][0] + '_' + x[1][1]):
            fout.write(k + '\t' + '\t'.join(v) + '\n')

    return playersDict


def updateIttfPlayers(mw, driver):
    playersDict = dict()
    playersDictInv = dict()
    with open('data/propingpong/propingpong_players_' + mw + '.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            tokens = [e.strip() for e in tokens]
            if len(tokens[2]) > 0:
                playersDict[tokens[2]] = tokens[0]
            playersDictInv[tokens[0]] = tokens[1:]

    namesList = []
    for i in range(2):
        table = driver.find_elements_by_xpath('//*//table[@class = "main"][@width="98%"]')
        s = table[0].get_attribute('outerHTML')
        #print(s[:200])
        #print(len(s))
        indexesPlayers = [[m.start(), m.end(), 0] for m in re.finditer('<a href=\"profile.php(.)*</a>', s)]
        for j,e in enumerate(indexesPlayers):
            href = s[e[0]:e[1]]
            tokens = href.split('"')
            playerId = tokens[1].split('=')[1]
            tokens1 = href.split('>')
            playerName = tokens1[1].split('<')[0]
            if i == 0:
                namesList.append([playerName, ''])
            else:
                namesList[j][1] = playerName
            if not (playerId in playersDict):
                print((playerId, playerName))
                playersDict[playerId] = playerName
            if playerName in playersDictInv:
                if playersDictInv[playerName][1] == '':
                    playersDictInv[playerName][1] = playerId
                elif playersDictInv[playerName][1] != playerId:
                    print('COLLISION: ' + playerName + '\t' + playersDictInv[playerName][1] + '\t' + playerId)
            else:
                playersDictInv[playerName] = ['', playerId]
        driver.find_element_by_xpath('//*//a[@class = "setenglang"]').click()

    for e in namesList:
        for i in range(2):
            if playersDictInv[e[0]][i] == '':
                if playersDictInv[e[1]][i] != '':
                    playersDictInv[e[0]][i] = playersDictInv[e[1]][i]
            else:
                if playersDictInv[e[1]][i] == '':
                    playersDictInv[e[1]][i] = playersDictInv[e[0]][i]
                else:
                    if playersDictInv[e[1]][i] != playersDictInv[e[0]][i]:
                        print('COLLISION: ' + e[0] + '\t' + playersDictInv[e[0]][i] + '\t' + e[1] + '\t' + playersDictInv[e[1]][i])

    with open('data/propingpong/propingpong_players_' + mw + '.txt', 'w', encoding='utf-8') as fout:
        for k,v in sorted(playersDictInv.items(), key = lambda x: x[1][0] + '_' + x[1][1]):
            if len(k) > 0:
                fout.write(k + '\t' + '\t'.join(v) + '\n')
    return playersDict

#def readPlayersRankings(mw, playersDict):
def readPlayersRankings():
    playersRankings = dict()
    for f in os.listdir('data/propingpong/ranking_rus'):
        with open('data/propingpong/ranking_rus/' + f, 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                tokens = [e.strip() for e in tokens]
                playersRankings[f[:7] + '\t' + tokens[0]] = line
    return playersRankings

months = dict(zip(['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
                  list(range(1,13))))

def updateRusRankings(mw, driver, playersRankings):
    table = driver.find_elements_by_xpath('//*//table[@class = "main"][@width="98%"]')
    
    s = table[0].get_attribute('outerHTML')
    print(s[:200])
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

        try:
            driver.get(url)
            table = driver.find_elements_by_xpath('//*//table[@class = "main"]')
        except:
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
                with open('data/propingpong/ranking_rus/' + idate + '_' + mw + '.txt', 'a', encoding='utf-8') as fout:
                    fout.write(playerId + '\t' + rt + '\t' + rg + '\n')
#        break

def updateRusRanking():
    playersRankings = readPlayersRankings()
    for mw in ['men', 'women']:
        #    for mw in ['women']:
        url = 'http://propingpong.ru/rating_rf.php?gender=' + str(int(mw == 'men')) + '&&page=1'
        driver = initDriver(url)
        playersDict = updateRusPlayers(mw, driver)
        #continue
        print('updateRankings')
        updateRusRankings(mw, driver, playersRankings)
        driver.quit()

def getIttfRankings(mw, driver, year, month):
    tds = driver.find_elements_by_xpath('//*//table[@class = "main"][@width="98%"]//tr//td')
    playerId = None
    playerRating = None
    res = dict()
    ths = driver.find_elements_by_xpath('//*//table[@class = "main"][@width="98%"]//tr//th')
    numCols = 8
    indName = 4
    indR = 7
    if len(ths) == 7:
        numCols = 10
        indName = 5
        indR = 8
    for i,td in enumerate(tds[4:]):
#        print(i, td.get_attribute('innerHTML')[:100].replace('\n', ' '))
        if i % numCols == indName:
            try:
                playerId = td.get_attribute('innerHTML').split('ittfid=')[1].split('">')[0]
            except:
                playerId = None
        if i % numCols == indR:
            if not (playerId is None):
                playerRating = int(td.get_attribute('innerHTML'))
                res[playerId] = playerRating
#            print((playerId, playerRating))
    return res

def updateIttfRanking():
    curDate = datetime.datetime.now().date().strftime("%Y-%m-%d")
    for mw in ['men', 'women']:
#    for mw in ['men']:
        #    for mw in ['women']:
        for year in range(2001,2018):
            for month in range(1, 13):
                if str(year) + '-' + str(month).zfill(2) >= curDate:
                    break
                filename = 'data/propingpong/ranking_ittf/' + str(year) + '-' + str(month).zfill(2) + '_' + mw + '.txt'
                if not os.path.exists(filename):
                    url = 'http://propingpong.ru/rating_ittf.php?gender=' + str(int(mw == 'men')) + '&&page=1&sortby=undefined&year=' + str(year - 1) + '&month=' + str(month)
                    driver = initDriver(url)
                    playersDict = updateIttfPlayers(mw, driver)
                    r = getIttfRankings(mw, driver, year, month)
                    with open(filename, 'w', encoding='utf-8') as fout:
                        lastR = -1
                        rank = 0
                        i = 0
                        for k,v in sorted(r.items(), key = lambda x: -x[1]):
                            i += 1
                            if lastR != v:
                                rank = i
                                lastR = v
                            fout.write('\t'.join([k, str(v), str(rank)]) + '\n')
                    driver.quit()
                '''
                else:
                    r = dict()
                    with open(filename, 'r', encoding='utf-8') as fin:
                        for line in fin:
                            tokens = line.strip().split('\t')
                            r[tokens[0]] = int(tokens[1])

                    with open(filename, 'w', encoding='utf-8') as fout:
                        lastR = -1
                        rank = 0
                        i = 0
                        for k,v in sorted(r.items(), key = lambda x: -x[1]):
                            i += 1
                            if lastR != v:
                                rank = i
                                lastR = v
                            fout.write('\t'.join([k, str(v), str(rank)]) + '\n')
                '''


def main():

    updateIttfRanking()
    updateRusRanking()


    '''
    for f in walk('data/propingpong/ranking_rus'):
        for ff in f[2]:
            print(ff)
            lines = []
            with open('data/propingpong/ranking_rus/' + ff) as fin:
                for line in fin:
                    lines.append(line)
            with open('data/propingpong/ranking_rus/' + ff, 'w', encoding = 'utf-8') as fout:
                for line in lines:
                    fout.write(line)
    '''


if __name__ == "__main__":
    main()