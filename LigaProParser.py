import time
import datetime as datetime
import random
import os
from os import walk
from bs4 import BeautifulSoup
from Logger import Logger

class LigaProParser:

    @staticmethod
    def run(logger=Logger()):
        print('LigaProParser')
        logger.print('LigaProParser')
        for f in walk('data/liga_pro/tours'):
            for ff in sorted(f[2]):
                logger.print(ff)
                sKey, lines = LigaProParser.parse('data/liga_pro/tours/' + ff, logger)
                logger.print(sKey)
                with open('data/liga_pro/results/' + sKey + '.txt', 'w', encoding='utf-8') as fout:
                    fout.write(lines)
                '''
                for e1, e2 in zip(c[ff.split('_')[1][:-4]], s):
                    e1 = e1.replace('Бурдин А', 'Бурдин Ал-й').strip()
                    e1 = e1.replace('Медведев С;59', 'Медведев С;256')
                    e1 = e1.replace('Филатов В;104', 'Филатов В;231')
                    e2 = e2.strip()
                    if e1 != e2:
                        print(e1)
                        print(e2)
                        print()
                        #return
                '''

    @staticmethod
    def parse(filename, logger):
        tid = filename.split('_')[-1][:-4]
        soup = BeautifulSoup(open(filename, encoding='utf-8').read(), "lxml")

        compName = soup.h1.getText()
#        print(compName)
        dt = soup.find_all(class_='day')[0].getText()
#        print(dt)
        st = soup.find_all(class_='day')[1].getText()
#        print(st)
        place = ''
        try:
            descs = soup.find_all('div', class_="desc")
            if len(descs) == 3:
                place = descs[1].find('div', class_="desc-item").find('a').getText()
            else:
                place = descs[0].find('div', class_="desc-item").find('a').getText()
        except:
            logger.print('no place')
            pass
#        print(place)
        monthname2Num = {'Янв':1,'Фев':2,'Мар':3,'Апр':4,'Май':5,'Мая':5,'Июн':6,'Июня':6,
                         'Июл':7,'Июля':7,'Авг':8,'Сен':9,'Окт':10,'Ноя':11,'Дек':12}
        dt = dt.split(' ')[2] + '-' + str(monthname2Num[dt.split(' ')[1]]).zfill(2) + '-' + dt.split(' ')[0].zfill(2)
        compInfo = compName + ';' + place + ';' + st
#        print([dt, compInfo])
        lines2 = []
        trs = soup.find('div', class_='tournament-info').find('table', class_="games_list").\
                   findChildren('tr', recursive=0)
        for tr in trs[1:]:
            tds = tr.findChildren('td', class_='center')
            if len(tds) == 1:
                stage = tds[0].getText().replace('<b>', '').replace('</b>', '').strip()
                #print(stage)
            else:
                s = tr.find('td').getText()
                tt = s#.split('>')[1][:5]
#                print(tt)

                s = str(tr.find('td', class_="right").contents[0])
                pl1Id = s.split('">')[0].split('/')[1]
                pl1Name = s.split('">')[1].split('<')[0]
#                print(pl1Id, pl1Name)

                s = str(tr.find_all('td', class_="left")[-1].contents[0])
                pl2Id = s.split('">')[0].split('/')[1]
                pl2Name = s.split('">')[1].split('<')[0]
#                print(pl2Id, pl2Name)

                r1 = tr.find_all('td', class_="rating")[0].contents[0].getText()
                r2 = tr.find_all('td', class_="rating")[1].contents[0].getText()
#                print(r1, r2)
                try:
                    dr1 = tr.find_all('td', class_="rating")[0].contents[2].getText()
                    dr2 = tr.find_all('td', class_="rating")[1].contents[2].getText()
                except:
                    dr1 = '0'
                    dr2 = '0'
                    logger.print(pl1Name, pl2Name, 'wrong dr')
#                print(dr1, dr2)

                try:
                    score = str(tr.find('td', class_="score").find_all('td')[1].contents[0])  # .getText()
#                    print(score)
                    gameId = score.split('">')[0].split('/')[1]
                    score = score.split('>')[1].split('<')[0]
#                    print(gameId, score)
                    pointsScore = str(tr.find('td', class_="score").contents[2].getText())
#                    print(pointsScore)
                except:
                    score = ''
                    gameId = ''
                    pointsScore = ''
                    logger.print('wrong score')

                lines2.append('\t'.join([dt, tt, compInfo, gameId, stage,
                                         pl1Name + ';' + pl1Id, r1, dr1,
                                         pl2Name + ';' + pl2Id, r2, dr2,
                                         score, pointsScore]))
                #print([dt, tt, compInfo, gameId, stage, pl1Name + ';' + pl1Id, r1, dr1, pl2Name + ';' + pl2Id, r2, dr2, score, pointsScore])
                #print()

        return (dt + '_' + str(tid) + '_' + compName), '\n'.join(lines2)
#        filename = 'data/liga_pro/results/' + dt + '_' + str(tid) + '_' + compName + '.txt'
#        with open(filename, 'w', encoding = 'utf-8') as fout:
#            for line in lines2:
#                fout.write(line + '\n')
#        return 0


def main():
    LigaProParser.run(logger=Logger('LigaProParser.txt'))

if __name__ == "__main__":
    main()