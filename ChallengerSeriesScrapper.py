import time
import requests
from bs4 import BeautifulSoup
import os


class ChallengerSeriesScrapper:
    @staticmethod
    def run():
        url = 'http://challengerseries.net/content/results'
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")

        arr = soup.find(id='headselect').find_all('option')
        ids = []
        for e in arr:
            print(e)
            print(e.get('value'), e.text)
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

        print(len(ids), j)

        # ids = [['1035', '27.02. - 28.02.2017']]
        for id, dt in ids[j:]:
            print([id, dt])
            ChallengerSeriesScrapper.scrapp(url + '?q=node/' + id, id, dt)
            time.sleep(2)

    @staticmethod
    def scrapp(url, id, dts):
        startDate = dts[-4:] + '-' + dts[3:5] + '-' + dts[:2]
        filename = 'data/challenger_series/results_raw/' + startDate + '_' + id + '.txt'

        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(str(soup))


def main():
    ChallengerSeriesScrapper.run()

if __name__ == "__main__":
    main()