from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime as datetime
import random
import re
import os
from os import walk
from common import *


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

        tds = table[1].find_element_by_xpath('//tr//td')
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

'''
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
'''

def getLastRusRankings(mw):
    url = 'http://propingpong.ru/rating_rf.php?gender=' + str(int(mw == 'men')) + '&settlement=&settlement=&area=&year=0&page=1'
    try:
        driver = initDriver(url)
        pagesCnt = int(driver.find_elements_by_xpath('//*[@class = "pagination"]')[0].find_elements(By.TAG_NAME, 'a')[-2].get_attribute('innerHTML'))
    except:
        driver = initDriver(url)
        pagesCnt = int(driver.find_elements_by_xpath('//*[@class = "pagination"]')[0].find_elements(By.TAG_NAME, 'a')[-2].get_attribute('innerHTML'))

    print(pagesCnt)

    rankings = dict()
    rusid2names = dict()
    ids = set()
    for page in range(1, pagesCnt + 1):
        try:
            driver.get(url + '&page=' + str(page))
        except:
            driver = initDriver(url + '&page=' + str(page))

        rows = driver.find_elements_by_xpath('//table[@id="rightarea"]//div[@class="table"]//div[@class="row"]')
        for i,row in enumerate(rows[1:]):
            s = row.find_elements_by_xpath('./div[@class="cell-val"]')[0].get_attribute('innerHTML')
#            print(s)
#            continue
            arr = s.split('id=')
#            if len(arr) < 2:
#                print(s)
#                continue
            playerId = arr[1].split('">')[0]
            playerName = arr[1].split('>')[1].split('<')[0]
            playerRating = int(row.find_elements_by_xpath('./div[@class="cell"]')[4].get_attribute('innerHTML'))
            #print([playerId, playerName, playerRating])
            rankings[playerId] = playerRating
            if not (playerId in rusid2names):
                rusid2names[playerId] = []
            if not (playerName in rusid2names[playerId]):
                rusid2names[playerId].append(playerName)
            if playerId in ids:
                print([page, playerName])
            ids.add(playerId)
        print([page, len(rankings)])
        #break
    driver.quit()
    return [rankings, rusid2names]

