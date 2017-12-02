from os import walk
import datetime as datetime
import re
from Entity import *
from Logger import Logger


class LigaProPreparator:

    @staticmethod
    def run(logger=Logger()):
        print('LigaProPreparator')
        logger.print('LigaProPreparator')

        corrections = dict()
        wrongLines = list()
        matches = LigaProPreparator.getMatches(corrections, wrongLines)
        logger.print(len(matches))

        LigaProPreparator.makePlayer2Id(logger, matches)
        player2id, id2player = readPlayer2Id('data/liga_pro/player2id.txt')

        idLinks = dict()
        idLinks['2'] = 'm249'
        idLinks['3'] = 'm434'
        idLinks['10'] = 'm260'
        idLinks['13'] = 'm256'
        idLinks['17'] = 'w9'
        idLinks['27'] = 'm2730'
        idLinks['31'] = 'm326'
        idLinks['30'] = 'm248'
        idLinks['32'] = 'm5'
        idLinks['42'] = 'm2728'
        idLinks['49'] = 'w144'
        idLinks['55'] = 'm267'
        idLinks['58'] = 'm421'
        idLinks['61'] = 'm337'
        idLinks['64'] = 'm2706'
        idLinks['79'] = 'm552'
        idLinks['89'] = 'm2732'
        idLinks['90'] = 'm269'
        idLinks['102'] = 'm577'
        idLinks['119'] = 'm3655'
        idLinks['126'] = 'w241'
        idLinks['128'] = 'w179'
        idLinks['131'] = 'm311'
        idLinks['132'] = 'm501'
        idLinks['138'] = 'm279'
        idLinks['142'] = 'm22'
        idLinks['143'] = 'm3344'
        idLinks['147'] = 'w191'
        idLinks['148'] = 'w185'
        idLinks['156'] = 'm11608'
        idLinks['185'] = 'm280'
        idLinks['186'] = 'm322'
        idLinks['187'] = 'm16248'
        idLinks['189'] = 'm16245'
        idLinks['192'] = 'm16244'
        idLinks['194'] = 'm16400'
        idLinks['200'] = 'm537'
        idLinks['210'] = 'm16397'
        idLinks['220'] = 'm9198'
        idLinks['221'] = 'm44'
        idLinks['238'] = 'm604'
        idLinks['249'] = 'm2781'
        idLinks['273'] = 'm6638'
        idLinks['286'] = 'm292'
        idLinks['301'] = 'm9894'
        idLinks['304'] = 'm16758'
        idLinks['309'] = 'm619'
        idLinks['310'] = 'm2739'
        idLinks['357'] = 'm391'
        idLinks['360'] = 'm2853'
        idLinks['396'] = 'm16251'
        idLinks['406'] = 'm278'
        idLinks['495'] = 'm16244'
        idLinks['500'] = 'm17093'
        idLinks['544'] = 'm6638'
        idLinks['652'] = 'm521'
        idLinks['665'] = 'w11'

        #enrich and check idLinks
        for player, playerId in sorted(player2id.items(), key=lambda x: x[0]):
            idLinked = list(set([idLinks.get(playerId[i]) for i in range(len(playerId)) if playerId[i] in idLinks]))
            if len(idLinked) == 1:
                for i in range(len(playerId)):
                    if playerId[i] not in idLinks:
                        idLinks[playerId[i]] = idLinked[0]
                        logger.print('enrich links', player, playerId, idLinked[0])
            elif len(idLinked) > 1:
                print('bad links', player, playerId, idLinked)
                logger.print('bad links', player, playerId, idLinked)
                raise

        playersDict = GlobalPlayersDict("filtered")

        for k, v in idLinks.items():
            if v not in playersDict.id2names:
                logger.print('bad links', k, v)
                raise

        with open('prepared_data/liga_pro/players_liga_pro.txt', 'w', encoding='utf-8') as fout:
            for player, playerId in sorted(player2id.items(), key=lambda x: x[0]):
                if playerId[-1] in idLinks:
                    idLinked = idLinks[playerId[-1]]
                    ids = playersDict.getId(player)
                    if idLinked not in ids:
                        logger.print('strange id in links', player, playerId, idLinked, ids)
                        raise
                    logger.print('solved player', player, playerId, idLinked, playersDict.getNames(idLinked))
                    fout.write('\t'.join([idLinked, player, 'http://tt-liga.pro/players/' + playerId[-1]]) + '\n')
                else:
                    ids = playersDict.getId(player)
                    if len(ids) == 1:
                        fout.write('\t'.join([ids[0], player, 'http://tt-liga.pro/players/' + playerId[-1]]) + '\n')
                    elif len(ids) > 1:
                        logger.print('multiple players', player, playerId, ids)
                    else:
                        logger.print('unknown player', player, playerId)

        rankings = LigaProPreparator.getRankings()
        with open('prepared_data/liga_pro/ranking_liga_pro.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(rankings):
                dt, player, ranking = e.split('\t')
                playerName, playerId = player.split(';')
                if playerId in idLinks:
                    id = [idLinks[playerId]]
                else:
                    id = playersDict.getId(playerName)
                if len(id) == 1:
                    fout.write(dt + '\t' + id[0] + '\t' + ranking + '\n')
                else:
                    logger.print('Ranking error ', playerName, playerId, id)

        matchesDict = dict()

        usedLinks = set()
        badPlayers = set()

        with open('prepared_data/liga_pro/all_results.txt', 'w', encoding='utf-8') as fout:
            fout.write('date\ttime\tcompName\tid1\tid2\t')
            fout.write('setsScore\tpointsScore\tname1\tname2\tround\n')
            for match in sorted(matches, key=lambda x: x.date + ' ' + x.time):
                if match.flError == 0:
                    flError = 0
                    ids = [[], []]
                    for i in range(2):
                        for player in match.names[i]:
                            playerName, playerId = player.split(';')
                            if playerId in idLinks:
                                id = [idLinks[playerId]]
                                usedLinks.add(playerId)
                            else:
                                id = playersDict.getId(playerName)
                            if len(id) == 1:
                                ids[i].append(id[0])
                            else:
                                logger.print(playerName, playerId, id)
                                if match.compName.find('Кубок баттерфляя') == -1:
                                    badPlayers.add('\t'.join([str(e) for e in [playerName, playerId, id]]))
                                flError = 1
                    if flError == 0 and len(ids[0]) > 0 and len(ids[1]) > 0:
                        if match.hash in matchesDict and match.round in [e.round for e in matchesDict[match.hash]]:
                            for m in matchesDict[match.hash]:
                                logger.print('HASHES', m.toArr(round=True))
                            logger.print('HASHES', match.toArr(round=True))
                        else:
                            if match.hash not in matchesDict:
                                matchesDict[match.hash] = []
                            matchesDict[match.hash].append(match)

                            resTokens = match.toArr(round=True)
                            resTokens.append(resTokens[3].split(';')[0])
                            resTokens.append(resTokens[4].split(';')[0])
                            resTokens[3] = ';'.join(ids[0])
                            resTokens[4] = ';'.join(ids[1])
                            fout.write('\t'.join(resTokens) + '\n')
                    else:
                        if match.compName.find('Кубок баттерфляя') == -1:
                            logger.print('flError ' + match.toStr())
                else:
                    logger.print('match.flError ' + match.toStr())

        for e in badPlayers:
            logger.print('bad players', e)

        for k, v in idLinks.items():
            if k not in usedLinks:
                logger.print(k, v)

    @staticmethod
    def correctDate(matchDate, round):
        arr = round.split(' ')
        month2num = dict(zip(['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'], range(12)))
        if len(arr) >= 2:
            if arr[0].isdigit() and arr[1] in month2num:
                print(round, matchDate)
                matchDate = matchDate[:4] + '-' + str(month2num[arr[1]] + 1).zfill(2) + '-' + arr[0].zfill(2)
                print(matchDate)

        return matchDate

    @staticmethod
    def getMatches(corrections, wrongLines):
        pattern = re.compile('|'.join(corrections.keys()))
        matches = []
        for f in walk('data/liga_pro/results'):
            for ff in sorted(f[2]):
                with open('data/liga_pro/results/' + ff, 'r', encoding='utf-8') as fin:
                    for line in fin:
    #                    line = corrections.get(line, line)
    #                    line = pattern.sub(lambda x: corrections[x.group()], line)
                        tokens = line.split('\t')
                        tokens = [e.strip() for e in tokens]
                        #if not (tokens[5] in ['0:3', '1:3', '2:3', '3:2', '3:1', '3:0']) or len(tokens[4]) == 0:
                        #    wrongLines.append(line)
                        #    continue
                        pointsScore = tokens[-1].strip().replace('(', '').replace(')', '').replace(' ', ';').replace('-', ':')
                        if tokens[0] == '2017-04-20' and tokens[1] == '20:00':
                            pointsScore = None
                        try:
                            names = [[tokens[5]], [tokens[8]]]
                        except:
                            print(ff)
                            print(line)
                            raise
                        time = tokens[1]
                        setsScore = tokens[-2].strip().replace(' ', '')
                        compName = 'Лига-Про (' + tokens[2].split(';')[0].replace('лига ', '') + '), ' + tokens[0]

                        round = tokens[4]
                        matchDate = LigaProPreparator.correctDate(tokens[0], round)

                        if compName == 'Лига-Про (500-550), 2017-06-02':
                            if names[0][0] == 'Гречаников С;234' and names[1][0] == 'Заргарян М;209':
                                pointsScore = '12:10;7:11;5:11;11:9;7:11'
                                time = '22:50'
                                print(tokens, setsScore, pointsScore)

                        if compName == 'Лига-Про (1150-1300), 2017-08-16':
                            if names[0][0] == 'Овчинников Е;254' and names[1][0] == 'Перов П;474':
                                setsScore = '1:3'
                                pointsScore = '11:7;9:11;6:11;3:11'
                                print(tokens, setsScore, pointsScore)
                            if names[0][0] == 'Зоненко В;518' and names[1][0] == 'Медведев С;256':
                                setsScore = '3:2'
                                pointsScore = '11:6;12:10;1:11;8:11;11:7'
                                print(tokens, setsScore, pointsScore)
                            if names[0][0] == 'Алчимбаев Р;486' and names[1][0] == 'Перов П;474':
                                setsScore = '1:3'
                                pointsScore = '11:8;17:19;9:11;7:11'
                                print(tokens, setsScore, pointsScore)
                            if names[0][0] == 'Медведев С;256' and names[1][0] == 'Овчинников Е;254':
                                setsScore = '0:3'
                                pointsScore = '11:13;7:11;5:11'
                                print(tokens, setsScore, pointsScore)
                            if names[0][0] == 'Перов П;474' and names[1][0] == 'Зоненко В;518':
                                setsScore = '2:3'
                                pointsScore = '11:5;6:11;7:11;11:5;12:14'
                                print(tokens, setsScore, pointsScore)
                            if names[0][0] == 'Медведев С;256' and names[1][0] == 'Алчимбаев Р;486':
                                setsScore = '2:3'
                                pointsScore = '3:11;11:8;3:11;11:4;7:11'
                                print(tokens, setsScore, pointsScore)
                            if names[0][0] == 'Зоненко В;518' and names[1][0] == 'Овчинников Е;254':
                                setsScore = '1:3'
                                pointsScore = '4:11;11:9;7:11;13:15'
                                print(tokens, setsScore, pointsScore)

                        match = Match(matchDate,
                                      names,
                                      names=names,
                                      setsScore=setsScore,
                                      pointsScore=pointsScore,
                                      time=time,
                                      compName=compName,
                                      round=round)
                        matches.append(match)
        return matches

    @staticmethod
    def getRankings():
        rankings = set()
        for f in walk('data/liga_pro/results'):
            for ff in sorted(f[2]):
                rnew = dict()
                dt = None
                with open('data/liga_pro/results/' + ff, 'r', encoding='utf-8') as fin:
                    for line in fin:
                        tokens = line.split('\t')
                        tokens = [e.strip() for e in tokens]
                        pointsScore = tokens[-1].strip().replace('(', '').replace(')', '').replace(' ', ';').replace('-', ':')
                        if tokens[0] == '2017-04-20' and tokens[1] == '20:00':
                            pointsScore = None
                        names = [[tokens[5]], [tokens[8]]]
                        round = tokens[4]
                        matchDate = LigaProPreparator.correctDate(tokens[0], round)
                        match = Match(matchDate,
                                names,
                                names=names,
                                setsScore=tokens[-2].strip().replace(' ', ''),
                                pointsScore=pointsScore,
                                time=tokens[1],
                                compName='Лига-Про, ' + tokens[2].split(';')[0],
                                round=round)
                        id1 = tokens[5]
                        id2 = tokens[8]
                        r1 = tokens[6]
                        dr1 = float(tokens[7].replace('+', '').zfill(1))
                        r2 = tokens[9]
                        dr2 = float(tokens[10].replace('+', '').zfill(1))

                        if match.flError == 0:
                            if tokens[4] == 'Финал':
                                if match.wins[0]:
                                    dr1 += 0.8
                                    dr2 += 0.6
                                else:
                                    dr2 += 0.8
                                    dr1 += 0.6
                            if tokens[4] == 'за 3-е место':
                                if match.wins[0]:
                                    dr1 += 0.4
                                else:
                                    dr2 += 0.4
                        rankings.add('\t'.join([tokens[0], id1, r1]))
                        rankings.add('\t'.join([tokens[0], id2, r2]))
                        dt = tokens[0]
                        if not (id1 in rnew):
                            rnew[id1] = float(r1)
                        rnew[id1] += dr1
                        if not (id2 in rnew):
                            rnew[id2] = float(r2)
                        rnew[id2] += dr2
                for id, r in rnew.items():
                    rankings.add('\t'.join([(datetime.datetime.strptime(dt, "%Y-%m-%d").date() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"), id, format(r, '.1f')]))

        return rankings

    @staticmethod
    def makePlayer2Id(logger, matches):
        player2id = dict()
        for match in matches:
            for i in range(2):
                playerName, playerId = match.names[i][0].split(';')
                if not (playerName in player2id):
                    player2id[playerName] = []
                if not (playerId in player2id[playerName]):
                    player2id[playerName].append(playerId)
                    #if len(player2id[playerName]) > 1:
                    #    logger.print('MULTIPLE PLAYERS ' + playerName + ' ' + ';'.join(player2id[playerName]))
        with open('data/liga_pro/player2id.txt', 'w', encoding='utf-8') as fout:
            for k, v in sorted(player2id.items(), key=lambda x: x[0]):
                fout.write(k + '\t' + ';'.join(v) + '\n')


def main():
    LigaProPreparator.run(logger=Logger('LigaProPreparator.txt'))


if __name__ == "__main__":
    main()