from os import walk
import re
from Entity import *


class ChallengerSeriesPreparator:

    @staticmethod
    def run():
        playersDict = GlobalPlayersDict("filtered")

        corrections = dict()
        corrections['Chtchetinine Evgueny'] = 'CHTCHETININE Evgueni'
        corrections['Horejsi Mirsolav'] = 'Horejsi Miroslav'
        corrections['MÖregardh Malte'] = 'Moregard Malte'
        wrongLines = list()
        matches = ChallengerSeriesPreparator.getMatches(corrections, wrongLines)
        print(len(matches))
        for line in wrongLines:
            print(line, end=' ')

        multiple = dict()
        solved = dict()
        unknown = dict()

        with open('prepared_data/challenger_series/all_results.txt', 'w', encoding='utf-8') as fout:
            fout.write('\t'.join(['date', 'time', 'compName', 'id1', 'id2',
                                  'setsScore', 'pointsScore', 'name1', 'name2']) + '\n')
            for match in matches:
                if match.flError == 0:
                    flError = 0
                    ids = [[], []]
                    for i in range(2):
                        for player in match.names[i]:
                            id = playersDict.getId(player)
                            if len(id) == 1:
                                ids[i].append(id[0])
                            elif len(id) == 0:
                                flError = 1
                                if not (player in unknown):
                                    unknown[player] = 0
                                unknown[player] += 1
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
        for k, v in sorted(multiple.items(), key=lambda x: -x[1]):
            print([k, v])
        print('\nUNKNOWN')
        for k, v in sorted(unknown.items(), key=lambda x: -x[1]):
            print([k, v])

    @staticmethod
    def getMatches(corrections, wrongLines):
        pattern = re.compile('|'.join(corrections.keys()))
        matches = []
        for f in walk('data/challenger_series/results'):
            for ff in f[2]:
                with open('data/challenger_series/results/' + ff, 'r', encoding='utf-8') as fin:
                    for line in fin:
    #                    line = corrections.get(line, line)
                        line = pattern.sub(lambda x: corrections[x.group()], line)
                        tokens = line.split('\t')
                        tokens = [e.strip() for e in tokens]
                        if ff[:10] == '2014-06-26' or ff[:10] == '2014-06-19':
                            tokens[2] = tokens[2].replace(' ', ';')
                            tokens[3] = tokens[3].replace(' ', ';')

                        for i in [2,3]:
                            for e in ['(', ')', '[', ']', 'BLR', 'CZE', 'POL', 'HUN', 'ESP', 'BEL', 'GER', 'SVK', 'CRO', 'UKR']:
                                tokens[i] = tokens[i].replace(e, '').strip()
                        names = [tokens[2].replace('Ö', 'o').split(';'), tokens[3].replace('Ö', 'o').split(';')]
                        matches.append(Match(tokens[0],
                                             names,
                                             names=names,
                                             setsScore=tokens[4].strip().replace('-',':').replace('(','').replace(')',''),
                                             pointsScore=None,
                                             time=tokens[1],
                                             compName='Challenger Series, ' + ff[:10]))
        return matches

def main():
    ChallengerSeriesPreparator.run()

if __name__ == "__main__":
    main()