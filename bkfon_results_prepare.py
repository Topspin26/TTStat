from os import walk
from lxml import html
from common import *
from Entity import *
import time
import datetime as datetime
import random
import re

def getMatches(corrections, wrongLines):
#    pattern = re.compile('|'.join(corrections.keys()))
    matches = []
    for f in walk('data/bkfon/results'):
        for ff in f[2]:
            print(ff)
            if ff.find('old') != -1:
                continue
#            if ff.find('2016-12') == -1 and ff.find('2017-') == -1:
#                continue
            with open('data/bkfon/results/' + ff, 'r', encoding='utf-8') as fin:
                for line in fin:
                    table = html.fromstring(line)
                    trs = table.xpath("*//tr")
                    flTT = 0
                    compName = ''
                    for tr in trs:
                        if tr.get('class') == 'sectCaption':
                            s = tr.xpath('.//th/text()')[0].replace(u'\xa0', ' ')
                            compName = s
                            if s.find('Наст. теннис') != -1 and s.find('TT-CUP') == -1:
                                flTT = 1
                                #print(s)
                            else:
                                flTT = 0
                        else:
                            if flTT == 1:
                                arr = [re.sub(' +', ' ', e.replace(u'\xa0', ' ')) for e in tr.xpath('.//text()')]
                                s0 = '\t'.join(arr)
                                for k,v in corrections:
                                    if k.find(';') != -1:
                                        if k.split(';')[0] == ff[:10]:
                                            arr = [e.replace(k.split(';')[1], v) for e in arr]
                                    else:
                                        arr = [e.replace(k, v) for e in arr]
                                if '\t'.join(arr) != s0:
                                    print(s0 + '\n' + '\t'.join(arr) + '\n')
#                                if s0.find('(ж)') != -1:
#                                    print(s0)
                                #arr = [pattern.sub(lambda x: corrections[x.group()], e) for e in arr]

                                names = arr[2].strip().split(' - ')
                                if len(names) != 2:
                                    print(arr)
                                    continue
                                if names[0].lower().find('game') != -1:
                                    continue
                                timeArr = arr[1].split(' ')
                                if len(timeArr) == 2:
                                    time = timeArr[1].strip()
                                else:
                                    time = time.strip()
                                dt = timeArr[0].strip()
                                if len(dt) == 2:
                                    day = dt.split('.')[0].zfill(2)
                                    month = dt.split('.')[1].zfill(2)
                                    year = ff[:4]
                                    dt = year + '-' + month + '-' + day
                                else:
                                    dt = ff[:10]
#                                if dt != ff[:10]:
#                                    print(dt + ' ' + ff[:10])
                                if arr[4] != 'отмена':
                                    matches.append(Match(dt,
                                                         [[e.strip() for e in names[0].strip().split('/')],
                                                          [e.strip() for e in names[1].strip().split('/')]],
                                                         setsScore=arr[3],
                                                         pointsScore=arr[4].replace('(', '').\
                                                            replace(')', '').replace(' ', ';').replace('-', ':'),
                                                         time=time,
                                                         compName=compName))
    return matches

def getMatchesPlayers(matches):
    res = dict()
    for match in matches:
        for i in range(2):
            for player in match.players[i]:
                updateDict(res, player)
    return res

def updateDict(d, k):
    if k in d:
        d[k] += 1
    else:
        d[k] = 1

