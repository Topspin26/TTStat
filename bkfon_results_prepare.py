from os import walk
from lxml import html
from lxml import etree
from common import *
from Entity import *
import time
import datetime as datetime
import random
import re

lpCorr = []
chsCorr = []
mtCorr = []

def fillLPCorr(ligaProCorr):
    ligaProCorr.append(['Бурдин А', 'Алексей Бурдин'])
    ligaProCorr.append(['Заикин А', 'Алан Заикин'])
    ligaProCorr.append(['Карпенко В', 'Вячеслав Карпенко'])
    ligaProCorr.append(['Попов Д', 'Дмитрий Попов'])
    ligaProCorr.append(['Терехов А', 'Антон Терехов'])
    ligaProCorr.append(['Егоров Н', 'Николай Егоров'])
    ligaProCorr.append(['Анохин И', 'Илья Анохин'])
    ligaProCorr.append(['Королев С', 'Семен Королев'])
    ligaProCorr.append(['Анисимов А', 'Антон Анисимов'])
    ligaProCorr.append(['Семин А', 'Артем Семин'])
    ligaProCorr.append(['Виноградов А', 'Алексей Виноградов'])
    ligaProCorr.append(['Макаров А', 'Александр Макаров'])
    ligaProCorr.append(['Меркушев С', 'Станислав Меркушев'])
    ligaProCorr.append(['Морозов А', 'Александр Морозов'])
    ligaProCorr.append(['Ануфриев В', 'Владимир Ануфриев'])
    ligaProCorr.append(['Маслов Д', 'Даниил Маслов'])
    ligaProCorr.append(['Федоров Д', 'Дмитрий Федоров'])
    ligaProCorr.append(['Голубева А', 'Анастасия Голубева'])
    ligaProCorr.append(['Лебедева В', 'Виктория Лебедева'])
    ligaProCorr.append(['Свиридов А', 'Алексей Свиридов'])
    ligaProCorr.append(['Крылов А', 'Александр Крылов'])
    ligaProCorr.append(['Морозова В', 'Валерия Морозова'])
    ligaProCorr.append(['Резниченко А', 'Александр Резниченко'])
    ligaProCorr.append(['Беспалова Е', 'Екатерина Беспалова'])
    ligaProCorr.append(['Булхак А', 'Антон Булхак'])
    ligaProCorr.append(['Фомина А', 'Анастасия Фомина'])
    ligaProCorr.append(['Кутузова А', 'Алина Кутузова'])

def fillChSCorr(chsCorr):
    chsCorr.append(['Мего П', 'Павол Мего'])

def fillMTCorr(mtCorr):
    mtCorr.append(['Млинарж А', 'Алексей Млинарж'])
    mtCorr.append(['Млинарж', 'Алексей Млинарж'])
    mtCorr.append(['Алексей Алексей Млинарж', 'Алексей Млинарж'])
    mtCorr.append(['Иванов Н', 'Никита Иванов'])

fillLPCorr(lpCorr)
fillChSCorr(chsCorr)
fillMTCorr(mtCorr)

def processOld(ff, matches, corrections):
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
                        # print(s)
                    else:
                        flTT = 0
                else:
                    if flTT == 1:
                        tcorr = corrections.copy()
                        if compName.replace('Жен. ', '').find('Лига Про. Москва') != -1:
                            tcorr += lpCorr
                        if compName.replace('Жен. ', '').find('Челленджер серия') != -1:
                            tcorr += chsCorr
                        if compName.replace('Жен. ', '').find('Мастер-Тур') != -1:
                            tcorr += mtCorr
                        arr = [re.sub(' +', ' ', e.replace(u'\xa0', ' ')) for e in tr.xpath('.//text()')]

                        #print(arr)
                        timeArr = arr[1].split(' ')
                        if len(timeArr) == 2:
                            time = timeArr[1].strip()
                        else:
                            time = timeArr[0].strip()

                        matchTime = time

                        dt = timeArr[0].strip()
                        if len(dt.split('.')) == 2:
                            day = dt.split('.')[0].zfill(2)
                            month = dt.split('.')[1].zfill(2)
                            year = ff[:4]
                            dt = year + '-' + month + '-' + day
                        else:
                            dt = ff[:10]

                        arr = [e.replace('(ж)', '') for e in arr]
                        s0 = '\t'.join(arr)
                        for k, v in tcorr:
                            if k.find(';') != -1:
                                if k.split(';')[0] == dt:
                                    arr = [e.replace(k.split(';')[1], v) for e in arr]
                            else:
                                arr = [e.replace(k, v) for e in arr]
                        if '\t'.join(arr) != s0:
                            print(s0 + '\n' + '\t'.join(arr) + '\n')
                            #                                if s0.find('(ж)') != -1:
                            #                                    print(s0)
                        # arr = [pattern.sub(lambda x: corrections[x.group()], e) for e in arr]

                        names = arr[2].strip().split(' - ')
                        if len(names) != 2:
                            print(arr)
                            continue
                        if names[0].lower().find('game') != -1:
                            continue
                            #                                if dt != ff[:10]:
                            #                                    print(dt + ' ' + ff[:10])
                        if arr[4] != 'отмена':
                            matches.append(Match(dt,
                                                 [[e.strip() for e in names[0].strip().split('/')],
                                                  [e.strip() for e in names[1].strip().split('/')]],
                                                 setsScore=arr[3],
                                                 pointsScore=arr[4].replace('(', '').replace(')', '').replace(' ', ';').replace('-', ':'),
                                                 time=matchTime,
                                                 compName=compName,
                                                 matchId=arr[0]))


