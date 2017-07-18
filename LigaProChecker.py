import os
import datetime
from Storages import *
from common import *
from Logger import Logger


class LigaProChecker:
    @staticmethod
    def run(logger=Logger()):
        print('LigaProChecker')
        logger.print('LigaProChecker')
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
        rankingSources.append(['ttfr', dirname + '/prepared_data/propingpong/ranking_rus.txt'])
        rankingStorage = RankingsStorage(rankingSources)

        checkedRttf = set()
        checkedRttf.add('Алексей Головинский')
        checkedRttf.add('Алан Заикин')
        checkedRttf.add('Александр Винокуров')
        checkedRttf.add('Дмитрий Овчаров')
        checkedRttf.add('Джун Мизутани')
        checkedRttf.add('Кирилл Скачков')
        checkedRttf.add('Елена Трошнева')
        checkedRttf.add('Фан Бо')
        checkedRttf.add('Янг Цзоу')
        checkedRttf.add('Федор Кузьмин')
        checkedRttf.add('Святослав Уразов')
        checkedRttf.add('Светлана Крекина')
        checkedRttf.add('Саади Исмаилов')
        checkedRttf.add('Яна Носкова')
        checkedRttf.add('Григорий Власов')
        checkedRttf.add('Филипп Куимов')
        checkedRttf.add('Шамиль Хайруллин')
        checkedRttf.add('Юрий Бесчастный')
        checkedRttf.add('Руслан Алчимбаев')
        checkedRttf.add('Светлана Мохначева')
        checkedRttf.add('Сергей Сарычев')
        checkedRttf.add('Михаил Гладышев')
        checkedRttf.add('Кирилл Швец')
        checkedRttf.add('Константин Чернов')
        checkedRttf.add('Кристина Казанцева')
        checkedRttf.add('Рамиль Мутыгуллин')
        checkedRttf.add('Павел Хрипуненко')
        checkedRttf.add('Мария Долгих')
        checkedRttf.add('Павел Тарутин')
        checkedRttf.add('Лев Волин')
        checkedRttf.add('Максим Стулий')
        checkedRttf.add('Елизавета Хлызова')
        checkedRttf.add('Ольга Куликова')
        checkedRttf.add('Татьяна Михайлова')
        checkedRttf.add('Виталий Мурзин')
        checkedRttf.add('Владимир Сидоренко')
        checkedRttf.add('MAJSTOROVIC Ilija')
        checkedRttf.add('MARINKOVIC Nikola')
        checkedRttf.add('Эльза Шибаева')
        checkedRttf.add('Вячеслав Буров')
        checkedRttf.add('Василий Дедов')
        checkedRttf.add('Артем Зимарин')
        checkedRttf.add('Артем Панченко')
        checkedRttf.add('Артем Семин')
        checkedRttf.add('Артур Абусев')
        checkedRttf.add('Бекташ Игорь')
        checkedRttf.add('Булхак Антон')
        checkedRttf.add('Валерия Щербатых')
        checkedRttf.add('Алексей Чернышков')
        checkedRttf.add('Александр Шибаев')
        checkedRttf.add('Андрей Гачина')
        checkedRttf.add('Екатерина Охотникова')
        checkedRttf.add('Елена Абаимова')
        checkedRttf.add('Егор Овчинников')
        checkedRttf.add('Михаил Ефимов')
        checkedRttf.add('Максим Гребнев')
        checkedRttf.add('Кирилл Воробьев')
        checkedRttf.add('Карен Мовсисян')
        checkedRttf.add('Карен Мовсисян')
        checkedRttf.add('Екатерина Гусева')
        checkedRttf.add('Екатерина Гусева')
        checkedRttf.add('Екатерина Голубева')
        checkedRttf.add('Екатерина Зиронова')
        checkedRttf.add('Екатерина Беспалова')
        checkedRttf.add('Вячеслав Карпенко')
        checkedRttf.add('Дарья Чернорай')
        checkedRttf.add('Денис Гаврилов')
        checkedRttf.add('Денис Ивонин')
        checkedRttf.add('Алина Кутузова')
        checkedRttf.add('Альфия Халикова')
        checkedRttf.add('Александр Резниченко')
        checkedRttf.add('Анна Россихина')
        checkedRttf.add('Сергей Полозов')
        checkedRttf.add('Илья Игошин')
        checkedRttf.add('Илья Березин')
        checkedRttf.add('Иван Таламанов')
        checkedRttf.add('Иван Степанов')
        checkedRttf.add('Анна Тихомирова')
        checkedRttf.add('Антонина Савельева')
        checkedRttf.add('Арсений Гусев')
        checkedRttf.add('Артем Двойников')
        checkedRttf.add('Василий Филатов')
        checkedRttf.add('Виктория Кандыбина')
        checkedRttf.add('Анна Иванникова')
        checkedRttf.add('Виктория Серебренникова')
        checkedRttf.add('Григорий Рементов')
        checkedRttf.add('Дарья Азаренкова')
        checkedRttf.add('Дарья Федорчукова')
        checkedRttf.add('Наталья Малинина')
        checkedRttf.add('Валерия Кудинова')
        checkedRttf.add('Ольга Шишмарева')
        checkedRttf.add('Родион Чмелев')
        checkedRttf.add('Валерия Морозова')
        checkedRttf.add('Анастасия Голубева')
        checkedRttf.add('Елисей Полуянов')
        checkedRttf.add('Владислав Самсонов')
        checkedRttf.add('Александр Воронов')
        checkedRttf.add('Андрей Бесшапошников')
        checkedRttf.add('Антон Хурцилава')
        checkedRttf.add('Виктория Лебедева')
        checkedRttf.add('Виктория Семенова')
        checkedRttf.add('Владислав Казаков')
        checkedRttf.add('Егор Шемелин')
        checkedRttf.add('Илья Анохин')
        checkedRttf.add('Константин Поликарпов')
        checkedRttf.add('Карпеш Роман')
        checkedRttf.add('Константин Носов')
        checkedRttf.add('Никита Мошков')
        checkedRttf.add('Валерия Щетинкина')
        checkedRttf.add('Евгений Груздов')
        checkedRttf.add('Павел Перов')

        checkedTtfr = set()
        checkedTtfr.add('Григорий Парсегов')
        checkedTtfr.add('Елена Чунихина')
        checkedTtfr.add('Юрий Меркушин')
        checkedTtfr.add('Феликс Каплан')
        checkedTtfr.add('Кует Нгуен')
        checkedTtfr.add('MAJSTOROVIC Ilija')
        checkedTtfr.add('Саркис Моклозян')
        checkedTtfr.add('Семен Комиссаров')
        checkedTtfr.add('Айк Луликян')
        checkedTtfr.add('Георгий Прикащенков')
        checkedTtfr.add('Евгений Масокин')
        checkedTtfr.add('Жасур Худайбердиев')
        checkedTtfr.add('Игорь Кример')
        checkedTtfr.add('Илья Корогодский')
        checkedTtfr.add('Марсель Сафиулин')
        checkedTtfr.add('KOLESAU Andrei')
        checkedTtfr.add('Александр Екжанов')
        checkedTtfr.add('Александр Корепанов')
        checkedTtfr.add('Андрей Бабенко')
        checkedTtfr.add('Владимир Немашкало')
        checkedTtfr.add('Тимофей Разинков')
        checkedTtfr.add('Дмитрий Разинков')
        checkedTtfr.add('Игорь Авдеев')
        checkedTtfr.add('Николай Барабаш')
        checkedTtfr.add('Мухаммед Ахмеджанов')
        checkedTtfr.add('Михаил Минченков')
        checkedTtfr.add('Максим Пищанский')
        checkedTtfr.add('Анатолий Нам')
        checkedTtfr.add('Виталий Базилевский')
        checkedTtfr.add('Иван Мошков')
        checkedTtfr.add('Юрий Лбов')
        checkedTtfr.add('Филипп Ерошов')
        checkedTtfr.add('Сергей Шихалеев')
        checkedTtfr.add('Сергей Хомутов')
        checkedTtfr.add('Сергей Симонов')
        checkedTtfr.add('Сергей Курдюков')
        checkedTtfr.add('Сергей Гречаников')
        checkedTtfr.add('Рустам Нарзикулов')
        checkedTtfr.add('Сергей Огай')
        checkedTtfr.add('Андрей Сырцов')
        checkedTtfr.add('Константин Климкин')
        checkedTtfr.add('Сергей Плешивцев')
        checkedTtfr.add('Олег Сухарьков')
        checkedTtfr.add('Константин Поликарпов')
        checkedTtfr.add('Владимир Ашихмин')
        checkedTtfr.add('Алик Гиревенков')
        checkedTtfr.add('Алексей Лобанов')
        checkedTtfr.add('Алексей Свиридов')
        checkedTtfr.add('Андрей Овчинников')
        checkedTtfr.add('Василий Ермилин')
        checkedTtfr.add('Дмитрий Здобнов')
        checkedTtfr.add('Дмитрий Игнатьев')
        checkedTtfr.add('Илья Новиков')
        checkedTtfr.add('Сергей Воробьев')
        checkedTtfr.add('Дмитрий Осипов')
        checkedTtfr.add('Иванов Виктор')
        checkedTtfr.add('Крылов Александр')
        checkedTtfr.add('Олег Попов')

        for playerId, player in sorted(players.items(), key=lambda x: x[1].name):
            flLP = 0
            flRttf = 0
            flTtfr = 0
            if len(rankingStorage.getPlayerAllRankings(playerId, 'rttf')) > 0:
                flRttf = 1
            if len(rankingStorage.getPlayerAllRankings(playerId, 'ttfr')) > 0:
                flTtfr = 1
            for match in player.matches:
                if 'liga_pro' in match.sources:
                    flLP = 1
                if 'rttf' in match.sources:
                    flRttf = 1
            if flLP == 1 and flRttf == 0 and player.name not in checkedRttf:
                logger.print('rttf', player.names)
            if flLP == 1 and flRttf == 1 and player.name in checkedRttf:
                logger.print('rttf', player.names)
                raise

            if flLP == 1 and flTtfr == 0 and player.name not in checkedTtfr:
                logger.print('ttfr', player.names)
            if flLP == 1 and flTtfr == 1 and player.name in checkedTtfr:
                logger.print('ttfr', player.names)
                raise
            if playerId == 'm16244':
                assert rankingStorage.getPlayerAllRankings(playerId, 'ttfr')['2017-06-01'][0] == '333'


def main():
    LigaProChecker.run(logger=Logger('LigaProChecker.txt'))

if __name__ == "__main__":
    main()