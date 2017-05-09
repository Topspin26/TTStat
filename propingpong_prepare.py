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

    filterPlayersByRusRanking.main()
    playersDict = GlobalPlayersDict("filtered")

    idLinks = {'rus':{}, 'ittf':{}}
    idLinks['rus']['121'] = 'm249'
    idLinks['rus']['1820'] = 'm323'
    idLinks['rus']['599'] = 'm256'
    idLinks['rus']['14286'] = 'm502'
    idLinks['rus']['3857'] = 'm577'
    idLinks['rus']['3808'] = 'm251'
    idLinks['rus']['2262'] = 'm267'
    idLinks['rus'][''] = 'm421'
    idLinks['rus'][''] = 'm279'
    idLinks['rus'][''] = 'w185'
    idLinks['rus']['1630'] = 'm2803'
    idLinks['rus']['1576'] = 'm38'
    idLinks['rus']['177'] = None #Архипов Иван
    idLinks['rus']['17185'] = None #Морозов Александр
    idLinks['rus']['9703'] = None #Игорь Егоров
    idLinks['rus']['14596'] = None #Иванов Виктор
    idLinks['rus']['3853'] = 'm2781'#Федоров Владислав
    idLinks['rus']['1413'] = 'm284'#Иванов Михаил
    idLinks['rus']['1412'] = None#Иванов Михаил

    prefix = 'prepared_data/propingpong/'
    for rt in ['rus', 'ittf']:
        collisions = dict()
        multiple = dict()
        unknown = dict()
        badIds = dict()

        rankings = readPlayersRankings('data/propingpong/ranking_' + rt)
        with open('prepared_data/propingpong/ranking_' + rt + '.txt', 'w', encoding = 'utf-8') as fout:
            for k,v in sorted(rankings.items(), key = lambda x: x[0]):
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
                if len(id) == 1 or playerId in idLinks[rt] or (len(id) == 2 and len(id[0]) != len(id[1])):
                    if playerId in idLinks[rt] and idLinks[rt][playerId] is None:
                        continue
                    if playerId in idLinks[rt]:
                        id = [idLinks[rt][playerId]]
                    else:
                        id = playersDict.getId(playerName)
#                    if playerName == 'Морозов Александр' or playerName == 'Александр Морозов':
#                        print(playerName, id, playerId)
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

if __name__ == "__main__":
    main()