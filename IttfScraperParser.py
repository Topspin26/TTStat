import time
import datetime as datetime
import random
import re
import os
from os import walk
import requests
from bs4 import BeautifulSoup


class IttfScraper:
    @staticmethod
    def scrap(url):
        result = requests.get(url)
        if result.ok is False:
            return 1

        soup = BeautifulSoup(result.content, "lxml")
        return str(soup)


class IttfParser:
    @staticmethod
    def parse(s):
        flPage = 0
        soup = BeautifulSoup(s, "lxml")
        trs = soup.select('table[bordercolor="#000080"]')[0].find_all('tr')
        numCols = 6
        matches = dict()
        match = []
        for tr in trs:
            tds = tr.find_all('td')
            for i, td in enumerate(tds):
                tokens = str(td).strip().replace('\t', '').replace('\n', '').replace('\r', '').split('<br/>')
                if i % numCols == 1 or i % numCols == 3:
                    tokensNew = []
                    for e in tokens:
                        if len(re.sub('<[^<]+?>', '', e).strip()) > 0:
                            tokensNew.append(e)
                            result = re.search('P_ID=([^&]*)&', e)
                            tokensNew.append(result.group(1))
                    tokens = tokensNew
                tokens = [re.sub('<[^<]+?>', '', e).strip() for e in tokens]
                match.append(tokens)
                if i % numCols == 5:
                    dt = match[0][-1]
                    try:
                        arr = dt.split(' ')[-1].split('/')
                        dt = arr[2] + '-' + arr[1].zfill(2) + '-' + arr[0].zfill(2)
                    except:
                        dt = 'error_' + dt.replace('/', '_').replace('\\', '_')
                    if not dt in matches:
                        matches[dt] = []
                    matches[dt].append([';'.join(e) for e in match])
#                    print(match)
                    match = []

        for e in matches.items():
            try:
                rows = []
                flChange = 0
                if os.path.exists('data/ittf/results/' + e[0] + '.txt'):
                    with open('data/ittf/results/' + e[0] + '.txt', encoding = 'utf-8') as fin:
                        for line in fin:
                            rows.append(line.strip().split('\t'))
                    for s in e[1]:
                        fl = 0
                        for ir,row in enumerate(rows):
                            if row[0] == s[0] and row[1] == s[1] and row[3] == s[3]:
                                if '\t'.join(row) != '\t'.join(s):
                                    print('CHANGE')
                                    print(row)
                                    print(s)
                                    rows[ir] = s
                                    flChange = 1
                                fl = 1
                                break
                        if fl == 0:
                            print('NEW')
                            print(s)
                            flChange = 1
                            rows.append(s)
                else:
                    flChange = 1
                    rows = e[1]
                if flChange == 1:
                    flPage = 1
                    with open('data/ittf/results/' + e[0] + '.txt', 'w', encoding='utf-8') as fout:
                        for s in rows:
                            fout.write('\t'.join(s) + '\n')
            except Exception as ex:
                print(str(ex))
        return flPage

    @staticmethod
    def run(pages=list(range(1, 101))):
        url = 'http://www.old.ittf.com/competitions/matches_per_player_all.asp?P_ID=&Formrnd64_Page='
        unchanged = 0

        for page in pages:
            print([page, unchanged])
            if unchanged == 20:
                break
            flPage = IttfParser.parse(IttfScraper.scrap(url + str(page)))
            if flPage == 1:
                unchanged = 0
            else:
                unchanged += 1


def main():
    IttfParser.run(list(range(1, 101)))


if __name__ == "__main__":
    main()