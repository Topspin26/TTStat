import requests
from bs4 import BeautifulSoup
from os import walk
from Logger import Logger
import time

class LigaProScraper:
    @staticmethod
    def run(logger=Logger(), mode='tours'):
        print('LigaProScraper_' + mode)
        logger.print('LigaProScraper_' + mode)
        curId = 1
        for f in walk('data/liga_pro/' + mode):
            for ff in f[2]:
                curId = max(curId, int(ff.split('_')[1][:-4]))
        curId = max(1, curId - 4) if mode == 'tours' else max(1, curId - 200)
        logger.print(curId)
        fl = 0
        for tid in range(curId, 15000):
            #if tid % 2 == 0:
            #    time.sleep(1)
            logger.print(tid)
            tfl = LigaProScraper.scrap(tid, mode=mode)
            fl = (fl + 1) if tfl == 1 else 0
            if fl == 4 and mode == 'tours' or fl == 100 and mode == 'games':
                break

    @staticmethod
    def scrap(tid, mode):
        url = 'http://tt-liga.pro/' + mode + '/' + str(tid)

        result = requests.get(url)
        if result.ok is False:
            return 1

        soup = BeautifulSoup(result.content, "lxml")

    #    if not os.path.exists('data/liga_pro/tours/' + str(tid)):
    #        os.mkdir('data/liga_pro/tours/' + str(tid))
        filename = 'data/liga_pro/' + mode + '/' + mode + '_' + str(tid) + '.txt'
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(str(soup))
        return 0

def main():
    LigaProScraper.run(logger=Logger('LigaProScraper_tours.txt'), mode='tours')
    LigaProScraper.run(logger=Logger('LigaProScraper_games.txt'), mode='games')

if __name__ == "__main__":
    main()