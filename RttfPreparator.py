import os
from os import walk
import datetime
from Entity import *


class RttfPreparator:
    @staticmethod
    def run():
        matches, player2id, id2player = RttfPreparator.getMatches()
        playersDict = GlobalPlayersDict("filtered")

        idLinks = dict()

        # Макаров Денис
        idLinks['3710'] = 'm16244'

        # Степанов Иван
        idLinks['162'] = None

        # Шибаев Александр
        idLinks['6708'] = None

        # Карпов Андрей
        idLinks['6209'] = None

        # Сафиулин Марсель
        idLinks['210'] = 'm16233'
        idLinks['8482'] = None

        # Воробьев Сергей
        idLinks['3879'] = 'm16248'
        idLinks['3581'] = None

        # Овчинников Егор
        idLinks['4551'] = None

        # Осипов Дмитрий
        idLinks['4172'] = None
        idLinks['635'] = 'm16251'

        # Свиридов Алексей
        idLinks['5018'] = None
        idLinks['1340'] = 'm2732'

        # Коротков Александр
        idLinks['8429'] = None
        idLinks['8421'] = 'm323'

        # Пищук Дмитрий
        idLinks['1656'] = None
        idLinks['10072'] = None
        idLinks['8794'] = 'm554'

        # Попов Дмитрий
        idLinks['9674'] = None
        idLinks['139'] = 'm279'

        # Попов Олег
        idLinks['8155'] = None
        idLinks['3932'] = None
        idLinks['2671'] = 'm16397'

        # Егоров Николай
        idLinks['9376'] = None
        idLinks['7115'] = None
        idLinks['59'] = 'm2730'

        # Пульный Павел
        idLinks['673'] = None
        idLinks['282'] = 'm157'

        # Донич Александр
        idLinks['8380'] = None
        idLinks['3053'] = 'm393'

        # Федоров Дмитрий
        idLinks['5703'] = None
        idLinks['2611'] = 'm577'

        # Голубева Екатерина
        idLinks['6314'] = None

        # Малахов Павел
        idLinks['6618'] = None
        idLinks['1137'] = None
        idLinks['3179'] = 'm397'

        # Маслов Даниил
        idLinks['3613'] = None
        idLinks['4331'] = 'm421'

        with open('prepared_data/rttf/players_rttf.txt', 'w', encoding='utf-8') as fout:
            for player, playerId in sorted(player2id.items(), key=lambda x: x[0]):
                playerId = [e for e in playerId if idLinks.get(e, 1) is not None]
                if len(playerId) > 1:
                    print('multiple rttf players', player, playerId)
                    continue
                if len(playerId) == 0:
                    print('ignore rttf player', player, playerId)
                    continue
                ids = playersDict.getId(player)
                if len(ids) == 1:
                    fout.write('\t'.join([ids[0], player, 'http://or.rttf.ru/players/' + playerId[0]]) + '\n')
                elif len(ids) == 0:
                    idLinked = idLinks.get(playerId[0])
                    if idLinked in playersDict.id2names:
                        print('solved unknown player', player, playerId, idLinked, playersDict.getNames(idLinked))
                        fout.write('\t'.join([idLinked, player, 'http://or.rttf.ru/players/' + playerId[0]]) + '\n')
                    else:
                        print('unknown player', player, playerId, idLinked)
                elif len(ids) > 1:
                    idLinked = idLinks.get(playerId[0])
                    if idLinked in playersDict.id2names:
                        if not (idLinked in ids):
                            print('strange id')
                            raise
                        print('solved multiple players', player, playerId, idLinked, playersDict.getNames(idLinked))
                        fout.write('\t'.join([idLinked, player, 'http://or.rttf.ru/players/' + playerId[0]]) + '\n')
                    else:
                        print('multiple players', player, playerId, ids, idLinked)

        rankings = RttfPreparator.getRankings()
        with open('prepared_data/rttf/ranking_rttf.txt', 'w', encoding='utf-8') as fout:
            for e, ranking in sorted(rankings.items()):
                dt, player = e.split('\t')
                playerName, playerId = player.split(';')
                if playerId in idLinks:
                    id = [idLinks[playerId]]
                else:
                    id = playersDict.getId(playerName)
                if len(id) == 1 and id[0] is not None:
                    fout.write(dt + '\t' + id[0] + '\t' + ranking + '\n')
                else:
                    print('Ranking error ', playerName, playerId, id)

        multiple = dict()
        unknown = dict()

        prefix = 'prepared_data/rttf/'
        with open(prefix + 'all_results.txt', 'w', encoding='utf-8') as fout:
            fout.write(
                '\t'.join(
                    ['date', 'time', 'compName', 'id1', 'id2', 'setsScore', 'pointsScore', 'name1', 'name2']) + '\n')

            for match in matches:
                if match.flError == 0:
                    flError = 0
                    ids = [[], []]
                    players = [[], []]
                    for i in range(2):
                        for player in match.ids[i]:
                            playerName = id2player[player]
                            playerId = player2id[playerName]
                            playerId = [e for e in playerId if idLinks.get(e, 1) is not None]
                            if (len(playerId) == 1 or player in idLinks) and not (idLinks.get(player, '') is None):
                                players[i].append(playerName)
                                if player in idLinks:
                                    playerId = [idLinks[player]]
                                    # print(player, playerName, id)
                                else:
                                    playerId = playersDict.getId(playerName)
                                if len(playerId) == 1:
                                    ids[i].append(playerId[0])
                                elif len(playerId) == 0:
                                    flError = 1
                                    updateDict(unknown, playerName)
                                else:
                                    flError = 1
                                    fl_mw = ''
                                    for e in playerId:
                                        fl_mw += e[0]
                                    fl_mw = ''.join(sorted(set(list(fl_mw))))
                                    updateDict(multiple, fl_mw + ' ' + playerName)
                            else:
                                updateDict(multiple, playerName)

                    if flError == 0 and len(ids[0]) > 0 and len(ids[1]) > 0:
                        resTokens = match.toArr()
                        resTokens.append(';'.join(players[0]))
                        resTokens.append(';'.join(players[1]))
                        resTokens[3] = ';'.join(ids[0])
                        resTokens[4] = ';'.join(ids[1])
                        fout.write('\t'.join([str(e) for e in resTokens]) + '\n')

        with open(prefix + 'rttf_players_multiple.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(multiple.items(), key=lambda x: -x[1]):
                fout.write(e[0] + '\t' + str(e[1]) + '\n')
        with open(prefix + 'rttf_players_unknown.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(unknown.items(), key=lambda x: -x[1]):
                fout.write(e[0] + '\t' + str(e[1]) + '\n')

    @staticmethod
    def getRankings():
        rankings = dict()
        dirname = 'data/rttf/results_new'
        for f in walk(dirname):
            for ff in sorted(f[2]):
                fp = os.path.abspath(os.path.join(f[0], ff))
                if fp.find('_rankings.txt') == -1:
                    continue
                if fp.lower().find('artt-про') != -1 or fp.lower().find('ttleader-pro') != -1:
                    print(fp)
                    continue
                with open(fp, encoding='utf-8') as fin:
                    for line in fin:
                        tokens = line.rstrip('\n').split('\t')
                        dt = tokens[0]
                        id1 = tokens[2]
                        r1 = tokens[3]
                        dr1 = float(tokens[4].replace('+', '').zfill(1))
                        if '\t'.join([dt, id1]) not in rankings:
                            rankings['\t'.join([dt, id1])] = r1
                        rankings['\t'.join([(datetime.datetime.strptime(dt, "%Y-%m-%d").date() +
                                             datetime.timedelta(days=1)).strftime("%Y-%m-%d"), id1])] = \
                            format(float(r1) + dr1, '.1f')
        return rankings

    @staticmethod
    def getMatches():
        player2id = dict()
        id2player = dict()
        matches = []

        dirname = 'data/rttf/results_new'
        filenames = []
        for f in walk(dirname):
            for ff in f[2]:
                fp = os.path.abspath(os.path.join(f[0], ff))
                if fp.find('_rankings.txt') != -1:
                    continue
                if fp.lower().find('artt-про') != -1 or fp.lower().find('ttleader-pro') != -1:
                    print(fp)
                    continue
                with open(fp, encoding='utf-8') as fin:
                    for line in fin:
                        tokens = line.rstrip('\n').split('\t')
                        ids = [[], []]
                        names = [[], []]
                        for ii, i in enumerate([2, 3]):
                            arr = tokens[i].split(';')
                            for j in range(len(arr)):
                                if j % 2 == 0:
                                    name = arr[j]
                                    name = name.replace('o', 'о')
                                    name = name.replace('O', 'О')
                                    name = name.replace('p', 'р')
                                    name = name.replace('P', 'Р')
                                    name = name.replace('a', 'а')
                                    name = name.replace('A', 'А')
                                    id = arr[j + 1]
                                    if name == 'Заярная Наталья':
                                        name = 'Заярная Наталия'
                                    if name == 'Мамасабиров Ильяз':
                                        name = 'Мамасабиров Илиязбек'
                                    if name == 'Корякин Алексей' and id == '10281':
                                        name = 'Корякин Ярослав'
                                    if name == 'Соколов (МГУ)' and id == '8765':
                                        name = 'Соколов Никита'
                                    ids[ii].append(id)
                                    names[ii].append(name)
                                    if id in id2player and id2player[id] != name:
                                        print([id, id2player[id], name])
                                        print('error')
                                        #raise
                                    else:
                                        id2player[id] = name
                                    if not (name in player2id):
                                        player2id[name] = []
                                    if not (id in player2id[name]):
                                        player2id[name].append(id)

                        time = ''
                        ids = [[e.strip() for e in ids[0]], [e.strip() for e in ids[1]]]
                        names = [[e.strip() for e in names[0]], [e.strip() for e in names[1]]]
                        matches.append(Match(tokens[0],
                                             ids,
                                             names=names,
                                             setsScore=tokens[4].replace('-', ':'),
                                             time=time,
                                             compName=tokens[1]))
                filenames.append(fp)
    #        if len(filenames) == 100:
    #            break
        print(len(filenames))
        print(len(matches))

        with open('data/rttf/player2id.txt', 'w', encoding='utf-8') as fout:
            for name,ids in sorted(player2id.items(), key = lambda x: -len(x[1])):
                fout.write(name + '\t' + ';'.join(ids) + '\n')

        return matches, player2id, id2player


def main():
    RttfPreparator.run()

if __name__ == "__main__":
    main()