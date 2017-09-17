import time
import random

import os
from os import walk

from common import *
from Entity import *
from Storages import *
import json
import re

def main():
    playersDict = GlobalPlayersDict("filtered")

    activePlayers = set()

    matchesDict = dict()

    bkfonMatchesDict = dict()

    with open('prepared_data/bkfon/all_results.txt', encoding='utf-8') as fin:
        headerTokens = next(fin).strip().split('\t')
        headerDict = dict(zip(headerTokens, range(len(headerTokens))))
        for line in fin:
            tokens = line.rstrip().split('\t')
            ids = [tokens[headerDict['id1']].split(';'), tokens[headerDict['id2']].split(';')]
            names = [tokens[headerDict['name1']].split(';'), tokens[headerDict['name2']].split(';')]
            dt = tokens[headerDict['date']]

            match = Match(dt,
                          ids,
                          names=names,
                          setsScore=tokens[headerDict['setsScore']],
                          pointsScore=tokens[headerDict['pointsScore']],
                          time=tokens[headerDict['time']],
                          compName=tokens[headerDict['compName']],
                          source='bkfon',
                          matchId=tokens[headerDict['matchId']])
            print(dt + '\t' + tokens[headerDict['compName']] + '\t' + tokens[headerDict['matchId']])
            bkfonMatchesDict[dt + '\t' + tokens[headerDict['compName']] + '\t' + tokens[headerDict['matchId']]] = match

    sources = []
    sources.append(['master_tour', 'prepared_data/master_tour/all_results.txt'])
    sources.append(['liga_pro', 'prepared_data/liga_pro/all_results.txt'])
    sources.append(['bkfon', 'prepared_data/bkfon/all_results.txt'])

