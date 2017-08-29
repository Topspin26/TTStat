from os import walk
import re
from Entity import *
from Logger import Logger


class MasterTourPreparator:

    @staticmethod
    def run(logger=Logger()):
        print('MasterTourPreparator')
        logger.print('MasterTourPreparator')

        playersDict = GlobalPlayersDict('filtered')

        corrections = readCorrections('data/master_tour/corrections.txt')

        wrongLines = list()
        matches = MasterTourPreparator.getMatches(corrections, wrongLines)
        logger.print(len(matches))
        for line in wrongLines:
            logger.print(line, end=' ')

        logger.print()
        logger.print('---------------------')
        multiple = dict()
        solved = dict()
        unknown = dict()

        idsAll = set()
        for match in matches:
            if match.flError == 0:
                for i in range(2):
                    for player in match.names[i]:
                        id = playersDict.getId(player)
                        if len(id) == 1:
                            idsAll.add(id[0])

        with open('prepared_data/master_tour/all_results.txt', 'w', encoding='utf-8') as fout:
            fout.write('\t'.join(['date', 'time', 'compName', 'id1', 'id2',
                                  'setsScore', 'pointsScore', 'name1', 'name2']) + '\n')
            for match in matches:
                if match.flError == 0:
                    flError = 0
                    ids = [[], []]
                    for i in range(2):
                        for player in match.names[i]:
                            id = playersDict.getId(player)

                            if player == 'Анастасия Голубева':
                                if match.compName == 'Мастер-тур, 2014-05-12' or \
                                   match.compName == 'Мастер-тур, 2014-08-11':
                                    id = ['w11133']
                                elif match.date <= '2017':
                                    id = ['w9']

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
                        logger.print('flError ' + match.toStr())
                else:
                    logger.print('match.flError ' + match.toStr())

        logger.print('\nMULTIPLE')
        for k, v in sorted(multiple.items(), key=lambda x: -x[1]):
            logger.print([k, v])
        logger.print('\nUNKNOWN')
        for k, v in sorted(unknown.items(), key=lambda x: -x[1]):
            logger.print([k, v])
        logger.print('\nSOLVED')
        for k, v in sorted(solved.items(), key=lambda x: -x[1]):
            logger.print([k, v])

    @staticmethod
    def getMatches(corrections, wrongLines):
        pattern = re.compile('|'.join(corrections.keys()))
        matches = []
        for f in walk('data/master_tour/results'):
            for ff in sorted(f[2]):
                with open('data/master_tour/results/' + ff, 'r', encoding='utf-8') as fin:
                    for line in fin:
                        line = corrections.get(line, line)
                        line = pattern.sub(lambda x: corrections[x.group()], line)
                        tokens = line.split('\t')
                        tokens = [e.strip() for e in tokens]
                        if tokens[5] == '':
                            wrongLines.append(line)
                            continue

                        if tokens[3].find('(') != -1:
                            wrongLines.append(line)
                            continue
                        if tokens[4].find('(') != -1:
                            wrongLines.append(line)
                            continue
                        if tokens[5] not in ['0:3', '1:3', '2:3', '3:2', '3:1', '3:0'] or len(tokens[6]) == 0:
                            wrongLines.append(line)
                            continue
                        names = [[e.strip() for e in tokens[3].replace('ё', 'е').strip().split('-')],
                                 [e.strip() for e in tokens[4].replace('ё', 'е').strip().split('-')]]
                        matches.append(Match(tokens[0],
                                             names,
                                             names=names,
                                             setsScore=tokens[5].strip(),
                                             pointsScore=tokens[6].strip(),
                                             time=tokens[1],
                                             compName='Мастер-тур, ' + ff[:10]))
        return matches


def main():
    MasterTourPreparator.run(logger=Logger('MasterTourPreparator.txt'))

if __name__ == "__main__":
    main()