import os
import requests
from bs4 import BeautifulSoup
import datetime
from Logger import Logger


class RttfScraper:
    @staticmethod
    def run(logger=Logger()):
        print('RttfScraper')
        logger.print('RttfScraper')
        for year in range(2017, datetime.datetime.now().year + 1):
            for month in range(1, 13):
                RttfScraper.scrapMonth(str(year) + '-' + str(month).zfill(2), logger)
                if year == datetime.datetime.now().year and month == datetime.datetime.now().month:
                    break

    @staticmethod
    def scrapMonth(month, logger):
        url = 'http://or.rttf.ru/tournaments/' + month
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")

        table = soup.find(class_='tournaments')
        hrs = table.find_all('a')
        sh = []
        for hr in hrs:
            s = hr.getText()
            href = hr.get('href')
            sh.append([s, href])
        for s, href in sh:
            dt = s[6:10] + '-' + s[3:5] + '-' + s[:2]
            dirname = 'data/rttf/tournaments/' + dt
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            logger.print([s, href])

            compId = href.split('/')[-1]
            compName = s.split(' ', 1)[-1].replace('"', '')
            filename = compId + '_' + compName + '.txt'
            if os.path.exists(dirname + '/' + filename):
                continue

            result = requests.get('http://or.rttf.ru/' + href)
            soup = BeautifulSoup(result.content, "lxml")
            with open(dirname + '/' + filename, 'w', encoding='utf-8') as fout:
                fout.write(str(soup))


def main():
    RttfScraper.run(logger=Logger('RttfScraper.txt'))

if __name__ == "__main__":
    main()