monthname2Num = {'янв':1,'фев':2,'мар':3,'апр':4,'май':5,'мая':5,'июн':6,'июл':7,'авг':8,'сен':9,'окт':10,'ноя':11,'дек':12}

def processNew(ff, matches, corrections):
    print(ff)
    with open('data/bkfon/results/' + ff, 'r', encoding='utf-8') as fin:
        for line in fin:
            table = html.fromstring(line)
            trs = table.xpath("//tr")
            print(len(trs))
            compName = ''
            for itr,tr in enumerate(trs):
                if tr.get('class').find('table__row _type_segment _sport_3088') != -1:
                    s = re.sub(r'\<\!--[^>]*--\>', '', etree.tostring(tr, pretty_print=True, encoding='unicode'))
                    #print(s)
                    compName = s.split('"table__title-text">')[1].split('<')[0]
#                    print(compName)
                else:
                    if compName.find('TT-CUP') != -1:
                        continue
                    tds = tr.xpath('//tr[' + str(itr+1) + ']/td')
                    s = re.sub(r'\<\!--[^>]*--\>', '', etree.tostring(tds[0], pretty_print=True, encoding='unicode'))
#                    print(s.strip())
                    timeArr = s.split('"table__time-icon')[1].split('<span>')[1].split('<')[0].split(' в ')
                    matchTime = timeArr[1]
                    month =  str(monthname2Num[timeArr[0].split()[1][:3]]).zfill(2)
                    dt = ff[:4] + '-' + month + '-' + timeArr[0].split()[0].zfill(2)
#                    print(timeArr)
#                    print(dt)
                    names = s.split('"table__event-number">')[1].split('</span>')[1].split('<')[0].strip()

                    tcorr = corrections.copy()
                    if compName.replace('Жен. ', '').find('Лига Про. Москва') != -1:
                        tcorr += lpCorr
                    if compName.replace('Жен. ', '').find('Челленджер серия') != -1:
                        tcorr += chsCorr
                    if compName.replace('Жен. ', '').find('Мастер-Тур') != -1:
                        tcorr += mtCorr

                    names = re.sub(' +', ' ', names.replace(u'\xa0', ' '))

                    names = names.strip().split(' - ')

                    for k, v in tcorr:
                        if k.find(';') != -1:
                            if k.split(';')[0] == dt:
                                names = [e.replace(k.split(';')[1], v) for e in names]
                        else:
                            names = [e.replace(k, v) for e in names]
        #                    print(names)

                    matchId = s.split('"table__event-number">')[1].split('</span>')[0].strip()
#                    print(matchId)
                    setsScore = ''
                    try:
                        setsScore = s.split('"table__score">')[1].split('<')[0]
                    except:
                        pass
#                    print(setsScore)
                    pointsScore = ''
                    try:
                        pointsScore = s.split('"table__score-more">')[1].split('<')[0]
                        pointsScore = pointsScore.replace('(', '').replace(')', '').replace('\xa0', ';').replace('-', ':')
                    except:
                        pass
#                    print(pointsScore)

                    if names[0].lower().find('game') != -1:
                        continue

                    if len(setsScore) > 0:
                        matches.append(Match(dt,
                         [[e.strip() for e in names[0].strip().split('/')],
                          [e.strip() for e in names[1].strip().split('/')]],
                         setsScore=setsScore,
                         pointsScore=pointsScore,
                         time=matchTime,
                         compName=compName,
                         matchId=matchId))

                        print(matches[-1].toStr())


def getMatches(corrections, wrongLines):
#    pattern = re.compile('|'.join(corrections.keys()))
    matches = []
    for f in walk('data/bkfon/results'):
        fSet = set(f[2])
        for ff in f[2]:
            #print(ff)
            if ff.find('old') != -1:
                continue
            if ff.find('new') != -1:
                if not (ff.replace('_new', '') in fSet):
                    processNew(ff, matches, corrections)
#                    break
                continue
    #            if ff.find('2016-11') == -1 and ff.find('2016-12') == -1 and ff.find('2017-') == -1:
#                continue
#            if ff.find('2017-02-07') == -1:
#                continue
            processOld(ff, matches, corrections)
    return matches

