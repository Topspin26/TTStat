from os import walk
import time
import datetime as datetime
import random
import re


def read_players(filename):
    players = dict()
    players2 = dict()
    with open(filename, 'r', encoding = 'utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            id = tokens[0].strip()
            names = tokens[1].strip().split(';')
            for name in names:
                players[name] = id
                tn = name.split(' ')
#                print(tn)
                for short_player in [name, tn[1], tn[1] + ' ' + tn[0][0] + '.', tn[1] + ' ' + tn[0][0]]:
                    if not (short_player in players2):
                        players2[short_player] = [id]
                    else:
                        players2[short_player].append(id)
                        players2[short_player] = list(set(players2[short_player]))
    return (players, players2) 

def checkSetScore(score):
    tt = score.split(':')
    res = True
    try:
        set1 = int(tt[0])
        set2 = int(tt[1])
        if min(set1, set2) < 0 or max(set1, set2) < 11:
            res = False
        if max(set1, set2) == 11:
            if min(set1, set2) > 9:
                res = False
        else:
            if max(set1, set2) - min(set1, set2) != 2:
                res = False
    except:
        res = False
    return res

def getPoints(pointsScore):
    res = [0, 0]
    for e in pointsScore.split(';'):
        try:
            tt = e.split(':')
            res[0] += int(tt[0])
            res[1] += int(tt[1])
        except:
            pass
    return res

def checkCorrectness(men_players, men2_players, women_players, women2_players, wrongLines):
    new_players_dict = dict()
    pairs_players = set()
    for f in walk('data/master_tour/results'):
        for ff in f[2]:
#            print(ff)
            with open('data/master_tour/results/' + ff, 'r', encoding='utf-8') as fin:
                for line in fin:
                    tokens = line.split('\t')
                    tokens = [e.strip() for e in tokens]
                    if tokens[5] == '':
#                        print(line.strip())
                        wrongLines.add(line)
                        continue
                    for i in range(2,4):
                        t = tokens[i]
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
        

def getPlayerId(player, men2_players, women2_players):
    res = '0'
    if player in men2_players:
        res = men2_players[player][0]
    if player in women2_players:
        res = women2_players[player][0]
    return res

def main():

    (men_players, men2_players) = read_players('data/master_tour/master_tour_players_men.txt')
    (women_players, women2_players) = read_players('data/master_tour/master_tour_players_women.txt')
#    for e in men2_players.items():
#        print(e)
#    for e in women2_players.items():
#        print(e)
    wrongLines = set()
    checkCorrectness(men_players, men2_players, women_players, women2_players, wrongLines)
    for e in sorted(list(wrongLines)):
        print(e.strip())

    with open('data/master_tour/all_results.txt', 'w', encoding='utf-8') as fout:
        fout.write('date\ttime\tisPair\tid1\tid2\t')
        fout.write('win1\twin2\tset1\tset2\tpoints1\tpoints2\tsetsScore\tpointsScore\n')
        for f in walk('data/master_tour/results'):
            for ff in f[2]:
                with open('data/master_tour/results/' + ff, 'r', encoding='utf-8') as fin:
                    for line in fin:
                        if line in wrongLines:
                            continue
                        tokens = line.split('\t')
                        tokens = [e.strip() for e in tokens]
                        isPair = '0'
                        for i in range(2,4):
                            t = tokens[i]
                            if t.find('-') != -1:
                                isPair = '1'
                                p = t.split('-')
                                p = getPlayerId(p[0].strip(), men2_players, women2_players) + \
                                ';' + getPlayerId(p[1].strip(), men2_players, women2_players)
                            else:
                                p = getPlayerId(t.strip(), men2_players, women2_players)
                            tokens[i] = p
                        tokens1 = list(tokens[:2])
                        tokens1.append(str(isPair))
                        tokens1 += tokens[2:4]
                        sets = tokens[5].split(':')
                        tokens1.append(str(0 + (int(sets[0]) > int(sets[1]))))
                        tokens1.append(str(0 + (int(sets[1]) > int(sets[0]))))
                        tokens1 += sets
                        points = getPoints(tokens[4])
                        tokens1 += [str(points[0]), str(points[1])]
                        tokens1 += [tokens[-1], tokens[-2]]
                        fout.write('\t'.join(tokens1) + '\n')
                                

if __name__ == "__main__":
    main()