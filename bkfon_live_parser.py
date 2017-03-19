import time
import random

import os
from os import walk

from common import *
from Entity import *
from ParserBKFon import ParserBKFon
import json

def parseDirs(segments):
    dirname = 'D:/Programming/SportPrognoseSystem/BetsWinner/data/bkfon/live'
    dirname_parsed = 'D:/Programming/SportPrognoseSystem/BetsWinner/data/bkfon/live_parsed'

    for segment in segments:
        for e in os.walk(dirname):
            ff = e[0].split('\\')[-1]
            if ff == dirname:
                continue
            print(e[0], ff)
            if os.path.exists(e[0] + '/' + segments[segment]):
                if os.path.exists(dirname_parsed + '/' + ff + '/' + segments[segment]):
                    continue
                parser = ParserBKFon(e[0], segments[segment], maxCnt=-1)
                if not (os.path.exists(dirname_parsed + '/' + ff)):
                    os.mkdir(dirname_parsed + '/' + ff)
                with open(dirname_parsed + '/' + ff + '/' + segments[segment], 'w', encoding='utf-8') as fout:
                    for match in parser.matches:
                        fout.write('\t'.join([match.eventId, match.dt, match.compName, ';'.join(match.players[0]), ';'.join(match.players[1])]))
                        info = []
                        lastS = None
                        for i in range(len(match.ts)):
                            s = ';'.join([match.score[i], ';'.join([str(ee) for ee in match.bet_win[0][i]]), ';'.join([str(ee) for ee in match.bet_win[1][i]])])
                            if lastS != s:
                                info.append([match.ts[i], match.score[i], [match.bet_win[0][i], match.bet_win[1][i]]])
                            lastS = s

                        fout.write('\t' + json.dumps(info, ensure_ascii=False))
                        fout.write('\n')
                        print([match.eventId, match.dt, match.compName, match.players, match.score[0], [match.bet_win[0][0], match.bet_win[1][0]]])
                        print([match.eventId, match.ts[-1], match.compName, match.players, match.score[-1], [match.bet_win[0][-1], match.bet_win[1][-1]]])

def main():
    #playersDict = GlobalPlayersDict()

    segments = {'master_tour_mix': 'segment28824.txt',
                'master_tour_women': 'segment25827.txt',  # + CHINA!?
                'master_tour_men_spb': 'segment26989.txt',
                'master_tour_men_isr': 'segment30240.txt',
                'master_tour_women_chn': 'segment18054.txt',
                'master_tour_men_chn': 'segment34654.txt'}

    segments['liga_pro_men'] = 'segment37716.txt'
    segments['liga_pro_women'] = 'segment37984.txt'

#    parseDirs(segments)

    dirname_parsed = 'D:/Programming/SportPrognoseSystem/BetsWinner/data/bkfon/live_parsed'

    matchesBets = dict()
    for segment in segments:
        filename = segments[segment]
        for f in walk(dirname_parsed):
            for ff in f[2]:
                fp = os.path.abspath(os.path.join(f[0], ff))
                if fp.find(filename) != -1:
                    with open(fp, encoding='utf-8') as fin:
                        for line in fin:
                            tokens = line.split('\t')
                            eventId = tokens[0]
                            dt = tokens[1]
                            compName = tokens[2]
                            players = [tokens[3].split(';'), tokens[4].split(';')]
                            info = json.loads(tokens[5])
                            ts = []; score = []; bet_win = [[],[]]
                            for i in range(len(info)):
                                ts.append(info[i][0])
                                score.append(info[i][1])
                                bet_win[0].append(info[i][2][0])
                                bet_win[1].append(info[i][2][1])
                            matchBet = MatchBet(eventId, [], dt, compName, players, ts, score, bet_win)
                            mbKey = eventId
                            if mbKey in matchesBets:
                                try:
                                    print(mbKey)
                                    matchesBets[mbKey] = [matchesBets[mbKey][0] + segment, matchesBets[mbKey][1].merge(matchBet)]
                                except:
                                    print('Error')
                                    print(dt)
                                    print(mbKey)
                            else:
                                matchesBets[mbKey] = [[segment], matchBet]

    print(len(matchesBets))
    with open('prepared_data/bkfon/live/all_bets.txt', 'w', encoding='utf-8') as fout:
        for mbKey, matchBet in sorted(matchesBets.items(), key = lambda x: x[1][1].dt):
            segment = matchBet[0]
            match = matchBet[1]
            fout.write(';'.join(segment) + '\t')
            fout.write('\t'.join(
                [match.eventId, match.dt, match.compName, ';'.join(match.players[0]), ';'.join(match.players[1])]))
            info = []
            lastS = None
            for i in range(len(match.ts)):
                if match.score[i].find('http') != -1:
                    match.score[i] = match.score[i].split('http')[0].strip()
                s = ';'.join([match.score[i], ';'.join([str(ee) for ee in match.bet_win[0][i]]),
                              ';'.join([str(ee) for ee in match.bet_win[1][i]])])
                if lastS != s:
                    info.append([match.ts[i], match.score[i], [match.bet_win[0][i], match.bet_win[1][i]]])
                lastS = s

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