def main():
    filenameGlobalPlayersMen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_men.txt'
    (mIdG, mId2G) = readPlayersInv(filenameGlobalPlayersMen)
    filenameGlobalPlayersWomen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_women.txt'
    (wIdG, wId2G) = readPlayersInv(filenameGlobalPlayersWomen)

    corrections = readCorrectionsList(r'D:\Programming\SportPrognoseSystem\BetsWinner\data\bkfon\corrections.txt')
    wrongLines = []
    matches = getMatches(corrections, wrongLines)
    print(len(matches))
    players = getMatchesPlayers(matches)
    empty = dict()
    m = dict()
    w = dict()
    mw = dict()
    for e in players:
        if e in mId2G and e in wId2G:
            updateDict(mw, e)
            print('MW ' + e)
        if e in mId2G and not (e in wId2G):
            print('M ' + e)
            updateDict(m, e)
        if not (e in mId2G) and (e in wId2G):
            print('W ' + e)
            updateDict(w, e)
        if not (e in mId2G) and not (e in wId2G):
            print('? ' + e)
            updateDict(empty, e)
    playersMW = dict()
    playersMatches = dict()
    for player in players:
        playersMW[player] = [0, 0, 0]
    for match in matches:
        if len(match.players[0]) == 1:
            pl1 = match.players[0][0]
            pl2 = match.players[1][0]
            if pl1 in m:
                playersMW[pl2][0] += 1
            elif pl1 in w:
                playersMW[pl2][1] += 1
            if pl2 in m:
                playersMW[pl1][0] += 1
            elif pl2 in w:
                playersMW[pl1][1] += 1
            playersMW[pl1][2] += 1
            playersMW[pl2][2] += 1
            if not (pl1 in playersMatches):
                playersMatches[pl1] = []
            playersMatches[pl1].append(match.toStr())
            if not (pl2 in playersMatches):
                playersMatches[pl2] = []
            playersMatches[pl2].append(match.toStr())

    with open(r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\bkfon\bkfon_players_x_mw.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(playersMW.items(), key = lambda x: -x[1][2]):
#        for e in sorted(playersMW.items(), key = lambda x: (x[1][0] + 1) / (x[1][2] + 2)):
            if (e[0] in empty) and e[1][2] > 0:
                print(e)
                fout.write(e[0] + '\t' + str(e[1]) + '\t' + '\t'.join(playersMatches[e[0]]) + '\n')

    prefix = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\bkfon\\'
    with open(prefix + 'bkfon_players_men.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(m.keys()):
            fout.write(e + '\t' + ';'.join(mId2G[e]) + '\n')
    with open(prefix + 'bkfon_players_women.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(w.keys()):
            fout.write(e + '\t' + ';'.join(wId2G[e]) + '\n')
    with open(prefix + 'bkfon_players_mw.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(mw.keys()):
            fout.write(e + '\t' + ';'.join(mId2G[e]) + '\t' + ';'.join(wId2G[e]) + '\n')
    with open(prefix + 'bkfon_players_x.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(empty.keys()):
            fout.write(e + '\t' + '?' + '\n')

    with open(prefix + 'all_results.txt', 'w', encoding='utf-8') as fout, open(prefix + 'players_collisions.txt', 'w', encoding='utf-8') as fout1:
        fout.write('\t'.join(['date', 'time', 'compName', 'id1', 'id2', 'setsScore', 'pointsScore', 'name1', 'name2']) + '\n')
        for match in matches:
            if match.flError == 0:
#                print(match.toStr())
                flError = 0
                ids = [[], []]
                for i in range(2):
                    for player in match.players[i]:
                        if player in mw:
                            flError = 1
                        elif (player in m):
                            if len(mId2G[player]) == 1:
                                ids[i].append(mId2G[player][0])
                            else:
                                if player.find('Желуб') != -1:
                                    print(match.toStr())
                                if len(mId2G[player]) > 1:
                                    fout1.write('MANY ' + player + ' ' + str(mId2G[player]) + ' ' + match.toStr() + '\n')
                                    print('MANY ' + player + ' ' + str(mId2G[player]) + ' ' + match.toStr())
                                flError = 1
                        elif (player in w):
                            if len(wId2G[player]) == 1:
                                ids[i].append(wId2G[player][0])
                            else:
                                flError = 1
                                if len(wId2G[player]) > 1:
                                    fout1.write('MANY ' + player + ' ' + str(wId2G[player]) + ' ' + match.toStr() + '\n')
                                    print('MANY ' + player + ' ' + str(wId2G[player]) + ' ' + match.toStr())
                        else:
                            flError = 1
                if flError == 0:
                    resTokens = match.toArr()
                    resTokens.append(resTokens[3])
                    resTokens.append(resTokens[4])
                    resTokens[3] = ';'.join(ids[0])
                    resTokens[4] = ';'.join(ids[1])
                    fout.write('\t'.join(resTokens) + '\n')

if __name__ == "__main__":
    main()