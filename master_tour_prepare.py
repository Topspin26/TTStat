from os import walk
import time
import datetime as datetime
import random
import re
from common import *
from Entity import *

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

    playersDict = GlobalPlayersDict()

    corrections = readCorrections('data/master_tour/corrections.txt')

    wrongLines = list()
    matches = getMatches(corrections, wrongLines)
    print(len(matches))
    for line in wrongLines:
        print(line, end = ' ')

    multiple = dict()
    solved = dict()
    unknown = dict()

    idsAll = set()
    for match in matches:
        if match.flError == 0:
            for i in range(2):
                for player in match.players[i]:
                    id = playersDict.getId(player)
                    if len(id) == 1:
                        idsAll.add(id[0])

    with open('prepared_data/master_tour/all_results.txt', 'w', encoding='utf-8') as fout:
        fout.write('date\ttime\tcompName\tid1\tid2\t')
        fout.write('setsScore\tpointsScore\tname1\tname2\n')
        for match in matches:
            if match.flError == 0:
                flError = 0
                ids = [[], []]
                for i in range(2):
                    for player in match.players[i]:
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
                            for e in id:
                                if e in idsAll:
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

                if flError == 0 and len(ids[0]) > 0 and len(ids[1]) > 0:
                    resTokens = match.toArr()
                    resTokens.append(resTokens[3])
                    resTokens.append(resTokens[4])
                    resTokens[3] = ';'.join(ids[0])
                    resTokens[4] = ';'.join(ids[1])
                    fout.write('\t'.join(resTokens) + '\n')
                else:
                    print('flError ' + match.toStr())
            else:
                print('match.flError ' + match.toStr())

        print('\nMULTIPLE')
        for k,v in sorted(multiple.items(), key = lambda x: -x[1]):
            print([k, v])
        print('\nUNKNOWN')
        for k,v in sorted(unknown.items(), key = lambda x: -x[1]):
            print([k, v])
        print('\nSOLVED')
        for k,v in sorted(solved.items(), key = lambda x: -x[1]):
            print([k, v])

if __name__ == "__main__":
    main()