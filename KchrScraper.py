import requests
from bs4 import BeautifulSoup
from os import walk
from Logger import Logger
import time

class KchrScraper:
    @staticmethod
    def run(logger=Logger()):
        print('KchrScraper')
        logger.print('KchrScraper')
        for sex in [0, 1]:
            for season in ['2016-2017', '2017-2018']:
                for league in range(1, 7):
                    for tour in range(1, 6):
                        logger.print('{}_{}_{}_{}'.format(sex, league, tour, season))
                        KchrScraper.scrap(sex, league, tour, season)

    @staticmethod
    def scrap(sex, league, tour, season):
        url = 'http://kcr.ttfr.ru/results?Meeting[sex]={}&Meeting[league]={}&Meeting[tour]={}&Meeting[season]={}'.\
            format(sex, league, tour, season)

        last_str = None
        filename = 'data/kchr/{}_{}_{}_{}'.format(sex, league, tour, season)
        for page in range(1, 101):
            result = requests.get(url + '&page={}'.format(page))
            if result.ok is False:
                return 1

            soup = BeautifulSoup(result.content, "lxml")

            if str(soup).split('<title>Таблица Результатов</title>')[1].split('</table>\n')[0] == last_str:
                break
            with open(filename + '_{}'.format(page) + '.txt', 'w', encoding='utf-8') as fout:
                fout.write(str(soup))
            last_str = str(soup).split('<title>Таблица Результатов</title>')[1].split('</table>\n')[0]


def main():
    KchrScraper.run(logger=Logger('KchrScraper.txt'))

if __name__ == "__main__":
    main()