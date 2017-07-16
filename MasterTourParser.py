import time
import datetime as datetime
import random
import os
from os import walk
from common import *
from bs4 import BeautifulSoup
from Logger import Logger


class MasterTourParser:

    @staticmethod
    def run(logger=Logger()):
        print('MasterTourParser')
        logger.print('MasterTourParser')
        for f in walk('data/master_tour/tournaments'):
            for ff in sorted(f[2]):
                logger.print(ff)
                sKey, lines = MasterTourParser.parse('data/master_tour/tournaments/' + ff, logger)
                logger.print(sKey)
                with open('data/master_tour/results/' + sKey + '.txt', 'w', encoding='utf-8') as fout:
                    fout.write(lines)

    @staticmethod
    def parse(filename, logger):
        soup = BeautifulSoup(open(filename, encoding='utf-8').read(), "lxml")

        lines2 = []
        trs = soup.find(class_='table striped table-100').find_all('tr')
        for tr in trs:
            if tr.find(class_='sheduleTableSeparator'):
                sdt = tr.find(class_='sheduleTableSeparator').text
                dt = datetime.datetime.strptime(sdt, "%d.%m.%Y").date().strftime("%Y-%m-%d")
            else:
                tds = tr.find_all('td')

                tt = tds[0].text
                p1 = tds[2].find('a').text
                p2 = tds[3].find('a').text
                sets_score = tds[5].text
                points_score = tds[4].text
                stage = tds[6].text
#                print(tt, p1, p2, sets_score, points_score)
                lines2.append('\t'.join([dt, tt, stage, p1, p2, sets_score, points_score]))

        tid = filename.split('/')[-1][:-4]
        return tid, '\n'.join(lines2)


def main():
    MasterTourParser.run(logger=Logger('MasterTourParser.txt'))

if __name__ == "__main__":
    main()