def getMatchesPlayers(matches):
    res = dict()
    for match in matches:
        for i in range(2):
            for player in match.players[i]:
                updateDict(res, player)
    return res

def main():
    playersDict = GlobalPlayersDict("filtered")

    corrections = readCorrectionsList('data/bkfon/corrections.txt')
    wrongLines = []
    matches = getMatches(corrections, wrongLines)
    print(len(matches))
    players = getMatchesPlayers(matches)

    m = dict()
    w = dict()
    mw = dict()

    multiple = dict()
    unknown = dict()

    for player in players:

        id = playersDict.getId(player)
        if len(id) == 1:
            if id[0][0] == 'm':
                updateDict(m, player)
            else:
                updateDict(w, player)
        elif len(id) == 0:
            updateDict(unknown, player)
        else:
            fl_mw = ''
            for e in id:
                fl_mw += e[0]
            fl_mw = ''.join(sorted(set(list(fl_mw))))
            if fl_mw == 'm':
                updateDict(m, player)
            elif fl_mw == 'w':
                updateDict(w, player)
            else:
                updateDict(mw, player)
            if not (fl_mw + ' ' + player in multiple):
                multiple[fl_mw + ' ' + player] = 0
            multiple[fl_mw + ' ' + player] += 1

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

    prefix = 'prepared_data/bkfon/'

    with open(prefix + 'bkfon_players_x_mw.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(playersMW.items(), key = lambda x: -x[1][2]):
#        for e in sorted(playersMW.items(), key = lambda x: (x[1][0] + 1) / (x[1][2] + 2)):
            if (e[0] in unknown) and e[1][2] > 0:
                print(e)
                fout.write(e[0] + '\t' + str(e[1]) + '\t' + '\t'.join(playersMatches[e[0]]) + '\n')

    with open(prefix + 'bkfon_players_men.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(m.keys()):
            fout.write(e + '\t' + ';'.join(playersDict.getId(e)) + '\n')
    with open(prefix + 'bkfon_players_women.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(w.keys()):
            fout.write(e + '\t' + ';'.join(playersDict.getId(e)) + '\n')
    with open(prefix + 'bkfon_players_mw.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(mw.keys()):
            fout.write(e + '\t' + ';'.join(playersDict.getId(e)) + '\n')

    multiple = dict()
    unknown = dict()

    with open(prefix + 'all_results.txt', 'w', encoding='utf-8') as fout, open(prefix + 'players_collisions.txt', 'w', encoding='utf-8') as fout1:
        fout.write('\t'.join(['date', 'time', 'compName', 'id1', 'id2', 'setsScore', 'pointsScore', 'name1', 'name2', 'matchId']) + '\n')
        for match in matches:
            flError = 0
            if match.flError == 0:
#                print(match.toStr())
                ids = [[], []]
                for i in range(2):
                    for player in match.players[i]:

                        id = playersDict.getId(player)

                        if len(id) == 1:
                            ids[i].append(id[0])
                        elif len(id) == 0:
                            flError = 'unknown ' + player
                            if not (player in unknown):
                                unknown[player] = 0
                            unknown[player] += 1
                        else:
                            flError = 'multiple ' + player
                            fl_mw = ''
                            for e in id:
                                fl_mw += e[0]
                            fl_mw = ''.join(sorted(set(list(fl_mw))))
                            if not (fl_mw + ' ' + player in multiple):
                                multiple[fl_mw + ' ' + player] = 0
                            multiple[fl_mw + ' ' + player] += 1
                            fout1.write('MANY ' + player + ' ' + str(id) + ' ' + match.toStr() + '\n')
                            #print('MANY ' + player + ' ' + str(id) + ' ' + match.toStr())

                if flError == 0:
                    resTokens = match.toArr()
                    resTokens.append(resTokens[3])
                    resTokens.append(resTokens[4])
                    resTokens[3] = ';'.join(ids[0])
                    resTokens[4] = ';'.join(ids[1])
                    resTokens.append(match.matchId)
                    fout.write('\t'.join(resTokens) + '\n')
            if (match.flError != 0 or flError != 0) and match.compName.lower().replace('-', '').find('лига про') != -1:
                print('LIGA PRO error ' + str(match.flError) + ' ' + str(flError) + ' ' + match.toStr())


    with open(prefix + 'bkfon_players_multiple.txt', 'w', encoding='utf-8') as fout:
        for e in sorted(multiple.items(), key = lambda x: -x[1]):
            fout.write(e[0] + '\t' + str(e[1]) + '\n')
    with open(prefix + 'bkfon_players_unknown.txt', 'w', encoding='utf-8') as fout:
        for e in sorted(unknown.items(), key = lambda x: -x[1]):
            fout.write(e[0] + '\t' + str(e[1]) + '\n')

if __name__ == "__main__":
    main()