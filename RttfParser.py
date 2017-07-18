import datetime as datetime
import random
import os
from os import walk
from bs4 import BeautifulSoup
from Logger import Logger


class RttfParser:

    @staticmethod
    def run(logger=Logger()):
        print('RttfParser')
        logger.print('RttfParser')
        dirname = 'data/rttf/tournaments/'
        dirnameOut = 'data/rttf/results_new/'
        for f in walk(dirname):
            for fd in f[1]:
                logger.print(fd)
                for ff in walk(dirname + fd):
                    for filename in ff[2]:
                        logger.print(filename)

                        sKey = filename[:-4]
                        if os.path.exists(dirnameOut + fd + '/' + sKey + '.txt') and \
                                os.path.exists(dirnameOut + fd + '/' + sKey + '_rankings.txt'):
                            continue
                        _, lines = RttfParser.parse(dirname + fd + '/' + filename)
                        logger.print(sKey)
                        logger.print(lines['games'])
                        logger.print(lines['rankings'])
                        if not os.path.exists(dirnameOut + fd):
                            os.mkdir(dirnameOut + fd)
                        with open(dirnameOut + fd + '/' + sKey + '.txt', 'w', encoding='utf-8') as fout:
                            fout.write(lines['games'])
                        with open(dirnameOut + fd + '/' + sKey + '_rankings.txt', 'w', encoding='utf-8') as fout:
                            fout.write(lines['rankings'])

    @staticmethod
    def parse(filename):
        soup = BeautifulSoup(open(filename, encoding='utf-8').read(), "lxml")
        table = soup.find(class_='games')
        trs = table.find_all('tr')
        lines = dict()
        lines['games'] = list()

        dt = filename.split('/')[-2]
        compId = filename.split('/')[-1].split('_')[0]
        compName = filename.split('_', 1)[-1][:-4]

        for tr in trs:
            tds = tr.find_all('td')

            name1 = name2 = ''
            score = ''
            for i, td in enumerate(tds):
                if i == 0:
                    name1 = td.find('a').getText().strip()
                    name1 += ';' + td.find('a').get('href').split('/')[-1]
                elif i == 1 or i == 3:
                    score += td.getText().replace('&nbsp;', '').strip()
                elif i == 2:
                    score += '-'
                else:
                    name2 = td.find('a').getText().strip()
                    name2 += ';' + td.find('a').get('href').split('/')[-1]
            lines['games'].append('\t'.join([dt, compName, name1, name2, score]))

        lines['rankings'] = list()

        table = soup.find(class_='players')
        trs = table.find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            name = tds[1].find('a').getText().strip()
            name += ';' + tds[1].find('a').get('href').split('/')[-1]
            rank = tds[3].getText().strip()
            drank = tds[4].getText().strip()
            lines['rankings'].append('\t'.join([dt, compName, name, rank, drank]))

        lines['games'] = '\n'.join(lines['games'])
        lines['rankings'] = '\n'.join(lines['rankings'])
        return compId + '_' + compName, lines


def main():
    RttfParser.run(logger=Logger('RttfParser.txt'))

if __name__ == "__main__":
    main()