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

def main():

    filenameGlobalPlayersMen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_men.txt'
    (mIdG, mId2G) = readPlayersInv(filenameGlobalPlayersMen)
    filenameGlobalPlayersWomen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_women.txt'
    (wIdG, wId2G) = readPlayersInv(filenameGlobalPlayersWomen)

    mId = readPlayers(filenameGlobalPlayersMen, flAll = 1)
    wId = readPlayers(filenameGlobalPlayersWomen, flAll = 1)

    maxV = {'men': max([int(e[1:]) for e in mIdG.values()]) + 1,
            'women': max([int(e[1:]) for e in wIdG.values()]) + 1}
    print(maxV)
    newPlayers = {'men': dict(), 'women': dict()}
    id2Name = {'men': dict(), 'women': dict()}
    idRus2Name = {'men': dict(), 'women': dict()}
    idIttf2Name = {'men': dict(), 'women': dict()}
    for mw in ['men', 'women']:
        with open('data/propingpong/propingpong_players_' + mw + '.txt', encoding = 'utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                tokens[2] = tokens[2].strip()
                key = tokens[1] + '\t' + tokens[2]
                if key in id2Name[mw]:
                    id2Name[mw][key].append(tokens[0])
                else:
                    id2Name[mw][key] = [tokens[0]]
                if tokens[1] != '':
                    if tokens[1] in idRus2Name[mw]:
                        idRus2Name[mw][tokens[1]].append(tokens[0])
                    else:
                        idRus2Name[mw][tokens[1]] = [tokens[0]]
                if tokens[2] != '':
                    if tokens[2] in idIttf2Name[mw]:
                        idIttf2Name[mw][tokens[2]].append(tokens[0])
                    else:
                        idIttf2Name[mw][tokens[2]] = [tokens[0]]

            dd = mIdG
            d = mId
            if mw == 'women':
                dd = wIdG
                d = wId
            for k,v in id2Name[mw].items():
                name = None
                for e in v:
                    if e in dd:
                        name = e
                        break
                if (name is None):
                    newPlayers[mw][';'.join(v)] = mw[0] + str(maxV[mw])
                    maxV[mw] += 1
                else:
                    #print((k, v, name, d[dd[name]]))
                    for e in v:
                        if not (e in d[dd[name]]):
                            d[dd[name]].append(e)
                    #print(d[dd[name]])


    with open(filenameGlobalPlayersMen, 'w', encoding='utf-8') as fout:
        for k,v in sorted(mId.items(), key = lambda x: int(x[0][1:])):
            fout.write(k + '\t' + ';'.join(v) + '\n')

        for k,v in sorted(newPlayers['men'].items(), key = lambda x: int(x[1][1:])):
            fout.write(v + '\t' + k + '\n')

    with open(filenameGlobalPlayersWomen, 'w', encoding='utf-8') as fout:
        for k, v in sorted(wId.items(), key=lambda x: int(x[0][1:])):
            fout.write(k + '\t' + ';'.join(v) + '\n')

        for k, v in sorted(newPlayers['women'].items(), key=lambda x: int(x[1][1:])):
            fout.write(v + '\t' + k + '\n')


    (mIdG, mId2G) = readPlayersInv(filenameGlobalPlayersMen)
    (wIdG, wId2G) = readPlayersInv(filenameGlobalPlayersWomen)

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

if __name__ == "__main__":
    main()