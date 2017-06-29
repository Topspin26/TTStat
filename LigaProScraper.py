import requests
from bs4 import BeautifulSoup
from os import walk


class LigaProScraper:
    @staticmethod
    def run():
        curId = 1
        for f in walk('data/liga_pro/tours'):
            for ff in f[2]:
                curId = max(curId, int(ff.split('_')[1][:-4]))
        curId = max(1, curId - 2)
        print(curId)
        fl = 0
        for tid in range(curId, 300):
            print(tid)
            tfl = LigaProScrapper.scrapp(tid)
            fl = (fl + 1) if tfl == 1 else 0
            if fl == 4:
                break
                #        break

    @staticmethod
    def scrap(tid):
        url = 'http://tt-liga.pro/tours/' + str(tid)

        result = requests.get(url)
        if result.ok is False:
            return 1

        soup = BeautifulSoup(result.content, "lxml")

    #    if not os.path.exists('data/liga_pro/tours/' + str(tid)):
    #        os.mkdir('data/liga_pro/tours/' + str(tid))
        filename = 'data/liga_pro/tours/tours_' + str(tid) + '.txt'
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(str(soup))
        return 0


def main():
    LigaProScraper.run()

if __name__ == "__main__":
    main()