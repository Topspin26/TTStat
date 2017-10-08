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

    #!!! Сейчас попадают коллизии из propingpong-а, т.к. у них НЕ записывается российский рейтинг (Тихонов Александр)

    for id, names in playersDict.id2names.items():
        r = rankingStorage.getPlayerAllRankings(id, 'ttfr')
        if len(r) == 0 or max([int(e[0]) for e in r.values()]) > 400 or \
                        names[0] == 'Бекташ Игорь' or \
                        names[0] == 'Николай Егоров' or \
                        names[0] == 'Меркушев Денис' or \
                        names[0] == 'Салогуб Дмитрий' or \
                        names[0] == 'Дулатов Марат' or \
                        names[0] == 'Духов Григорий' or \
                        names[0] == 'Ота Рики' or \
                        names[0] == 'Скребнев Александр' or \
                        names[0] == 'Минченко Сергей' or \
                        names[0] == 'Фомин Константин' or \
                        names[0] == 'Данилович Игорь' or \
                        names[0] == 'Кешишян Артур' or \
                        names[0] == 'Демид Любезнов' or \
                        names[0] == 'Старкова Лидия' or \
                        id == 'm16244' or \
                        id == 'm12038' or \
                        id == 'm9611' or \
                        id == 'm8983' or \
                        id == 'm2781': #Макаров Денис, Малышев Константин, Борисов Георгий, Киселев Виктор, Федоров Владислав
            if id != 'm9378' and id != 'm6453':
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