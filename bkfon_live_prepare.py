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
    playersDict = GlobalPlayersDict()

    activePlayers = set()

    matchesDict = dict()

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
                ids = tokens[headerDict['id1']].split(';') + tokens[headerDict['id2']].split(';')
                dt = tokens[headerDict['date']]
                for id in ids:
                    activePlayers.add(source + '\t' + dt + '\t' + id)

                match = Match(tokens[headerDict['date']],
                              [tokens[headerDict['id1']].split(';'), tokens[headerDict['id2']].split(';')],
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

    with open('prepared_data/bkfon/live/all_bets.txt', encoding='utf-8') as fin,\
         open('prepared_data/bkfon/live/all_bets_prepared.txt', 'w', encoding='utf-8') as fout:
        for line in fin:
            tokens = line.rstrip('\n').split('\t')
            segment = tokens[0]
            if segment == 'master_tour_women_chn' or segment == 'master_tour_men_chn':
                continue
            eventId = tokens[1]
            dt = tokens[2]
            compName = tokens[3]
            players = [tokens[4].split(';'), tokens[5].split(';')]
            info = json.loads(tokens[6])

            flError = 0
            ids = [[], []]
            for i in range(2):
                for player in players[i]:
                    player = ' '.join(player.split()).strip()
                    player = player.replace('(ж)', '').strip()
                    if player == 'Желубенков Ал-р':
                        player = 'Желубенков Александр'
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
                fout.write('\t'.join(tokens[:4] + [';'.join(ids[0]), ';'.join(ids[1])] + tokens[4:]) + '\n')

                pattern = r"\(([A-Za-z0-9- ]+)\)"
                pointsScore = re.search(pattern, info[-1][1])
                points = None
                if not (pointsScore is None):
                    pointsScore = pointsScore.group(0).replace('(', '').replace(')', '').replace(' ', ';').replace('-', ':') + ';'
                    _, points = Match.getPointsScoreInfo(pointsScore)
                setsScore = info[-1][1].split(' ')[0]
                if setsScore != '':
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

    return

if __name__ == "__main__":
    main()