def updateRusRanking(year, month):
    for mw in ['men', 'women']:
        rusId2names = dict()
        with open('data/propingpong/propingpong_rusId2names_' + mw + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                rusId2names[tokens[0]] = tokens[1].strip().split(';')

        filename = 'data/propingpong/ranking_rus/' + str(year) + '-' + str(month).zfill(2) + '_' + mw + '.txt'
        if not os.path.exists(filename):
            rankings, year_month_rusid2names = getLastRusRankings(mw)

            for id,names in year_month_rusid2names.items():
                if not (id in rusId2names):
                    print('NEW ID ' + id + '\t' + ';'.join(names))
                    rusId2names[id] = names
                elif ';'.join(sorted(rusId2names[id])) != ';'.join(sorted(names)):
                    for name in names:
                        if not (name in rusId2names[id]):
                            rusId2names[id].append(name)
                            print('CHANGED ID ' + id + '\t' + ';'.join(rusId2names[id]) + '\t' + ';'.join(names))

            with open('data/propingpong/propingpong_rusId2names_' + mw + '.txt', 'w', encoding='utf-8') as fout:
                for e in sorted(rusId2names.items(), key=lambda x: int(x[0])):
                    fout.write(e[0] + '\t' + ';'.join(e[1]) + '\n')

            with open(filename, 'w', encoding='utf-8') as fout:
                lastR = -1
                rank = 0
                i = 0
                for k,v in sorted(rankings.items(), key = lambda x: -x[1]):
                    i += 1
                    if lastR != v:
                        rank = i
                        lastR = v
                    fout.write('\t'.join([k, str(v), str(rank)]) + '\n')


def getIttfRankings(mw, year, month):
    url = 'http://propingpong.ru/rating_ittf.php?gender=' + str(int(mw == 'men')) + '&&page=1&sortby=undefined&year=' + str(year) + '&month=' + str(month)
    try:
        driver = initDriver(url)
        pagesCnt = int(driver.find_elements_by_xpath('//*[@class = "pagination"]')[0].find_elements(By.TAG_NAME, 'a')[-2].get_attribute('innerHTML'))
    except:
        driver = initDriver(url)
        pagesCnt = int(driver.find_elements_by_xpath('//*[@class = "pagination"]')[0].find_elements(By.TAG_NAME, 'a')[-2].get_attribute('innerHTML'))

    rankings = dict()
    ittfid2names = dict()
    if driver.find_element_by_xpath('//*//select[@id = "date"]//option[@selected = ""]').get_attribute('innerHTML')[-7:] != str(month).zfill(2) + '.' + str(year):
        print('bad date ' + str(month).zfill(2) + '.' + str(year))
    else:
        ids = [set(), set()]
        for page in range(1, pagesCnt + 1):
            driver.get(url + '&page=' + str(page))
            ul = driver.find_elements_by_xpath('//li[@class="dropdown"]')[-1]
            ul.click()
            ul.find_elements_by_xpath('./ul/li/a')[0].click()
            for ii in range(2):
                rows = driver.find_elements_by_xpath('//table[@id="rightarea"]//div[@class="table"]//div[@class="row"]')
                for i,row in enumerate(rows[1:]):
                    s = row.get_attribute('innerHTML')
#                    print(s)
                    playerId = s.split('ittfid=')[1].split('">')[0]
                    playerName = s.split('ittfid=')[1].split('>')[1].split('<')[0]
                    playerRating = int(s.split('country=')[1].split('</div>')[1].split('>')[-1])
                    #print([playerId, playerName, playerRating])
                    rankings[playerId] = playerRating
                    if not (playerId in ittfid2names):
                        ittfid2names[playerId] = []
                    if not (playerName in ittfid2names[playerId]):
                        ittfid2names[playerId].append(playerName)
                    if playerId in ids[ii]:
                        print([page, playerName])
                    ids[ii].add(playerId)
                if ii == 0:
                    ul = driver.find_elements_by_xpath('//li[@class="dropdown"]')[-1]
                    ul.click()
                    ul.find_elements_by_xpath('./ul/li/a')[1].click()
            print([page, len(rankings)])
    driver.quit()

    return [rankings, ittfid2names]

def updateIttfRanking():
    curDate = datetime.datetime.now().date().strftime("%Y-%m-%d")
    for mw in ['men', 'women']:
        ittfId2names = dict()
        with open('data/propingpong/propingpong_ittfId2names_' + mw + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                ittfId2names[tokens[0]] = tokens[1].strip().split(';')

        for year in range(2001,2018):
            for month in range(1, 13):
                if str(year) + '-' + str(month).zfill(2) > curDate:
                    break
                filename = 'data/propingpong/ranking_ittf/' + str(year) + '-' + str(month).zfill(2) + '_' + mw + '.txt'
                if not os.path.exists(filename):
                    rankings, year_month_ittfid2names = getIttfRankings(mw, year, month)

                    for id,names in year_month_ittfid2names.items():
                        if not (id in ittfId2names):
                            print('NEW ID ' + id + '\t' + ';'.join(names))
                            ittfId2names[id] = names
                        elif ';'.join(sorted(ittfId2names[id])) != ';'.join(sorted(names)):
                            for name in names:
                                if not (name in ittfId2names[id]):
                                    print('CHANGED ID ' + id + '\t' + ';'.join(ittfId2names[id]) + '\t' + ';'.join(names))
                                    ittfId2names[id].append(name)

                    with open('data/propingpong/propingpong_ittfId2names_' + mw + '.txt', 'w', encoding='utf-8') as fout:
                        for e in sorted(ittfId2names.items(), key=lambda x: x[0]):
                            fout.write(e[0] + '\t' + ';'.join(e[1]) + '\n')

                    with open(filename, 'w', encoding='utf-8') as fout:
                        lastR = -1
                        rank = 0
                        i = 0
                        for k,v in sorted(rankings.items(), key = lambda x: -x[1]):
                            i += 1
                            if lastR != v:
                                rank = i
                                lastR = v
                            fout.write('\t'.join([k, str(v), str(rank)]) + '\n')

def changeScript():
    for mw in ['men', 'women']:
        rusId2names = dict()
        ittfId2names = dict()
        with open('data/propingpong/propingpong_players_' + mw + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                tokens = [e.strip() for e in tokens]
                if len(tokens[1]) > 0:
                    if not tokens[1] in rusId2names:
                        rusId2names[tokens[1]] = []
                    rusId2names[tokens[1]].append(tokens[0])
                if len(tokens[2]) > 0:
                    if not tokens[2] in ittfId2names:
                        ittfId2names[tokens[2]] = []
                    ittfId2names[tokens[2]].append(tokens[0])
        #print(ittfId2names['25040772'])
        with open('data/propingpong/propingpong_ittfId2names_' + mw + '.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(ittfId2names.items(), key = lambda x: x[0]):
                fout.write(e[0] + '\t' + ';'.join(e[1]) + '\n')
        with open('data/propingpong/propingpong_rusId2names_' + mw + '.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(rusId2names.items(), key=lambda x: x[0]):
                fout.write(e[0] + '\t' + ';'.join(e[1]) + '\n')

def parseAllRusPlayers(left = 1, right = 1000):
    '''
    rusId2names = dict()
    for mw in ['men', 'women']:
        with open('data/propingpong/propingpong_ittfId2names_' + mw + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                rusId2names[tokens[0]] = tokens[1].strip().split(';')
    '''

    driver = initDriver('http://propingpong.ru')
    for id in range(left, right + 1):
        try:
            url = 'http://propingpong.ru/profile.php?id=' + str(id)
            try:
                driver.get(url)
                rows = driver.find_elements_by_xpath('//*[@class = "table"]')[0].find_elements_by_xpath('//*[@class = "row"]')
            except:
                try:
                    driver.quit()
                except:
                    pass
                driver = initDriver(url)
                rows = driver.find_elements_by_xpath('//*[@class = "table"]')[0].find_elements_by_xpath('//*[@class = "row"]')

            playerName = driver.find_elements(By.TAG_NAME, 'h3')[0].text
            countryInd = -1
            for ir, row in enumerate(rows):
                arr = row.get_attribute('innerHTML').split('country=')
                if len(arr) == 2:
                    countryInd = ir
                    break
            if countryInd == -1:
                print([id, playerName, 'bad'])
                continue
            mw = 'men'
            if rows[countryInd].get_attribute('innerHTML').find('gender=1') == -1:
                mw = 'women'
            country = rows[countryInd].get_attribute('innerHTML').split('country=')[1].split('">')[0]

            town = region = district = year = ''
            for row in rows[(countryInd + 1):(countryInd + 6)]:
                s = row.get_attribute('innerHTML')
                if s.find('Населённый пункт') != -1:
                    town = s.split('settlement=')[1].split('">')[0]
                elif s.find('Регион') != -1:
                    region = s.split('area=')[1].split('">')[0]
                elif s.find('Федеральный округ') != -1:
                    district = s.split('district=')[1].split('">')[0]
                elif s.find('Год рождения') != -1:
                    year = s.split('">')[2].split('<')[0]
            print([id, playerName, mw, country, district, region, town, year])

            url = 'http://propingpong.ru/alldata.php?player=' + str(id)
            try:
                driver.get(url)
                table = driver.find_elements_by_xpath('//*//table[@class = "main"]')[1]
            except:
                try:
                    driver.quit()
                except:
                    pass
                driver = initDriver(url)
                table = driver.find_elements_by_xpath('//*//table[@class = "main"]')[1]

            try:
                tds = table.find_elements_by_xpath('//tr//td')
                rankings = dict()
                for i in range(5, len(tds), 4):
                    idate = tds[i].get_attribute('innerHTML') + '-' + str(months[tds[i + 1].get_attribute('innerHTML')]).zfill(2)
                    rt = tds[i + 2].get_attribute('innerHTML')
                    rg = tds[i + 3].get_attribute('innerHTML')
                    rankings[idate] = [str(id), rt, rg]

                for idate, values in rankings.items():
                    with open('data/propingpong/ranking_rus/' + idate + '_' + mw + '.txt', 'a', encoding='utf-8') as fout:
                        fout.write('\t'.join(values) + '\n')
                with open('data/propingpong/propingpong_rusId2names_' + mw + '.txt', 'a', encoding='utf-8') as fout:
                    fout.write('\t'.join([str(id), playerName]) + '\n')
                with open('data/propingpong/propingpong_rusId2info_' + mw + '.txt', 'a', encoding='utf-8') as fout:
                    fout.write('\t'.join([str(id), country, district, region, town, year]) + '\n')
            except:
                print('bad ranking')
        except:
            pass
        #break
    driver.quit()

def findMWErrors():
    mw = 'men'
    ids = set()
    id2name = dict()
    with open('data/propingpong/propingpong_rusId2names_' + mw + '.txt', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.strip('\n').split('\t')
            ids.add(tokens[0])
            id2name[tokens[0]] = tokens[1]

    with open('data/propingpong/propingpong_rusId2info_' + mw + '.txt', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.strip('\n').split('\t')
            if tokens[5] == '':
                print([line, id2name[tokens[0]]])

    for f in os.listdir('data/propingpong/ranking_rus'):
        if f.find('_' + mw) != -1:
            with open('data/propingpong/ranking_rus/' + f, 'r', encoding='utf-8') as fin:
                lines = []
                linesSet = set()
                for line in fin:
                    tokens = line.split('\t')
                    tokens = [e.strip() for e in tokens]
                    if not (tokens[0] in ids):
                        print(line)
                        continue
                    if line in linesSet:
                        print(line)
                        continue
                    lines.append(line)
                    linesSet.add(line)
            #with open('data/propingpong/ranking_rus/' + f, 'w', encoding='utf-8') as fout:
            #    for line in lines:
            #        fout.write(line)


def main():
    #getLastRusRankings('men')
    #updateRusRanking(2017, 4)

    #findMWErrors()

    #parseAllRusPlayers(2746, 2746)
    #parseAllRusPlayers(18801, 19800)
    #parseAllRusPlayers(10106, 10106)
#    getIttfRankings('men', 2005, 5)

    #updateIttfRanking()
    updateRusRanking(2017, 9)


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