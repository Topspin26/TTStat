from os import walk
import time
import datetime as datetime
import random
import re
from common import *
from Entity import *

def getPlayerId(player, men2_players, women2_players):
    res = '0'
    if player in men2_players:
        res = men2_players[player][0]
    if player in women2_players:
        res = women2_players[player][0]
    return res

def checkCorrectness(men_players, men2_players, women_players, women2_players, corrections, wrongLines):
    new_players_dict = dict()
    pairs_players = set()
    for f in walk('data/master_tour/results'):
        for ff in f[2]:
#            print(ff)
            with open('data/master_tour/results/' + ff, 'r', encoding='utf-8') as fin:
                for line in fin:
                    if line in corrections:
                        line = corrections[line]
                    tokens = line.split('\t')
                    tokens = [e.strip() for e in tokens]
                    if tokens[5] == '':
#                        print(line.strip())
                        wrongLines.add(line)
                        continue
                    for i in range(2,4):
                        t = tokens[i]
                        t = t.replace('ё', 'е')
                        if t.find('(') != -1:
                            wrongLines.add(line)
                            if t.find('дисквалификация') == -1:
                                print(line.strip())
                            continue
                        if t.find('-') != -1:
                            p = t.split('-')
                            p1 = p[0].strip()
                            p2 = p[1].strip()
                            pairs_players.add(p1)
                            pairs_players.add(p2)
                            for p in [p1, p2]:
                                if not (p in men2_players) and not (p in women2_players):
                                    print('NEW PAIRED PLAYER: ' + p)
                                    print(line)
                                else:
                                    if p in men2_players and p in women2_players:
                                        print('PAIRED PLAYER: W or M?: ' + p)
                                        print(line)
                                    else:
                                        if p in men2_players:
                                            if len(men2_players[p]) > 1:
                                                print('PAIRED MULTIPLE MEN: ' + p) 
                                                print(line)
                                        if p in women2_players:
                                            if len(women2_players[p]) > 1:
                                                print('PAIRED MULTIPLE WOMEN: ' + p) 
                                                print(line)
                        else:
                            p = t.strip()
                            if not (p in men_players) and not (p in women_players):
                                if not (p in new_players_dict):
                                    new_players_dict[p] = [0, 0]
                                if tokens[5 - i].strip() in men_players:
                                    new_players_dict[p][0] += 1
                                if tokens[5 - i].strip() in women_players:
                                    new_players_dict[p][1] += 1
                    if not (tokens[5] in ['0:3', '1:3', '2:3', '3:2', '3:1', '3:0']):
                        wrongLines.add(line)
#                        print(line.strip())
                    set1 = set2 = 0
                    if len(tokens[4]) == 0:
#                        print(line.strip())
                        wrongLines.add(line)
                    else:
                        if tokens[4][-1] == ';':
                            tokens[4] = tokens[4][:-1] 
                        for e in tokens[4].split(';'):
                            if not checkSetScore(e):
                                print(line)
                                wrongLines.add(line)
                            tt = e.split(':')
                            try:
                                set1 += (int(tt[0]) > int(tt[1]))
                                set2 += (int(tt[1]) > int(tt[0]))
                            except:
                                pass
                        if tokens[5] != str(set1) + ':' + str(set2):
                            print(line.strip())
                            wrongLines.add(line)
                        
                            
    for e in new_players_dict.items():
        print('NEW SINGLE PLAYER')
        print(e)

