import datetime as datetime
import time
import requests
from bs4 import BeautifulSoup
from os import walk


class MasterTourScrapper:
    @staticmethod
    def run():
        curDate = '2013-01-03'
        for f in walk('data/master_tour/tournaments'):
            for ff in f[2]:
                curDate = max(curDate, ff[:-4])
        curDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() - datetime.timedelta(days=2)).strftime(
            "%Y-%m-%d")
        print(curDate)

        while True:
            tUrl = 'http://master-tour.pro/tournaments/' + curDate + '.html'
            print(tUrl + '\t', end='')
            fl = MasterTourScrapper.scrapp(curDate, tUrl)
            print(fl)
            if curDate == datetime.datetime.now().strftime("%Y-%m-%d"):
                break
            curDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)).strftime(
                "%Y-%m-%d")
            time.sleep(2)

    @staticmethod
    def scrapp(curDate, url):
        try:
            result = requests.get(url)
        except Exception as ex:
            print(ex)
            time.sleep(15)
            result = requests.get(url)

        if result.ok is False:
            return 1

        soup = BeautifulSoup(result.content, "lxml")

        filename = 'data/master_tour/tournaments/' + str(curDate) + '.txt'
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(str(soup))
        return 0


def main():
    MasterTourScrapper.run()

if __name__ == "__main__":
    main()