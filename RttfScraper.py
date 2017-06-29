import os
import requests
from bs4 import BeautifulSoup


class RttfScraper:
    @staticmethod
    def run():
        for year in range(2017, 2018):
            for month in range(1, 13):
                RttfScraper.scrapMonth(str(year) + '-' + str(month).zfill(2))
                if year == 2017 and month == 6:
                    break

    @staticmethod
    def scrapMonth(month):
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
            print([s, href])

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
    RttfScraper.run()

if __name__ == "__main__":
    main()