#    matchesStorage = MatchesStorage(sources) #заменить кусок кода ниже

    for source, filename in sources:
        print(filename)
        with open(filename, encoding='utf-8') as fin:
            headerTokens = next(fin).strip().split('\t')
            headerDict = dict(zip(headerTokens, range(len(headerTokens))))
            for line in fin:
                tokens = line.split('\t')
                ids = [tokens[headerDict['id1']].split(';'), tokens[headerDict['id2']].split(';')]
                names = [tokens[headerDict['name1']].split(';'), tokens[headerDict['name2']].split(';')]
                dt = tokens[headerDict['date']]
                for id in ids[0] + ids[1]:
                    activePlayers.add(source + '\t' + dt + '\t' + id)

                match = Match(tokens[headerDict['date']],
                              ids,
                              names=names,
                              setsScore=tokens[headerDict['setsScore']],
                              pointsScore=tokens[headerDict['pointsScore']],
                              time=tokens[headerDict['time']],
                              compName=tokens[headerDict['compName']],
                              source=source)
                matchHash = match.getHash()
                if not (matchHash in matchesDict) and match.date >= '2014':
                    if not matchHash in matchesDict:
                        matchesDict[matchHash] = []
                    matchesDict[matchHash].append(match)
                elif matchHash in matchesDict:
                    matchesDict[matchHash][0].addSource(source)

    multiple = dict()
    unknown = dict()
    solved = dict()
    mbCnt = 0

    sourcesCount = dict()

    filenames = list()
    filenames.append(['liga_pro_men', 'liga_pro_men'])
    filenames.append(['liga_pro_women', 'liga_pro_women'])
    filenames.append(['challenger_series_men', 'challenger_series_men'])
    filenames.append(['challenger_series_women', 'challenger_series_women'])
    filenames.append(['master_tour_women', 'master_tour_women'])
    filenames.append(['master_tour_men_spb', 'master_tour_men_spb'])
    filenames.append(['master_tour_men_isr', 'master_tour_men_isr'])

    with open('prepared_data/bkfon/live/all_bets_prepared.txt', 'w', encoding='utf-8') as fout:
        for dirname, segment in filenames:
            print(dirname, segment)
            if segment == 'master_tour_women_chn' or segment == 'master_tour_men_chn':
                continue
            for f in walk('data/bkfon/live_parsed_new2/' + dirname):
                for filename in sorted(f[2]):
                    if filename.find('parsed_filenames') != -1:
                        continue
                    with open('data/bkfon/live_parsed_new2/' + dirname + '/' + filename, encoding='utf-8') as fin:
                        for line in fin:
                            tokens = line.rstrip('\n').split('\t')
                            eventId = tokens[0]
                            dt = tokens[1]
                            compName = tokens[2]
                            players = [tokens[3].split(';'), tokens[4].split(';')]
                            info = json.loads(tokens[5])

                            for i in range(len(info)):
                                for name in info[i][1]:
                                    info[i][1][name]['score'] = info[i][1][name]['score'].split('http')[0].strip()

                            flError = 0
                            ids = [[], []]
                            for i in range(2):
                                for player in players[i]:
                                    player = ' '.join(player.split()).strip()
                                    player = player.replace('(ж)', '').strip()
                                    #if player == 'Желубенков Ал-р':
                                    #    player = 'Желубенков Александр'
                                    if player == 'Какунина Я':
                                        player = 'Кокунина Я'
                                    id = playersDict.getId(player)
                                    if len(id) == 1:
                                        ids[i].append(id[0])
                                    elif len(id) == 0:
                                        flError = 1
                                        if not (player in unknown):
                                            unknown[player] = 0
                                        unknown[player] += 1
                                    else:
                                        idGood = []
                                        source = 'bkfon'
                                        if segment.find('master_tour') != -1:
                                            source = 'master_tour'
                                        elif segment.find('liga_pro') != -1:
                                            source = 'liga_pro'

                                        for e in id:
                                            if (source + '\t' + dt[:10] + '\t' + e) in activePlayers:
                                                idGood.append(e)

                                        if len(idGood) == 1:
                                            ids[i].append(idGood[0])
                                            if not (player in solved):
                                                solved[player] = 0
                                            solved[player] += 1
                                        else:
                                            flError = 1
                                            fl_mw = ''
                                            for e in id:
                                                fl_mw += e[0]
                                            fl_mw = ''.join(sorted(set(list(fl_mw))))
                                            if not (fl_mw + ' ' + player in multiple):
                                                multiple[fl_mw + ' ' + player] = 0
                                            multiple[fl_mw + ' ' + player] += 1
                            if flError == 0:
                                if segment not in sourcesCount:
                                    sourcesCount[segment] = 0
                                sourcesCount[segment] += 1
                                finalScore = '\t'
                                mKey = (dt[:10] + '\t' + compName.replace('Наст. теннис.', '').strip() + '\t' + eventId)
                #                print(mKey)
                                if mKey in bkfonMatchesDict:
                                    mm = bkfonMatchesDict[mKey]
                                    finalScore = mm.setsScore + '\t' + mm.pointsScore

                                fout.write('\t'.join([segment] + tokens[:3] + [';'.join(ids[0]), ';'.join(ids[1])] +
                                                     tokens[3:] + [finalScore]) + '\n')
                                pattern = r"\(([A-Za-z0-9- ]+)\)"
                #                print(info)
                #                print(info[-1])
                                lastMatchInd = len(info) - 1
                                while not ('match' in info[lastMatchInd][1]):
                                    lastMatchInd -= 1
                                    if lastMatchInd == -1:
                                        break
                                if lastMatchInd == -1:
                                    print('bad info')
                                    raise
                                    continue
                                pointsScore = re.search(pattern, info[lastMatchInd][1]['match']['score'])
                                points = None
                                if not (pointsScore is None):
                                    pointsScore = pointsScore.group(0).replace('(', '').replace(')', '').replace(' ', ';').replace('-', ':') + ';'
                                    _, points = Match.getPointsScoreInfo(pointsScore)
                                setsScore = info[lastMatchInd][1]['match']['score'].split(' ')[0]
                                if setsScore != '' and setsScore.replace('5сетов', '').replace('7сетов', '') != '':
                                    matchHash = calcHash([dt[:10]] + ids[0] + ids[1] + [int(e) for e in setsScore.split(':')] + [e * i for i, e in enumerate(Match.getSetSumPoints(points))])
                                    if matchHash in matchesDict:
                                        mbCnt += 1
                                else:
                                    print(info[-1])

    print('\nMULTIPLE')
    for k, v in sorted(multiple.items(), key=lambda x: -x[1]):
        print([k, v])
    print('\nUNKNOWN')
    for k, v in sorted(unknown.items(), key=lambda x: -x[1]):
        print([k, v])
    print('\nSOLVED')
    for k, v in sorted(solved.items(), key=lambda x: -x[1]):
        print([k, v])
    print(mbCnt)
    for k, v in sorted(sourcesCount.items(), key=lambda x: -x[1]):
        print([k, v])

    return

if __name__ == "__main__":
    main()