import os
from os import walk
from common import *
from Entity import *
from Storages import *

def main():

    rankingSources = []
    rankingSources.append(['ttfr', 'prepared_data/propingpong/ranking_rus.txt'])
    rankingStorage = RankingsStorage(rankingSources)

    playersDict = GlobalPlayersDict()

    id2names_filtered = dict()

    for id,names in playersDict.id2names.items():
        r = rankingStorage.getPlayerAllRankings(id, 'ttfr')
        if len(r) == 0 or max([int(e[0]) for e in r.values()]) > 400 or names[0] == 'Бекташ Игорь':
            id2names_filtered[id] = names
    with open('prepared_data/players_men_filtered.txt', 'w', encoding='utf-8') as fout_men, \
         open('prepared_data/players_women_filtered.txt', 'w', encoding='utf-8') as fout_women:
        for id,names in sorted(id2names_filtered.items(), key=lambda x: int(x[0][1:])):
            if id[0] == 'm':
                fout_men.write(id + '\t' + ';'.join(names) + '\n')
            else:
                fout_women.write(id + '\t' + ';'.join(names) + '\n')

if __name__ == "__main__":
    main()