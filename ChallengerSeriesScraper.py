import time
import requests
from bs4 import BeautifulSoup
import os
from Logger import Logger


class ChallengerSeriesScraper:
    @staticmethod
    def run(logger=Logger()):
        print('ChallengerSeriesScraper')
        logger.print('ChallengerSeriesScraper')
        url = 'http://challengerseries.net/content/results'
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")

        arr = soup.find(id='headselect').find_all('option')
        ids = []
        for e in arr:
            logger.print(e)
            logger.print(e.get('value'), e.text)
            ids.append([e.get('value'), e.text])

        ids.reverse()

        j = 0
        for id, dt in ids:
            startDate = dt[-4:] + '-' + dt[3:5] + '-' + dt[:2]
            filename = 'data/challenger_series/results_raw/' + startDate + '_' + id + '.txt'
            if not os.path.exists(filename):
                break
            j += 1
        j = max(j - 2, 0)

        logger.print(len(ids), j)

        # ids = [['1035', '27.02. - 28.02.2017']]
        for id, dt in ids[j:]:
            logger.print([id, dt])
            ChallengerSeriesScraper.scrap(url + '?q=node/' + id, id, dt)
            time.sleep(2)

    @staticmethod
    def scrap(url, id, dts):
        startDate = dts[-4:] + '-' + dts[3:5] + '-' + dts[:2]
        filename = 'data/challenger_series/results_raw/' + startDate + '_' + id + '.txt'

        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(str(soup))


def main():
    ChallengerSeriesScraper.run(logger=Logger('ChallengerSeriesScraper.txt'))

if __name__ == "__main__":
    main()