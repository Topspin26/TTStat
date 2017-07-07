import os
import datetime
from Storages import *
from common import *


class LigaProChecker:
    @staticmethod
    def run():
        dirname = 'C:/Programming/SportPrognoseSystem/TTStat'

        playersDict = GlobalPlayersDict(dirname=dirname + '/')
        players = dict()
        for k, v in sorted(playersDict.id2names.items(), key=lambda x: x[0]):
            players[k] = Player(k, v, k[0])

        sources = list()
        #sources.append(['master_tour', dirname + '/prepared_data/master_tour/all_results.txt'])
        sources.append(['liga_pro', dirname + '/prepared_data/liga_pro/all_results.txt'])
        #sources.append(['challenger_series', dirname + '/prepared_data/challenger_series/all_results.txt'])
        #sources.append(['bkfon', dirname + '/prepared_data/bkfon/all_results.txt'])
        #sources.append(['local', dirname + '/prepared_data/local/kchr_results.txt'])
        #sources.append(['ittf', dirname + '/prepared_data/ittf/all_results.txt'])
        sources.append(['rttf', dirname + '/prepared_data/rttf/all_results.txt'])
        matchesStorage = MatchesStorage(sources)

        for match in matchesStorage.matches:
            for i in range(2):
                for e in match.ids[i]:
                    players[e].matches.append(match)

        rankingSources = list()
        rankingSources.append(['rttf', dirname + '/prepared_data/rttf/ranking_rttf.txt'])
        rankingStorage = RankingsStorage(rankingSources)

        checked = set()
        checked.add('Алексей Головинский')
        checked.add('Алан Заикин')
        checked.add('Александр Винокуров')
        checked.add('Дмитрий Овчаров')
        checked.add('Джун Мизутани')
        checked.add('Кирилл Скачков')
        checked.add('Елена Трошнева')
        checked.add('Фан Бо')
        checked.add('Янг Цзоу')
        checked.add('Федор Кузьмин')
        checked.add('Святослав Уразов')
        checked.add('Светлана Крекина')
        checked.add('Саади Исмаилов')
        checked.add('Яна Носкова')
        checked.add('Григорий Власов')
        checked.add('Филипп Куимов')
        checked.add('Шамиль Хайруллин')
        checked.add('Юрий Бесчастный')
        checked.add('Руслан Алчимбаев')
        checked.add('Светлана Мохначева')
        checked.add('Сергей Сарычев')
        checked.add('Михаил Гладышев')
        checked.add('Кирилл Швец')
        checked.add('Константин Чернов')
        checked.add('Кристина Казанцева')
        checked.add('Рамиль Мутыгуллин')
        checked.add('Павел Хрипуненко')
        checked.add('Мария Долгих')
        checked.add('Павел Тарутин')
        checked.add('Лев Волин')
        checked.add('Максим Стулий')
        checked.add('Елизавета Хлызова')
        checked.add('Ольга Куликова')
        checked.add('Татьяна Михайлова')
        checked.add('Виталий Мурзин')
        checked.add('Владимир Сидоренко')
        checked.add('MAJSTOROVIC Ilija')
        checked.add('MARINKOVIC Nikola')
        checked.add('Эльза Шибаева')
        checked.add('Вячеслав Буров')
        checked.add('Василий Дедов')
        checked.add('Артем Зимарин')
        checked.add('Артем Панченко')
        checked.add('Артем Семин')
        checked.add('Артур Абусев')
        checked.add('Бекташ Игорь')
        checked.add('Булхак Антон')
        checked.add('Валерия Щербатых')
        checked.add('Алексей Чернышков')
        checked.add('Александр Шибаев')
        checked.add('Андрей Гачина')
        checked.add('Екатерина Охотникова')
        checked.add('Елена Абаимова')
        checked.add('Егор Овчинников')
        checked.add('Михаил Ефимов')
        checked.add('Максим Гребнев')
        checked.add('Кирилл Воробьев')
        checked.add('Карен Мовсисян')
        checked.add('Карен Мовсисян')
        checked.add('Екатерина Гусева')
        checked.add('Екатерина Гусева')
        checked.add('Екатерина Голубева')
        checked.add('Екатерина Зиронова')
        checked.add('Екатерина Беспалова')
        checked.add('Вячеслав Карпенко')
        checked.add('Дарья Чернорай')
        checked.add('Денис Гаврилов')
        checked.add('Денис Ивонин')
        checked.add('Алина Кутузова')
        checked.add('Альфия Халикова')
        checked.add('Александр Резниченко')
        checked.add('Анна Россихина')
        checked.add('Сергей Полозов')
        checked.add('Илья Игошин')
        checked.add('Илья Березин')
        checked.add('Иван Таламанов')
        checked.add('Иван Степанов')
        checked.add('Анна Тихомирова')
        checked.add('Антонина Савельева')
        checked.add('Арсений Гусев')
        checked.add('Артем Двойников')
        checked.add('Василий Филатов')
        checked.add('Виктория Кандыбина')
        checked.add('Анна Иванникова')
        checked.add('Виктория Серебренникова')
        checked.add('Григорий Рементов')
        checked.add('Дарья Азаренкова')
        checked.add('Дарья Федорчукова')
        checked.add('Наталья Малинина')
        checked.add('Валерия Кудинова')
        checked.add('Ольга Шишмарева')
        checked.add('Родион Чмелев')
        checked.add('Валерия Морозова')
        checked.add('Анастасия Голубева')
        checked.add('Елисей Полуянов')
        checked.add('Владислав Самсонов')
        checked.add('Александр Воронов')
        checked.add('Андрей Бесшапошников')
        checked.add('Антон Хурцилава')
        checked.add('Виктория Лебедева')
        checked.add('Виктория Семенова')
        checked.add('Владислав Казаков')
        checked.add('Егор Шемелин')
        checked.add('Илья Анохин')
        checked.add('Константин Поликарпов')
        checked.add('Карпеш Роман')
        checked.add('Константин Носов')
        checked.add('Никита Мошков')

        for playerId, player in sorted(players.items(), key=lambda x: x[1].name):
            flLP = 0
            flRttf = 0
            for match in player.matches:
                if 'liga_pro' in match.sources:
                    flLP = 1
                if 'rttf' in match.sources or len(rankingStorage.getPlayerAllRankings(playerId, 'rttf')) > 0:
                    flRttf = 1
            if flLP == 1 and flRttf == 0 and player.name not in checked:
                print(player.names)
            if flLP == 1 and flRttf == 1 and player.name in checked:
                print(player.names)
                raise


def main():
    LigaProChecker.run()

if __name__ == "__main__":
    main()