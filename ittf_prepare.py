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
from Entity import *


def initDriver(url):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver', port = 5938)
    driver.get(url)
    #time.sleep(2) # Let the user actually see something!
    return driver

def readIttfPlayers():
    playersDict = dict()
    with open('data/ittf/ittf_players.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            tokens = [e.strip() for e in tokens]
            playersDict[tokens[1]] = tokens[0]
    return playersDict

def getIttfMatches(driver, url, pages):
    playersDict = readIttfPlayers()

    for page in pages:
        print(page)
        driver.get(url + str(page))

        tds = driver.find_elements_by_xpath('//*//table[@bordercolor = "#000080"]//tr//td')
        playerId = None
        playerRating = None
        numCols = 6
        matches = dict()
        match = []
        for i,td in enumerate(tds[:-1]):
            tokens = td.get_attribute('innerHTML').replace('\t', '').replace('\n', '').split('<br>')
            if i % numCols == 1 or i % numCols == 3:
                tokensNew = []
                for e in tokens:
                    if len(re.sub('<[^<]+?>', '', e).strip()) > 0:
                        tokensNew.append(e)
                        result = re.search('P_ID=([^&]*)&', e)
                        tokensNew.append(result.group(1))
                tokens = tokensNew
            tokens = [re.sub('<[^<]+?>', '', e).strip() for e in tokens]
            match.append(tokens)
            if i % numCols == 5:
#                print(match)
                dt = match[0][-1]
                try:
                    arr = dt.split(' ')[-1].split('/')
                    dt = arr[2] + '-' + arr[1].zfill(2) + '-' + arr[0].zfill(2)
                except:
                    dt = 'error_' + dt.replace('/', '_').replace('\\', '_')
                if not dt in matches:
                    matches[dt] = []
                matches[dt].append([';'.join(e) for e in match])
                match = []
        for e in matches.items():
            try:
                with open('data/ittf/results/' + e[0] + '.txt', 'a', encoding = 'utf-8') as fout:
                    for s in e[1]:
                        fout.write('\t'.join(s) + '\n')
            except Exception as ex:
                print(str(ex))
def getMW(s):
    arr = s.replace('&amp;', '').split(';')
    if arr[2].find('Mixed') != -1:
        return '?'
    if arr[2].find('Women') != -1 or arr[2].find('Girl') != -1 or arr[2].find('Female') != -1 or arr[2].find('WS 4th Stage') != -1 or arr[2].find('WS 3rd Stage') != -1:
        return 'w'
    if arr[2].find('Men') != -1 or arr[2].find('Boy') != -1 or arr[2].find('Male') != -1 or arr[2].find('MS 4th Stage') != -1 or arr[2].find('MS 3rd Stage') != -1 or arr[2].find('MS 2nd Stage') != -1:
        return 'm'
    print(s)
    return '?'

def main():
    filenameGlobalPlayersMen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_men.txt'

    (mIdG, mId2G) = readPlayersInv(filenameGlobalPlayersMen)
    filenameGlobalPlayersWomen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_women.txt'
    (wIdG, wId2G) = readPlayersInv(filenameGlobalPlayersWomen)

#    getIttfMatches(driver, url, list(range(1,11109)))
    player2id = dict()
    id2player = dict()
    with open('data/ittf/player2id.txt', encoding = 'utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            if len(tokens[1].split(';')) == 1 and len(tokens[1].strip()) > 0:
                player2id[tokens[0]] = tokens[1].strip()
                id2player[tokens[1].strip()] = tokens[0]
    print(player2id['ZHUKOV Aleksei'])

    id2info = dict()

    matches = []
    dirname = 'data/ittf/results'
    for f in os.listdir(dirname):
        if f.find('error') != -1:
            continue
        print([f, len(matches)])
        with open(dirname + '/' + f, 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                ids = [[], []]
                for ii,i in enumerate([1, 3]):
                    if len(tokens[i]) > 0:
                        arr = tokens[i].replace('&nbsp;', '').split(';')
                        for j in range(len(arr)):
                            if j % 2 == 0:
                                name = ' '.join(arr[j].split(' ')[:-1])
                                id = arr[j + 1]
                                if arr[j].find('---') != -1:
                                    continue
                                if len(id) == 0:
                                    id = player2id.get(name,id)
                                ids[ii].append(id)
                time = ''
                matches.append(Match(f[:10],
                         [[e.strip() for e in ids[0]],
                          [e.strip() for e in ids[1]]],
                         setsScore=tokens[5].replace('-', ':').split(';')[0],
                         pointsScore=tokens[4].replace(', ', ',').replace(',', ';').replace(';0-0', '').replace('-', ':').replace(':;', '').replace(';:', ''),
                         time=time,
                         compName=tokens[0].split(';')[0]))
    print(len(player2id))

    prefix = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\ittf\\'

    with open(prefix + 'all_results.txt', 'w', encoding='utf-8') as fout:
        fout.write('\t'.join(['date', 'time', 'compName', 'id1', 'id2', 'setsScore', 'pointsScore', 'name1', 'name2']) + '\n')
        for match in matches:
            if match.flError == 0:
                flError = 0
                ids = [[], []]
                players = [[], []]
                for i in range(2):
                    for player in match.players[i]:
                        player = id2player.get(player, player).title()
                        players[i].append(player)
                        if (player in mId2G) and not (player in wId2G):
                            if len(mId2G[player]) == 1:
                                ids[i].append(mId2G[player][0])
                            else:
                                flError = 1
                        elif not (player in mId2G) and (player in wId2G):
                            if len(wId2G[player]) == 1:
                                ids[i].append(wId2G[player][0])
                            else:
                                flError = 1
                        else:
                            flError = 1
                if flError == 0 and len(ids[0]) > 0 and len(ids[1]) > 0 and match.date < '2018':
                    resTokens = match.toArr()
                    resTokens.append(';'.join(players[0]))
                    resTokens.append(';'.join(players[1]))
                    resTokens[3] = ';'.join(ids[0])
                    resTokens[4] = ';'.join(ids[1])
                    fout.write('\t'.join(resTokens) + '\n')

    return


    print('id')
    for k, v in player2id.items():
        if len(v) != 1:
            print((k, v))
    print('info')
    for k, v in id2info.items():
        if len(v['country']) > 1:
            print((k, v))
        if 'm' in v['mw'] and 'w' in v['mw']:
            print((k, v, player2id.get(k, k)))

    fouts = dict()
    for e in ['men', 'women', 'mw', 'x']:
        fouts[e] = open('data/ittf/ittf_players_' + e + '.txt', 'w', encoding = 'utf-8')
    with open('data/ittf/player2id.txt', 'w', encoding = 'utf-8') as fout:
        for k,v in sorted(player2id.items(), key = lambda x: str(len(x[1])).zfill(3) + x[0], reverse=True):
            fout.write(k + '\t' + ';'.join(sorted(v)) + '\n')
            m = set()
            for e in v:
                for ee in id2info[e]['mw']:
                    m.add(ee)
            if ('m' in m) and (not ('w' in m)):
                fouts['men'].write(k + '\t' + ';'.join(sorted(v)) + '\n')
            elif ('w' in m) and (not ('m' in m)):
                fouts['women'].write(k + '\t' + ';'.join(sorted(v)) + '\n')
            elif ('m' in m) and ('w' in m):
                fouts['mw'].write(k + '\t' + ';'.join(sorted(v)) + '\n')
            else:
                fouts['x'].write(k + '\t' + ';'.join(sorted(v)) + '\n')

    with open('data/ittf/id2info.txt', 'w', encoding='utf-8') as fout:
        for k, v in sorted(id2info.items(), key = lambda x: x[0], reverse=True):
            fout.write(k + '\t' + ';'.join(sorted(v['country'])) + '\t' + ';'.join(sorted(v['mw'])) + '\n')

    for e in ['men', 'women', 'mw', 'x']:
        fouts[e].close()

if __name__ == "__main__":
    main()