from os import walk
import datetime as datetime
import re
from Entity import *


class LigaProPreparator:

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
                        names = [[tokens[5]], [tokens[8]]]
                        matches.append(Match(tokens[0],
                                             names,
                                             names=names,
                                             setsScore=tokens[-2].strip().replace(' ', ''),
                                             pointsScore=pointsScore,
                                             time=tokens[1],
                                             compName='Лига-Про (' + tokens[2].split(';')[0].replace('лига ', '') + '), ' + tokens[0],
                                             round=tokens[4]))
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
                        match = Match(tokens[0],
                                names,
                                names=names,
                                setsScore=tokens[-2].strip().replace(' ', ''),
                                pointsScore=pointsScore,
                                time=tokens[1],
                                compName='Лига-Про, ' + tokens[2].split(';')[0],
                                round=tokens[4])
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
    def makePlayer2Id():
        corrections = dict()
        wrongLines = list()
        matches = LigaProPreparator.getMatches(corrections, wrongLines)
        player2id = dict()
        for match in matches:
            for i in range(2):
                playerName, playerId = match.names[i][0].split(';')
                if not (playerName in playerId):
                    player2id[playerName] = []
                if not (playerId in player2id[playerName]):
                    player2id[playerName].append(playerId)
                    if len(player2id[playerName]) > 1:
                        print('MULTIPLE PLAYERS ' + playerName + ';'.join(player2id[playerName]))
        with open('data/liga_pro/player2id.txt', 'w', encoding='utf-8') as fout:
            for k,v in sorted(player2id.items(), key=lambda x: x[0]):
                fout.write(k + '\t' + ';'.join(v) + '\n')

    @staticmethod
    def run():
        LigaProPreparator.makePlayer2Id()
        player2id, id2player = readPlayer2Id('data/liga_pro/player2id.txt')

        idLinks = dict()
        idLinks['30'] = 'm248'
        idLinks['58'] = 'm421'
        idLinks['10'] = 'm260'
        idLinks['2'] = 'm249'
        idLinks['132'] = 'm501'
        idLinks['3'] = 'm434'
        idLinks['128'] = 'w179'
        idLinks['143'] = 'm3344'
        idLinks['13'] = 'm256'
        idLinks['186'] = 'm322'
        idLinks['17'] = 'w9'
        idLinks['27'] = 'm2730'
        idLinks['31'] = 'm326'
        idLinks['142'] = 'm22'
        idLinks['32'] = 'm5'
        idLinks['185'] = 'm280'
        idLinks['42'] = 'm2728'
        idLinks['119'] = 'm3655'
        idLinks['147'] = 'w191'
        idLinks['49'] = 'w144'
        idLinks['55'] = 'm267'
        idLinks['192'] = 'm16244'
        idLinks['61'] = 'm337'
        idLinks['64'] = 'm2706'
        idLinks['126'] = 'w241'
        idLinks['189'] = 'm16245'
        idLinks['79'] = 'm552'
        idLinks['138'] = 'm279'
        idLinks['131'] = 'm311'
        idLinks['89'] = 'm2732'
        idLinks['90'] = 'm269'
        idLinks['156'] = 'm11608'
        idLinks['102'] = 'm577'
        idLinks['148'] = 'w185'
        idLinks['200'] = 'm537'
        idLinks['187'] = 'm16248'
        idLinks['221'] = 'm44'
        idLinks['396'] = 'm16251'
        idLinks['220'] = 'm9198'
        idLinks['210'] = 'm16397'
        idLinks['286'] = 'm292'
        idLinks['249'] = 'm2781'
        idLinks['194'] = 'm16400'
        idLinks['273'] = 'm6638'
        idLinks['304'] = 'm16758'
        idLinks['238'] = 'm604'
        idLinks['309'] = 'm619'
        idLinks['310'] = 'm2739'
        idLinks['301'] = 'm9894'
        idLinks['406'] = 'm278'
        idLinks['360'] = 'm2853'
        # idLinks['301'] = 'm9894'

        playersDict = GlobalPlayersDict("filtered")

        if len(set(idLinks.values())) != len(idLinks):
            print('bad links')
            raise

        for k, v in idLinks.items():
            if not v in playersDict.id2names:
                print(k, v)
                raise

        with open('prepared_data/liga_pro/players_liga_pro.txt', 'w', encoding='utf-8') as fout:
            for player, playerId in sorted(player2id.items(), key=lambda x: x[0]):
                if len(playerId) > 1:
                    print(player, playerId)
                    raise
                ids = playersDict.getId(player)
                if len(ids) == 1:
                    fout.write('\t'.join([ids[0], player, 'http://tt-liga.pro/players/' + playerId[0]]) + '\n')
                elif len(ids) == 0:
                    idLinked = idLinks.get(playerId[0])
                    if idLinked in playersDict.id2names:
                        print('solved unknown player', player, playerId, idLinked, playersDict.getNames(idLinked))
                        fout.write('\t'.join([idLinked, player, 'http://tt-liga.pro/players/' + playerId[0]]) + '\n')
                    else:
                        print('unknown player', player, playerId, idLinked)
                elif len(ids) > 1:
                    idLinked = idLinks.get(playerId[0])
                    if idLinked in playersDict.id2names:
                        if not (idLinked in ids):
                            print('strange id')
                            raise
                        print('solved multiple players', player, playerId, idLinked, playersDict.getNames(idLinked))
                        fout.write('\t'.join([idLinked, player, 'http://tt-liga.pro/players/' + playerId[0]]) + '\n')
                    else:
                        print('multiple players', player, playerId, ids, idLinked)

        corrections = dict()
        wrongLines = list()
        matches = LigaProPreparator.getMatches(corrections, wrongLines)
        print(len(matches))

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
                    print('Ranking error ', playerName, playerId, id)

                    #    multiple = dict()
                    #    solved = dict()
                    #    unknown = dict()

        matchesDict = dict()

        usedLinks = set()
        badPlayers = set()

        with open('prepared_data/liga_pro/all_results.txt', 'w', encoding='utf-8') as fout:
            fout.write('date\ttime\tcompName\tid1\tid2\t')
            fout.write('setsScore\tpointsScore\tname1\tname2\n')
            for match in matches:
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
                                print(playerName, playerId, id)
                                if match.compName.find('Кубок баттерфляя') == -1:
                                    badPlayers.add('\t'.join([str(e) for e in [playerName, playerId, id]]))
                                flError = 1
                    if flError == 0 and len(ids[0]) > 0 and len(ids[1]) > 0:
                        if match.hash in matchesDict:
                            print('HASHES', matchesDict[match.hash], match.toArr(), match.round)
                        else:
                            resTokens = match.toArr()
                            matchesDict[match.hash] = resTokens
                            resTokens.append(resTokens[3].split(';')[0])
                            resTokens.append(resTokens[4].split(';')[0])
                            resTokens[3] = ';'.join(ids[0])
                            resTokens[4] = ';'.join(ids[1])
                            fout.write('\t'.join(resTokens) + '\n')
                    else:
                        if match.compName.find('Кубок баттерфляя') == -1:
                            print('flError ' + match.toStr())
                else:
                    print('match.flError ' + match.toStr())

        for e in badPlayers:
            print(e)

        for k, v in idLinks.items():
            if k not in usedLinks:
                print(k, v)


def main():
    LigaProPreparator.run()


if __name__ == "__main__":
    main()