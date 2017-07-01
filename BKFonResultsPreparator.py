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
    ligaProCorr.append(['Воронов А', 'Александр Воронов'])

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

class BKFonResultsPreparator:

    @staticmethod
    def run():
        playersDict = GlobalPlayersDict("filtered")

        corrections = readCorrectionsList('data/bkfon/corrections.txt')
        wrongLines = []
        matches = BKFonResultsPreparator.getMatches(corrections, wrongLines)
        print(len(matches))
        players = BKFonResultsPreparator.getMatchesPlayers(matches)

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
            if len(match.names[0]) == 1:
                pl1 = match.names[0][0]
                pl2 = match.names[1][0]
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

        with open(prefix + 'bkfon_players_x_mw.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(playersMW.items(), key=lambda x: -x[1][2]):
                #        for e in sorted(playersMW.items(), key = lambda x: (x[1][0] + 1) / (x[1][2] + 2)):
                if (e[0] in unknown) and e[1][2] > 0:
                    print(e)
                    fout.write(e[0] + '\t' + str(e[1]) + '\t' + '\t'.join(playersMatches[e[0]]) + '\n')

        with open(prefix + 'bkfon_players_men.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(m.keys()):
                fout.write(e + '\t' + ';'.join(playersDict.getId(e)) + '\n')
        with open(prefix + 'bkfon_players_women.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(w.keys()):
                fout.write(e + '\t' + ';'.join(playersDict.getId(e)) + '\n')
        with open(prefix + 'bkfon_players_mw.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(mw.keys()):
                fout.write(e + '\t' + ';'.join(playersDict.getId(e)) + '\n')

        multiple = dict()
        unknown = dict()

        with open(prefix + 'all_results.txt', 'w', encoding='utf-8') as fout, open(prefix + 'players_collisions.txt',
                                                                                   'w', encoding='utf-8') as fout1:
            fout.write('\t'.join(
                ['date', 'time', 'compName', 'id1', 'id2', 'setsScore', 'pointsScore', 'name1', 'name2',
                 'matchId']) + '\n')
            for match in matches:
                flError = 0
                if match.flError == 0:
                    #                print(match.toStr())
                    ids = [[], []]
                    for i in range(2):
                        for player in match.names[i]:

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
                                # print('MANY ' + player + ' ' + str(id) + ' ' + match.toStr())

                    if flError == 0:
                        resTokens = match.toArr()
                        resTokens.append(resTokens[3])
                        resTokens.append(resTokens[4])
                        resTokens[3] = ';'.join(ids[0])
                        resTokens[4] = ';'.join(ids[1])
                        resTokens.append(match.matchId)
                        fout.write('\t'.join(resTokens) + '\n')
                if (match.flError != 0 or flError != 0) and match.compName.lower().replace('-', '').find(
                        'лига про') != -1:
                    print('LIGA PRO error ' + str(match.flError) + ' ' + str(flError) + ' ' + match.toStr())

        with open(prefix + 'bkfon_players_multiple.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(multiple.items(), key=lambda x: -x[1]):
                fout.write(e[0] + '\t' + str(e[1]) + '\n')
        with open(prefix + 'bkfon_players_unknown.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(unknown.items(), key=lambda x: -x[1]):
                fout.write(e[0] + '\t' + str(e[1]) + '\n')

    @staticmethod
    def process(filename, matches, matchesHashes, corrections):
        with open(filename, 'r', encoding='utf-8') as fin:
            for line in fin:
                dt, matchTime, compName, matchId, names1, names2, setsScore, pointsScore = line.rstrip('\n').split('\t')
                names = [names1, names2]

                tcorr = corrections.copy()
                if compName.replace('Жен. ', '').find('Лига Про. Москва') != -1:
                    tcorr += lpCorr
                if compName.replace('Жен. ', '').find('Челленджер серия') != -1:
                    tcorr += chsCorr
                if compName.replace('Жен. ', '').find('Мастер-Тур') != -1:
                    tcorr += mtCorr

    #            names = re.sub(' +', ' ', names.replace(u'\xa0', ' '))
    #            names = names.strip().split(' - ')

                for k, v in tcorr:
                    if k.find(';') != -1:
                        if k.split(';')[0] == dt:
                            names = [e.replace(k.split(';')[1], v) for e in names]
                    else:
                        names = [e.replace(k, v) for e in names]
                        #                    print(names)

    #            if (names[0] + names[1]).find('Харимото') != -1:
    #                print(filename, line)
                names = [names[0].split(';'), names[1].split(';')]
                if pointsScore != 'отмена' and pointsScore != 'прерван' and len(setsScore) > 0:
                    match = Match(dt,
                                  names,
                                  names=names,
                                  setsScore=setsScore,
                                  pointsScore=pointsScore,
                                  time=matchTime,
                                  compName=compName,
                                  matchId=matchId)
                    try:
                        mHash = calcHash([match.date, match.time] + match.names[0] + match.names[1] + match.sets)
                    except:
                        print(line)
                        raise
                    if mHash not in matchesHashes:
                        matches.append(match)
                        matchesHashes[mHash] = filename + '\t' + line.rstrip()
                    else:
                        print(matchesHashes[mHash])
                        print(filename + '\t' + line.rstrip())
                        print()


    @staticmethod
    def getMatches(corrections, wrongLines):
        matches = list()
        matchesHashes = dict()
        for f in walk('data/bkfon/results_parsed'):
            for ff in f[2]:
                BKFonResultsPreparator.process('data/bkfon/results_parsed' + '/' + ff, matches, matchesHashes, corrections)
    #            if ff.find('new') != -1:
    #                processNew(ff, matches, corrections)
    #            else:
    #                processOld(ff, matches, corrections)
        return matches

    @staticmethod
    def getMatchesPlayers(matches):
        res = dict()
        for match in matches:
            for i in range(2):
                for player in match.names[i]:
                    updateDict(res, player)
        return res


def main():
    BKFonResultsPreparator.run()

if __name__ == "__main__":
    main()