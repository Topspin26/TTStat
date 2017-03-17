from common import *
import os

def readPlayersRankings(dirname):
    playersRankings = dict()
    for f in os.listdir(dirname):
        with open(dirname + '/' + f, 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                tokens = [e.strip() for e in tokens]
                playersRankings[f[:7] + '\t' + tokens[0]] = tokens[1:]
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
    ittfId2names = {}
    for mw in ['men', 'women']:
        ittfId2names[mw] = dict()
        with open('data/propingpong/propingpong_ittfId2names_' + mw + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                line = line.replace('&nbsp;', ' ')
                tokens = line.split('\t')
                ittfId2names[mw][tokens[0]] = tokens[1].strip().split(';')
        rusId2names[mw] = dict()
        with open('data/propingpong/propingpong_rusId2names_' + mw + '.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                line = line.replace('&nbsp;', ' ')
                tokens = line.split('\t')
                rusId2names[mw][tokens[0]] = tokens[1].strip().split(';')

    updateGlobalPlayersDict(rusId2names)
    updateGlobalPlayersDict(ittfId2names)

#    playersDict = GlobalPlayersDict()

    '''
    rusRankings = readPlayersRankings('data/propingpong/ranking_rus')
    print(idRus2Name)
    id2G = dict()
    for k,v in idRus2Name['men'].items():
        for name in v:
            if name in mIdG:
                if not (k in id2G):
                    id2G[k] = [mIdG[name]]
                else:
                    if not (mIdG[name] in id2G[k]):
                        id2G[k].append(mIdG[name])
    for k,v in idRus2Name['women'].items():
        for name in v:
            if name in wIdG:
                if not (k in id2G):
                    id2G[k] = [wIdG[name]]
                else:
                    if not (wIdG[name] in id2G[k]):
                        id2G[k].append(wIdG[name])
    print(sorted(id2G.items(), key = lambda x: -len(x[1])))
    badIds = set()
    with open('prepared_data/propingpong/ranking_rus.txt', 'w', encoding = 'utf-8') as fout:
        for k,v in sorted(rusRankings.items(), key = lambda x: x[0]):
            arr = k.split('\t')
            if (arr[1] in id2G):
                fout.write('\t'.join([arr[0], id2G[arr[1]][0]] + v) + '\n')
            else:
                badIds.add(arr[1])
    print("badRusPlayers: " + str(badIds))

    ittfRankings = readPlayersRankings('data/propingpong/ranking_ittf')
    print(idIttf2Name)
    id2G = dict()
    for k, v in idIttf2Name['men'].items():
        for name in v:
            if name in mIdG:
                if not (k in id2G):
                    id2G[k] = [mIdG[name]]
                else:
                    if not (mIdG[name] in id2G[k]):
                        id2G[k].append(mIdG[name])
    for k, v in idIttf2Name['women'].items():
        for name in v:
            if name in wIdG:
                if not (k in id2G):
                    id2G[k] = [wIdG[name]]
                else:
                    if not (wIdG[name] in id2G[k]):
                        id2G[k].append(wIdG[name])
    print(sorted(id2G.items(), key=lambda x: -len(x[1])))
    badIds = set()
    with open('prepared_data/propingpong/ranking_ittf.txt', 'w', encoding='utf-8') as fout:
        for k, v in sorted(ittfRankings.items(), key=lambda x: x[0]):
            arr = k.split('\t')
            if (arr[1] in id2G):
                fout.write('\t'.join([arr[0], id2G[arr[1]][0]] + v) + '\n')
            else:
                badIds.add(arr[1])
    print("badIttfPlayers: " + str(badIds))
    '''

if __name__ == "__main__":
    main()