def getMatches(corrections, wrongLines):
    pattern = re.compile('|'.join(corrections.keys()))
    matches = []
    for f in walk('data/master_tour/results'):
        for ff in f[2]:
            with open('data/master_tour/results/' + ff, 'r', encoding='utf-8') as fin:
                for line in fin:
                    line = corrections.get(line, line)
                    line = pattern.sub(lambda x: corrections[x.group()], line)
                    tokens = line.split('\t')
                    tokens = [e.strip() for e in tokens]
                    if tokens[5] == '':
                        wrongLines.append(line)
                        continue

                    if tokens[2].find('(') != -1:
                        wrongLines.append(line)
                        continue
                    if tokens[3].find('(') != -1:
                        wrongLines.append(line)
                        continue
                    if not (tokens[5] in ['0:3', '1:3', '2:3', '3:2', '3:1', '3:0']) or len(tokens[4]) == 0:
                        wrongLines.append(line)
                        continue
                    matches.append(Match(tokens[0],
                                         [[e.strip() for e in tokens[2].replace('ё', 'е').strip().split('-')],
                                          [e.strip() for e in tokens[3].replace('ё', 'е').strip().split('-')]],
                                         setsScore=tokens[5].strip(),
                                         pointsScore=tokens[4].strip(),
                                         time=tokens[1],
                                         compName='Мастер-тур, ' + ff[:10]))
    return matches

def main():

    filenameGlobalPlayersMen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_men.txt'
    (mIdG, mId2G) = readPlayersInv(filenameGlobalPlayersMen)
    filenameGlobalPlayersWomen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_women.txt'
    (wIdG, wId2G) = readPlayersInv(filenameGlobalPlayersWomen)

#    (men_players, men2_players) = readPlayersInv('prepared_data/master_tour/master_tour_players_men.txt')
#    (women_players, women2_players) = readPlayersInv('prepared_data/master_tour/master_tour_players_women.txt')

    corrections = readCorrections('data/master_tour/corrections.txt')

    wrongLines = list()
    matches = getMatches(corrections, wrongLines)
    print(len(matches))
    for line in wrongLines:
        print(line, end = ' ')
    #return

#    checkCorrectness(men_players, men2_players, women_players, women2_players, corrections, wrongLines)
    for e in sorted(list(wrongLines)):
        print(e.strip())

    with open('prepared_data/master_tour/all_results.txt', 'w', encoding='utf-8') as fout:
        fout.write('date\ttime\tcompName\tid1\tid2\t')
        fout.write('setsScore\tpointsScore\tname1\tname2\n')
        for f in walk('data/master_tour/results'):
            for ff in f[2]:
                with open('data/master_tour/results/' + ff, 'r', encoding='utf-8') as fin:
                    for line in fin:
                        if line in corrections:
                            line = corrections[line]                        
                        if line in wrongLines:
                            continue
                        try:
                            flBad = 0
                            tokens = line.split('\t')
                            tokens = [e.strip() for e in tokens]
                            isPair = '0'
                            pp = [[], []]
                            for i in range(2,4):
                                t = tokens[i]
                                if t.find('-') != -1:
                                    isPair = '1'
                                    p = t.split('-')
                                    pp[i - 2] = [ee.strip() for ee in p]
                                    id0 = getPlayerId(p[0].strip(), mId2G, wId2G)
                                    id1 = getPlayerId(p[1].strip(), mId2G, wId2G)
                                    if id0 == '0' or id1 == '0':
                                        flBad = 1 
                                    p = id0 + ';' + id1
                                else:
                                    pp[i - 2].append(t.strip())
                                    id0 = getPlayerId(t.strip(), mId2G, wId2G)
                                    p = id0
                                    if id0 == '0':
                                        print(t.strip())
                                        flBad = 1 
                                tokens[i] = p
                            if flBad == 1:
                                continue
                            tokens1 = list(tokens[:2])
                            tokens1.append('Мастер Тур ' + ff[:-4])
                            #tokens1.append(str(isPair))
                            tokens1 += tokens[2:4]
                            #sets = tokens[5].split(':')
                            #tokens1.append(str(0 + (int(sets[0]) > int(sets[1]))))
                            #tokens1.append(str(0 + (int(sets[1]) > int(sets[0]))))
                            #tokens1 += sets
                            #points = getPoints(tokens[4])
                            #tokens1 += [str(points[0]), str(points[1])]
                            tokens1 += [tokens[-1], tokens[-2]]
                            tokens1 += [';'.join(pp[0]), ';'.join(pp[1])]

                            fout.write('\t'.join(tokens1) + '\n')
                        except Exception as exc:
                            print(exc)
                            print(line)

if __name__ == "__main__":
    main()