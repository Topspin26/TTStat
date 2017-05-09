import time
import random

import os
from os import walk

from common import *
from Entity import *
from ParserBKFon import *
import json

def parseDirs(segments, flNew = 0):
    dirname = 'data/bkfon/live'
    dirname_parsed = 'data/bkfon/live_parsed'

    for segment in segments:
        for e in os.walk(dirname):
            ff = e[0].split('\\')[-1]
            if ff == dirname:
                continue
            if os.path.exists(e[0] + '/' + segments[segment]):
                print(e[0], ff)
                if os.path.exists(dirname_parsed + '/' + ff + '/' + segments[segment]):
                    continue
                if flNew == 0:
                    parser = ParserBKFon(e[0], segments[segment], maxCnt=-1)
                else:
                    parser = ParserBKFonNew(e[0], segments[segment], maxCnt=-1)
                if not (os.path.exists(dirname_parsed + '/' + ff)):
                    os.mkdir(dirname_parsed + '/' + ff)
                with open(dirname_parsed + '/' + ff + '/' + segments[segment], 'w', encoding='utf-8') as fout:
                    for match in parser.matches:
                        fout.write('\t'.join([match.eventId, match.dt, match.compName, ';'.join(match.players[0]), ';'.join(match.players[1])]))
                        info = []
                        lastS = None
                        for i in range(len(match.ts)):
                            s = str(match.eventsInfo[i])
                            if lastS != s:
                                info.append([match.ts[i], match.eventsInfo[i]])
                            lastS = s

                        fout.write('\t' + json.dumps(info, ensure_ascii=False))
                        fout.write('\n')
                        print([match.eventId, match.dt, match.compName, match.players, match.eventsInfo[0]])
                        print([match.eventId, match.ts[-1], match.compName, match.players, match.eventsInfo[-1]])

