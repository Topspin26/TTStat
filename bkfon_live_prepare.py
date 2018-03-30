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

    sources = []
    sources.append(['master_tour', 'prepared_data/master_tour/all_results.txt'])
    sources.append(['liga_pro', 'prepared_data/liga_pro/all_results.txt'])
    sources.append(['bkfon', 'prepared_data/bkfon/all_results.txt'])

    matchesStorage = MatchesStorage(sources)
    matchesDict = matchesStorage.matchesDict

    bkfonMatchesDict = dict()
    for match in matchesStorage.getMatches(source='bkfon'):
        bkfonMatchesDict[match.date + '\t' + match.compName + '\t' + match.matchId] = match

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
                    if filename.find('_last') != -1:
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
                                            if matchesStorage.isActive(e, source, dt[:10]):
                                                idGood.append(e)

                                        if len(idGood) == 1:
                                            ids[i].append(idGood[0])
                                            if player not in solved:
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
                #                print(info)
                #                print(info[-1])


                                matchBet = MatchBet(eventId, dt, compName, ids, info, names=players)
                                match = matchBet.buildMatch()
                                setsScore, pointsScore = match.setsScore, match.pointsScore

                                if setsScore != '':
                                    matchHash = match.getHash()
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