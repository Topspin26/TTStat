from common import *
import os
import filterPlayersByRusRanking

def readPlayersRankings(dirname):
    playersRankings = dict()
    for f in os.listdir(dirname):
        with open(dirname + '/' + f, 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                tokens = [e.strip() for e in tokens]
                playersRankings[f.split('_')[-1][:-4] + '\t' + f[:7] + '\t' + tokens[0]] = tokens[1:]
    return playersRankings

def updateGlobalPlayersDict(newId2names):
    playersDict = GlobalPlayersDict()

    maxV = {'men': playersDict.getMaxId('m') + 1,
            'women': playersDict.getMaxId('w') + 1,}

    for mw in ['men', 'women']:
            for k, v in newId2names[mw].items():
                name = None
                id = None
                for e in v:
                    id = playersDict.getId(e, 0)
                    if not (id is None):
                        name = e
                        break
                if (name is None):
                    print(v, playersDict.getId(e, 0))
                    playersDict.setId2Names(mw[0] + str(maxV[mw]), v)
                    maxV[mw] += 1
                else:
                    #print(v)
                    for e in v:
                        playersDict.updateId2names(id, e)

    for mw in ['m', 'w']:
        with open(playersDict.filenames[mw], 'w', encoding='utf-8') as fout:
            for k, v in sorted(playersDict.id2names.items(), key=lambda x: int(x[0][1:])):
                if k[0] == mw:
                    fout.write(k + '\t' + ';'.join(v) + '\n')

def main():

    rusId2names = {}
    rusName2Id = {}
    ittfId2names = {}
    ittfName2Id = {}
    for mw in ['men', 'women']:
        ittfId2names[mw] = dict()
        with open('data/propingpong/propingpong_ittfId2names_' + mw + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                line = line.replace('&nbsp;', ' ')
                tokens = line.split('\t')
                playerId = tokens[0]
                playerName = tokens[1].strip()
                ittfId2names[mw][playerId] = playerName.split(';')
                for playerName in ittfId2names[mw][playerId]:
                    if not (playerName in ittfName2Id):
                        ittfName2Id[playerName] = []
                    if not (playerId in ittfName2Id[playerName]):
                        ittfName2Id[playerName].append(playerId)
        rusId2names[mw] = dict()
        with open('data/propingpong/propingpong_rusId2names_' + mw + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                line = line.replace('&nbsp;', ' ')
                tokens = line.split('\t')
                playerId = tokens[0]
                playerName = tokens[1].strip()
                rusId2names[mw][playerId] = playerName.split(';')
                for playerName in rusId2names[mw][playerId]:
                    if not (playerName in rusName2Id):
                        rusName2Id[playerName] = []
                    if not (playerId in rusName2Id[playerName]):
                        rusName2Id[playerName].append(playerId)

    updateGlobalPlayersDict(rusId2names)
    updateGlobalPlayersDict(ittfId2names)

    playersDict = GlobalPlayersDict()

    idLinks = {'rus': dict(), 'ittf': dict()}

    idLinks['rus']['121'] = 'm249' # Анисимов Антон
    idLinks['rus']['1820'] = 'm323' # Коротков Александр
    idLinks['rus']['599'] = 'm256' # Виноградов Алексей
    idLinks['rus']['14286'] = 'm502' # Соколов Юрий
    idLinks['rus']['3857'] = 'm577' # Федоров Дмитрий
    idLinks['rus']['3808'] = 'm251' # Уланов Алексей
    idLinks['rus']['2262'] = 'm267' # Уланов Алексей
    idLinks['rus']['1630'] = 'm2803' # Кирсанов Сергей
    idLinks['rus']['1576'] = 'm38' # Карпов Андрей
    idLinks['rus']['177'] = None # Архипов Иван
    idLinks['rus']['17185'] = None # Морозов Александр
    idLinks['rus']['9703'] = None # Игорь Егоров
    idLinks['rus']['14596'] = None # Иванов Виктор
    idLinks['rus']['3853'] = 'm2781' # Федоров Владислав
    idLinks['rus']['1413'] = 'm284' # Иванов Михаил
    idLinks['rus']['1412'] = None # Иванов Михаил
    idLinks['rus']['15288'] = 'm2853'# Савельев Алексей
    idLinks['rus']['3211'] = None # Савельев Алексей, по идее надо объединить с предыдущим
    idLinks['rus']['8288'] = None # Савельев Алексей
    idLinks['rus']['20152'] = None # Воробьев Сергей

    idLinks['rus']['1477'] = 'm231' # Исмаилов Саади
    idLinks['rus']['20166'] = 'm231' # Исмаилов Саъди
    idLinks['rus']['19370'] = 'm231' # Исмаилов Саъди

    idLinks['rus']['13855'] = None # Попов Дмитрий
    idLinks['rus']['7516'] = None # Попов Дмитрий
    idLinks['rus']['2990'] = 'm279' # Попов Дмитрий

    idLinks['rus']['4959'] = None # Гусева Екатерина
    idLinks['rus']['8624'] = None # Гусева Екатерина
    idLinks['rus']['4958'] = 'w54' # Гусева Екатерина

    idLinks['rus']['14458'] = None # Степанов Иван
    idLinks['rus']['18224'] = None # Степанов Иван
    idLinks['rus']['3559'] = 'm292' # Степанов Иван

    idLinks['rus']['8901'] = None # Резниченко Александр
    idLinks['rus']['3097'] = 'm311' # Резниченко Александр

    idLinks['rus']['8747'] = None # Макаров Денис
    idLinks['rus']['19039'] = 'm16244' # Макаров Денис

    idLinks['rus']['10003'] = None # Мельников Алексей
    idLinks['rus']['17831'] = 'm9198' # Мельников Алексей

    idLinks['rus']['2775'] = None # Осипов Дмитрий
    idLinks['rus']['2773'] = None # Осипов Дмитрий
    idLinks['rus']['2774'] = None # Осипов Дмитрий

    idLinks['rus']['9414'] = None # Маслов Даниил
    idLinks['rus']['12153'] = None # Маслов Даниил
    idLinks['rus']['2359'] = None # Маслов Даниил
    idLinks['rus']['2358'] = 'm421' # Маслов Даниил

    idLinks['rus']['6713'] = None # Фомина Анастасия
    idLinks['rus']['6712'] = 'w185' # Фомина Анастасия

    idLinks['rus']['7340'] = None # Овчаров Дмитрий
    idLinks['rus']['2722'] = 'm226' # Овчаров Дмитрий

    idLinks['rus']['4888'] = None # Голубева Анастасия
    idLinks['rus']['4886'] = None # Голубева Анастасия (1992, нужно объединить со след)
    idLinks['rus']['15645'] = 'w9' # Голубева Анастасия
    idLinks['rus']['4887'] = 'w11133' # Голубева Анастасия

    idLinks['rus']['8893'] = None # Мошков Никита
    idLinks['rus']['8239'] = 'm306' # Мошков Никита

    idLinks['rus']['14596'] = None # Иванов Виктор

    idLinks['rus']['14669'] = None # Крылов Александр
    idLinks['rus']['18872'] = None # Крылов Александр

    idLinks['rus']['11187'] = None # Попов Олег
    idLinks['rus']['20143'] = None # Попов Олег

    idLinks['rus']['18136'] = None # Макаров Сергей
    idLinks['rus']['2274'] = None # Макаров Сергей
    idLinks['rus']['10285'] = 'm2856' # Макаров Сергей

    idLinks['rus']['19283'] = None # Винокуров Александр
    idLinks['rus']['605'] = 'm261' # Винокуров Александр

    idLinks['rus']['5121'] = None # Анастасия Ефимова

    idLinks['rus']['5016'] = None # Дмитриева Анна
    idLinks['rus']['12761'] = None # Дмитриева Анна
    idLinks['rus']['5015'] = 'w209' # Дмитриева Анна


    prefix = 'prepared_data/propingpong/'
    for rt in ['rus', 'ittf']:
        collisions = dict()
        multiple = dict()
        unknown = dict()
        badIds = dict()

        rankings = readPlayersRankings('data/propingpong/ranking_' + rt)
        with open('prepared_data/propingpong/ranking_' + rt + '.txt', 'w', encoding='utf-8') as fout:
            for k, v in sorted(rankings.items(), key=lambda x: x[0]):
                arr = k.split('\t')
                mw = arr[0]
                dt = arr[1]
                playerId = arr[2]
                try:
                    if rt == 'rus':
                        playerName = rusId2names[mw][playerId][0]
                    else:
                        playerName = ittfId2names[mw][playerId][0]
                except:
                    updateDict(badIds, playerId)
                    print(k, v)
                    raise
                    continue
                if rt == 'rus':
                    id = rusName2Id[playerName]
                else:
                    id = ittfName2Id[playerName]
                if playerName == 'Исмаилов Саади' or playerName == 'Саъди Исмаилов':
                    print(dt, playerName, id, playerId, v)
                if playerName == 'Старостин Александр' or playerName == 'Александр Старостин':
                    print(dt, playerName, id, playerId, v)

                id = [e for e in id if idLinks[rt].get(e, 1) is not None]
                if len(id) == 1 or playerId in idLinks[rt] or (len(id) == 2 and len(id[0]) != len(id[1])):
                    if playerId in idLinks[rt] and idLinks[rt][playerId] is None:
                        continue
                    if playerId in idLinks[rt]:
                        id = [idLinks[rt][playerId]]
                    else:
                        id = playersDict.getId(playerName)
                    #if playerName == 'Станислав Медведев' or playerName == 'Гусев Андрей':
                    #    print(playerName, id, playerId)
                    if len(id) == 1:
                        fout.write('\t'.join([dt, id[0]] + v) + '\n')
                    elif len(id) == 0:
                        updateDict(unknown, playerName)
                    else:
                        updateDict(multiple, playerName)
                else:
                    updateDict(collisions, playerName)

        with open(prefix + rt + '_players_multiple.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(multiple.items(), key=lambda x: -x[1]):
                fout.write(e[0] + '\t' + str(e[1]) + '\n')
        with open(prefix + rt + '_players_unknown.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(unknown.items(), key=lambda x: -x[1]):
                fout.write(e[0] + '\t' + str(e[1]) + '\n')
        with open(prefix + rt + '_players_collisions.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(collisions.items(), key=lambda x: -x[1]):
                fout.write(e[0] + '\t' + str(e[1]) + '\n')
        with open(prefix + rt + '_players_bad.txt', 'w', encoding='utf-8') as fout:
            for e in sorted(badIds.items(), key=lambda x: -x[1]):
                fout.write(e[0] + '\t' + str(e[1]) + '\n')

    playersDict = GlobalPlayersDict('filtered')


if __name__ == "__main__":
    main()