def updateMatchDict(fp, segment, matchesBets):
    with open(fp, encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            eventId = tokens[0]
            dt = tokens[1]
            compName = tokens[2]
            players = [tokens[3].split(';'), tokens[4].split(';')]
            info = json.loads(tokens[5])
            ts = []
            eventsInfo = []
            for i in range(len(info)):
                ts.append(info[i][0])
                eventsInfo.append(info[i][1])
            matchBet = MatchBet(eventId, [], dt, compName, players, ts, eventsInfo)
            mbKey = compName + '\t' + eventId + '\t' + ';'.join(players[0]) + '\t' + ';'.join(players[1])
            if mbKey in matchesBets:
                try:
                    print(mbKey)
                    matchesBets[mbKey] = [matchesBets[mbKey][0] + [segment], matchesBets[mbKey][1].merge(matchBet)]
                except Exception as e:
                    print('Error')
                    print(e)
                    print(matchesBets[mbKey][0])
                    print(matchesBets[mbKey][1])
                    print(matchBet)
                    print(dt)
                    print(mbKey)
                    raise
            else:
                matchesBets[mbKey] = [[segment], matchBet]


def main():
    #playersDict = GlobalPlayersDict()

    segments = dict()

    segments = {'master_tour_mix': 'segment28824.txt',
                'master_tour_women': 'segment25827.txt',  # + CHINA!?
                'master_tour_men_spb': 'segment26989.txt',
                'master_tour_men_isr': 'segment30240.txt',
                'master_tour_women_chn': 'segment18054.txt',
                'master_tour_men_chn': 'segment34654.txt'}

    segments['liga_pro_men'] = 'segment37716.txt'
    segments['liga_pro_women'] = 'segment37984.txt'
    segments['challenger_series_men'] = 'segment13574.txt'
    segments['challenger_series_women'] = 'segment19423.txt'

    segments1 = dict()
    segments1['liga_pro_men'] = 'Наст. теннис. Лига Про. Москва.txt'
    segments1['liga_pro_women'] = 'Наст.теннис.Жен.Лига Про.Москва.txt'
    segments1['challenger_series_men'] = 'Наст. теннис. Челленджер серия.txt'
    segments1['challenger_series_women'] = 'Наст. теннис. Жен. Челленджер серия.txt'
    segments1['master_tour_men_spb'] = 'Наст. теннис. Мастер-Тур. С-Петербург.txt'
    segments1['master_tour_women'] = 'Наст. теннис. Жен. Мастер-Тур. С-Петербург.txt'
    segments1['master_tour_men_isr'] = 'Наст. теннис. Мастер-Тур. Израиль.txt'

#    parseDirs(segments, flNew = 0)
    parseDirs(segments1, flNew = 1)

    dirname_parsed = 'data/bkfon/live_parsed'

    matchesBets = dict()
    for segment in segments:
#        break
        filename = segments[segment]
        for f in walk(dirname_parsed):
            for ff in f[2]:
                fp = os.path.abspath(os.path.join(f[0], ff))
                if fp.find(filename) != -1:
                    updateMatchDict(fp, segment, matchesBets)

    for segment in segments1:
        filename = segments1[segment]
        for f in walk(dirname_parsed):
            for ff in f[2]:
                fp = os.path.abspath(os.path.join(f[0], ff))
                if fp.find(filename) != -1:
                    updateMatchDict(fp, segment, matchesBets)

    print(len(matchesBets))

    with open('prepared_data/bkfon/live/all_bets.txt', 'w', encoding='utf-8') as fout:
        for mbKey, matchBet in sorted(matchesBets.items(), key = lambda x: x[1][1].dt):
            segment = matchBet[0]
            match = matchBet[1]
            fout.write(';'.join(segment) + '\t')
            fout.write('\t'.join(
                [match.eventId, match.dt, match.compName, ';'.join(match.players[0]), ';'.join(match.players[1])]))
#            info = []
#            lastS = None
#            for i in range(len(match.ts)):
#                if match.score[i].find('http') != -1:
#                    match.score[i] = match.score[i].split('http')[0].strip()
#                s = ';'.join([match.score[i], ';'.join([str(ee) for ee in match.bet_win[0][i]]),
#                              ';'.join([str(ee) for ee in match.bet_win[1][i]])])
#                if lastS != s:
#                info.append([match.ts[i], match.score[i], [match.bet_win[0][i], match.bet_win[1][i]]])
#                lastS = s
            info = []
            for i in range(len(match.ts)):
                info.append([match.ts[i], match.eventsInfo[i]])
            fout.write('\t' + json.dumps(info, ensure_ascii=False))
            fout.write('\n')

    return

    for e in segments:
        print(e)
        parserBKFon[e] = ParserBKFon(dirname, segments[e], maxCnt=10000)

    players = set()
    
    print(len(parserBKFon.matches))


    for match in parserBKFon.matches:
#    for key,value in matches.items():
#        match = Match(value)
        for i in range(2):
            for j in range(len(match.players[i])):
                if not(match.players[i][j]) in women2_players and not(match.players[i][j]) in men2_players:
                    print(match.players[i])
#        players.add(match.players[0])
#        players.add(match.players[1])

        print(match.eventId)
        print(match.compName)
        print(match.players)
        for i in range(len(match.score)):
            print((match.score[i], match.bet_win[0][i], match.bet_win[1][i]))

#        print(match.score)
#        print(match.win[0])
#        print(match.win[1])
    
    return

#    for f in walk(dir):
#        for ff in f[2]:
#            if ff[:7] == 'segment':
#                print(ff)
#                ParserBKFon.parseOneSegment(dir + '/' + ff)
#    match = Match(matches['event5192677'])
#    with open('foo_out.txt', 'w') as fout:
#        for e in sorted(players):
#            fout.write(e + '\n')
    
    '''    
    fout = ''
    for e in eventsData:
        if e[0] != lastEventId:
            lastEventId = e[0]
            if fout != '':
                fout.close()
            fout = open(e[0] + '.txt', 'a', encoding='utf-8')
        fout.write(e[1] + '\n')
    if fout != '':
        fout.close()
    
    time.sleep(timeout)
    '''        
    return

if __name__ == "__main__":
    main()